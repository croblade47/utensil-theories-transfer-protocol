<#
.SYNOPSIS
  MeAgent: a personal, local-only agent that slowly learns your device habits and guesses what you will do next.

.DESCRIPTION
  Runs in a visible PowerShell window on Windows. Close the window or press Ctrl+C to stop; it saves on exit.
  It learns, and keeps everything only on this PC (default folder: %USERPROFILE%\MeAgent):
    - which app you use and for how long (sessions.csv, one row per app session)
    - when you are on the device (time per hour of the day; "idle" after 2 minutes without input)
    - how fast you type (keys per minute and words per minute, typing.csv)
    - your vocabulary (how often you type each word; word COUNTS only, never the order of what you typed)
    - your workflow (which app usually follows which, overall and by hour of day)
  Then it predicts the next app you will switch to, and keeps score of how often it is right.

  Privacy built in:
    - Nothing leaves the PC. No network calls.
    - While a password manager is in front, or the window title looks private (password, sign in, bank, payment,
      checkout, credential, verification code, incognito / InPrivate...), it records no words at all.
    - Digits are never recorded as words. Use -NoVocab to switch the vocabulary off completely.
    - -Forget deletes everything it has learned.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File .\MeAgent.ps1             # start learning (leave the window open)
  powershell -ExecutionPolicy Bypass -File .\MeAgent.ps1 -Report     # see what it has learned, and its guess right now
  powershell -ExecutionPolicy Bypass -File .\MeAgent.ps1 -NoVocab    # learn everything except words
  powershell -ExecutionPolicy Bypass -File .\MeAgent.ps1 -Install    # start automatically (minimized) at sign-in
  powershell -ExecutionPolicy Bypass -File .\MeAgent.ps1 -Uninstall  # stop starting automatically
  powershell -ExecutionPolicy Bypass -File .\MeAgent.ps1 -Forget     # delete everything it learned

  Author and owner: Garrett C. Gauthier. Written with Claude (Anthropic) in Claude Code, a tool the owner uses.
#>
[CmdletBinding()]
param(
    [switch]$Report,
    [switch]$Install,
    [switch]$Uninstall,
    [switch]$Forget,
    [switch]$NoVocab,
    [string]$DataDir = (Join-Path $env:USERPROFILE 'MeAgent'),
    [int]$IdleSeconds = 120
)

$ErrorActionPreference = 'Stop'
$StatePath   = Join-Path $DataDir 'state.json'
$SessionsCsv = Join-Path $DataDir 'sessions.csv'
$TypingCsv   = Join-Path $DataDir 'typing.csv'

$PrivateApps  = @('keepass', 'keepassxc', '1password', 'bitwarden', 'lastpass', 'dashlane', 'credentialuibroker', 'consent', 'logonui')
$PrivateTitle = 'password|passcode|passwort|sign ?in|log ?in|login|credential|bank|checkout|payment|credit card|vault|2fa|verification code|one-time code|private|incognito|inprivate'
$Stopwords = @('the','and','for','you','that','this','with','are','was','but','not','have','has','had','its','it''s','i''m','can','will','just','what','when','your','from','they','them','then','there','their','out','all','get','got','one','our','his','her','she','him','who','how','why','did','does','dont','don''t','about','would','could','should','been','were','into','some','more','like','also','than','only','very','too','any','yes','yeah','okay','ok')

Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
using System.Text;
public static class MeNative {
    [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint processId);
    [DllImport("user32.dll")] public static extern short GetAsyncKeyState(int vKey);
    [DllImport("user32.dll", CharSet = CharSet.Unicode)] public static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int count);
    [StructLayout(LayoutKind.Sequential)] public struct LASTINPUTINFO { public uint cbSize; public uint dwTime; }
    [DllImport("user32.dll")] public static extern bool GetLastInputInfo(ref LASTINPUTINFO info);
    public static uint IdleMs() {
        LASTINPUTINFO l = new LASTINPUTINFO();
        l.cbSize = (uint)Marshal.SizeOf(l);
        GetLastInputInfo(ref l);
        return unchecked((uint)Environment.TickCount - l.dwTime);
    }
    public static string Title(IntPtr hWnd) {
        StringBuilder sb = new StringBuilder(512);
        GetWindowText(hWnd, sb, 512);
        return sb.ToString();
    }
}
"@

# ----------------------------------------------------------------------------------------------------------------
# Memory (state.json)
# ----------------------------------------------------------------------------------------------------------------
function ConvertTo-Hashtable($obj) {
    $h = @{}
    if ($null -eq $obj) { return $h }
    foreach ($p in $obj.PSObject.Properties) { $h[$p.Name] = [double]$p.Value }
    return $h
}

function Read-State {
    $s = @{
        appSeconds = @{}; hourSeconds = @{}; transitions = @{}; transHour = @{}; vocab = @{}
        keys = 0; typingMinutes = 0; peakWpm = 0; predMade = 0; predHits = 0; runs = 0
        firstSeen = (Get-Date).ToString('s')
    }
    if (Test-Path $StatePath) {
        $j = Get-Content -Path $StatePath -Raw | ConvertFrom-Json
        foreach ($k in @('appSeconds', 'hourSeconds', 'transitions', 'transHour', 'vocab')) { $s[$k] = ConvertTo-Hashtable $j.$k }
        foreach ($k in @('keys', 'typingMinutes', 'peakWpm', 'predMade', 'predHits', 'runs')) {
            if ($null -ne $j.$k) { $s[$k] = [double]$j.$k }
        }
        if ($j.firstSeen) { $s.firstSeen = [string]$j.firstSeen }
    }
    return $s
}

function Save-State($s) {
    $tmp = "$StatePath.tmp"
    $s | ConvertTo-Json -Depth 4 -Compress | Set-Content -Path $tmp -Encoding UTF8
    Move-Item -Path $tmp -Destination $StatePath -Force
}

function Add-Count($table, [string]$key, [double]$n) {
    if ($table.ContainsKey($key)) { $table[$key] = [double]$table[$key] + $n } else { $table[$key] = $n }
}

# ----------------------------------------------------------------------------------------------------------------
# Prediction: which app usually comes next from this one (overall, plus double weight for this hour of the day)
# ----------------------------------------------------------------------------------------------------------------
function Get-Prediction($s, [string]$from, [int]$hour) {
    $scores = @{}
    foreach ($k in @($s.transitions.Keys)) {
        $p = $k -split '\|', 2
        if ($p[0] -eq $from) { Add-Count $scores $p[1] ([double]$s.transitions[$k]) }
    }
    foreach ($k in @($s.transHour.Keys)) {
        $p = $k -split '\|', 3
        if ($p[0] -eq $from -and $p[1] -eq [string]$hour) { Add-Count $scores $p[2] (2 * [double]$s.transHour[$k]) }
    }
    if ($scores.Count -eq 0) { return $null }
    $total = ($scores.Values | Measure-Object -Sum).Sum
    $best = $scores.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First 1
    return [pscustomobject]@{ App = $best.Key; Pct = [math]::Round(100 * $best.Value / $total) }
}

function Get-ForegroundApp {
    $h = [MeNative]::GetForegroundWindow()
    $procId = [uint32]0
    [void][MeNative]::GetWindowThreadProcessId($h, [ref]$procId)
    $app = 'unknown'
    try { $app = (Get-Process -Id $procId -ErrorAction Stop).ProcessName.ToLower() } catch { }
    return [pscustomobject]@{ App = $app; Title = [MeNative]::Title($h) }
}

# ----------------------------------------------------------------------------------------------------------------
# Report
# ----------------------------------------------------------------------------------------------------------------
function Show-Report {
    if (-not (Test-Path $StatePath)) { Write-Host "Nothing learned yet. Run MeAgent.ps1 (without -Report) and leave it open for a while."; return }
    $s = Read-State
    Write-Host ""
    Write-Host "=== MeAgent: what I have learned about you ===" -ForegroundColor Cyan
    Write-Host ("Learning since {0}, over {1} runs." -f $s.firstSeen, [int]$s.runs)

    Write-Host "`nWhere your time goes (hours):" -ForegroundColor Yellow
    $s.appSeconds.GetEnumerator() | Where-Object { $_.Key -ne 'idle' } | Sort-Object Value -Descending | Select-Object -First 12 |
        ForEach-Object { Write-Host ("  {0,-28} {1,7:N1}" -f $_.Key, ($_.Value / 3600)) }
    if ($s.appSeconds.ContainsKey('idle')) { Write-Host ("  {0,-28} {1,7:N1}" -f '(idle / away)', ($s.appSeconds['idle'] / 3600)) }

    Write-Host "`nWhen you are on the device (hour of day):" -ForegroundColor Yellow
    $max = 1
    foreach ($v in $s.hourSeconds.Values) { if ($v -gt $max) { $max = $v } }
    for ($h = 0; $h -lt 24; $h++) {
        $v = 0
        if ($s.hourSeconds.ContainsKey([string]$h)) { $v = $s.hourSeconds[[string]$h] }
        $bar = '#' * [int](30 * $v / $max)
        Write-Host ("  {0:00}:00  {1,-30} {2,6:N1} h" -f $h, $bar, ($v / 3600))
    }

    Write-Host "`nTyping:" -ForegroundColor Yellow
    if ($s.typingMinutes -gt 0) {
        Write-Host ("  Average {0:N0} words per minute while typing; fastest minute {1:N0} wpm; {2:N0} keys in total." -f (($s.keys / 5) / $s.typingMinutes), $s.peakWpm, $s.keys)
    } else { Write-Host "  Not enough typing yet." }

    Write-Host "`nYour words (most used, common words left out):" -ForegroundColor Yellow
    $top = $s.vocab.GetEnumerator() | Where-Object { $_.Key.Length -ge 3 -and $Stopwords -notcontains $_.Key } |
        Sort-Object Value -Descending | Select-Object -First 30
    if ($top) { Write-Host ("  " + (($top | ForEach-Object { "{0} ({1})" -f $_.Key, [int]$_.Value }) -join ', ')) }
    else { Write-Host "  None yet (or vocabulary is switched off)." }

    Write-Host "`nYour workflow (what usually comes next):" -ForegroundColor Yellow
    $s.transitions.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First 10 |
        ForEach-Object { $p = $_.Key -split '\|', 2; Write-Host ("  {0,-22} -> {1,-22} {2,5} times" -f $p[0], $p[1], [int]$_.Value) }

    Write-Host "`nHow well I predict you:" -ForegroundColor Yellow
    if ($s.predMade -gt 0) {
        Write-Host ("  Right {0} of {1} times ({2:N0}%)." -f [int]$s.predHits, [int]$s.predMade, (100 * $s.predHits / $s.predMade))
    } else { Write-Host "  No predictions checked yet." }

    $now = Get-ForegroundApp
    $guess = Get-Prediction $s $now.App (Get-Date).Hour
    if ($guess) { Write-Host ("`nRight now you are in {0}. My guess for your next app: {1} ({2}% sure)." -f $now.App, $guess.App, $guess.Pct) -ForegroundColor Green }
    Write-Host ""
}

# ----------------------------------------------------------------------------------------------------------------
# Install / uninstall / forget
# ----------------------------------------------------------------------------------------------------------------
$StartupCmd = Join-Path ([Environment]::GetFolderPath('Startup')) 'MeAgent.cmd'
if ($Install) {
    $self = $MyInvocation.MyCommand.Path
    $line = 'start "MeAgent" /min powershell -NoProfile -ExecutionPolicy Bypass -File "' + $self + '"'
    if ($NoVocab) { $line += ' -NoVocab' }
    Set-Content -Path $StartupCmd -Value $line -Encoding ASCII
    Write-Host "MeAgent will start (minimized, visible in the taskbar) each time you sign in. Remove it with -Uninstall."
    return
}
if ($Uninstall) {
    if (Test-Path $StartupCmd) { Remove-Item $StartupCmd -Force; Write-Host "MeAgent will no longer start at sign-in." }
    else { Write-Host "MeAgent was not set to start at sign-in." }
    return
}
if ($Forget) {
    $answer = Read-Host "Delete everything MeAgent has learned in $DataDir ? Type YES to confirm"
    if ($answer -eq 'YES') { Remove-Item -Path $DataDir -Recurse -Force -ErrorAction SilentlyContinue; Write-Host "Forgotten." }
    else { Write-Host "Nothing deleted." }
    return
}
if ($Report) { Show-Report; return }

# ----------------------------------------------------------------------------------------------------------------
# Learn (main loop)
# ----------------------------------------------------------------------------------------------------------------
New-Item -ItemType Directory -Path $DataDir -Force | Out-Null
if (-not (Test-Path $SessionsCsv)) { 'start,end,seconds,app' | Set-Content -Path $SessionsCsv -Encoding UTF8 }
if (-not (Test-Path $TypingCsv)) { 'minute,app,keys,wpm' | Set-Content -Path $TypingCsv -Encoding UTF8 }

$state = Read-State
$state.runs = [double]$state.runs + 1

# Keys watched: Backspace, Enter, Space, 0-9, A-Z, and punctuation keys. Only key counts and timing are kept,
# plus (unless -NoVocab, and never in private windows) completed letter-only words for the word counts.
$keyCodes = @(0x08, 0x0D, 0x20) + (0x30..0x39) + (0x41..0x5A) + (0xBA..0xC0) + (0xDB..0xDE)
$wasDown = @{}
foreach ($k in $keyCodes) { $wasDown[$k] = $false }

$word = New-Object System.Text.StringBuilder
$private = $false
$curApp = $null
$curStart = Get-Date
$lastRealApp = $null
$prediction = $null
$minuteKeys = 0
$minuteStart = Get-Date
$lastTick = Get-Date
$lastSave = Get-Date

$host.UI.RawUI.WindowTitle = 'MeAgent (learning) - close this window or press Ctrl+C to stop'
Write-Host "MeAgent is learning. Everything stays in $DataDir" -ForegroundColor Cyan
Write-Host "Close this window or press Ctrl+C to stop. Run with -Report to see what it has learned.`n"

try {
    while ($true) {
        # --- keys: count presses (typing speed) and collect words (vocabulary) ---
        foreach ($k in $keyCodes) {
            $isDown = ([MeNative]::GetAsyncKeyState($k) -band 0x8000) -ne 0
            if ($isDown -and -not $wasDown[$k]) {
                $minuteKeys++
                $state.keys = [double]$state.keys + 1
                if (-not $NoVocab -and -not $private) {
                    if ($k -ge 0x41 -and $k -le 0x5A) { [void]$word.Append([char]($k + 32)) }
                    elseif ($k -eq 0xDE) { [void]$word.Append("'") }
                    elseif ($k -eq 0x08) { if ($word.Length -gt 0) { [void]$word.Remove($word.Length - 1, 1) } }
                    else {
                        $w = $word.ToString().Trim("'")
                        if ($w.Length -ge 2 -and $w.Length -le 30) { Add-Count $state.vocab $w 1 }
                        [void]$word.Clear()
                    }
                } else { [void]$word.Clear() }
            }
            $wasDown[$k] = $isDown
        }

        $now = Get-Date

        # --- once a second: which app is in front, and is anyone there ---
        if (($now - $lastTick).TotalMilliseconds -ge 1000) {
            $lastTick = $now
            $fg = Get-ForegroundApp
            $app = $fg.App
            $private = ($PrivateApps -contains $app) -or ($fg.Title -match $PrivateTitle)
            if ($private) { [void]$word.Clear() }
            if ([MeNative]::IdleMs() -gt ($IdleSeconds * 1000)) { $app = 'idle' }

            Add-Count $state.appSeconds $app 1
            Add-Count $state.hourSeconds ([string]$now.Hour) 1

            if ($app -ne $curApp) {
                if ($null -ne $curApp) {
                    $secs = [int]($now - $curStart).TotalSeconds
                    Add-Content -Path $SessionsCsv -Value ("{0},{1},{2},{3}" -f $curStart.ToString('s'), $now.ToString('s'), $secs, $curApp)
                }
                if ($app -ne 'idle') {
                    $mark = ''
                    if ($null -ne $lastRealApp -and $app -ne $lastRealApp) {
                        Add-Count $state.transitions ("{0}|{1}" -f $lastRealApp, $app) 1
                        Add-Count $state.transHour ("{0}|{1}|{2}" -f $lastRealApp, $now.Hour, $app) 1
                        if ($prediction) {
                            $state.predMade = [double]$state.predMade + 1
                            if ($prediction.App -eq $app) { $state.predHits = [double]$state.predHits + 1; $mark = '  (I guessed it: HIT)' }
                            else { $mark = "  (I guessed $($prediction.App): miss)" }
                        }
                    }
                    $lastRealApp = $app
                    $prediction = Get-Prediction $state $app $now.Hour
                    $next = ''
                    if ($prediction) { $next = "   next guess: $($prediction.App) ($($prediction.Pct)%)" }
                    $score = ''
                    if ($state.predMade -gt 0) { $score = "   score {0:N0}%" -f (100 * $state.predHits / $state.predMade) }
                    Write-Host ("[{0}] {1}{2}{3}{4}" -f $now.ToString('HH:mm'), $app, $mark, $next, $score)
                }
                $curApp = $app
                $curStart = $now
            }
        }

        # --- once a minute: typing speed ---
        if (($now - $minuteStart).TotalSeconds -ge 60) {
            if ($minuteKeys -gt 0) {
                $wpm = [math]::Round($minuteKeys / 5, 1)
                $state.typingMinutes = [double]$state.typingMinutes + 1
                if ($wpm -gt $state.peakWpm) { $state.peakWpm = $wpm }
                Add-Content -Path $TypingCsv -Value ("{0},{1},{2},{3}" -f $minuteStart.ToString('s'), $curApp, $minuteKeys, $wpm)
            }
            $minuteKeys = 0
            $minuteStart = $now
        }

        # --- once a minute: save what was learned ---
        if (($now - $lastSave).TotalSeconds -ge 60) { Save-State $state; $lastSave = $now }

        Start-Sleep -Milliseconds 30
    }
}
finally {
    $end = Get-Date
    if ($null -ne $curApp) {
        Add-Content -Path $SessionsCsv -Value ("{0},{1},{2},{3}" -f $curStart.ToString('s'), $end.ToString('s'), [int]($end - $curStart).TotalSeconds, $curApp)
    }
    Save-State $state
    Write-Host "`nMeAgent saved what it learned. See it with: MeAgent.ps1 -Report" -ForegroundColor Cyan
}
