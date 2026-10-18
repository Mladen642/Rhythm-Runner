import sys
from songlib import *
from songs2 import play, drums, shift
from songs3 import synth_bar, loop_song
from songs4 import M, rock_bar, metal_bar, root, RT
from songs5 import goth_bar, rap_bar, TRI, sub808, scratch

TRI.setdefault('C#m', [61, 64, 68])


def power_bar(S, bar, ch, style, fill=False):
    t, r, tr = S.T(bar), root(ch), TRI[ch]
    st = S.STEP
    if style in ('intro', 'outro'):
        S.pad(tr, t, S.BAR * 0.98, gain=0.034, rate=3.0)
        S.power(r + 12, t, 8 * st, gain=0.11); S.power(r + 12, t + 8 * st, 8 * st, gain=0.1)
        S.bass(r, t, 8 * st); S.bass(r, t + 8 * st, 8 * st)
        if style == 'intro' and bar == 0:
            return
        drums(S, bar, 'eighths', fill=fill)
    elif style == 'verse':
        for b_ in range(4):
            tb = t + b_ * 4 * st
            for s, ln in ((0, 2), (2, 1), (3, 1)):
                S.power(r + 12, tb + s * st, ln * st, mute=not (b_ == 0 and s == 0), gain=0.1)
                S.bass(r, tb + s * st, ln * st, gain=0.25)
        drums(S, bar, 'eighths', fill=fill)
    elif style == 'pre':
        S.pad(tr, t, S.BAR * 0.98, gain=0.03, rate=3.0)
        for s in range(0, 16, 2):
            S.power(r + 12, t + s * st, 2 * st, gain=0.1); S.bass(r, t + s * st, 2 * st)
        drums(S, bar, 'rock', fill=fill)
    elif style == 'chorus':
        S.pad(tr, t, S.BAR * 0.98, gain=0.036, rate=3.0)
        for s in (0, 4, 8, 12):
            S.power(r + 12, t + s * st, 4 * st, gain=0.105)
        for s in range(0, 16, 2):
            S.bass(r + (12 if s % 4 == 2 else 0), t + s * st, 2 * st)
        drums(S, bar, 'blast', fill=fill); S.crash(t, 0.08, rec=False)
    elif style == 'break':
        for s in (0, 3, 6, 10):
            S.power(r + 12, t + s * st, 2 * st, mute=(s != 0), gain=0.11); S.bass(r, t + s * st, 2 * st)
        drums(S, bar, 'half', fill=fill)


def song6(name, bpm, secs, harm_key, seed):
    nbars = sum(len(c) for _, c, _, _, _ in secs) + 1
    S = Song2(bpm, nbars, seed=seed)
    bar = 0
    for name_, chords, mel, style, o in secs:
        S.mark(name_, S.T(bar))
        if name_.startswith('chorus'):
            S.mark('chorus_any', S.T(bar)); S.crash(S.T(bar))
        if name_ in ('breakdown', 'helper', 'solo'):
            S.crash(S.T(bar))
        if mel:
            play(S, bar, mel, gain=o.get('gain', 0.18), harm_key=harm_key if o.get('harm', True) else None, harm_oct=o.get('oct', False))
        for k, ch in enumerate(chords):
            fill = (k % 4 == 3) and o.get('fills', True)
            power_bar(S, bar + k, ch, style, fill)
            if o.get('solo'):
                sc, t = o['solo'], S.T(bar + k)
                for i in range(8):
                    idx = (k * 2 + [0, 2, 4, 2, 5, 4, 6, 5][i]) % len(sc)
                    S.lead2(sc[idx], t + i * 2 * S.STEP, 2 * S.STEP, gain=0.16)
                    S.lead2(third_below(sc[idx], harm_key), t + i * 2 * S.STEP, 2 * S.STEP, gain=0.08, duty=0.5, rec=False, echo=False, pan=0.3)
        bar += len(chords)
    tE = S.T(bar)
    last = secs[-1][1][-1]
    S.kick(tE); S.crash(tE, 0.14); S.power(root(last) + 12, tE, 1.6, gain=0.13); S.pad(TRI[last], tE, 1.8, gain=0.05, rate=3.0)
    S.bass(root(last), tE, 1.2); S.lead2(root(last) + 24 + (12 if root(last) < 44 else 0), tE, 1.6)
    S.mark('final', tE)
    return S.finish2(name, tE)


HM_A = [n(x) for x in ('A5', 'B5', 'C6', 'D6', 'E6', 'F6', 'G#6', 'A6')]
HM_E = [n(x) for x in ('E5', 'F#5', 'G5', 'A5', 'B5', 'C6', 'D#6', 'E6')]


def valor():
    V = ['Am', 'F', 'G', 'E', 'Am', 'F', 'G', 'Am']
    P_ = ['Dm', 'F', 'G', 'G']
    C_ = ['F', 'G', 'Am', 'Am', 'F', 'G', 'E', 'E']
    vm = M('A4:4 C5:4 E5:4 D5:4', 'C5:4 A4:4 F4:8', 'G4:4 B4:4 D5:4 B4:4', 'G#4:8 B4:8', 'E5:4 D5:4 C5:4 A4:4', 'A4:4 C5:4 F5:8', 'D5:4 E5:4 G5:4 B4:4', 'A4:14')
    pm = M('D5:8 F5:8', 'F5:8 A5:8', 'G5:8 B5:8', 'D6:14')
    cm = M('C5:4 F5:4 A5:8', 'B5:4 G5:4 D5:8', 'C5:4 E5:4 A5:4 C6:4', 'A5:12 E5:4', 'C5:4 F5:4 A5:8', 'D6:4 B5:4 G5:8', 'G#5:4 B5:4 E6:4 D6:4', 'B5:14')
    om = M('A5:16', 'F5:16', 'E5:8 G#5:8', 'A5:14')
    return song6('c6_valor', 168, [('intro', ['Am', 'F', 'G', 'E'], cm[:4], 'intro', {}), ('verse', V, vm, 'verse', {'harm': False}), ('pre', P_, pm, 'pre', {}),
                                   ('chorus', C_, cm, 'chorus', {}), ('verse', V, vm, 'verse', {'harm': False}), ('pre', P_, pm, 'pre', {}),
                                   ('solo', ['Am', 'F', 'G', 'E'] * 2, None, 'verse', {'solo': HM_A}), ('chorus', C_, cm, 'chorus', {'oct': True}), ('outro', ['F', 'G', 'E', 'Am'], om, 'outro', {'fills': False})],
                 'Am', 101)


def labyrinth():
    V = ['Dm', 'Bb', 'C', 'A'] * 2
    C_ = ['Bb', 'C', 'Dm', 'Dm', 'Bb', 'C', 'A', 'A']
    vm = M('D5:4 F5:4 A5:4 G5:4', 'F5:4 D5:4 Bb4:8', 'C5:4 E5:4 G5:4 E5:4', 'C#5:8 E5:8', 'D5:4 F5:4 A5:4 D6:4', 'C6:4 Bb5:4 F5:8', 'E5:4 G5:4 C6:4 G5:4', 'A5:14')
    cm = M('D5:4 F5:4 Bb5:8', 'C6:4 A5:4 G5:8', 'F5:4 A5:4 D6:4 C6:4', 'D6:12 A5:4', 'D5:4 F5:4 Bb5:8', 'C6:4 E6:4 G6:8', 'E6:4 C#6:4 A5:4 E5:4', 'A5:14')
    om = M('F5:16', 'D5:16', 'C#5:8 E5:8', 'D5:14')
    return song6('c6_labyrinth', 160, [('intro', ['Dm', 'Bb', 'A', 'A'], None, 'intro', {}), ('verse', V, vm, 'verse', {'harm': False}), ('chorus', C_, shift(cm, -12), 'chorus', {}),
                                       ('breakdown', ['Dm', 'Dm', 'Bb', 'Bb', 'C', 'C', 'A', 'A'], None, 'break', {}), ('verse', V, vm, 'verse', {'harm': False}),
                                       ('chorus', C_, shift(cm, -12), 'chorus', {'oct': True}), ('outro', ['Dm', 'Bb', 'A', 'Dm'], om, 'outro', {'fills': False})],
                 'Dm', 102)


def thunder():
    V = ['Em', 'C', 'D', 'B', 'Em', 'C', 'D', 'Em']
    P_ = ['Am', 'C', 'D', 'D']
    C_ = ['G', 'D', 'Em', 'C', 'G', 'D', 'C', 'B']
    vm = M('E5:4 G5:4 B5:4 A5:4', 'G5:4 E5:4 C5:8', 'D5:4 F#5:4 A5:4 F#5:4', 'D#5:8 F#5:8', 'B5:4 A5:4 G5:4 E5:4', 'E5:4 G5:4 C6:8', 'B5:4 A5:4 F#5:4 D5:4', 'E5:14')
    pm = M('C5:8 E5:8', 'E5:8 G5:8', 'F#5:8 A5:8', 'D6:14')
    cm = M('D5:4 G5:4 B5:8', 'A5:4 F#5:4 D6:8', 'B5:4 G5:4 E5:4 G5:4', 'E5:12 G5:4', 'D5:4 G5:4 B5:8', 'A5:4 D6:4 F#5:8', 'G5:4 E5:4 C5:4 E5:4', 'D#5:14')
    om = M('G5:16', 'F#5:16', 'E5:16', 'B4:14')
    return song6('c6_thunder', 172, [('intro', ['Em', 'C', 'D', 'Em'], None, 'intro', {}), ('verse', V, vm, 'verse', {'harm': False}), ('pre', P_, pm, 'pre', {}),
                                     ('chorus', C_, cm, 'chorus', {}), ('verse', V, vm, 'verse', {'harm': False}), ('chorus', C_, cm, 'chorus', {}),
                                     ('chorus_last', C_, shift(cm, 0), 'chorus', {'oct': True}), ('outro', ['G', 'D', 'Em', 'Em'], om, 'outro', {'fills': False})],
                 'Em', 103)


TITAN_HELP_CH = ['Em', 'C', 'D', 'B', 'Em', 'C', 'D', 'B']
TITAN_HM = M('E5:2 G5:2 B5:4 A5:2 G5:2 E5:4', 'C5:2 E5:2 G5:4 F#5:2 E5:2 C5:4', 'D5:2 F#5:2 A5:4 G5:2 F#5:2 D5:4', 'B4:8 D#5:8',
             'E5:2 G5:2 B5:4 E6:4 D6:4', 'C6:4 B5:4 G5:8', 'A5:4 F#5:4 D5:4 F#5:4', 'B5:14')


def storm_song():
    V = ['Em', 'C', 'D', 'B'] * 2
    C_ = ['C', 'D', 'Em', 'Em', 'C', 'D', 'B', 'B']
    vm = M('E5:4 B4:4 E5:4 G5:4', 'F#5:8 E5:8', 'G5:4 E5:4 C5:8', 'D5:8 F#5:8', 'E5:4 B4:4 E5:4 G5:4', 'B5:8 A5:8', 'G5:4 E5:4 C5:8', 'D#5:14')
    cm = M('E5:4 G5:4 C6:8', 'D6:4 B5:4 A5:8', 'G5:4 B5:4 E6:4 D6:4', 'B5:12 E5:4', 'E5:4 G5:4 C6:8', 'D6:4 F#6:4 A6:8', 'F#6:4 D#6:4 B5:4 D#6:4', 'B5:14')
    om = M('G5:16', 'E5:16', 'F#5:8 D#5:8', 'E5:14')
    return song6('c6_storm', 176, [('intro', ['Em'] * 4, None, 'intro', {}), ('verse', V, vm, 'verse', {'harm': False}), ('chorus', C_, shift(cm, -12), 'chorus', {}),
                                   ('verse', V, vm, 'verse', {'harm': False}), ('helper', TITAN_HELP_CH, TITAN_HM, 'chorus', {'harm': False}),
                                   ('chorus_cor', C_, shift(cm, -12), 'chorus', {'oct': True}), ('finale', ['Em', 'Em', 'C', 'C', 'D', 'D', 'B', 'B'], None, 'break', {}),
                                   ('outro', ['Em', 'C', 'B', 'Em'], om, 'outro', {'fills': False})],
                 'Em', 104)


def pause_power():
    m = M('B4:8 E5:8', 'G5:8 F#5:8', 'E5:8 B4:8', 'D#5:14')
    return loop_song('c6_pause', 76, ['Em', 'C', 'Em', 'B'], m, 4, 105, soft=True)


# ---------- helper clips: the same melody arranged in each helper's genre ----------
from songs4 import M as _M
TITAN2_CH = ['C', 'D', 'Em', 'Bm', 'C', 'D', 'Em', 'B']
TITAN2_HM = _M('E5:2 G5:2 C6:4 B5:2 G5:2 E5:4', 'F#5:2 A5:2 D6:4 C#6:2 A5:2 F#5:4', 'G5:2 B5:2 E6:4 D6:2 B5:2 G5:4', 'F#5:8 D#5:8',
               'E5:2 G5:2 C6:4 B5:2 C6:2 E6:4', 'D6:2 C6:2 A5:4 F#5:2 A5:2 D6:4', 'B5:2 G5:2 E5:4 G5:2 B5:2 E6:4', 'D#6:14')
COUNTESS_CH = ['Em', 'C', 'D', 'B', 'Em', 'C', 'D', 'B']
COUNTESS_HM = _M('E5:2 G5:2 B5:4 A5:2 G5:2 E5:4', 'C5:2 E5:2 G5:4 F#5:2 E5:2 C5:4', 'D5:2 F#5:2 A5:4 G5:2 F#5:2 D5:4', 'B4:8 D#5:8',
                 'E5:2 G5:2 B5:4 E6:4 D6:4', 'C6:4 B5:4 G5:8', 'A5:4 F#5:4 D5:4 F#5:4', 'B5:14')
BOSSES = {'c2_titan': (152, TITAN2_CH, TITAN2_HM), 'c4_countess': (124, COUNTESS_CH, COUNTESS_HM), 'c6_storm': (176, TITAN_HELP_CH, TITAN_HM)}
GENRES = ['synth', 'rock', 'metal', 'goth', 'rap', 'power']


def clip(boss, genre):
    bpm, chords, mel = BOSSES[boss]
    S = Song2(bpm, 9, seed=7)
    lead = {'synth': dict(duty=0.125, gain=0.18), 'rock': dict(duty=0.25, gain=0.19), 'metal': dict(duty=0.25, gain=0.18), 'goth': dict(duty=0.25, gain=0.2, vib=0.008, rev=0.55),
            'rap': dict(duty=0.5, gain=0.17), 'power': dict(duty=0.25, gain=0.18)}[genre]
    play(S, 0, mel, harm_key='Em' if genre in ('power', 'metal') else None, **lead)
    for k, ch in enumerate(chords):
        fill = k % 4 == 3
        if genre == 'synth':
            synth_bar(S, k, ch, 'helper', pattern=[0, 2, 1, 3] * 4, pad=True, style='four', fill=fill, gated=True)
        elif genre == 'rock':
            rock_bar(S, k, ch, 'chorus', fill); S.hey(S.T(k, 12)) if k % 2 else None
        elif genre == 'metal':
            metal_bar(S, k, ch, 'gallop', fill)
        elif genre == 'goth':
            goth_bar(S, k, ch, 'chorus', fill)
        elif genre == 'rap':
            rap_bar(S, k, ch, 'hook' if k % 4 else 'verse', fill)
        else:
            power_bar(S, k, ch, 'chorus', fill)
    S.crash(0)
    return S.finish2(f'hc_{boss}_{genre}', S.T(8) - 0.01, rev_wet=0.3 if genre == 'goth' else 0.22, cho=(genre == 'goth'))


if __name__ == '__main__':
    F = {'valor': valor, 'labyrinth': labyrinth, 'thunder': thunder, 'storm': storm_song, 'ppower': pause_power}
    for nm in sys.argv[1:]:
        if nm.startswith('clip:'):
            _, boss, genre = nm.split(':')
            print(nm, round(clip(boss, genre), 1), flush=True)
        else:
            print(nm, round(F[nm](), 1), 's', flush=True)
