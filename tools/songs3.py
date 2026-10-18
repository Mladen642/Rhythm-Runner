import sys
from songlib import *
from songs2 import mel, shift, play, drums

ARPS = {'Am': [69, 72, 76, 81], 'F': [65, 69, 72, 77], 'C': [67, 72, 76, 79], 'G': [67, 71, 74, 79], 'E': [64, 68, 71, 76],
        'Dm': [62, 65, 69, 74], 'Em': [64, 67, 71, 76], 'Bb': [62, 65, 70, 74], 'A': [64, 69, 73, 76], 'D': [62, 66, 69, 74],
        'Bm': [62, 66, 71, 74], 'F#m': [61, 66, 69, 73], 'Cm': [63, 67, 72, 75], 'Ab': [63, 68, 72, 75], 'Eb': [63, 67, 70, 75],
        'Gm': [62, 67, 70, 74], 'B': [63, 66, 71, 75]}
ROOTS = {'Am': 45, 'F': 41, 'C': 48, 'G': 43, 'E': 40, 'Dm': 50, 'Em': 40, 'Bb': 46, 'A': 45, 'D': 50, 'Bm': 47, 'F#m': 42,
         'Cm': 48, 'Ab': 44, 'Eb': 51, 'Gm': 43, 'B': 47}


def synth_bar(S, bar, ch, name, kup=0, arp_gain=0.07, pattern=None, pad=False, bass='oct', style=None, fill=False, gated=False):
    t = S.T(bar)
    tones = [x + kup for x in ARPS[ch]]
    r = ROOTS[ch] + kup
    pat = pattern or [0, 1, 2, 3] * 4
    for s, idx in enumerate(pat):
        S.arp(tones[idx], t + s * S.STEP, gain=arp_gain, pan=-0.45 if s % 2 else 0.45)
    if pad:
        S.pad([x - 12 for x in tones[:3]], t, S.BAR * 0.98, gain=0.03)
    if gated:
        for s in (0, 3, 6, 10, 12):
            for m in tones[:3]:
                S.arp(m - 12, t + s * S.STEP, gain=0.03, pan=0.0, duty=0.5, length=S.STEP * 1.5)
    if bass == 'oct':
        for s in range(0, 16, 2):
            S.bass(r + (12 if s % 4 == 2 else 0), t + s * S.STEP, 2 * S.STEP)
    elif bass == 'pulse':
        for s in range(0, 16):
            S.bass(r, t + s * S.STEP, S.STEP, gain=0.22)
    elif bass == 'long':
        S.bass(r, t, 8 * S.STEP); S.bass(r + 12, t + 8 * S.STEP, 8 * S.STEP)
    if style:
        drums(S, bar, style, fill=fill)


# ======================= 1-2 Chrome Heart (E minor, 124) =======================
def chrome():
    S = Song2(124, 41, seed=31)
    V = ['Em', 'C', 'G', 'D'] * 2
    CH = ['C', 'D', 'Em', 'Em', 'C', 'D', 'B', 'B']
    secs = [('intro', ['Em', 'C', 'G', 'D']), ('verse', V), ('chorus', CH), ('verse', V), ('chorus', CH), ('outro', ['Em', 'C', 'D', 'Em'])]
    VM = mel([(0, 4, 'B4'), (4, 2, 'E5'), (6, 2, 'G5'), (8, 6, 'F#5'), (14, 2, 'E5')], [(0, 4, 'E5'), (4, 4, 'G5'), (8, 8, 'C5')],
             [(0, 2, 'D5'), (2, 2, 'D5'), (4, 4, 'B4'), (8, 4, 'D5'), (12, 4, 'G5')], [(0, 12, 'F#5'), (12, 4, 'A5')],
             [(0, 4, 'G5'), (4, 2, 'F#5'), (6, 2, 'E5'), (8, 6, 'B5'), (14, 2, 'A5')], [(0, 4, 'G5'), (4, 4, 'E5'), (8, 8, 'C5')],
             [(0, 2, 'B4'), (2, 2, 'D5'), (4, 4, 'G5'), (8, 4, 'B5'), (12, 4, 'A5')], [(0, 14, 'F#5')])
    CM = mel([(0, 2, 'E5'), (2, 2, 'G5'), (4, 4, 'C6'), (8, 2, 'B5'), (10, 2, 'C6'), (12, 4, 'E6')],
             [(0, 4, 'D6'), (4, 4, 'A5'), (8, 8, 'F#5')],
             [(0, 2, 'G5'), (2, 2, 'B5'), (4, 4, 'E6'), (8, 4, 'D6'), (12, 4, 'B5')], [(0, 12, 'E6'), (12, 4, 'B5')],
             [(0, 2, 'E5'), (2, 2, 'G5'), (4, 4, 'C6'), (8, 2, 'B5'), (10, 2, 'C6'), (12, 4, 'E6')],
             [(0, 4, 'F#6'), (4, 4, 'D6'), (8, 8, 'A5')],
             [(0, 4, 'D#6'), (4, 4, 'B5'), (8, 4, 'F#5'), (12, 4, 'A5')], [(0, 14, 'B5')])
    OM = mel([(0, 16, 'G5')], [(0, 16, 'E5')], [(0, 8, 'F#5'), (8, 8, 'A5')], [(0, 14, 'E5')])
    bar, nch = 0, 0
    for name, chords in secs:
        if name == 'chorus':
            S.crash(S.T(bar)); S.mark('chorus', S.T(bar)); nch += 1
        mm = {'verse': VM, 'chorus': CM, 'outro': OM}.get(name)
        if mm:
            play(S, bar, mm, gain=0.18, harm_key='Em' if (name == 'chorus' and nch == 2) else None, harm_oct=(name == 'chorus' and nch == 1))
        for k, ch in enumerate(chords):
            pe = k % 4 == 3
            if name == 'intro':
                synth_bar(S, bar + k, ch, name, arp_gain=0.05, bass='long', style='pop' if k >= 2 else None, fill=(k == 3))
            elif name == 'verse':
                synth_bar(S, bar + k, ch, name, style='pop', fill=pe, gated=(k % 2 == 1))
            elif name == 'chorus':
                synth_bar(S, bar + k, ch, name, pattern=[0, 2, 1, 3] * 4, pad=True, style='four', fill=pe, gated=True)
            else:
                synth_bar(S, bar + k, ch, name, pad=True, bass='long', style='pop' if k < 3 else None)
        bar += len(chords)
    tE = S.T(bar)
    S.kick(tE); S.crash(tE, 0.14); S.bass(40, tE, 1.2); S.lead2(n('E5'), tE, 1.6)
    for m in (64, 67, 71):
        S.lead2(m, tE, 1.6, gain=0.07, duty=0.5, rec=False, echo=False)
    S.mark('final', tE)
    return S.finish2('ch_chrome', tE)


# ======================= 1-3 Arcade Nights (D minor, 128, breakdown for the mini boss) =======================
def arcade():
    S = Song2(128, 41, seed=32)
    V = ['Dm', 'Bb', 'C', 'Am'] * 2
    CH = ['Bb', 'C', 'Dm', 'Dm', 'Bb', 'C', 'A', 'A']
    BRK = ['Dm', 'Bb', 'C', 'A'] * 2
    secs = [('intro', ['Dm', 'Bb', 'C', 'A']), ('verse', V), ('chorus', CH), ('breakdown', BRK), ('chorus', CH), ('outro', ['Dm', 'Bb', 'A', 'Dm'])]
    VM = mel([(0, 2, 'A4'), (2, 2, 'D5'), (4, 2, 'F5'), (6, 2, 'A5'), (8, 4, 'G5'), (12, 4, 'F5')], [(0, 4, 'D5'), (4, 4, 'F5'), (8, 8, 'Bb4')],
             [(0, 2, 'C5'), (2, 2, 'E5'), (4, 2, 'G5'), (6, 2, 'C6'), (8, 4, 'Bb5'), (12, 4, 'G5')], [(0, 12, 'A5'), (12, 4, 'E5')],
             [(0, 2, 'A4'), (2, 2, 'D5'), (4, 2, 'F5'), (6, 2, 'A5'), (8, 4, 'D6'), (12, 4, 'C6')], [(0, 4, 'Bb5'), (4, 4, 'A5'), (8, 8, 'F5')],
             [(0, 2, 'G5'), (2, 2, 'A5'), (4, 2, 'Bb5'), (6, 2, 'C6'), (8, 4, 'A5'), (12, 4, 'G5')], [(0, 14, 'E5')])
    CM = mel([(0, 4, 'F5'), (4, 2, 'D5'), (6, 2, 'F5'), (8, 4, 'Bb5'), (12, 4, 'A5')], [(0, 4, 'G5'), (4, 2, 'E5'), (6, 2, 'G5'), (8, 4, 'C6'), (12, 4, 'Bb5')],
             [(0, 4, 'A5'), (4, 4, 'D6'), (8, 4, 'C6'), (12, 4, 'A5')], [(0, 12, 'D6'), (12, 4, 'A5')],
             [(0, 4, 'F5'), (4, 2, 'D5'), (6, 2, 'F5'), (8, 4, 'Bb5'), (12, 4, 'A5')], [(0, 4, 'G5'), (4, 2, 'C6'), (6, 2, 'E6'), (8, 4, 'D6'), (12, 4, 'C6')],
             [(0, 4, 'C#6'), (4, 4, 'E6'), (8, 4, 'A5'), (12, 4, 'C#6')], [(0, 14, 'A5')])
    OM = mel([(0, 16, 'F5')], [(0, 16, 'D5')], [(0, 8, 'C#5'), (8, 8, 'E5')], [(0, 14, 'D5')])
    bar, nch = 0, 0
    for name, chords in secs:
        if name in ('chorus', 'breakdown'):
            S.crash(S.T(bar)); S.mark(name, S.T(bar))
        if name == 'chorus':
            nch += 1
        mm = {'verse': VM, 'chorus': CM, 'outro': OM}.get(name)
        if mm:
            play(S, bar, mm, gain=0.18, duty=0.125 if name == 'verse' else 0.25, harm_key='Dm' if (name == 'chorus' and nch == 2) else None)
        for k, ch in enumerate(chords):
            pe = k % 4 == 3
            if name == 'intro':
                synth_bar(S, bar + k, ch, name, arp_gain=0.06, pattern=[0, 1, 2, 3, 2, 1] * 2 + [0, 1, 2, 3], bass='long', style='pop' if k >= 2 else None, fill=(k == 3))
            elif name == 'verse':
                synth_bar(S, bar + k, ch, name, pattern=[0, 3, 1, 3, 2, 3, 1, 3] * 2, style='pop', fill=pe)
            elif name == 'chorus':
                synth_bar(S, bar + k, ch, name, pattern=[0, 1, 2, 3] * 4, pad=True, style='four', fill=pe, gated=True)
            elif name == 'breakdown':
                synth_bar(S, bar + k, ch, name, arp_gain=0.05, pad=True, bass='long', style='half', fill=(k == 7))
                if k % 2 == 0:
                    S.bell(ARPS[ch][3] + 12, S.T(bar + k, 6), gain=0.04)
            else:
                synth_bar(S, bar + k, ch, name, pad=True, bass='long', style='pop' if k < 3 else None)
        bar += len(chords)
    tE = S.T(bar)
    S.kick(tE); S.crash(tE, 0.14); S.bass(50, tE, 1.2); S.lead2(n('D5'), tE, 1.6)
    S.mark('final', tE)
    return S.finish2('ch_arcade', tE)


# ======================= 1-4 Laser Love (F# minor, 132, final chorus up a key) =======================
def laser():
    S = Song2(132, 49, seed=33)
    V = ['F#m', 'D', 'A', 'E'] * 2
    PRE = ['Bm', 'D', 'E', 'E']
    CH = ['D', 'E', 'F#m', 'A', 'D', 'E', 'F#m', 'F#m']
    secs = [('intro', ['F#m', 'D', 'A', 'E'], 0), ('verse', V, 0), ('pre', PRE, 0), ('chorus', CH, 0), ('verse', V, 0), ('pre', PRE, 0),
            ('chorus', CH, 1), ('outro', ['F#m', 'D', 'E', 'F#m'], 1)]
    VM = mel([(0, 3, 'C#5'), (3, 3, 'C#5'), (6, 2, 'E5'), (8, 4, 'F#5'), (12, 4, 'A5')], [(0, 3, 'A5'), (3, 3, 'F#5'), (6, 2, 'D5'), (8, 8, 'F#5')],
             [(0, 3, 'E5'), (3, 3, 'E5'), (6, 2, 'C#5'), (8, 4, 'E5'), (12, 4, 'A5')], [(0, 4, 'G#5'), (4, 4, 'B5'), (8, 8, 'E5')],
             [(0, 3, 'F#5'), (3, 3, 'A5'), (6, 2, 'C#6'), (8, 4, 'B5'), (12, 4, 'A5')], [(0, 3, 'F#5'), (3, 3, 'D5'), (6, 2, 'F#5'), (8, 8, 'A5')],
             [(0, 3, 'C#6'), (3, 3, 'B5'), (6, 2, 'A5'), (8, 4, 'E5'), (12, 4, 'A5')], [(0, 14, 'G#5')])
    PM = mel([(0, 4, 'D5'), (4, 4, 'F#5'), (8, 4, 'B5'), (12, 4, 'F#5')], [(0, 4, 'F#5'), (4, 4, 'A5'), (8, 4, 'D6'), (12, 4, 'A5')],
             [(0, 4, 'G#5'), (4, 4, 'B5'), (8, 4, 'E6'), (12, 4, 'B5')], [(0, 14, 'G#5')])
    CM = mel([(0, 2, 'F#5'), (2, 2, 'A5'), (4, 4, 'D6'), (8, 2, 'C#6'), (10, 2, 'D6'), (12, 4, 'F#6')],
             [(0, 4, 'E6'), (4, 4, 'B5'), (8, 8, 'G#5')],
             [(0, 2, 'A5'), (2, 2, 'C#6'), (4, 4, 'F#6'), (8, 4, 'E6'), (12, 4, 'C#6')], [(0, 12, 'E6'), (12, 4, 'C#6')],
             [(0, 2, 'F#5'), (2, 2, 'A5'), (4, 4, 'D6'), (8, 2, 'C#6'), (10, 2, 'D6'), (12, 4, 'F#6')],
             [(0, 4, 'G#6'), (4, 4, 'E6'), (8, 8, 'B5')],
             [(0, 4, 'A5'), (4, 4, 'C#6'), (8, 4, 'E6'), (12, 4, 'C#6')], [(0, 14, 'F#6')])
    OM = mel([(0, 16, 'A5')], [(0, 16, 'F#5')], [(0, 8, 'G#5'), (8, 8, 'B5')], [(0, 14, 'F#5')])
    bar = 0
    for name, chords, kup in secs:
        if name == 'chorus':
            S.crash(S.T(bar)); S.mark('chorus', S.T(bar))
        mm = {'verse': VM, 'pre': PM, 'chorus': CM, 'outro': OM}.get(name)
        if mm:
            play(S, bar, shift(mm, kup - (12 if name == 'chorus' else 0)), gain=0.19, harm_oct=(name == 'chorus'))
        for k, ch in enumerate(chords):
            pe = k % 4 == 3
            if name == 'intro':
                synth_bar(S, bar + k, ch, name, kup, arp_gain=0.055, bass='pulse', style='four' if k >= 2 else None, fill=(k == 3))
            elif name == 'verse':
                synth_bar(S, bar + k, ch, name, kup, bass='pulse', style='pop', fill=pe, gated=True)
            elif name == 'pre':
                synth_bar(S, bar + k, ch, name, kup, pad=True, bass='oct', style='pop' if k < 3 else None)
                if k == 3:
                    S.fill(bar + k, start=0)
            elif name == 'chorus':
                synth_bar(S, bar + k, ch, name, kup, pattern=[0, 2, 1, 3] * 4, pad=True, style='four', fill=pe, gated=True)
            else:
                synth_bar(S, bar + k, ch, name, kup, pad=True, bass='long', style='four' if k < 3 else None)
        bar += len(chords)
    tE = S.T(bar)
    S.kick(tE); S.crash(tE, 0.14); S.bass(43, tE, 1.2); S.lead2(n('G5'), tE, 1.6)
    S.mark('final', tE)
    return S.finish2('ch_laser', tE)


# ======================= 1-5 Mainframe Meltdown (C minor, 136, the boss) =======================
def mainframe():
    S = Song2(136, 49, seed=34)
    V = ['Cm', 'Ab', 'Eb', 'Bb'] * 2
    CH = ['Ab', 'Bb', 'Cm', 'Cm', 'Ab', 'Bb', 'G', 'G']
    FIN = ['Cm', 'Cm', 'Ab', 'Ab', 'Bb', 'Bb', 'G', 'G']
    secs = [('intro', ['Cm'] * 4), ('verse', V), ('chorus', CH), ('verse_rev', V), ('chorus_cor', CH), ('finale', FIN), ('outro', ['Cm', 'Ab', 'G', 'Cm'])]
    VM = mel([(0, 2, 'C5'), (2, 2, 'Eb5'), (4, 2, 'G5'), (6, 2, 'C6'), (8, 4, 'Bb5'), (12, 4, 'G5')], [(0, 4, 'Ab5'), (4, 4, 'G5'), (8, 8, 'Eb5')],
             [(0, 2, 'Bb4'), (2, 2, 'Eb5'), (4, 2, 'G5'), (6, 2, 'Bb5'), (8, 4, 'Ab5'), (12, 4, 'G5')], [(0, 12, 'F5'), (12, 4, 'D5')],
             [(0, 2, 'C5'), (2, 2, 'Eb5'), (4, 2, 'G5'), (6, 2, 'C6'), (8, 4, 'D6'), (12, 4, 'Eb6')], [(0, 4, 'C6'), (4, 4, 'Ab5'), (8, 8, 'Eb5')],
             [(0, 2, 'G5'), (2, 2, 'Bb5'), (4, 2, 'Eb6'), (6, 2, 'D6'), (8, 4, 'Bb5'), (12, 4, 'F5')], [(0, 14, 'D5')])
    CM = mel([(0, 4, 'C6'), (4, 2, 'Ab5'), (6, 2, 'C6'), (8, 4, 'Eb6'), (12, 4, 'C6')], [(0, 4, 'D6'), (4, 2, 'Bb5'), (6, 2, 'D6'), (8, 4, 'F6'), (12, 4, 'D6')],
             [(0, 4, 'Eb6'), (4, 4, 'G6'), (8, 4, 'F6'), (12, 4, 'Eb6')], [(0, 12, 'C6'), (12, 4, 'G5')],
             [(0, 4, 'C6'), (4, 2, 'Ab5'), (6, 2, 'C6'), (8, 4, 'Eb6'), (12, 4, 'C6')], [(0, 4, 'D6'), (4, 2, 'F6'), (6, 2, 'D6'), (8, 4, 'Bb5'), (12, 4, 'D6')],
             [(0, 4, 'B5'), (4, 4, 'D6'), (8, 4, 'G6'), (12, 4, 'F6')], [(0, 14, 'D6')])
    OM = mel([(0, 16, 'G5')], [(0, 16, 'Eb5')], [(0, 8, 'D5'), (8, 8, 'B4')], [(0, 14, 'C5')])
    bar = 0
    for name, chords in secs:
        S.mark(name, S.T(bar))
        if name in ('chorus', 'chorus_cor'):
            S.crash(S.T(bar)); S.mark('chorus_any', S.T(bar))
        mm = {'verse': VM, 'verse_rev': VM, 'chorus': shift(CM, -12), 'chorus_cor': shift(CM, -12), 'outro': OM}.get(name)
        if mm:
            play(S, bar, mm, gain=0.18, harm_oct=name.startswith('chorus'), duty=0.25)
        for k, ch in enumerate(chords):
            t = S.T(bar + k)
            pe = k % 4 == 3
            if name == 'intro':
                synth_bar(S, bar + k, ch, name, arp_gain=0.05, bass='pulse', style='half' if k >= 1 else None, fill=(k == 3))
                if k == 0:
                    for i in range(6):
                        S.tom(t + i * 2 * S.STEP, 36 + i, gain=0.25)
            elif name in ('verse', 'verse_rev'):
                synth_bar(S, bar + k, ch, name, pattern=[0, 3, 2, 3, 1, 3, 2, 3] * 2, bass='pulse', style='four', fill=pe, gated=(name == 'verse_rev'))
                if name == 'verse_rev' and k % 2 == 1:
                    for s in (12, 13, 14, 15):
                        S.arp(ARPS[ch][s % 4] + 24, t + s * S.STEP, gain=0.05, pan=0.0)
            elif name in ('chorus', 'chorus_cor'):
                synth_bar(S, bar + k, ch, name, pattern=[0, 2, 1, 3] * 4, pad=True, bass='oct', style='four', fill=pe, gated=True)
            elif name == 'finale':
                synth_bar(S, bar + k, ch, name, arp_gain=0.05, pad=True, bass='pulse', style='half', fill=(k == 7))
                if k % 2 == 0:
                    S.bell(ARPS[ch][3] + 12, t, gain=0.05)
            else:
                synth_bar(S, bar + k, ch, name, pad=True, bass='long', style='four' if k < 3 else None)
        bar += len(chords)
    tE = S.T(bar)
    S.kick(tE); S.crash(tE, 0.15); S.bass(48, tE, 1.4); S.lead2(n('C5'), tE, 1.8)
    for m in (60, 63, 67, 72):
        S.lead2(m, tE, 1.8, gain=0.07, duty=0.5, rec=False, echo=False)
    S.mark('final', tE)
    return S.finish2('ch_mainframe', tE)


# ======================= title theme and pause loop (seamless loops) =======================
def loop_song(name, bpm, chords, melody, bars, seed, soft=False):
    S = Song2(bpm, bars * 2 + 1, seed=seed)
    for rep in range(2):
        for k, ch in enumerate(chords):
            b = rep * bars + k
            synth_bar(S, b, ch, 'loop', arp_gain=0.05 if soft else 0.06, pad=True, bass='long', style=('half' if soft else 'pop') if rep or not soft else 'half')
        play(S, rep * bars, melody, gain=0.15 if soft else 0.17, rec=False, rev=0.5)
    S.finish2(name + '_raw', S.T(bars * 2) + 0.01)
    from scipy.io import wavfile
    sr, x = wavfile.read(f'{name}_raw.wav')
    L = int(round(S.T(bars) * sr))
    wavfile.write(f'{name}.wav', sr, x[L:2 * L])
    return L / sr


def title():
    m = mel([(0, 6, 'E5'), (6, 2, 'D5'), (8, 8, 'C5')], [(0, 6, 'A5'), (6, 2, 'G5'), (8, 8, 'E5')],
            [(0, 4, 'F5'), (4, 4, 'A5'), (8, 8, 'C6')], [(0, 14, 'B5')],
            [(0, 6, 'E5'), (6, 2, 'D5'), (8, 8, 'C5')], [(0, 6, 'A5'), (6, 2, 'G5'), (8, 8, 'E5')],
            [(0, 4, 'F5'), (4, 4, 'E5'), (8, 8, 'D5')], [(0, 14, 'C5')])
    return loop_song('ch_title', 108, ['C', 'Am', 'F', 'G', 'C', 'Am', 'F', 'G'], m, 8, 41)


def pause_theme():
    m = mel([(0, 8, 'E5'), (8, 8, 'C5')], [(0, 8, 'D5'), (8, 8, 'A4')], [(0, 8, 'C5'), (8, 8, 'E5')], [(0, 14, 'D5')])
    return loop_song('ch_pause', 92, ['Am', 'F', 'C', 'G'], m, 4, 42, soft=True)


if __name__ == '__main__':
    for nm in sys.argv[1:]:
        fn = {'chrome': chrome, 'arcade': arcade, 'laser': laser, 'mainframe': mainframe, 'title': title, 'pause': pause_theme}[nm]
        print(nm, round(fn(), 1), 's', flush=True)
