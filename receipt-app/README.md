# Door Receipts

A quick receipt and shift-tracking app for door-to-door work.

**On the phone (works with no internet):**
- 📷 Photo of the house, address and description (type or tap 🎤 to talk), amount, how they paid
- ✍️ Customer prints their name and signs on the screen; email is optional
- ✖ One-tap "Said No", "Not Home" and "Come Back Later" logs (with photo + reason), so the AI can compare yes-houses and no-houses
- ▶ Start / ■ End Shift: tracks where you were, when, and for how long (GPS)
- End of shift: summary, printable report with every receipt, CSV download

**On the laptop (the "hub"):**
- Plug in the phone → it links up automatically → tap **Sync**
- Printable shift reports (every receipt, photo and signature) → Print / Save as PDF
- `earnings.xlsx` spreadsheet: receipts, shifts, weekly hours & money, and a **Tax Estimate** sheet (self-employment tax, federal, state, mileage deduction, how much to set aside, take-home per hour)
- Survey emails with a copy of the receipt, sent a few days after the visit
- AI coach report: stats by day, hour, street and "no" reason, plus every house photo labeled SALE / NO / NOT-HOME, ready to upload to an AI chat

Everything stays on your phone and laptop. Nothing goes to the internet unless you send survey emails or press "Ask Claude".

---

## 1. Laptop setup (once)

1. Install **Python 3** (python.org — on Windows tick "Add Python to PATH").
2. Install **Android platform-tools** (this gives the laptop the `adb` command that talks to the phone over USB):
   - Windows: download "SDK Platform-Tools for Windows" from developer.android.com/tools/releases/platform-tools, unzip it, and add the folder to PATH (or copy `receipt-app/laptop` into that folder).
   - Mac: `brew install android-platform-tools`
   - Linux: `sudo apt install adb`
3. Download this folder (`receipt-app`) to the laptop.

## 2. Phone setup (once, Android)

1. Turn on **Developer options**: Settings → About phone → tap *Build number* 7 times.
2. Settings → Developer options → turn on **USB debugging**.
3. On the laptop, start the hub:
   ```
   cd receipt-app/laptop
   python3 receipt_hub.py        (Windows: py receipt_hub.py)
   ```
   The dashboard opens in your browser.
4. Plug the phone in with USB. Tap **Allow** on the "Allow USB debugging?" pop-up (tick "Always allow").
   The hub prints `📱 Phone connected`.
5. On the phone, open **Chrome** and go to `http://localhost:8765`.
6. Chrome menu (⋮) → **Add to Home screen / Install app**. Allow **Location** and **Camera** when asked.
7. Fill in your name and business in Settings.

From now on, open the app from your home screen. It works all day without the cable or internet.

## 3. Daily use

1. Open the app → **▶ Start Shift**. (Keep the app open; the screen stays on so GPS keeps tracking. Phones pause GPS for web apps when the screen is locked.)
2. At each door:
   - Sale → **✔ Sale / Receipt** → photo, address, what you did, amount → hand the phone to the customer to print their name and sign → **Save** → show them the receipt.
   - No sale → **✖ Said No**, **⌂ Not Home** or **↺ Come Back Later** → snap the house → pick a reason → Save. (These photos are what let the AI spot the pattern.)
3. **■ End Shift** → you'll see hours, miles, money, close rate and how much to set aside for taxes. Tap **Print Shift Report** to save a PDF on the phone.
4. Back home: start the hub, plug in the phone, tap **⇅ Sync to Laptop** (the dot in the top-right turns green when the laptop is connected).

## 4. On the laptop dashboard (`http://localhost:8765/dashboard`)

- **Shifts** → click a date → **Print / Save as PDF** for a full printable report.
- **Tax & hours spreadsheet** → open `earnings.xlsx` in Excel, Google Sheets or Numbers. Change the yellow cells on the *Tax Estimate* sheet (your tax bracket, state rate, this year's IRS mileage rate) and everything recalculates. These are estimates — check with a tax preparer.
- **Customer surveys** → first open `data/config.json` and set:
  - `survey_url` — your survey link (a free Google Form works well)
  - `survey_days_after` — how many days to wait (default 2)
  - To send automatically from Gmail: `smtp_user` = your Gmail address, `smtp_password` = a Gmail **App Password** (Google Account → Security → App passwords). If you leave these blank, the hub creates ready-to-send email drafts in `data/reports/outbox` instead.
  - Then click **Send due surveys** (or run `python3 receipt_hub.py surveys`).
- **AI coach** → open a chat with your AI assistant and upload `REPORT.md` plus the photo package (`ai_package.zip`, or print the contact sheet to PDF). The report already includes the prompt to paste. It asks the AI to compare houses that bought with houses that said no, give you a "knock / skip" checklist, and find your best days, hours and streets.
  - Optional: **Ask Claude directly** sends it all in one click. Needs `pip install anthropic` and an API key from console.anthropic.com (`set ANTHROPIC_API_KEY=...` on Windows, `export ANTHROPIC_API_KEY=...` on Mac/Linux, before starting the hub). The answer is saved in `data/reports/ai/`.

## iPhone / no cable

iPhones can't use the USB link. Two options:
- Put the `phone` folder on any HTTPS web host (for example GitHub Pages), open it in Safari, then Share → **Add to Home Screen**. To sync, go to **History → Export sync file**, AirDrop or email the file to the laptop, and pick it under "Import a sync file" on the dashboard (or drop it in `data/inbox`).
- Same Wi-Fi: run `python3 receipt_hub.py --lan`. Note that browsers only allow GPS and offline mode on `https` or `localhost` pages, so use this only for syncing.

## Where your data lives

- Phone: inside the app's browser storage until you sync. After syncing, **Settings → Delete synced data from phone** frees up space.
- Laptop: `receipt-app/laptop/data/` (photos, signatures, receipts, reports). **Back this folder up.** It holds customer names and emails, so keep it private; it's excluded from git.

## Commands

```
python3 receipt_hub.py            start the hub + dashboard
python3 receipt_hub.py rebuild    rebuild all reports
python3 receipt_hub.py surveys    send survey emails that are due
python3 receipt_hub.py analyze    send the AI report to Claude (needs API key)
```
