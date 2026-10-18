import sys
from songlib import *
from songs2 import play, drums, shift
from songs3 import synth_bar, loop_song, ARPS, ROOTS

RT = {'E': 40, 'F': 41, 'F#': 42, 'G': 43, 'G#': 44, 'A': 45, 'Bb': 46, 'A#': 46, 'B': 47, 'C': 36, 'C#': 37, 'D': 38, 'Eb': 39, 'Ab': 44}


def root(ch):
    return RT[ch.rstrip('m')] if ch.rstrip('m') in RT else RT[ch[:2]]


def M(*bars):
    out = []
    for b in bars:
        pos, notes = 0, []
        for tok in b.split():
            nm, ln = tok.split(':')
            ln = int(ln)
            if nm != '-':
                notes.append((pos, ln, n(nm)))
            pos += ln
        out.append(notes)
    return out


def rock_bar(S, bar, ch, style, fill=False):
    t, r = S.T(bar), root(ch)
    st = S.STEP
    if style == 'riff':
        for s in range(0, 16, 2):
            acc = s in (0, 6, 12)
            S.power(r + 12, t + s * st, 2 * st, mute=not acc, gain=0.11)
        drums(S, bar, 'rock', fill=fill)
    elif style == 'drive':
        for s in range(0, 16, 2):
            S.power(r + 12, t + s * st, 2 * st, mute=(s % 4 != 0), gain=0.1)
        drums(S, bar, 'rock', fill=fill)
    elif style == 'chorus':
        for s in (0, 4, 8, 12):
            S.power(r + 12, t + s * st, 4 * st, gain=0.11)
        drums(S, bar, 'rockch', fill=fill)
    elif style == 'half':
        for s in (0, 3, 6, 10):
            S.power(r + 12, t + s * st, 2 * st, mute=(s != 0), gain=0.11)
        drums(S, bar, 'half', fill=fill)
    elif style == 'broken':
        S.bass(r, t, 8 * st, gain=0.26); S.bass(r, t + 8 * st, 8 * st, gain=0.26)
        drums(S, bar, 'half', fill=fill)
        for s in (2, 9, 13):
            S.lead2(r + 36 + (s % 3), t + s * st, st, gain=0.05, duty=0.5, rec=False, echo=False)
        return
    for s in range(0, 16, 2):
        S.bass(r + (12 if style == 'chorus' and s % 4 == 2 else 0), t + s * st, 2 * st)


def metal_bar(S, bar, ch, style, fill=False):
    t, r = S.T(bar), root(ch)
    st = S.STEP
    if style == 'gallop':
        for b_ in range(4):
            tb = t + b_ * 4 * st
            for s, ln in ((0, 2), (2, 1), (3, 1)):
                S.power(r + 12, tb + s * st, ln * st, mute=not (b_ == 0 and s == 0), gain=0.1)
                S.bass(r, tb + s * st, ln * st, gain=0.26)
        drums(S, bar, 'gallop', fill=fill)
    elif style == 'blast':
        for s in (0, 4, 8, 12):
            S.power(r + 12, t + s * st, 3 * st, gain=0.105)
        for s in range(0, 16, 2):
            S.bass(r, t + s * st, 2 * st)
        drums(S, bar, 'blast', fill=fill); S.crash(t, 0.08, rec=False)
    elif style == 'chug':
        for s in range(16):
            S.power(r + 12, t + s * st, st, mute=True, gain=0.095)
        for s in range(0, 16, 2):
            S.bass(r, t + s * st, 2 * st)
        drums(S, bar, 'eighths', fill=fill)
    elif style == 'break':
        for s in (0, 3, 6, 10):
            S.power(r + 12, t + s * st, 2 * st, mute=(s != 0), gain=0.11); S.bass(r, t + s * st, 2 * st)
        drums(S, bar, 'half', fill=fill)
    elif style == 'eighth':
        for s in range(0, 16, 2):
            S.power(r + 12, t + s * st, 2 * st, mute=(s % 8 != 0), gain=0.1); S.bass(r, t + s * st, 2 * st)
        drums(S, bar, 'eighths', fill=fill)


def song(name, bpm, secs, kind, harm_key, seed, extra_end=None):
    """secs: list of (section_name, chords, melody_or_None, style, opts)"""
    nbars = sum(len(c) for _, c, _, _, _ in secs) + 1
    S = Song2(bpm, nbars, seed=seed)
    bar = 0
    nch = 0
    for name_, chords, mel, style, o in secs:
        S.mark(name_, S.T(bar))
        if name_.startswith('chorus'):
            nch += 1; S.mark('chorus_any', S.T(bar))
        if name_ in ('chorus', 'solo', 'breakdown') or name_.startswith('chorus'):
            S.crash(S.T(bar))
        if mel:
            play(S, bar, mel, gain=o.get('gain', 0.18), duty=o.get('duty', 0.25), harm_key=harm_key if o.get('harm') else None,
                 harm_oct=o.get('oct', False), vib=o.get('vib', 0.004))
        for k, ch in enumerate(chords):
            fill = (k % 4 == 3) and o.get('fills', True)
            if style == 'synth':
                synth_bar(S, bar + k, ch, 'helper', pattern=[0, 2, 1, 3] * 4, pad=True, style='four', fill=fill, gated=True)
            elif kind == 'rock':
                rock_bar(S, bar + k, ch, style, fill)
            else:
                metal_bar(S, bar + k, ch, style, fill)
            if o.get('hey') and k % 2 == 1:
                S.hey(S.T(bar + k, 4)); S.hey(S.T(bar + k, 12))
            if o.get('solo'):
                sc = o['solo']
                t = S.T(bar + k)
                for i in range(8):
                    idx = (k * 3 + [0, 2, 4, 3, 5, 4, 2, 1][i]) % len(sc)
                    S.lead2(sc[idx], t + i * 2 * S.STEP, 2 * S.STEP, gain=0.16)
                    if o.get('twin'):
                        S.lead2(third_below(sc[idx], harm_key), t + i * 2 * S.STEP, 2 * S.STEP, gain=0.08, duty=0.5, rec=False, echo=False, pan=0.3)
        bar += len(chords)
    tE = S.T(bar)
    last = secs[-1][1][-1]
    S.kick(tE); S.crash(tE, 0.14); S.power(root(last) + 12, tE, 1.6, gain=0.13); S.bass(root(last), tE, 1.2)
    if kind == 'rock':
        S.hey(tE)
    S.lead2(root(last) + 24 + (12 if root(last) < 44 else 0), tE, 1.6)
    S.mark('final', tE)
    return S.finish2(name, tE)


PENT_E = [n(x) for x in ('E5', 'G5', 'A5', 'B5', 'D6', 'E6', 'G6', 'A5')]
PENT_A = [n(x) for x in ('A4', 'C5', 'D5', 'E5', 'G5', 'A5', 'C6', 'D6')]
HM_D = [n(x) for x in ('D5', 'E5', 'F5', 'G5', 'A5', 'Bb5', 'C#6', 'D6')]
HM_E = [n(x) for x in ('E5', 'F#5', 'G5', 'A5', 'B5', 'C6', 'D#6', 'E6')]


def desert():
    V = ['Em', 'Em', 'C', 'D', 'Em', 'Em', 'C', 'B']
    C_ = ['C', 'G', 'D', 'Em', 'C', 'G', 'B', 'B']
    vm = M('E5:4 G5:2 E5:2 B4:8', 'E5:4 G5:2 A5:2 B5:8', 'C6:4 B5:2 A5:2 G5:4 E5:4', 'F#5:12 D5:4',
           'E5:4 G5:2 E5:2 B4:8', 'E5:4 G5:2 A5:2 B5:8', 'C6:4 B5:2 A5:2 G5:4 A5:4', 'B5:14')
    cm = M('E5:4 G5:4 C6:8', 'D6:4 B5:4 G5:8', 'A5:4 F#5:4 D5:4 F#5:4', 'E5:12 G5:4',
           'E5:4 G5:4 C6:8', 'D6:4 E6:4 D6:8', 'D#6:4 B5:4 F#5:4 A5:4', 'B5:14')
    om = M('G5:16', 'E5:16', 'F#5:8 A5:8', 'E5:14')
    return song('c2_desert', 140, [('intro', ['Em', 'Em', 'C', 'D'], None, 'riff', {}), ('verse', V, vm, 'riff', {}),
                                   ('chorus', C_, cm, 'chorus', {'hey': True}), ('verse', V, vm, 'drive', {}), ('chorus', C_, cm, 'chorus', {'hey': True, 'harm': True}),
                                   ('solo', ['Em', 'C', 'D', 'B'] * 2, None, 'drive', {'solo': PENT_E}), ('outro', ['Em', 'C', 'B', 'Em'], om, 'chorus', {'fills': False})],
                'rock', 'Em', 51)


def motel():
    V = ['Am', 'F', 'C', 'G'] * 2
    C_ = ['F', 'G', 'Am', 'Am', 'F', 'G', 'E', 'E']
    vm = M('A4:2 C5:2 E5:4 D5:2 C5:2 A4:4', 'F5:4 E5:2 C5:2 A4:8', 'G5:2 E5:2 C5:4 E5:2 G5:2 C6:4', 'B5:8 G5:8',
           'A4:2 C5:2 E5:4 D5:2 C5:2 A4:4', 'F5:4 A5:2 F5:2 C5:8', 'D5:2 E5:2 G5:4 B5:4 D6:4', 'B5:14')
    cm = M('C6:4 A5:4 F5:8', 'D6:4 B5:4 G5:8', 'E6:4 C6:4 A5:4 C6:4', 'E6:12 A5:4',
           'C6:4 A5:4 F5:8', 'D6:4 E6:4 D6:8', 'B5:4 G#5:4 E5:4 G#5:4', 'A5:14')
    om = M('E5:16', 'C5:16', 'D5:8 B4:8', 'A4:14')
    return song('c2_motel', 144, [('intro', ['Am', 'F', 'E', 'E'], None, 'riff', {}), ('verse', V, vm, 'riff', {}), ('chorus', C_, shift(cm, -12), 'chorus', {'hey': True}),
                                  ('verse', V, vm, 'drive', {}), ('breakdown', ['Am', 'Am', 'F', 'F', 'C', 'C', 'E', 'E'], None, 'half', {'hey': True}),
                                  ('chorus', C_, shift(cm, -12), 'chorus', {'harm': True}), ('outro', ['Am', 'F', 'E', 'Am'], om, 'chorus', {'fills': False})],
                'rock', 'Am', 52)


def storm():
    SCALES['Bm'] = [11, 1, 2, 4, 6, 7, 9]
    V = ['Bm', 'G', 'D', 'A'] * 2
    P = ['G', 'A', 'F#', 'F#']
    C_ = ['G', 'D', 'A', 'Bm', 'G', 'D', 'F#', 'F#']
    vm = M('B4:4 D5:2 F#5:2 E5:4 D5:4', 'D5:4 G5:4 F#5:4 E5:4', 'F#5:4 A5:2 F#5:2 D5:8', 'E5:4 C#5:4 A4:8',
           'B4:4 D5:2 F#5:2 B5:4 A5:4', 'G5:4 F#5:4 E5:4 D5:4', 'F#5:4 A5:4 D6:4 C#6:4', 'C#6:14')
    pm = M('B5:8 A5:8', 'C#6:8 B5:8', 'A#5:8 C#6:8', 'F#5:14')
    cm = M('B5:4 D6:4 G5:8', 'F#5:4 A5:4 D6:8', 'E6:4 C#6:4 A5:8', 'B5:12 F#5:4',
           'B5:4 D6:4 G5:8', 'F#5:4 A5:4 D6:8', 'C#6:4 A#5:4 F#5:4 C#6:4', 'F#5:14')
    om = M('D5:16', 'B4:16', 'C#5:8 A#4:8', 'B4:14')
    return song('c2_storm', 150, [('intro', ['Bm', 'G', 'D', 'A'], None, 'riff', {}), ('verse', V, vm, 'riff', {}), ('pre', P, pm, 'drive', {}),
                                  ('chorus', C_, cm, 'chorus', {'hey': True}), ('verse', V, vm, 'drive', {}), ('pre', P, pm, 'drive', {}),
                                  ('chorus', C_, cm, 'chorus', {'harm': True}), ('chorus_last', C_, cm, 'chorus', {'hey': True, 'oct': True}),
                                  ('outro', ['G', 'D', 'F#', 'Bm'], om, 'chorus', {'fills': False})],
                'rock', 'Bm', 53)


def titan():
    V = ['Em', 'G', 'D', 'A'] * 2
    C_ = ['C', 'D', 'Em', 'Em', 'C', 'D', 'B', 'B']
    vm = M('E5:2 E5:2 G5:4 A5:4 B5:4', 'D5:4 G5:4 B5:8', 'A5:4 F#5:4 D5:8', 'C#5:4 E5:4 A5:8',
           'E5:2 E5:2 G5:4 A5:4 B5:4', 'D6:4 B5:4 G5:8', 'F#5:4 A5:4 D6:4 C#6:4', 'C#6:14')
    cm = M('E5:4 G5:4 C6:8', 'F#5:4 A5:4 D6:8', 'E6:4 D6:4 B5:4 G5:4', 'E5:12 B5:4',
           'E5:4 G5:4 C6:8', 'F#5:4 A5:4 D6:8', 'D#6:4 B5:4 F#5:4 D#5:4', 'B5:14')
    hm = M('E5:2 G5:2 C6:4 B5:2 G5:2 E5:4', 'F#5:2 A5:2 D6:4 C#6:2 A5:2 F#5:4', 'G5:2 B5:2 E6:4 D6:2 B5:2 G5:4', 'F#5:8 D#5:8',
           'E5:2 G5:2 C6:4 B5:2 C6:2 E6:4', 'D6:2 C6:2 A5:4 F#5:2 A5:2 D6:4', 'B5:2 G5:2 E5:4 G5:2 B5:2 E6:4', 'D#6:14')
    om = M('G5:16', 'E5:16', 'F#5:8 D#5:8', 'E5:14')
    return song('c2_titan', 152, [('intro', ['Em'] * 4, None, 'riff', {}), ('verse', V, vm, 'riff', {}), ('chorus', C_, cm, 'chorus', {'hey': True}),
                                  ('broken', ['Em'] * 4, None, 'broken', {'fills': False}),
                                  ('helper', ['C', 'D', 'Em', 'Bm', 'C', 'D', 'Em', 'B'], hm, 'synth', {'duty': 0.125}),
                                  ('chorus_back', C_, cm, 'chorus', {'hey': True, 'harm': True}),
                                  ('finale', ['Em', 'Em', 'C', 'C', 'D', 'D', 'B', 'B'], None, 'half', {}), ('outro', ['Em', 'C', 'B', 'Em'], om, 'chorus', {'fills': False})],
                'rock', 'Em', 54)


def iron():
    V = ['Dm', 'Dm', 'Bb', 'C', 'Dm', 'Dm', 'Bb', 'A']
    C_ = ['Bb', 'C', 'Dm', 'Dm', 'Bb', 'C', 'A', 'A']
    cm = M('D5:4 F5:4 Bb5:8', 'C6:4 A5:4 G5:8', 'F5:4 E5:4 D5:4 A4:4', 'D5:14', 'D5:4 F5:4 Bb5:8', 'C6:4 D6:4 E6:8', 'C#6:4 A5:4 E5:4 C#5:4', 'A5:14')
    vm2 = M('D5:8 E5:4 F5:4', 'D5:16', 'F5:8 G5:4 A5:4', 'G5:8 E5:8', 'D5:8 E5:4 F5:4', 'A5:16', 'Bb5:8 A5:4 G5:4', 'E5:14')
    om = M('F5:16', 'D5:16', 'C#5:8 E5:8', 'D5:14')
    return song('c3_iron', 160, [('intro', ['Dm', 'Dm', 'Bb', 'A'], None, 'gallop', {}), ('verse', V, None, 'gallop', {}), ('chorus', C_, cm, 'blast', {}),
                                 ('verse', V, vm2, 'gallop', {}), ('chorus', C_, cm, 'blast', {'harm': True}), ('solo', ['Dm', 'Bb', 'C', 'A'] * 2, None, 'gallop', {'solo': HM_D, 'twin': True}),
                                 ('chorus', C_, cm, 'blast', {'oct': True}), ('outro', ['Dm', 'Bb', 'A', 'Dm'], om, 'break', {'fills': False})],
                'metal', 'Dm', 61)


def troll_song():
    V = ['Cm', 'Cm', 'Ab', 'Bb', 'Cm', 'Cm', 'Ab', 'G']
    C_ = ['Ab', 'Bb', 'Cm', 'Cm', 'Ab', 'Bb', 'G', 'G']
    vm = M('C5:8 D5:4 Eb5:4', 'C5:16', 'Eb5:8 F5:4 G5:4', 'Eb5:8 D5:8', 'C5:8 D5:4 Eb5:4', 'G5:16', 'Ab5:8 G5:4 F5:4', 'D5:14')
    cm = M('C5:4 Eb5:4 Ab5:8', 'Bb5:4 G5:4 F5:8', 'Eb5:4 D5:4 C5:4 G4:4', 'C5:14', 'C5:4 Eb5:4 Ab5:8', 'Bb5:4 C6:4 D6:8', 'B5:4 G5:4 D5:4 B4:4', 'G5:14')
    om = M('Eb5:16', 'C5:16', 'D5:8 B4:8', 'C5:14')
    SCALES['Cm'] = [0, 2, 3, 5, 7, 8, 10]
    return song('c3_troll', 150, [('intro', ['Cm'] * 4, None, 'gallop', {}), ('verse', V, vm, 'gallop', {}), ('chorus', C_, cm, 'blast', {}),
                                  ('breakdown', ['Cm', 'Cm', 'Ab', 'Ab', 'Bb', 'Bb', 'G', 'G'], None, 'break', {}), ('verse', V, vm, 'chug', {}),
                                  ('chorus', C_, cm, 'blast', {'harm': True}), ('outro', ['Cm', 'Ab', 'G', 'Cm'], om, 'break', {'fills': False})],
                'metal', 'Cm', 62)


def ash():
    V = ['Em', 'Em', 'C', 'D', 'Em', 'Em', 'C', 'B']
    P = ['Am', 'C', 'D', 'B']
    C_ = ['Em', 'C', 'D', 'Em', 'Em', 'C', 'B', 'B']
    pm = M('B4:8 C5:8', 'D5:8 E5:8', 'F#5:8 G5:8', 'B5:14')
    cm = M('E5:4 G5:4 B5:8', 'C6:4 B5:4 A5:8', 'D6:4 C6:4 B5:4 A5:4', 'B5:12 G5:4', 'E5:4 G5:4 B5:8', 'C6:4 D6:4 E6:8', 'D#6:4 B5:4 F#5:4 A5:4', 'B5:14')
    vm2 = M('E5:4 B4:4 E5:4 G5:4', 'F#5:8 E5:8', 'G5:4 E5:4 C5:8', 'D5:8 F#5:8', 'E5:4 B4:4 E5:4 G5:4', 'B5:8 A5:8', 'G5:4 E5:4 C5:8', 'D#5:14')
    om = M('G5:16', 'E5:16', 'F#5:8 D#5:8', 'E5:14')
    return song('c3_ash', 168, [('intro', ['Em', 'C', 'D', 'B'], None, 'blast', {}), ('verse', V, None, 'gallop', {}), ('pre', P, pm, 'chug', {}),
                                ('chorus', C_, cm, 'blast', {}), ('verse', V, vm2, 'gallop', {}), ('pre', P, pm, 'chug', {}),
                                ('chorus', C_, cm, 'blast', {'harm': True}), ('chorus_last', C_, cm, 'blast', {'oct': True}),
                                ('outro', ['Em', 'C', 'B', 'Em'], om, 'break', {'fills': False})],
                'metal', 'Em', 63)


def drake_song():
    V = ['Dm', 'Bb', 'C', 'A'] * 2
    C_ = ['Dm', 'C', 'Dm', 'Dm', 'Bb', 'C', 'A', 'A']
    vm = M('D5:2 F5:2 A5:4 G5:2 F5:2 D5:4', 'Bb4:4 D5:4 F5:8', 'C5:2 E5:2 G5:4 F5:2 E5:2 C5:4', 'A4:4 C#5:4 E5:8',
           'D5:2 F5:2 A5:4 D6:4 C6:4', 'Bb5:4 A5:4 F5:8', 'G5:4 E5:4 C5:4 E5:4', 'C#5:14')
    cm = M('F5:4 A5:4 D6:8', 'C6:4 G5:4 E5:8', 'D6:4 E6:4 F6:4 E6:4', 'D6:12 A5:4', 'F5:4 A5:4 D6:8', 'C6:4 E6:4 G6:8', 'E6:4 C#6:4 A5:4 E5:4', 'A5:14')
    om = M('F5:16', 'D5:16', 'C#5:8 E5:8', 'D5:14')
    return song('c3_drake', 156, [('intro', ['Dm'] * 4, None, 'break', {}), ('verse', V, vm, 'gallop', {}), ('chorus', C_, shift(cm, -12), 'blast', {'oct': True}),
                                  ('verse_rev', V, vm, 'chug', {}), ('chorus_cor', C_, shift(cm, -12), 'blast', {'harm': True}),
                                  ('finale', ['Dm', 'Dm', 'Bb', 'Bb', 'C', 'C', 'A', 'A'], None, 'break', {}), ('outro', ['Dm', 'Bb', 'A', 'Dm'], om, 'break', {'fills': False})],
                'metal', 'Dm', 64)


def pause_rock():
    m = M('E5:8 C#5:8', 'D5:8 B4:8', 'C#5:8 E5:8', 'B4:14')
    return loop_song('c2_pause', 84, ['A', 'D', 'A', 'E'], m, 4, 71, soft=True)


def pause_metal():
    m = M('D5:8 F5:8', 'E5:8 C5:8', 'D5:8 A4:8', 'C#5:14')
    return loop_song('c3_pause', 72, ['Dm', 'Bb', 'Dm', 'A'], m, 4, 72, soft=True)


if __name__ == '__main__':
    F = {'desert': desert, 'motel': motel, 'storm': storm, 'titan': titan, 'iron': iron, 'troll': troll_song, 'ash': ash, 'drake': drake_song,
         'prock': pause_rock, 'pmetal': pause_metal}
    for nm in sys.argv[1:]:
        print(nm, round(F[nm](), 1), 's', flush=True)
