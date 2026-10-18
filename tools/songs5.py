import sys
import numpy as np
from scipy.signal import butter, lfilter
from songlib import *
from songs2 import play, drums, shift
from songs3 import synth_bar, loop_song, ARPS
from songs4 import M, rock_bar, metal_bar, root, RT
RT['Db'] = 37

TRI = {'Em': [64, 67, 71], 'C': [60, 64, 67], 'G': [59, 62, 67], 'D': [62, 66, 69], 'Am': [57, 60, 64], 'B': [59, 63, 66], 'Dm': [62, 65, 69],
       'F': [60, 65, 69], 'Bb': [58, 62, 65], 'A': [57, 61, 64], 'Bm': [59, 62, 66], 'F#': [58, 61, 66], 'Cm': [60, 63, 67], 'Ab': [60, 63, 68],
       'Eb': [58, 63, 67], 'Fm': [60, 65, 68], 'Db': [61, 65, 68], 'Gm': [58, 62, 67], 'E': [59, 64, 68], 'F#m': [61, 66, 69], 'Eb+': [58, 63, 67]}


def goth_bar(S, bar, ch, style, fill=False):
    t, r, tr = S.T(bar), root(ch), TRI[ch]
    arp = [tr[0], tr[1], tr[2], tr[0] + 12, tr[2], tr[1], tr[2], tr[0] + 12]
    for i, m in enumerate(arp):
        S.chorus_gtr(m, t + i * 2 * S.STEP, 2 * S.STEP, gain=0.06 if style != 'bridge' else 0.045)
    S.organ(tr, t, S.BAR * 0.98, gain=0.022 if style not in ('chorus', 'bridge') else 0.032)
    if style == 'bridge':
        for i, s in enumerate((0, 4, 8, 12)):
            S.bell(tr[i % 3] + 24, t + s * S.STEP, gain=0.045)
        S.bass(r + 12, t, S.BAR * 0.9, gain=0.24); S.kick(t); S.tom(t + 12 * S.STEP, 38, gain=0.25)
        return
    pat = [0, 12, 7, 12, 0, 12, 10, 12]
    for i, s in enumerate(range(0, 16, 2)):
        S.bass(r + 12 + pat[i], t + s * S.STEP, 2 * S.STEP, gain=0.24, bright=0.35)
    if style == 'chorus':
        for i, s in enumerate((0, 4, 8, 12)):
            S.bell(tr[i % 3] + 12, t + s * S.STEP, gain=0.04)
        S.power(r + 12, t, 8 * S.STEP, gain=0.06); S.power(r + 12, t + 8 * S.STEP, 8 * S.STEP, gain=0.055)
    if style == 'intro':
        return
    drums(S, bar, 'goth', fill=fill)


def sub808(S, m, t, dur, gain=0.32):
    n_ = int(dur * SR); tt = np.arange(n_) / SR
    f = mtof(m) * (1 + 0.6 * np.exp(-tt * 30))
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) * np.exp(-tt * 1.6) * np.clip(tt / 0.004, 0, 1)
    y = np.tanh(y * 1.6) / 1.2
    S.add(y, t, gain)


def scratch(S, t, gain=0.16):
    for k, (f0, ln) in enumerate(((1200, 0.07), (2400, 0.05), (900, 0.08))):
        n_ = int(ln * SR); nz = S.noise(n_, 1)
        b, a = butter(2, [f0 * 0.6 / (SR / 2), min(0.99, f0 * 1.6 / (SR / 2))], btype='band')
        y = lfilter(b, a, nz) * np.hanning(n_) * 3
        S.add(y, t + k * 0.075, gain, 0.2 * (k - 1))


def piano(S, ms, t, dur, gain=0.05):
    for m in ms:
        e = adsr(dur, 0.002, 0.25, 0.25, 0.2)
        tt = np.arange(len(e)) / SR
        y = (np.sin(2 * np.pi * mtof(m) * tt) * 0.7 + pulse(np.full(len(e), mtof(m)), 0.5) * 0.18 + np.sin(4 * np.pi * mtof(m) * tt) * 0.2) * e
        S.add(y, t, gain, 0.0); S.send(y, t, gain, 0.35)


def rap_drums(S, bar, fill=False, light=False):
    t, st = S.T(bar), S.STEP
    sw = 0.16 * st
    for s in (0, 7, 10) if not light else (0, 10):
        S.kick(t + s * st + (sw if s % 2 else 0), gain=0.5)
    for s in (4, 12):
        S.snare(t + s * st, gain=0.3, clap=True)
    for s in range(0, 16, 2):
        S.hat(t + s * st + (sw if (s // 2) % 2 else 0), gain=0.05 if s % 4 else 0.07, open_=(s == 14))
    if fill:
        S.snare(t + 14 * st, gain=0.18); S.snare(t + 15 * st, gain=0.22)


def rap_bar(S, bar, ch, style, fill=False):
    t, r, tr = S.T(bar), root(ch), TRI[ch]
    st = S.STEP
    if style in ('verse', 'intro', 'bridge'):
        for s in (0, 6, 10) if style != 'bridge' else (0, 8):
            piano(S, tr, t + s * st, 3 * st, gain=0.045)
        sub808(S, r + 12, t, 6 * st); sub808(S, r + 12, t + 10 * st, 5 * st, gain=0.26)
        if style == 'intro' and bar < 2:
            S.hat(t, gain=0.05)
        else:
            rap_drums(S, bar, fill=fill, light=(style == 'bridge'))
    elif style == 'hook':
        for s in (0, 4, 8, 12):
            S.power(r + 12, t + s * st, 4 * st, gain=0.1)
        sub808(S, r + 12, t, 8 * st, gain=0.22); sub808(S, r + 12, t + 8 * st, 8 * st, gain=0.2)
        for s in (0, 6, 8):
            S.kick(t + s * st, gain=0.5)
        for s in (4, 12):
            S.snare(t + s * st, gain=0.32)
        for s in range(0, 16, 2):
            S.hat(t + s * st, gain=0.07, open_=True)
        if fill:
            S.fill(bar, start=12)
    elif style == 'beatbox':
        for s in (0, 8, 11):
            S.kick(t + s * st, gain=0.45)
        for s in (4, 12):
            S.snare(t + s * st, gain=0.25, clap=True)
        sub808(S, r + 12, t, 14 * st, gain=0.2)
        if bar % 2 == 1:
            scratch(S, t + 12 * st)


def song5(name, bpm, secs, kind, harm_key, seed):
    nbars = sum(len(c) for _, c, _, _, _ in secs) + 1
    S = Song2(bpm, nbars, seed=seed)
    bar = 0
    for name_, chords, mel, style, o in secs:
        S.mark(name_, S.T(bar))
        if name_.startswith('chorus'):
            S.mark('chorus_any', S.T(bar)); S.crash(S.T(bar))
        if name_ in ('breakdown', 'helper', 'broken'):
            S.crash(S.T(bar))
        if kind == 'rap' and name_ in ('verse', 'chorus', 'broken', 'chorus_cor', 'finale', 'chorus_last', 'bridge'):
            scratch(S, S.T(bar) - 2 * S.STEP)
        if mel:
            play(S, bar, mel, gain=o.get('gain', 0.18), duty=o.get('duty', 0.25), harm_key=harm_key if o.get('harm') else None,
                 harm_oct=o.get('oct', False), vib=o.get('vib', 0.004), rev=o.get('rev', 0.3))
        for k, ch in enumerate(chords):
            fill = (k % 4 == 3) and o.get('fills', True)
            if style == 'metal':
                metal_bar(S, bar + k, ch, 'gallop', fill)
            elif style == 'synth':
                synth_bar(S, bar + k, ch, 'helper', pattern=[0, 2, 1, 3] * 4, pad=True, style='four', fill=fill, gated=True)
            elif kind == 'goth':
                goth_bar(S, bar + k, ch, style, fill)
            else:
                rap_bar(S, bar + k, ch, style, fill)
            if o.get('hey') and k % 2 == 1:
                S.hey(S.T(bar + k, 4)); S.hey(S.T(bar + k, 12))
        bar += len(chords)
    tE = S.T(bar)
    last = secs[-1][1][-1]
    S.kick(tE); S.crash(tE, 0.14); S.bass(root(last), tE, 1.2)
    if kind == 'goth':
        S.organ(TRI[last], tE, 2.0, gain=0.04); S.bell(TRI[last][0] + 24, tE, 0.06)
    else:
        sub808(S, root(last) + 12, tE, 1.4); S.power(root(last) + 12, tE, 1.6, gain=0.12); scratch(S, tE + 0.3)
    S.lead2(root(last) + 24 + (12 if root(last) < 44 else 0), tE, 1.6)
    S.mark('final', tE)
    return S.finish2(name, tE, rev_wet=0.3 if kind == 'goth' else 0.2, cho=(kind == 'goth'))


GV = dict(gain=0.2, vib=0.008, rev=0.55)


def cathedral():
    V = ['Am', 'F', 'C', 'G', 'Am', 'F', 'E', 'E']
    C_ = ['F', 'G', 'Am', 'Am', 'F', 'G', 'E', 'E']
    vm = M('A4:6 B4:2 C5:8', 'A4:6 G4:2 F4:8', 'E4:6 G4:2 C5:4 B4:4', 'D5:12 B4:4', 'A4:6 B4:2 C5:8', 'F5:6 E5:2 C5:8', 'B4:6 C5:2 D5:4 B4:4', 'G#4:14')
    cm = M('C5:4 F5:4 A5:8', 'B5:4 G5:4 D5:8', 'C5:4 E5:4 A5:4 G5:4', 'A5:12 E5:4', 'C5:4 F5:4 A5:8', 'D6:4 B5:4 G5:8', 'G#5:4 B5:4 E5:4 G#5:4', 'A5:14')
    om = M('E5:16', 'C5:16', 'B4:8 G#4:8', 'A4:14')
    return song5('c4_cathedral', 112, [('intro', ['Am', 'F', 'E', 'E'], None, 'intro', {}), ('verse', V, vm, 'verse', GV), ('chorus', C_, cm, 'chorus', GV),
                                      ('verse', V, vm, 'verse', GV), ('chorus', C_, cm, 'chorus', dict(GV, harm=True)), ('outro', ['Am', 'F', 'E', 'Am'], om, 'chorus', dict(GV, fills=False))],
                 'goth', 'Am', 81)


def gargoyle_song():
    V = ['Dm', 'Bb', 'F', 'C', 'Dm', 'Bb', 'A', 'A']
    C_ = ['Bb', 'C', 'Dm', 'Dm', 'Bb', 'C', 'A', 'A']
    vm = M('D5:6 E5:2 F5:8', 'D5:6 C5:2 Bb4:8', 'A4:6 C5:2 F5:4 E5:4', 'G5:12 E5:4', 'D5:6 E5:2 F5:8', 'Bb5:6 A5:2 F5:8', 'E5:6 F5:2 G5:4 E5:4', 'C#5:14')
    cm = M('F5:4 D5:4 Bb5:8', 'G5:4 E5:4 C6:8', 'A5:4 F5:4 D5:4 F5:4', 'A5:12 D5:4', 'F5:4 D5:4 Bb5:8', 'C6:4 D6:4 E6:8', 'C#6:4 A5:4 E5:4 C#5:4', 'D5:14')
    om = M('F5:16', 'D5:16', 'C#5:8 E5:8', 'D5:14')
    return song5('c4_gargoyle', 116, [('intro', ['Dm', 'Bb', 'A', 'A'], None, 'intro', {}), ('verse', V, vm, 'verse', GV), ('chorus', C_, shift(cm, -12), 'chorus', GV),
                                      ('breakdown', ['Dm', 'Dm', 'Bb', 'Bb', 'C', 'C', 'A', 'A'], None, 'bridge', {}),
                                      ('chorus', C_, shift(cm, -12), 'chorus', dict(GV, harm=True)), ('outro', ['Dm', 'Bb', 'A', 'Dm'], om, 'chorus', dict(GV, fills=False))],
                 'goth', 'Dm', 82)


def raven():
    SCALES['Bm'] = [11, 1, 2, 4, 6, 7, 9]
    V = ['Bm', 'G', 'D', 'A', 'Bm', 'G', 'F#', 'F#']
    C_ = ['G', 'D', 'A', 'Bm', 'G', 'D', 'F#', 'F#']
    vm = M('B4:6 C#5:2 D5:8', 'B4:6 A4:2 G4:8', 'F#4:6 A4:2 D5:4 C#5:4', 'E5:12 C#5:4', 'B4:6 C#5:2 D5:8', 'G5:6 F#5:2 D5:8', 'C#5:6 D5:2 E5:4 C#5:4', 'A#4:14')
    cm = M('D5:4 G5:4 B5:8', 'A5:4 F#5:4 D5:8', 'C#5:4 E5:4 A5:4 G5:4', 'F#5:12 B4:4', 'D5:4 G5:4 B5:8', 'A5:4 D6:4 F#5:8', 'A#5:4 C#6:4 F#5:4 A#5:4', 'B5:14')
    om = M('D5:16', 'B4:16', 'C#5:8 A#4:8', 'B4:14')
    return song5('c4_raven', 120, [('intro', ['Bm', 'G', 'F#', 'F#'], None, 'intro', {}), ('verse', V, vm, 'verse', GV), ('chorus', C_, cm, 'chorus', GV),
                                   ('verse', V, vm, 'verse', GV), ('chorus', C_, cm, 'chorus', dict(GV, harm=True)), ('chorus_last', C_, cm, 'chorus', dict(GV, oct=True)),
                                   ('outro', ['G', 'D', 'F#', 'Bm'], om, 'chorus', dict(GV, fills=False))],
                 'goth', 'Bm', 83)


def countess_song():
    V = ['Em', 'C', 'G', 'D', 'Em', 'C', 'B', 'B']
    C_ = ['C', 'G', 'D', 'Em', 'C', 'G', 'B', 'B']
    vm = M('E5:6 F#5:2 G5:8', 'E5:6 D5:2 C5:8', 'B4:6 D5:2 G5:4 F#5:4', 'A5:12 F#5:4', 'E5:6 F#5:2 G5:8', 'C6:6 B5:2 G5:8', 'F#5:6 G5:2 A5:4 F#5:4', 'D#5:14')
    cm = M('E5:4 G5:4 C6:8', 'D6:4 B5:4 G5:8', 'F#5:4 A5:4 D6:4 C6:4', 'B5:12 E5:4', 'E5:4 G5:4 C6:8', 'D6:4 E6:4 D6:8', 'D#6:4 B5:4 F#5:4 A5:4', 'B5:14')
    hm = M('E5:2 G5:2 B5:4 A5:2 G5:2 E5:4', 'C5:2 E5:2 G5:4 F#5:2 E5:2 C5:4', 'D5:2 F#5:2 A5:4 G5:2 F#5:2 D5:4', 'B4:8 D#5:8',
           'E5:2 G5:2 B5:4 E6:4 D6:4', 'C6:4 B5:4 G5:8', 'A5:4 F#5:4 D5:4 F#5:4', 'B5:14')
    om = M('G5:16', 'E5:16', 'F#5:8 D#5:8', 'E5:14')
    return song5('c4_countess', 124, [('intro', ['Em'] * 4, None, 'intro', {}), ('verse', V, vm, 'verse', GV), ('chorus', C_, shift(cm, -12), 'chorus', dict(GV, oct=True)),
                                      ('verse_rev', V, vm, 'verse', GV), ('helper', ['Em', 'C', 'D', 'B', 'Em', 'C', 'D', 'B'], hm, 'metal', {'gain': 0.17}),
                                      ('chorus_back', C_, shift(cm, -12), 'chorus', dict(GV, harm=True)),
                                      ('finale', ['Em', 'Em', 'C', 'C', 'D', 'D', 'B', 'B'], None, 'bridge', {}), ('outro', ['Em', 'C', 'B', 'Em'], om, 'chorus', dict(GV, fills=False))],
                 'goth', 'Em', 84)


RV = dict(gain=0.17, duty=0.5, rev=0.25)
RH = dict(gain=0.18, hey=True)


def concrete():
    SCALES['Cm'] = [0, 2, 3, 5, 7, 8, 10]
    V = ['Cm', 'Ab', 'Eb', 'Bb'] * 2
    H_ = ['Ab', 'Bb', 'Cm', 'Cm', 'Ab', 'Bb', 'G', 'G']
    vm = M('C5:3 Eb5:3 G5:2 F5:4 Eb5:4', 'C5:3 Eb5:3 Ab5:2 G5:8', 'G5:3 Bb5:3 G5:2 Eb5:4 F5:4', 'D5:12 Bb4:4',
           'C5:3 Eb5:3 G5:2 C6:4 Bb5:4', 'Ab5:3 G5:3 Eb5:2 C5:8', 'Bb4:3 D5:3 F5:2 Bb5:4 Ab5:4', 'G5:14')
    hm = M('C5:4 Eb5:4 Ab5:8', 'Bb5:4 F5:4 D5:8', 'Eb5:4 G5:4 C6:4 Bb5:4', 'C6:12 G5:4', 'C5:4 Eb5:4 Ab5:8', 'Bb5:4 D6:4 F6:8', 'D6:4 B5:4 G5:4 B5:4', 'C6:14')
    om = M('Eb5:16', 'C5:16', 'D5:8 B4:8', 'C5:14')
    return song5('c5_concrete', 92, [('intro', ['Cm', 'Ab', 'Eb', 'Bb'], None, 'intro', {}), ('verse', V, vm, 'verse', RV), ('chorus', H_, hm, 'hook', RH),
                                     ('verse', V, vm, 'verse', RV), ('chorus', H_, hm, 'hook', dict(RH, harm=True)), ('outro', ['Cm', 'Ab', 'G', 'Cm'], om, 'verse', dict(RV, fills=False))],
                 'rap', 'Cm', 91)


def subway():
    SCALES['Fm'] = [5, 7, 8, 10, 0, 1, 3]
    V = ['Fm', 'Db', 'Ab', 'Eb'] * 2
    H_ = ['Db', 'Eb', 'Fm', 'Fm', 'Db', 'Eb', 'C', 'C']
    TRI['C'] = [60, 64, 67]
    vm = M('F4:3 Ab4:3 C5:2 Bb4:4 Ab4:4', 'F4:3 Ab4:3 Db5:2 C5:8', 'C5:3 Eb5:3 C5:2 Ab4:4 Bb4:4', 'G4:12 Eb4:4',
           'F4:3 Ab4:3 C5:2 F5:4 Eb5:4', 'Db5:3 C5:3 Ab4:2 F4:8', 'Eb5:3 G5:3 Bb5:2 G5:4 Eb5:4', 'E5:14')
    hm = M('F5:4 Ab5:4 Db6:8', 'Eb6:4 Bb5:4 G5:8', 'Ab5:4 C6:4 F6:4 Eb6:4', 'F6:12 C6:4', 'F5:4 Ab5:4 Db6:8', 'Eb6:4 G6:4 Bb6:8', 'G6:4 E6:4 C6:4 E6:4', 'F6:14')
    om = M('Ab5:16', 'F5:16', 'G5:8 E5:8', 'F5:14')
    return song5('c5_subway', 95, [('intro', ['Fm', 'Db', 'Ab', 'Eb'], None, 'intro', {}), ('verse', V, shift(vm, 12), 'verse', RV), ('chorus', H_, shift(hm, -12), 'hook', RH),
                                   ('verse', V, shift(vm, 12), 'verse', RV), ('chorus', H_, shift(hm, -12), 'hook', dict(RH, harm=True)), ('outro', ['Fm', 'Db', 'C', 'Fm'], om, 'verse', dict(RV, fills=False))],
                 'rap', 'Fm', 92)


def court():
    SCALES['Gm'] = [7, 9, 10, 0, 2, 3, 5]
    V = ['Gm', 'Eb', 'Bb', 'F'] * 2
    H_ = ['Eb', 'F', 'Gm', 'Gm', 'Eb', 'F', 'D', 'D']
    vm = M('G4:3 Bb4:3 D5:2 C5:4 Bb4:4', 'G4:3 Bb4:3 Eb5:2 D5:8', 'D5:3 F5:3 D5:2 Bb4:4 C5:4', 'A4:12 F4:4',
           'G4:3 Bb4:3 D5:2 G5:4 F5:4', 'Eb5:3 D5:3 Bb4:2 G4:8', 'F5:3 A5:3 C6:2 A5:4 F5:4', 'F#5:14')
    hm = M('G5:4 Bb5:4 Eb6:8', 'F6:4 C6:4 A5:8', 'Bb5:4 D6:4 G6:4 F6:4', 'G6:12 D6:4', 'G5:4 Bb5:4 Eb6:8', 'F6:4 A6:4 C7:8', 'A6:4 F#6:4 D6:4 F#6:4', 'G6:14')
    om = M('Bb5:16', 'G5:16', 'A5:8 F#5:8', 'G5:14')
    return song5('c5_court', 98, [('intro', ['Gm', 'Eb', 'D', 'D'], None, 'intro', {}), ('verse', V, shift(vm, 12), 'verse', RV), ('chorus', H_, shift(hm, -12), 'hook', RH),
                                  ('breakdown', ['Gm', 'Gm', 'Eb', 'Eb', 'F', 'F', 'D', 'D'], None, 'beatbox', {}),
                                  ('chorus', H_, shift(hm, -12), 'hook', dict(RH, harm=True)), ('outro', ['Gm', 'Eb', 'D', 'Gm'], om, 'verse', dict(RV, fills=False))],
                 'rap', 'Gm', 93)


def alley():
    V = ['Dm', 'Bb', 'F', 'C'] * 2
    H_ = ['Bb', 'C', 'Dm', 'Dm', 'Bb', 'C', 'A', 'A']
    vm = M('D5:3 F5:3 A5:2 G5:4 F5:4', 'D5:3 F5:3 Bb5:2 A5:8', 'A5:3 C6:3 A5:2 F5:4 G5:4', 'E5:12 C5:4',
           'D5:3 F5:3 A5:2 D6:4 C6:4', 'Bb5:3 A5:3 F5:2 D5:8', 'C5:3 E5:3 G5:2 C6:4 Bb5:4', 'A5:14')
    hm = M('D5:4 F5:4 Bb5:8', 'C6:4 G5:4 E5:8', 'F5:4 A5:4 D6:4 C6:4', 'D6:12 A5:4', 'D5:4 F5:4 Bb5:8', 'C6:4 E6:4 G6:8', 'E6:4 C#6:4 A5:4 C#6:4', 'D6:14')
    om = M('F5:16', 'D5:16', 'E5:8 C#5:8', 'D5:14')
    return song5('c5_alley', 100, [('intro', ['Dm', 'Bb', 'A', 'A'], None, 'intro', {}), ('verse', V, vm, 'verse', RV), ('chorus', H_, hm, 'hook', RH),
                                   ('bridge', ['Bb', 'C', 'A', 'A'], None, 'bridge', {}), ('chorus', H_, hm, 'hook', dict(RH, harm=True)),
                                   ('chorus_last', H_, hm, 'hook', dict(RH, oct=True)), ('outro', ['Dm', 'Bb', 'A', 'Dm'], om, 'verse', dict(RV, fills=False))],
                 'rap', 'Dm', 94)


def pitch():
    V = ['Am', 'F', 'C', 'G'] * 2
    H_ = ['F', 'G', 'Am', 'Am', 'F', 'G', 'E', 'E']
    vm = M('A4:3 C5:3 E5:2 D5:4 C5:4', 'A4:3 C5:3 F5:2 E5:8', 'E5:3 G5:3 E5:2 C5:4 D5:4', 'B4:12 G4:4',
           'A4:3 C5:3 E5:2 A5:4 G5:4', 'F5:3 E5:3 C5:2 A4:8', 'G5:3 B5:3 D6:2 B5:4 G5:4', 'G#5:14')
    hm = M('A5:4 C6:4 F6:8', 'G6:4 D6:4 B5:8', 'C6:4 E6:4 A6:4 G6:4', 'A6:12 E6:4', 'A5:4 C6:4 F6:8', 'G6:4 B6:4 D7:8', 'B6:4 G#6:4 E6:4 G#6:4', 'A6:14')
    om = M('C6:16', 'A5:16', 'B5:8 G#5:8', 'A5:14')
    return song5('c5_pitch', 104, [('intro', ['Am'] * 4, None, 'intro', {}), ('verse', V, shift(vm, 12), 'verse', RV), ('chorus', H_, shift(hm, -12), 'hook', RH),
                                   ('broken', ['Am'] * 4, None, 'beatbox', {'fills': False}), ('chorus_cor', H_, shift(hm, -12), 'hook', dict(RH, harm=True)),
                                   ('finale', ['Am', 'Am', 'F', 'F', 'G', 'G', 'E', 'E'], None, 'beatbox', {}), ('outro', ['Am', 'F', 'E', 'Am'], om, 'verse', dict(RV, fills=False))],
                 'rap', 'Am', 95)


def pause_goth():
    m = M('E5:8 G5:8', 'F#5:8 D5:8', 'E5:8 B4:8', 'D#5:14')
    return loop_song('c4_pause', 70, ['Em', 'C', 'Em', 'B'], m, 4, 85, soft=True)


def pause_rap():
    m = M('C5:4 Eb5:4 G5:8', 'Ab5:8 G5:8', 'Eb5:4 F5:4 G5:8', 'D5:14')
    return loop_song('c5_pause', 86, ['Cm', 'Ab', 'Eb', 'Bb'], m, 4, 96, soft=True)


if __name__ == '__main__':
    F = {'cathedral': cathedral, 'gargoyle': gargoyle_song, 'raven': raven, 'countess': countess_song, 'concrete': concrete, 'subway': subway,
         'court': court, 'alley': alley, 'pitch': pitch, 'pgoth': pause_goth, 'prap': pause_rap}
    for nm in sys.argv[1:]:
        print(nm, round(F[nm](), 1), 's', flush=True)
