import sys
from songlib import *


def mel(*bars):
    return [[(a, b, n(c)) for a, b, c in bar] for bar in bars]


def shift(melody, k):
    return [[(a, b, m + k) for a, b, m in bar] for bar in melody]


def play(S, bar, melody, gain=0.19, duty=0.25, harm_key=None, harm_oct=False, vib=0.004, rev=0.3, rec=True):
    for k, notes in enumerate(melody):
        for a, ln, m in notes:
            t = S.T(bar + k, a)
            S.lead2(m, t, ln * S.STEP, gain=gain, duty=duty, vib=vib, rev=rev, rec=rec)
            if harm_key:
                S.lead2(third_below(m, harm_key), t, ln * S.STEP, gain=gain * 0.55, duty=0.5, rec=False, echo=False, pan=0.3, rev=rev)
            if harm_oct:
                S.lead2(m - 12, t, ln * S.STEP, gain=gain * 0.4, duty=0.5, rec=False, echo=False, pan=-0.3, rev=rev)


def drums(S, bar, style, fill=False):
    t = S.T(bar)
    st = S.STEP
    if style == 'four':
        for s in (0, 4, 8, 12):
            S.kick(t + s * st)
        for s in (4, 12):
            S.snare(t + s * st, clap=True)
        for s in range(16):
            S.hat(t + s * st, gain=0.085 if s % 4 == 2 else 0.035, open_=(s % 4 == 2))
    elif style == 'pop':
        for s in (0, 8, 10):
            S.kick(t + s * st)
        for s in (4, 12):
            S.snare(t + s * st, clap=True)
        for s in range(0, 16, 2):
            S.hat(t + s * st, gain=0.06, open_=(s == 14))
    elif style == 'half':
        S.kick(t); S.kick(t + 10 * st, gain=0.4)
        S.snare(t + 8 * st)
        for s in range(0, 16, 4):
            S.hat(t + s * st, gain=0.05)
    elif style == 'rock':
        for s in (0, 8, 10):
            S.kick(t + s * st)
        for s in (4, 12):
            S.snare(t + s * st)
        for s in range(0, 16, 2):
            S.hat(t + s * st, gain=0.07)
    elif style == 'rockch':
        for s in (0, 6, 8):
            S.kick(t + s * st)
        for s in (4, 12):
            S.snare(t + s * st, clap=True)
        for s in range(0, 16, 2):
            S.hat(t + s * st, gain=0.08, open_=True)
    elif style == 'gallop':
        for b in range(4):
            for s in (0, 2, 3):
                S.kick(t + (b * 4 + s) * st, gain=0.48)
        for s in (4, 12):
            S.snare(t + s * st)
        for s in (0, 8):
            S.hat(t + s * st, open_=True)
    elif style == 'blast':
        for s in range(16):
            S.kick(t + s * st, gain=0.34)
        for s in (4, 12):
            S.snare(t + s * st)
    elif style == 'eighths':
        for s in range(0, 16, 2):
            S.kick(t + s * st, gain=0.44)
        for s in (4, 12):
            S.snare(t + s * st)
        for s in (0, 8):
            S.hat(t + s * st, open_=True)
    elif style == 'goth':
        for s in (0, 10):
            S.kick(t + s * st)
        for s in (4, 12):
            S.snare(t + s * st)
        for s in range(0, 16, 2):
            S.hat(t + s * st, gain=0.05)
        S.tom(t + 14 * st, 41, gain=0.22)
    if fill:
        S.fill(bar, 'snare' if style not in ('goth',) else 'tom', start=12)


# ======================= 1-1 SYNTHPOP: Neon Skate =======================
def synth():
    S = Song2(118, 49, seed=21)
    ROOT = {'Am': 45, 'F': 41, 'C': 48, 'G': 43, 'E': 40, 'Dm': 50, 'Em': 52}
    ARP = {'Am': [69, 72, 76, 81], 'F': [65, 69, 72, 77], 'C': [67, 72, 76, 79], 'G': [67, 71, 74, 79], 'E': [64, 68, 71, 76],
           'Dm': [62, 65, 69, 74], 'Em': [64, 67, 71, 76]}
    V = ['Am', 'F', 'C', 'G', 'Am', 'F', 'G', 'E']
    PRE = ['Dm', 'Em', 'F', 'G']
    CH = ['F', 'G', 'Am', 'C', 'F', 'G', 'E', 'Am']
    BRK = ['Am', 'F', 'C', 'G'] * 2
    secs = [('intro', ['Am', 'F', 'C', 'G'], 0), ('verse', V, 0), ('pre', PRE, 0), ('chorus', CH, 0), ('breakdown', BRK, 0),
            ('pre', PRE, 0), ('chorus', CH, 2), ('outro', ['Am', 'F', 'G', 'Am'], 2)]
    VM = mel([(0, 3, 'E5'), (3, 3, 'E5'), (6, 2, 'D5'), (8, 4, 'C5'), (12, 4, 'A4')],
             [(0, 3, 'C5'), (3, 3, 'C5'), (6, 2, 'D5'), (8, 8, 'A4')],
             [(0, 3, 'E5'), (3, 3, 'E5'), (6, 2, 'G5'), (8, 4, 'E5'), (12, 4, 'C5')],
             [(0, 4, 'D5'), (4, 4, 'B4'), (8, 8, 'G4')],
             [(0, 3, 'A5'), (3, 3, 'G5'), (6, 2, 'E5'), (8, 4, 'C5'), (12, 4, 'E5')],
             [(0, 3, 'F5'), (3, 3, 'E5'), (6, 2, 'C5'), (8, 8, 'A4')],
             [(0, 3, 'D5'), (3, 3, 'E5'), (6, 2, 'G5'), (8, 4, 'B5'), (12, 4, 'A5')],
             [(0, 8, 'G#5'), (8, 6, 'B5')])
    PM = mel([(0, 4, 'F5'), (4, 4, 'A5'), (8, 4, 'D5'), (12, 4, 'F5')], [(0, 4, 'G5'), (4, 4, 'B5'), (8, 4, 'E5'), (12, 4, 'G5')],
             [(0, 4, 'A5'), (4, 4, 'C6'), (8, 4, 'F5'), (12, 4, 'A5')], [(0, 14, 'B5')])
    CM = mel([(0, 2, 'C6'), (2, 2, 'C6'), (4, 4, 'A5'), (8, 2, 'C6'), (10, 2, 'D6'), (12, 4, 'C6')],
             [(0, 2, 'B5'), (2, 2, 'B5'), (4, 4, 'G5'), (8, 4, 'D5'), (12, 4, 'G5')],
             [(0, 2, 'C6'), (2, 2, 'C6'), (4, 4, 'E6'), (8, 4, 'D6'), (12, 4, 'C6')],
             [(0, 12, 'G5'), (12, 4, 'E5')],
             [(0, 2, 'C6'), (2, 2, 'C6'), (4, 4, 'A5'), (8, 2, 'C6'), (10, 2, 'D6'), (12, 4, 'C6')],
             [(0, 2, 'D6'), (2, 2, 'D6'), (4, 4, 'B5'), (8, 4, 'G5'), (12, 4, 'B5')],
             [(0, 4, 'G#5'), (4, 4, 'B5'), (8, 4, 'E6'), (12, 4, 'D6')],
             [(0, 14, 'A5')])
    OM = mel([(0, 16, 'E5')], [(0, 16, 'C5')], [(0, 8, 'D5'), (8, 8, 'B4')], [(0, 14, 'A4')])
    bar = 0
    for name, chords, kup in secs:
        if name in ('chorus', 'breakdown'):
            S.crash(S.T(bar)); S.mark(name, S.T(bar))
        mm = {'verse': VM, 'pre': PM, 'chorus': CM, 'outro': OM}.get(name)
        if mm:
            play(S, bar, shift(mm, kup), gain=0.19, harm_key='Am' if (name == 'chorus' and kup == 0) else None, harm_oct=(name == 'chorus' and kup > 0))
        for k, ch in enumerate(chords):
            t = S.T(bar + k)
            r, tones = ROOT[ch] + kup, [x + kup for x in ARP[ch]]
            phrase_end = (k % 4 == 3)
            pat = [0, 1, 2, 3] * 4 if name not in ('chorus',) else [0, 2, 1, 3, 2, 1, 3, 2] * 2
            for s, idx in enumerate(pat):
                S.arp(tones[idx], t + s * S.STEP, gain=(0.05 if name == 'intro' else 0.075), pan=-0.45 if s % 2 else 0.45)
            if name == 'breakdown':
                S.pad([x - 12 for x in tones[:3]], t, S.BAR * 0.98, gain=0.04, rev=0.7)
                if k % 2 == 0:
                    S.bell(tones[3] + 12, t + 6 * S.STEP, gain=0.04)
                S.bass(r, t, 8 * S.STEP); S.bass(r + 12, t + 8 * S.STEP, 8 * S.STEP)
                drums(S, bar + k, 'half', fill=(k == 7))
                continue
            if name in ('chorus', 'outro'):
                S.pad([x - 12 for x in tones[:3]], t, S.BAR * 0.98, gain=0.032)
            if name == 'intro':
                S.bass(r, t, S.BAR * 0.9, gain=0.22)
                if k >= 2:
                    for s in (0, 4, 8, 12):
                        S.kick(t + s * S.STEP, gain=0.4)
                if k == 3:
                    S.fill(bar + k, start=12)
                continue
            for s in range(0, 16, 2):
                S.bass(r + (12 if s % 4 == 2 else 0), t + s * S.STEP, 2 * S.STEP)
            if name == 'verse':
                drums(S, bar + k, 'pop', fill=phrase_end)
                if k % 2 == 1:
                    S.chorus_gtr(tones[3] + 12, t + 14 * S.STEP, 2 * S.STEP, gain=0.04)
            elif name == 'pre':
                drums(S, bar + k, 'pop', fill=(k == 3))
            elif name == 'chorus':
                drums(S, bar + k, 'four', fill=phrase_end)
            elif name == 'outro':
                if k < 3:
                    drums(S, bar + k, 'pop')
                else:
                    S.kick(t)
        bar += len(chords)
    tE = S.T(bar)
    S.kick(tE); S.crash(tE, 0.14); S.bass(47, tE, 1.2)
    for m in (71, 74, 78):
        S.lead2(m, tE, 1.6, gain=0.08, duty=0.5, rec=False, echo=False)
    S.lead2(n('B5'), tE, 1.6)
    S.mark('final', tE)
    return S.finish2('synth2', tE)


# ======================= 2-1 ROCK: Sunset Highway =======================
def rock():
    S = Song2(136, 57, seed=22)
    ROOT = {'A': 45, 'G': 43, 'D': 50, 'E': 40, 'F#m': 42}
    V = ['A', 'G', 'D', 'A', 'A', 'G', 'D', 'E']
    CH = ['D', 'A', 'E', 'F#m', 'D', 'A', 'E', 'E']
    SOLO = ['F#m', 'D', 'A', 'E'] * 2
    secs = [('intro', ['A'] * 4), ('verse', V), ('chorus', CH), ('verse', V), ('chorus', CH), ('solo', SOLO), ('chorus', CH),
            ('outro', ['A', 'G', 'D', 'A'])]
    VM = mel([(0, 4, 'E5'), (4, 2, 'C#5'), (6, 2, 'E5'), (8, 6, 'A5'), (14, 2, 'E5')], [(0, 4, 'D5'), (4, 4, 'B4'), (8, 8, 'G4')],
             [(0, 2, 'F#5'), (2, 2, 'E5'), (4, 4, 'D5'), (8, 4, 'A4'), (12, 4, 'D5')], [(0, 12, 'C#5'), (12, 4, 'E5')],
             [(0, 4, 'A5'), (4, 2, 'G5'), (6, 2, 'E5'), (8, 6, 'C#5'), (14, 2, 'E5')], [(0, 4, 'D5'), (4, 4, 'G5'), (8, 8, 'B4')],
             [(0, 2, 'A5'), (2, 2, 'F#5'), (4, 4, 'D5'), (8, 4, 'F#5'), (12, 4, 'A5')], [(0, 8, 'B4'), (8, 6, 'E5')])
    CM = mel([(0, 4, 'D5'), (4, 4, 'F#5'), (8, 8, 'A5')], [(0, 4, 'C#6'), (4, 4, 'B5'), (8, 8, 'A5')],
             [(0, 4, 'G#5'), (4, 4, 'B5'), (8, 4, 'E5'), (12, 4, 'G#5')], [(0, 12, 'F#5'), (12, 4, 'A5')],
             [(0, 4, 'D5'), (4, 4, 'F#5'), (8, 8, 'A5')], [(0, 4, 'C#6'), (4, 4, 'E6'), (8, 8, 'C#6')],
             [(0, 4, 'B5'), (4, 4, 'G#5'), (8, 4, 'E5'), (12, 4, 'B5')], [(0, 14, 'B5')])
    OM = mel([(0, 16, 'E5')], [(0, 16, 'D5')], [(0, 8, 'F#5'), (8, 8, 'A5')], [(0, 14, 'A5')])
    PENT = [n('F#4'), n('A4'), n('B4'), n('C#5'), n('E5'), n('F#5'), n('A5'), n('B5'), n('C#6'), n('E6')]
    bar, nch = 0, 0
    for name, chords in secs:
        if name in ('chorus', 'solo'):
            S.crash(S.T(bar)); S.mark(name, S.T(bar))
        if name == 'chorus':
            nch += 1
        mm = {'verse': VM, 'chorus': CM, 'outro': OM}.get(name)
        if mm:
            play(S, bar, mm, gain=0.19, harm_key='A' if (name == 'chorus' and nch >= 2) else None)
        for k, ch in enumerate(chords):
            t, r = S.T(bar + k), ROOT[ch]
            pe = k % 4 == 3
            if name == 'intro':
                for s in range(0, 16, 2):
                    rr = 43 if s == 12 else (50 if s == 14 else 45)
                    S.power(rr + 12, t + s * S.STEP, 2 * S.STEP, mute=(s % 4 != 0 and s < 12), gain=0.1)
                if k >= 2:
                    drums(S, bar + k, 'rock', fill=(k == 3))
            elif name == 'verse':
                S.power(r + 12, t, 2 * S.STEP, gain=0.11)
                for s in range(2, 16, 2):
                    S.power(r + 12, t + s * S.STEP, 2 * S.STEP, mute=True, gain=0.1)
                drums(S, bar + k, 'rock', fill=pe)
                if pe:
                    for i, s in enumerate((12, 13, 14, 15)):
                        S.lead2(PENT[4 - i] + 12, t + s * S.STEP, S.STEP, gain=0.1, rec=False, echo=False, pan=0.35)
            elif name == 'chorus':
                for s in (0, 4, 8, 12):
                    S.power(r + 12, t + s * S.STEP, 4 * S.STEP, gain=0.11)
                drums(S, bar + k, 'rockch', fill=pe)
                if k in (1, 3, 5):
                    S.hey(t + 4 * S.STEP); S.hey(t + 12 * S.STEP)
            elif name == 'solo':
                for s in range(0, 16, 2):
                    S.power(r + 12, t + s * S.STEP, 2 * S.STEP, mute=(s % 8 != 0), gain=0.09)
                drums(S, bar + k, 'rockch', fill=pe)
                for i in range(8):
                    idx = (k * 3 + [0, 2, 4, 3, 5, 4, 2, 1][i]) % len(PENT)
                    S.lead2(PENT[idx] + 12 if PENT[idx] < 64 else PENT[idx], t + i * 2 * S.STEP, 2 * S.STEP, gain=0.16, duty=0.25)
            elif name == 'outro':
                S.power(r + 12, t, 8 * S.STEP, gain=0.11); S.power(r + 12, t + 8 * S.STEP, 8 * S.STEP, gain=0.1)
                if k < 3:
                    drums(S, bar + k, 'rock')
                else:
                    S.kick(t)
            for s in range(0, 16, 2):
                S.bass(r - (12 if r > 45 else 0) + (12 if name in ('chorus', 'solo') and s % 4 == 2 else 0), t + s * S.STEP, 2 * S.STEP)
        bar += len(chords)
    tE = S.T(bar)
    S.kick(tE); S.crash(tE, 0.14); S.power(57, tE, 1.6, gain=0.13); S.bass(45, tE, 1.2); S.hey(tE)
    S.lead2(n('A5'), tE, 1.6)
    S.mark('final', tE)
    return S.finish2('rock2', tE)


# ======================= 3-1 METAL: Forge of Fury =======================
def metal():
    S = Song2(155, 61, seed=23)
    E, F, G, A, C, D, B, Bb = 40, 41, 43, 45, 48, 50, 47, 46
    RIFF = [[E, E, E, E], [E, E, G, A], [E, E, E, E], [C, C, D, D]]
    CH = [C, D, E, E, C, D, B, B]
    PRE = [A, C, D, B]
    secs = [('intro', 4), ('verse', 8), ('pre', 4), ('chorus', 8), ('breakdown', 8), ('verse', 8), ('solo', 8), ('chorus', 8), ('outro', 4)]
    CM = mel([(0, 4, 'E5'), (4, 4, 'G5'), (8, 8, 'C6')], [(0, 4, 'B5'), (4, 4, 'A5'), (8, 8, 'F#5')],
             [(0, 4, 'G5'), (4, 4, 'F#5'), (8, 4, 'E5'), (12, 4, 'B4')], [(0, 14, 'E5')],
             [(0, 4, 'E5'), (4, 4, 'G5'), (8, 8, 'C6')], [(0, 4, 'D6'), (4, 4, 'C6'), (8, 8, 'B5')],
             [(0, 4, 'D#6'), (4, 4, 'B5'), (8, 4, 'F#5'), (12, 4, 'D#5')], [(0, 14, 'B5')])
    HARM = [n('E5'), n('F#5'), n('G5'), n('A5'), n('B5'), n('C6'), n('D#6'), n('E6')]
    bar, nch = 0, 0
    for name, nb in secs:
        if name in ('chorus', 'breakdown', 'solo'):
            S.mark(name, S.T(bar)); S.crash(S.T(bar))
        if name == 'chorus':
            nch += 1
            play(S, bar, CM, gain=0.18, harm_key='Em' if nch == 2 else None, harm_oct=(nch == 1))
        for k in range(nb):
            t = S.T(bar + k)
            pe = k % 4 == 3
            if name in ('intro', 'verse'):
                for b_, r in enumerate(RIFF[k % 4]):
                    tb = t + b_ * 4 * S.STEP
                    for s, ln in ((0, 2), (2, 1), (3, 1)):
                        S.power(r + 12, tb + s * S.STEP, ln * S.STEP, mute=not (b_ == 0 and s == 0), gain=0.1)
                        S.bass(r, tb + s * S.STEP, ln * S.STEP, gain=0.26)
                if name == 'verse' or k >= 2:
                    drums(S, bar + k, 'gallop', fill=pe)
                elif k == 1:
                    for s in (8, 10, 12, 13, 14, 15):
                        S.tom(t + s * S.STEP, 47 - (s - 8))
                if name == 'verse' and k % 4 == 0:
                    S.crash(t, 0.09)
            elif name == 'pre':
                r = PRE[k]
                for s in range(16):
                    S.power(r + 12, t + s * S.STEP, S.STEP, mute=True, gain=0.095)
                for s in range(0, 16, 2):
                    S.bass(r, t + s * S.STEP, 2 * S.STEP)
                if k < 3:
                    drums(S, bar + k, 'eighths')
                else:
                    S.fill(bar + k, start=0)
            elif name == 'chorus':
                r = CH[k]
                S.crash(t, 0.1, rec=False)
                for s in (0, 4, 8, 12):
                    S.power(r + 12, t + s * S.STEP, 3 * S.STEP, gain=0.105)
                for s in range(0, 16, 2):
                    S.bass(r, t + s * S.STEP, 2 * S.STEP)
                drums(S, bar + k, 'blast', fill=(k == 7))
            elif name == 'breakdown':
                r = E if k % 4 < 2 else (C if k % 4 == 2 else D)
                for s in (0, 3, 6, 10):
                    S.power(r + 12, t + s * S.STEP, 2 * S.STEP, mute=(s != 0), gain=0.11)
                    S.bass(r, t + s * S.STEP, 2 * S.STEP)
                drums(S, bar + k, 'half', fill=(k == 7))
                if k % 2 == 1:
                    S.hey(t + 8 * S.STEP); S.hey(t + 12 * S.STEP)
                if k % 2 == 0:
                    for s in (12, 13, 14, 15):
                        S.tom(t + s * S.STEP, 45 - (s - 12) * 2, gain=0.26)
            elif name == 'solo':
                r = [E, C, D, B][k % 4]
                for b_ in range(4):
                    tb = t + b_ * 4 * S.STEP
                    for s, ln in ((0, 2), (2, 1), (3, 1)):
                        S.power(r + 12, tb + s * S.STEP, ln * S.STEP, mute=(s != 0), gain=0.09)
                        S.bass(r, tb + s * S.STEP, ln * S.STEP, gain=0.24)
                drums(S, bar + k, 'gallop', fill=pe)
                for i in range(8):
                    idx = (k * 2 + [0, 1, 2, 4, 3, 2, 5, 4][i]) % len(HARM)
                    S.lead2(HARM[idx], t + i * 2 * S.STEP, 2 * S.STEP, gain=0.16)
            elif name == 'outro':
                r = [E, C, D, E][k]
                S.power(r + 12, t, 14 * S.STEP, gain=0.11); S.bass(r, t, 14 * S.STEP)
                if k < 3:
                    drums(S, bar + k, 'half')
                    S.lead2(n('E5') + [0, 3, 5][k], t, 14 * S.STEP, gain=0.17)
                else:
                    S.kick(t)
        bar += nb
    tE = S.T(bar)
    S.kick(tE); S.crash(tE, 0.14); S.power(52, tE, 1.6, gain=0.13); S.bass(40, tE, 1.2); S.hey(tE)
    S.lead2(n('E5'), tE, 1.6)
    S.mark('final', tE)
    return S.finish2('metal2', tE)


# ======================= 4-1 GOTH ROCK: Moonlit Graves =======================
def goth():
    S = Song2(108, 45, seed=24)
    ROOT = {'Em': 40, 'C': 48, 'G': 43, 'D': 50, 'Am': 45, 'B': 47}
    TRI = {'Em': [64, 67, 71], 'C': [60, 64, 67], 'G': [59, 62, 67], 'D': [62, 66, 69], 'Am': [57, 60, 64], 'B': [59, 63, 66]}
    V = ['Em', 'C', 'G', 'D', 'Em', 'C', 'Am', 'B']
    CH = ['C', 'G', 'D', 'Em', 'C', 'G', 'B', 'B']
    secs = [('intro', ['Em', 'C', 'G', 'D']), ('verse', V), ('chorus', CH), ('bridge', ['Am', 'Em', 'Am', 'B']), ('verse', V), ('chorus', CH),
            ('outro', ['Em', 'C', 'B', 'Em'])]
    VM = mel([(0, 6, 'G4'), (6, 2, 'F#4'), (8, 8, 'E4')], [(0, 6, 'G4'), (6, 2, 'A4'), (8, 8, 'E4')],
             [(0, 6, 'B4'), (6, 2, 'A4'), (8, 4, 'G4'), (12, 4, 'D4')], [(0, 12, 'F#4'), (12, 4, 'A4')],
             [(0, 6, 'B4'), (6, 2, 'A4'), (8, 8, 'G4')], [(0, 6, 'E5'), (6, 2, 'D5'), (8, 8, 'C5')],
             [(0, 6, 'C5'), (6, 2, 'B4'), (8, 4, 'A4'), (12, 4, 'E4')], [(0, 14, 'F#4')])
    CM = mel([(0, 4, 'E5'), (4, 4, 'D5'), (8, 8, 'C5')], [(0, 4, 'D5'), (4, 4, 'B4'), (8, 8, 'G4')],
             [(0, 4, 'A4'), (4, 4, 'D5'), (8, 4, 'F#5'), (12, 4, 'E5')], [(0, 12, 'E5'), (12, 4, 'B4')],
             [(0, 4, 'E5'), (4, 4, 'G5'), (8, 8, 'E5')], [(0, 4, 'D5'), (4, 4, 'G5'), (8, 8, 'B4')],
             [(0, 4, 'D#5'), (4, 4, 'F#5'), (8, 4, 'B4'), (12, 4, 'D#5')], [(0, 14, 'B4')])
    OM = mel([(0, 16, 'G4')], [(0, 16, 'E4')], [(0, 8, 'D#4'), (8, 8, 'F#4')], [(0, 14, 'E4')])
    bar, nch = 0, 0
    for name, chords in secs:
        if name in ('chorus', 'bridge'):
            S.crash(S.T(bar)); S.mark(name, S.T(bar))
        if name == 'chorus':
            nch += 1
        mm = {'verse': VM, 'chorus': CM, 'outro': OM}.get(name)
        if mm:
            play(S, bar, mm, gain=0.2, vib=0.008, rev=0.55, harm_oct=False, harm_key='Em' if nch == 2 and name == 'chorus' else None)
        for k, ch in enumerate(chords):
            t, r, tr = S.T(bar + k), ROOT[ch], TRI[ch]
            pe = k % 4 == 3
            arp = [tr[0], tr[1], tr[2], tr[0] + 12, tr[2], tr[1], tr[2], tr[0] + 12]
            for i, m in enumerate(arp):
                S.chorus_gtr(m, t + i * 2 * S.STEP, 2 * S.STEP, gain=0.06 if name != 'bridge' else 0.045)
            S.organ(tr, t, S.BAR * 0.98, gain=0.022 if name not in ('chorus', 'bridge') else 0.032)
            if name == 'bridge':
                for i, s in enumerate((0, 4, 8, 12)):
                    S.bell(tr[i % 3] + 24, t + s * S.STEP, gain=0.045)
                S.bass(r, t, S.BAR * 0.9, gain=0.24)
                S.kick(t); S.tom(t + 12 * S.STEP, 38, gain=0.25)
                continue
            pat = [0, 12, 7, 12, 0, 12, 10, 12]
            for i, s in enumerate(range(0, 16, 2)):
                S.bass(r + pat[i], t + s * S.STEP, 2 * S.STEP, gain=0.24, bright=0.35)
            if name == 'chorus':
                for i, s in enumerate((0, 4, 8, 12)):
                    S.bell(tr[i % 3] + 12, t + s * S.STEP, gain=0.04)
            if name == 'intro' and k < 2:
                continue
            if name == 'outro' and k == 3:
                S.kick(t); continue
            drums(S, bar + k, 'goth', fill=pe and name != 'intro')
        bar += len(chords)
    tE = S.T(bar)
    S.kick(tE); S.crash(tE, 0.13); S.organ(TRI['Em'], tE, 2.0, gain=0.04); S.bass(40, tE, 1.4)
    S.bell(88, tE, 0.06); S.lead2(n('E5'), tE, 1.6)
    S.mark('final', tE)
    return S.finish2('goth2', tE, rev_wet=0.3, cho=True)


# ======================= 5-1 POWER METAL: Dawn of Steel =======================
def power():
    S = Song2(160, 57, seed=25)
    ROOT = {'Em': 40, 'C': 48, 'D': 50, 'B': 47, 'G': 43, 'Am': 45}
    TRI = {'Em': [64, 67, 71], 'C': [60, 64, 67], 'D': [62, 66, 69], 'B': [59, 63, 66], 'G': [59, 62, 67], 'Am': [57, 60, 64]}
    V = ['Em', 'C', 'D', 'B', 'Em', 'C', 'D', 'Em']
    PRE = ['Am', 'C', 'D', 'D']
    CH = ['G', 'D', 'Em', 'C', 'G', 'D', 'C', 'B']
    SOLO = ['Em', 'C', 'D', 'B'] * 2
    secs = [('intro', ['Em', 'C', 'D', 'Em'], 0), ('verse', V, 0), ('pre', PRE, 0), ('chorus', CH, 0), ('verse', V, 0), ('pre', PRE, 0),
            ('solo', SOLO, 0), ('chorus', CH, 2), ('outro', ['G', 'D', 'Em', 'Em'], 2)]
    IM = mel([(0, 4, 'B5'), (4, 4, 'G5'), (8, 4, 'E5'), (12, 4, 'G5')], [(0, 4, 'C6'), (4, 4, 'G5'), (8, 8, 'E5')],
             [(0, 4, 'D6'), (4, 4, 'A5'), (8, 4, 'F#5'), (12, 4, 'A5')], [(0, 14, 'B5')])
    VM = mel([(0, 4, 'E5'), (4, 4, 'G5'), (8, 4, 'B5'), (12, 4, 'A5')], [(0, 4, 'G5'), (4, 4, 'E5'), (8, 8, 'C5')],
             [(0, 4, 'D5'), (4, 4, 'F#5'), (8, 4, 'A5'), (12, 4, 'F#5')], [(0, 8, 'D#5'), (8, 8, 'F#5')],
             [(0, 4, 'B5'), (4, 4, 'A5'), (8, 4, 'G5'), (12, 4, 'E5')], [(0, 4, 'E5'), (4, 4, 'G5'), (8, 8, 'C6')],
             [(0, 4, 'B5'), (4, 4, 'A5'), (8, 4, 'F#5'), (12, 4, 'D5')], [(0, 14, 'E5')])
    PM = mel([(0, 8, 'C5'), (8, 8, 'E5')], [(0, 8, 'E5'), (8, 8, 'G5')], [(0, 8, 'F#5'), (8, 8, 'A5')], [(0, 14, 'D6')])
    CM = mel([(0, 4, 'D5'), (4, 4, 'G5'), (8, 8, 'B5')], [(0, 4, 'A5'), (4, 4, 'F#5'), (8, 8, 'D6')],
             [(0, 4, 'B5'), (4, 4, 'G5'), (8, 4, 'E5'), (12, 4, 'G5')], [(0, 12, 'E5'), (12, 4, 'G5')],
             [(0, 4, 'D5'), (4, 4, 'G5'), (8, 8, 'B5')], [(0, 4, 'A5'), (4, 4, 'D6'), (8, 8, 'F#5')],
             [(0, 4, 'G5'), (4, 4, 'E5'), (8, 4, 'C5'), (12, 4, 'E5')], [(0, 14, 'D#5')])
    OM = mel([(0, 16, 'G5')], [(0, 16, 'F#5')], [(0, 16, 'E5')], [(0, 14, 'B4')])
    HARM = [n('E5'), n('F#5'), n('G5'), n('A5'), n('B5'), n('C6'), n('D6'), n('E6')]
    bar = 0
    for name, chords, kup in secs:
        if name in ('chorus', 'solo'):
            S.crash(S.T(bar)); S.mark(name, S.T(bar))
        mm = {'intro': IM, 'verse': VM, 'pre': PM, 'chorus': CM, 'outro': OM}.get(name)
        if mm:
            play(S, bar, shift(mm, kup), gain=0.18, harm_key='Em' if (name in ('intro', 'chorus') and kup == 0) else None,
                 harm_oct=(name == 'chorus' and kup > 0))
        for k, ch in enumerate(chords):
            t, r, tr = S.T(bar + k), ROOT[ch] + kup, [x + kup for x in TRI[ch]]
            pe = k % 4 == 3
            if name in ('intro', 'chorus', 'outro', 'pre'):
                S.pad(tr, t, S.BAR * 0.98, gain=0.034, rate=3.0)
            if name in ('intro', 'outro'):
                S.power(r + 12, t, 8 * S.STEP, gain=0.11); S.power(r + 12, t + 8 * S.STEP, 8 * S.STEP, gain=0.1)
                S.bass(r, t, 8 * S.STEP); S.bass(r, t + 8 * S.STEP, 8 * S.STEP)
                if (name == 'intro' and k >= 1) or (name == 'outro' and k < 3):
                    drums(S, bar + k, 'eighths', fill=(name == 'intro' and k == 3))
                elif name == 'outro':
                    S.kick(t)
            elif name in ('verse', 'solo'):
                for b_ in range(4):
                    tb = t + b_ * 4 * S.STEP
                    for s, ln in ((0, 2), (2, 1), (3, 1)):
                        S.power(r + 12, tb + s * S.STEP, ln * S.STEP, mute=not (b_ == 0 and s == 0), gain=0.1)
                        S.bass(r, tb + s * S.STEP, ln * S.STEP, gain=0.25)
                drums(S, bar + k, 'eighths', fill=pe)
                if name == 'solo':
                    for i in range(8):
                        idx = (k * 2 + [0, 2, 4, 2, 5, 4, 6, 5][i]) % len(HARM)
                        S.lead2(HARM[idx], t + i * 2 * S.STEP, 2 * S.STEP, gain=0.16)
                        S.lead2(third_below(HARM[idx], 'Em'), t + i * 2 * S.STEP, 2 * S.STEP, gain=0.08, duty=0.5, rec=False, echo=False, pan=0.3)
            elif name == 'pre':
                for s in range(0, 16, 2):
                    S.power(r + 12, t + s * S.STEP, 2 * S.STEP, gain=0.1); S.bass(r, t + s * S.STEP, 2 * S.STEP)
                if k < 3:
                    drums(S, bar + k, 'rock')
                else:
                    S.fill(bar + k, start=0)
            elif name == 'chorus':
                for s in (0, 4, 8, 12):
                    S.power(r + 12, t + s * S.STEP, 4 * S.STEP, gain=0.105)
                for s in range(0, 16, 2):
                    S.bass(r + (12 if s % 4 == 2 else 0), t + s * S.STEP, 2 * S.STEP)
                drums(S, bar + k, 'blast', fill=pe)
                S.crash(t, 0.08, rec=False)
        bar += len(chords)
    tE = S.T(bar)
    S.kick(tE); S.crash(tE, 0.14); S.power(54, tE, 1.6, gain=0.13); S.pad([66, 69, 73], tE, 1.8, gain=0.05, rate=3.0)
    S.bass(42, tE, 1.2); S.lead2(n('F#5'), tE, 1.6)
    S.mark('final', tE)
    return S.finish2('power2', tE)


if __name__ == '__main__':
    for nm in sys.argv[1:]:
        secs = {'synth': synth, 'rock': rock, 'metal': metal, 'goth': goth, 'power': power}[nm]()
        print(nm, round(secs, 1), 's', flush=True)
