import os
os.makedirs('../dist', exist_ok=True)
import json, sys, subprocess, os
sys.path.insert(0, '.')
from assemble import build_page
def songs_for(d, n, pause):
    s = {'main': f'chapter{n}.mp3' if n != 1 else 'chapter1.mp3', 'title': 'ch_title.mp3', 'pause': f'{pause}.mp3'}
    for b in d['chapter'].get('bonus', []):
        if b.get('key'):
            s[b['key']] = f"{b['key']}.mp3"
    for c in d['chapter'].get('cast', []):
        if c.get('clip') and os.path.exists(f"{c['clip']}.mp3"):
            s[c['clip']] = f"{c['clip']}.mp3"
    return s
CH = [(1, 'chapter1v3', 'Chapter 1, Neon City', 'ch_pause'), (2, 'chapter2', 'Chapter 2, Sunset Highway', 'c2_pause'), (3, 'chapter3', 'Chapter 3, Molten Keep', 'c3_pause'),
      (4, 'chapter4', 'Chapter 4, Ravenmoor', 'c4_pause'), (5, 'chapter5', 'Chapter 5, Concrete City', 'c5_pause'), (6, 'chapter6', 'Chapter 6, Sky Citadel', 'c6_pause'), (7, 'chapter7', 'Chapter 7, Velvet District', 'c7_pause'), (8, 'chapter8', 'Chapter 8, Dusty Gulch', 'c8_pause'), (9, 'chapter9', 'Chapter 9, Bass Planet', 'c9_pause'), (10, 'chapter10', 'Chapter 10, Grand Opera', 'c10_pause'), (11, 'chapter11', 'Chapter 11, Riot Street', 'c11_pause'), (12, 'chapter12', 'Chapter 12, Steel Harbor', 'c12_pause')]
for n, js, name, pause in CH:
    if len(sys.argv) > 1 and str(n) not in sys.argv[1:]:
        continue
    d = json.load(open(f'{js}.json'))
    mb = build_page(d, songs_for(d, n, pause), 'Rhythm runner: ' + name, f'../dist/rhythm-runner-chapter-{n}.html', f'{pause}.wav')
    print(f'ch{n}', mb, 'MB', subprocess.run(['node', '--check', 'check.js'], capture_output=True, text=True).stderr or 'syntax ok')
