import math, random, sys
import numpy as np
from PIL import Image
from songlib import *
from songs5 import piano
from songs3 import loop_song
from anim import *
from stage_assets2 import magic, rgba, b64, L_scroll, L_static, W, frames_sheet
from new_art import rim, flash
HZ, PT, GY = 126, 180, 166

# ======================= music =======================
JZ = {'Cmaj7': [60, 64, 67, 71], 'Dm7': [62, 65, 69, 72], 'Em7': [64, 67, 71, 74], 'Fmaj7': [65, 69, 72, 76], 'G7': [67, 71, 74, 77], 'Am7': [57, 60, 64, 67],
      'A7': [57, 61, 64, 67], 'D7': [62, 66, 69, 72], 'Gm7': [55, 58, 62, 65], 'C7': [60, 64, 67, 70], 'Bb7': [58, 62, 65, 68], 'Bbmaj7': [58, 62, 65, 69],
      'Bbm7': [58, 61, 65, 68], 'Ebmaj7': [63, 67, 70, 74], 'Eb7': [63, 67, 70, 73], 'F7': [65, 69, 72, 75], 'Cm7': [60, 63, 67, 70], 'Fm7': [65, 68, 72, 75],
      'E7': [64, 68, 71, 74], 'Gmaj7': [55, 59, 62, 66], 'Bm7': [59, 62, 66, 69], 'Dm6': [62, 65, 69, 71], 'Gm6': [55, 58, 62, 64], 'Em7b5': [64, 67, 70, 74],
      'A7b9': [57, 61, 64, 70], 'Cm6': [60, 63, 67, 69]}
SW = 0.67


def jroot(ch):
    r = JZ[ch][0] % 12
    return 36 + r if r >= 4 else 48 + r


def sw(s):
    return s + SW if s % 4 == 2 else s


def swing_bar(S, bar, ch, nxt, style, fill=False):
    t, st, tones = S.T(bar), S.STEP, JZ[ch]
    r = jroot(ch); rn = jroot(nxt)
    for s in (0, 4, 6 + SW, 8, 12, 14 + SW):
        S.hat(t + s * st, gain=0.07 if s in (0, 8) else 0.05, open_=True)
    for s in (4, 12):
        S.hat(t + s * st, gain=0.045)
    for s in (0, 4, 8, 12):
        S.kick(t + s * st, gain=0.16 if style != 'shout' else 0.32)
    if style in ('shout', 'head2'):
        for s in (4, 12):
            S.snare(t + s * st, gain=0.18)
    if random.Random(bar * 7 + 1).random() < 0.5:
        S.snare(t + (6 + SW) * st, gain=0.07)
    walk = [r, r + (tones[1] - tones[0]), r + (tones[2] - tones[0]), rn + (1 if random.Random(bar).random() < 0.5 else -1)]
    for i, m in enumerate(walk):
        S.bass(m, t + i * 4 * st, 3.6 * st, gain=0.27, bright=0.25)
    if style != 'break':
        piano(S, [x - 12 if x > 66 else x for x in tones], t, 1.6 * st, gain=0.04)
        piano(S, [x - 12 if x > 66 else x for x in tones], t + (6 + SW) * st, 1.6 * st, gain=0.04)
    if style == 'shout':
        for s in (0, 10 + SW):
            for m in tones[1:]:
                S.lead2(m + 12, t + s * st, 1.8 * st, gain=0.035, duty=0.5, rec=False, echo=False, rev=0.2)
    if fill:
        for s in (12, 13, 14, 15):
            S.snare(t + s * st, gain=0.1 + (s - 12) * 0.04)


def bebop(S, bars, chords, seed, lo=64, hi=86):
    rng = random.Random(seed)
    RH = [[2, 2, 2, 2, 4, 4], [4, 2, 2, 4, 4], [2, 2, 4, 2, 2, 4], [6, 2, 4, 4], [2, 2, 2, 2, 2, 2, 4], [4, 4, 2, 2, 4]]
    out, p = [], 72
    for ch in chords:
        tones = [x % 12 for x in JZ[ch]]
        rh = rng.choice(RH); pos = 0; notes = []
        for i, ln in enumerate(rh):
            if pos % 8 == 0 or i == 0:
                cands = [m for m in range(lo, hi) if m % 12 in tones]
            else:
                cands = [m for m in range(lo, hi) if abs(m - p) <= 3 and m != p]
            p = min(cands, key=lambda m: abs(m - p) + rng.random() * 3)
            notes.append((pos, ln, p)); pos += ln
        out.append(notes)
    return out


def riff(chords, idx=(0, 1, 2, 1, 3), rh=(4, 2, 2, 4, 4), up=12):
    out = []
    for ch in chords:
        tones = JZ[ch]; pos = 0; notes = []
        for i, ln in zip(idx, rh):
            notes.append((pos, ln, tones[i] + up)); pos += ln
        out.append(notes)
    return out


def play_sw(S, bar, mel, gain=0.18, duty=0.25, rec=True):
    for k, notes in enumerate(mel):
        for a, ln, m in notes:
            a2 = sw(a)
            S.lead2(m, S.T(bar + k, a2), max(0.6, ln - (a2 - a)) * S.STEP, gain=gain, duty=duty, vib=0.008, rev=0.35, rec=rec)


def jazz_song(name, bpm, secs, seed):
    nb = sum(len(c) for _, c, _ in secs) + 1
    S = Song2(bpm, nb, seed=seed)
    bar = 0
    allch = [c for _, cs, _ in secs for c in cs] + [secs[-1][1][-1]]
    for name_, chords, kind in secs:
        S.mark(name_, S.T(bar))
        if name_.startswith('chorus'):
            S.mark('chorus_any', S.T(bar)); S.crash(S.T(bar))
        if name_ in ('breakdown', 'broken', 'finale'):
            S.crash(S.T(bar))
        if kind == 'head':
            play_sw(S, bar, bebop(S, len(chords), chords, seed + bar), gain=0.18)
        elif kind == 'shout':
            play_sw(S, bar, riff(chords, up=12 if bar % 16 else 0), gain=0.19)
        elif kind == 'outro':
            play_sw(S, bar, [[(0, 14, JZ[c][2] + 12)] for c in chords], gain=0.17)
        for k, ch in enumerate(chords):
            nxt = allch[min(len(allch) - 1, bar + k + 1)]
            style = {'head': 'head', 'shout': 'shout', 'outro': 'head', 'intro': 'head', 'break': 'break'}[kind]
            swing_bar(S, bar + k, ch, nxt, style, fill=(k % 4 == 3))
            if kind == 'break' and k % 2 == 1:
                for s in range(0, 16, 2):
                    S.tom(S.T(bar + k, s), 46 - s // 2, gain=0.22)
        bar += len(chords)
    tE = S.T(bar)
    last = secs[-1][1][-1]
    S.kick(tE, gain=0.4); S.crash(tE, 0.14); S.bass(jroot(last), tE, 1.4)
    for m in JZ[last]:
        S.lead2(m + 12, tE, 1.8, gain=0.05, duty=0.5, rec=False, echo=False)
    S.lead2(JZ[last][0] + 12, tE, 1.8)
    S.mark('final', tE)
    return S.finish2(name, tE, rev_wet=0.25)


V1 = ['Cmaj7', 'Am7', 'Dm7', 'G7', 'Em7', 'A7', 'Dm7', 'G7']; C1 = ['Fmaj7', 'Fm7', 'Em7', 'A7', 'Dm7', 'G7', 'Cmaj7', 'Cmaj7']
V2 = ['Fmaj7', 'Dm7', 'Gm7', 'C7', 'Am7', 'D7', 'Gm7', 'C7']; C2 = ['Bbmaj7', 'Bbm7', 'Am7', 'D7', 'Gm7', 'C7', 'Fmaj7', 'Fmaj7']
V3 = ['Bbmaj7', 'Gm7', 'Cm7', 'F7'] * 2; C3 = ['Eb7', 'Eb7', 'Bbmaj7', 'Bbmaj7', 'F7', 'Eb7', 'Bbmaj7', 'F7']
V4 = ['Gmaj7', 'Em7', 'Am7', 'D7'] * 2; C4 = ['Cmaj7', 'Cm7', 'Bm7', 'E7', 'Am7', 'D7', 'Gmaj7', 'Gmaj7']
V5 = ['Dm6', 'Dm6', 'Gm6', 'Gm6', 'Em7b5', 'A7b9', 'Dm6', 'A7b9']; C5 = ['Gm6', 'Gm6', 'Dm6', 'Dm6', 'Em7b5', 'A7b9', 'Dm6', 'Dm6']
SONGS = {
    'strut': ('c7_strut', 150, [('intro', V1[:4], 'intro'), ('verse', V1, 'head'), ('chorus', C1, 'shout'), ('verse', V1, 'head'), ('chorus', C1, 'shout'), ('outro', ['Fmaj7', 'G7', 'Cmaj7', 'Cmaj7'], 'outro')], 701),
    'shuffle': ('c7_shuffle', 160, [('intro', V2[:4], 'intro'), ('verse', V2, 'head'), ('chorus', C2, 'shout'), ('verse', V2, 'head'), ('chorus', C2, 'shout'), ('outro', ['Gm7', 'C7', 'Fmaj7', 'Fmaj7'], 'outro')], 702),
    'boogie': ('c7_boogie', 165, [('intro', V3[:4], 'intro'), ('verse', V3, 'head'), ('chorus', C3, 'shout'), ('breakdown', V3, 'break'), ('chorus', C3, 'shout'), ('outro', ['Eb7', 'F7', 'Bbmaj7', 'Bbmaj7'], 'outro')], 703),
    'riverboat': ('c7_riverboat', 172, [('intro', V4[:4], 'intro'), ('verse', V4, 'head'), ('chorus', C4, 'shout'), ('verse', V4, 'head'), ('chorus', C4, 'shout'), ('chorus_last', C4, 'shout'), ('outro', ['Am7', 'D7', 'Gmaj7', 'Gmaj7'], 'outro')], 704),
    'tony': ('c7_tony', 180, [('intro', V5[:4], 'intro'), ('verse', V5, 'head'), ('chorus', C5, 'shout'), ('verse_rev', V5, 'head'), ('broken', ['Dm6'] * 4, 'break'),
                              ('chorus_back', C5, 'shout'), ('finale', ['Dm6', 'Dm6', 'Gm6', 'Gm6', 'Em7b5', 'A7b9', 'Dm6', 'A7b9'], 'break'), ('outro', ['Gm6', 'A7b9', 'Dm6', 'Dm6'], 'outro')], 705),
}


def pause_jazz():
    S = Song2(84, 9, seed=706)
    ch = ['Dm7', 'G7', 'Cmaj7', 'A7']
    for rep in range(2):
        for k, c in enumerate(ch):
            b = rep * 4 + k
            swing_bar(S, b, c, ch[(k + 1) % 4], 'head')
        play_sw(S, rep * 4, [[(0, 6, JZ[c][2] + 12), (8, 6, JZ[c][3] + 12)] for c in ch], gain=0.13, rec=False)
    S.finish2('c7_pause_raw', S.T(8) + 0.01)
    from scipy.io import wavfile
    sr, x = wavfile.read('c7_pause_raw.wav'); L = int(round(S.T(4) * sr))
    wavfile.write('c7_pause.wav', sr, x[L:2 * L])
    return L / sr


# ======================= art =======================
FUR, FUR_L, SUIT, SUIT_D = '#2a2a3a', '#5a5a6a', '#5a2a8e', '#3a1a5e'


def cat(c, x, gy, f, pose='run', pal=None):
    pal = pal or {}
    fur, furl, suit, suitd = pal.get('fur', FUR), pal.get('furl', FUR_L), pal.get('suit', SUIT), pal.get('suitd', SUIT_D)
    p = f / 8 * 2 * math.pi
    bob = 1 if (pose == 'run' and f % 4 in (1, 2)) or (pose != 'run' and f % 2) else 0
    hip = (x, gy - 13 + bob)
    for side, ph in ((0, p), (1, p + math.pi)):
        if pose == 'run':
            fx = x + 6 * math.sin(ph); fy = gy - max(0, 3 * math.cos(ph)); kx = (hip[0] + fx) / 2 + 2 + 2 * math.sin(ph); ky = (hip[1] + fy) / 2
        else:
            fx = x - 3 + side * 6; fy = gy; kx = fx; ky = gy - 6
        col = '#2a1a3e' if side == 0 else '#3a2a5a'
        c.line([hip, (kx, ky), (fx, fy - 2)], K, 5); c.line([hip, (kx, ky), (fx, fy - 2)], col, 3)
        c.r(fx - 2, fy - 3, 6, 3, K); c.r(fx - 1, fy - 2, 5, 1, '#f4f4f4'); c.p(fx + 3, fy - 2, '#1b1030')
    tx = x - 6
    c.line([(tx, gy - 14 + bob), (tx - 5, gy - 18 + int(2 * math.sin(p))), (tx - 7, gy - 24 + int(2 * math.sin(p + 1)))], K, 4)
    c.line([(tx, gy - 14 + bob), (tx - 5, gy - 18 + int(2 * math.sin(p))), (tx - 7, gy - 24 + int(2 * math.sin(p + 1)))], fur, 2)
    ty = gy - 26 + bob
    c.r(x - 5, ty, 11, 14, K); c.r(x - 4, ty + 1, 9, 12, '#f4f4f4'); c.r(x - 4, ty + 3, 3, 10, suit); c.r(x + 2, ty + 3, 3, 10, suit)
    for yy in range(ty + 4, ty + 12, 2):
        c.p(x - 3, yy, suitd); c.p(x + 3, yy, suitd)
    c.r(x - 1, ty + 1, 3, 2, '#e8344e')
    c.line([(x - 3, ty + 2), (x - 6, ty + 8)], K, 4); c.line([(x - 3, ty + 2), (x - 6, ty + 8)], fur, 2)
    hy = ty - 11
    c.r(x - 4, hy, 10, 11, K); c.r(x - 3, hy + 1, 8, 9, fur); c.r(x + 1, hy + 5, 4, 4, furl)
    c.p(x + 1, hy + 4, '#ffe066'); c.p(x + 3, hy + 4, '#ffe066'); c.p(x + 2, hy + 4, K); c.p(x + 4, hy + 6, '#ff9ab8')
    c.r(x + 5, hy + 6, 3, 1, '#c8ccd8'); c.r(x + 5, hy + 8, 3, 1, '#c8ccd8')
    c.poly([(x - 3, hy + 1), (x - 3, hy - 4), (x, hy + 1)], fur, None); c.poly([(x + 2, hy + 1), (x + 4, hy - 4), (x + 5, hy + 1)], fur, None)
    c.r(x - 5, hy - 2, 12, 3, K); c.r(x - 7, hy, 16, 2, K); c.r(x - 4, hy - 1, 10, 1, '#3a3a48'); c.r(x - 6, hy, 14, 1, '#4a4a58'); c.r(x - 4, hy, 10, 1, '#e8344e')
    sx = [(x + 5, ty - 2), (x + 8, ty + 4), (x + 9, ty + 10), (x + 13, ty + 9)]
    c.line(sx, K, 5); c.line(sx, '#ffd23f', 3); c.r(x + 12, ty + 7, 4, 4, K); c.r(x + 13, ty + 8, 2, 2, '#c98a1a')
    c.line([(x + 3, ty + 3), (x + 8, ty + 6)], K, 3); c.line([(x + 3, ty + 3), (x + 8, ty + 6)], fur, 1)
    for k in range(3):
        c.p(x + 8, ty + 3 + k * 2, '#c98a1a')
    return (14, ty + 9 - gy, 9, ty + 5 - gy)


def cat_sheet():
    cw, ch, ax, ay, n = 40, 46, 16, 44, 8
    sheet = Image.new('RGBA', (cw * n, ch)); tips = []
    for f in range(n):
        c = magic(64); t = cat(c, ax, ay, f); sheet.paste(rgba(c.im, (0, 0, cw, ch)), (f * cw, 0)); tips.append(list(t))
    return {'src': b64(sheet), 'n': n, 'cw': cw, 'ch': ch, 'ax': ax, 'ay': ay, 'fps': 11, 'x': 38, 'tips': tips}


def e_hat(c):
    c.r(8, 10, 16, 3, K); c.r(9, 11, 14, 1, '#3a3a48'); c.r(11, 4, 10, 7, K); c.r(12, 5, 8, 5, '#3a3a48'); c.r(12, 8, 8, 1, '#e8344e')
    c.r(12, 13, 3, 2, '#ffe066'); c.r(17, 13, 3, 2, '#ffe066'); c.p(13, 13, K); c.p(18, 13, K)
    c.poly([(8, 9), (1, 4), (7, 12)], '#f4f4f4', None); c.poly([(24, 9), (31, 4), (25, 12)], '#f4f4f4', None)


def e_case(c):
    c.r(7, 6, 18, 12, K); c.r(8, 7, 16, 10, '#7a4a28'); c.r(8, 11, 16, 1, '#5a3418'); c.r(14, 4, 4, 3, K)
    c.r(11, 8, 3, 2, '#f4f4f4'); c.r(18, 8, 3, 2, '#f4f4f4'); c.p(12, 9, K); c.p(19, 9, K); c.r(13, 14, 6, 1, K)
    c.r(24, 10, 4, 2, '#3a3a48'); c.p(28, 10, '#ffe066')


def e_rat(c):
    c.disc(14, 17, 6, K); c.disc(14, 17, 5, '#8a8a98'); c.disc(20, 13, 4, K); c.disc(20, 13, 3, '#a8a8b8'); c.p(23, 14, '#ff9ab8')
    c.p(21, 12, '#ff3b3b'); c.r(16, 7, 10, 2, K); c.r(18, 4, 6, 4, K); c.r(19, 5, 4, 2, '#3a3a48'); c.r(23, 15, 5, 1, '#e8d8b0')
    c.line([(8, 18), (3, 15), (2, 11)], '#ff9ab8'); c.r(11, 22, 2, 2, K); c.r(17, 22, 2, 2, K)


def enemies_sheet():
    out = Image.new('RGBA', (32 * 6, 24))
    for l, (fn, col) in enumerate(((e_hat, '#5ef2ff'), (e_case, '#ff4fa3'), (e_rat, '#ffe066'))):
        c = magic(64); fn(c); im = rim(rgba(c.im, (0, 0, 32, 24)), col)
        out.paste(im, (l * 64, 0)); out.paste(flash(im), (l * 64 + 32, 0))
    return {'src': b64(out), 'anch': [[16, 12], [16, 12], [16, 23]]}


def notes_sheet():
    out = Image.new('RGBA', (40, 20))
    c = magic(64); c.disc(7, 14, 4, K); c.disc(7, 14, 3, '#ffd23f'); c.r(10, 3, 2, 12, K); c.r(10, 3, 6, 3, K); c.r(11, 4, 4, 1, '#ffd23f')
    out.paste(rgba(c.im, (0, 0, 20, 20)), (0, 0))
    c = magic(64); c.r(3, 9, 10, 3, K); c.r(4, 10, 8, 1, '#ffd23f'); c.poly([(12, 6), (18, 3), (18, 17), (12, 14)], '#ffd23f', None); c.r(5, 7, 2, 2, '#c98a1a')
    out.paste(rgba(c.im, (0, 0, 20, 20)), (20, 0))
    return b64(out)


def musician(c, x, gy, f, inst, suit):
    bob = f % 2
    c.r(x - 3, gy - 6, 2, 6, K); c.r(x + 1, gy - 6, 2, 6, K)
    c.r(x - 4, gy - 18 + bob, 9, 12, K); c.r(x - 3, gy - 17 + bob, 7, 10, suit); c.r(x - 1, gy - 17 + bob, 3, 3, '#f4f4f4'); c.p(x, gy - 16 + bob, '#e8344e')
    c.r(x - 3, gy - 25 + bob, 7, 7, K); c.r(x - 2, gy - 24 + bob, 5, 5, '#c88a5a'); c.p(x + 1, gy - 22 + bob, K); c.r(x - 3, gy - 26 + bob, 7, 2, '#1b1030')
    if inst == 'trumpet':
        c.r(x + 2, gy - 21 + bob, 9, 2, '#ffd23f'); c.poly([(x + 10, gy - 23 + bob), (x + 14, gy - 25 + bob), (x + 14, gy - 17 + bob), (x + 10, gy - 19 + bob)], '#ffd23f', None)
    elif inst == 'trombone':
        sl = 4 + (f % 4) * 2
        c.r(x + 2, gy - 21 + bob, 8 + sl, 1, '#ffd23f'); c.r(x + 2, gy - 18 + bob, 8 + sl, 1, '#ffd23f'); c.poly([(x + 9, gy - 23 + bob), (x + 13, gy - 26 + bob), (x + 13, gy - 16 + bob)], '#ffd23f', None)
    elif inst == 'sax':
        c.line([(x + 2, gy - 22 + bob), (x + 5, gy - 16 + bob), (x + 8, gy - 12 + bob), (x + 10, gy - 15 + bob)], '#ffd23f', 2)
    else:
        c.disc(x + 6, gy - 10, 8, K); c.disc(x + 6, gy - 10, 7, '#f4f4f4'); c.disc(x + 6, gy - 10, 5, '#e8344e'); text(c, 'BB', x + 1, gy - 13, '#ffffff', 1, None)
        c.line([(x + 2, gy - 18 + bob), (x + 6 - f % 2 * 2, gy - 22)], '#8a5a2b')


def bigband_buddy():
    cw, ch, n = 88, 40, 4
    sheet = Image.new('RGBA', (cw * n, ch))
    for f in range(n):
        c = magic(128)
        c.r(2, ch - 4, 84, 4, K); c.r(3, ch - 3, 82, 2, '#c2260f')
        for i, (inst, suit) in enumerate((('drum', '#1b1030'), ('trombone', '#3a3a48'), ('sax', '#5a2a8e'), ('trumpet', '#3a3a48'))):
            musician(c, 10 + i * 20, ch - 4, f + i, inst, suit)
        sheet.paste(rgba(c.im, (0, 0, cw, ch)), (f * cw, 0))
    return {'kind': 'sweep', 'name': 'THE BIG BAND', 'sfx': 'bigband', 'say': 'SWING IT!', 'pitch': 0.9, 'rate': 1.1, 'speed': 190,
            'src': b64(sheet), 'n': n, 'cw': cw, 'ch': ch, 'ox': 20, 'oy': ch - 1, 'front': 70, 'bolts': False}


def bouncer(c, x, gy):
    c.r(x - 18, gy - 50, 36, 40, K); c.r(x - 17, gy - 49, 34, 38, '#1b1030'); c.r(x - 3, gy - 49, 6, 14, '#f4f4f4'); c.r(x - 2, gy - 48, 4, 3, '#e8344e')
    c.r(x - 24, gy - 40, 48, 10, K); c.r(x - 23, gy - 39, 46, 8, '#3a2a2a'); c.r(x + 6, gy - 46, 8, 4, '#ffd23f'); text(c, 'STAFF', x - 14, gy - 26, '#ffd23f', 1, None)
    c.r(x - 12, gy - 66, 24, 18, K); c.r(x - 11, gy - 65, 22, 16, '#4a3a3a'); c.r(x - 7, gy - 58, 14, 7, '#7a6a5a')
    c.r(x - 8, gy - 62, 5, 2, '#ff3b3b'); c.r(x + 3, gy - 62, 5, 2, '#ff3b3b'); c.r(x - 9, gy - 64, 18, 1, K); c.r(x - 4, gy - 53, 8, 1, K)
    c.r(x - 9, gy - 64, 18, 2, '#1b1030'); c.r(x - 6, gy - 61, 12, 1, '#05030a')
    c.r(x - 14, gy - 10, 10, 10, K); c.r(x + 4, gy - 10, 10, 10, K); c.r(x - 13, gy - 9, 8, 8, '#1b1030'); c.r(x + 5, gy - 9, 8, 8, '#1b1030')


def big_tony(c, x, gy):
    x0 = x
    c.r(x0, gy - 72, 70, 66, K); c.r(x0 + 1, gy - 71, 68, 64, '#4a4a58')
    for sx in range(x0 + 4, x0 + 68, 5):
        c.r(sx, gy - 71, 1, 64, '#8a8a98')
    c.r(x0 + 28, gy - 71, 14, 30, '#f4f4f4'); c.r(x0 + 32, gy - 70, 6, 26, '#c2260f')
    c.r(x0 + 15, gy - 100, 40, 30, K); c.r(x0 + 16, gy - 99, 38, 28, '#d8a878'); c.r(x0 + 16, gy - 82, 38, 11, '#a87848')
    c.r(x0 + 22, gy - 90, 8, 3, '#1b1030'); c.r(x0 + 40, gy - 90, 8, 3, '#1b1030'); c.r(x0 + 22, gy - 93, 9, 2, K); c.r(x0 + 39, gy - 93, 9, 2, K)
    c.r(x0 + 26, gy - 80, 18, 2, K); c.r(x0 + 44, gy - 79, 10, 1, '#e8d8b0')
    c.r(x0 + 8, gy - 104, 54, 6, K); c.r(x0 + 16, gy - 118, 38, 16, K); c.r(x0 + 17, gy - 117, 36, 14, '#2a2a38'); c.r(x0 + 17, gy - 106, 36, 3, '#c2260f')
    c.r(x0 - 8, gy - 60, 12, 30, K); c.r(x0 - 7, gy - 59, 10, 28, '#4a4a58'); c.disc(x0 - 2, gy - 28, 5, '#d8a878'); c.p(x0 - 2, gy - 30, '#ffd23f')
    c.r(x0 - 40, gy - 34, 44, 3, '#ffd23f'); c.r(x0 - 40, gy - 28, 44, 3, '#ffd23f'); c.poly([(x0 - 40, gy - 38), (x0 - 52, gy - 44), (x0 - 52, gy - 18), (x0 - 40, gy - 24)], '#ffd23f', None)
    c.r(x0 + 8, gy - 6, 20, 6, K); c.r(x0 + 42, gy - 6, 20, 6, K)
    text(c, 'TONY', x0 + 24, gy - 60, '#ffd23f', 1, None)


def intro_jazz(c, f):
    c.r(170, GY - 70, 3, 70, '#1b1424'); c.r(164, GY - 74, 15, 5, K); c.disc(171, GY - 66, 4, '#ffe066'); c.disc(171, GY - 66, 2, '#ffffff')
    for k in range(12):
        c.p(150 + (k * 13 + f * 7) % 50, GY - 60 + (k * 17 + f * 9) % 50, '#8ab4ff')
    c.r(126, GY - 4, 14, 3, K); c.r(127, GY - 4, 12, 2, '#3a3a48'); c.r(129, GY - 6, 8, 2, '#3a3a48')
    if f % 4 == 2:
        c.disc(133, GY - 10 - f, 2, '#ffd23f')
    cat(c, 150, GY, f, pose='idle')
    for k in range(3):
        ph = (f + k * 3) % 8
        c.disc(170 + k * 10 + ph, GY - 40 - ph * 4, 2, '#ffd23f'); c.r(171 + k * 10 + ph, GY - 46 - ph * 4, 1, 5, '#ffd23f')
    if f % 8 in (3, 4):
        text(c, 'SMOOTH...', 150, GY - 56, '#ffffff', 1, K)


def props_jazz(c):
    c.r(170, GY - 70, 3, 70, '#1b1424'); c.r(164, GY - 74, 15, 5, K); c.disc(171, GY - 66, 4, '#ffe066')
    c.r(126, GY - 4, 14, 3, K); c.r(127, GY - 4, 12, 2, '#3a3a48'); c.r(129, GY - 6, 8, 2, '#3a3a48')


def jazz_street(P):
    far = Cv()
    sky(far, 0, HZ, P['sky'])
    r = random.Random(P['seed'])
    if P.get('moon'):
        far.disc(P['moon'][0], P['moon'][1], 12, '#f4f1d0')
    x = 0
    while x < W:
        w = r.randrange(26, 46); h = r.randrange(40, 90)
        far.r(x, HZ - h, w, h, P['bld'])
        for wy in range(HZ - h + 5, HZ - 6, 8):
            for wx in range(x + 3, x + w - 4, 6):
                if r.random() < 0.4:
                    far.r(wx, wy, 3, 4, '#ffb02e')
        x += w + 2
    L = [L_static(far, 0, HZ)]
    sg = magic(640)
    for i, (word, col) in enumerate(P['signs']):
        bx = 40 + i * 200
        sg.r(bx, HZ - 70, 6, 50, '#1b1424'); sg.r(bx - 4, HZ - 70, len(word) * 6 + 8, 13, K); sg.r(bx - 3, HZ - 69, len(word) * 6 + 6, 11, '#120a20')
        text(sg, word, bx, HZ - 67, col, 1, None)
    for lx in range(100, 640, 160):
        sg.r(lx, HZ - 40, 2, 40, '#1b1424'); sg.disc(lx + 1, HZ - 42, 3, '#ffe066')
    if P.get('car'):
        for cx in (260, 560):
            sg.r(cx, HZ - 12, 40, 10, K); sg.r(cx + 1, HZ - 11, 38, 8, '#2a2a38'); sg.r(cx + 8, HZ - 18, 20, 7, K); sg.r(cx + 9, HZ - 17, 18, 5, '#3a3a48')
            sg.disc(cx + 8, HZ - 2, 4, K); sg.disc(cx + 32, HZ - 2, 4, K); sg.r(cx + 38, HZ - 9, 2, 2, '#ffe066')
    L.append(L_scroll(sg, HZ - 72, HZ + 2, 22))
    gd = magic(640)
    gd.r(0, HZ, 640, PT - HZ, P['ground'])
    for x in range(0, 640, 10):
        for y in range(HZ + 2, PT, 6):
            o = 5 if (y // 6) % 2 else 0
            gd.r(x + o, y, 9, 5, P['stone']) if (x // 10 + y // 6) % 3 else None
    gd.r(0, HZ, 640, 1, P['edge'])
    L.append(L_scroll(gd, HZ, PT, 50, transparent=False))
    return L


def jazz_interior(P):
    far = Cv()
    far.r(0, 0, W, HZ, P['wall'])
    for x in range(0, W, 12):
        far.r(x, 24, 1, HZ - 24, P['wall_d'])
    if P.get('bar'):
        far.r(0, HZ - 34, W, 4, '#5a3418')
        for x in range(10, W, 9):
            far.r(x, HZ - 46, 4, 12, ['#3a7a3a', '#7a3a1a', '#c8a060', '#5a2a5a'][x % 4]); far.r(x + 1, HZ - 49, 2, 3, '#3a3a3a')
        far.r(0, HZ - 30, W, 30, '#7a4a28'); far.r(0, HZ - 30, W, 2, '#c8862a')
    if P.get('stage'):
        far.r(200, 30, 120, 70, '#05030a'); far.disc(260, 60, 10, '#ffe066')
        for k in range(8):
            far.r(196 + (k % 2) * 116, 28 + k * 10, 8, 10, '#a3102a')
        far.r(200, 26, 120, 6, '#c98a1a')
    if P.get('casino'):
        for cx in (60, 160):
            far.disc(cx, 70, 22, K); far.disc(cx, 70, 20, '#2a5a2a')
            for k in range(16):
                a = k * math.pi / 8
                far.line([(cx, 70), (cx + 19 * math.cos(a), 70 + 19 * math.sin(a))], '#c2260f' if k % 2 else '#1b1030')
            far.disc(cx, 70, 5, '#ffd23f')
        for sx in range(200, 320, 30):
            far.r(sx, 50, 24, 50, K); far.r(sx + 1, 51, 22, 48, '#c2260f'); far.r(sx + 4, 58, 16, 10, '#f4f4f4'); text(far, '777', sx + 3, 59, '#c2260f', 1, None)
    L = [L_static(far, 0, HZ)]
    if P.get('lights'):
        lt = magic(640)
        for x in range(0, 640, 8):
            y = 30 + int(4 * math.sin(x / 20)); lt.p(x, y, '#3a2a1a')
            if x % 16 == 0:
                lt.disc(x, y + 2, 1, ['#ffe066', '#ff4fa3', '#5ef2ff'][x // 16 % 3])
        L.append(L_scroll(lt, 26, 40, 15))
    fl = magic(640)
    fl.r(0, HZ, 640, PT - HZ, P['floor'])
    for x in range(0, 640, P.get('plank', 16)):
        fl.r(x, HZ, 1, PT - HZ, P['floor_d'])
    if P.get('carpet'):
        fl.r(0, HZ + 16, 640, 30, '#8a0a1e'); fl.r(0, HZ + 16, 640, 1, '#ffd23f'); fl.r(0, HZ + 45, 640, 1, '#ffd23f')
    fl.r(0, HZ, 640, 1, P.get('edge', '#c8862a'))
    L.append(L_scroll(fl, HZ, PT, 50, transparent=False))
    return L


def jazz_rooftop():
    L = jazz_street(dict(sky=['#05061a', '#0a0c26', '#141838', '#1e2248'], seed=73, bld='#0a0a18', moon=(250, 40), signs=[('SWING', '#ff4fa3'), ('HOTEL', '#ffe066'), ('BLUES', '#5ef2ff')],
                         ground='#2a2a30', stone='#232328', edge='#5a5a6a'))
    wt = magic(640)
    for x in (60, 380):
        wt.r(x, HZ - 50, 24, 26, K); wt.r(x + 1, HZ - 49, 22, 24, '#5a3a28'); wt.poly([(x - 2, HZ - 50), (x + 12, HZ - 60), (x + 26, HZ - 50)], '#3a2a1a', None)
        wt.r(x + 3, HZ - 24, 2, 24, '#2a1a10'); wt.r(x + 19, HZ - 24, 2, 24, '#2a1a10')
    for x in range(0, 640, 6):
        y = HZ - 30 + int(3 * math.sin(x / 15)); wt.p(x, y, '#3a3a48')
        if x % 18 == 0:
            wt.disc(x, y + 2, 1, '#ffe066')
    L.insert(-1, L_scroll(wt, HZ - 62, HZ, 25))
    return L


def jazz_riverboat():
    far = Cv()
    sky(far, 0, HZ, ['#06081a', '#0c1030', '#141a44', '#1c2456'])
    stars_r = random.Random(74)
    for _ in range(50):
        far.p(stars_r.randrange(W), stars_r.randrange(26, 70), '#ffffff')
    far.disc(70, 46, 12, '#f4f1d0')
    for x in range(0, W, 10):
        h = 6 + (x * 7) % 18; far.r(x, HZ - 34 - h, 8, h, '#0a0c1e')
        if x % 20 == 0:
            far.p(x + 3, HZ - 30 - h, '#ffb02e')
    far.r(0, HZ - 34, W, 34, '#0a1430')
    for y in range(HZ - 32, HZ, 3):
        for x in range(60 + (y % 6), 84, 4):
            far.p(x, y, '#f4f1d0')
    L = [L_static(far, 0, HZ)]
    pw = magic(640)
    for x in range(30, 640, 160):
        pw.disc(x, HZ - 10, 18, K); pw.disc(x, HZ - 10, 16, '#c2260f')
        for k in range(8):
            a = k * math.pi / 4
            pw.line([(x, HZ - 10), (x + 15 * math.cos(a), HZ - 10 + 15 * math.sin(a))], '#5a0a10', 2)
    L.append(L_scroll(pw, HZ - 30, HZ + 8, 30))
    dk = magic(640)
    dk.r(0, HZ, 640, PT - HZ, '#7a4a28')
    for x in range(0, 640, 14):
        dk.r(x, HZ, 1, PT - HZ, '#5a3418')
    dk.r(0, HZ - 12, 640, 2, '#f4f4f4'); dk.r(0, HZ - 6, 640, 1, '#f4f4f4')
    for x in range(0, 640, 12):
        dk.r(x, HZ - 12, 1, 12, '#f4f4f4')
    L.append(L_scroll(dk, HZ - 14, PT, 50))
    return L


JAZZ_V = [lambda: jazz_interior(dict(wall='#3a1a12', wall_d='#2a120a', bar=True, stage=True, lights=True, floor='#5a3418', floor_d='#3a2008')),
          jazz_rooftop, jazz_riverboat,
          lambda: jazz_interior(dict(wall='#1a0408', wall_d='#2a0a10', casino=True, lights=True, floor='#2a0a10', floor_d='#1a0408', carpet=True, plank=24, edge='#ffd23f'))]


def jazz_base():
    layers = jazz_street(dict(sky=['#0a0818', '#120e28', '#1a1438', '#241a48'], seed=71, bld='#0e0a1a', signs=[('JAZZ', '#ff4fa3'), ('CLUB', '#5ef2ff'), ('HOT', '#ffe066')],
                              car=True, ground='#2a2632', stone='#34303e', edge='#5a5670'))
    fs = frames_sheet(lambda c, f: intro_jazz(c, f), 8, (0, 0)); fs.pop('extra', None)
    c = magic(); props_jazz(c); box = rgba(c.im).getbbox()
    fs['props'] = {'src': b64(rgba(c.im, box)), 'x': box[0], 'y': box[1]}
    return {'id': '7-1', 'layers': layers, 'hero': cat_sheet(), 'enemies': enemies_sheet(), 'notes': notes_sheet(), 'buddy': bigband_buddy(), 'intro': fs}


if __name__ == '__main__':
    for nm in sys.argv[1:]:
        if nm == 'pause':
            print(nm, round(pause_jazz(), 1))
        else:
            key, bpm, secs, seed = SONGS[nm]
            print(nm, round(jazz_song(key, bpm, secs, seed), 1), flush=True)
