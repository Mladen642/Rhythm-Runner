
const DATA = window.__DATA;
const SONGS = window.__SONGS;
const LOOPS = window.__LOOPS;

const cv = document.getElementById('c');
const g = cv.getContext('2d');
g.imageSmoothingEnabled = false;
const W = 320, H = 180, HZ = 126, GY = 166, IMP = 78, TX = IMP + 10;
const LC = ['#5ef2ff', '#ff4fa3', '#ffe066'], K = '#1b1030';
const SPEED = 115, WP = 0.05, WG = 0.1, WO = 0.15;
const EY = [GY - 84, GY - 48, GY - 10];
const isTouch = ('ontouchstart' in window) || navigator.maxTouchPoints > 0;
const CH = DATA.chapter, F = DATA.font, STG = CH.stages, B0 = CH.boss, MB = CH.miniboss;

function fit() {
  const hint = document.getElementById('hint');
  const s = Math.max(0.5, Math.min(window.innerWidth / W, window.innerHeight / H));
  cv.style.width = Math.floor(W * s) + 'px'; cv.style.height = Math.floor(H * s) + 'px'; fit.w = innerWidth; fit.h = innerHeight;
}
window.addEventListener('resize', fit); fit(); setInterval(() => { if (innerWidth !== fit.w || innerHeight !== fit.h) fit(); }, 300);

// ---------- images ----------
let imgPending = 0;
function img(src) { const im = new Image(); imgPending++; im.onload = () => { imgPending--; }; im.src = src; return im; }
for (const st of STG) for (const L of st.layers) L.img = img(L.src);
CH.hero.img = img(CH.hero.src); CH.enemies.img = img(CH.enemies.src); CH.notesImg = img(CH.notes); CH.buddy.img = img(CH.buddy.src);
CH.intro.img = img(CH.intro.src); MB.img = img(MB.src); MB.flashImg = img(MB.flash); B0.img = img(B0.src); B0.flashImg = img(B0.flash);
for (const o of CH.outfits) o.img = img(o.src);
CH.rivalImg = img(CH.rival); CH.extrasImg = img(CH.extras); CH.duet.img = img(CH.duet.src);
for (const c of (CH.cast || [])) c.img = img(c.src);
if (CH.hammer) CH.hammer.img = img(CH.hammer.src);
if (CH.helper) CH.helper.img = img(CH.helper.src);
if (CH.intro.props) CH.intro.props.img = img(CH.intro.props.src);
CH.comicImg = { start: img(CH.comics.start), end: img(CH.comics.end) };
CH.evImg = {}; for (const k in (CH.eventComics || {})) CH.evImg[k] = img(CH.eventComics[k]);

// ---------- pixel drawing ----------
function R(x, y, w, h, c) { g.fillStyle = c; g.fillRect(Math.round(x), Math.round(y), w, h); }
function Px(x, y, c) { R(x, y, 1, 1, c); }
function disc(cx, cy, r, c) { cx = Math.round(cx); cy = Math.round(cy); for (let dy = -r; dy <= r; dy++) { const s = Math.floor(Math.sqrt(r * r - dy * dy) + 0.35); R(cx - s, cy + dy, 2 * s + 1, 1, c); } }
function ring(cx, cy, r, c, a0 = 0, a1 = 360) { for (let a = a0; a < a1; a += 3) { const t = a * Math.PI / 180; Px(cx + r * Math.cos(t), cy + r * Math.sin(t), c); } }
function tw(s, sc = 1) { return (s.length * 6 - 1) * sc; }
function text(s, x, y, col, sc = 1, sh = K) {
  const layers = sh ? [[sh, sc], [col, 0]] : [[col, 0]];
  for (const [c, o] of layers) {
    g.fillStyle = c;
    for (let i = 0; i < s.length; i++) {
      const gl = F[s[i]] || F[s[i].toUpperCase()];
      if (!gl) continue;
      for (let r = 0; r < 7; r++) { const row = gl[r]; for (let k = 0; k < 5; k++) if (row[k] === '#') g.fillRect(Math.round(x + (i * 6 + k) * sc + o), Math.round(y + r * sc + o), sc, sc); }
    }
  }
}
function ctext(s, cx, y, col, sc = 1, sh = K) { text(s, cx - Math.floor(tw(s, sc) / 2), y, col, sc, sh); }
function rtext(s, rx, y, col, sc = 1, sh = K) { text(s, rx - tw(s, sc), y, col, sc, sh); }
function bracket(cx, cy, r, c, grow) {
  const a = 5 + grow * 2, t = 2 + grow * 2, o = grow;
  R(cx - r - o, cy - r - o, a, t, c); R(cx - r - o, cy - r - o, t, a, c);
  R(cx + r - 3 - o, cy - r - o, a, t, c); R(cx + r - 1 - o, cy - r - o, t, a, c);
  R(cx - r - o, cy + r - 1 - o, a, t, c); R(cx - r - o, cy + r - 3 - o, t, a, c);
  R(cx + r - 3 - o, cy + r - 1 - o, a, t, c); R(cx + r - 1 - o, cy + r - 3 - o, t, a, c);
}
function spark(cx, cy) {
  for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) for (let t = 10; t < 14; t++) Px(cx + dx * t, cy + dy * t, '#ffffff');
  for (const [dx, dy] of [[1, 1], [-1, -1], [1, -1], [-1, 1]]) for (let t = 8; t < 11; t++) Px(cx + dx * t, cy + dy * t, '#ffe066');
}
function waves(x0, y0, x1, y1, cols, n = 3, h0 = 3) {
  for (let k = 0; k < n; k++) {
    const t = (k + 1) / (n + 1), cx = x0 + (x1 - x0) * t, cy = y0 + (y1 - y0) * t, h = h0 + k;
    for (let dy = -h; dy <= h; dy++) R(cx - Math.round(dy * dy / (1.6 * h)) - 1, cy + dy, 2, 1, cols[k % 2]);
  }
}
function thick(x0, y0, x1, y1, w, c) { const n = Math.max(1, Math.ceil(Math.hypot(x1 - x0, y1 - y0))); for (let i = 0; i <= n; i++) { const t = i / n; R(x0 + (x1 - x0) * t - (w >> 1), y0 + (y1 - y0) * t - (w >> 1), w, w, c); } }
function boom2(cx, cy, r) { disc(cx, cy, r, '#c2260f'); disc(cx, cy, Math.max(1, r - 1), '#ff5a1f'); disc(cx, cy, Math.max(1, r - 3), '#ffb02e'); disc(cx, cy, Math.max(1, r - 5), '#ffffff'); }
function meter(x, y, w, frac, col) { R(x - 1, y - 1, w + 2, 7, '#3a3550'); R(x, y, w, 5, '#1b1730'); const n = Math.floor((w / 4) * Math.max(0, Math.min(1, frac))); for (let i = 0; i < n; i++) R(x + i * 4, y, 3, 5, col); }
function panel(x, y, w, h, border) { R(x, y, w, h, K); R(x + 1, y + 1, w - 2, h - 2, border); R(x + 3, y + 3, w - 6, h - 6, '#0d0a18'); }
function bubble(s, x, y, col) {
  const w = tw(s) + 10; x = Math.max(4, Math.min(W - w - 4, x));
  R(x, y, w, 13, K); R(x + 1, y + 1, w - 2, 11, '#ffffff'); R(x + 6, y + 13, 4, 2, K); R(x + 7, y + 13, 2, 1, '#ffffff');
  text(s, x + 5, y + 3, col, 1, null);
}
function burst(word, x, y, age, big) {
  const pop = age < 0.08 ? 0.6 + age * 5 : 1, r = Math.round((big ? 15 : 11) * pop), sc = big && word.length < 8 ? 2 : 1;
  x = Math.max(r + 8, Math.min(W - r - 8, x)); y = Math.max(30 + r * 0.5, Math.min(H - 10, y));
  for (let k = 0; k < 10; k++) { const a = k * Math.PI / 5 + 0.3, L = r + (k % 2 ? 4 : 9); thick(x, y, x + Math.cos(a) * L, y + Math.sin(a) * L * 0.6, 5, K); }
  disc(x, y, r, K);
  for (let k = 0; k < 10; k++) { const a = k * Math.PI / 5 + 0.3, L = r + (k % 2 ? 3 : 7); thick(x, y, x + Math.cos(a) * L, y + Math.sin(a) * L * 0.6, 3, '#ffe066'); }
  disc(x, y, r - 1, '#ffe066');
  ctext(word, x, y - 3 * sc, '#c2260f', sc, K);
}
function flame(x, y, n, big, vis) {
  const fl = Math.sin(vis * 31 + x) > 0 ? 1 : 0, r0 = big ? 5 : 4;
  disc(x, y - 1, r0, 'rgba(255,59,59,0.85)'); disc(x + fl - 0.5, y - 2 - fl, r0 - 1, '#ff9e3d'); disc(x, y - 3, Math.max(1, r0 - 2), '#ffe066'); Px(x, y - 4, '#ffffff');
  R(x - 1 + fl, y - r0 - 4, 2, 3, '#ff9e3d'); R(x - fl, y - r0 - 7, 1, 3, '#ff3b3b');
  for (let i = 0; i < n; i++) {
    const ph = (vis * 2.4 + i * 0.37) % 1, px = x + Math.sin(i * 12.3 + vis * 9) * 2.5 * (1 - ph), py = y - ph * (big ? 15 : 10);
    const col = ph < 0.25 ? '#ffffff' : ph < 0.5 ? '#ffe066' : ph < 0.75 ? '#ff9e3d' : '#ff3b3b';
    R(px, py, ph < 0.4 ? 3 : 2, ph < 0.4 ? 3 : 2, col);
  }
}
function warnBand(y, a, title, sub) {
  R(0, y, W, 40, K); R(0, y + 1, W, 38, '#1a0508');
  for (let x = -30 + Math.floor(a * 40) % 12; x < W + 30; x += 12) for (let k = 0; k < 6; k++) { R(x + k - 5, y + 1 + k, 6, 1, '#ff3b3b'); R(x + k - 5, y + 33 + k, 6, 1, '#ff3b3b'); }
  if (Math.floor(a * 6) % 2) ctext(title, 160, y + 9, '#ff3b3b', 2);
  ctext(sub, 160, y + 26, '#ffffff', 1, null);
}

// ---------- audio ----------
let lp = null, lpTarget = 20000, lastVoice = -9, jukeSrc = null;
let actx = null, master = null, mainSrc = null, startAt = 0, noiseBuf = null, loopSrc = null, loopGain = null;
const BUF = {};
function lat() { return actx ? (actx.outputLatency || actx.baseLatency || 0) : 0; }
function decode(key) {
  if (BUF[key]) return BUF[key];
  BUF[key] = fetch(SONGS[key]).then(r => r.arrayBuffer()).then(b => new Promise((res, rej) => actx.decodeAudioData(b, res, rej)));
  return BUF[key];
}
function initAudio() {
  actx = new (window.AudioContext || window.webkitAudioContext)();
  master = actx.createGain(); master.gain.value = 0.9; master.connect(actx.destination);
  lp = actx.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 20000; lp.Q.value = 0.7; lp.connect(master);
  mainGain = actx.createGain(); mainGain.connect(lp); clipGain = actx.createGain(); clipGain.connect(lp);
  noiseBuf = actx.createBuffer(1, actx.sampleRate * 2, actx.sampleRate);
  const d = noiseBuf.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
  for (const c of (CH.cast || [])) if (c.clip && SONGS[c.clip]) decode(c.clip);
  return Promise.all([decode('title'), decode('pause'), decode('main')]);
}
function playLoop(key) {
  stopLoop();
  decode(key).then(b => {
    loopSrc = actx.createBufferSource(); loopSrc.buffer = b; loopSrc.loop = true; loopSrc.loopStart = 0; loopSrc.loopEnd = Math.min(b.duration, LOOPS[key]);
    loopGain = actx.createGain(); loopGain.gain.value = 0.85; loopSrc.connect(loopGain); loopGain.connect(master); loopSrc.start();
  });
}
function stopLoop(fade) {
  if (!loopSrc) return;
  const s = loopSrc, gn = loopGain; loopSrc = null;
  if (fade) { gn.gain.setTargetAtTime(0.0001, actx.currentTime, fade / 3); setTimeout(() => { try { s.stop(); } catch (e) {} }, fade * 1000 + 100); }
  else { try { s.stop(); } catch (e) {} }
}
let mainGain = null, clipGain = null, clipSrc = null;
function startMain(pos) {
  stopMain();
  decode('main').then(b => {
    mainSrc = actx.createBufferSource(); mainSrc.buffer = b; mainSrc.connect(mainGain); lp.frequency.cancelScheduledValues(0); lp.frequency.setValueAtTime(20000, actx.currentTime); lpTarget = 20000;
    const when = actx.currentTime + 0.15; startAt = when - pos; mainSrc.start(when, Math.max(0, pos));
    applyTempo(pos, when); syncClip(pos, when);
  });
  startAt = actx.currentTime + 0.15 - pos;
}
function stopClip() { if (clipSrc) { try { clipSrc.stop(); } catch (e) {} clipSrc.disconnect(); clipSrc = null; } }
function syncClip(pos, when) {
  stopClip();
  mainGain.gain.cancelScheduledValues(0); mainGain.gain.setValueAtTime(1, actx.currentTime);
  const Hw = B0.helper, hp = CH.helper;
  if (!Hw || !hp || !hp.clip || !SONGS[hp.clip] || pos >= Hw[1]) return;
  decode(hp.clip).then(b => {
    clipSrc = actx.createBufferSource(); clipSrc.buffer = b; clipSrc.connect(clipGain);
    const t0 = when + Math.max(0, Hw[0] - pos), off = Math.max(0, pos - Hw[0]), t1 = when + (Hw[1] - pos);
    clipGain.gain.cancelScheduledValues(0); clipGain.gain.setValueAtTime(1, actx.currentTime); clipGain.gain.setValueAtTime(1, t1 - 0.06); clipGain.gain.linearRampToValueAtTime(0.0001, t1);
    clipSrc.start(t0, off); clipSrc.stop(t1 + 0.05);
    mainGain.gain.setValueAtTime(pos >= Hw[0] ? 0 : 1, actx.currentTime); mainGain.gain.setValueAtTime(0, t0); mainGain.gain.setValueAtTime(1, t1);
  });
}
function stopMain() { stopClip(); TEMPO = null; if (mainSrc) { try { mainSrc.stop(); } catch (e) {} mainSrc.disconnect(); mainSrc = null; } }
let TEMPO = null;
function songTime() {
  const c = actx.currentTime;
  if (TEMPO && c >= TEMPO.c0) return (c < TEMPO.c1 ? TEMPO.s0 + (c - TEMPO.c0) * TEMPO.r : TEMPO.we + (c - TEMPO.c1)) - lat();
  return c - startAt - lat();
}
function applyTempo(pos, when) {
  TEMPO = null; const w = MW.tempo; if (!w || !mainSrc || pos >= w[1]) return;
  const r = 1.12, s0 = Math.max(w[0], pos), c0 = when + (s0 - pos), c1 = c0 + (w[1] - s0) / r;
  mainSrc.playbackRate.setValueAtTime(r, c0); mainSrc.playbackRate.setValueAtTime(1, c1);
  TEMPO = { s0, c0, c1, we: w[1], r };
}
function judgeTime() { return songTime() - offsetMs / 1000; }
function mf(m) { return 440 * Math.pow(2, (m - 69) / 12); }
function tone(type, f0, f1, dur, vol, delay = 0) {
  const t = actx.currentTime + delay, o = actx.createOscillator(), gn = actx.createGain();
  o.type = type; o.frequency.setValueAtTime(f0, t); if (f1) o.frequency.exponentialRampToValueAtTime(f1, t + dur);
  gn.gain.setValueAtTime(0.0001, t); gn.gain.linearRampToValueAtTime(vol, t + 0.008); gn.gain.exponentialRampToValueAtTime(0.0001, t + dur);
  o.connect(gn); gn.connect(master); o.start(t); o.stop(t + dur + 0.02);
}
function noise(dur, vol, f0, f1, type = 'lowpass', delay = 0) {
  const t = actx.currentTime + delay, s = actx.createBufferSource(), f = actx.createBiquadFilter(), gn = actx.createGain();
  s.buffer = noiseBuf; s.loop = true; f.type = type; f.frequency.setValueAtTime(f0, t); f.frequency.exponentialRampToValueAtTime(f1, t + dur);
  gn.gain.setValueAtTime(vol, t); gn.gain.exponentialRampToValueAtTime(0.0001, t + dur);
  s.connect(f); f.connect(gn); gn.connect(master); s.start(t); s.stop(t + dur + 0.02);
}
function blip(m) { tone('square', mf(m + 12), 0, 0.14, 0.05); }
function boom() { tone('triangle', 140, 40, 0.3, 0.35); noise(0.25, 0.25, 2000, 200); }
function bigBoom() { tone('triangle', 110, 30, 0.8, 0.45); noise(1.2, 0.45, 3000, 100); [0.15, 0.35, 0.6].forEach(d => tone('triangle', 90, 30, 0.4, 0.3, d)); }
function buzz() { tone('sawtooth', 120, 90, 0.18, 0.08); tone('square', 123, 95, 0.18, 0.05); }
function siren() { for (let i = 0; i < 6; i++) tone('square', i % 2 ? 620 : 820, 0, 0.18, 0.05, i * 0.2); }
function glitchSfx() { for (let i = 0; i < 8; i++) tone('square', 200 + Math.random() * 1600, 0, 0.04, 0.04, i * 0.05); noise(0.4, 0.15, 6000, 800, 'bandpass'); }
function tick(hi) { tone('square', hi ? 1320 : 880, 0, 0.08, 0.06); }
function fanfare() { [72, 76, 79, 84].forEach((m, i) => tone('square', mf(m), 0, 0.14, 0.07, i * 0.07)); }
function victory() { [72, 76, 79, 84, 79, 84, 88].forEach((m, i) => tone('square', mf(m), 0, 0.18, 0.07, i * 0.11)); }
const LASTPICK = new Map();
function P(v) {
  if (!Array.isArray(v)) return v || '';
  if (v.length < 2) return v[0] || '';
  let i; do { i = Math.floor(Math.random() * v.length); } while (i === LASTPICK.get(v));
  LASTPICK.set(v, i); return v[i];
}
function U(v) { return String(v).toUpperCase(); }
const MS = { ready: false, src: null };
(function msInit() {
  if (!window.meSpeak) return;
  Promise.all([fetch('lib/mespeak_config.json').then(r => r.json()), fetch('lib/en-us.json').then(r => r.json())])
    .then(([cfg, vc]) => { meSpeak.loadConfig(cfg); meSpeak.loadVoice(vc); MS.ready = true; setTimeout(() => { try { meSpeak.speak('ready', { rawdata: 'arraybuffer' }); } catch (e) {} }, 50); }).catch(() => {});
})();
function sysVoices() { try { return 'speechSynthesis' in window && speechSynthesis.getVoices().length > 0; } catch (e) { return false; } }
function msStop() { if (MS.src) { try { MS.src.stop(); } catch (e) {} MS.src = null; } }
function say(s, pitch, rate) {
  if (actx) lastVoice = actx.currentTime;
  if (sysVoices()) { try { const u = new SpeechSynthesisUtterance(s); u.pitch = pitch; u.rate = rate; speechSynthesis.cancel(); speechSynthesis.speak(u); } catch (e) {} return; }
  if (!MS.ready || !actx) return;
  try {
    const data = meSpeak.speak(s, { pitch: Math.max(0, Math.min(99, Math.round(pitch * 50))), speed: Math.round(165 * rate), amplitude: 110,
      variant: pitch >= 1.3 ? 'f2' : pitch <= 0.45 ? 'm7' : 'm3', rawdata: 'arraybuffer' });
    if (!data) return;
    actx.decodeAudioData(data, b => { msStop(); const src = actx.createBufferSource(); src.buffer = b; src.connect(master); src.start(); MS.src = src; }, () => {});
  } catch (e) {}
}
function laugh(pitch = 0.2) { [0, 0.16, 0.32].forEach((d, i) => { tone('square', 330 - i * 30, 260 - i * 30, 0.13, 0.08, d); tone('sawtooth', 165 - i * 15, 130 - i * 15, 0.13, 0.05, d); }); say('Ha ha ha!', pitch, 1.1); }
function coin() { tone('square', 988, 0, 0.08, 0.06); tone('square', 1319, 0, 0.3, 0.06, 0.08); }
function shatter() { noise(0.25, 0.3, 9000, 3000, 'highpass'); tone('sine', 2400, 3600, 0.15, 0.05); }
function splitSfx() { tone('square', 600, 1200, 0.12, 0.05); tone('square', 900, 1800, 0.12, 0.04, 0.05); }
function crowd(dur = 1.4) { noise(dur, 0.22, 2500, 1200, 'bandpass'); noise(dur * 0.8, 0.12, 5000, 3000, 'bandpass', 0.1); for (let i = 0; i < 6; i++) tone('triangle', 400 + Math.random() * 300, 0, 0.08, 0.02, Math.random() * dur * 0.7); }
function voice(s, pitch, rate, force) {
  const now = actx.currentTime;
  if (!force && now - lastVoice < 3.5) return;
  lastVoice = now; say(s, pitch, rate);
}
function stinger(kind) {
  if (kind === 'keytar') {
    [72, 76, 79, 84, 88, 91, 96].forEach((m, i) => tone('square', mf(m), 0, 0.12, 0.07, i * 0.05));
    tone('sawtooth', 1800, 120, 0.8, 0.09, 0.5); [60, 64, 67, 72].forEach(m => tone('square', mf(m), 0, 0.6, 0.05, 0.5));
  } else if (kind === 'biker') {
    [40, 47, 52].forEach(m => tone('square', mf(m), 0, 0.5, 0.07));
    tone('sawtooth', 55, 160, 2.0, 0.14, 0.1); noise(2.0, 0.18, 400, 1600, 'lowpass', 0.1);
  } else if (kind === 'pyro') {
    noise(0.6, 0.35, 400, 3000, 'bandpass'); tone('sawtooth', 70, 40, 0.5, 0.2);
    for (let i = 0; i < 4; i++) { tone('triangle', 60, 30, 0.3, 0.4, 0.6 + i * 0.25); noise(0.25, 0.3, 1200, 200, 'lowpass', 0.6 + i * 0.25); }
  } else if (kind === 'cart') {
    [40, 45, 47].forEach((m, i) => tone('square', mf(m + 12), 0, 0.25, 0.07, i * 0.25));
    for (let i = 0; i < 3; i++) { noise(0.15, 0.3, 1500, 900, 'bandpass', 0.7 + i * 0.25); tone('square', 180, 150, 0.15, 0.06, 0.7 + i * 0.25); }
    for (let i = 0; i < 8; i++) tone('triangle', 130, 50, 0.08, 0.3, i * 0.15);
  } else if (kind === 'cannon') {
    [62, 66, 69, 74].forEach((m, i) => tone('square', mf(m), 0, 0.3, 0.05, i * 0.12));
    for (let i = 0; i < 10; i++) tone('triangle', 90, 50, 0.08, 0.25, 0.5 + i * 0.05);
    [0.95, 1.25, 1.55].forEach(d => { tone('triangle', 70, 25, 0.5, 0.5, d); noise(0.4, 0.4, 2000, 150, 'lowpass', d); });
  } else if (kind === 'basscannon') {
    tone('sawtooth', 220, 1800, 0.55, 0.06); noise(0.55, 0.25, 1000, 8000, 'bandpass');
    for (let i = 0; i < 8; i++) { tone('sawtooth', 55, 0, 0.12, 0.16, 0.6 + i * 0.13); tone('square', 110, 0, 0.06, 0.06, 0.66 + i * 0.13); }
    tone('sine', 80, 30, 1.6, 0.5, 0.6);
  } else if (kind === 'stampede') {
    for (let i = 0; i < 4; i++) tone('sawtooth', 160 - i * 10, 90, 0.5, 0.06, i * 0.22);
    for (let i = 0; i < 12; i++) tone('triangle', 90, 40, 0.1, 0.3, i * 0.11); noise(1.6, 0.25, 600, 200, 'lowpass');
  } else if (kind === 'bigband') {
    [[60, 64, 67, 70], [62, 65, 69, 72], [64, 67, 71, 74], [65, 69, 72, 76]].forEach((ch, i) => ch.forEach(m => tone('square', mf(m + 12), 0, 0.18, 0.035, i * 0.16)));
    for (let i = 0; i < 6; i++) { tone('triangle', 140, 50, 0.12, 0.3, 0.7 + i * 0.1); noise(0.1, 0.18, 6000, 2500, 'highpass', 0.7 + i * 0.1); }
    [55, 59, 62, 65, 67].forEach(m => tone('square', mf(m + 12), 0, 1.0, 0.03, 1.4));
  } else if (kind === 'headbang') {
    for (let i = 0; i < 8; i++) { tone('triangle', 130, 40, 0.15, 0.4, i * 0.12); if (i % 2) noise(0.12, 0.25, 4000, 1500, 'highpass', i * 0.12); }
    [64, 67, 71, 76].forEach(m => tone('triangle', mf(m), 0, 1.6, 0.06, 0.1)); noise(1.2, 0.2, 8000, 3000, 'highpass', 0.96);
  } else if (kind === 'reaper') {
    [50, 53, 56, 62].forEach(m => { tone('square', mf(m) * 1.004, 0, 1.8, 0.035); tone('square', mf(m) * 0.996, 0, 1.8, 0.03); });
    noise(0.5, 0.35, 300, 4000, 'bandpass', 0.75); tone('sine', 2000, 4200, 0.35, 0.08, 0.8); tone('sawtooth', 60, 30, 1.5, 0.12, 0.1);
  } else if (kind === 'dj') {
    for (let i = 0; i < 4; i++) noise(0.12, 0.3, 800 + i * 900, 3000 + i * 500, 'bandpass', i * 0.13);
    [0.5, 0.75].forEach(d => [58, 62, 65].forEach(m => tone('sawtooth', mf(m), 0, 0.22, 0.05, d)));
    tone('sine', 120, 35, 1.2, 0.5, 0.55); tone('triangle', 60, 30, 1.0, 0.35, 0.55);
  } else if (kind === 'boar') {
    noise(1.0, 0.5, 3000, 150); tone('triangle', 90, 35, 0.6, 0.4);
    tone('square', 500, 1300, 0.45, 0.06, 0.25); noise(0.8, 0.4, 2500, 150, 'lowpass', 0.7); noise(0.8, 0.4, 2500, 150, 'lowpass', 1.3);
  }
}

// ---------- settings ----------
let offsetMs = 0, noFail = false, sel = 0, best = 0;
let PROG = { stars: [0, 0, 0, 0, 0], tapes: [false, false, false, false, false], outfit: 0, comicSeen: false };
try {
  offsetMs = parseInt(localStorage.getItem('rr_offset') || '0', 10) || 0; best = parseInt(localStorage.getItem('rr_ch' + CH.num + '_best') || '0', 10) || 0;
  const p = JSON.parse(localStorage.getItem('rr_ch' + CH.num + '_prog') || 'null'); if (p) PROG = Object.assign(PROG, p);
} catch (e) {}
function saveProg() { try { localStorage.setItem('rr_ch' + CH.num + '_prog', JSON.stringify(PROG)); } catch (e) {} }
function totalStars() { return PROG.stars.reduce((a, b) => a + b, 0); }
function outfitOK(i) { return totalStars() >= CH.outfits[i].stars; }
function heroImg() { return CH.outfits[outfitOK(PROG.outfit) ? PROG.outfit : 0].img; }
function adjOff(d) { offsetMs = Math.max(-250, Math.min(250, offsetMs + d)); try { localStorage.setItem('rr_offset', String(offsetMs)); } catch (e) {} }
function sgn(v) { return (v >= 0 ? '+' : '-') + Math.abs(v); }

// ---------- run state ----------
let state = 'loading', notes = [], score = 0, combo = 0, maxCombo = 0, groove = 10, buddy = 0, lostAt = -9, lastLoss = 1, pressAt = [-9, -9, -9];
let stats = [], errs = [], fx = [], judgeTxt = null, lastHitAt = -9, held = [false, false, false];
let shakeUntil = -9, shakeAmp = 2, flashUntil = -9, buddyRun = null, frozen = 0, result = null, souls = [], qte = null, mbDone = false, wipe = null;
let introT0 = 0, lastTick = -1, runFrom = 0, cur = 0, stageBanner = null, boss = null, phaseSeen = {};
let fever = { on: false, until: 0, t0: -9 }, leadIdx = 0, schedTo = 0, recentMiss = [], lowSaid = false, milestone = 0, announce = null;
let heroJumpAt = -9, heroStumbleAt = -9, celebrate = null, cheerUntil = -9, cameo = null, tipShown = {}, tipNow = null;
let parentKill = {}, stageScore0 = [0, 0, 0, 0, 0], rival = { said: false, done: false, res: null }, duetSaid = false, encoreSaid = false;
let starsRun = [null, null, null, null, null], tapesRun = [], bombHits = [0, 0, 0, 0, 0], taunt = null, nextTaunt = 0, unlocks = [], prevStars = 0, voiceSaid = {};
let comicNext = null;
let EVS = [], projs = [], duetAct = { next: 0, n: 0 }, partnerSay = null, kickReady = false, kbBase = 0, heroLungeAt = -9;
const COMIC_DUR = 2.6, COMIC_REAL = 3.6;
let evc = null, fadeIn = null;
function resetRun(from) {
  const t0 = from ? STG[from].t0 + 0.05 : -1;
  notes = CH.chart.map(n => Object.assign({}, n, { st: n.t >= t0 ? 'p' : 'skip', vic: false }));
  score = 0; combo = 0; maxCombo = 0; groove = 10; buddy = 0; lostAt = -9; pressAt = [-9, -9, -9];
  stats = STG.map(() => ({ P: 0, G: 0, O: 0, M: 0, B: 0, K: 0 })); errs = []; fx = []; judgeTxt = null; lastHitAt = -9;
  held = [false, false, false]; shakeUntil = -9; flashUntil = -9; buddyRun = null; result = null; souls = []; qte = null; wipe = null;
  mbDone = from > 2; miniRes = null; runFrom = from; cur = from; stageBanner = { i: from, t: from ? STG[from].t0 - 1.2 : 0 }; phaseSeen = {};
  boss = { phase: 'none', hp: 1, hitAt: -9, laughAt: -9, enterAt: 0, endAt: 0 };
  for (const n of notes) if (n.child !== undefined) n.hidden = true;
  {
    const CHP = [0, 0, 0.14, 0.22, 0.3], add = [];
    const busyL = (l, t, d) => notes.some(o => o.l === l && Math.abs(o.t - t) < d) || add.some(o => o.l === l && Math.abs(o.t - t) < d);
    for (const n of notes) {
      if (n.st !== 'p' || n.k !== 'tap' || n.hidden || n.child !== undefined || n.part2 || n.sw !== undefined || n.gold || n.l < 0) continue;
      const p = CHP[sidx(n)] || 0;
      if (!p || hsh(n.t * 31.7) > p) continue;
      if (notes.some(o => o !== n && Math.abs(o.t - n.t) < 0.01) || add.some(o => Math.abs(o.t - n.t) < 0.01)) continue;
      const opts = [0, 1, 2].filter(l => l !== n.l), l2 = opts[Math.floor(hsh(n.t * 7.3) * 2)];
      if (busyL(l2, n.t, 0.3) || notes.some(o => o.k === 'hold' && o.l === l2 && n.t > o.t - 0.3 && n.t < o.t + o.d + 0.3)) continue;
      add.push({ t: n.t, l: l2, m: n.m + 5, k: 'tap', s: n.s, e: 99000 + add.length, st: n.st, vic: false, chord: true });
    }
    for (const n of add) notes.push(n);
    notes.sort((a, b) => a.t - b.t || a.l - b.l);
  }
  fever = { on: false, until: 0, t0: -9 }; leadIdx = 0; schedTo = 0; recentMiss = []; lowSaid = false; milestone = 0; announce = null;
  heroJumpAt = -9; heroStumbleAt = -9; celebrate = null; cheerUntil = -9; cameo = null; tipShown = {}; tipNow = null; parentKill = {};
  stageScore0 = [0, 0, 0, 0, 0]; rival = { said: false, done: false, res: null }; duetSaid = false; encoreSaid = false;
  starsRun = [null, null, null, null, null]; tapesRun = []; bombHits = [0, 0, 0, 0, 0]; taunt = null; nextTaunt = 0; unlocks = []; prevStars = totalStars(); voiceSaid = {};
  projs = []; duetAct = { next: 0, n: 0 }; partnerSay = null; kickReady = false; kbBase = 0; heroLungeAt = -9;
  rival = { said: false, done: false, res: null, init: false, state: 'idle', next: 0, kickT: 0, tauntNext: 0, adj: 0, koAt: -9, hitAt: -9, yoinkNext: 0, yoinkAt: 0, yoinkT: null, snatchNext: 0 };
  const tStart = from ? STG[from].t0 - 1.2 : -1;
  EVS = [];
  if (CH.cast && CH.cast.length) {
    const pool = CH.cast.slice(), d = pool[Math.floor(Math.random() * pool.length)];
    CH.duet = d;
  }
  setupMechs();
  const addEv = (k, t) => { if (CH.evImg[k] && t > tStart) EVS.push({ k, t }); };
  if (!mbDone) for (const n of notes) if (n.st === 'p' && n.t >= MB.t0 - 0.6 && n.t <= MB.t0 + 14) n.st = 'skip';
  addEv('enter', B0.t_enter);
  if (B0.rev) addEv('rev', B0.rev[0]);
  if (B0.cor) addEv('cor', B0.cor[0] - 0.8);
  if (B0.broken) addEv('broken', B0.broken[0]);
  if (B0.helper) addEv(CH.helper && CH.evImg['helper_' + CH.helper.id] ? 'helper_' + CH.helper.id : 'helper', B0.helper[0]);
  addEv('finale', B0.fin[0]);
  const dw = CH.special.duet;
  if (dw && dw[0] > tStart) {
    let sd = 17; const rr = () => (sd = (sd * 9301 + 49297) % 233280) / 233280;
    let t = dw[0] + 1.0; const add = [];
    while (t < dw[1] - 0.5) {
      t += 0.3 + rr() * 0.35;
      const tt = Math.round((t + (rr() - 0.5) * 0.12) * 1000) / 1000;
      const ln = Math.floor(rr() * 3);
      if (notes.some(n => n.st === 'p' && ((n.l === ln || n.l === -1) && Math.abs(n.t - tt) < 0.3 || Math.abs(n.t - tt) < 0.1 || (n.k === 'hold' && n.l === ln && tt > n.t - 0.3 && tt < n.t + n.d + 0.3))) || add.some(n => Math.abs(n.t - tt) < 0.3)) continue;
      add.push({ t: tt, l: ln, m: 72, k: 'tap', s: STG[3].id, e: 90000 + add.length, st: 'p', vic: false, extra: true });
    }
    for (const n of add) notes.push(n);
    notes.sort((a, b) => a.t - b.t || a.l - b.l);
  }
  for (const e of EVS) if (e.k !== 'mini') for (const n of notes) if (n.st === 'p' && n.t >= e.t - 0.3 && n.t <= e.t + 1.3) n.st = 'skip';
  BM = { nextShot: MPICK.includes('shots') ? B0.t_enter + 7 : 1e9, nextCrit: MPICK.includes('crits') ? B0.t_enter + 12 : 1e9, coreStart: -9, coreUntil: -9, tele: null, echoes: [], seen: {}, shotN: 0 };
  const s5 = STG[4], bar = 240 / (s5.bpm || 120), beat = bar / 4;
  BM.bar = bar; BM.beat = beat;
  const PATS = [[0, 1, 2, 3], [0, 1, 1.5, 3], [0, 0.5, 2, 3], [0, 1, 2, 2.5], [0, 1.5, 2, 3]];
  let lastEcho = -99;
  for (let k = Math.ceil((B0.t_enter + 6 - s5.t0) / bar); BM.echoes.length < 0; k++) {
    const tb = s5.t0 + k * bar;
    if (tb > s5.t1 - 6) break;
    if (tb < tStart + 2 || tb - lastEcho < 18 || bossBusy(tb) || bossBusy(tb + bar) || bossBusy(tb + 2 * bar)) continue;
    const pat = PATS[Math.floor(Math.random() * PATS.length)], idx = BM.echoes.length;
    const calls = pat.map(p => ({ t: tb + p * beat, l: Math.floor(Math.random() * 3), played: false }));
    for (const n of notes) if (n.st === 'p' && n.t >= tb - 0.25 && n.t <= tb + 2 * bar + 0.1) n.st = 'skip';
    calls.forEach((c, i) => notes.push({ t: Math.round((c.t + bar) * 1000) / 1000, l: c.l, m: 60 + c.l * 5, k: 'echo', s: s5.id, e: 96000 + idx * 10 + i, st: 'p', vic: false, ev: idx }));
    BM.echoes.push({ tb, calls, hits: 0, misses: 0, resolved: false, said: false });
    lastEcho = tb;
  }
  notes.sort((a, b) => a.t - b.t || a.l - b.l);
}

const MECH = {
  rev: { n: 'REVERSED KEYS', len: 8, inp: 1, a: 'KEYS REVERSED!', b: 'W IS GROUND, R IS HIGH' },
  cor: { n: 'CORRUPTED SPACE', len: 8, inp: 1, a: 'SPACE CORRUPTED!', b: 'HIT W+E+R TOGETHER' },
  broken: { n: 'BROKEN INSTRUMENT', len: 4, inp: 1, a: 'INSTRUMENT BROKEN!', b: 'ONLY SPACE WORKS' },
  helper: { n: 'HELPER TAKEOVER', len: 8 },
  shots: { n: 'BOSS SHOTS', len: 0 }, crits: { n: 'WEAK SPOTS', len: 0 }, rage: { n: 'RAGE PHASE', len: 0 },
  lock: { n: 'LANE LOCK', len: 4, inp: 1, a: 'LANE LOCKED!', b: 'DO NOT PRESS THE FROZEN LANE' },
  glitch: { n: 'GLITCH PHASE', len: 4, inp: 1, a: 'GLITCH PHASE!', b: 'EVERY ENEMY SWITCHES LANES' },
  chords: { n: 'CHORD STORM', len: 4, inp: 1, a: 'CHORD STORM!', b: 'HIT BOTH KEYS TOGETHER' },
  lights: { n: 'LIGHTS OUT', len: 8, a: 'LIGHTS OUT!', b: 'WATCH FOR THE GLOWING EYES' },
  speed: { n: 'SPEED SHIFT', len: 8, a: 'SPEED SHIFT!', b: 'SAME BEAT, NEW SPEED' },
  decoys: { n: 'DECOYS', len: 8, a: 'DECOYS!', b: 'IGNORE THE FLICKERING FAKES' },
  minions: { n: 'MINION WAVE', len: 4, a: 'MINION WAVE!', b: 'EVERY ONE THAT GETS PAST HEALS THE BOSS' },
  drain: { n: 'GROOVE DRAIN', len: 4, a: 'GROOVE DRAIN!', b: 'ONLY PERFECTS REFILL' },
  bombs: { n: 'BOMB RAIN', len: 4, a: 'BOMB RAIN!', b: 'DO NOT HIT THE BOMBS' },
  charge: { n: 'CHARGE ATTACK', len: 2, a: 'CHARGE ATTACK!', b: 'BLOCK IT WITH THE CHORDS' },
  riff: { n: 'RIFF BATTLE', len: 4, a: 'RIFF BATTLE!', b: 'BOSS PLAYS, THEN YOU PLAY' },
  tug: { n: 'TUG OF WAR', len: 2, a: 'TUG OF WAR!', b: 'HIT SPACE ON EVERY BEAT' },
  perfect: { n: 'PERFECT WINDOW', len: 4, a: 'PERFECTS ONLY!', b: 'TRIPLE DAMAGE FOR PERFECTS' },
  hypno: { n: 'HYPNOTIZED BUDDY', len: 2, a: 'BUDDY HYPNOTIZED!', b: 'HIT ALL ITS ATTACKS TO FREE IT' },
  spot: { n: 'SPOTLIGHT LANE', len: 4, a: 'SPOTLIGHT!', b: 'DOUBLE DAMAGE IN THE GLOWING LANE' },
  jam: { n: 'JAM SESSION', len: 8, a: 'JAM SESSION!', b: '8 HITS IN A ROW = BIG DAMAGE' },
  coins: { n: 'COIN RAIN', len: 4, a: 'COIN RAIN!', b: 'GRAB COINS TO FILL YOUR BUDDY' },
  slowmo: { n: 'SLOW-MO', len: 2, a: 'SLOW-MO!', b: 'BIG AND SLOW, SAME BEAT' },
  mirror: { n: 'MIRROR ARENA', len: 4, inp: 1, a: 'MIRROR ARENA!', b: 'LANES FLIPPED, KEYS STAY THE SAME' },
  shield: { n: 'SHIELD WALL', len: 8, a: 'SHIELD WALL!', b: 'HOLD A 20 COMBO TO HURT THE BOSS' },
  turncoat: { n: 'TURNCOAT NOTES', len: 4, a: 'TURNCOATS!', b: 'SOME ENEMIES TURN INTO BOMBS' },
  holds: { n: 'HOLD STORM', len: 4, a: 'HOLD STORM!', b: 'HOLD THE LONG NOTES, TAP THE REST' },
  tempo: { n: 'TEMPO SURGE', len: 4, a: 'TEMPO SURGE!', b: 'THE MUSIC SPEEDS UP' },
};
const COST = { helper: 1, crits: 1, perfect: 1, riff: 1, tug: 1, hypno: 1, broken: 1, spot: 1, jam: 1, coins: 1, slowmo: 1,
  shots: 2, bombs: 2, charge: 2, chords: 2, speed: 2, decoys: 2, minions: 2, lock: 2,
  rev: 3, cor: 3, lights: 3, glitch: 3, drain: 3, rage: 3, mirror: 3, shield: 3, turncoat: 3, holds: 3, tempo: 3 };
const MINCH = { rev: 8, mirror: 10 };
const BUDGET = [6, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 9];
function mechOk(k) { const n = CH.num || 1; return n >= (MINCH[k] || (COST[k] >= 3 ? 6 : 1)); }
let MW = {}, MX = {}, MPICK = [];
function mOn(k, t) { const w = MW[k]; return !!w && t >= w[0] && t < w[1]; }
function pickMechs() {
  if (window.FORCE_MECH) return window.FORCE_MECH.slice();
  const helperOk = !!(CH.helperWin && CH.cast && CH.cast.some(c => c.clip && SONGS[c.clip]));
  const B = BUDGET[Math.min(12, CH.num || 6)];
  const keys = Object.keys(MECH).filter(k => COST[k] && (k !== 'helper' || helperOk) && mechOk(k));
  const ok = [], near = [];
  for (let i = 0; i < keys.length; i++) for (let j = i + 1; j < keys.length; j++) for (let l = j + 1; l < keys.length; l++) {
    const t = [keys[i], keys[j], keys[l]];
    if (t.filter(k => MECH[k].inp).length > 1 || (t.includes('helper') && t.includes('tempo'))) continue;
    const c = COST[t[0]] + COST[t[1]] + COST[t[2]];
    if (c <= B && c >= B - 1) ok.push(t); else if (c <= B) near.push(t);
  }
  const pool = ok.length ? ok : near, pick = pool[Math.floor(Math.random() * pool.length)].slice();
  for (let i = pick.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [pick[i], pick[j]] = [pick[j], pick[i]]; }
  return pick;
}
function scheduleMechs(picks) {
  MW = {}; MX = {};
  const s5 = STG[4], bar = 240 / (s5.bpm || 120), o = s5.t0, f0 = B0.fin ? B0.fin[0] : s5.t1;
  const k0 = Math.ceil((B0.t_enter + 5 - o) / bar), k1 = Math.floor((f0 - 1.5 - o) / bar), occ = [], placed = [];
  const free = (a, b) => a >= k0 && b <= k1 && !occ.some(([c, d]) => a < d + 1 && b > c - 1);
  if (picks.includes('helper') && CH.helperWin) { const a = Math.round((CH.helperWin[0] - o) / bar); occ.push([a, a + 8]); MW.helper = CH.helperWin.slice(); placed.push('helper'); }
  for (const k of picks) {
    if (k === 'helper') continue;
    if (!MECH[k].len) { placed.push(k); continue; }
    for (let L = MECH[k].len; L >= 2; L = Math.floor(L / 2)) {
      const c = []; for (let a = k0; a + L <= k1; a++) if (free(a, a + L)) c.push(a);
      if (c.length) { const a = c[Math.floor(Math.random() * c.length)]; occ.push([a, a + L]); MW[k] = [o + a * bar, o + (a + L) * bar]; placed.push(k); break; }
    }
  }
  for (const k of ['crits', 'shots']) if (placed.length < 3 && !placed.includes(k)) placed.push(k);
  return placed;
}
function applyMechs() {
  const s5 = STG[4], sid = s5.id, bar = 240 / (s5.bpm || 120), beat = bar / 4, add = [];
  let eid = 98000;
  const mk = (t, l, k, ex) => Object.assign({ t: Math.round(t * 1000) / 1000, l, m: 60 + Math.max(0, l) * 5, k, s: sid, e: eid++, st: 'p', vic: false }, ex || {});
  const inW = (n, w) => w && n.s === sid && n.t >= w[0] - 0.01 && n.t < w[1] - 0.01;
  const laneN = n => n.st === 'p' && n.l >= 0 && !n.hidden && ['tap', 'shield', 'split', 'hold'].includes(n.k);
  const clearW = (w, pred) => { for (const n of notes) if (n.st === 'p' && n.s === sid && n.t >= w[0] - 0.15 && n.t < w[1] - 0.05 && (!pred || pred(n))) n.st = 'skip'; };
  const beats = (w, step, off = 0) => { const r = []; for (let t = w[0] + off; t < w[1] - 0.02; t += step) r.push(t); return r; };
  const freeLane = (t, d) => { const ls = [0, 1, 2].filter(l => !notes.some(o => o.st === 'p' && o.l === l && Math.abs(o.t - t) < d) && !add.some(o => o.l === l && Math.abs(o.t - t) < d)); return ls.length ? ls[Math.floor(Math.random() * ls.length)] : -1; };
  for (const n of notes) if (n.k === 'wall' && n.s === sid) { n.k = 'space'; n.got = 0; }
  if (MW.cor) {
    for (const n of notes) if (inW(n, MW.cor) && n.k === 'space' && n.st === 'p') n.k = 'wall';
    for (const t of beats(MW.cor, bar)) if (!notes.some(n => n.st === 'p' && n.k === 'wall' && Math.abs(n.t - t) < 0.3)) { for (const n of notes) if (n.st === 'p' && n.s === sid && Math.abs(n.t - t) < 0.25) n.st = 'skip'; add.push(mk(t, -1, 'wall')); }
  }
  if (MW.broken) { clearW(MW.broken, laneN); for (const t of beats(MW.broken, beat)) if (!notes.some(n => n.st === 'p' && n.k === 'space' && Math.abs(n.t - t) < 0.2)) add.push(mk(t, -1, 'space')); }
  if (MW.lock) {
    const L = MX.lockL = Math.floor(Math.random() * 3);
    for (const n of notes) if (inW(n, MW.lock) && laneN(n) && n.l === L) { n.k = 'bomb'; delete n.d; }
    for (const t of beats(MW.lock, beat * 2, beat)) if (!notes.some(n => n.st === 'p' && n.l === L && Math.abs(n.t - t) < 0.3)) add.push(mk(t, L, 'bomb'));
  }
  if (MW.glitch) for (const n of notes) {
    if (!inW(n, MW.glitch) || n.st !== 'p' || n.k !== 'tap' || n.hidden || n.child !== undefined || n.part2 || n.sw !== undefined || n.chord) continue;
    const to = [0, 1, 2].filter(l => l !== n.l)[Math.floor(Math.random() * 2)];
    if (notes.some(o => o !== n && Math.abs(o.t - n.t) < (o.l === to ? 0.3 : 0.01))) continue;
    n.sw = n.l; n.l = to;
  }
  if (MW.chords) for (const n of notes) {
    if (!inW(n, MW.chords) || n.st !== 'p' || n.k !== 'tap' || n.hidden || n.child !== undefined || n.part2 || n.sw !== undefined || n.chord) continue;
    if (notes.some(o => o !== n && Math.abs(o.t - n.t) < 0.01) || add.some(o => Math.abs(o.t - n.t) < 0.01)) continue;
    const l2 = [0, 1, 2].filter(l => l !== n.l)[Math.floor(Math.random() * 2)];
    if (notes.some(o => o.l === l2 && Math.abs(o.t - n.t) < 0.25) || add.some(o => o.l === l2 && Math.abs(o.t - n.t) < 0.25)) continue;
    add.push(mk(n.t, l2, 'tap', { chord: true }));
  }
  if (MW.speed) { MX.speed = Math.random() < 0.5 ? 'dash' : 'brake'; for (const n of notes) if (inW(n, MW.speed) && n.k !== 'hold') n.warp = MX.speed; }
  if (MW.decoys) for (const t of beats(MW.decoys, beat, beat / 2)) { const l = freeLane(t, 0.3); if (l >= 0) add.push(mk(t, l, 'decoy')); }
  if (MW.minions) {
    for (const n of notes) if (inW(n, MW.minions) && n.k === 'tap' && n.st === 'p' && !n.hidden) n.minion = true;
    for (const t of beats(MW.minions, beat, beat / 2)) { const l = freeLane(t, 0.3); if (l >= 0) add.push(mk(t, l, 'tap', { minion: true })); }
  }
  if (MW.bombs) for (const t of beats(MW.bombs, beat, beat / 2)) { const l = freeLane(t, 0.3); if (l >= 0) add.push(mk(t, l, 'bomb')); }
  if (MW.charge) {
    const w2 = [MW.charge[0] + bar, MW.charge[1]]; clearW(w2);
    [[0, 1], [1, 2], [0, 2]].forEach((pr, i) => pr.forEach(l => add.push(mk(w2[0] + i * beat, l, 'tap', { block: true, chord: true }))));
  }
  if (MW.riff) for (const n of notes) {
    if (!inW(n, MW.riff) || n.st !== 'p') continue;
    const b = Math.floor((n.t - MW.riff[0]) / bar + 1e-6);
    if (b % 2 === 0) { if (['tap', 'shield', 'split'].includes(n.k) && !n.hidden) n.bp = true; else n.st = 'skip'; }
    else n.riff = true;
  }
  if (MW.tug) { clearW(MW.tug); for (const t of beats(MW.tug, beat)) add.push(mk(t, -1, 'space', { tug: true })); }
  if (MW.hypno) { clearW(MW.hypno); for (const t of beats(MW.hypno, beat)) add.push(mk(t, Math.floor(Math.random() * 3), 'tap', { hyp: true })); }
  if (MW.spot) MX.spotL = Math.floor(Math.random() * 3);
  if (MW.coins) for (const t of beats(MW.coins, beat, beat / 2)) { const l = freeLane(t, 0.3); if (l >= 0) add.push(mk(t, l, 'coin')); }
  if (MW.slowmo) {
    for (const n of notes) if (n.st === 'p' && n.s === sid && n.t >= MW.slowmo[0] - 0.5 && n.t < MW.slowmo[0] - 0.01) n.st = 'skip';
    for (const n of notes) if (inW(n, MW.slowmo) && n.k !== 'hold') { n.warp = 'slow'; n.big = true; }
  }
  if (MW.turncoat) for (const n of notes) if (inW(n, MW.turncoat) && n.k === 'tap' && n.st === 'p' && !n.hidden && !n.chord && n.sw === undefined && Math.random() < 0.3) n.turn = true;
  if (MW.holds) { const L = MX.holdL = Math.floor(Math.random() * 3); clearW(MW.holds, n => n.l === L || n.k === 'hold'); for (const t of beats(MW.holds, bar)) add.push(mk(t, L, 'hold', { d: Math.round(beat * 3 * 1000) / 1000 })); }
  for (const n of add) notes.push(n);
  notes.sort((a, b) => a.t - b.t || a.l - b.l);
}
function setupMechs() {
  MPICK = scheduleMechs(pickMechs());
  B0.rev = MW.rev || null; B0.cor = MW.cor || null; B0.broken = MW.broken || null; B0.helper = MW.helper || null;
  if (B0.helper) { const hp = CH.cast.filter(c => c.clip && SONGS[c.clip]); CH.helper = hp[Math.floor(Math.random() * hp.length)]; }
  applyMechs();
}
function resolveMechs(st) {
  for (const [k, f] of [['charge', 'block'], ['tug', 'tug'], ['hypno', 'hyp']]) {
    const w = MW[k]; if (!w || BM['r_' + k] || st < w[1] + 0.25) continue; BM['r_' + k] = true;
    const ns = notes.filter(n => n[f]), ok = ns.length && ns.every(n => n.st === 'd');
    if (k === 'charge') { if (ok) bossDamage(0.06, 'BLOCKED!'); else { loseGroove(2); shake(0.6, 5); bigBoom(); heroStumbleAt = st; fx.push({ k: 'banner', t0: st, a: 'KNOCKBACK!', b: '-2 GROOVE' }); } }
    if (k === 'tug') { if (ok) bossDamage(0.08, 'SHOVED!'); else { loseGroove(2); shake(0.5, 4); fx.push({ k: 'banner', t0: st, a: 'PUSHED BACK!', b: '-2 GROOVE' }); } }
    if (k === 'hypno') { if (ok) { buddy = 1; fx.push({ k: 'banner', t0: st, a: 'BUDDY FREED!', b: 'BUDDY METER FULL' }); fanfare(); } else { buddy = 0; boss.laughAt = st; fx.push({ k: 'banner', t0: st, a: 'BUDDY LOST IT!', b: 'BUDDY METER EMPTY' }); } }
  }
}
function lightsDraw(vis) {
  const w = MW.lights; if (!w || vis < w[0] - 0.5 || vis > w[1] + 0.5 || boss.phase !== 'fight') return;
  const a = Math.max(0, Math.min(1, (vis - (w[0] - 0.5)) / 0.5, (w[1] + 0.5 - vis) / 0.5)) * 0.92, x0 = TX + 72;
  g.fillStyle = 'rgba(4,2,10,' + a + ')'; g.fillRect(x0, 24, W - x0, GY - 18);
  for (let x = x0 - 16; x < x0; x += 2) { g.fillStyle = 'rgba(4,2,10,' + (a * (x - x0 + 16) / 16) + ')'; g.fillRect(x, 24, 2, GY - 18); }
  for (const n of notes) {
    const x = noteX(n, vis); if (x > W + 8) break;
    if (x < x0 || n.st !== 'p' || n.hidden) continue;
    if (n.l < 0) { R(x, EY[0] - 10, 1, GY - EY[0] + 10, '#ffd23f'); continue; }
    const y = n.sw !== undefined ? EY[n.sw] : EY[n.l], col = n.k === 'bomb' ? '#ff9e3d' : '#ff3b3b';
    R(x - 3, y - 2, 2, 1, col); R(x + 2, y - 2, 2, 1, col);
  }
}
function mechStatus(vis) {
  if (boss.phase !== 'fight') return;
  const bar = 240 / (STG[4].bpm || 120);
  let s = null, c = '#ffffff';
  if (mOn('lock', vis)) { const y = EY[MX.lockL]; g.fillStyle = 'rgba(94,242,255,0.16)'; g.fillRect(TX - 12, y - 9, W - TX + 12, 18); text('LOCKED', TX + 14, y - 3, '#5ef2ff', 1, null); }
  if (mOn('spot', vis)) { const y = EY[MX.spotL]; g.fillStyle = 'rgba(255,210,63,0.16)'; g.fillRect(TX - 12, y - 9, W - TX + 12, 18); }
  if (mOn('riff', vis)) { const b = Math.floor((vis - MW.riff[0]) / bar); s = b % 2 ? 'YOUR TURN!' : 'BOSS TURN - WATCH'; c = b % 2 ? '#7cf06a' : '#ff6b6b'; }
  else if (mOn('perfect', vis)) { s = 'PERFECTS ONLY  x3 DAMAGE'; c = '#ffd23f'; }
  else if (mOn('drain', vis)) { s = 'GROOVE DRAIN - ONLY PERFECTS REFILL'; c = '#b06bff'; }
  else if (mOn('tug', vis)) { const ns = notes.filter(n => n.tug); s = 'TUG OF WAR  ' + ns.filter(n => n.st === 'd').length + '/' + ns.length; c = '#ff9e3d'; }
  else if (mOn('hypno', vis)) { s = 'FREE YOUR BUDDY!'; c = '#ff7ac8'; }
  else if (mOn('lock', vis)) { s = 'LANE ' + 'WER'[MX.lockL] + ' IS LOCKED'; c = '#5ef2ff'; }
  else if (mOn('charge', vis)) { s = vis < MW.charge[0] + bar ? 'CHARGE INCOMING!' : 'BLOCK!'; c = '#ff3b3b'; }
  else if (mOn('minions', vis)) { s = 'STOP THE MINIONS!'; c = '#b06bff'; }
  else if (mOn('spot', vis)) { s = 'SPOTLIGHT ON ' + 'WER'[MX.spotL] + ' - DOUBLE DAMAGE'; c = '#ffd23f'; }
  else if (mOn('jam', vis)) { s = 'JAM SESSION  ' + (MX.jam || 0) + '/8'; c = '#7cf06a'; }
  else if (mOn('coins', vis)) { s = 'COIN RAIN - FREE BUDDY POWER'; c = '#ffd23f'; }
  else if (mOn('slowmo', vis)) { s = 'SLOW-MO'; c = '#9af8ff'; }
  else if (mOn('mirror', vis)) { s = 'MIRROR ARENA - KEYS STAY THE SAME'; c = '#ff7ac8'; }
  else if (mOn('shield', vis)) { s = combo >= 20 ? 'SHIELD DOWN - HIT HARD!' : 'SHIELD WALL - COMBO ' + combo + '/20'; c = combo >= 20 ? '#7cf06a' : '#5ef2ff'; }
  else if (mOn('turncoat', vis)) { s = 'WATCH FOR TURNCOATS'; c = '#ff3b3b'; }
  else if (mOn('holds', vis)) { s = 'HOLD STORM'; c = '#ff9e3d'; }
  else if (mOn('tempo', vis)) { s = 'TEMPO SURGE'; c = '#ff3b3b'; }
  if (s) ctext(s, W / 2, 27, c, 1, K);
}
let BM = { nextShot: 1e9, nextCrit: 1e9, echoes: [], coreStart: -9, coreUntil: -9, tele: null, seen: {} };
function bossBusy(t) {
  if (t < B0.t_enter + 5 || t > STG[4].t1 - 4) return true;
  if (B0.fin && t > B0.fin[0] - 2) return true;
  for (const w of [B0.rev, B0.cor, B0.broken, B0.helper, ...Object.values(MW)]) if (w && t > w[0] - 1.5 && t < w[1] + 0.8) return true;
  if (EVS.some(e => t > e.t - 1 && t < e.t + 1.6)) return true;
  return false;
}
function shotBusy(t) {
  if (t < B0.t_enter + 5 || t > STG[4].t1 - 4 || (B0.fin && t > B0.fin[0] - 2)) return true;
  for (const w of [B0.broken, B0.helper, MW.tug, MW.charge, MW.hypno, MW.riff]) if (w && t > w[0] - 1.5 && t < w[1] + 0.8) return true;
  return EVS.some(e => t > e.t - 1 && t < e.t + 1.6);
}
function inEcho(t) { return BM.echoes.some(e => t > e.tb - 0.5 && t < e.tb + 2 * BM.bar + 0.4); }
function bossDamage(a, label, col) {
  if (boss.phase !== 'fight') return;
  if (shieldUp()) { MX.ping = songTime(); return; }
  const st = songTime(); boss.hp = Math.max(0.12, boss.hp - a); boss.hitAt = st; shake(0.25, 3);
  const [bx] = bossPos(st); fx.push({ k: 'burst', word: label, x: bx + 10, y: GY - B0.oy / 2, t0: st, big: true });
}
function firstTime(key, a, b) { if (BM.seen[key]) return; BM.seen[key] = true; fx.push({ k: 'banner', t0: songTime(), a, b }); }
function bossMechUpdate(st) {
  if (boss.phase !== 'fight' || (qte && qte.phase !== 'done')) return;
  const dt = Math.min(0.1, Math.max(0, st - (BM.lastSt || st))); BM.lastSt = st;
  if (!BM.annPick && st > B0.t_enter + 3.2) { BM.annPick = true; fx.push({ k: 'banner', t0: st, a: 'BOSS MECHANICS', b: MPICK.map(k => MECH[k].n).join(' + ') }); }
  for (const k of MPICK) {
    const w = MW[k]; if (!w || BM['a_' + k] || st < w[0] - 0.8) continue; BM['a_' + k] = true;
    const comic = EVS.some(e => Math.abs(e.t - w[0]) < 1.7 && e.k !== 'enter' && e.k !== 'finale');
    if (!comic && MECH[k].a) { fx.push({ k: 'banner', t0: st, a: k === 'broken' ? (CH.brokenTitle || MECH[k].a) : MECH[k].a, b: MECH[k].b }); glitchSfx(); boss.laughAt = st; }
  }
  if (MPICK.includes('rage') && !BM.rage && (boss.hp < 0.55 || st > (B0.t_enter + B0.fin[0]) / 2)) { BM.rage = true; fx.push({ k: 'banner', t0: st, a: 'RAGE MODE!', b: 'THE BOSS ATTACKS TWICE AS OFTEN' }); shake(0.8, 5); bigBoom(); boss.laughAt = st; if (BM.nextShot > 1e8) BM.nextShot = st + 1.5; }
  if (mOn('drain', st)) groove = Math.max(2, groove - dt * 0.8 * BOSS_DMG);
  if (MW.turncoat) for (const n of notes) { if (n.t > st + 1) break; if (n.turn && n.st === 'p' && n.k === 'tap' && n.t - st < 0.75 && n.t > st) { n.k = 'bomb'; n.turn = false; fx.push({ k: 'burst', word: 'TRAITOR!', x: noteX(n, st), y: EY[n.l] - 12, t0: st }); } }
  resolveMechs(st);
  if (st > BM.nextShot && !buddyRun && !brokenOn(st)) {
    const s0 = STG[4].t0, ta = s0 + Math.ceil((st + 1.9 - s0) / BM.beat) * BM.beat, l = Math.floor(Math.random() * 3);
    const clash = n => n.st === 'p' && Math.abs(n.t - ta) < (n.l === l || n.l < 0 ? 0.4 : 0.12);
    const special = n => n.l < 0 || n.k === 'hold' || n.k === 'tape' || n.gold || n.crit || n.block || n.tug || n.hyp || n.bp;
    const free = !shotBusy(ta) && !inEcho(ta) && !notes.some(n => clash(n) && special(n));
    if (free) {
      for (const n of notes) if (clash(n)) { n.st = 'skip'; if (n.k === 'split') for (const c of notes) if (c.child === n.e) c.st = 'skip'; }
      const n = { t: Math.round(ta * 1000) / 1000, l, m: 40, k: 'shot', s: STG[4].id, e: 97000 + (BM.shotN++), st: 'p', vic: false };
      const i = notes.findIndex(o => o.t > n.t); notes.splice(i < 0 ? notes.length : i, 0, n);
      BM.tele = { t: st, ta, l }; BM.nextShot = st + (BM.rage ? 0.5 : 1) * (5.5 + Math.random() * 2.5);
      tone('sawtooth', 200, 900, 0.5, 0.05); firstTime('shot', 'INCOMING SHOT!', 'HIT ITS LANE ON TIME TO PARRY');
    } else BM.nextShot = st + 0.5;
  }
  if (st > BM.nextCrit && st > BM.coreUntil + 1) {
    if (bossBusy(st + 1) || inEcho(st + 3.5)) BM.nextCrit = st + 1;
    else {
      const cands = notes.filter(n => n.st === 'p' && !n.vic && !n.hidden && !n.claimed && ['tap', 'shield', 'split'].includes(n.k) && n.sw === undefined && n.t > st + 1.0 && n.t < st + 3.4).slice(0, 4);
      if (cands.length >= 2) {
        cands.forEach(n => n.crit = true); BM.coreStart = st; BM.coreUntil = st + 3.5; BM.nextCrit = st + 15 + Math.random() * 4;
        tone('square', 660, 1320, 0.3, 0.05); firstTime('crit', 'WEAK SPOT!', 'HIT THE GOLDEN TARGETS FOR CRITS');
      } else BM.nextCrit = st + 1.5;
    }
  }
  for (const [i, E] of BM.echoes.entries()) {
    if (!E.said && st > E.tb - 0.8) { E.said = true; firstTime('echo', 'CALL AND RESPONSE!', 'WATCH THE LANES, THEN REPEAT THEM'); if (BM.seen.echo && i > 0) fx.push({ k: 'banner', t0: st, a: 'CALL AND RESPONSE!', b: 'AGAIN, FASTER THIS TIME' }); }
    for (const c of E.calls) if (!c.played && st >= c.t - 0.06) { c.played = true; tone('square', mf([84, 79, 72][c.l]), 0, 0.18, 0.07, Math.max(0, c.t - st)); boss.laughAt = -9; }
    if (!E.resolved && st > E.tb + 2 * BM.bar + 0.3) {
      E.resolved = true;
      if (E.hits >= E.calls.length) { bossDamage(0.07, 'PERFECT ECHO!'); fanfare(); }
      else { boss.laughAt = st; laugh(0.2); taunt = { who: 'boss', txt: 'OFF KEY!', t: st }; }
    }
  }
}
function comicEvent(t) { return EVS.find(e => e.shown && t >= e.t - 0.85 && t < e.t + 2.4); }
function startEvComic(e, st) {
  e.shown = true; frozen = st; state = 'evcomic';
  const now = actx.currentTime;
  for (const src of [mainSrc, clipSrc]) if (src) { src.playbackRate.cancelScheduledValues(now); src.playbackRate.setValueAtTime(1, now); src.playbackRate.exponentialRampToValueAtTime(0.12, now + 0.5); }
  if (lp) { lp.frequency.cancelScheduledValues(now); lp.frequency.setValueAtTime(lp.frequency.value, now); lp.frequency.exponentialRampToValueAtTime(1400, now + 0.5); lpTarget = 1400; }
  master.gain.cancelScheduledValues(now); master.gain.setValueAtTime(master.gain.value, now); master.gain.linearRampToValueAtTime(0.6, now + 0.5);
  evc = { e, real0: performance.now() / 1000 }; try { speechSynthesis.cancel(); } catch (x) {} msStop();
  tone('square', 220, 880, 0.18, 0.05); noise(0.25, 0.15, 6000, 1500, 'highpass');
}
function endEvComic() {
  if (!evc) return;
  evc = null; state = 'play';
  stopMain();
  master.gain.cancelScheduledValues(0); master.gain.setValueAtTime(0.2, actx.currentTime); master.gain.linearRampToValueAtTime(0.9, actx.currentTime + 0.5);
  startMain(frozen); fadeIn = { real0: performance.now() / 1000 };
}
function evComicDraw(real) {
  const a = real - evc.real0, im = CH.evImg[evc.e.k];
  g.fillStyle = 'rgba(5,3,10,' + Math.min(0.62, a * 3) + ')'; g.fillRect(0, 24, W, H - 24);
  for (let gy = 26; gy < H; gy += 8) for (let gx = (gy / 8) % 2 ? 4 : 0; gx < W; gx += 8) Px(gx, gy, '#2a1a48');
  const xin = a < 0.2 ? Math.round((1 - a / 0.2) * W) : a > COMIC_REAL - 0.2 ? -Math.round((a - (COMIC_REAL - 0.2)) / 0.2 * W) : 0;
  const bob = a > 0.2 && a < COMIC_REAL - 0.2 ? Math.round(Math.sin(a * 2.5)) : 0;
  g.drawImage(im, Math.round((W - im.width) / 2) + xin, 42 + bob);
  R(0, 146, W, 12, K); if (Math.floor(a * 3) % 2) ctext('MEANWHILE...', 160, 148, '#ffe066', 1, null);
  const left = Math.max(0, 1 - a / COMIC_REAL); R(110, 162, 100, 3, '#2a1a48'); R(110, 162, Math.round(100 * left), 3, '#ffe066');
  if (a > 0.8) rtext(isTouch ? 'TAP: SKIP' : 'SPACE: SKIP', 314, 170, '#8f88b3', 1, null);
}
function fadeInDraw(real) {
  const p = (real - fadeIn.real0) / 0.8;
  if (p >= 1) { fadeIn = null; return; }
  const r = Math.round(6 * (1 - p));
  if (p < 0.12) { g.fillStyle = 'rgba(255,255,255,' + (0.5 * (1 - p / 0.12)) + ')'; g.fillRect(0, 24, W, H - 24); }
  if (r > 0) for (let gy = 24; gy < H + 8; gy += 10) for (let gx = (gy / 10) % 2 ? 5 : 0; gx < W + 8; gx += 10) disc(gx, gy, r, '#05030a');
}
function startRun(from) {
  actx.resume(); stopLoop(0.5); resetRun(from); lastTick = -1; tick(true);
  startMain(from ? STG[from].t0 - 1.2 : 0);
  state = 'play';
}
function pause() {
  if (state !== 'play') return;
  frozen = songTime(); state = 'paused'; stopMain(); playLoop('pause');
  try { speechSynthesis.cancel(); } catch (e) {} msStop();
}
function resume() { if (state !== 'paused') return; stopLoop(); startMain(frozen); state = 'play'; }
function toMap() { stopMain(); stopLoop(); playLoop('title'); state = 'map'; }
function rnd(n) { const x = Math.sin(n.t * 12.9898 + n.l * 78.233) * 43758.5453; return x - Math.floor(x); }
function hsh(k) { const x = Math.sin(k * 12.9898 + 4.1) * 43758.5453; return x - Math.floor(x); }
function shake(dur, amp) { shakeUntil = songTime() + dur; shakeAmp = amp; }
function stageAt(t) { let i = 0; for (let k = 0; k < STG.length; k++) if (t >= STG[k].t0 - 0.01) i = k; return i; }
function inWin(t, w) { return t >= w[0] && t < w[1]; }
function reversed(t) { return !!B0.rev && inWin(t, B0.rev); }
function corrupted(t) { return !!B0.cor && inWin(t, B0.cor); }
function sidx(n) { return STG.findIndex(s => s.id === n.s); }

let lastMisclick = -9;
const NAMES = { K: ['LOCKED!', '#5ef2ff'], D: ['DECOY!', '#b06bff'], E: ['TOO EARLY', '#ff9e3d'], L: ['TOO LATE', '#ff9e3d'], P: ['PERFECT!', '#ffe066'], G: ['GREAT!', '#ffffff'], O: ['GOOD', '#7cf06a'], M: ['MISS', '#ff6b6b'], B: ['BREAK', '#ff6b6b'] };
function grade(e) { const a = Math.abs(e); return a <= WP ? 'P' : a <= WG ? 'G' : 'O'; }
function shieldUp() { return mOn('shield', songTime()) && combo < 20; }
function bossHit(k = 1) { if (boss.phase === 'fight') { if (shieldUp()) { MX.ping = songTime(); return; } boss.hp = Math.max(0.12, boss.hp - 0.45 / B0.notes * k); boss.hitAt = songTime(); } }
function mult(st) { return (fever.on ? 2 : 1) * (special('duet', st) ? 1.5 : 1) * (encoreOn(st) ? 2 : 1); }
function special(k, st) { const w = CH.special[k]; return w && st >= w[0] && st < w[1]; }
function encoreOn(st) { return boss.phase === 'ko' && special('encore', st); }
function award(gr, e, n, w = 1) {
  stats[sidx(n)][gr]++; errs.push(e); combo += w; maxCombo = Math.max(maxCombo, combo);
  score += Math.round({ P: 300, G: 200, O: 100 }[gr] * (1 + Math.min(combo, 100) / 100) * mult(songTime())) * w;
  onCombo();
  const st0 = songTime();
  let gg = { P: 0.34, G: 0.2, O: 0.1 }[gr] * w;
  if (mOn('drain', st0)) gg = gr === 'P' ? gg * 2 : 0;
  groove = Math.min(16, groove + gg);
  buddy = Math.min(1, buddy + { P: 0.009, G: 0.006, O: 0.002 }[gr] * w);
  judgeTxt = { g: gr, t: songTime() };
  if (mOn('perfect', st0)) { if (gr === 'P') bossHit(3); } else bossHit();
  if (n.riff && boss.phase === 'fight') { boss.hp = Math.max(0.12, boss.hp - 0.012); boss.hitAt = st0; }
  if (mOn('spot', st0) && n.l === MX.spotL) bossHit(1);
  if (mOn('jam', st0)) { MX.jam = (MX.jam || 0) + 1; if (MX.jam >= 8) { MX.jam = 0; bossDamage(0.05, 'JAM!'); } }
}
function startFever(st) {
  fever = { on: true, until: st + 12, t0: st }; schedTo = st + 0.05;
  fx.push({ k: 'banner', t0: st, a: 'FEVER!', b: 'DOUBLE SCORE' }); voice(P(['Fever!', 'Fever time!', 'Feel the fever!', 'Burning up!', 'Here we go!', 'Turn it up!']), 1.3, 1.1, true); crowd(); cheerUntil = st + 2;
}
function endFever() { fever.on = false; }
const MILES = [[25, ['GROOVY!', 'NICE!', 'SMOOTH!', 'FUNKY!', 'SWEET!', 'SLICK!']], [50, ['ON FIRE!', 'SIZZLING!', 'BLAZING!', 'RED HOT!', 'SCORCHING!']],
  [100, ['UNSTOPPABLE!', 'RELENTLESS!', 'MONSTER!', 'INSANE!', 'BEAST MODE!']], [150, ['LEGENDARY!', 'MYTHICAL!', 'GODLIKE!', 'HEROIC!', 'EPIC!']],
  [200, ['GROOVE GOD!', 'IMMORTAL!', 'TRANSCENDENT!', 'ASCENDED!', 'PERFECTION!']]];
const CAMEOS = ['KEEP IT UP!', 'YOU ROCK!', 'LOOKING GOOD!', 'DONT STOP NOW!', 'THATS MY HERO!', 'SO PROUD!', 'NAILED IT!'];
function onCombo() {
  const st = songTime();
  for (const [c, words] of MILES) if (combo === c && milestone < c) { milestone = c; const wd = P(words); announce = { txt: wd, t: st }; voice(wd.toLowerCase(), 0.5, 0.9, true); cheerUntil = st + 1.6; crowd(1); }
  if (combo === 75) voice(P(CH.lines.combo), CH.voicePitch, 1.15);
  if ((combo === 40 || combo === 120) && !buddyRun) { cameo = { t: st, txt: P(CAMEOS) }; projs.push({ kind: 'heart', t0: st + 0.4, dur: 0.7, from: [W - 30, 70], heal: true, small: true }); }
  if (combo < 25) milestone = 0;
}
const BOSS_DMG = 0.85;
function dmgScale() { return BOSS_DMG; }
function loseGroove(n) { n *= dmgScale(); groove = Math.max(0, groove - n); lostAt = songTime(); lastLoss = n; }
function missed(n) {
  const st = songTime();
  if (n.k === 'split') for (const c of notes) if (c.child === n.e) c.st = 'skip';
  if (encoreOn(st)) { combo = 0; return; }
  stats[sidx(n)].M++; combo = 0; loseGroove(2); judgeTxt = { g: 'M', t: st };
  heroStumbleAt = st; recentMiss.push(st); if (fever.on) endFever();
  if (n.k === 'shot') { loseGroove(1); shake(0.5, 5); bigBoom(); fx.push({ k: 'burst', word: 'OUCH!', x: CH.hero.x + 6, y: GY - 30, t0: st, big: true }); }
  if (mOn('jam', st)) MX.jam = 0;
  if (n.minion && boss.phase === 'fight') { boss.hp = Math.min(1, boss.hp + 0.02); const [bx] = bossPos(st); fx.push({ k: 'burst', word: 'HEAL!', x: bx + 10, y: GY - B0.oy / 2, t0: st }); }
  if (n.crit && st < BM.coreUntil) { BM.coreUntil = st; boss.hp = Math.min(1, boss.hp + 0.03); boss.laughAt = st; fx.push({ k: 'banner', t0: st, a: 'SHIELD UP!', b: 'THE BOSS HEALS' }); for (const o of notes) o.crit = false; }
  if (boss.phase === 'fight' && hsh(n.t * 7) < 0.3) { boss.laughAt = songTime(); laugh(0.15); }
}
function special2(n, x) {
  const st = songTime();
  if (n.k === 'shield') { fx.push({ k: 'shatter', x, l: n.l, t0: st }); shatter(); }
  if (n.k === 'shot') { fx.push({ k: 'reflect', l: n.l, t0: st }); tone('square', 1800, 600, 0.2, 0.07); noise(0.15, 0.3, 8000, 2000, 'highpass'); setTimeout(() => bossDamage(0.05, 'PARRY!'), 260); }
  if (n.k === 'echo' && BM.echoes[n.ev]) BM.echoes[n.ev].hits++;
  if (n.crit) { bossDamage(0.035, 'CRIT!'); coin(); }
  if (n.k === 'split') { for (const c of notes) if (c.child === n.e) c.hidden = false; parentKill[n.e] = { t: st, x, l: n.l }; splitSfx(); }
  if (n.gold) { buddy = Math.min(1, buddy + 0.35); score += 1000; coin(); fx.push({ k: 'banner', t0: st, a: 'GOLDEN!', b: '+1000  BUDDY BOOST' }); heroJumpAt = st; }
  if (n.k === 'tape') {
    const i = sidx(n); tapesRun.push(i); score += 2000; coin(); setTimeout(coin, 160);
    fx.push({ k: 'banner', t0: st, a: 'CASSETTE FOUND!', b: PROG.tapes[i] ? 'ALREADY IN YOUR JUKEBOX' : 'BONUS TRACK UNLOCKED' });
    if (!PROG.tapes[i]) { PROG.tapes[i] = true; saveProg(); }
    heroJumpAt = st;
  }
}
function killFx(n, x, src) { special2(n, x); const st = songTime(), pop = rnd(n) < 0.42 || n.gold; fx.push({ k: 'kill', l: n.l, x, t0: st, pop, m: n.m }); if (src) fx.push({ k: 'atk', l: n.l, t0: st }); if (pop) blip(n.m); }
function wallPress(lane, t) {
  for (const n of notes) {
    if (n.t - t > WO) break;
    if (n.st === 'p' && n.k === 'wall' && Math.abs(t - n.t) <= WO) {
      n.got = (n.got || 0) | (1 << lane); n.e = Math.max(n.e || 0, Math.abs(t - n.t));
      if (n.got === 7) { award(grade(n.e), n.e, n, 3); n.st = 'd'; blast(n, 'W+E+R!'); }
      return true;
    }
  }
  return false;
}
function lanePress(key) {
  const st = songTime(), lane = reversed(st) ? 2 - key : key;
  held[lane] = true; pressAt[lane] = st;
  const t = judgeTime();
  if (corrupted(st) && wallPress(lane, t)) return;
  if (mOn('lock', st) && lane === MX.lockL) {
    const b = notes.find(n => n.st === 'p' && n.k === 'bomb' && n.l === lane && Math.abs(t - n.t) <= WO);
    if (b) { b.st = 'boom'; bombHits[sidx(b)]++; combo = 0; loseGroove(2); heroStumbleAt = st; shake(0.35, 3); bigBoom(); fx.push({ k: 'bomb', x: TX, l: lane, t0: st }); }
    else if (st - lastMisclick > 0.15) { lastMisclick = st; loseGroove(1); buzz(); judgeTxt = { g: 'K', t: st }; }
    return;
  }
  { const cn = notes.find(n => n.st === 'p' && n.k === 'coin' && n.l === lane && Math.abs(t - n.t) <= WO);
    if (cn) { cn.st = 'd'; buddy = Math.min(1, buddy + 0.06); score += 200; coin(); fx.push({ k: 'burst', word: '+COIN', x: TX + 6, y: EY[lane] - 10, t0: st }); return; } }
  if (brokenOn(st)) { buzz(); if (!fx.some(e => e.k === 'banner' && st - e.t0 < 1)) fx.push({ k: 'banner', t0: st, a: CH.brokenTitle || 'GUITAR BROKEN!', b: 'ONLY SPACE WORKS' }); return; }
  let bh = null;
  for (const n of notes) {
    if (n.t - t > WO) break;
    if (n.st !== 'p' || n.l !== lane || n.vic || n.hidden || n.k === 'bomb' || n.k === 'decoy' || n.k === 'coin' || n.bp) continue;
    const e = t - n.t;
    if (Math.abs(e) <= WO && (!bh || Math.abs(e) < Math.abs(bh.e))) bh = { n, e };
  }
  if (!bh) {
    for (const n of notes) {
      if (n.t - t > WO) break;
      if (n.st === 'p' && n.k === 'bomb' && n.l === lane && Math.abs(t - n.t) <= WO) {
        n.st = 'boom'; bombHits[sidx(n)]++; combo = 0; loseGroove(2); heroStumbleAt = st; shake(0.35, 3); bigBoom();
        fx.push({ k: 'bomb', x: TX, l: lane, t0: st }); fx.push({ k: 'banner', t0: st, a: 'BOOM!', b: "DON'T HIT THE BOMBS  -2 GROOVE" });
        if (fever.on) endFever();
        return;
      }
    }
    if (!buddyRun && st - lastMisclick > 0.15) {
      const near = notes.find(o => (o.st === 'p' || o.st === 'x') && !o.hidden && !o.bp && o.k !== 'bomb' && o.k !== 'tape' && o.k !== 'coin' && Math.abs(o.t - t) < 0.45);
      if (near) { lastMisclick = st; loseGroove(1); judgeTxt = { g: near.k === 'decoy' && near.l === lane && Math.abs(near.t - t) <= WO ? 'D' : near.t > t ? 'E' : 'L', t: st }; tone('square', 160, 120, 0.08, 0.04); }
    }
    return;
  }
  award(grade(bh.e), bh.e, bh.n); lastHitAt = st;
  if (notes.some(o => o !== bh.n && Math.abs(o.t - bh.n.t) < 0.01 && o.st === 'd' && o.l !== lane)) { heroJumpAt = st; }
  if (bh.n.k === 'hold') bh.n.st = 'h'; else { bh.n.st = 'd'; killFx(bh.n, TX, true); }
}
function finishHold(n) { n.st = 'd'; score += 200; killFx(n, TX, true); bossHit(); }
function laneRelease(key) {
  const st = songTime(), lane = reversed(st) ? 2 - key : key;
  held[lane] = false;
  const t = judgeTime();
  for (const n of notes) if (n.st === 'h' && n.l === lane) {
    if (t < n.t + n.d - 0.15) { n.st = 'x'; stats[sidx(n)].B++; combo = 0; loseGroove(1); judgeTxt = { g: 'B', t: songTime() }; }
    else finishHold(n);
  }
}
function spacePress() {
  const st = songTime(), t = judgeTime();
  if (corrupted(st)) { buzz(); fx.push({ k: 'banner', t0: st, a: 'CORRUPTED!', b: 'USE W+E+R TOGETHER' }); return; }
  for (const n of notes) {
    if (n.t - t > WO) break;
    if (n.st === 'p' && n.k === 'space' && !n.vic && Math.abs(t - n.t) <= WO) { award(grade(t - n.t), t - n.t, n, 3); n.st = 'd'; blast(n, 'SPACE!'); return; }
  }
}
function blast(n, label) {
  const st = songTime();
  shake(0.16, 2); lastHitAt = st;
  let c = 3;
  for (let l = 0; l < 3; l++) fx.push({ k: 'kill', l, x: TX, t0: st, pop: l !== 1, m: n.m });
  for (const o of notes) if (o.st === 'p' && !o.hidden && o.k !== 'space' && o.k !== 'wall' && o.k !== 'bomb' && o.t > n.t && o.t <= n.t + 0.35) {
    special2(o, TX + (o.t - st) * SPEED);
    o.st = 'k'; stats[sidx(o)].K++; c++; score += 100; bossHit();
    fx.push({ k: 'kill', l: o.l, x: TX + (o.t - st) * SPEED, t0: st, pop: false, m: o.m });
  }
  fx.push({ k: 'shock', t0: st }); fx.push({ k: 'banner', t0: st, a: label, b: 'x' + c + '  NEARBY ONLY' });
  boom(); blip(n.m);
}

// ---------- buddy ----------
function noteX(n, st) {
  if (n.warp) { const dt = n.t - st; if (dt > 0) return TX + SPEED * (n.warp === 'slow' ? (dt < 1.2 ? 0.75 * dt : 0.9 + (dt - 1.2) * 1.25) : n.warp === 'dash' ? (dt < 0.6 ? 1.5 * dt : 0.9 + (dt - 0.6) * 0.75) : (dt < 0.6 ? 0.6 * dt : 0.36 + (dt - 0.6) * 1.2)); }
  return TX + (n.t - st) * SPEED;
}
function laserPos(a) {
  if (a < 0.55) { const s = a / 0.55; return [-50 + 90 * s, 4 + 26 * s - 22 * Math.sin(Math.PI * s)]; }
  if (a < 1.8) return [40, 30 + (a - 0.55) / 1.25 * 46];
  if (a < 2.4) { const s = (a - 1.8) / 0.6; return [40 + 300 * s, 76 - 110 * s]; }
  return null;
}
function sweepX(a) { return -150 + CH.buddy.speed * a; }
function buddyDuration() { const B = CH.buddy; return B.kind === 'sweep' ? (W + 170 + B.ox) / B.speed : B.kind === 'slash' ? 1.8 : B.kind === 'drop' ? 1.7 : B.kind === 'beam' ? 2.3 : 2.4; }
const SLASH_C = [IMP + 40, GY - 44], DROP_C = [176, GY - 18];
function radialR(a) { const B = CH.buddy; if (B.kind === 'slash') return a < 0.75 ? 0 : 40 + (a - 0.75) * 380; return a < 0.55 ? 0 : 20 + (a - 0.55) * 360; }
function bolt(x0, y0, x1, y1, seed) {
  let px = x0, py = y0;
  for (let k = 1; k <= 6; k++) {
    const t = k / 6, j = k < 6 ? Math.sin(seed * 7.1 + k * 3.3) * 6 : 0, nx = x0 + (x1 - x0) * t + j, ny = y0 + (y1 - y0) * t + j * 0.5;
    thick(px, py, nx, ny, 3, '#5a7fd8'); thick(px, py, nx, ny, 1, '#eaf6ff'); px = nx; py = ny;
  }
}
function buddyPress() {
  if (buddy < 1 || buddyRun || (qte && qte.phase !== 'done')) return;
  const st = songTime(), D = buddyDuration(), B = CH.buddy;
  buddy = 0; buddyRun = { t0: st, D, kills: 0, say: P(B.says || B.say) };
  for (const n of notes) if (n.st === 'p' && n.k !== 'bomb' && n.k !== 'tape' && n.t > st - WO && n.t <= st + D + 2.1) n.vic = true;
  flashUntil = st + 0.15; shake(0.45, 4); stinger(B.sfx); say(buddyRun.say.replace(/!+/g, '!'), B.pitch, B.rate); crowd(2.2);
  if (B.sfx === 'boar') setTimeout(() => { for (let i = 0; i < 3; i++) tone('square', 1400 + i * 200, 900, 0.09, 0.04, i * 0.13); }, 900);
}
const BSHOUT = { keytar: ['TUBULAR!', 'GNARLY!', 'RADICAL!', 'BODACIOUS!', 'COWABUNGA!', 'FAR OUT!'], biker: ['YEEHAW!', 'EAT ASPHALT!', 'BORN TO RIDE!', 'NO BRAKES!', 'FULL THROTTLE!', 'RIDE OR DIE!'],
  boar: ['OINK!', 'CHAAARGE!', 'FOR THE KING!', 'HOG WILD!', 'BACON? NEVER!', 'SNORT SNORT!'], reaper: ['TIME IS UP!', 'BOO.', 'DOOOOM!', 'COME WITH ME.', 'MWAHAHA!', 'NO REFUNDS.'],
  dj: ['DROP IT!', 'BASS!', 'HANDS UP!', 'LOUDER!', 'ONE MORE TIME!', 'FEEL THAT?'], headbang: ['HAIR FLIP!', 'BANG IT!', 'METAL!', 'NECKS OF STEEL!', 'WINDMILL!', 'FOR THE HORDE!'], bigband: ['SWING IT!', 'DIG IT!', 'CRAZY, DADDY-O!', 'BE-BOP!', 'HOT JAZZ!', 'TAKE FIVE!'], stampede: ['YEEHAW!', 'GIDDY UP!', 'MOOOVE!', 'STAMPEDE!', 'HOT DANG!', 'RIDE EM!'], basscannon: ['FIRING!', 'MAX BASS!', 'WUB MODE!', 'CHARGING!', 'BOOM!', 'DROP IT!'], cannon: ['FORTISSIMO!', 'TUTTI!', 'BRAVO!', 'FIRE!', 'CRESCENDO!', 'MAESTOSO!'], cart: ['OI OI!', 'NO BRAKES!', 'FASTER!', 'MOSH!', 'CHAOS!', 'ANARCHY!'], pyro: ['FEUER!', 'HOTTER!', 'BURN!', 'FLAMMEN!', 'JA!', 'PYRO!'] };
const BMID = { keytar: ['AIR SOLO!!', 'SHRED IT!!', 'MAX SYNTH!!', 'FLY HIGH!!', 'NEON POWER!!'], biker: ['WHEEEEE!', 'AIRTIME!', 'LOOK MA!', 'YAHOOO!', 'SEND IT!'],
  boar: ['MY CROWN!', 'NOT THE CROWN!', 'CROWN OVERBOARD!', 'ROYAL OOPS!', 'GET THAT CROWN!'], headbang: ['WINDMILL!!', 'HAIR TORNADO!!', 'MAXIMUM MOSH!!', 'WALL OF HAIR!!', 'NECKBREAKER!!'], bigband: ['SHOUT CHORUS!!', 'BRASS ATTACK!!', 'HIGH NOTE!!', 'SWING TIME!!', 'TUTTI!!'], stampede: ['RODEO!!', 'BULL RIDE!!', 'EIGHT SECONDS!!', 'HANG ON!!', 'BUCKAROO!!'], basscannon: ['BASS BEAM!!', 'WOBBLE RAY!!', 'SUB ZERO!!', 'MEGA DROP!!', 'FREQUENCY MAX!!'], cannon: ['1812!!', 'OVERTURE!!', 'GRAND FINALE!!', 'SALUTE!!', 'CANNONADE!!'], cart: ['CART SURF!!', 'WHEELIE!!', 'CROWD SURF!!', 'FULL SEND!!', 'NO HANDS!!'], pyro: ['FLAMMENWERFER!!', 'INFERNO!!', 'WALL OF FIRE!!', 'MAXIMUM PYRO!!', 'FEUERWERK!!'] };
function buddyKill(n, x) {
  const st = songTime();
  n.st = 'k'; n.vic = false; n.hidden = false; special2(n, x);
  const lanes = (n.k === 'space' || n.k === 'wall') ? [0, 1, 2] : [n.l];
  for (const l of lanes) {
    stats[sidx(n)].K++; score += 150; buddyRun.kills++; bossHit();
    if (x < W + 8) fx.push({ k: 'kill', l, x, t0: st, pop: rnd(n) < 0.6, m: n.m, big: true });
  }
  tone('square', mf(60 + (buddyRun.kills * 3) % 36), 0, 0.09, 0.04);
  if (x < W) { const WD = BWORDS[CH.buddy.sfx] || BWORDS.keytar; fx.push({ k: 'burst', word: WD[buddyRun.kills % WD.length], x, y: EY[n.l === -1 ? 1 : n.l] - 14 - (buddyRun.kills % 2) * 6, t0: st, big: buddyRun.kills % 2 === 1 }); shake(0.08, 2); }
}
const BWORDS = { keytar: ['ZAP!', 'PEW PEW!', 'RADICAL!', 'BZZT!', 'KZZAK!', 'FWOOSH!'], biker: ['VROOOM!', 'SCREECH!', 'KA-BLAM!', 'WHAM!', 'CRUNCH!', 'BRAAAP!'],
  boar: ['OINK!', 'THUD!', 'SMASH!', 'KRAKOOM!', 'SQUEAL!', 'BONK!'], reaper: ['SHHNK!', 'SLICE!', 'WHOOSH!', 'GLOOM!', 'BOO!', 'SNIKT!'],
  dj: ['WUB WUB!', 'BOOM!', 'WICKA!', 'DROP!', 'BWAAAP!', 'THUMP!'], headbang: ['HEY!', 'HEY HEY!', 'MOSH!', 'WHIPLASH!', 'THWACK!', 'RAAAH!'], bigband: ['BWAAAP!', 'DOO-WOP!', 'SKIDDLY!', 'BA-DAP!', 'HONK!', 'SWING!'], stampede: ['MOOO!', 'STOMP!', 'THUNDER!', 'MOOOOO!', 'CLOMP!', 'YEEHAW!'], basscannon: ['WUB!', 'WOMP!', 'BWAAAM!', 'ZZZRT!', 'DROP!', 'WUBWUB!'], cannon: ['BOOM!', 'KABOOM!', 'FORTE!', 'BLAM!', 'TA-DAAA!', 'POW!'], cart: ['OI!', 'SMASH!', 'CRASH!', 'WHAM!', 'BASH!', 'RIOT!'], pyro: ['FWOOSH!', 'BRENN!', 'WHOOMPH!', 'FEUER!', 'SIZZLE!', 'KA-BOOM!'] };
const GAGS = {
  keytar: [['KA-BOOM!', 'KRAKA-BOOM!', 'FZZT-BOOM!', 'KABLOOEY!', 'BLAMMO!'], ['...TOTALLY WORTH IT.', '...MY KEYTAR!', '...NAILED THE LANDING.', '...IS MY HAIR OK?', '...ENCORE?']],
  biker: [['KRA-KOOM!', 'KA-RASH!', 'BOOM-SKRT!', 'WHUMPF!', 'KABOOM!'], ["I'M OKAY!", 'NO BRAKES!', 'MEANT TO DO THAT!', 'WHERE IS MY BIKE?', 'AGAIN! AGAIN!']],
  boar: [['THUD!', 'KA-THONK!', 'BONK!', 'SPLAT!', 'WHUMP!'], ['OINK... OW.', 'WHO MOVED THE WALL?', 'MY HAM HURTS.', 'TOTALLY PLANNED.', 'OINK? OINK.']],
  reaper: [['SHUNK!', 'THUNK!', 'KRRK!', 'CHUNK!', 'TWANG!'], ['...THIS IS AWKWARD.', '...STUCK. AGAIN.', '...NOBODY SAW THAT.', '...I NEED A NEW SCYTHE.', '...DEATH IS HARD.']],
  pyro: [['BACKFIRE!', 'POOF!', 'FWUMP!', 'KA-BLAM!', 'PFFFT!'], ['...ZU HEISS.', '...MY EYEBROWS. GONE.', '...TOO MUCH FIRE.', '...SMELLS LIKE STEEL.', '...WUNDERBAR. OW.']],
  cart: [['KER-CRASH!', 'CLATTER!', 'BONK!', 'KA-SPLAT!', 'CRUNCH!'], ['...SORRY, MOM.', '...CLEAN UP ON AISLE 5.', '...DO NOT TELL SECURITY.', '...STILL PUNK.', '...WHO STEERS THIS?']],
  cannon: [['BACKFIRE!', 'KA-BLAM!', 'WHUMP!', 'POOF!', 'BOOM-TSS!'], ['...BRAVO.', '...A BIT MUCH?', '...ENCORE. NEVER.', '...MY EYEBROWS.', '...TCHAIKOVSKY APPROVES.']],
  basscannon: [['KA-BLOOEY!', 'FZZZT-BOOM!', 'OVERLOAD!', 'KRZZK!', 'BZZZAP!'], ['...ERROR 404: BASS NOT FOUND.', '...TOO MUCH WUB.', '...REBOOTING.', '...SPEAKERS BLOWN.', '...WORTH IT. BEEP.']],
  stampede: [['MOO-CRASH!', 'KA-THUD!', 'COW PILE!', 'MOOOMPH!', 'SPLAT!'], ['...THAT IS A LOT OF STEAK.', '...MOO.', '...WHO BROUGHT THE COWS?', '...UDDERLY RIDICULOUS.', '...GOOD BOYS.']],
  bigband: [['KER-RASH!', 'CLANG-A-LANG!', 'KA-BLAMMO!', 'BONG!', 'CRASH-BANG!'], ['...WRONG CHART.', '...WHO TRIPPED?', '...TAKE FIVE.', '...ENCORE? NO.', '...STILL SWINGING.']],
  headbang: [['KONK!', 'BONK BONK!', 'CLONK!', 'KA-THUNK!', 'DOINK!'], ['...MY NECK.', '...WHO TURNED OFF GRAVITY?', '...ENCORE. LATER.', '...SEEING STARS.', '...WORTH IT.']],
  dj: [['SQUISH!', 'SPLORT!', 'KA-THUMP!', 'FLOMP!', 'SQUASH!'], ["...I'M FLAT.", '...BASS WAS TOO HEAVY.', '...STILL GOT THE BEAT.', '...NEEDS MORE SUB.', '...WORTH IT.']] };
function buddyEnd() {
  const st = songTime();
  for (const n of notes) if (n.vic) buddyKill(n, noteX(n, st));
  wipe = { t0: st, n: buddyRun.kills }; boom(); fanfare(); flashUntil = st + 0.12; buddyRun = null;
  const sfx = CH.buddy.sfx;
  if (sfx === 'keytar') setTimeout(() => { for (let i = 0; i < 6; i++) tone('square', i % 2 ? 660 : 880, 0, 0.12, 0.05, i * 0.14); }, 950);
  if (sfx === 'biker') setTimeout(() => { bigBoom(); }, 1050);
  if (sfx === 'boar') setTimeout(() => { for (let i = 0; i < 5; i++) tone('square', 1200 + (i % 2) * 300, 800, 0.08, 0.04, i * 0.1); }, 650);
  fx.push({ k: 'gag', t0: st + (CH.buddy.kind === 'laser' ? 0 : 0) }); setTimeout(bigBoom, 60);
}
function updateBuddy(st) {
  const B = CH.buddy, a = st - buddyRun.t0;
  for (const n of notes) if (n.vic && n.t <= st + 0.02) buddyKill(n, TX);
  if (B.kind === 'laser') {
    const p = laserPos(a);
    if (p && a >= 0.55 && a < 1.8) {
      const ang = (a - 0.55) / 1.25 * 40 * Math.PI / 180, ox = p[0] - 6 + B.o[0], oy = p[1] - 6 + B.o[1];
      for (const n of notes) if (n.vic) {
        const x = noteX(n, st);
        if (x < W + 4) { const lanes = (n.k === 'space' || n.k === 'wall') ? [0, 1, 2] : [n.l]; if (lanes.some(l => Math.abs(oy + (x - ox) * Math.tan(ang) - EY[l]) < 9)) buddyKill(n, x); }
      }
    }
  } else if (B.kind === 'beam') {
    if (a > 0.6) { const front = 70 + Math.min(1, (a - 0.6) / 0.6) * (W - 60); for (const n of notes) if (n.vic) { const x = noteX(n, st); if (x <= front && x < W + 4) buddyKill(n, x); } }
    if (a > 0.6 && !buddyRun.fired) { buddyRun.fired = true; bigBoom(); shake(0.8, 5); flashUntil = st + 0.1; }
  } else if (B.kind === 'slash' || B.kind === 'drop') {
    const rad = radialR(a), C0 = B.kind === 'slash' ? SLASH_C : DROP_C;
    if (rad > 0) for (const n of notes) if (n.vic) { const x = noteX(n, st); if (x < W + 4 && Math.hypot(x - C0[0], (n.l < 0 ? EY[1] : EY[n.l]) - C0[1]) <= rad) buddyKill(n, x); }
    if (B.kind === 'drop' && a > 0.55 && !buddyRun.landed) { buddyRun.landed = true; bigBoom(); shake(0.6, 6); flashUntil = st + 0.1; }
  } else {
    const front = sweepX(a) + B.front;
    for (const n of notes) if (n.vic) { const x = noteX(n, st); if (x <= front && x < W + 4) buddyKill(n, x); }
  }
  if (a >= buddyRun.D) buddyEnd();
}

// ---------- quick time events: mini boss at 1-3, finisher on the boss at 1-5 ----------
const QKEYS = ['W', 'E', 'R', 'SPACE'], KEYT = 1.4;
function shapePts(shape, n, cx, cy, r) {
  if (shape === 'circle') return Array.from({ length: n }, (_, k) => [cx + r * Math.cos(-Math.PI / 2 + k * 2 * Math.PI / n), cy + r * Math.sin(-Math.PI / 2 + k * 2 * Math.PI / n)]);
  if (shape === 'triangle') return [[cx, cy - r], [cx + r, cy + r * 0.7], [cx - r, cy + r * 0.7]];
  if (shape === 'line') return Array.from({ length: n }, (_, k) => [cx - r * 1.3 + k * (2.6 * r / (n - 1)), cy + (k % 2 ? 10 : -10)]);
  if (shape === 'zigzag') return Array.from({ length: n }, (_, k) => [cx - 62 + k * 124 / (n - 1), cy + (k % 2 ? 14 : -14)]);
  if (shape === 'square') return [[cx - r, cy - r * 0.75], [cx + r, cy - r * 0.75], [cx + r, cy + r * 0.75], [cx - r, cy + r * 0.75]];
  return [[cx, cy - r], [cx + r, cy], [cx, cy + r], [cx - r, cy]];
}
function shuffle(a) { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }
function newQTE(st, kind) {
  const n = kind === 'boss' ? 5 + Math.floor(Math.random() * 3) : 4 + Math.floor(Math.random() * 4);
  const keys = [];
  for (let k = 0; k < n; k++) { let c; do { c = QKEYS[Math.floor(Math.random() * 4)]; } while (k && c === keys[k - 1]); keys.push(c); }
  const shape = n === 3 ? (Math.random() < 0.5 ? 'triangle' : 'line') : n === 4 ? (Math.random() < 0.5 ? 'square' : 'diamond') : n === 5 ? 'circle' : (Math.random() < 0.5 ? 'circle' : 'zigzag');
  const big = n >= 6, cy = big ? 84 : 78, rad = big ? 38 : 30;
  qte = { kind, phase: kind === 'boss' ? 'active' : 'warn', t0: st, n, keys, pos: shuffle(shapePts(shape, n, 146, cy, rad)), cy, rad, ex: big ? 76 : 64, ey: big ? 58 : 50, k: 0, wrongAt: -9, hitAt: -9,
          endAt: -9, laughAt: -9, failed: 0, res: [], keyStart: st, retryAt: 0 };
  if (kind === 'mini') siren();
}
function qteLaugh(st) { qte.laughAt = st; if (qte.kind === 'boss') boss.laughAt = st; laugh(); shake(0.2, 2); }
function qteAdvance(st, ok) {
  qte.res[qte.k] = ok ? 'ok' : 'fail';
  if (!ok) qte.failed++;
  qte.k++; qte.keyStart = st;
  if (qte.k < qte.n) return;
  qte.endAt = st;
  if (qte.kind === 'mini') {
    miniRes = qte.failed === 0 ? 'K.O.' : 'ESCAPED';
    if (qte.failed === 0) { qte.phase = 'ko'; score += 5000; groove = Math.min(16, groove + 2); boom(); fanfare(); shake(0.4, 3); flashUntil = st + 0.12; const ml = P(CH.lines.mini); celebrate = { t: st + 0.6, txt: U(ml) }; setTimeout(() => voice(ml, CH.voicePitch, 1.1, true), 700); cheerUntil = st + 2.5; crowd(); }
    else { qte.phase = 'fled'; if (st - qte.laughAt > 0.5) qteLaugh(st); }
  } else {
    if (qte.failed === 0) { qte.phase = 'done'; boss.phase = 'ko'; boss.endAt = st; boss.hp = 0; score += 20000; groove = Math.min(16, groove + 4); bigBoom(); victory(); shake(1.0, 4); flashUntil = st + 0.25; say(P(CH.bossLines.ko), B0.pitch, 0.8); const bkl = P(CH.lines.boss); celebrate = { t: st + 1.2, txt: U(bkl) }; setTimeout(() => voice(bkl, CH.voicePitch, 1.05, true), 1600); cheerUntil = st + 5; crowd(2.5); }
    else { qte.phase = 'retry'; qte.retryAt = st + 0.9; }
  }
}
function qteKey(lab) {
  if (!qte || qte.phase !== 'active') return;
  const st = songTime();
  if (lab === qte.keys[qte.k]) {
    qte.hitAt = st; score += 300; combo++; maxCombo = Math.max(maxCombo, combo);
    blip(64 + qte.k * 4); tone('square', mf(76 + qte.k * 4), 0, 0.12, 0.05, 0.06);
    fx.push({ k: 'qhit', t0: st }); shake(0.1, 2); lastHitAt = st;
    if (qte.kind === 'boss') { boss.hitAt = st; boss.hp = Math.max(0.02, boss.hp - 0.025); }
    qteAdvance(st, true);
  } else { qte.wrongAt = st; buzz(); loseGroove(3); combo = 0; qteLaugh(st); }
}
function updateQTE(st) {
  if (!qte && !mbDone && st >= MB.t0) newQTE(st, 'mini');
  if (boss.phase === 'fight' && st >= B0.fin[0] + 1.0 && !qte) { if (!phaseSeen.fin) { phaseSeen.fin = true; say(P(CH.bossLines.fin), B0.pitch, 0.7); } newQTE(st, 'boss'); }
  if (!qte) return;
  if (qte.phase === 'warn' && st - qte.t0 >= 1.5) { qte.phase = 'active'; qte.keyStart = st; }
  if (qte.phase === 'active' && st - qte.keyStart > KEYT) { qte.wrongAt = st; buzz(); loseGroove(3); combo = 0; qteLaugh(st); qteAdvance(st, false); }
  if (qte.kind === 'mini' && (qte.phase === 'ko' || qte.phase === 'fled') && st - qte.endAt > 1.8) { qte.phase = 'done'; mbDone = true; qte = null; }
  else if (qte && qte.kind === 'boss' && qte.phase === 'retry' && st >= qte.retryAt) {
    if (st < B0.fin[1] - 2.2) newQTE(st, 'boss');
    else { qte = null; boss.phase = 'fled'; boss.endAt = st; boss.laughAt = st; laugh(0.1); }
  }
  else if (qte && qte.kind === 'boss' && qte.phase === 'done') qte = null;
}
function miniX(st) {
  const a = st - qte.t0;
  if (a < 1.5) { const s = Math.min(1, a / 1.5); return W + 60 - (W + 60 - 210) * (1 - (1 - s) * (1 - s)); }
  if (qte.phase === 'fled') return 210 + Math.max(0, st - qte.endAt - 0.7) * 260;
  return 210;
}

// ---------- the boss ----------
function updateBoss(st) {
  if (boss.phase === 'none' && st >= B0.t_enter) { boss.phase = 'enter'; boss.enterAt = st; siren(); { const bl = P(CH.bossLines.enter); say(bl, B0.pitch, 0.8); taunt = { who: 'boss', txt: U(bl), t: st + 2.2 }; } }
  if (boss.phase === 'enter' && st - boss.enterAt > 2.2) boss.phase = 'fight';
  if (boss.phase === 'fight') {
    if (B0.rev && !phaseSeen.rev && st >= B0.rev[0]) { phaseSeen.rev = true; glitchSfx(); boss.laughAt = st; { const bl = P(CH.bossLines.rev); say(bl, B0.pitch, 0.8); taunt = { who: 'boss', txt: U(bl), t: st + 2.2 }; } }
    if (B0.rev && !phaseSeen.revEnd && st >= B0.rev[1]) { phaseSeen.revEnd = true; fx.push({ k: 'banner', t0: st, a: 'KEYS RESTORED', b: 'W HIGH  R GROUND AGAIN' }); }
    if (B0.cor && !phaseSeen.cor && st >= B0.cor[0] - 0.8) { phaseSeen.cor = true; glitchSfx(); boss.laughAt = st; { const bl = P(CH.bossLines.cor); say(bl, B0.pitch, 0.8); taunt = { who: 'boss', txt: U(bl), t: st + 1.6 }; } }
    if (B0.cor && !phaseSeen.corEnd && st >= B0.cor[1]) { phaseSeen.corEnd = true; fx.push({ k: 'banner', t0: st, a: 'SPACE IS BACK', b: '' }); }
    if (B0.broken && !phaseSeen.brk && st >= B0.broken[0]) { phaseSeen.brk = true; glitchSfx(); bigBoom(); shake(0.5, 3); boss.laughAt = st; { const bl = P(CH.bossLines.broken); say(bl, B0.pitch, 0.85); taunt = { who: 'boss', txt: U(bl), t: st + 2.2 }; } fx.push({ k: 'guitar', t0: st }); }
    if (B0.helper && !phaseSeen.help && st >= B0.helper[0]) { phaseSeen.help = true; crowd(); { const hl = P(CH.helper.helpLine || CH.helper.line); say(hl, CH.helper.pitch, 1.1); taunt = { who: 'none', txt: '', t: -9 }; } }
    if (B0.helper && !phaseSeen.helpEnd && st >= B0.helper[1]) { phaseSeen.helpEnd = true; fx.push({ k: 'banner', t0: st, a: 'THANKS, ' + CH.helper.name + '!', b: 'YOUR TURN AGAIN' }); voice(P(CH.lines.recover), CH.voicePitch, 1.1, true); }
  }
}
function bossPos(st) {
  if (boss.phase === 'enter') { const s = Math.min(1, (st - boss.enterAt) / 1.6); return [W + 30 - (W + 30 - B0.x) * (1 - (1 - s) * (1 - s)), 0]; }
  if (boss.phase === 'fled') { const a = st - boss.endAt; return [B0.x + a * 40, -a * 90]; }
  if (MW.charge && boss.phase === 'fight') {
    const bar = 240 / (STG[4].bpm || 120), a = MW.charge[0] + bar, b = MW.charge[1];
    if (st >= a && st < b + 0.4) { const p = st < b ? (st - a) / bar : 1 - (st - b) / 0.4; return [B0.x - 90 * Math.max(0, p), 0]; }
  }
  return [B0.x, Math.round(Math.sin(st * 2) * 3)];
}
function bossDraw(st) {
  const vis = st;
  if (boss.phase === 'none') return;
  if (boss.phase === 'ko' && st - boss.endAt > 2.2) return;
  if (boss.phase === 'fled' && st - boss.endAt > 2.5) return;
  const [bx, by0] = bossPos(st), laughing = st - boss.laughAt < 0.9;
  const by = by0 - (laughing ? Math.round(Math.abs(Math.sin((st - boss.laughAt) * 22)) * 4) : 0);
  const hit = st - boss.hitAt < 0.06, ko = boss.phase === 'ko';
  if (!ko || st - boss.endAt < 0.3 || Math.floor(st * 12) % 2) g.drawImage(hit || ko ? B0.flashImg : B0.img, Math.round(bx - B0.ox), GY - B0.oy + by);
  if (!ko && shieldUp()) { const cx = bx - B0.ox + B0.w / 2, cy = GY - B0.oy + B0.h / 2 + by; ring(cx, cy, B0.w / 2 + 8, '#5ef2ff'); ring(cx, cy, B0.w / 2 + 11, '#9af8ff'); if (MX.ping && vis - MX.ping < 0.4) ctext('SHIELDED!', cx, GY - B0.oy - 22 + by, '#5ef2ff', 1, K); }
  if (!ko && (BM.rage || (MW.charge && vis >= MW.charge[0] && vis < MW.charge[0] + 240 / (STG[4].bpm || 120)))) {
    const cx = bx - B0.ox + B0.w / 2, cy = GY - B0.oy + B0.h / 2 + by, p = Math.floor(vis * 10) % 2;
    ring(cx, cy, B0.w / 2 + 4 + p * 2, '#ff3b3b'); if (!BM.rage) text('!', cx - 2, GY - B0.oy - 18 + by, '#ff3b3b', 2);
  }
  if (BM.tele && vis >= BM.tele.t && vis < BM.tele.ta - 1.2 && !ko) {
    const p = Math.floor(vis * 14) % 2, cx = bx - B0.ox + B0.w / 2, cy = GY - B0.oy + B0.h / 2 + by;
    ring(cx, cy, 20 + p * 3, '#ff3b3b'); ring(cx, cy, 26 + p * 3, '#ff9e3d'); text('!', cx - 2, GY - B0.oy - 18 + by, '#ff3b3b', 2);
    R(W - 14, EY[BM.tele.l] - 6, 12, 12, K); R(W - 13, EY[BM.tele.l] - 5, 10, 10, p ? '#ff3b3b' : LC[BM.tele.l]);
  }
  if (vis >= BM.coreStart && vis < BM.coreUntil && !ko) {
    const cx = bx - B0.ox + B0.w / 2, cy = GY - B0.oy + B0.h / 2 + by, r = 8 + Math.round(Math.abs(Math.sin(vis * 8)) * 3);
    disc(cx, cy, r + 3, rgbaOf('#ffd23f', 0.35)); disc(cx, cy, r, '#ffd23f'); disc(cx, cy, r - 3, '#ffffff'); ring(cx, cy, r + 6, '#ffd23f');
    ctext('WEAK SPOT', cx, GY - B0.oy - 12 + by, '#ffd23f', 1, K);
  }
  for (const E of BM.echoes) for (const [i, c] of E.calls.entries()) if (vis >= c.t && vis < c.t + 0.45 && !ko) {
    const ix = bx - B0.ox + 6 + i * 16, iy = GY - B0.oy - 18 + by;
    disc(ix, iy, 7, K); disc(ix, iy, 6, LC[c.l]); text('WER'[c.l], ix - 2, iy - 3, K, 1, null);
  }
  if (laughing && !ko) bubble('HA HA HA!', bx - 70, GY - B0.oy - 18 + by, '#c2260f');
  if (ko) {
    const a = st - boss.endAt, af = a * 25, cx = bx + 15, cy = GY - B0.oy / 2;
    for (let i = 0; i < 9; i++) if (a < 2) boom2(cx + (hsh(i) - 0.5) * 80, cy + (hsh(i + 5) - 0.5) * 80 + a * 20, Math.max(2, 12 - Math.floor(((af + i * 3) % 25) / 2)));
    ring(cx, cy, 10 + af * 6, '#ffffff'); ring(cx, cy, 6 + af * 4, '#ff2a4a');
  }
}
function bossBar(st) {
  if (boss.phase !== 'enter' && boss.phase !== 'fight' && !(boss.phase === 'ko' && st - boss.endAt < 2)) return;
  const bx = Math.max(85, tw(B0.name) + 10), bw = 236 - bx;
  R(0, 169, 240, 11, '#0d0a18'); text(B0.name, 4, 171, '#ffffff', 1, null);
  R(bx, 171, bw, 7, K); R(bx + 1, 172, bw - 2, 5, '#1b1730');
  const w = Math.round((bw - 2) * boss.hp); R(bx + 1, 172, w, 5, '#ff2a4a'); R(bx + 1, 172, w, 1, '#ff8a8a');
}

function update() {
  const st = songTime(), t = judgeTime();
  const ev = EVS.find(e => !e.shown && st >= e.t);
  if (ev) { startEvComic(ev, st); return; }
  const ns = Math.max(runFrom, stageAt(st));
  if (ns !== cur) { if (cur >= runFrom) evalStage(cur); cur = ns; stageBanner = { i: ns, t: st }; stageScore0[ns] = score; }
  if (st > 0.4 && !voiceSaid.start) { voiceSaid.start = true; voice(P(CH.lines.start), CH.voicePitch, 1.1, true); }
  if (!fever.on && groove >= 16 && combo >= 30 && !(qte && qte.phase !== 'done')) startFever(st);
  if (fever.on && st > fever.until) endFever();
  rivalUpdate(st); duetUpdate(st); projUpdate(st); bossMechUpdate(st);
  if (fever.on) {
    while (leadIdx < CH.lead.length && CH.lead[leadIdx][0] < schedTo) leadIdx++;
    while (leadIdx < CH.lead.length && CH.lead[leadIdx][0] <= st + 0.3) {
      const [lt, ld, m] = CH.lead[leadIdx++], d = Math.max(0, lt - st);
      tone('square', mf(m + 12), 0, Math.min(0.22, ld), 0.03, d); tone('triangle', mf(m + 19), 0, 0.18, 0.025, d + 0.03);
    }
    schedTo = st + 0.3;
  } else { schedTo = st + 0.3; }
  recentMiss = recentMiss.filter(x => st - x < 2.5);
  const slump = groove <= 4 || recentMiss.length >= 3, want = slump ? 650 : 20000;
  if (want !== lpTarget && lp) { lpTarget = want; lp.frequency.setTargetAtTime(want, actx.currentTime, slump ? 0.15 : 0.4); }
  if (groove <= 4 && !lowSaid) { lowSaid = true; voice(P(CH.lines.low), CH.voicePitch, 1.2, true); }
  if (lowSaid && groove >= 8) { lowSaid = false; voice(P(CH.lines.recover), CH.voicePitch, 1.1); }
  if (runFrom <= 1 && special('rival', st) && !rival.said) { rival.said = true; { const rl = P(CH.rivalLines.start); taunt = { who: 'rival', txt: U(rl), t: st }; say(rl, CH.rivalLines.pitch, 1.2); } }
  if (CH.special.rival && st >= CH.special.rival[1] && rival.said && !rival.done) {
    rival.done = true; const mine = score - stageScore0[1], theirs = rivalScore(CH.special.rival[1]);
    rival.res = mine >= theirs ? 'WIN' : 'LOSE';
    if (rival.res === 'WIN') { score += 3000; fx.push({ k: 'banner', t0: st, a: 'RACE WON!', b: '+3000  RIVAL DEFEATED' }); celebrate = { t: st, txt: 'SEE YA!' }; crowd(); }
    else { fx.push({ k: 'banner', t0: st, a: 'RIVAL WINS...', b: 'BEAT HER SCORE NEXT TIME' }); { const rl = P(CH.rivalLines.win); taunt = { who: 'rival', txt: U(rl), t: st }; say(rl, CH.rivalLines.pitch, 1.2); } }
  }
  if (special('duet', st) && !duetSaid) { duetSaid = true; fx.push({ k: 'banner', t0: st, a: 'DUET!', b: CH.duet.name + ' JOINS  x1.5 SCORE' }); setTimeout(() => { if (state === 'play') { fx.push({ k: 'banner', t0: songTime(), a: 'INCOMING!', b: 'THEY BROUGHT FRIENDS, OFF THE BEAT' }); siren(); } }, 1500); voice(P(CH.duet.line), CH.duet.pitch, 1.0, true); crowd(); }
  if (encoreOn(st) && !encoreSaid) { encoreSaid = true; fx.push({ k: 'banner', t0: st, a: 'ENCORE!', b: 'VICTORY LAP: NOTHING CAN HURT YOU' }); crowd(2); cheerUntil = st + 7; }
  for (const tp of CH.tips) if (!tipShown[tp.k] && st >= tp.t && st < tp.t + 1) { tipShown[tp.k] = true; tipNow = { txt: tp.txt, t: st }; }
  if (boss.phase === 'fight' && st > nextTaunt && !qte) {
    const T = CH.bossLines.taunts;
    if (nextTaunt) taunt = { who: 'boss', txt: T[Math.floor(st) % T.length], t: st };
    nextTaunt = st + 13;
  }
  for (const n of notes) {
    if (n.t > t + 1) break;
    if (n.st === 'p' && (n.k === 'decoy' || n.k === 'coin') && t - n.t > 0.05) { n.st = 'lost'; continue; }
    if (n.st === 'p' && n.bp && t - n.t > -0.01) { n.st = 'lost'; fx.push({ k: 'kill', l: n.l, x: TX, t0: st, pop: false, m: n.m }); tone('square', mf(n.m + 12), 0, 0.12, 0.05); boss.laughAt = st; continue; }
    if (n.st === 'p' && !n.vic && n.claimed && t - n.t > -0.5) continue;
    if (n.st === 'p' && !n.vic && t - n.t > WO) {
      if (n.k === 'bomb' || n.k === 'tape' || n.hidden) { n.st = n.k === 'bomb' ? 'gone' : 'lost'; continue; }
      n.st = 'x'; missed(n);
    }
    if (n.st === 'h' && t >= n.t + n.d) finishHold(n);
  }
  if (buddyRun) updateBuddy(st);
  updateBoss(st);
  updateQTE(st);
  if (groove <= 0 && !noFail) {
    frozen = st; state = 'failed';
    master.gain.setTargetAtTime(0.0001, actx.currentTime, 0.25);
    const dying = mainSrc; setTimeout(() => { if (mainSrc === dying) stopMain(); master.gain.cancelScheduledValues(0); master.gain.setValueAtTime(0.9, actx.currentTime); }, 1200);
  }
  if (st > CH.total - 0.6) finish(st);
}
function stageNotes(i) { return notes.filter(x => x.s === STG[i].id && x.st !== 'skip' && x.k !== 'bomb' && x.k !== 'tape'); }
function stageAcc(i) { const n = stageNotes(i).length || 1, c = stats[i]; return Math.min(1, (c.P + c.K + c.G * 0.7 + c.O * 0.4) / n); }
function evalStage(i) {
  if (starsRun[i]) return;
  const c = stats[i], acc = stageAcc(i);
  const s = [true, acc >= 0.85, c.M + c.B + bombHits[i] === 0];
  starsRun[i] = s;
  const n = s.filter(Boolean).length;
  if (n > PROG.stars[i]) { PROG.stars[i] = n; saveProg(); }
}
function rivalScore(t) { const w = CH.special.rival; return Math.max(0, notes.filter(x => x.s === STG[1].id && x.t <= Math.min(t, w[1]) && x.k !== 'bomb' && x.k !== 'tape').length * 430 + rival.adj); }
function finish(st) {
  evalStage(cur);
  frozen = st; state = 'clear'; stopMain();
  const rows = STG.map((s, i) => {
    if (i < runFrom) return null;
    const n = notes.filter(x => x.s === s.id && x.st !== 'skip').length || 1, c = stats[i];
    const acc = (c.P + c.K + c.G * 0.7 + c.O * 0.4) / n;
    return { id: s.id, track: s.track, acc: Math.min(1, acc), gr: acc >= 0.95 ? 'S' : acc >= 0.85 ? 'A' : acc >= 0.7 ? 'B' : acc >= 0.5 ? 'C' : 'D' };
  });
  const played = rows.filter(Boolean), acc = played.reduce((a, r) => a + r.acc, 0) / played.length;
  const avg = errs.length ? errs.reduce((a, b) => a + b, 0) / errs.length * 1000 : 0;
  if (runFrom === 0 && score > best) { best = score; try { localStorage.setItem('rr_ch' + CH.num + '_best', String(best)); } catch (e) {} }
  result = { rows, acc, gr: acc >= 0.95 ? 'S' : acc >= 0.85 ? 'A' : acc >= 0.7 ? 'B' : acc >= 0.5 ? 'C' : 'D', avg,
    mini: runFrom > 2 ? '-' : (miniRes || 'ESCAPED'), boss: boss.phase === 'ko' ? 'DEFEATED' : 'RETREATED',
    suggest: Math.max(-250, Math.min(250, Math.round((offsetMs + avg) / 5) * 5)) };
  CH.outfits.forEach((o, i) => { if (i && totalStars() >= o.stars && prevStars < o.stars) unlocks.push('NEW OUTFIT: ' + o.name); });
  tapesRun.forEach(i => unlocks.push('BONUS TRACK: ' + CH.bonus[i].title));
  playLoop('title'); victory();
  if (runFrom === 0 && boss.phase === 'ko') { state = 'comic'; comicNext = 'clear'; comicPage = 'end'; }
}
let comicPage = 'start';
let miniRes = null;

// ---------- rendering ----------
function drawLayers(st, vis) {
  for (const L of st.layers) {
    const im = L.img;
    if (L.type === 'static') g.drawImage(im, 0, L.y);
    else if (L.type === 'scroll') { const w = im.width, off = Math.round((((vis * L.speed) % w) + w) % w); g.drawImage(im, -off, L.y); g.drawImage(im, w - off, L.y); }
    else { const k = ((Math.floor(vis * L.fps) % L.n) + L.n) % L.n; g.drawImage(im, 0, k * L.h, im.width, L.h, 0, L.y, im.width, L.h); }
  }
}
function background(vis, playing) {
  if (!playing) { drawLayers(STG[cur], vis); ambient(STG[cur], vis); return; }
  playing = true;
  const i = stageAt(vis + 0.6);
  if (i > 0 && i > runFrom && vis < STG[i].t0 + 0.9 && vis > STG[i].t0 - 0.6) {
    const wx = Math.round(W - (vis - (STG[i].t0 - 0.6)) / 1.5 * W);
    drawLayers(STG[i - 1], vis); ambient(STG[i - 1], vis);
    g.save(); g.beginPath(); g.rect(wx, 0, W, H); g.clip(); drawLayers(STG[i], vis); ambient(STG[i], vis); g.restore();
    for (let y = 24; y < H; y += 2) Px(wx, y, '#ffffff');
  } else { drawLayers(STG[i], vis); ambient(STG[i], vis); }
  beatFx(vis, STG[i]);
  if (fever.on) { for (let y = 24; y < H; y += 6) { g.fillStyle = 'hsla(' + ((vis * 140 + y * 3) % 360) + ',100%,60%,0.06)'; g.fillRect(0, y, W, 6); } }
  if (helperOn(vis)) { g.fillStyle = 'rgba(255,79,163,0.10)'; g.fillRect(0, 24, W, H - 24); }
  if (playing) {
    g.fillStyle = 'rgba(8,4,18,0.34)'; g.fillRect(0, 24, W, H - 24);
    g.fillStyle = 'rgba(8,4,18,0.38)';
    for (let l = 0; l < 3; l++) g.fillRect(TX - 12, EY[l] - 12, W - TX + 12, 24);
  }
}
function lastBefore(arr, t) { let lo = 0, hi = arr.length - 1, r = -9; while (lo <= hi) { const m = (lo + hi) >> 1; if (arr[m] <= t) { r = arr[m]; lo = m + 1; } else hi = m - 1; } return r; }
function pulse(arr, t, d) { const b = lastBefore(arr, t); return b < 0 ? 0 : Math.max(0, 1 - (t - b) / d); }
function rgbaOf(hex, a) { const n = parseInt(hex.slice(1), 16); return 'rgba(' + (n >> 16) + ',' + ((n >> 8) & 255) + ',' + (n & 255) + ',' + a + ')'; }
function inChorus(t) { return CH.chorus.some(c => t >= c[0] && t < c[1]); }
let KP = 0, SP = 0;
const FANS = [40, 150, 260, 350, 470, 580];
function fans(vis, acc) {
  const cheer = vis < cheerUntil || fever.on || encoreOn(vis);
  for (let i = 0; i < FANS.length; i++) {
    const x = ((FANS[i] - vis * 15) % 640 + 640) % 640;
    if (x > W + 6) continue;
    const jump = cheer ? Math.round(Math.abs(Math.sin(vis * 9 + i)) * 3) : Math.round(KP * 1), y = HZ - 36 - jump;
    R(x - 4, HZ - 30, 9, 2, '#1b1030');
    disc(x, y - 6, 2, '#1b1030'); R(x - 2, y - 4, 5, 6, '#1b1030'); R(x - 1, y - 3, 3, 1, acc);
    if (cheer) { R(x - 4, y - 9 + (i % 2), 1, 5, '#1b1030'); R(x + 4, y - 9 + ((i + 1) % 2), 1, 5, '#1b1030'); if (Math.floor(vis * 4 + i) % 3 === 0) text('!', x - 2, y - 18, '#ffe066', 1, null); }
    else { R(x - 3, y - 3, 1, 4, '#1b1030'); R(x + 3, y - 3, 1, 4, '#1b1030'); }
  }
}
function beatFx(vis, st) {
  KP = pulse(CH.kicks, vis, 0.16); SP = pulse(CH.snares, vis, 0.13);
  const acc = st.acc;
  if (KP > 0) { g.fillStyle = rgbaOf(acc, 0.08 * KP); g.fillRect(0, HZ, W, H - HZ); g.fillStyle = rgbaOf(acc, 0.10 * KP); g.fillRect(0, HZ - 54, W, 30); }
  R(0, HZ, W, 1, KP > 0.5 ? '#ffffff' : acc);
  const nw = Math.floor(SP * 30), seed = Math.floor(vis * 8);
  for (let i = 0; i < nw; i++) Px(hsh(seed * 31 + i) * W, HZ - 4 - hsh(seed * 17 + i) * 34, ['#ffe066', '#5ef2ff', '#ff7ac8'][i % 3]);
  if (inChorus(vis)) {
    g.fillStyle = 'rgba(255,255,255,0.04)'; g.fillRect(0, 24, W, HZ - 24);
    for (let i = 0; i < 26; i++) { const x = (i * 37 + vis * 20 * (1 + i % 3)) % W, y = 24 + ((i * 53) + vis * (40 + (i % 5) * 12)) % (EY[0] - 38); R(x, y, 2, 1, ['#ff4fa3', '#5ef2ff', '#ffe066', '#7cf06a', '#ffffff'][i % 5]); }
  }
  fans(vis, acc);
}
function ambient(st, vis) {
  const A = st.amb || {};
  if (A.stars) for (let k = Math.floor(vis / 2.3) - 1; k <= Math.floor(vis / 2.3); k++) {
    const age = vis - k * 2.3; if (age < 0 || age > 0.5) continue;
    const x0 = 40 + hsh(k) * 220, y0 = 30 + hsh(k + 7) * 40, p = age / 0.5;
    for (let i = 0; i < 14; i++) Px(x0 + p * 60 - i, y0 + (p * 60 - i) / 3, i < 4 ? '#ffffff' : '#ff7ac8');
  }
  if (A.rain) for (let i = 0; i < 70; i++) {
    const x = (i * 47 + vis * 40) % (W + 20) - 10, y = 24 + ((i * 61) + vis * 210) % (H - 24);
    Px(x, y, '#7f9fe0'); Px(x - 1, y + 1, '#7f9fe0'); Px(x - 2, y + 2, '#4f6fb8');
  }
  if (A.data) for (let i = 0; i < 26; i++) {
    const x = (i * 13) % W, sp = 40 + hsh(i) * 60, y = 24 + ((vis * sp + i * 37) % (HZ - 24));
    for (let k = 0; k < 6; k++) Px(x, y - k * 3, k === 0 ? '#aaffbb' : '#2fbf5a');
  }
  if (A.glitch && (Math.floor(vis * 10) % 37 === 0)) for (let k = 0; k < 4; k++) R(0, 30 + hsh(Math.floor(vis * 10) + k) * 120, W, 2, ['#ff2a4a', '#5ef2ff', '#2fbf5a', '#ffffff'][k]);
  if (A.vultures) for (let i = 0; i < 2; i++) {
    const a = vis * 0.8 + i * Math.PI, x = A.vultures[0] + 24 * Math.cos(a), y = A.vultures[1] + 8 * Math.sin(a), fl = Math.floor(vis * 6 + i) % 2;
    for (const [dx, dy] of [[0, 0], [-1, -1 - fl], [1, -1 - fl], [-2, -fl], [2, -fl], [-3, -fl], [3, -fl]]) Px(x + dx, y + dy, '#2a1630');
  }
  if (A.embers) for (let i = 0; i < 26; i++) Px((i * 53 + vis * 9 + 7 * Math.sin(vis + i)) % W, GY - 4 - ((vis * 22 + i * 37) % (GY - 34)), i % 3 ? '#ff7a1a' : '#ffb02e');
  if (A.eruptions) for (let j = Math.floor(vis / 1.9) - 1; j <= Math.floor(vis / 1.9); j++) {
    const age = vis - j * 1.9; if (age < 0 || age > 1.1) continue;
    const x = 120 + hsh(j * 3) * 190, h = Math.sin(Math.min(1, age / 0.4) * Math.PI / 2) * 30 * (age < 0.8 ? 1 : (1.1 - age) / 0.3);
    R(x - 3, GY - 2 - h, 6, h, '#ff5a1f'); R(x - 1, GY + 2 - h, 2, Math.max(0, h - 4), '#ffe066');
    for (let d = 0; d < 5; d++) disc(x + (hsh(j * 5 + d) - 0.5) * 34 * age, GY - 2 - h - 18 * age + 40 * age * age, 1, '#ffb02e');
  }
  if (A.lightning) for (let j = Math.floor(vis / 5.3) - 1; j <= Math.floor(vis / 5.3); j++) {
    const age = vis - j * 5.3 - 2; if (age < 0 || age > 0.16) continue;
    g.fillStyle = 'rgba(220,230,255,0.22)'; g.fillRect(0, 24, W, HZ - 24);
    const x = 140 + hsh(j) * 160; bolt(x, 24, x - 20 + hsh(j + 1) * 40, HZ - 30, j);
  }
  if (A.spots) for (let b = 0; b < 3; b++) {
    const ang = (-90 + 28 * Math.sin(vis * 0.7 + b * 2.1)) * Math.PI / 180, x0 = 60 + b * 100, y0 = HZ;
    g.fillStyle = 'rgba(255,240,200,0.07)'; g.beginPath(); g.moveTo(x0 - 3, y0); g.lineTo(x0 + Math.cos(ang - 0.12) * 140, y0 + Math.sin(ang - 0.12) * 140);
    g.lineTo(x0 + Math.cos(ang + 0.12) * 140, y0 + Math.sin(ang + 0.12) * 140); g.lineTo(x0 + 3, y0); g.fill();
  }
  if (A.streaks) for (let i = 0; i < 14; i++) { const y = 30 + (i * 37) % (HZ - 34), x = W - ((vis * (280 + i * 30) + i * 97) % (W + 80)); R(x, y, 24 + i % 3 * 10, 1, ['#ff4fa3', '#5ef2ff', '#ffe066', '#ffffff'][i % 4]); }
  if (A.spores) for (let i = 0; i < 22; i++) Px((i * 47 + Math.sin(vis + i) * 6 + W) % W, HZ - ((vis * 9 + i * 29) % (HZ - 30)), i % 3 ? '#2fd8c8' : '#9af8ff');
  if (A.ash) for (let i = 0; i < 40; i++) { const x = ((i * 41 - vis * 18) % W + W) % W, y = 24 + ((i * 37) + vis * 26) % (H - 24); R(x, y, 2, 1, i % 4 ? '#8a7e88' : '#c8bcc4'); }
  if (A.glitter) for (let i = 0; i < 6; i++) { const k = Math.floor(vis * 5 + i * 1.7); if (k % 3 === 0) { const x = hsh(k + i) * W, y = HZ - 10 + hsh(k * 3 + i) * 12; Px(x, y, '#ffffff'); Px(x - 1, y, '#ffe066'); Px(x + 1, y, '#ffe066'); Px(x, y - 1, '#ffe066'); Px(x, y + 1, '#ffe066'); } }
}
function hammerless() {}
function heroDraw(vis) {
  const h = CH.hero, f = ((Math.floor(vis * h.fps) % h.n) + h.n) % h.n;
  const ja = vis - heroJumpAt, jy = ja >= 0 && ja < 0.42 ? -Math.round(Math.sin(Math.PI * ja / 0.42) * 10) : 0;
  const sa = vis - heroStumbleAt, sx = sa >= 0 && sa < 0.3 ? -2 + (Math.floor(vis * 40) % 2) : 0;
  const ca = celebrate ? vis - celebrate.t : -1, cy = ca >= 0 && ca < 1.4 ? -Math.round(Math.abs(Math.sin(ca * 7)) * 7) : 0;
  const yy = jy + cy;
  if (jy || fever.on) for (let k = 0; k < 6; k++) Px(h.x - 6 - k * 3, GY - 12 + yy + (k % 2) * 4 + Math.sin(vis * 20 + k) * 2, ['#ffe066', '#ff7ac8', '#5ef2ff'][k % 3]);
  if (helperOn(vis)) {
    const hp = CH.helper, hf = ((Math.floor(vis * hp.fps) % hp.n) + hp.n) % hp.n;
    g.globalAlpha = 0.85; g.drawImage(heroImg(), f * h.cw, 0, h.cw, h.ch, 6 - h.ax, GY - h.ay - 4, h.cw, h.ch); g.globalAlpha = 1;
    g.drawImage(hp.img, hf * hp.cw, 0, hp.cw, hp.ch, hp.x - hp.ax, GY - hp.ay + yy, hp.cw, hp.ch);
    const tp = hp.tips[hf];
    return [[hp.x + tp[0], GY + tp[1] + yy], [hp.x + tp[2], GY + tp[3] + yy]];
  }
  const tier = combo >= 200 ? 5 : combo >= 150 ? 4 : combo >= 100 ? 3 : combo >= 50 ? 2 : combo >= 25 ? 1 : 0;
  const la = vis - heroLungeAt, lx = la >= 0 && la < 0.3 ? -Math.round(Math.sin(Math.PI * la / 0.3) * 14) : 0;
  const cxh = h.x + 2 + sx + lx, cyh = GY - 14 + yy;
  if (tier >= 1) {
    const col = tier >= 4 ? '#ffd23f' : CH.acc, rr = 15 + Math.round(KP * 3) + (tier >= 4 ? 3 : 0);
    disc(cxh, cyh, rr, rgbaOf(col, tier >= 4 ? 0.3 : 0.2)); ring(cxh, cyh, rr, col);
    if (tier >= 2) ring(cxh, cyh, rr + 3, rgbaOf(col, 0.5));
  }
  if (tier >= 3) {
    g.globalAlpha = 0.25; g.drawImage(heroImg(), f * h.cw, 0, h.cw, h.ch, h.x - h.ax + sx + lx - 9, GY - h.ay + yy, h.cw, h.ch);
    g.globalAlpha = 0.12; g.drawImage(heroImg(), f * h.cw, 0, h.cw, h.ch, h.x - h.ax + sx + lx - 18, GY - h.ay + yy, h.cw, h.ch); g.globalAlpha = 1;
    for (let k = 0; k < 3; k++) if (Math.floor(vis * 12 + k) % 3 === 0) { const a = hsh(Math.floor(vis * 12) + k * 5) * Math.PI * 2, r0 = 18; const x0 = cxh + Math.cos(a) * r0, y0 = cyh + Math.sin(a) * r0; thick(x0, y0, x0 + 3, y0 - 3, 1, '#9af8ff'); thick(x0 + 3, y0 - 3, x0 + 1, y0 - 6, 1, '#ffffff'); }
  }
  g.drawImage(heroImg(), f * h.cw, 0, h.cw, h.ch, h.x - h.ax + sx + lx, GY - h.ay + yy, h.cw, h.ch);
  if (tier >= 5) { for (let a = 0; a < 360; a += 20) { const t = a * Math.PI / 180; Px(cxh + 7 * Math.cos(t), GY - 32 + yy + 2 * Math.sin(t), '#ffd23f'); } }
  if (brokenOn(vis)) { const k = Math.floor(vis * 10) % 2; Px(h.x + 10, GY - 14 + yy, '#ffe066'); Px(h.x + 12 + k, GY - 16 + yy, '#ffffff'); Px(h.x + 8 - k, GY - 17 + yy, '#ff9e3d'); }
  if (sa >= 0 && sa < 0.45) { text('!', h.x - 2, GY - 40, '#ff3b3b', 2); }
  if (ca >= 0 && ca < 1.6) bubble(celebrate.txt, h.x - 6, GY - 48 + yy, '#c8327f');
  const tp = h.tips[f];
  let hi = [h.x + tp[0] + sx, GY + tp[1] + yy], lo = [h.x + tp[2] + sx, GY + tp[3] + yy];
  if (CH.hammer) {
    const hm = CH.hammer, age = vis - lastHitAt, i = age < 0.04 ? 1 : age < 0.08 ? 2 : age < 0.12 ? 3 : age < 0.16 ? 4 : 0;
    g.drawImage(hm.img, i * 64, 0, 64, 64, hi[0] - 32, hi[1] - 32, 64, 64);
    R(hi[0] - 1, hi[1] - 1, 3, 3, K); Px(hi[0], hi[1], '#f2b98c');
    hi = [hi[0] + hm.heads[i][0], hi[1] + hm.heads[i][1]]; lo = hi;
  }
  if (tier >= 2) {
    const big = tier >= 4;
    flame(hi[0], hi[1], big ? 10 : 7, big, vis);
    if (!CH.hammer) { flame(lo[0], lo[1], big ? 8 : 5, big, vis + 0.3); flame((hi[0] + lo[0]) / 2, (hi[1] + lo[1]) / 2, 5, big, vis + 0.6); }
    for (let k = 0; k < 4; k++) { const ph = (vis * 3 + k * 0.25) % 1; R(cxh - 10 - ph * 18, cyh + 6 - k * 3, 2, 1, ph < 0.5 ? '#ffb02e' : '#ff3b3b'); }
  }
  return [hi, lo];
}
function helperOn(t) { return !!(B0.helper && t >= B0.helper[0] && t < B0.helper[1]); }
function brokenOn(t) { return !!(B0.broken && t >= B0.broken[0] && t < B0.broken[1]); }
function rivalDraw(vis) {
  const w = CH.special.rival; if (!w || vis < w[0] - 0.5 || vis > w[1] + 2.5) return;
  const h = CH.hero, f = ((Math.floor(vis * h.fps + 3) % h.n) + h.n) % h.n;
  const diff = rivalScore(vis) - (score - stageScore0[1]), ent = Math.min(1, (vis - w[0] + 0.5) / 0.8), lv = vis > w[1] ? (vis - w[1]) * 90 : 0;
  let x = Math.round(-30 + ent * 46 + Math.max(-1, Math.min(1, diff / 2500)) * 16 + lv), y = GY - h.ay - 6, ang = 0;
  if (rival.state === 'wind') { const a = Math.min(1, (vis - (rival.kickT - 0.9)) / 0.9); x = Math.round(x + (h.x - 14 - x) * a); y -= Math.round(Math.sin(a * Math.PI) * 3); }
  if (rival.state === 'recover') { const a = Math.min(1, (vis - rival.hitAt) / 0.6); x = Math.round(h.x - 14 + (x - h.x + 14) * a); }
  if (rival.state === 'ko') { const a = vis - rival.koAt; if (a < 1.2) { x = Math.round(x - a * 140); y -= Math.round(Math.sin(Math.min(1, a / 0.6) * Math.PI) * 18); ang = -a * 9; } else x = -60; }
  if (x > -40) {
    g.save(); g.translate(x, y + h.ch / 2); g.rotate(ang); g.globalAlpha = 0.95;
    g.drawImage(CH.rivalImg, f * h.cw, 0, h.cw, h.ch, -h.ax, -h.ch / 2, h.cw, h.ch); g.restore(); g.globalAlpha = 1;
    if (rival.state === 'wind') { text('!', x - 2, y - 14, '#ff3b3b', 2); }
    if (rival.yoinkAt && vis - rival.yoinkAt < 0.45 && rival.yoinkT) for (const n of rival.yoinkT) { if (n.st !== 'p') continue; const tx = noteX(n, vis), ty = laneY(n.swAt !== undefined && vis < n.swAt + 0.35 ? n.swFrom : n.l); thick(x + 8, y + 12, tx, ty, 1, '#c8ccd8'); R(tx - 2, ty - 2, 4, 4, '#ffe066'); }
    if (rival.state === 'recover' && vis - rival.hitAt < 0.25) { R(x + 6, GY - 10, 10, 3, K); R(x + 7, GY - 9, 8, 1, '#e8344e'); }
  }
  if (kickReady && vis < w[1] && rival.state !== 'ko') {
    const bx = Math.max(4, x - 30), by = GY - 64;
    if (Math.floor(vis * 6) % 2) { R(bx, by, 86, 12, K); R(bx + 1, by + 1, 84, 10, '#ffe066'); text('Q: KICK BACK!', bx + 4, by + 3, K, 1, null); }
  }
}
function kickBack() {
  const st = songTime(), w = CH.special.rival;
  if (!kickReady || !w || st >= w[1] || rival.state === 'ko' || runFrom > 1) return;
  kickReady = false; kbBase = combo; heroLungeAt = st; rival.state = 'ko'; rival.koAt = st; rival.adj -= 2500; score += 1000;
  rival.next = Math.max(rival.next, st + 9); shake(0.4, 4); bigBoom(); fx.push({ k: 'burst', word: 'POW!', x: 40, y: GY - 30, t0: st, big: true });
  { const rl = P(CH.rivalLines.hurt); say(rl, CH.rivalLines.pitch, 1.2); taunt = { who: 'rival', txt: U(rl), t: st + 0.4 }; }
}
function rivalUpdate(st) {
  const w = CH.special.rival;
  if (!w || runFrom > 1 || st < w[0] || st >= w[1]) return;
  if (!rival.init) { rival.init = true; rival.next = w[0] + 7; rival.tauntNext = w[0] + 4; rival.yoinkNext = w[0] + 11; rival.snatchNext = w[0] + 16; kbBase = combo; }
  if (rival.state === 'idle' && st >= rival.snatchNext && st < w[1] - 3 && !buddyRun) {
    rival.snatchNext = st + 14; if (rival.next < st + 3) rival.next = st + 3.5;
    if (buddy > 0.05) {
      const stolen = Math.min(buddy, 0.35); fx.push({ k: 'snatch', t0: st, from: buddy, amt: stolen }); buddy -= stolen; rival.adj += 800;
      noise(0.2, 0.25, 5000, 1500, 'bandpass'); tone('square', 900, 300, 0.25, 0.05);
      fx.push({ k: 'burst', word: 'SNATCH!', x: 120, y: 70, t0: st, big: true }); taunt = { who: 'rival', txt: U(P(CH.rivalLines.snatch || ['Your buddy is mine!', 'Thanks for the meter!', 'Mine now!', 'Finders keepers!', 'Yoink, again!'])), t: st + 0.2 };
    }
  }
  if (rival.state === 'idle' && st >= rival.yoinkNext && st < w[1] - 3 && !(qte && qte.phase !== 'done') && !buddyRun) {
    rival.yoinkNext = st + 9.5; if (rival.next < st + 3) rival.next = st + 3.5;
    const pool = notes.filter(n => n.st === 'p' && n.k === 'tap' && !n.vic && !n.hidden && !n.part2 && n.child === undefined && n.sw === undefined && !n.claimed && n.t - st > 1.0 && n.t - st < 2.1);
    const picks = pool.filter((n, i) => i % 2 === 0).slice(0, 4);
    if (picks.length) {
      rival.yoinkAt = st; rival.yoinkT = picks.slice();
      picks.forEach((n, k) => { n.swFrom = n.l; n.l = (n.l + 1 + Math.floor(hsh(n.t * 13) * 2)) % 3; n.swAt = st + 0.12 * k; });
      noise(0.18, 0.2, 7000, 2500, 'highpass'); tone('square', 300, 1200, 0.2, 0.05);
      fx.push({ k: 'burst', word: 'YOINK!', x: noteX(picks[0], st), y: EY[picks[0].l] - 18, t0: st + 0.15, big: true });
      taunt = { who: 'rival', txt: U(P(CH.rivalLines.yoink || ['Mixed up yet?', 'Wrong lane!', 'Oops, my bad!', 'Guess again!', 'Try this!'])), t: st };
    }
  }
  if (combo < kbBase) kbBase = combo;
  if (!kickReady && combo - kbBase >= 12) { kickReady = true; tick(true); }
  if (rival.state === 'ko' && st - rival.koAt > 4) rival.state = 'idle';
  if (rival.state === 'recover' && st - rival.hitAt > 0.6) rival.state = 'idle';
  if (rival.state === 'idle' && st > rival.tauntNext) { const T = CH.rivalLines.taunts; taunt = { who: 'rival', txt: U(P(T)), t: st }; rival.tauntNext = st + 9; }
  if (rival.state === 'idle' && st >= rival.next - 0.9 && st < w[1] - 3 && !(qte && qte.phase !== 'done') && !buddyRun) { rival.state = 'wind'; rival.kickT = rival.next; }
  if (rival.state === 'wind' && st >= rival.kickT) {
    rival.state = 'recover'; rival.hitAt = st; rival.next = st + 9.5; if (rival.yoinkNext < st + 3.5) rival.yoinkNext = st + 4; if (rival.snatchNext < st + 3) rival.snatchNext = st + 3.5;
    loseGroove(2); combo = 0; rival.adj += 1500; shake(0.55, 5); heroStumbleAt = st; boom();
    fx.push({ k: 'burst', word: 'WHAM!', x: CH.hero.x + 6, y: GY - 30, t0: st, big: true });
    { const rl = P(CH.rivalLines.kick); say(rl, CH.rivalLines.pitch, 1.2); taunt = { who: 'rival', txt: U(rl), t: st + 0.3 }; }
  }
}
function duetDraw(vis) {
  const w = CH.special.duet; if (!w || vis < w[0] - 0.6 || vis > w[1] + 1) return null;
  const r = CH.duet, f = ((Math.floor(vis * r.fps) % r.n) + r.n) % r.n;
  const ent = Math.min(1, (vis - w[0] + 0.6) / 0.6), lv = vis > w[1] ? (vis - w[1]) * 120 : 0, x = Math.round(-20 + ent * 34 - lv);
  g.drawImage(r.img, f * r.cw, 0, r.cw, r.ch, x - r.ax, GY - r.ay, r.cw, r.ch);
  if (partnerSay && vis - partnerSay.t < 1.4 && vis >= partnerSay.t) bubble(partnerSay.txt, x - 4, GY - r.ay - 34, '#1b1030');
  const tp = r.tips[f]; duetPos = [x + tp[0], GY + tp[1]]; return duetPos;
}
let duetPos = [20, GY - 20];
function duetUpdate(st) {
  const w = CH.special.duet;
  if (!w || st < w[0] + 1.5 || st > w[1] - 0.5) return;
  if (!duetAct.next) duetAct.next = w[0] + 1.6;
  if (st < duetAct.next || (qte && qte.phase !== 'done') || buddyRun) return;
  duetAct.next = st + 3.4; duetAct.n++;
  const D = CH.duet;
  const target = notes.find(n => n.st === 'p' && !n.vic && !n.hidden && ['tap', 'shield', 'split'].includes(n.k) && n.sw === undefined && n.t - st > 0.9 && n.t - st < 1.9);
  if ((duetAct.n % 2 === 0 && groove < 15) || !target) {
    partnerSay = { txt: U(P(D.healLine)), t: st }; projs.push({ kind: D.healKind, t0: st, dur: 0.6, from: duetPos.slice(), heal: true });
  } else {
    target.claimed = true; partnerSay = { txt: U(P(D.atkLine)), t: st }; projs.push({ kind: D.kind, t0: st, dur: 0.5, from: duetPos.slice(), n: target });
  }
}
function projUpdate(st) {
  for (const p of projs) if (!p.done && st >= p.t0 + p.dur) {
    p.done = true;
    if (p.heal && p.small) { groove = Math.min(16, groove + 1); fx.push({ k: 'burst', word: '<3', x: CH.hero.x + 4, y: GY - 44, t0: st, big: false }); }
    else if (p.heal) {
      groove = Math.min(16, groove + 2); celebrate = { t: st, txt: U(P(CH.duet.healReact)) }; tone('square', 880, 1760, 0.15, 0.05);
      fx.push({ k: 'burst', word: U(P(CH.duet.healWord)), x: CH.hero.x + 4, y: GY - 44, t0: st, big: false }); fx.push({ k: 'banner', t0: st, a: '+2 GROOVE', b: '' });
    } else if (p.n.st === 'p') {
      const n = p.n, x = noteX(n, st);
      n.st = 'k'; stats[sidx(n)].K++; score += 200; special2(n, x); boom();
      fx.push({ k: 'kill', l: n.l, x, t0: st, pop: true, m: n.m, big: true });
      fx.push({ k: 'burst', word: U(P(CH.duet.atkWord)), x, y: EY[n.l] - 16, t0: st, big: true });
    }
  }
  projs = projs.filter(p => !p.done || st - p.t0 < 3);
}
function projDraw(vis) {
  for (const p of projs) {
    if (p.done) continue;
    const a = Math.min(1, (vis - p.t0) / p.dur);
    const to = p.heal ? [CH.hero.x + 2, GY - 20] : [noteX(p.n, vis), EY[p.n.l]];
    const x = p.from[0] + (to[0] - p.from[0]) * a, y = p.from[1] + (to[1] - p.from[1]) * a - Math.sin(Math.PI * a) * 26;
    const k = p.kind, spin = vis * 20;
    if (k === 'guitar') { const dx = Math.cos(spin) * 6, dy = Math.sin(spin) * 6; thick(x - dx, y - dy, x + dx, y + dy, 3, '#e8344e'); thick(x, y, x - dy * 0.6, y + dx * 0.6, 3, '#9e1c35'); }
    else if (k === 'mug' || k === 'ale') { R(x - 3, y - 3, 7, 8, K); R(x - 2, y - 2, 5, 6, '#c8862a'); R(x - 2, y - 2, 5, 2, '#f4f4f4'); if (a > 0.2) Px(x - 4, y - 4, '#f4f4f4'); }
    else if (k === 'crow') { const fl = Math.floor(vis * 14) % 2; R(x - 3, y - 1, 7, 4, '#0a0612'); R(x + 3, y - 2, 3, 3, '#0a0612'); Px(x + 6, y - 1, '#ffd23f'); R(x - 1, y - 4 + fl * 6, 4, 2, '#1b1424'); }
    else if (k === 'pick') { R(x - 2, y - 2, 5, 3, '#ff9e3d'); R(x - 1, y + 1, 3, 1, '#ff9e3d'); Px(x, y + 2, '#ff9e3d'); }
    else if (k === 'poem') { for (let i = 0; i < 4; i++) Px(x + Math.cos(spin + i) * 4, y + Math.sin(spin + i) * 4, i % 2 ? '#b06bff' : '#e8e6f4'); text('~', x - 2, y - 4, '#e8e6f4', 1, null); }
    else if (k === 'gear') { for (let q = 0; q < 8; q++) { const a2 = spin + q * Math.PI / 4; R(x + Math.cos(a2) * 5 - 1, y + Math.sin(a2) * 5 - 1, 3, 3, '#8a8a98'); } disc(x, y, 4, '#5a5a6a'); disc(x, y, 1, K); }
    else if (k === 'cassette') { R(x - 4, y - 3, 9, 6, K); R(x - 3, y - 2, 7, 4, '#ff4fa3'); R(x - 2, y - 1, 5, 1, '#1b1030'); Px(x - 2, y + 1, '#ffffff'); Px(x + 2, y + 1, '#ffffff'); }
    else if (k === 'vinyl') { disc(x, y, 5, K); disc(x, y, 4, '#1b1424'); disc(x, y, 1, '#ff3b3b'); Px(x + Math.cos(spin) * 3, y + Math.sin(spin) * 3, '#5a5670'); }
    else if (k === 'star') { star4(x, y); star4(x + 2, y); R(x - 3, y - 1, 7, 3, '#ffd23f'); R(x - 1, y - 3, 3, 7, '#ffd23f'); Px(x, y, '#ffffff'); }
    else if (k === 'hype') { text('!!', x - 5, y - 3, ['#ffe066', '#ff4fa3', '#5ef2ff'][Math.floor(vis * 10) % 3], 1, K); }
    else if (k === 'note') { R(x - 2, y, 4, 3, '#ffd23f'); R(x + 1, y - 7, 1, 8, '#ffd23f'); R(x + 1, y - 7, 4, 2, '#ffd23f'); }
    else if (k === 'heart') { R(x - 3, y - 2, 3, 3, '#ff3b6b'); R(x + 1, y - 2, 3, 3, '#ff3b6b'); R(x - 2, y + 1, 5, 2, '#ff3b6b'); Px(x, y + 3, '#ff3b6b'); }
  }
}
function enemyDraw(l, x, flash, yc, gold) {
  const E = CH.enemies, a = E.anch[l], y = (yc === undefined ? EY[l] : yc) - Math.round(KP * 2);
  const dy = y + (l === 2 ? 10 : 0) - a[1];
  if (!flash) { disc(x, y, 12, 'rgba(8,4,18,0.55)'); ring(x, y, 12, LC[l]); }
  if (gold && !flash) g.drawImage(CH.extrasImg, l * 32, 0, 32, 24, Math.round(x) - a[0], dy, 32, 24);
  else g.drawImage(E.img, (l * 2 + (flash ? 1 : 0)) * 32, 0, 32, 24, Math.round(x) - a[0], dy, 32, 24);
}
function laneY(l) { return EY[l]; }
function shieldPending(e) { return notes.some(o => o.e === e && o.k === 'shield' && o.st === 'p'); }
function drawEnemyNote(n, x, vis) {
  if (n.hidden) return;
  if (n.part2 && shieldPending(n.e)) return;
  let y = laneY(n.l), xx = x;
  if (n.child !== undefined && parentKill[n.child]) {
    const p = parentKill[n.child], a = (vis - p.t) / 0.22;
    if (a < 1) { xx = p.x + (x - p.x) * a; y = EY[p.l] + (y - EY[p.l]) * a; }
  }
  if (n.swAt !== undefined && vis - n.swAt < 0.35 && vis >= n.swAt) {
    const a = (vis - n.swAt) / 0.35; y = laneY(n.swFrom) + (laneY(n.l) - laneY(n.swFrom)) * a; xx += (Math.floor(vis * 40) % 2 ? 2 : -2);
  } else if (n.swAt !== undefined && vis < n.swAt) y = laneY(n.swFrom);
  if (n.sw !== undefined) {
    const from = laneY(n.sw), to = laneY(n.l);
    y = x > 205 ? from : x > 165 ? from + (to - from) * (205 - x) / 40 : to;
    if (x > 165) { const up = to < from, ax = Math.round(x) - 16, ay = Math.round(y); for (let r = 0; r < 4; r++) R(ax - r, ay + (up ? -4 + r : 4 - r), 1 + r * 2, 1, '#ffffff'); R(ax, ay - (up ? 0 : 4), 1, 5, '#ffffff'); }
  }
  if (n.k === 'shot') {
    if (x > B0.x - 6) return;
    for (let k = 1; k < 6; k++) disc(xx + k * 6, y, Math.max(1, 5 - k), rgbaOf('#ff3b3b', 0.5 - k * 0.08));
    disc(xx, y, 7, K); disc(xx, y, 6, '#ff3b3b'); disc(xx, y, 3, '#ffe066'); Px(xx - 1, y - 1, '#ffffff');
    for (let k = 0; k < 8; k++) { const a = k * Math.PI / 4 + vis * 8; R(xx + Math.cos(a) * 8, y + Math.sin(a) * 8, 2, 2, '#ff9e3d'); }
    ring(xx, y, 11 + Math.floor(vis * 10) % 3, LC[n.l]); return;
  }
  if (n.k === 'coin') { const w = Math.round(Math.abs(Math.cos(vis * 6)) * 5) + 1; R(xx - w - 1, y - 7, w * 2 + 2, 14, K); R(xx - w, y - 6, w * 2, 12, '#ffd23f'); R(xx - 1, y - 4, 2, 8, '#fff3b0'); return; }
  if (n.turn && Math.floor(vis * 8) % 3 === 0) R(xx - 1, y - 15, 3, 3, '#ff3b3b');
  if (n.hyp) { const a = vis * 7; disc(xx, y, 9, K); disc(xx, y, 8, '#7a3cc8'); for (let k = 0; k < 3; k++) ring(xx, y, 2 + k * 2, k % 2 ? '#ff7ac8' : '#b06bff'); R(xx + Math.cos(a) * 6, y + Math.sin(a) * 6, 2, 2, '#ffffff'); return; }
  if (n.minion) { disc(xx, y, 13, 'rgba(176,107,255,0.3)'); R(xx - 8, y - 15, 2, 5, '#b06bff'); R(xx + 6, y - 15, 2, 5, '#b06bff'); }
  if (n.block) ring(xx, y, 13 + Math.floor(vis * 12) % 2, '#ff3b3b');
  if (n.riff) ring(xx, y, 12, '#7cf06a');
  if (n.k === 'echo') {
    for (let yy = EY[0] - 10; yy < GY; yy += 3) Px(xx, yy, '#8f88b3');
    disc(xx, EY[0] - 18, 5, K); disc(xx, EY[0] - 18, 4, '#5a5670'); text('?', xx - 2, EY[0] - 21, '#ffffff', 1, null); return;
  }
  if (n.k === 'bomb') { disc(xx, y, 12, 'rgba(255,40,40,0.25)'); ring(xx, y, 12, '#ff3b3b'); g.drawImage(CH.extrasImg, (3 + Math.floor(vis * 8) % 2) * 32, 0, 32, 24, Math.round(xx) - 16, y - 14 - Math.round(KP * 2), 32, 24); return; }
  if (n.k === 'tape') {
    disc(xx, y, 12, 'rgba(255,210,63,0.25)');
    g.drawImage(CH.extrasImg, 5 * 32, 0, 32, 24, Math.round(xx) - 16, y - 12, 32, 24);
    for (let k = 0; k < 3; k++) if (Math.floor(vis * 6 + k) % 3 === 0) { const a = vis * 3 + k * 2.1; Px(xx + 14 * Math.cos(a), y + 10 * Math.sin(a), '#ffffff'); }
    return;
  }
  const gold = n.gold || n.crit || encoreOn(vis);
  enemyDraw(n.l, xx, false, y, gold);
  if (gold) for (let k = 0; k < 2; k++) if (Math.floor(vis * 8 + k) % 2) Px(xx - 8 + hsh(Math.floor(vis * 8) + k) * 16, y - 10 + hsh(k + Math.floor(vis * 8)) * 18, '#ffffff');
  if (n.crit) { const a = vis * 4; for (let k = 0; k < 4; k++) { const c = a + k * Math.PI / 2; thick(xx + Math.cos(c) * 11, y + Math.sin(c) * 11, xx + Math.cos(c) * 16, y + Math.sin(c) * 16, 1, '#ffd23f'); } ring(xx, y, 14, '#ffd23f'); }
  if (n.k === 'shield') { ring(xx, y, 13, '#9af8ff'); ring(xx, y, 12, '#5ef2ff'); Px(xx - 7, y - 8, '#ffffff'); Px(xx - 8, y - 7, '#ffffff'); }
  if (n.k === 'split') { R(xx - 7, y - 21, 14, 9, K); text('x3', xx - 5, y - 20, '#ff7ac8', 1, null); }
}
function noteSprite(x, y, k) { g.drawImage(CH.notesImg, (k % 2) * 20, 0, 20, 20, Math.round(x) - 2, Math.round(y) - 2, 20, 20); }
function targets(vis) {
  const rev = reversed(vis), KL = rev ? 'REW' : 'WER';
  const DIM = ['#2f6f80', '#86306a', '#86752f'];
  for (let l = 0; l < 3; l++) for (let x = IMP + 26; x < 302; x += 6) Px(x, EY[l], DIM[l]);
  for (let y = EY[0] - 10; y < GY - 2; y += 2) Px(TX, y, rev ? '#ff3bd8' : '#5a3a8a');
  const pulse = (((vis % 0.5) + 0.5) % 0.5) < 0.08;
  for (let l = 0; l < 3; l++) {
    const y = EY[l], c = rev ? '#ff3bd8' : LC[l], r = pulse ? 9 : 8;
    if (vis - pressAt[l] < 0.1) { disc(TX, y, 7, LC[l]); disc(TX, y, 3, '#ffffff'); }
    bracket(TX, y, r, K, 1); bracket(TX, y, r, c, 0);
    const jx = rev ? (Math.floor(vis * 20) % 2) : 0;
    R(TX + r + 3 + jx, y - 5, 11, 10, K); R(TX + r + 4 + jx, y - 4, 9, 8, c); text(KL[l], TX + r + 6 + jx, y - 3, K, 1, null);
    R(306, y - 5, 11, 10, K); R(307, y - 4, 9, 8, c); text(KL[l], 309, y - 3, K, 1, null);
  }
  if (rev) for (let k = 0; k < 5; k++) R(hsh(Math.floor(vis * 15) + k) * W, 30 + hsh(Math.floor(vis * 15) + k + 3) * 130, 12 + hsh(k) * 40, 1, k % 2 ? '#ff3bd8' : '#5ef2ff');
}
function notesInScene(vis, hi, lo) {
  for (const n of notes) {
    if (n.k !== 'hold' || (n.st !== 'p' && n.st !== 'h')) continue;
    const x0 = n.st === 'h' ? TX : noteX(n, vis), x1 = TX + (n.t + n.d - vis) * SPEED;
    if (x0 > W + 16) break;
    if (x1 < TX - 4) continue;
    const y = EY[n.l], w = Math.max(1, Math.round(Math.min(x1, W) - x0));
    R(x0, y - 4, w, 9, K); R(x0, y - 3, w, 7, LC[n.l]); R(x0, y - 3, w, 2, '#ffffff');
    if (x1 < W) { R(x1 - 2, y - 6, 4, 13, K); R(x1 - 1, y - 5, 2, 11, LC[n.l]); }
  }
  const byT = new Map();
  for (const n of notes) {
    const x = noteX(n, vis);
    if (x > W + 16) break;
    if (n.st !== 'p' || n.k === 'space' || n.k === 'wall' || n.k === 'bomb' || n.k === 'tape' || n.k === 'shot' || n.k === 'echo' || n.k === 'decoy' || n.bp || n.hidden || n.sw !== undefined || n.part2) continue;
    if (!byT.has(n.t)) byT.set(n.t, []);
    byT.get(n.t).push(n.l); byT.get(n.t).x = x;
  }
  for (const [t, ls] of byT) if (ls.length > 1) { const x = ls.x; for (let y = EY[Math.min(...ls)]; y < EY[Math.max(...ls)]; y += 2) Px(x, y, '#ffffff'); }
  for (const n of notes) {
    const x = noteX(n, vis);
    if (x > W + 16) break;
    if ((n.k === 'space' || n.k === 'wall') && n.st === 'p') {
      const wall = n.k === 'wall';
      R(x - 4, EY[0] - 14, 9, GY - EY[0] + 14, K);
      if (wall) { for (let y = EY[0] - 13; y < GY - 1; y++) R(x - 3, y, 7, 1, ['#5a2a8e', '#b06bff', '#05020a', '#ff3bd8'][(y + Math.floor(vis * 30)) % 4]); }
      else { R(x - 3, EY[0] - 13, 7, GY - EY[0] + 12, '#ffd23f'); R(x - 1, EY[0] - 13, 2, GY - EY[0] + 12, '#fff3b0'); }
      ctext(wall ? 'W+E+R' : 'SPACE', x, EY[0] - 24, wall ? '#ff3bd8' : '#ffd23f');
      for (let l = 0; l < 3; l++) if (!(n.got & (1 << l))) enemyDraw(l, x, false);
      continue;
    }
    if (n.st === 'p') {
      const fake = n.k === 'decoy';
      if (fake) g.globalAlpha = Math.floor(vis * 16) % 3 ? 0.22 : 0.5; else if (n.bp) g.globalAlpha = 0.45;
      if (n.big) { const yy = n.l >= 0 ? EY[n.l] : (EY[0] + GY) / 2; g.save(); g.translate(x, yy); g.scale(1.4, 1.4); g.translate(-x, -yy); }
      drawEnemyNote(n, fake ? x + (Math.floor(vis * 20) % 2 ? 2 : -2) : x, vis); g.globalAlpha = 1;
      if (n.big) g.restore();
      if (n.bp) ring(x, EY[n.l], 12, '#ff3b3b');
    }
    if (n.st === 'gone' && x > TX - 60) { g.globalAlpha = 0.5; g.drawImage(CH.extrasImg, 4 * 32, 0, 32, 24, Math.round(x) - 16, EY[n.l] - 14, 32, 24); g.globalAlpha = 1; }
    if (n.st === 'h') {
      enemyDraw(n.l, TX, Math.floor(vis * 12) % 2 === 0);
      const src = n.l < 2 ? hi : lo;
      thick(src[0], src[1], TX - 4, EY[n.l], 3, LC[n.l]); thick(src[0], src[1], TX - 4, EY[n.l], 1, '#ffffff');
    }
  }
}
function gagDraw(a, vis, e) {
  const B = CH.buddy, GG = GAGS[B.sfx] || GAGS.keytar;
  if (!e.G) e.G = [P(GG[0]), P(GG[1])];
  const G = e.G;
  if (B.kind === 'slash' || B.kind === 'drop' || B.kind === 'beam') return gagDraw2(a, vis, G);
  if (B.sfx === 'keytar') {
    if (a < 0.5) { boom2(282, 40, Math.max(2, 14 - Math.floor(a * 20))); boom2(296, 52, Math.max(2, 9 - Math.floor(a * 14))); }
    for (let k = 0; k < 5; k++) disc(282 + Math.sin(k * 2 + a * 3) * 8, 40 - a * 30 - k * 5, 3 + (k % 2), '#5a5670');
    const y = 40 + a * a * 120; g.save(); g.translate(282, y); g.rotate(a * 6); g.drawImage(B.img, -B.img.width / 2, -B.img.height / 2); g.restore();
    for (let k = 0; k < 6; k++) Px(282 + (hsh(k) - 0.5) * 14, y + (hsh(k + 3) - 0.5) * 10, '#1b1030');
    if (a < 0.6) burst(G[0], 260, 46, a, true); else if (a < 1.0) bubble(G[1], 170, Math.min(150, y - 20), '#c8327f');
    if (a > 0.95) {
      R(250, GY - 12, 40, 10, K); R(251, GY - 11, 38, 8, '#3a6aa8'); R(256, GY - 16, 26, 5, K); R(257, GY - 15, 24, 3, '#5a8ad8'); disc(258, GY - 2, 3, K); disc(282, GY - 2, 3, K);
      if (Math.floor(vis * 8) % 2) { R(266, GY - 19, 4, 3, '#ff3b3b'); R(270, GY - 19, 4, 3, '#3b6bff'); }
      g.drawImage(B.img, 258, GY - 30);
      burst('WEE-WOO!', 230, GY - 46, a - 0.95, true); if (a > 1.3) bubble(e.G2 || (e.G2 = P(['...I MEANT TO DO THAT.', '...NICE CAR.', '...PARKING IS HARD.', '...TOTALLY STUCK IT.', '...BEEP BEEP.'])), 120, GY - 66, '#c8327f');
    }
  } else {
    const fx0 = 296, gy = GY;
    if (a < 0.45) { boom2(fx0, gy - 16, Math.max(2, 16 - Math.floor(a * 26))); boom2(fx0 - 14, gy - 8, Math.max(2, 11 - Math.floor(a * 20))); }
    for (let i = 0; i < 5; i++) flame(fx0 - 22 + i * 10, gy - 2, 6, true, vis + i * 0.2);
    if (B.sfx === 'cart') {
      g.save(); g.translate(fx0 - 24, gy - 20); g.rotate(a < 0.3 ? 0 : -Math.min(1.6, (a - 0.3) * 4)); g.drawImage(B.img, 0, 0, B.cw, B.ch, -B.cw / 2, -B.ch / 2, B.cw, B.ch); g.restore();
      for (let k = 0; k < 3; k++) { const p = Math.min(1, Math.max(0, (a - 0.2 - k * 0.1) / 0.6)); R(fx0 - 40 + k * 18 + p * 20, gy - 30 - Math.sin(p * Math.PI) * 30, 5, 7, K); R(fx0 - 39 + k * 18 + p * 20, gy - 29 - Math.sin(p * Math.PI) * 30, 3, 5, ['#7cf06a', '#ff4fa3', '#5ef2ff'][k]); }
      for (let k = 0; k < 4; k++) { const t = vis * 6 + k * 1.57; star4(fx0 - 30 + Math.cos(t) * 16, gy - 46 + Math.sin(t) * 5); }
    } else if (B.sfx === 'cannon') {
      if (a < 0.5) { boom2(fx0 - 20, gy - 20, Math.max(2, 18 - Math.floor(a * 30))); }
      for (let k = 0; k < 8; k++) disc(fx0 - 40 + Math.sin(k * 2 + a * 3) * 16, gy - 30 - a * 30 - k * 5, 4 + k % 3, '#3a3a48');
      g.drawImage(B.img, 0, 0, B.cw, B.ch, fx0 - B.cw + 20, gy - B.oy, B.cw, B.ch);
      for (let k = 0; k < 8; k++) Px(fx0 - 20 + (hsh(k) - 0.5) * 14, gy - 30 + (hsh(k + 3) - 0.5) * 8, '#1b1030');
    } else if (B.sfx === 'stampede') {
      for (let k = 0; k < 5; k++) { const p = Math.min(1, Math.max(0, (a - k * 0.12) / 0.4)); g.save(); g.translate(fx0 - 20 + (k % 2) * 10, gy - 12 - k * 7 * p); g.rotate((k % 2 ? 0.3 : -0.3) * p); g.drawImage(B.img, 0, 0, 30, B.ch, -15, -B.ch / 2, 30, B.ch); g.restore(); }
      for (let k = 0; k < 6; k++) { const t = vis * 6 + k * 1.05; star4(fx0 - 22 + Math.cos(t) * 18, gy - 52 + Math.sin(t) * 5); }
    } else if (B.sfx === 'bigband') {
      g.save(); g.translate(fx0 - 30, gy - B.oy / 2); g.rotate(a < 0.4 ? 0 : Math.min(1.2, (a - 0.4) * 3)); g.drawImage(B.img, 0, 0, B.cw, B.ch, -B.cw / 2, -B.ch / 2, B.cw, B.ch); g.restore();
      for (let k = 0; k < 5; k++) { const t = a * 2.5, ix = fx0 - 40 + k * 14 + Math.cos(k) * t * 30, iy = gy - 30 - Math.sin(Math.PI * Math.min(1, t)) * 40 - k * 3; R(ix, iy, 8, 2, '#ffd23f'); R(ix + 6, iy - 2, 3, 6, '#ffd23f'); }
    } else if (B.sfx === 'headbang') {
      for (let k = 0; k < 4; k++) { const ang = a < 0.4 ? 0 : Math.min(1.5, (a - 0.4) * 4) * (k % 2 ? 1 : -1); g.save(); g.translate(fx0 - 40 + k * 12, gy - B.oy / 2); g.rotate(ang); g.drawImage(B.img, 0, 0, B.cw, B.ch, -B.cw / 2, -B.ch / 2, B.cw, B.ch); g.restore(); }
      for (let k = 0; k < 6; k++) { const t = vis * 6 + k * 1.05; star4(fx0 - 30 + Math.cos(t) * 20, gy - B.oy - 6 + Math.sin(t) * 5); }
    } else if (B.sfx === 'biker') {
      const y = gy - 30 - Math.sin(Math.min(1, a / 0.9) * Math.PI) * 50; g.save(); g.translate(fx0 - 20 + a * 30, y); g.rotate(-a * 8);
      g.drawImage(B.img, 0, 0, B.cw, B.ch, -B.cw / 2, -B.ch / 2, B.cw, B.ch); g.restore();
      if (a > 1.05) { boom2(fx0 - 10, gy - 14, Math.max(2, 18 - Math.floor((a - 1.05) * 30))); if (a > 1.2) bubble(e.G2 || (e.G2 = P(['...MOSTLY.', '...KINDA.', '...STILL OKAY.', '...SEND HELP.', '...TOTALLY FINE.'])), 180, gy - 92, '#c2260f'); }
    } else {
      g.globalAlpha = 0.9; g.drawImage(B.img, 0, 0, B.cw, B.ch, fx0 - B.cw + 10, gy - B.oy, B.cw, B.ch); g.globalAlpha = 1;
      for (let k = 0; k < 4; k++) { const t = vis * 6 + k * 1.57; star4(fx0 - 26 + Math.cos(t) * 12, gy - B.oy - 4 + Math.sin(t) * 4); }
      for (let k = 0; k < 3; k++) { const s0 = 0.55 + k * 0.18, p = Math.min(1, Math.max(0, (a - s0) / 0.35)); if (a > s0) pig(200 + k * 10 + p * 60, gy - 4 - Math.sin(p * Math.PI) * 22 - p * 18 - k * 5, Math.floor(vis * 10) + k); }
      if (a > 1.1) burst(e.G2 || (e.G2 = P(['OINK OINK!', 'SQUEEE!', 'PIG PILE!', 'OINKAPALOOZA!', 'SNORT!'])), 210, gy - 60, a - 1.1, true);
    }
    if (a < 0.6) burst(G[0], fx0 - 30, gy - 40, a, true); else if (a < 1.05 || B.sfx !== 'biker') bubble(G[1], 200, gy - 70, '#c2260f');
  }
}
function pig(x, y, f) {
  const b = f % 2;
  R(x - 5, y - 4, 10, 6, K); R(x - 4, y - 3, 8, 4, '#ff9ab8'); R(x + 3, y - 6, 5, 5, K); R(x + 4, y - 5, 3, 3, '#ff9ab8'); Px(x + 7, y - 4, '#c8577a');
  Px(x + 5, y - 5, K); R(x - 4, y + 2, 1, 1 + b, K); R(x + 2, y + 2, 1, 2 - b, K); Px(x - 6, y - 4, '#ff9ab8'); Px(x - 7, y - 5, '#ff9ab8');
}
function crown(x, y) { R(x - 4, y, 9, 3, '#c98a1a'); R(x - 4, y - 2, 1, 2, '#ffd23f'); R(x, y - 3, 1, 3, '#ffd23f'); R(x + 4, y - 2, 1, 2, '#ffd23f'); R(x - 3, y, 7, 1, '#ffe066'); Px(x, y + 1, '#ff3b3b'); }
function gagDraw2(a, vis, G) {
  const B = CH.buddy;
  if (B.kind === 'beam') {
    const y = 34 + Math.max(0, a - 0.6) * Math.max(0, a - 0.6) * 160, x = 14;
    for (let k = 0; k < 6; k++) disc(x + 20 + Math.sin(k * 2 + a * 4) * 10, 30 - a * 25 - k * 6, 3 + k % 2, '#5a5670');
    g.save(); g.translate(x + 26, y + 19); g.rotate(a > 0.6 ? (a - 0.6) * 3 : Math.sin(a * 40) * 0.05); g.drawImage(B.img, 0, 0, B.cw, B.ch, -B.cw / 2, -B.ch / 2, B.cw, B.ch); g.restore();
    for (let k = 0; k < 5; k++) if (Math.floor(vis * 16 + k) % 3 === 0) star4(x + 10 + k * 9, y + 10 + (k % 2) * 8);
    if (a > 0.3 && a < 0.8) burst(G[0], 90, 60, a - 0.3, true);
    if (a > 0.8) bubble(G[1], 70, 40, '#5a2a8e');
    return;
  }
  if (B.kind === 'slash') {
    const x = 150, gy = GY;
    thick(x + 24, gy - 40, x + 44, gy + 2, 2, '#c8ccd8'); thick(x + 24, gy - 40, x + 6, gy - 46, 2, '#8a8a98');
    const tilt = a < 0.9 ? Math.sin(a * 40) * 0.08 : Math.min(1.4, (a - 0.9) * 3);
    g.save(); g.translate(x, gy - 20); g.rotate(tilt); g.drawImage(B.img, (B.n - 1) * B.cw, 0, B.cw, B.ch, -B.cw / 2, -B.ch / 2 - 10, B.cw, B.ch); g.restore();
    if (a > 0.9) for (let k = 0; k < 8; k++) { const t = (a - 0.9) * 3, bx = x + Math.cos(k * 0.8) * t * 60, by = gy - 30 - Math.sin(k * 0.8 + 0.5) * t * 50, fl = Math.floor(vis * 14 + k) % 2; Px(bx, by, '#05020a'); Px(bx - 1, by - 1 - fl, '#05020a'); Px(bx + 1, by - 1 - fl, '#05020a'); Px(bx - 2, by - fl, '#05020a'); Px(bx + 2, by - fl, '#05020a'); }
    if (a < 0.6) burst(G[0], x + 40, gy - 56, a, true); else bubble(G[1], x - 30, gy - 80, '#5a2a8e');
    if (a > 0.95 && a < 1.5) burst('FLAP FLAP!', x + 80, gy - 70, a - 0.95, false);
  } else {
    const cx = DROP_C[0], gy = GY, tip = Math.min(1.57, Math.max(0, (a - 0.2) * 3.5));
    g.save(); g.translate(cx + 24, gy - 6); g.rotate(tip);
    R(-48, -52, 48, 52, K); R(-47, -51, 46, 50, '#2a2238'); disc(-24, -22, 14, '#05030a'); disc(-24, -22, 9, '#3a3550'); g.restore();
    if (a > 0.65) { g.drawImage(B.img, 0, 0, B.cw, B.ch, cx + 30, gy - Math.round(B.ch * 0.3), B.cw, Math.round(B.ch * 0.3)); }
    if (a > 0.6 && a < 1.1) burst(G[0], cx + 50, gy - 50, a - 0.6, true);
    if (a > 1.0) bubble(G[1], cx - 20, gy - 72, '#c2260f');
  }
}
function star4(x, y) { Px(x, y, '#ffffff'); Px(x - 1, y, '#ffe066'); Px(x + 1, y, '#ffe066'); Px(x, y - 1, '#ffe066'); Px(x, y + 1, '#ffe066'); }
function buddyDraw(vis) {
  const B = CH.buddy, a = vis - buddyRun.t0;
  if (B.kind === 'laser') {
    const p = laserPos(a);
    if (p) {
      if (a < 0.55) for (let k = 0; k < 4; k++) R(p[0] - 10 - k * 8, p[1] + 10 + k * 4, 8, 1, '#ff7ac8');
      if (a >= 0.55 && a < 1.8) { g.save(); g.translate(Math.round(p[0] - 6 + B.img.width / 2), Math.round(p[1] - 6 + B.img.height / 2)); g.rotate((a - 0.55) * 10); g.drawImage(B.img, -B.img.width / 2, -B.img.height / 2); g.restore(); }
      else g.drawImage(B.img, Math.round(p[0] - 6), Math.round(p[1] - 6));
      for (let k = 0; k < 10; k++) { const ph = (a * 1.3 + k * 0.11) % 1; noteSprite(20 + k * 30 + Math.sin(a * 4 + k) * 6, 24 + ph * 130, k); }
      if (a >= 0.55 && a < 1.8) {
        const ang = (a - 0.55) / 1.25 * 40 * Math.PI / 180, ox = p[0] - 6 + B.o[0], oy = p[1] - 6 + B.o[1];
        const cyc = ['#ff4fa3', '#ffe066', '#5ef2ff', '#7cf06a'], fr = Math.floor(vis * 25), tn = Math.tan(ang);
        for (let x = Math.round(ox); x < W; x++) { const y = Math.round(oy + (x - ox) * tn); if (y > H) break; R(x, y - 6, 1, 13, K); for (let k = 0; k < 11; k++) Px(x, y - 5 + k, k === 5 ? '#ffffff' : cyc[(k + fr) % 4]); }
        const rr = 7 + fr % 3; disc(ox, oy, rr, '#ff4fa3'); disc(ox, oy, rr - 2, '#ffe066'); disc(ox, oy, rr - 4, '#ffffff');
      }
      if (a < 1.6) bubble(buddyRun.say, p[0] + 30, p[1] - 14, '#c8327f');
    }
  } else if (B.kind === 'beam') {
    const ry = a < 0.5 ? -40 + (a / 0.5) * 74 : 34 + Math.round(Math.sin(a * 6) * 2), f = Math.floor(a * 12) % B.n;
    const shk = a > 0.6 && a < 2.0 ? (Math.floor(a * 40) % 2 ? 1 : -1) : 0;
    g.drawImage(B.img, f * B.cw, 0, B.cw, B.ch, 14 + shk, ry, B.cw, B.ch);
    const ox = 14 + 44, oy = ry + 18;
    if (a > 0.45 && a < 0.6) { const rr = Math.round((a - 0.45) * 80); disc(ox, oy, rr, '#5ef2ff'); disc(ox, oy, Math.max(1, rr - 3), '#ffffff'); }
    if (a > 0.6 && a < 2.0) {
      const front = 70 + Math.min(1, (a - 0.6) / 0.6) * (W - 60), cyc = B.cols || ['#b06bff', '#5ef2ff', '#ff4fa3', '#ffffff'];
      for (let x = ox; x < front; x += 2) {
        const w1 = Math.sin(x / 9 + a * 30) * 6, top = EY[0] - 14 + w1, bot = GY + 2 - w1;
        R(x, top, 2, bot - top, rgbaOf(cyc[Math.floor((x + a * 300) / 18) % 4], 0.55)); R(x, (top + bot) / 2 - 3, 2, 6, '#ffffff');
      }
      for (let k = 0; k < 3; k++) ring(front, (EY[0] + GY) / 2, 10 + k * 6 + Math.floor(a * 20) % 6, cyc[k]);
    }
    if (a < 1.8) bubble(buddyRun.say, 70, Math.max(30, ry - 14), '#5a2a8e');
    if (a > 0.8 && a < 1.6) burst(buddyRun.mid || (buddyRun.mid = P(BMID.basscannon)), 230, 50, 0.2, true);
  } else if (B.kind === 'slash') {
    const alpha = a < 0.35 ? a / 0.35 : a > 1.45 ? Math.max(0, 1 - (a - 1.45) / 0.3) : 1;
    let f = 0;
    if (a >= 0.4 && a < 0.75) f = 1 + Math.min(3, Math.floor((a - 0.4) / 0.35 * 4));
    else if (a >= 0.75) f = Math.min(B.n - 1, 5 + Math.floor((a - 0.75) / 0.2 * 6));
    g.fillStyle = 'rgba(40,0,60,' + (0.4 * Math.min(1, a / 0.3) * alpha) + ')'; g.fillRect(0, 24, W, H - 24);
    for (let k = 0; k < 7; k++) { const ph = (a * 0.9 + k * 0.14) % 1; const gx = 30 + k * 42, gyy = GY - 10 - ph * 120; disc(gx, gyy, 4, rgbaOf('#e8e6f4', 0.7 * (1 - ph))); Px(gx - 1, gyy - 1, K); Px(gx + 1, gyy - 1, K); R(gx - 1, gyy + 1, 3, 1, K); }
    g.globalAlpha = alpha; g.drawImage(B.img, f * B.cw, 0, B.cw, B.ch, 56 - B.ox, GY - 86 - B.oy, B.cw, B.ch); g.globalAlpha = 1;
    const rad = radialR(a);
    if (rad > 0 && a < 1.5) for (const [k, c] of [[0, '#5a2a8e'], [1, '#b06bff'], [2, '#e8e6f4'], [3, '#ffffff'], [4, '#ffffff'], [5, '#b06bff']]) ring(SLASH_C[0], SLASH_C[1], rad + k, c, -75, 75);
    if (a > 0.2 && a < 1.5) bubble(buddyRun.say, 110, GY - 110, '#5a2a8e');
    if (a > 0.8 && a < 1.5) ctext(buddyRun.mid || (buddyRun.mid = P(['TIME IS UP!!', 'MEMENTO MORI!!', 'LIGHTS OUT!!', 'GAME OVER!!', 'SEE YOU NEVER!!'])), 170, 92, ['#b06bff', '#e8e6f4'][Math.floor(a * 10) % 2], 2);
  } else if (B.kind === 'drop') {
    const y = a < 0.55 ? -90 + (a / 0.55) * (GY - 58 + 90) : GY - 58, sq = a >= 0.55 && a < 0.7 ? 3 : 0;
    if (a < 0.55) for (let k = 0; k < 6; k++) R(DROP_C[0] - 20 + k * 8, y - 10 - k * 6, 1, 14, '#ffffff');
    R(DROP_C[0] - 24, y + sq, 48, 52 - sq, K); R(DROP_C[0] - 23, y + 1 + sq, 46, 50 - sq, '#2a2238');
    const pump = Math.round(KP * 2 + (a > 0.55 ? Math.abs(Math.sin(a * 30)) * 2 : 0));
    disc(DROP_C[0], y + 30, 14 + pump, '#05030a'); disc(DROP_C[0], y + 30, 9 + pump, '#3a3550'); disc(DROP_C[0], y + 30, 3, '#5a5670'); disc(DROP_C[0], y + 10, 5, '#05030a');
    text('BASS', DROP_C[0] - 11, y + 44, '#ffe066', 1, null);
    const f = Math.floor(a * 12) % B.n; g.drawImage(B.img, f * B.cw, 0, B.cw, B.ch, DROP_C[0] - B.cw / 2, y - B.ch + 2, B.cw, B.ch);
    if (a > 0.55) { for (let b = 0; b < 4; b++) { const ang = (a * 2 + b * 1.57), x2 = DROP_C[0] + Math.cos(ang) * 200, y2 = 24 + Math.abs(Math.sin(ang)) * 40; g.fillStyle = rgbaOf(['#ff4fa3', '#5ef2ff', '#ffe066', '#7cf06a'][b], 0.12); g.beginPath(); g.moveTo(DROP_C[0], y); g.lineTo(x2 - 20, y2); g.lineTo(x2 + 20, y2); g.fill(); } }
    const rad = radialR(a);
    if (rad > 0 && a < 1.6) for (let k = 0; k < 3; k++) ring(DROP_C[0], DROP_C[1], Math.max(1, rad - k * 26), ['#ffffff', '#5ef2ff', '#ff4fa3'][k]);
    if (a > 0.55 && a < 0.9) burst(buddyRun.mid || (buddyRun.mid = P(['BASS DROP!', 'WUB-BOOM!', 'DROPPED IT!', 'SUB ATTACK!', 'BOOM BAP!'])), DROP_C[0] + 70, 60, a - 0.55, true);
    if (a < 1.6) bubble(buddyRun.say, DROP_C[0] - 90, Math.max(30, y - 30), '#c2260f');
  } else {
    const x = sweepX(a), f = Math.floor(a * 12) % B.n;
    for (let k = 0; k < 8; k++) R(x - B.ox - 20 - ((k * 37 + Math.floor(a * 80)) % 120), GY - 10 - k * 11, 18, 1, '#ffffff');
    for (let k = 0; k < 6; k++) flame(x - B.ox - 6 - k * 12, GY - 4 - (k % 2) * 3, 4, k < 2, vis + k * 0.17);
    let jy = 0, rot = 0;
    if (B.sfx === 'biker') {
      R(118, GY - 2, 30, 2, K); for (let i = 0; i < 14; i++) R(120 + i * 2, GY - 2 - Math.round(i * 0.9), 2, Math.round(i * 0.9) + 1, '#8a5a2b');
      const fx_ = x + B.front * 0.4; if (fx_ > 140 && fx_ < 250) { const p = (fx_ - 140) / 110; jy = -Math.round(Math.sin(p * Math.PI) * 38); rot = -0.45 + p * 0.65; }
    }
    if (rot) { g.save(); g.translate(Math.round(x - B.ox + B.cw / 2), GY - B.oy + B.ch / 2 + jy); g.rotate(rot); g.drawImage(B.img, f * B.cw, 0, B.cw, B.ch, -B.cw / 2, -B.ch / 2, B.cw, B.ch); g.restore(); }
    else g.drawImage(B.img, f * B.cw, 0, B.cw, B.ch, Math.round(x - B.ox), GY - B.oy + jy, B.cw, B.ch);
    if (B.sfx === 'biker' && jy < -20) { if (!buddyRun.mid) buddyRun.mid = P(BMID.biker); burst(buddyRun.mid, x, GY - B.oy - 30 + jy, 0.2, true); }
    if (B.sfx === 'cart') {
      for (let k = 0; k < 6; k++) { const ph = (a * 2.5 + k * 0.17) % 1; R(x - B.ox - 6 - ph * 40, GY - 6 - (k % 3) * 4, 3, 1, ['#ffe066', '#ff9e3d', '#ffffff'][k % 3]); }
      if (a > 0.5 && a < 1.4) { if (!buddyRun.mid) buddyRun.mid = P(BMID.cart); burst(buddyRun.mid, x - B.ox + 40, GY - B.oy - 24, 0.2, true); }
    }
    if (B.sfx === 'cannon') {
      for (let k = 0; k < 3; k++) { const ph = (a * 2 + k * 0.33) % 1; const bx2 = x - B.ox + 34 + k * 24 + ph * 140, by2 = GY - 22 - Math.sin(ph * Math.PI) * 40; disc(bx2, by2, 3, K); disc(bx2, by2, 2, '#3a3a48'); if (ph > 0.9) boom2(bx2, by2, 6); }
      if (a > 0.5 && a < 1.4) { if (!buddyRun.mid) buddyRun.mid = P(BMID.cannon); burst(buddyRun.mid, x - B.ox + 50, GY - B.oy - 24, 0.2, true); }
    }
    if (B.sfx === 'stampede') {
      for (let k = 0; k < 10; k++) disc(x - B.ox - 10 - k * 9 + Math.sin(a * 9 + k) * 3, GY - 4 - (k % 3) * 3, 4 + k % 3, rgbaOf('#c8a060', 0.6 - k * 0.05));
      if (a > 0.5 && a < 1.4) { if (!buddyRun.mid) buddyRun.mid = P(BMID.stampede); burst(buddyRun.mid, x - B.ox + 50, GY - B.oy - 24, 0.2, true); }
    }
    if (B.sfx === 'bigband') {
      for (let k = 0; k < 8; k++) { const ph = (a * 1.5 + k * 0.13) % 1; noteSprite(x - B.ox + 10 + k * 9 + Math.sin(a * 6 + k) * 4, GY - B.oy - ph * 60, k); }
      if (a > 0.5 && a < 1.4) { if (!buddyRun.mid) buddyRun.mid = P(BMID.bigband); burst(buddyRun.mid, x - B.ox + 50, GY - B.oy - 24, 0.2, true); }
    }
    if (B.sfx === 'headbang') {
      for (let k = 0; k < 4; k++) { const hx = x - B.ox + 10 + k * 14, hy = GY - B.oy + 6, a0 = a * 26 + k; for (let j = 0; j < 4; j++) thick(hx, hy, hx + Math.cos(a0 + j * 1.57) * 10, hy + Math.sin(a0 + j * 1.57) * 5, 2, ['#b0661e', '#ffd23f', '#1b1030', '#c84a2a'][k % 4]); }
      if (a > 0.5 && a < 1.4) { if (!buddyRun.mid) buddyRun.mid = P(BMID.headbang); burst(buddyRun.mid, x - B.ox + 40, GY - B.oy - 24, 0.2, true); }
    }
    if (B.sfx === 'boar') {
      for (let k = 0; k < 3; k++) pig(x - B.ox - 14 - k * 16, GY - 5 - Math.abs(Math.round(Math.sin(a * 18 + k) * 3)), Math.floor(a * 14) + k);
      if (a > 0.7 && a < 1.9) { const p = (a - 0.7) / 1.2; crown(x - B.ox + 30 - p * 90, GY - B.oy - 6 - Math.sin(p * Math.PI) * 40); if (a < 1.3) { if (!buddyRun.mid) buddyRun.mid = P(BMID.boar); bubble(buddyRun.mid, x - B.ox, GY - B.oy - 36, '#c2260f'); } }
    }
    if (B.bolts) {
      const hx = x + B.heads[f][0], hy = GY + B.heads[f][1], front = x + B.front;
      let c = 0;
      for (const n of notes) if (n.vic && c < 3) { const ex = noteX(n, vis); if (ex > front && ex < front + 140) { bolt(hx, hy, ex, EY[(n.k === 'space' || n.k === 'wall') ? 1 : n.l], n.t + Math.floor(a * 12)); c++; } }
      if (Math.floor(a * 8) % 3 === 0) { g.fillStyle = 'rgba(234,246,255,0.25)'; g.fillRect(0, 24, W, H - 24); }
    }
    const bx = Math.max(10, Math.min(x - B.ox + B.cw * 0.4, W - 120));
    if (a < 1.8) bubble(buddyRun.say, bx, GY - B.oy - 18, '#c2260f');
  }
  if (a < 0.8) {
    const sl = Math.round((1 - Math.min(1, a / 0.12)) * -330) + (a > 0.65 ? Math.round((a - 0.65) * 2200) : 0);
    for (let y = 30; y < 76; y++) { const sh = Math.round((y - 30) / 3); R(sl + sh - 10, y, 340, 1, y < 32 || y > 73 ? '#ffe066' : (y % 4 ? '#1b1030' : '#2a1a48')); }
    for (let k = 0; k < 10; k++) R(sl + ((k * 53 + Math.floor(a * 400)) % 320), 36 + k * 4, 26, 1, '#ffffff');
    ctext(B.name + '!', 140 + sl, 38, '#ffe066', 2, '#c2260f');
    ctext(buddyRun.say, 140 + sl, 58, '#ffffff', 1, K);
    if (a > 0.1) burst('KA-POW!', 268 + sl, 52, a - 0.1, true);
  } else if (a > 0.15) {
    ctext('BUDDY!', 236, 30, '#ffe066', 3); ctext(B.name, 236, 54, '#ffffff'); if (buddyRun.kills) ctext('x' + buddyRun.kills + ' KILLS', 236, 66, ['#ff7ac8', '#ffe066', '#5ef2ff'][Math.floor(a * 10) % 3], 2);
    R(4, 27, 66, 46, K); R(5, 28, 64, 44, '#ffe066'); R(7, 30, 60, 40, '#2a1a48');
    for (let k = 0; k < 8; k++) { const ang = k * Math.PI / 4 + a; thick(37, 50, 37 + Math.cos(ang) * 40, 50 + Math.sin(ang) * 40, 1, '#3a2a60'); }
    g.save(); g.beginPath(); g.rect(7, 30, 60, 40); g.clip();
    if (B.kind === 'laser') g.drawImage(B.img, 0, 0, B.img.width, B.img.height, 37 - B.img.width + Math.round(Math.sin(a * 30)), 52 - B.img.height, B.img.width * 2, B.img.height * 2);
    else { const pf = B.kind === 'slash' ? B.n - 1 : 0; g.drawImage(B.img, pf * B.cw, 0, B.cw, B.ch, 37 - B.cw / 2 + Math.round(Math.sin(a * 30)), 70 - B.ch + (B.kind === 'slash' ? 10 : 0), B.cw, B.ch); }
    g.restore();
    const SH = BSHOUT[B.sfx] || BSHOUT.keytar; bubble(SH[Math.floor(a / 0.55) % SH.length], 66, 30, '#c2260f');
    if (B.sfx === 'keytar' && a > 0.6 && a < 1.5) ctext(buddyRun.mid || (buddyRun.mid = P(BMID.keytar)), 160, 92, ['#ff4fa3', '#ffe066', '#5ef2ff', '#7cf06a'][Math.floor(a * 12) % 4], 2);
  }
  if (a < buddyRun.D) { const c = ['#ff4fa3', '#ffe066', '#5ef2ff', '#7cf06a'][Math.floor(a * 14) % 4]; R(0, 24, W, 2, c); R(0, H - 2, W, 2, c); R(0, 24, 2, H - 24, c); R(W - 2, 24, 2, H - 24, c); }
}
function qteDraw(vis) {
  if (qte.kind === 'mini') {
    const bx = miniX(vis), hit = vis - qte.hitAt < 0.08, laughing = vis - qte.laughAt < 0.9;
    const by = laughing ? -Math.round(Math.abs(Math.sin((vis - qte.laughAt) * 22)) * 4) : 0;
    if (qte.phase !== 'ko' || vis - qte.endAt < 0.15) g.drawImage(hit || qte.phase === 'ko' ? MB.flashImg : MB.img, Math.round(bx - MB.ox + (hit ? 2 : 0)), GY - MB.oy + by);
    if (laughing) bubble('HA HA HA!', bx + 12, GY - MB.oy - 22 + by, '#c2260f');
    if (qte.phase === 'warn') { warnBand(40, vis - qte.t0, 'WARNING!', 'MINI BOSS: ' + MB.name); return; }
    const px = Math.round(bx), top = GY - MB.oy - 12;
    for (let i = 0; i < qte.n; i++) { const x = px - qte.n * 4 + i * 8; R(x, top, 6, 6, K); R(x + 1, top + 1, 4, 4, i < qte.n - qte.k ? '#ff4fa3' : '#2e2a45'); }
    if (qte.phase === 'ko') {
      const age = vis - qte.endAt, af = age * 25, cy = GY - MB.oy / 2;
      for (const [dx, dy, r] of [[0, 0, 12], [-14, 12, 8], [16, -10, 9], [10, 20, 7], [-12, -18, 7]]) if (age < 0.9) boom2(px + dx, cy + dy, Math.max(2, r - Math.floor(af / 5)));
      ring(px, cy, 10 + af * 4, '#ffffff');
      for (let k = 0; k < 6; k++) noteSprite(px - 30 + k * 12, cy - 10 - af * 2 - (k % 2) * 8, k);
      ctext('K.O.!', 200, 30, '#ffe066', 3); ctext('+5000', 200, 54, '#ffffff'); return;
    }
    if (qte.phase === 'fled') { ctext('IT GOT AWAY!', 160, 34, '#ff6b6b', 2); ctext(qte.failed + ' MISSED KEY' + (qte.failed > 1 ? 'S' : '') + ', 3 GROOVE EACH', 160, 52, '#ffffff'); return; }
  } else if (qte.phase === 'retry') {
    ctext('NOT CLEAN!', 146, 60, '#ff6b6b', 2); ctext('AGAIN!', 146, 80, '#ffffff', 2); return;
  } else if (qte.phase !== 'active') return;
  for (const e of fx) if (e.k === 'qhit' && vis - e.t0 < 0.7) {
    const age = vis - e.t0, af = age * 25;
    const tx = qte.kind === 'mini' ? miniX(vis) - 14 : B0.x, ty = qte.kind === 'mini' ? GY - MB.oy / 2 : GY - B0.oy / 2;
    if (age < 0.12) spark(tx, ty);
    noteSprite(tx - 12 + 2 * Math.sin(af / 2), ty - 14 - af, Math.floor(e.t0 * 10) % 2);
  }
  const wrong = vis - qte.wrongAt < 0.4;
  g.fillStyle = 'rgba(13,10,24,0.72)'; g.beginPath(); g.ellipse(146, qte.cy, qte.ex, qte.ey, 0, 0, Math.PI * 2); g.fill();
  for (let k = 0; k < qte.n - 1; k++) {
    const [ax, ay] = qte.pos[k], [bx2, by2] = qte.pos[k + 1], dist = Math.hypot(bx2 - ax, by2 - ay);
    for (let s = 0; s < dist; s += 4) R(ax + (bx2 - ax) * s / dist, ay + (by2 - ay) * s / dist, 2, 2, k < qte.k ? '#7cf06a' : '#5a5670');
  }
  for (let k = 0; k < qte.n; k++) {
    const lab = qte.keys[k], [cx, cy] = qte.pos[k], w = lab === 'SPACE' ? 30 : 14;
    let x = Math.round(cx - w / 2); const y = Math.round(cy - 7);
    const stt = k < qte.k ? (qte.res[k] === 'fail' ? 'bad' : 'done') : k === qte.k ? (wrong ? 'bad' : 'now') : 'todo';
    if (stt === 'bad' && k === qte.k) x += Math.floor(vis * 50) % 2 ? 2 : -2;
    const face = { done: '#7cf06a', now: '#ffe066', todo: '#a8a2c8', bad: '#ff3b3b' }[stt];
    if (stt === 'now' && Math.floor(vis * 8) % 2) { R(x - 3, y - 3, w + 6, 20, '#ffffff'); R(x - 2, y - 2, w + 4, 18, '#0d0a18'); }
    R(x, y, w, 14, K); R(x + 1, y + 1, w - 2, 12, '#5a5670'); R(x + 1, y + 1, w - 2, 10, face);
    ctext(lab, x + w / 2, y + 3, K, 1, null);
    R(x - 5, y - 5, 8, 10, K); R(x - 4, y - 4, 6, 8, stt === 'now' ? '#ff4fa3' : '#2e2a45'); text(String(k + 1), x - 4, y - 4, '#ffffff', 1, null);
    if (stt === 'now' || (stt === 'bad' && k === qte.k)) { const b = Math.round(2 * Math.sin(vis * 10)); for (let r = 0; r < 4; r++) R(cx - 4 + r, y - 13 + b + r, 9 - r * 2, 1, '#ffe066'); }
  }
  ctext(wrong ? 'WRONG KEY!' : (qte.kind === 'boss' ? 'FINISH HIM!' : 'QUICK TIME!  ' + qte.n + ' KEYS'), 146, Math.max(26, qte.cy - qte.rad - 18), wrong ? '#ff3b3b' : '#ffe066');
  const py = qte.cy + qte.rad + 10;
  if (qte.k < qte.n) ctext(wrong ? 'TRY ' + qte.keys[qte.k] : 'PRESS ' + qte.keys[qte.k], 146, py, wrong ? '#ff6b6b' : '#ffffff');
  const left = Math.max(0, 1 - (vis - qte.keyStart) / KEYT);
  R(96, py + 12, 100, 5, K); R(97, py + 13, Math.round(98 * left), 3, left < 0.3 ? '#ff3b3b' : '#7cf06a');
  if (wrong) for (let t = 0; t < 2; t++) { R(t, 24, 1, H - 24, '#ff3b3b'); R(W - 1 - t, 24, 1, H - 24, '#ff3b3b'); R(0, 24 + t, W, 1, '#ff3b3b'); R(0, H - 1 - t, W, 1, '#ff3b3b'); }
}
function swapEY() { const a = EY[0]; EY[0] = EY[2]; EY[2] = a; }
function scene(vis, playing) { const mir = playing && mOn('mirror', vis); if (mir) swapEY(); try { sceneInner(vis, playing); } finally { if (mir) swapEY(); } }
function sceneInner(vis, playing) {
  background(vis, playing);
  if (playing && !(qte && qte.phase !== 'done')) targets(vis);
  if (playing && CH.intro.props && runFrom === 0) { const P = CH.intro.props, x = P.x - (vis + 0.6) * 50; if (x + P.img.width > 0) g.drawImage(P.img, Math.round(x), P.y); }
  if (playing) rivalDraw(vis);
  const rk = playing ? duetDraw(vis) : null;
  const [hi, lo] = heroDraw(vis);
  if (!playing) return;
  bossDraw(vis);
  notesInScene(vis, hi, lo);
  lightsDraw(vis); mechStatus(vis);
  for (const e of fx) {
    const age = vis - e.t0, af = age * 25, y = EY[e.l];
    if (e.k === 'kill') {
      if (age < 0.08) { enemyDraw(e.l, e.x, true); spark(Math.round(e.x), y); }
      else if (age < 0.32) {
        if (e.big) boom2(e.x, y, Math.max(2, 9 - Math.floor(af)));
        ring(e.x, y, 3 + af * 2, Math.floor(af) % 2 ? '#ffffff' : STG[cur].acc);
        for (let k = 0; k < 6; k++) { const a = (k * 60 + e.l * 20) * Math.PI / 180; R(e.x + af * 3 * Math.cos(a), y + af * 3 * Math.sin(a), 2, 2, '#ffe066'); }
      }
      if (e.pop && age < 0.72) noteSprite(e.x - 3 + 2 * Math.sin(af / 2), y - 12 - af, Math.floor(e.m) % 2);
    } else if (e.k === 'atk' && age < 0.12) {
      if (CH.hammer && !helperOn(vis)) { for (const r of [6, 11, 16]) ring(TX, y, r + af, r % 2 ? '#ffe066' : '#ffffff', 120, 240); }
      else waves(hi[0], hi[1], TX - 6, y, [helperOn(vis) ? '#ff4fa3' : CH.acc, '#ffffff']);
      if (rk) waves(rk[0], rk[1], TX - 6, y, [CH.duet.col, '#ffffff'], 3, 2);
    }
    else if (e.k === 'guitar' && age < 1.2) { const h = CH.hero; for (let k = 0; k < 5; k++) { const a = age * 3; R(h.x + 8 + k * 6 * a, GY - 16 - 30 * a + 50 * a * a + k * 2, 3, 2, ['#e8344e', '#9e1c35', '#ffe066', '#c8ccd8', '#e8344e'][k]); } }
    else if (e.k === 'burst' && age < 0.6) burst(e.word, e.x, e.y, age, e.big);
    else if (e.k === 'reflect' && age < 0.3) { const p = age / 0.3, [bx2] = bossPos(vis), x = TX + (bx2 - TX) * p, y = EY[e.l] - Math.sin(p * Math.PI) * 20; disc(x, y, 6, '#5ef2ff'); disc(x, y, 3, '#ffffff'); for (let k = 1; k < 5; k++) Px(x - k * 5, y + k, '#9af8ff'); }
    else if (e.k === 'snatch' && age < 0.6) { const a = age / 0.6, x0 = 160 + 64 * e.from, x1 = 30, y = 16 + (GY - 40 - 16) * a - Math.sin(Math.PI * a) * 20; R(x0 + (x1 - x0) * a - 6, y - 3, 12, 6, K); R(x0 + (x1 - x0) * a - 5, y - 2, 10, 4, '#ffe066'); }
    else if (e.k === 'gag' && age < 2.0) gagDraw(age, vis, e);
    else if (e.k === 'shatter' && age < 0.35) { for (let k = 0; k < 8; k++) { const a = k * Math.PI / 4; R(e.x + Math.cos(a) * (8 + af * 4), EY[e.l] + Math.sin(a) * (8 + af * 4), 2, 2, k % 2 ? '#9af8ff' : '#ffffff'); } }
    else if (e.k === 'bomb' && age < 0.7) { boom2(e.x, EY[e.l], Math.max(2, 16 - Math.floor(af / 1.5))); boom2(e.x + 10, EY[e.l] - 8, Math.max(2, 10 - Math.floor(af / 2))); ring(e.x, EY[e.l], 8 + af * 3, '#ffe066'); }
    else if (e.k === 'qhit' && age < 0.12 && qte) { const tx = qte.kind === 'mini' ? miniX(vis) - 14 : B0.x, ty = qte.kind === 'mini' ? GY - MB.oy / 2 : GY - B0.oy / 2; if (CH.hammer) ring(tx, ty, 8 + af * 2, '#ffe066'); else waves(hi[0], hi[1], tx, ty, [CH.acc, '#ffffff'], 4); }
    else if (e.k === 'shock' && age < 0.45) { const rad = Math.min(36, 6 + af * 6); ring(TX, GY - 44, rad, Math.floor(af) % 2 ? '#ffe066' : '#ffffff', -90, 90); ring(TX, GY - 44, rad - 2, '#ffffff', -90, 90); }
  }
  fx = fx.filter(e => vis - e.t0 < 2.6);
  projDraw(vis);
  if (qte) qteDraw(vis);
  if (buddyRun) buddyDraw(vis);
  // banners, most important first
  var shown = false;
  if (comicEvent(vis)) { shown = true; }
  else if (boss.phase === 'enter') { warnBand(44, vis - boss.enterAt, 'BOSS!', B0.name); shown = true; }
  else if (boss.phase === 'fight' && B0.broken && inWin(vis, [B0.broken[0], B0.broken[0] + 2.2])) { warnBand(44, vis - B0.broken[0], CH.brokenTitle || 'GUITAR BROKEN!', 'LANE KEYS ARE DEAD, ONLY SPACE WORKS'); shown = true; }
  else if (boss.phase === 'fight' && B0.helper && inWin(vis, [B0.helper[0], B0.helper[0] + 2.4])) {
    R(0, 44, W, 30, K); R(0, 45, W, 28, '#2a0a20'); R(0, 45, W, 1, '#ff4fa3'); R(0, 72, W, 1, '#ff4fa3');
    ctext('HELP ARRIVES!', 160, 49, '#ff4fa3', 2); ctext(CH.helper.name + ' TAKES OVER  @ ' + CH.helper.genre, 160, 64, '#ffffff', 1, null); shown = true;
  }
  else if (boss.phase === 'fight' && B0.rev && inWin(vis, [B0.rev[0], B0.rev[0] + 2.2])) { warnBand(44, vis - B0.rev[0], 'KEYS REVERSED!', 'W HITS THE GROUND, R HITS HIGH'); shown = true; }
  else if (boss.phase === 'fight' && B0.cor && inWin(vis, [B0.cor[0] - 0.8, B0.cor[0] + 1.6])) { warnBand(44, vis - B0.cor[0], 'SPACE CORRUPTED!', 'HIT W+E+R TOGETHER ON THE WALLS'); shown = true; }
  else if (boss.phase === 'ko' && vis - boss.endAt < 3) { ctext('BOSS DOWN!', 160, 34, '#ffe066', 3); ctext('+20000', 160, 60, '#ffffff'); shown = true; }
  else if (boss.phase === 'fled' && vis - boss.endAt < 2.5) { ctext('IT RETREATED...', 160, 40, '#ff6b6b', 2); shown = true; }
  if (!shown && !buddyRun && !(qte && qte.phase !== 'done')) {
    const b = fx.find(e => e.k === 'banner' && vis - e.t0 < 1.4);
    if (b) { ctext(b.a, 160, 30, '#ffe066', 2); if (b.b) ctext(b.b, 160, 48, '#ffffff'); shown = true; }
    else if (stageBanner && vis - stageBanner.t < 2.6) {
      const s = STG[stageBanner.i], a = vis - stageBanner.t, slide = Math.max(0, Math.round((0.3 - a) * 400));
      R(0, 40, W, 28, K); R(0, 41, W, 26, '#0d0a18'); R(0, 41, W, 1, s.acc); R(0, 66, W, 1, s.acc);
      ctext('STAGE ' + s.id, 160 + slide, 45, '#ffffff', 2); ctext('@ NOW PLAYING: ' + s.track, 160 + slide, 59, s.acc, 1, null); shown = true;
    } else if (wipe && vis - wipe.t0 < 1.4) { ctext('WIPEOUT!', 200, 34, '#ffe066', 3); ctext('x' + wipe.n + ' ENEMIES  +' + wipe.n * 150, 200, 60, '#ffffff'); shown = true; }
  }
  if (!shown && !buddyRun && !(qte && qte.phase !== 'done') && judgeTxt && vis - judgeTxt.t < 0.4) { const [w, c] = NAMES[judgeTxt.g]; ctext(w, 160, 33 - Math.min(3, (vis - judgeTxt.t) * 25), c, 2); }
  if (combo > 0 && !buddyRun) { text(String(combo), 6, 30, fever.on ? '#ff7ac8' : '#ffe066', 2); text(fever.on ? 'FEVER' : 'COMBO', 6, 47, fever.on ? '#ffe066' : '#ffffff'); }
  if (fever.on && !buddyRun) { const left = Math.max(0, (fever.until - vis) / 12); R(6, 56, 40, 3, K); R(6, 56, Math.round(40 * left), 3, 'hsl(' + ((vis * 200) % 360) + ',100%,60%)'); }
  if (announce && vis - announce.t < 1.2 && !shown) { const a = vis - announce.t, sc = a < 0.1 ? 4 : 3; ctext(announce.txt, 160, 52 - Math.round(a * 6), ['#ffe066', '#ff7ac8', '#5ef2ff'][Math.floor(vis * 10) % 3], sc); }
  if (taunt && vis - taunt.t < 2.2 && vis >= taunt.t) {
    if (taunt.who === 'boss' && (boss.phase === 'fight' || boss.phase === 'enter')) { const [bx, by] = bossPos(vis); bubble(taunt.txt, bx - tw(taunt.txt) - 4, GY - B0.oy + 6 + by, '#c2260f'); }
    if (taunt.who === 'rival') bubble(taunt.txt, 14, GY - 52, '#c2260f');
  }
  if (cameo && vis - cameo.t < 1.8 && !buddyRun) {
    const a = vis - cameo.t, x = Math.round(W - 40 * Math.min(1, a / 0.25) + (a > 1.5 ? (a - 1.5) * 160 : 0));
    g.drawImage(CH.buddy.img, x, 60); bubble(cameo.txt, x - 76, 54, '#c8327f');
  }
  let by = 169;
  if (boss.phase === 'enter' || boss.phase === 'fight' || (boss.phase === 'ko' && vis - boss.endAt < 2)) by -= 12;
  if (runFrom <= 1 && special('rival', vis)) {
    R(0, by, W, 11, '#0d0a18'); R(0, by, W, 1, '#ff3b3b');
    text('YOU ' + String(Math.max(0, score - stageScore0[1])).padStart(6, '0'), 6, by + 2, '#5ef2ff', 1, null);
    ctext('RACE', 160, by + 2, '#ffffff', 1, null);
    rtext('RIVAL ' + String(rivalScore(vis)).padStart(6, '0'), 314, by + 2, '#ff3b3b', 1, null); by -= 12;
  }
  if (tipNow && vis - tipNow.t < 2.6) { const ty = by === 169 ? 169 : 26; R(0, ty, W, 11, K); R(0, ty + 1, W, 9, '#2a1a00'); ctext(tipNow.txt, 160, ty + 2, '#ffe066', 1, null); }
  bossBar(vis);
}
function hud(vis) {
  const s = STG[cur], acc = s.acc;
  R(0, 0, W, 24, '#0d0a18'); R(0, 23, W, 1, acc);
  text('SCORE', 6, 4, '#c9c3e6'); text(String(score).padStart(7, '0'), 6, 13, '#ffffff');
  const low = groove <= 4;
  text('GROOVE', 84, 4, low ? '#ff6b6b' : '#c9c3e6'); meter(84, 14, 64, Math.floor(groove) / 16, low ? '#ff3b3b' : acc);
  if (state === 'play' && vis - lostAt < 0.5) { if (Math.floor(vis * 12) % 2) R(84 + Math.floor(groove) * 4, 14, 4 * lastLoss - 1, 5, '#ffffff'); text('-' + lastLoss, 132, 4, '#ff6b6b'); }
  if (buddy >= 1 && !buddyRun) { text('PRESS B', 160, 4, Math.floor(vis * 6) % 2 ? '#ffe066' : '#ffffff'); meter(160, 14, 64, 1, '#ffe066'); }
  else { text('BUDDY', 160, 4, '#c9c3e6'); meter(160, 14, 64, buddy, '#ffe066'); }
  rtext('STAGE ' + s.id, 314, 4, '#c9c3e6'); rtext(CH.genre, 314, 13, acc);
}
const BTN = { b: [236, 156, 22, 18], space: [262, 156, 52, 18], pause: [298, 27, 16, 13], kick: [176, 156, 56, 18] };
function touchButtons() {
  if (!isTouch) return;
  const [bx, by, bw, bh] = BTN.b, [sx, sy, sw, sh] = BTN.space, [px, py, pw, ph] = BTN.pause;
  R(bx, by, bw, bh, K); R(bx + 1, by + 1, bw - 2, bh - 2, buddy >= 1 ? '#ffe066' : '#5a5670'); ctext('B', bx + bw / 2, by + 6, K, 1, null);
  R(sx, sy, sw, sh, K); R(sx + 1, sy + 1, sw - 2, sh - 2, '#ffd23f'); ctext('SPACE', sx + sw / 2, sy + 6, K, 1, null);
  R(px, py, pw, ph, K); R(px + 1, py + 1, pw - 2, ph - 2, '#e9e4ff'); R(px + 5, py + 3, 2, 7, K); R(px + 9, py + 3, 2, 7, K);
  if (kickReady) { const [kx, ky, kw, kh] = BTN.kick; R(kx, ky, kw, kh, K); R(kx + 1, ky + 1, kw - 2, kh - 2, '#ff3b3b'); ctext('KICK!', kx + kw / 2, ky + 6, '#ffffff', 1, null); }
}
function dimAll(a = 0.62) { g.fillStyle = 'rgba(5,3,10,' + a + ')'; g.fillRect(0, 0, W, H); }

// ---------- menus ----------
function splash(real) {
  drawLayers(STG[0], real); dimAll(0.5);
  ctext('RHYTHM RUNNER', 160, 52, '#ffe066', 3, '#b02c74');
  ctext(state === 'loading' ? 'LOADING...' : (Math.floor(real * 2) % 2 ? (isTouch ? 'TAP TO START' : 'CLICK OR PRESS ANY KEY') : ''), 160, 110, '#ffffff');
}
function titleScreen(real) {
  drawLayers(STG[0], real); ambient(STG[0], real);
  ctext('RHYTHM RUNNER', 160, 40, '#ffe066', 3, '#b02c74');
  ctext('WORKING TITLE', 160, 64, '#c9c3e6', 1, null);
  ctext('CHAPTER ' + CH.num + '  ' + CH.name, 160, 80, CH.acc);
  const f = Math.floor(real * 6) % CH.hero.n;
  g.drawImage(CH.hero.img, f * CH.hero.cw, 0, CH.hero.cw, CH.hero.ch, 150 - CH.hero.ax, GY - CH.hero.ay, CH.hero.cw, CH.hero.ch);
  if (Math.floor(real * 2.5) % 2) ctext(isTouch ? 'TAP TO CONTINUE' : 'PRESS SPACE', 160, 118, '#ffffff');
  if (best) ctext('BEST RUN ' + String(best).padStart(7, '0'), 160, 172, '#c9c3e6', 1, null);
}
const NODES = [[44, 120], [98, 108], [160, 120], [222, 108], [278, 120]];
const STARPIX = ['...#...', '..###..', '#######', '.#####.', '..###..', '.##.##.', '#.....#'];
function star(x, y, on) { for (let r = 0; r < 7; r++) for (let c = 0; c < 7; c++) if (STARPIX[r][c] === '#') Px(x + c, y + r, on ? '#ffd23f' : '#3a3550'); }
function stars3(cx, y, n) { for (let i = 0; i < 3; i++) star(cx - 12 + i * 8, y, i < n); }
function tapeIcon(x, y, on) { R(x, y, 9, 6, on ? '#ffd23f' : '#3a3550'); R(x + 2, y + 2, 5, 2, on ? '#1b1030' : '#1b1730'); }
function mapScreen(real) {
  drawLayers(STG[sel], real); ambient(STG[sel], real); dimAll(0.45);
  R(0, 0, W, 40, '#0d0a18'); R(0, 40, W, 1, CH.acc);
  ctext('CHAPTER ' + CH.num, 160, 6, '#ffffff', 2); ctext(CH.name + '  -  ' + CH.genre, 160, 26, CH.acc);
  for (let i = 0; i < 4; i++) { const [ax, ay] = NODES[i], [bx, by] = NODES[i + 1]; for (let k = 0; k < 60; k += 4) R(ax + (bx - ax) * k / 60, ay + (by - ay) * k / 60, 2, 2, '#ffe066'); }
  NODES.forEach(([x, y], i) => {
    const on = i === sel;
    if (on) ring(x, y, 10 + (Math.floor(real * 4) % 2), '#ffe066');
    disc(x, y, 7, K); disc(x, y, 6, on ? '#ffffff' : STG[i].acc);
    ctext(STG[i].id, x, y - 16, on ? '#ffe066' : '#ffffff', 1, null);
    stars3(x, y + 10, PROG.stars[i]); tapeIcon(x + 14, y - 4, PROG.tapes[i]);
    if (i === 2) ctext('MINI BOSS', x, y + 20, '#ff6b6b', 1, null);
    if (i === 4) { ctext('BOSS', x, y + 20, '#ff6b6b', 1, null); for (let k = 0; k < 4; k++) R(x - 8 + k * 5, y - 14 - (k % 2) * 2, 2, 4, '#ffd23f'); R(x - 8, y - 11, 17, 2, '#ffd23f'); }
  });
  const s = STG[sel];
  ctext('@ ' + s.track, 160, 148, s.acc);
  ctext(sel === 0 ? 'FULL RUN: ALL FIVE STAGES, NO STOPS' : 'PRACTICE: PLAY FROM ' + s.id + ' TO THE END', 160, 157, '#ffffff', 1, null);
  star(6, 46, true); text(totalStars() + '/15', 15, 46, '#ffd23f', 1, null);
  const o = CH.outfits[PROG.outfit];
  text('C OUTFIT: ' + o.name, 6, 56, outfitOK(PROG.outfit) ? '#5ef2ff' : '#ff6b6b', 1, null);
  if (!outfitOK(PROG.outfit)) text('NEEDS ' + o.stars + ' STARS', 6, 65, '#ff6b6b', 1, null);
  rtext('J JUKEBOX ' + PROG.tapes.filter(Boolean).length + '/5', 314, 46, '#ffd23f', 1, null);
  rtext('S STORY', 314, 56, '#c9c3e6', 1, null);
  const h = CH.hero, f = Math.floor(real * 8) % h.n;
  g.drawImage(heroImg(), f * h.cw, 0, h.cw, h.ch, NODES[sel][0] - h.ax + 2, NODES[sel][1] - 50 - h.ay + 26, h.cw, h.ch);
  ctext('< > PICK  SPACE PLAY  UP/DOWN OFFSET ' + sgn(offsetMs) + '  N NO-FAIL ' + (noFail ? 'ON' : 'OFF'), 160, 170, '#c9c3e6', 1, null);
}
let jsel = 0, jplaying = -1;
function jukebox(real) {
  drawLayers(STG[2], real); dimAll(0.6); panel(20, 26, 280, 148, '#ffd23f');
  ctext('JUKEBOX', 160, 34, '#ffd23f', 2);
  ctext('ONE HIDDEN CASSETTE IN EVERY STAGE', 160, 52, '#c9c3e6', 1, null);
  CH.bonus.forEach((b, i) => {
    const y = 66 + i * 14, on = i === jsel, got = PROG.tapes[i];
    if (on) R(26, y - 3, 268, 12, '#2e2a45');
    tapeIcon(32, y, got);
    text(got ? b.title : '??? FIND THE CASSETTE IN ' + STG[i].id, 46, y, got ? (on ? '#ffffff' : '#c9c3e6') : '#5a5670', 1, null);
    if (jplaying === i) for (let k = 0; k < 5; k++) { const hh = 2 + Math.floor(Math.abs(Math.sin(real * 8 + k)) * 7); R(272 + k * 4, y + 7 - hh, 3, hh, LC[k % 3]); }
  });
  ctext('UP/DOWN PICK   SPACE PLAY/STOP   T BACK', 160, 160, '#c9c3e6', 1, null);
}
function stopJuke() { if (jukeSrc) { try { jukeSrc.stop(); } catch (e) {} jukeSrc = null; } jplaying = -1; }
function playJuke(i) {
  stopJuke(); stopLoop();
  const e = CH.bonus[i];
  decode(e.key || 'main').then(b => { jukeSrc = actx.createBufferSource(); jukeSrc.buffer = b; jukeSrc.connect(master); if (e.seg) jukeSrc.start(0, e.seg[0], e.seg[1] - e.seg[0] + 2); else jukeSrc.start(); jplaying = i; jukeSrc.onended = () => { if (jplaying === i) jplaying = -1; }; });
}
function comicScreen(real) {
  g.drawImage(CH.comicImg[comicPage], 0, 0);
  if (Math.floor(real * 2) % 2) { R(250, 170, 70, 10, K); rtext('SPACE >', 316, 171, '#ffe066', 1, null); }
}
function introScreen(real) {
  const el = real - introT0;
  drawLayers(STG[sel], 0); ambient(STG[sel], el);
  const I = CH.intro, f = Math.floor(el * 5) % I.n;
  g.drawImage(I.img, f * I.cw, 0, I.cw, I.ch, -I.ox, -I.oy, I.cw, I.ch);
  const sec = Math.floor(el);
  if (sec !== lastTick && sec < 5) { lastTick = sec; if (sec > 0) tick(false); }
  ctext('CHAPTER ' + CH.num + '  ' + CH.name, 160, 30, '#ffffff');
  ctext('STAGE ' + STG[sel].id + '  @ ' + STG[sel].track, 160, 40, STG[sel].acc);
  const pop = 1 - (el - sec);
  if (sec < 5) ctext(String(5 - sec), 160, 54 - Math.round(pop * 3), '#ffe066', pop > 0.85 ? 7 : 6);
  ctext('GET READY!', 160, 102, '#ffffff');
  ctext(isTouch ? 'TAP TO SKIP' : 'SPACE TO SKIP', 280, 170, '#c9c3e6', 1, null);
}
function pauseOverlay() {
  dimAll(); panel(66, 34, 188, 112, CH.acc);
  ctext('PAUSED', 160, 42, '#ffffff', 2);
  ctext(isTouch ? 'TAP: RESUME' : 'P: RESUME', 160, 64, '#ffe066');
  ctext('R: RESTART STAGE ' + STG[cur].id, 160, 76, '#ffffff'); ctext('T: CHAPTER MAP', 160, 88, '#ffffff');
  ctext('< > OFFSET ' + sgn(offsetMs) + ' MS', 160, 104, '#c9c3e6');
  ctext('@ PAUSE THEME: ' + CH.genre, 160, 124, CH.acc, 1, null);
  for (let k = 0; k < 14; k++) { const h = 2 + Math.floor(Math.abs(Math.sin(performance.now() / 180 + k * 1.3)) * 8); R(118 + k * 6, 140 - h, 4, h, LC[k % 3]); }
}
function failOverlay() {
  dimAll(); ctext('GROOVE LOST', 160, 50, '#ff3b3b', 3);
  ctext(isTouch ? 'TAP: RETRY STAGE ' + STG[cur].id : 'R: RETRY FROM STAGE ' + STG[cur].id + '    T: MAP', 160, 86, '#ffffff');
  ctext('NO-FAIL CAN BE TURNED ON FROM THE MAP', 160, 100, '#c9c3e6', 1, null);
}
function clearOverlay() {
  dimAll(); panel(10, 26, 300, 150, CH.acc);
  ctext(runFrom === 0 ? 'CHAPTER ' + CH.num + ' CLEAR!' : 'PRACTICE RUN DONE', 160, 32, '#ffe066', 2);
  text('RANK', 26, 54, '#c9c3e6'); text(result.gr, 24, 66, '#ffd23f', 6, '#b8501f');
  let y = 52;
  result.rows.forEach(r => { if (!r) return; text(r.id + ' ' + r.track, 76, y, '#ffffff', 1, null); rtext(r.gr, 298, y, r.gr === 'S' ? '#ffd23f' : '#7cf06a', 1, null); y += 10; });
  y += 2;
  result.rows.forEach((r, i) => { if (r && starsRun[i]) { stars3(250, 52 + result.rows.slice(0, i).filter(Boolean).length * 10 - 0, starsRun[i].filter(Boolean).length); } });
  text('MINI BOSS', 76, y, '#c9c3e6', 1, null); rtext(result.mini, 298, y, result.mini === 'K.O.' ? '#7cf06a' : '#ff6b6b', 1, null); y += 10;
  text(B0.name, 76, y, '#c9c3e6', 1, null); rtext(result.boss, 298, y, result.boss === 'DEFEATED' ? '#7cf06a' : '#ff6b6b', 1, null); y += 12;
  text('SCORE', 76, y, '#ffe066', 1, null); rtext(String(score).padStart(7, '0'), 298, y, '#ffffff', 1, null); y += 10;
  text('MAX COMBO', 76, y, '#ffffff', 1, null); rtext(String(maxCombo), 298, y, '#ffffff', 1, null);
  const av = Math.round(result.avg);
  if (Math.abs(av) >= 8) ctext('TIMING ' + Math.abs(av) + ' MS ' + (av > 0 ? 'LATE' : 'EARLY') + '  O: SET OFFSET ' + sgn(result.suggest), 160, 154, '#7cf06a', 1, null);
  ctext(isTouch ? 'TAP: CHAPTER MAP' : 'R: PLAY AGAIN    T: CHAPTER MAP', 160, 164, '#c9c3e6', 1, null);
  if (rival.res) text(rival.res === 'WIN' ? 'RACE: WON' : 'RACE: LOST', 16, 120, rival.res === 'WIN' ? '#7cf06a' : '#ff6b6b', 1, null);
  if (unlocks.length) ctext(unlocks.join('   ').slice(0, 52), 160, 144, '#ffd23f', 1, null);
}

function frame(ts) {
  const real = ts / 1000;
  if (state === 'play') update();
  if (state === 'intro' && real - introT0 >= 5) startRun(sel);
  if (state === 'evcomic' && evc && real - evc.real0 >= COMIC_REAL) endEvComic();
  if (imgPending === 0) {
    if (state === 'loading' || state === 'splash') splash(real);
    else if (state === 'jukebox') jukebox(real);
    else if (state === 'comic') comicScreen(real);
    else if (state === 'title') titleScreen(real);
    else if (state === 'map') mapScreen(real);
    else if (state === 'intro') { introScreen(real); hud(0); }
    else {
      const vis = state === 'play' ? songTime() : frozen, playing = state !== 'clear';
      if (state === 'evcomic') KP = 0;
      g.save();
      if (state === 'play' && vis < shakeUntil) { const s = Math.floor(vis * 50) % 2 ? shakeAmp : -shakeAmp; g.translate(s, -s / 2); }
      scene(vis, playing);
      g.restore();
      if (state === 'play' && vis < flashUntil) { g.fillStyle = 'rgba(255,255,255,0.55)'; g.fillRect(0, 24, W, H - 24); }
      hud(vis);
      if (state === 'play') touchButtons();
      if (state === 'evcomic' && evc) evComicDraw(real);
      if (state === 'play' && fadeIn) fadeInDraw(real);
      if (state === 'paused') pauseOverlay(); else if (state === 'failed') failOverlay(); else if (state === 'clear') clearOverlay();
    }
  }
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
try { initAudio().then(() => { state = 'splash'; }).catch(() => { state = 'splash'; }); } catch (e) { state = 'splash'; }

// ---------- input ----------
const LANEKEYS = ['KeyW', 'KeyE', 'KeyR'];
function beginIntro() { stopJuke(); introT0 = performance.now() / 1000; lastTick = -1; resetRun(sel); cur = sel; state = 'intro'; tick(false); }
function qteActive() { return qte && qte.phase === 'active'; }
function unlock() { actx.resume(); playLoop('title'); state = 'title'; }
window.addEventListener('keydown', e => {
  if (['Space', 'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(e.code)) e.preventDefault();
  if (e.repeat) return;
  const c = e.code;
  if (state === 'splash') { unlock(); return; }
  if (state === 'title') { if (c === 'Space' || c === 'Enter') state = 'map'; return; }
  if (state === 'comic') {
    if (c === 'Space' || c === 'Enter' || c === 'Escape') { if (comicNext === 'intro') { PROG.comicSeen = true; saveProg(); beginIntro(); } else if (comicNext === 'clear') state = 'clear'; else state = 'map'; }
    return;
  }
  if (state === 'jukebox') {
    if (c === 'ArrowUp' || c === 'KeyW') jsel = (jsel + 4) % 5; else if (c === 'ArrowDown' || c === 'KeyR') jsel = (jsel + 1) % 5;
    else if (c === 'Space' || c === 'Enter') { if (jplaying === jsel) { stopJuke(); playLoop('title'); } else if (PROG.tapes[jsel]) playJuke(jsel); else buzz(); }
    else if (c === 'KeyT' || c === 'Escape' || c === 'KeyJ') { stopJuke(); playLoop('title'); state = 'map'; }
    return;
  }
  if (state === 'map') {
    if (c === 'KeyJ') { state = 'jukebox'; return; }
    if (c === 'KeyS') { comicPage = 'start'; comicNext = 'map'; state = 'comic'; return; }
    if (c === 'KeyC') { PROG.outfit = (PROG.outfit + 1) % CH.outfits.length; saveProg(); if (!outfitOK(PROG.outfit)) buzz(); else tick(true); return; }
    if ((c === 'Space' || c === 'Enter') && sel === 0 && !PROG.comicSeen) { comicPage = 'start'; comicNext = 'intro'; state = 'comic'; return; }
    if (c === 'Space' || c === 'Enter') beginIntro();
    else if (c === 'ArrowLeft' || c === 'KeyW') sel = (sel + 4) % 5; else if (c === 'ArrowRight' || c === 'KeyR') sel = (sel + 1) % 5;
    else if (c === 'ArrowUp') adjOff(5); else if (c === 'ArrowDown') adjOff(-5);
    else if (c === 'KeyN') noFail = !noFail;
    return;
  }
  if (state === 'intro') { if (c === 'Space' || c === 'Enter') startRun(sel); return; }
  if (state === 'evcomic') { if ((c === 'Space' || c === 'Enter') && evc && performance.now() / 1000 - evc.real0 > 0.8) endEvComic(); return; }
  if (state === 'play') {
    const i = LANEKEYS.indexOf(c);
    if (qteActive()) { if (i >= 0) { pressAt[i] = songTime(); qteKey('WER'[i]); } else if (c === 'Space') qteKey('SPACE'); else if (c === 'KeyP' || c === 'Escape') pause(); return; }
    if (i >= 0) lanePress(i); else if (c === 'Space') spacePress(); else if (c === 'KeyB') buddyPress(); else if (c === 'KeyQ') kickBack(); else if (c === 'KeyP' || c === 'Escape') pause();
    return;
  }
  if (state === 'paused') {
    if (c === 'KeyP' || c === 'Escape' || c === 'Space') resume();
    else if (c === 'KeyR') { stopLoop(); sel = cur; startRun(cur); } else if (c === 'KeyT') toMap();
    else if (c === 'ArrowLeft') adjOff(-5); else if (c === 'ArrowRight') adjOff(5);
    return;
  }
  if (state === 'failed') { if (c === 'KeyR' || c === 'Space') { sel = cur; master.gain.cancelScheduledValues(0); master.gain.setValueAtTime(0.9, actx.currentTime); startRun(cur); } else if (c === 'KeyT') toMap(); return; }
  if (state === 'clear') {
    if (c === 'KeyR') { stopLoop(); sel = 0; beginIntro(); } else if (c === 'KeyT') toMap();
    else if (c === 'KeyO' && result) { offsetMs = result.suggest; adjOff(0); result.avg = 0; }
  }
});
window.addEventListener('keyup', e => { const i = LANEKEYS.indexOf(e.code); if (i < 0) return; if (state === 'play') laneRelease(i); else held[i] = false; });
window.addEventListener('blur', () => { pause(); held = [false, false, false]; });
document.addEventListener('visibilitychange', () => { if (document.hidden) pause(); });
function toNative(ev) { const r = cv.getBoundingClientRect(); return [(ev.clientX - r.left) * W / r.width, (ev.clientY - r.top) * H / r.height]; }
function inBtn(b, x, y) { return x >= b[0] && x < b[0] + b[2] && y >= b[1] && y < b[1] + b[3]; }
const pointerLane = new Map();
cv.addEventListener('pointerdown', ev => {
  ev.preventDefault(); cv.focus();
  const [x, y] = toNative(ev);
  if (state === 'splash') { unlock(); return; }
  if (state === 'title') { state = 'map'; return; }
  if (state === 'comic') { if (comicNext === 'intro') { PROG.comicSeen = true; saveProg(); beginIntro(); } else if (comicNext === 'clear') state = 'clear'; else state = 'map'; return; }
  if (state === 'jukebox') { stopJuke(); playLoop('title'); state = 'map'; return; }
  if (state === 'map') { const i = NODES.findIndex(([nx, ny]) => Math.hypot(x - nx, y - ny) < 14); if (i >= 0) { if (i === sel) beginIntro(); else sel = i; } else if (y > 130) beginIntro(); return; }
  if (state === 'intro') { startRun(sel); return; }
  if (state === 'evcomic') { if (evc && performance.now() / 1000 - evc.real0 > 0.8) endEvComic(); return; }
  if (state === 'paused') { resume(); return; }
  if (state === 'failed') { sel = cur; startRun(cur); return; }
  if (state === 'clear') { toMap(); return; }
  if (state !== 'play') return;
  if (qteActive()) { for (let k = 0; k < qte.n; k++) { const [cx, cy] = qte.pos[k], w = qte.keys[k] === 'SPACE' ? 30 : 14; if (Math.abs(x - cx) <= w / 2 + 3 && Math.abs(y - cy) <= 10) { qteKey(qte.keys[k]); return; } } return; }
  if (isTouch && kickReady && inBtn(BTN.kick, x, y)) kickBack();
  else if (isTouch && inBtn(BTN.space, x, y)) spacePress();
  else if (isTouch && inBtn(BTN.b, x, y)) buddyPress();
  else if (isTouch && inBtn(BTN.pause, x, y)) pause();
  else if (y > 24) { const i = y < (EY[0] + EY[1]) / 2 ? 0 : y < (EY[1] + EY[2]) / 2 ? 1 : 2; const key = reversed(songTime()) ? 2 - i : i; pointerLane.set(ev.pointerId, key); lanePress(key); }
});
function pointerEnd(ev) { if (!pointerLane.has(ev.pointerId)) return; const i = pointerLane.get(ev.pointerId); pointerLane.delete(ev.pointerId); if (state === 'play') laneRelease(i); else held[i] = false; }
cv.addEventListener('pointerup', pointerEnd); cv.addEventListener('pointercancel', pointerEnd);
cv.focus();
