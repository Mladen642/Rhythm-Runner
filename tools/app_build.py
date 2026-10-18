import json, base64, hashlib, os, re, shutil, sys, io
sys.path.insert(0, '.')
from PIL import Image
from scipy.io import wavfile
from chapter_make import layer_canvas, bubble_on, caption_on, dec
from stage_assets2 import b64
WEB = '../build/web'
NEW2OLD = {1: 5, 2: 4, 3: 1, 4: 10, 5: 8, 6: 7, 7: 9, 8: 2, 9: 12, 10: 3, 11: 6, 12: 11}
OLD = {1: ('chapter1v3', 'ch_pause'), 2: ('chapter2', 'c2_pause'), 3: ('chapter3', 'c3_pause'), 4: ('chapter4', 'c4_pause'), 5: ('chapter5', 'c5_pause'), 6: ('chapter6', 'c6_pause'),
       7: ('chapter7', 'c7_pause'), 8: ('chapter8', 'c8_pause'), 9: ('chapter9', 'c9_pause'), 10: ('chapter10', 'c10_pause'), 11: ('chapter11', 'c11_pause'), 12: ('chapter12', 'c12_pause')}
TEASE = {1: ['YO, NEXT STOP:', 'SPOOKY TOWN!'], 2: ['NEXT: NEON LIGHTS', 'AND SYNTHS!'], 3: ['NEXT: A FANCY', 'OPERA HOUSE!'], 4: ['NEXT STOP:', 'THE WILD WEST!'],
         5: ['NEXT STOP:', 'A JAZZ CLUB!'], 6: ['NEXT: A RAVE', 'IN OUTER SPACE!'], 7: ['NEXT: THE', 'OPEN HIGHWAY!'], 8: ['NEXT: STEEL', 'AND RED BRICK!'],
         9: ['NEXT: A KEEP OF', 'MOLTEN METAL!'], 10: ['NEXT: THE', 'SKY CITADEL!'], 11: ['NEXT: A RIOT', 'ON THE STREETS!']}


FIT_OLD = "  let s = Math.min((window.innerWidth - 16) / W, (window.innerHeight - hint.offsetHeight - 40) / H);\n  if (s >= 2) s = Math.floor(s);\n  s = Math.max(1, s);\n  cv.style.width = Math.round(W * s) + 'px'; cv.style.height = Math.round(H * s) + 'px';"
FIT_NEW = "  const s = Math.max(0.5, Math.min(window.innerWidth / W, window.innerHeight / H));\n  cv.style.width = Math.floor(W * s) + 'px'; cv.style.height = Math.floor(H * s) + 'px'; fit.w = innerWidth; fit.h = innerHeight;"
CSS = '<style id="app-fullscreen">\n  html, body { background: #000 !important; margin: 0; overflow: hidden; }\n  body { gap: 0 !important; padding: 0 !important; justify-content: center; align-items: center; }\n  :root { padding: 0 !important; }\n  #hint { display: none !important; }\n  canvas { box-shadow: none !important; border-radius: 0 !important; flex-shrink: 0; max-width: none !important; }\n</style>\n</head>'


def load(old):
    return json.load(open(f'{OLD[old][0]}.json'))


def songs_for(d, n, pause):
    s = {'main': f'chapter{n}.mp3', 'title': 'ch_title.mp3', 'pause': f'{pause}.mp3'}
    for b in d['chapter'].get('bonus', []):
        if b.get('key'): s[b['key']] = f"{b['key']}.mp3"
    for c in d['chapter'].get('cast', []):
        if c.get('clip') and os.path.exists(f"{c['clip']}.mp3"): s[c['clip']] = f"{c['clip']}.mp3"
    return s


def remap(o, m):
    if isinstance(o, dict): return {k: remap(v, m) for k, v in o.items()}
    if isinstance(o, list): return [remap(v, m) for v in o]
    if isinstance(o, str) and o in m: return m[o]
    return o


STORE = {'n': 0, 'bytes': 0}
def extract(o):
    if isinstance(o, dict): return {k: extract(v) for k, v in o.items()}
    if isinstance(o, list): return [extract(v) for v in o]
    if isinstance(o, str) and o.startswith('data:image/'):
        raw = base64.b64decode(o.split(',', 1)[1]); h = hashlib.sha1(raw).hexdigest()[:16]
        p = f'{WEB}/assets/img/{h}.png'
        if not os.path.exists(p):
            open(p, 'wb').write(raw); STORE['n'] += 1; STORE['bytes'] += len(raw)
        return f'assets/img/{h}.png'
    return o


def frame0(sheet):
    return dec(sheet['src']).convert('RGBA').crop((0, 0, sheet['cw'], sheet['ch']))


def build():
    os.makedirs(os.path.dirname(WEB), exist_ok=True)
    if os.path.exists(WEB): shutil.rmtree(WEB)
    for d_ in ('data', 'assets/img', 'assets/audio'): os.makedirs(f'{WEB}/{d_}', exist_ok=True)
    LOOPS = json.load(open('loops.json')); title_len = LOOPS['ch_title']
    for new, old in NEW2OLD.items():
        d = load(old); c = d['chapter']
        if new < 12:
            nd = load(NEW2OLD[new + 1])['chapter']
            C2 = layer_canvas(nd['stages'][0]['layers']).crop((6, 98, 314, 178)).copy()
            C2.alpha_composite(frame0(nd['hero']), (200 - nd['hero']['ax'], 166 - 98 - nd['hero']['ay']))
            C2.alpha_composite(frame0(c['hero']), (60 - c['hero']['ax'], 166 - 98 - c['hero']['ay']))
            C2 = bubble_on(C2, TEASE[new], 150, 6); C2 = caption_on(C2, [f'NEXT: CHAPTER {new + 1}'], 4, 62)
            end = dec(c['comics']['end']).convert('RGBA'); end.paste(C2.convert('RGBA').crop((0, 0, 308, 78)), (6, 96))
            c['comics']['end'] = b64(end)
        c = remap(c, {f'{old}-{k}': f'{new}-{k}' for k in range(1, 6)}); c['num'] = new
        songs = {}
        for k, path in songs_for(d, old, OLD[old][1]).items():
            fn = os.path.basename(path); shutil.copy(path, f'{WEB}/assets/audio/{fn}'); songs[k] = f'assets/audio/{fn}'
        loops = {'title': title_len, 'pause': LOOPS[OLD[old][1]], 'main': 9999}
        out = {'data': {'chapter': extract(c), 'font': d['font']}, 'songs': songs, 'loops': loops}
        json.dump(out, open(f'{WEB}/data/ch{new}.json', 'w'), separators=(',', ':'))
        print(new, '<- old', old, c['name'], flush=True)
    # engine + loader page
    html = open('chapter_engine.html').read()
    head, rest = html.split('<script>', 1); script, tail = rest.split('</script>', 1)
    for a, b in (('const DATA = __DATA__;', 'const DATA = window.__DATA;'), ('const SONGS = __SONGS__;', 'const SONGS = window.__SONGS;'), ('const LOOPS = __LOOPS__;', 'const LOOPS = window.__LOOPS;'),
                 ("""  const bin = atob(SONGS[key]), u = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i);
  BUF[key] = new Promise((res, rej) => actx.decodeAudioData(u.buffer, res, rej));""",
                  """  BUF[key] = fetch(SONGS[key]).then(r => r.arrayBuffer()).then(b => new Promise((res, rej) => actx.decodeAudioData(b, res, rej)));""")):
        assert script.count(a) == 1, a[:60]
        script = script.replace(a, b)
    MS = """const MS = { ready: false, src: null };
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
}"""
    old_say = "function say(s, pitch, rate) { if (actx) lastVoice = actx.currentTime; try { if (!('speechSynthesis' in window)) return; const u = new SpeechSynthesisUtterance(s); u.pitch = pitch; u.rate = rate; speechSynthesis.cancel(); speechSynthesis.speak(u); } catch (e) {} }"
    assert script.count(old_say) == 1
    script = script.replace(old_say, MS)
    for a2, b2 in (("try { speechSynthesis.cancel(); } catch (x) {}", "try { speechSynthesis.cancel(); } catch (x) {} msStop();"), ("  try { speechSynthesis.cancel(); } catch (e) {}", "  try { speechSynthesis.cancel(); } catch (e) {} msStop();")):
        assert script.count(a2) == 1, a2
        script = script.replace(a2, b2)
    os.makedirs(f'{WEB}/lib', exist_ok=True)
    for fn in ('mespeak.js', 'mespeak_config.json', 'en-us.json'):
        shutil.copy(f'../vendor/mespeak/{fn}', f'{WEB}/lib/{fn}')
    assert script.count(FIT_OLD) == 1
    assert script.count("window.addEventListener('resize', fit); fit();") == 1
    script = script.replace("window.addEventListener('resize', fit); fit();", "window.addEventListener('resize', fit); fit(); setInterval(() => { if (innerWidth !== fit.w || innerHeight !== fit.h) fit(); }, 300);")
    script = script.replace(FIT_OLD, FIT_NEW)
    open(f'{WEB}/engine.js', 'w').write(script)
    loader = """<script>
window.addEventListener('keydown', e => { if (e.key === 'Escape' && typeof state !== 'undefined' && state === 'map') { e.stopImmediatePropagation(); location.href = 'index.html'; } }, true);
(async () => {
  const ch = new URLSearchParams(location.search).get('ch') || '1';
  const d = await (await fetch('data/ch' + ch + '.json')).json();
  window.__DATA = d.data; window.__SONGS = d.songs; window.__LOOPS = d.loops;
  document.title = 'Rhythm Runner: Chapter ' + ch;
  const ms = document.createElement('script'); ms.src = 'lib/mespeak.js';
  ms.onload = ms.onerror = () => { const s = document.createElement('script'); s.src = 'engine.js'; document.body.appendChild(s); };
  document.body.appendChild(ms);
})();
</script>"""
    assert head.count('</head>') == 1
    open(f'{WEB}/play.html', 'w').write(head.replace('__TITLE__', 'Rhythm Runner').replace('</head>', CSS) + loader + tail)
    shutil.copy('ch_title.mp3', f'{WEB}/assets/audio/ch_title.mp3')
    shutil.copy('../desktop/build/icon.png', f'{WEB}/icon.png')
    print('images', STORE['n'], round(STORE['bytes'] / 1e6, 1), 'MB')


if __name__ == '__main__':
    build()
