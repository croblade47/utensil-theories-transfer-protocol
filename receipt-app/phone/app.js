/* Door Receipts — phone app. Works offline; syncs to the laptop hub when reachable. */
(() => {
  'use strict';

  // ---------- helpers ----------
  const $ = id => document.getElementById(id);
  const uid = () => Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
  const money = n => '$' + (Number(n) || 0).toFixed(2);
  const fmtTime = t => new Date(t).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
  const fmtDate = t => new Date(t).toLocaleDateString([], { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' });
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const hms = ms => {
    const s = Math.max(0, Math.floor(ms / 1000));
    return `${Math.floor(s / 3600)}:${String(Math.floor(s / 60) % 60).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`;
  };
  function toast(msg, ms = 2200) {
    const t = $('toast'); t.textContent = msg; t.hidden = false;
    clearTimeout(toast._t); toast._t = setTimeout(() => { t.hidden = true; }, ms);
  }

  // ---------- settings ----------
  const SETTINGS_KEY = 'dr-settings';
  const defaults = { name: '', biz: '', phone: '', hub: '', tax: 25, wake: true };
  function loadSettings() {
    try { return { ...defaults, ...JSON.parse(localStorage.getItem(SETTINGS_KEY) || '{}') }; }
    catch { return { ...defaults }; }
  }
  let settings = loadSettings();
  function saveSettings() { try { localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings)); } catch {} }

  // ---------- navigation ----------
  function go(view) {
    document.querySelectorAll('.view').forEach(v => v.classList.toggle('active', v.id === 'view-' + view));
    window.scrollTo(0, 0);
    if (view === 'home') refreshHome();
    if (view === 'history') renderHistory();
    if (view === 'settings') fillSettings();
    if (view === 'sale') startSale();
  }
  document.addEventListener('click', e => {
    const g = e.target.closest('[data-go]'); if (g) { e.preventDefault(); go(g.dataset.go); }
    const q = e.target.closest('[data-quick]'); if (q) { e.preventDefault(); startQuick(q.dataset.quick); }
  });

  // ---------- location ----------
  let lastFix = null;          // most recent GPS fix, used to tag every visit
  let watchId = null;
  let lastSavedPoint = null;
  let wakeLock = null;

  function distM(a, b) {
    const R = 6371000, r = x => x * Math.PI / 180;
    const dLat = r(b.lat - a.lat), dLng = r(b.lng - a.lng);
    const h = Math.sin(dLat / 2) ** 2 + Math.cos(r(a.lat)) * Math.cos(r(b.lat)) * Math.sin(dLng / 2) ** 2;
    return 2 * R * Math.asin(Math.sqrt(h));
  }

  function startTracking(shiftId) {
    if (!('geolocation' in navigator)) { $('gps-status').textContent = 'GPS not available on this device'; return; }
    watchId = navigator.geolocation.watchPosition(async pos => {
      const p = { t: Date.now(), lat: pos.coords.latitude, lng: pos.coords.longitude, acc: Math.round(pos.coords.accuracy) };
      lastFix = p;
      $('gps-status').textContent = `GPS ±${p.acc}m`;
      // Save a breadcrumb every 30s or every 20m moved (skip very inaccurate fixes).
      if (p.acc > 100) return;
      if (!lastSavedPoint || p.t - lastSavedPoint.t > 30000 || distM(lastSavedPoint, p) > 20) {
        lastSavedPoint = p;
        await DB.put('points', { shiftId, ...p });
      }
    }, err => {
      $('gps-status').textContent = 'GPS: ' + (err.code === 1 ? 'permission denied — allow location for this app' : err.message);
    }, { enableHighAccuracy: true, maximumAge: 10000, timeout: 30000 });
    requestWake();
  }
  function stopTracking() {
    if (watchId !== null) navigator.geolocation.clearWatch(watchId);
    watchId = null; lastSavedPoint = null;
    if (wakeLock) { wakeLock.release().catch(() => {}); wakeLock = null; }
  }
  async function requestWake() {
    if (!settings.wake || !('wakeLock' in navigator)) return;
    try { wakeLock = await navigator.wakeLock.request('screen'); } catch {}
  }
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible' && currentShift && !currentShift.end) requestWake();
  });
  function oneFix() {
    return new Promise(resolve => {
      if (!('geolocation' in navigator)) return resolve(null);
      navigator.geolocation.getCurrentPosition(
        pos => resolve({ t: Date.now(), lat: pos.coords.latitude, lng: pos.coords.longitude, acc: Math.round(pos.coords.accuracy) }),
        () => resolve(null), { enableHighAccuracy: true, timeout: 8000, maximumAge: 15000 });
    });
  }
  async function fixForVisit() {
    if (lastFix && Date.now() - lastFix.t < 60000) return lastFix;
    return (await oneFix()) || lastFix;
  }

  // ---------- shifts ----------
  let currentShift = null;
  let clockTimer = null;

  async function loadCurrentShift() {
    const id = localStorage.getItem('dr-current-shift');
    if (!id) return null;
    const s = await DB.get('shifts', id);
    return s && !s.end ? s : null;
  }

  async function toggleShift() {
    if (!currentShift) {
      currentShift = { id: uid(), start: Date.now(), end: null, worker: settings.name, synced: false };
      await DB.put('shifts', currentShift);
      localStorage.setItem('dr-current-shift', currentShift.id);
      startTracking(currentShift.id);
      toast('Shift started — tracking location');
      refreshHome();
    } else {
      if (!confirm('End this shift?')) return;
      currentShift.end = Date.now();
      currentShift.synced = false;
      await DB.put('shifts', currentShift);
      localStorage.removeItem('dr-current-shift');
      stopTracking();
      const ended = currentShift;
      currentShift = null;
      await showSummary(ended.id);
      trySync(true);
    }
  }

  function tickClock() {
    clearInterval(clockTimer);
    const draw = () => { $('shift-clock').textContent = currentShift ? hms(Date.now() - currentShift.start) : '0:00:00'; };
    draw();
    if (currentShift) clockTimer = setInterval(draw, 1000);
  }

  async function shiftStats(shiftId) {
    const shift = await DB.get('shifts', shiftId);
    const visits = (await DB.byShift('visits', shiftId)).sort((a, b) => a.createdAt - b.createdAt);
    const points = (await DB.byShift('points', shiftId)).sort((a, b) => a.t - b.t);
    let meters = 0;
    for (let i = 1; i < points.length; i++) {
      const d = distM(points[i - 1], points[i]);
      if (d > 15 && d < 5000) meters += d; // ignore GPS jitter and jumps
    }
    const sales = visits.filter(v => v.type === 'sale');
    const total = sales.reduce((a, v) => a + (Number(v.amount) || 0), 0);
    const end = shift?.end || Date.now();
    const hours = shift ? (end - shift.start) / 3600000 : 0;
    return {
      shift, visits, points, sales, total, hours,
      miles: meters / 1609.344,
      doors: visits.length,
      nos: visits.filter(v => v.type === 'no').length,
      notHome: visits.filter(v => v.type === 'not_home').length,
      callbacks: visits.filter(v => v.type === 'callback').length,
    };
  }

  async function refreshHome() {
    $('btn-shift').textContent = currentShift ? '■ End Shift' : '▶ Start Shift';
    $('btn-shift').className = 'btn big ' + (currentShift ? 'danger' : 'primary');
    $('shift-status').textContent = currentShift ? `On shift since ${fmtTime(currentShift.start)}` : 'No shift running';
    if (!currentShift) $('gps-status').textContent = '';
    tickClock();
    if (currentShift) {
      const st = await shiftStats(currentShift.id);
      $('st-sales').textContent = st.sales.length;
      $('st-money').textContent = '$' + Math.round(st.total);
      $('st-doors').textContent = st.doors;
    } else {
      $('st-sales').textContent = '0'; $('st-money').textContent = '$0'; $('st-doors').textContent = '0';
    }
  }

  // Visits logged without a running shift get a same-day "loose" shift so nothing is lost.
  async function ensureShiftId() {
    if (currentShift) return currentShift.id;
    const day = new Date().toISOString().slice(0, 10);
    const id = 'day-' + day;
    let s = await DB.get('shifts', id);
    if (!s) {
      s = { id, start: Date.now(), end: Date.now(), worker: settings.name, untracked: true, synced: false };
    } else {
      s.end = Date.now(); s.synced = false;
    }
    await DB.put('shifts', s);
    return id;
  }

  // ---------- photos ----------
  function compressImage(file, maxSide = 1280, quality = 0.72) {
    return new Promise((resolve, reject) => {
      const img = new Image();
      const url = URL.createObjectURL(file);
      img.onload = () => {
        const scale = Math.min(1, maxSide / Math.max(img.width, img.height));
        const c = document.createElement('canvas');
        c.width = Math.round(img.width * scale); c.height = Math.round(img.height * scale);
        c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
        URL.revokeObjectURL(url);
        resolve(c.toDataURL('image/jpeg', quality));
      };
      img.onerror = e => { URL.revokeObjectURL(url); reject(e); };
      img.src = url;
    });
  }
  function wirePhoto(inputId, previewId, hintId, onData) {
    $(inputId).addEventListener('change', async e => {
      const f = e.target.files[0]; if (!f) return;
      try {
        const data = await compressImage(f);
        $(previewId).src = data; $(previewId).hidden = false; $(hintId).hidden = true;
        onData(data);
      } catch { toast('Could not read that photo'); }
    });
  }
  function resetPhoto(inputId, previewId, hintId) {
    $(inputId).value = ''; $(previewId).hidden = true; $(previewId).removeAttribute('src'); $(hintId).hidden = false;
  }

  // ---------- voice input ----------
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  document.querySelectorAll('.mic').forEach(btn => {
    if (!SR) { btn.addEventListener('click', () => toast('Tip: use the 🎤 key on your keyboard to talk')); return; }
    btn.addEventListener('click', () => {
      const input = $(btn.dataset.mic);
      const rec = new SR();
      rec.lang = navigator.language || 'en-US';
      rec.interimResults = false;
      btn.classList.add('listening');
      rec.onresult = ev => {
        const text = ev.results[0][0].transcript;
        input.value = input.value ? input.value + ' ' + text : text;
        input.dispatchEvent(new Event('input'));
      };
      rec.onerror = () => toast('Did not catch that — try again or use the keyboard mic');
      rec.onend = () => btn.classList.remove('listening');
      rec.start();
    });
  });

  // ---------- signature pad ----------
  const sig = (() => {
    const c = $('sig'); const ctx = c.getContext('2d');
    let drawing = false, dirty = false;
    function size() {
      const r = c.getBoundingClientRect(); if (!r.width) return;
      const dpr = window.devicePixelRatio || 1;
      c.width = r.width * dpr; c.height = r.height * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.lineWidth = 2.4; ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.strokeStyle = '#111';
      ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, r.width, r.height);
      dirty = false;
    }
    const pt = e => { const r = c.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top]; };
    c.addEventListener('pointerdown', e => { drawing = true; c.setPointerCapture(e.pointerId); ctx.beginPath(); ctx.moveTo(...pt(e)); });
    c.addEventListener('pointermove', e => { if (!drawing) return; ctx.lineTo(...pt(e)); ctx.stroke(); dirty = true; });
    ['pointerup', 'pointercancel'].forEach(ev => c.addEventListener(ev, () => { drawing = false; }));
    return { reset: size, isEmpty: () => !dirty, data: () => c.toDataURL('image/png') };
  })();
  $('sig-clear').addEventListener('click', () => sig.reset());

  // ---------- sale form ----------
  let salePhoto = null;
  wirePhoto('sale-photo', 'sale-photo-preview', 'photo-hint', d => { salePhoto = d; });
  let saleFix = null;

  function startSale() {
    $('sale-form').reset();
    resetPhoto('sale-photo', 'sale-photo-preview', 'photo-hint');
    salePhoto = null;
    requestAnimationFrame(() => sig.reset());
    saleFix = null;
    fixForVisit().then(f => { saleFix = f; }); // grab location while they fill in the form
  }

  async function nextReceiptNo() {
    const n = (parseInt(localStorage.getItem('dr-receipt-no') || '1000', 10) || 1000) + 1;
    localStorage.setItem('dr-receipt-no', String(n));
    return n;
  }

  $('sale-form').addEventListener('submit', async e => {
    e.preventDefault();
    if (sig.isEmpty() && !confirm('No signature yet. Save anyway?')) return;
    const shiftId = await ensureShiftId();
    const fix = saleFix || lastFix;
    const v = {
      id: uid(), type: 'sale', shiftId, createdAt: Date.now(),
      receiptNo: await nextReceiptNo(),
      address: $('sale-address').value.trim(),
      description: $('sale-desc').value.trim(),
      amount: Math.round(parseFloat($('sale-amount').value || '0') * 100) / 100,
      payment: $('sale-pay').value,
      customerName: $('sale-name').value.trim(),
      email: $('sale-email').value.trim(),
      signature: sig.isEmpty() ? null : sig.data(),
      photo: salePhoto,
      lat: fix?.lat ?? null, lng: fix?.lng ?? null, acc: fix?.acc ?? null,
      worker: settings.name, business: settings.biz, bizPhone: settings.phone,
      synced: false,
    };
    await DB.put('visits', v);
    $('receipt-out').innerHTML = receiptHTML(v);
    go('receipt');
    toast('Receipt saved');
  });

  function receiptHTML(v) {
    return `
      <h3>${esc(v.business || settings.biz || 'Receipt')}</h3>
      <div class="small">${esc(v.bizPhone || settings.phone || '')}</div>
      <div class="small">Receipt #${v.receiptNo} · ${fmtDate(v.createdAt)} ${fmtTime(v.createdAt)}</div>
      ${v.photo ? `<img class="house" src="${v.photo}" alt="House">` : ''}
      <table>
        <tr><td>Address</td><td>${esc(v.address)}</td></tr>
        <tr><td>Service</td><td>${esc(v.description)}</td></tr>
        <tr><td>Paid by</td><td>${esc(v.payment)}</td></tr>
        <tr><td>Provided by</td><td>${esc(v.worker || settings.name)}</td></tr>
      </table>
      <div class="amt">${money(v.amount)}</div>
      <table>
        <tr><td>Customer</td><td>${esc(v.customerName)}</td></tr>
        ${v.email ? `<tr><td>Email</td><td>${esc(v.email)}</td></tr>` : ''}
      </table>
      ${v.signature ? `<img class="signature" src="${v.signature}" alt="Signature">` : '<p class="small">(not signed)</p>'}
      <div class="small">Customer signature</div>`;
  }
  $('receipt-print').addEventListener('click', () => {
    $('print-area').innerHTML = `<div class="receipt">${$('receipt-out').innerHTML}</div>`;
    window.print();
  });

  // ---------- quick log ----------
  const REASONS = {
    no: ['Not interested', 'Too expensive', 'Already have someone', 'Do it myself', 'Renter', 'No soliciting sign', 'Rude'],
    not_home: ['No answer', 'Lights off', 'Dog only'],
    callback: ['Ask spouse', 'Busy now', 'Come back next week', 'Wants quote'],
  };
  const TITLES = { no: 'Said No', not_home: 'Not Home', callback: 'Come Back Later' };
  let quickType = 'no', quickPhoto = null, quickReason = '', quickFix = null;
  wirePhoto('quick-photo', 'quick-photo-preview', 'quick-photo-hint', d => { quickPhoto = d; });

  function startQuick(type) {
    quickType = type; quickPhoto = null; quickReason = '';
    $('quick-title').textContent = TITLES[type];
    $('quick-address').value = ''; $('quick-note').value = '';
    resetPhoto('quick-photo', 'quick-photo-preview', 'quick-photo-hint');
    $('quick-reasons').innerHTML = REASONS[type].map(r => `<button type="button" class="chip">${esc(r)}</button>`).join('');
    quickFix = null; fixForVisit().then(f => { quickFix = f; });
    go('quick');
  }
  $('quick-reasons').addEventListener('click', e => {
    const c = e.target.closest('.chip'); if (!c) return;
    const on = !c.classList.contains('on');
    $('quick-reasons').querySelectorAll('.chip').forEach(x => x.classList.remove('on'));
    c.classList.toggle('on', on);
    quickReason = on ? c.textContent : '';
  });
  $('quick-save').addEventListener('click', async () => {
    const shiftId = await ensureShiftId();
    const fix = quickFix || lastFix;
    await DB.put('visits', {
      id: uid(), type: quickType, shiftId, createdAt: Date.now(),
      address: $('quick-address').value.trim(), reason: quickReason, note: $('quick-note').value.trim(),
      photo: quickPhoto, amount: 0,
      lat: fix?.lat ?? null, lng: fix?.lng ?? null, acc: fix?.acc ?? null,
      worker: settings.name, synced: false,
    });
    toast('Logged: ' + TITLES[quickType]);
    go('home');
  });

  // ---------- summary / print / CSV ----------
  let summaryShiftId = null;
  async function showSummary(shiftId) {
    summaryShiftId = shiftId;
    const st = await shiftStats(shiftId);
    const setAside = st.total * (Number(settings.tax) || 0) / 100;
    const conv = st.doors - st.notHome > 0 ? (st.sales.length / (st.doors - st.notHome) * 100) : 0;
    $('summary-out').innerHTML = `
      <h2>Shift — ${fmtDate(st.shift.start)}</h2>
      <div class="card">
        <table class="sum">
          <tr><td>Time</td><td>${fmtTime(st.shift.start)} – ${fmtTime(st.shift.end || Date.now())}</td></tr>
          <tr><td>Hours worked</td><td>${st.hours.toFixed(2)}</td></tr>
          <tr><td>Distance tracked</td><td>${st.miles.toFixed(1)} mi</td></tr>
          <tr><td>Doors</td><td>${st.doors}</td></tr>
          <tr><td>Sales / No / Not home / Later</td><td>${st.sales.length} / ${st.nos} / ${st.notHome} / ${st.callbacks}</td></tr>
          <tr><td>Close rate (people who answered)</td><td>${conv.toFixed(0)}%</td></tr>
          <tr><td>Money made</td><td>${money(st.total)}</td></tr>
          <tr><td>Per hour</td><td>${st.hours >= 0.05 ? money(st.total / st.hours) : '—'}</td></tr>
          <tr><td>Set aside for taxes (${settings.tax}%)</td><td>${money(setAside)}</td></tr>
          <tr><td>Yours to keep</td><td>${money(st.total - setAside)}</td></tr>
        </table>
      </div>
      <p class="muted small">Full tax spreadsheet and AI report are built on the laptop after you sync.</p>`;
    go('summary');
  }

  async function printShift(shiftId) {
    const st = await shiftStats(shiftId);
    const head = `
      <div class="pb">
        <h2>${esc(settings.biz || 'Shift Report')} — ${fmtDate(st.shift.start)}</h2>
        <p>${esc(settings.name)} · ${fmtTime(st.shift.start)}–${fmtTime(st.shift.end || Date.now())} · ${st.hours.toFixed(2)} h · ${st.miles.toFixed(1)} mi</p>
        <table class="sum">
          <tr><td>Receipts</td><td>${st.sales.length}</td></tr>
          <tr><td>Total</td><td>${money(st.total)}</td></tr>
          <tr><td>Doors knocked</td><td>${st.doors}</td></tr>
        </table>
        <h3>All stops</h3>
        <table class="sum">${st.visits.map(v => `<tr><td>${fmtTime(v.createdAt)} — ${esc(v.address || '(no address)')} — ${esc(TITLES[v.type] || 'Sale')}${v.reason ? ' (' + esc(v.reason) + ')' : ''}</td><td>${v.type === 'sale' ? money(v.amount) : ''}</td></tr>`).join('')}</table>
      </div>`;
    $('print-area').innerHTML = head + st.sales.map(v => `<div class="receipt">${receiptHTML(v)}</div>`).join('');
    window.print();
  }

  function csvCell(v) { const s = String(v ?? ''); return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; }
  async function downloadCSV(shiftId) {
    const st = await shiftStats(shiftId);
    const rows = [['Receipt #', 'Date', 'Time', 'Type', 'Address', 'Description', 'Amount', 'Paid by', 'Customer', 'Email', 'Reason', 'Note', 'Lat', 'Lng']];
    st.visits.forEach(v => rows.push([v.receiptNo || '', new Date(v.createdAt).toLocaleDateString(), fmtTime(v.createdAt), v.type,
      v.address, v.description || '', v.type === 'sale' ? v.amount : '', v.payment || '', v.customerName || '', v.email || '',
      v.reason || '', v.note || '', v.lat ?? '', v.lng ?? '']));
    rows.push([]);
    rows.push(['', '', '', '', '', 'TOTAL', st.total.toFixed(2)]);
    rows.push(['', '', '', '', '', 'Hours', st.hours.toFixed(2)]);
    rows.push(['', '', '', '', '', `Tax set-aside (${settings.tax}%)`, (st.total * settings.tax / 100).toFixed(2)]);
    const blob = new Blob([rows.map(r => r.map(csvCell).join(',')).join('\n')], { type: 'text/csv' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `shift-${new Date(st.shift.start).toISOString().slice(0, 10)}.csv`;
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 5000);
  }
  $('summary-print').addEventListener('click', () => printShift(summaryShiftId));
  $('summary-csv').addEventListener('click', () => downloadCSV(summaryShiftId));
  $('summary-sync').addEventListener('click', () => trySync());

  // ---------- history ----------
  async function renderHistory() {
    const shifts = (await DB.all('shifts')).sort((a, b) => b.start - a.start);
    const rows = await Promise.all(shifts.map(async s => {
      const st = await shiftStats(s.id);
      return `<div class="list-item" data-shift="${s.id}">
        <div class="row"><b>${fmtDate(s.start)}</b><b>${money(st.total)}</b></div>
        <div class="row muted small"><span>${s.untracked ? 'No shift timer' : st.hours.toFixed(2) + ' h'} · ${st.sales.length} sales / ${st.doors} doors</span>
        <span>${s.synced ? '✓ synced' : 'not synced'}</span></div></div>`;
    }));
    $('history-list').innerHTML = rows.join('') || '<p class="muted">Nothing yet.</p>';
  }
  $('history-list').addEventListener('click', e => {
    const it = e.target.closest('[data-shift]'); if (it) showSummary(it.dataset.shift);
  });

  // ---------- sync ----------
  const hubBase = () => (settings.hub || '').replace(/\/$/, '');
  async function ping() {
    try {
      const r = await fetch(hubBase() + '/api/ping', { cache: 'no-store' });
      const ok = r.ok && (await r.json()).hub === 'door-receipts';
      $('sync-dot').classList.toggle('on', ok);
      $('sync-dot').title = ok ? 'Laptop connected' : 'Laptop not connected';
      return ok;
    } catch { $('sync-dot').classList.remove('on'); return false; }
  }

  async function buildPayload(onlyUnsynced = true) {
    const visits = (await DB.all('visits')).filter(v => !onlyUnsynced || !v.synced);
    const shifts = (await DB.all('shifts')).filter(s => !onlyUnsynced || !s.synced || s.id === currentShift?.id);
    const points = [];
    for (const s of shifts) points.push(...(await DB.byShift('points', s.id)).map(({ key, ...p }) => p));
    return { visits, shifts, points };
  }

  let syncing = false;
  async function trySync(silent = false) {
    if (syncing) return;
    syncing = true;
    const msg = $('sync-msg');
    try {
      if (!(await ping())) {
        if (!silent) { msg.textContent = 'Laptop not found. Plug in the USB cable and start the hub on the laptop.'; toast('Laptop not connected'); }
        return;
      }
      const { visits, shifts, points } = await buildPayload();
      if (!visits.length && !shifts.length) { if (!silent) toast('Everything is already synced'); return; }
      msg.textContent = 'Syncing…';
      // Send visits in small batches (photos make them large), shifts + GPS with the first batch.
      const batches = [];
      for (let i = 0; i < visits.length; i += 8) batches.push(visits.slice(i, i + 8));
      if (!batches.length) batches.push([]);
      for (let i = 0; i < batches.length; i++) {
        const body = { visits: batches[i], shifts: i === 0 ? shifts : [], points: i === 0 ? points : [], device: navigator.userAgent };
        const r = await fetch(hubBase() + '/api/sync', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
        if (!r.ok) throw new Error('Laptop said ' + r.status);
        for (const v of batches[i]) { v.synced = true; await DB.put('visits', v); }
        msg.textContent = `Syncing… ${Math.min((i + 1) * 8, visits.length)}/${visits.length}`;
      }
      for (const s of shifts) { if (s.end && s.id !== currentShift?.id) { s.synced = true; await DB.put('shifts', s); } }
      await fetch(hubBase() + '/api/rebuild', { method: 'POST' }).catch(() => {});
      msg.textContent = `Synced ${visits.length} visits at ${fmtTime(Date.now())}`;
      toast('Synced to laptop ✓');
    } catch (err) {
      msg.textContent = 'Sync failed: ' + err.message;
      if (!silent) toast('Sync failed — try again');
    } finally { syncing = false; }
  }
  $('btn-sync').addEventListener('click', () => trySync());
  setInterval(ping, 15000);

  $('btn-export').addEventListener('click', async () => {
    const payload = await buildPayload(false);
    const blob = new Blob([JSON.stringify({ ...payload, exportedAt: Date.now(), hub: 'door-receipts' })], { type: 'application/json' });
    const file = new File([blob], `door-receipts-${new Date().toISOString().slice(0, 10)}.json`, { type: 'application/json' });
    if (navigator.canShare && navigator.canShare({ files: [file] })) {
      try { await navigator.share({ files: [file], title: 'Door Receipts sync file' }); return; } catch {}
    }
    const a = document.createElement('a'); a.href = URL.createObjectURL(file); a.download = file.name; a.click();
  });

  // ---------- settings ----------
  function fillSettings() {
    $('set-name').value = settings.name; $('set-biz').value = settings.biz; $('set-phone').value = settings.phone;
    $('set-hub').value = settings.hub; $('set-tax').value = settings.tax; $('set-wake').checked = settings.wake;
  }
  $('set-save').addEventListener('click', () => {
    settings = { name: $('set-name').value.trim(), biz: $('set-biz').value.trim(), phone: $('set-phone').value.trim(),
      hub: $('set-hub').value.trim(), tax: parseFloat($('set-tax').value) || 0, wake: $('set-wake').checked };
    saveSettings(); toast('Saved'); go('home');
  });
  $('btn-wipe').addEventListener('click', async () => {
    if (!confirm('Delete everything that has already been synced to the laptop from this phone?')) return;
    const visits = await DB.all('visits');
    for (const v of visits) if (v.synced) await DB.del('visits', v.id);
    const shifts = await DB.all('shifts');
    for (const s of shifts) if (s.synced) {
      const left = await DB.byShift('visits', s.id);
      if (!left.length) {
        await DB.del('shifts', s.id);
        for (const p of await DB.byShift('points', s.id)) await DB.del('points', p.key);
      }
    }
    toast('Cleaned up');
  });

  $('btn-shift').addEventListener('click', toggleShift);

  // ---------- boot ----------
  (async () => {
    if ('serviceWorker' in navigator) navigator.serviceWorker.register('sw.js').catch(() => {});
    if (navigator.storage?.persist) navigator.storage.persist().catch(() => {});
    currentShift = await loadCurrentShift();
    if (currentShift) startTracking(currentShift.id);
    if (!settings.name) { go('settings'); toast('Enter your name and business first'); }
    else refreshHome();
    ping();
  })();
})();
