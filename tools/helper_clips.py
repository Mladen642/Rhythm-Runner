import json, sys, os, re, subprocess
sys.path.insert(0, '.')
from songlib import *
import songs2, songs3, songs4, songs5, songs6, jazz, country, edm, classical, punk, industrial
from songs3 import synth_bar
from songs4 import rock_bar, metal_bar
from songs5 import goth_bar, rap_bar
from songs6 import power_bar
PCS = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}
CHG = {1: 'synth', 2: 'rock', 3: 'metal', 4: 'goth', 5: 'rap', 6: 'power', 7: 'jazz', 8: 'country', 9: 'edm', 10: 'classical', 11: 'punk', 12: 'industrial'}


def simple(name):
    m = re.match(r'^([A-G][b#]?)(.*)$', name)
    r, q = m.group(1), m.group(2)
    minor = q.startswith('m') and not q.startswith('maj')
    return r + ('m' if minor else ''), PCS[r], minor


def place(pc, lo):
    r = lo + ((pc - lo) % 12)
    return r


def register(name):
    s, pc, mi = simple(name)
    th = 3 if mi else 4
    tri = lambda lo: [place(pc, lo), place(pc, lo) + th, place(pc, lo) + 7]
    songs3.ARPS.setdefault(s, [place(pc, 64), place(pc, 64) + th, place(pc, 64) + 7, place(pc, 64) + 12])
    songs5.TRI.setdefault(s, tri(57))
    songs4.RT.setdefault(s[:-1] if s.endswith('m') else s, 36 + pc)
    if hasattr(songs2, 'ROOT'):
        songs2.ROOT.setdefault(s, 36 + pc + (12 if pc < 4 else 0))
    jazz.JZ.setdefault(s, tri(55) + [place(pc, 55) + 10])
    country.CT.setdefault(s, tri(55))
    edm.CE.setdefault(s, tri(48))
    classical.CC.setdefault(s, tri(52))
    industrial.IC.setdefault(s, tri(40))
    return s


LEAD = {'synth': dict(duty=0.125, gain=0.18), 'rock': dict(duty=0.25, gain=0.19), 'metal': dict(duty=0.25, gain=0.18), 'goth': dict(duty=0.25, gain=0.2, vib=0.008, rev=0.55),
        'rap': dict(duty=0.5, gain=0.17), 'power': dict(duty=0.25, gain=0.18), 'jazz': dict(duty=0.25, gain=0.18, vib=0.008, rev=0.35), 'country': dict(duty=0.25, gain=0.17, vib=0.01),
        'classical': dict(duty=0.25, gain=0.17, vib=0.009, rev=0.45), 'punk': dict(duty=0.25, gain=0.19), 'industrial': dict(duty=0.25, gain=0.2, vib=0.003)}


def render(n, genre, spec):
    name = f"hc_{spec['song']}_{genre}"
    S = Song2(spec['bpm'], 9, seed=7)
    chords = [register(c) for c in spec['chords']]
    for t, d, m in spec['mel']:
        t = max(0.0, t)
        if genre == 'edm':
            edm.saw_lead(S, m, t, d, gain=0.13, rec=False)
        else:
            S.lead2(m, t, d, rec=False, **LEAD[genre])
    for k, ch in enumerate(chords):
        fill = k % 4 == 3; nxt = chords[(k + 1) % 8]
        if genre == 'synth': synth_bar(S, k, ch, 'helper', pattern=[0, 2, 1, 3] * 4, pad=True, style='four', fill=fill, gated=True)
        elif genre == 'rock': rock_bar(S, k, ch, 'chorus', fill); S.hey(S.T(k, 12)) if k % 2 else None
        elif genre == 'metal': metal_bar(S, k, ch, 'gallop', fill)
        elif genre == 'goth': goth_bar(S, k, ch, 'chorus', fill)
        elif genre == 'rap': rap_bar(S, k, ch, 'hook' if k % 4 else 'verse', fill)
        elif genre == 'power': power_bar(S, k, ch, 'chorus', fill)
        elif genre == 'jazz': jazz.swing_bar(S, k, ch, nxt, 'shout', fill)
        elif genre == 'country':
            country.blue_bar(S, k, ch, 'chorus', fill)
            if k % 4 == 1: S.hey(S.T(k, 12), gain=0.18)
        elif genre == 'edm': edm.edm_bar(S, k, ch, 'drop', 'house', fill)
        elif genre == 'classical': classical.classic_bar(S, k, ch, 'chorus', fill)
        elif genre == 'punk': rock_bar(S, k, ch, 'drive', fill); S.hey(S.T(k, 12), gain=0.16)
        elif genre == 'industrial': industrial.ind_bar(S, k, ch, 'chorus', fill)
    S.crash(0)
    S.finish2(name, S.T(8) - 0.01, rev_wet=0.3 if genre == 'goth' else 0.22, cho=(genre == 'goth'))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{name}.wav', '-codec:a', 'libmp3lame', '-b:a', '80k', f'{name}.mp3'], check=True)
    return name


if __name__ == '__main__':
    specs = json.load(open('helper_specs.json'))
    part, parts = int(sys.argv[1]), int(sys.argv[2])
    jobs = [(int(n), g) for n in sorted(specs, key=int) for g in CHG.values() if g != CHG[int(n)]]
    jobs = [j for i, j in enumerate(jobs) if i % parts == part]
    done = 0
    for n, g in jobs:
        nm = f"hc_{specs[str(n)]['song']}_{g}"
        if os.path.exists(f'{nm}.mp3'):
            continue
        render(n, g, specs[str(n)]); done += 1
    print('part', part, 'rendered', done, flush=True)
