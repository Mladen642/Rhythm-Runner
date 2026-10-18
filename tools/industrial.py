import math, random, sys
from PIL import Image
from songlib import *
from songs3 import loop_song
from songs4 import M
from anim import *
from stage_assets2 import magic, rgba, b64, L_scroll, L_static, W, frames_sheet
from new_art import rim, flash
HZ, PT, GY = 126, 180, 166

IC = {'Em': [52, 55, 59], 'C': [48, 52, 55], 'D': [50, 54, 57], 'B': [47, 51, 54], 'Dm': [50, 53, 57], 'Bb': [46, 50, 53], 'A': [45, 49, 52],
      'Am': [45, 48, 52], 'F': [41, 45, 48], 'G': [43, 47, 50], 'E': [40, 44, 47], 'Cm': [48, 51, 55], 'Ab': [44, 48, 51], 'Gm': [43, 46, 50]}


def iroot(ch):
    r = IC[ch][0] % 12
    return 36 + r if r >= 4 else 48 + r - 12 if r < 4 else 36 + r


RIFF = [1, 0, 0.5, 0.5, 1, 0, 0.5, 0, 1, 0, 0.5, 0.5, 1, 0, 0.5, 0]


def ind_bar(S, bar, ch, style, fill=False):
    t, st, tones = S.T(bar), S.STEP, IC[ch]
    r = iroot(ch)
    if style != 'intro':
        for s in (0, 4, 8, 12):
            S.kick(t + s * st, gain=0.55)
        if style == 'chorus':
            S.kick(t + 7 * st, gain=0.35); S.kick(t + 15 * st, gain=0.35)
        for s in (4, 12):
            S.snare(t + s * st, gain=0.34)
        for s in range(0, 16, 2):
            S.hat(t + s * st, gain=0.05)
    if style in ('verse', 'chorus'):
        for s, acc in enumerate(RIFF):
            if acc:
                S.power(r + 12, t + s * st, st * (1.8 if acc == 1 else 0.9), mute=(acc < 1), gain=0.12 if acc == 1 else 0.09)
        for s in range(0, 16, 2):
            S.bass(r, t + s * st, 1.8 * st, gain=0.25)
    seq = [24, 31, 36, 31]
    for s in range(16):
        S.arp(r + seq[s % 4], t + s * st, gain=0.026 if style != 'intro' else 0.03, pan=0.4 if s % 2 else -0.4, duty=0.25, length=st * 0.6)
    for s in (2, 6, 10, 14):
        S.bell(96, t + s * st, gain=0.03)
    if style in ('chorus', 'march', 'intro'):
        S.pad([x + 12 for x in tones], t, S.BAR * 0.98, gain=0.04, rate=1.0, duty=0.5)
        S.organ([x + 12 for x in tones], t, S.BAR * 0.98, gain=0.02)
    if style == 'march':
        S.kick(t, gain=0.5); S.kick(t + 8 * st, gain=0.5)
        for s in range(16):
            S.snare(t + s * st, gain=0.05 + 0.03 * (s % 4 == 0))
        S.bass(r, t, 14 * st, gain=0.25)
    if fill:
        S.fill(bar, start=12)


def ind_verse(chords, seed):
    rng = random.Random(seed)
    PAT = [[(0, 2, 0), (2, 2, 0), (4, 4, 1), (8, 2, 0), (10, 2, 0), (12, 4, 2)], [(0, 4, 0), (4, 2, 1), (6, 2, 0), (8, 8, 2)],
           [(0, 2, 2), (2, 2, 1), (4, 4, 0), (8, 4, 1), (12, 4, 0)], [(0, 6, 0), (6, 2, 1), (8, 4, 2), (12, 4, 1)]]
    out = []
    for i, ch in enumerate(chords):
        tones = IC[ch]; pat = PAT[(i // 2 + rng.randrange(2)) % len(PAT)]
        out.append([(a, ln, tones[idx] + 12) for a, ln, idx in pat])
    return out


def ind_chorus(chords):
    return [[(0, 8, IC[c][2] + 24 - (12 if IC[c][2] + 24 > 76 else 0)), (8, 6, IC[c][1] + 24 - (12 if IC[c][1] + 24 > 76 else 0)), (14, 2, IC[c][0] + 24)] for c in chords]


def ind_song(name, bpm, secs, seed):
    nb = sum(len(c) for _, c, _ in secs) + 1
    S = Song2(bpm, nb, seed=seed)
    bar = 0
    for name_, chords, kind in secs:
        S.mark(name_, S.T(bar))
        if name_.startswith('chorus'):
            S.mark('chorus_any', S.T(bar)); S.crash(S.T(bar))
        if name_ in ('breakdown', 'broken', 'finale'):
            S.crash(S.T(bar))
        mel = ind_verse(chords, seed + bar) if kind == 'verse' else ind_chorus(chords) if kind == 'chorus' else None
        if mel:
            for k, notes in enumerate(mel):
                for a, ln, m in notes:
                    S.lead2(m, S.T(bar + k, a), ln * S.STEP * 0.92, gain=0.2, duty=0.25, vib=0.003, rev=0.35)
                    if kind == 'chorus':
                        S.lead2(m - 12, S.T(bar + k, a), ln * S.STEP * 0.92, gain=0.1, duty=0.5, rec=False, echo=False, pan=-0.3, rev=0.4)
        if kind == 'chorus' and bar % 2 == 0:
            S.hey(S.T(bar, 4), gain=0.16)
        if kind == 'outro':
            for k, ch in enumerate(chords):
                S.lead2(IC[ch][0] + 24, S.T(bar + k), 14 * S.STEP, gain=0.18, rev=0.4)
        for k, ch in enumerate(chords):
            style = {'verse': 'verse', 'chorus': 'chorus', 'outro': 'chorus', 'intro': 'intro', 'march': 'march'}[kind]
            ind_bar(S, bar + k, ch, style, fill=(k % 4 == 3 and kind != 'march'))
        bar += len(chords)
    tE = S.T(bar)
    last = secs[-1][1][-1]
    S.kick(tE, gain=0.6); S.crash(tE, 0.14); S.power(iroot(last) + 12, tE, 1.8, gain=0.14); S.bass(iroot(last), tE, 1.6); S.bell(96, tE, 0.06)
    S.lead2(IC[last][0] + 24, tE, 1.8)
    S.mark('final', tE)
    return S.finish2(name, tE, rev_wet=0.28)


V1 = ['Em', 'Em', 'C', 'D'] * 2; C1 = ['C', 'D', 'Em', 'Em', 'C', 'D', 'B', 'B']
V2 = ['Dm', 'Dm', 'Bb', 'C'] * 2; C2 = ['Bb', 'C', 'Dm', 'Dm', 'Bb', 'C', 'A', 'A']
V3 = ['Am', 'Am', 'F', 'G'] * 2; C3 = ['F', 'G', 'Am', 'Am', 'F', 'G', 'E', 'E']
V4 = ['Cm', 'Cm', 'Ab', 'Bb'] * 2; C4 = ['Ab', 'Bb', 'Cm', 'Cm', 'Ab', 'Bb', 'G', 'G']
SONGS = {
    'stahl': ('c12_stahl', 112, [('intro', V1[:4], 'intro'), ('verse', V1, 'verse'), ('chorus', C1, 'chorus'), ('verse', V1, 'verse'), ('chorus', C1, 'chorus'), ('outro', ['C', 'B', 'Em', 'Em'], 'outro')], 1201),
    'hafen': ('c12_hafen', 116, [('intro', V2[:4], 'intro'), ('verse', V2, 'verse'), ('chorus', C2, 'chorus'), ('verse', V2, 'verse'), ('chorus', C2, 'chorus'), ('outro', ['Bb', 'A', 'Dm', 'Dm'], 'outro')], 1202),
    'fabrik': ('c12_fabrik', 120, [('intro', V3[:4], 'intro'), ('verse', V3, 'verse'), ('chorus', C3, 'chorus'), ('breakdown', V3, 'march'), ('chorus', C3, 'chorus'), ('outro', ['F', 'E', 'Am', 'Am'], 'outro')], 1203),
    'funken': ('c12_funken', 124, [('intro', V4[:4], 'intro'), ('verse', V4, 'verse'), ('chorus', C4, 'chorus'), ('verse', V4, 'verse'), ('chorus', C4, 'chorus'), ('chorus_last', C4, 'chorus'), ('outro', ['Ab', 'G', 'Cm', 'Cm'], 'outro')], 1204),
    'kran': ('c12_kran', 128, [('intro', ['Em'] * 4, 'intro'), ('verse', V1, 'verse'), ('chorus', C1, 'chorus'), ('verse_rev', V1, 'verse'), ('broken', ['Em'] * 4, 'march'),
                               ('chorus_back', C1, 'chorus'), ('finale', ['Em', 'Em', 'C', 'C', 'D', 'D', 'B', 'B'], 'march'), ('outro', ['C', 'B', 'Em', 'Em'], 'outro')], 1205),
}


def pause_ind():
    m = M('E4:8 G4:8', 'C4:8 E4:8', 'D4:8 F#4:8', 'B3:14')
    return loop_song('c12_pause', 80, ['Em', 'C', 'D', 'B'], m, 4, 1206, soft=True)


# ======================= art =======================
def kraft(c, x, gy, f, pose='run'):
    p = f / 8 * 2 * math.pi
    bob = 1 if (pose == 'run' and f % 4 in (1, 2)) or (pose != 'run' and f % 2) else 0
    hip = (x, gy - 15 + bob)
    for side, ph in ((0, p), (1, p + math.pi)):
        if pose == 'run':
            fx = x + 7 * math.sin(ph); fy = gy - max(0, 3 * math.cos(ph)); kx = (hip[0] + fx) / 2 + 2 + 2 * math.sin(ph); ky = (hip[1] + fy) / 2
        else:
            fx = x - 4 + side * 8; fy = gy; kx = fx; ky = gy - 8
        c.line([hip, (kx, ky), (fx, fy - 4)], K, 6); c.line([hip, (kx, ky), (fx, fy - 4)], '#1b1424' if side == 0 else '#2a2236', 4)
        c.r(fx - 3, fy - 6, 7, 6, K); c.r(fx - 2, fy - 5, 5, 4, '#2a2a38'); c.r(fx - 2, fy - 2, 6, 1, '#5a5a6a')
    ty = gy - 31 + bob
    c.r(x - 7, ty, 15, 17, K); c.r(x - 6, ty + 1, 13, 15, '#1b1424'); c.r(x - 2, ty + 1, 5, 15, '#2a2a38')
    c.r(x - 6, ty + 13, 13, 2, '#5a3418'); c.r(x, ty + 13, 2, 2, '#c8ccd8')
    c.poly([(x - 7, ty + 6), (x - 12, ty + 22 + int(2 * math.sin(p))), (x - 6, ty + 17)], '#1b1424', None)
    c.line([(x - 5, ty + 2), (x - 8, ty + 11)], K, 5); c.line([(x - 5, ty + 2), (x - 8, ty + 11)], '#1b1424', 3)
    hy = ty - 11
    c.r(x - 5, hy, 11, 11, K); c.r(x - 4, hy + 1, 9, 9, '#e8b890'); c.r(x - 4, hy + 1, 9, 2, '#5a4a3a')
    c.r(x - 5, hy + 2, 11, 3, K); c.r(x - 4, hy + 3, 4, 1, '#ff9e3d'); c.r(x + 1, hy + 3, 4, 1, '#ff9e3d')
    c.p(x + 3, hy + 6, K); c.r(x + 1, hy + 8, 4, 1, '#5a3418'); c.r(x - 4, hy + 9, 9, 1, '#c89070')
    gx, gyy = x + 4, ty + 8
    c.poly([(gx, gyy + 2), (gx + 14, gyy - 8), (gx + 16, gyy - 5), (gx + 3, gyy + 6)], '#3a3a48', None)
    c.r(gx - 2, gyy, 10, 9, K); c.r(gx - 1, gyy + 1, 8, 7, '#8a1a10'); c.r(gx + 1, gyy + 3, 4, 2, '#c8ccd8')
    c.r(gx + 14, gyy - 12, 2, 5, K); c.r(gx + 17, gyy - 11, 2, 4, K); c.p(gx + 14, gyy - 13, '#8a8a98'); c.p(gx + 17, gyy - 12, '#8a8a98')
    c.line([(x + 4, ty + 3), (x + 8, ty + 8)], K, 4); c.line([(x + 4, ty + 3), (x + 8, ty + 8)], '#e8b890', 2)
    return (gx + 15, gyy - 13 - gy, gx + 3, gyy + 4 - gy)


def kraft_sheet():
    cw, ch, ax, ay, n = 46, 52, 16, 50, 8
    sheet = Image.new('RGBA', (cw * n, ch)); tips = []
    for f in range(n):
        c = magic(64); t = kraft(c, ax, ay, f); sheet.paste(rgba(c.im, (0, 0, cw, ch)), (f * cw, 0)); tips.append([t[0] - ax, t[1], t[2] - ax, t[3]])
    return {'src': b64(sheet), 'n': n, 'cw': cw, 'ch': ch, 'ax': ax, 'ay': ay, 'fps': 10, 'x': 38, 'tips': tips}


def e_gear(c):
    c.disc(16, 12, 7, K); c.disc(16, 12, 6, '#8a8a98'); c.disc(16, 12, 2, '#ff3b3b')
    for k in range(8):
        a = k * math.pi / 4; c.r(16 + 8 * math.cos(a) - 1, 12 + 8 * math.sin(a) - 1, 3, 3, '#5a5a6a')
    c.r(8, 2, 16, 1, '#c8ccd8'); c.r(15, 2, 2, 3, '#5a5a6a')


def e_bolt(c):
    c.r(11, 5, 10, 6, K); c.r(12, 6, 8, 4, '#a8a8b8'); c.r(14, 11, 4, 10, K); c.r(15, 11, 2, 9, '#8a8a98')
    for y in range(12, 20, 2):
        c.r(14, y, 4, 1, '#5a5a6a')
    c.p(13, 7, '#ff3b3b'); c.p(18, 7, '#ff3b3b'); c.r(14, 9, 4, 1, K)


def e_oilcan(c):
    c.r(9, 8, 14, 13, K); c.r(10, 9, 12, 11, '#3a5a3a'); c.r(10, 13, 12, 2, '#ffd23f'); c.line([(22, 10), (29, 5)], K, 2)
    c.r(12, 10, 3, 2, '#ffffff'); c.r(17, 10, 3, 2, '#ffffff'); c.p(13, 11, K); c.p(18, 11, K)
    for lx in (10, 14, 18, 22):
        c.line([(lx, 21), (lx + (-2 if lx < 16 else 2), 23)], K)
    c.disc(30, 4, 1, '#1b1030')


def enemies_sheet():
    out = Image.new('RGBA', (32 * 6, 24))
    for l, (fn, col) in enumerate(((e_gear, '#5ef2ff'), (e_bolt, '#ff4fa3'), (e_oilcan, '#ffe066'))):
        c = magic(64); fn(c); im = rim(rgba(c.im, (0, 0, 32, 24)), col)
        out.paste(im, (l * 64, 0)); out.paste(flash(im), (l * 64 + 32, 0))
    return {'src': b64(out), 'anch': [[16, 12], [16, 12], [16, 23]]}


def notes_sheet():
    out = Image.new('RGBA', (40, 20))
    c = magic(64); c.disc(10, 10, 6, K); c.disc(10, 10, 5, '#ff9e3d'); c.disc(10, 10, 2, K)
    for k in range(6):
        a = k * math.pi / 3; c.r(10 + 7 * math.cos(a) - 1, 10 + 7 * math.sin(a) - 1, 3, 3, '#ff9e3d')
    out.paste(rgba(c.im, (0, 0, 20, 20)), (0, 0))
    c = magic(64); c.poly([(11, 1), (4, 11), (9, 11), (7, 19), (15, 7), (10, 7)], '#ff3b3b', None)
    out.paste(rgba(c.im, (0, 0, 20, 20)), (20, 0))
    return b64(out)


def pyro_guy(c, x, y, f):
    c.r(x + 6, y + 14, 14, 18, K); c.r(x + 7, y + 15, 12, 16, '#c8ccd8'); c.r(x + 7, y + 22, 12, 2, '#8a8a98')
    c.r(x + 8, y + 4, 10, 11, K); c.r(x + 9, y + 5, 8, 9, '#c8ccd8'); c.r(x + 10, y + 7, 6, 3, '#ff9e3d')
    c.r(x + 2, y + 16, 5, 12, K); c.r(x + 3, y + 17, 3, 10, '#c2260f')
    for k, yy in enumerate((y + 18, y + 24)):
        c.line([(x + 18, yy), (x + 34, yy - 2)], K, 4); c.line([(x + 18, yy), (x + 34, yy - 2)], '#5a5a6a', 2)
        c.disc(x + 35, yy - 2, 2, '#ff9e3d' if (f + k) % 2 else '#ffe066')
    c.r(x + 8, y + 31, 4, 6, K); c.r(x + 14, y + 31, 4, 6, K)


def pyro_buddy():
    cw, ch, n = 44, 38, 4
    sheet = Image.new('RGBA', (cw * n, ch))
    for f in range(n):
        c = magic(64); pyro_guy(c, 2, 0, f); sheet.paste(rgba(c.im, (0, 0, cw, ch)), (f * cw, 0))
    return {'kind': 'beam', 'name': 'DER PYROTECHNIKER', 'sfx': 'pyro', 'say': 'FEUER FREI!', 'pitch': 0.3, 'rate': 0.85,
            'src': b64(sheet), 'n': n, 'cw': cw, 'ch': ch, 'ox': 0, 'oy': 0, 'cols': ['#ff3b3b', '#ff9e3d', '#ffe066', '#ffffff']}


def press(c, x, gy):
    c.r(x - 26, gy - 80, 52, 12, K); c.r(x - 25, gy - 79, 50, 10, '#5a5a6a'); c.r(x - 24, gy - 79, 48, 2, '#ffd23f')
    for k in range(6):
        c.r(x - 24 + k * 9, gy - 74, 4, 3, K)
    c.r(x - 30, gy - 80, 6, 80, K); c.r(x + 24, gy - 80, 6, 80, K); c.r(x - 29, gy - 79, 4, 78, '#3a3a48'); c.r(x + 25, gy - 79, 4, 78, '#3a3a48')
    c.r(x - 6, gy - 68, 12, 22, K); c.r(x - 5, gy - 67, 10, 20, '#c8ccd8')
    c.r(x - 22, gy - 46, 44, 12, K); c.r(x - 21, gy - 45, 42, 10, '#8a1a10'); c.r(x - 14, gy - 42, 8, 4, '#ffe066'); c.r(x + 6, gy - 42, 8, 4, '#ffe066')
    c.r(x - 22, gy - 8, 44, 8, K); c.r(x - 21, gy - 7, 42, 6, '#3a3a48')
    text(c, 'DRUCK', x - 14, gy - 77, K, 1, None)


def crane(c, x, gy):
    x0 = x
    c.r(x0 + 20, gy - 110, 24, 104, K)
    for y in range(gy - 108, gy - 8, 10):
        c.line([(x0 + 21, y), (x0 + 43, y + 10)], '#c2260f', 2); c.line([(x0 + 43, y), (x0 + 21, y + 10)], '#c2260f', 2)
    c.r(x0 + 21, gy - 109, 2, 102, '#c2260f'); c.r(x0 + 41, gy - 109, 2, 102, '#c2260f')
    c.r(x0 + 10, gy - 128, 44, 20, K); c.r(x0 + 11, gy - 127, 42, 18, '#ffd23f'); c.r(x0 + 15, gy - 122, 12, 6, '#ff3b3b'); c.r(x0 + 37, gy - 122, 12, 6, '#ff3b3b')
    c.line([(x0 + 12, gy - 126), (x0 + 28, gy - 120)], K, 2); c.line([(x0 + 52, gy - 126), (x0 + 36, gy - 120)], K, 2); c.r(x0 + 22, gy - 113, 20, 3, K)
    c.r(x0 - 40, gy - 132, 96, 6, K); c.r(x0 - 39, gy - 131, 94, 4, '#c2260f')
    for k in range(10):
        c.line([(x0 - 38 + k * 9, gy - 131), (x0 - 34 + k * 9, gy - 127)], '#ffd23f')
    c.line([(x0 - 30, gy - 126), (x0 - 30, gy - 70)], '#1b1030', 1); c.poly([(x0 - 34, gy - 70), (x0 - 26, gy - 70), (x0 - 26, gy - 62), (x0 - 30, gy - 58), (x0 - 34, gy - 64)], '#5a5a6a', None)
    c.r(x0 + 8, gy - 8, 48, 8, K); c.r(x0 + 9, gy - 7, 46, 6, '#3a3a48')
    for wx in (x0 + 14, x0 + 50):
        c.disc(wx, gy - 2, 3, '#8a8a98')
    text(c, 'KRAN', x0 + 20, gy - 106, '#ffffff', 1, None)


def intro_ind(c, f):
    c.r(132, GY - 14, 22, 6, K); c.r(133, GY - 13, 20, 4, '#3a3a48'); c.r(138, GY - 8, 10, 8, K); c.r(139, GY - 7, 8, 7, '#2a2a38')
    c.r(140, GY - 17, 10, 3, '#ff5a1f'); c.r(142, GY - 18, 6, 1, '#ffe066')
    kraft(c, 162, GY, f, pose='idle')
    for k in range(10):
        ph = (f * 0.25 + k * 0.1) % 1
        c.p(145 + math.cos(k * 1.7) * ph * 22, GY - 18 - math.sin(k * 1.3 + 0.5) * ph * 20 + ph * ph * 10, '#ffe066' if k % 2 else '#ff9e3d')
    if f % 8 in (4, 5):
        text(c, 'WUNDERBAR.', 140, GY - 70, '#ffffff', 1, K)


def props_ind(c):
    c.r(132, GY - 14, 22, 6, K); c.r(133, GY - 13, 20, 4, '#3a3a48'); c.r(138, GY - 8, 10, 8, K); c.r(139, GY - 7, 8, 7, '#2a2a38')


def warehouse(c, x, base, w, h, seed, lit=0.4):
    r = random.Random(seed)
    c.r(x, base - h, w, h, '#7a2a1a')
    for y in range(base - h, base, 3):
        for bx in range(x + ((y // 3) % 2) * 3, x + w, 6):
            c.r(bx, y, 5, 2, r.choice(['#8a3422', '#7a2a1a', '#9a3e28']))
    steps = 4
    for k in range(steps):
        sw = w - k * (w // (steps * 2 + 1)) * 2
        c.r(x + (w - sw) // 2, base - h - (k + 1) * 6, sw, 6, '#7a2a1a')
    c.poly([(x + w // 2 - 4, base - h - steps * 6), (x + w // 2, base - h - steps * 6 - 14), (x + w // 2 + 4, base - h - steps * 6)], '#3a8a6a', None)
    for wy in range(base - h + 6, base - 8, 12):
        for wx in range(x + 4, x + w - 6, 9):
            c.r(wx, wy, 5, 8, '#1b1424'); c.disc(wx + 2, wy, 2, '#1b1424', ymax=wy)
            if r.random() < lit:
                c.r(wx + 1, wy + 1, 3, 6, '#ffb02e')


def brick_world(P):
    far = Cv()
    sky(far, 0, HZ, P['sky'])
    r = random.Random(P['seed'])
    if P.get('moon'):
        far.disc(P['moon'][0], P['moon'][1], 10, '#e8e6d0')
    if P.get('warehouses'):
        x = -6
        while x < W:
            w = r.randrange(40, 60); h = r.randrange(40, 70)
            warehouse(far, x, HZ - P.get('water', 0), w, h, r.randrange(999), P.get('lit', 0.4)); x += w + 2
    if P.get('water'):
        wy = HZ - P['water']
        far.r(0, wy, W, P['water'], '#1a3a3a')
        for y in range(wy, HZ, 2):
            for x in range(r.randrange(6), W, 9):
                far.r(x, y, 4, 1, r.choice(['#2a5a5a', '#ffb02e', '#3a6a6a']) if r.random() < 0.5 else '#1a3a3a')
    if P.get('cranes'):
        for cx in (40, 150, 260):
            far.r(cx, HZ - 80, 4, 80, '#2a1a1a'); far.r(cx - 30, HZ - 82, 60, 3, '#2a1a1a'); far.line([(cx - 28, HZ - 80), (cx - 28, HZ - 50)], '#2a1a1a')
        for k in range(14):
            far.r(k * 23, HZ - 18 - (k % 3) * 9, 22, 9, ['#c2260f', '#3a6aa8', '#ffb02e', '#3a8a3a'][k % 4]); far.r(k * 23, HZ - 18 - (k % 3) * 9, 22, 1, '#1b1030')
    if P.get('hall'):
        far.r(0, 24, W, HZ - 24, '#6a2a1a')
        for y in range(24, HZ, 4):
            for x in range(((y // 4) % 2) * 4, W, 8):
                far.r(x, y, 7, 3, r.choice(['#7a3422', '#6a2a1a']))
        for wx in range(20, W, 70):
            far.r(wx, 36, 34, 60, '#1a2a3a'); far.disc(wx + 17, 36, 17, '#1a2a3a', ymax=36)
            for k in range(1, 4):
                far.r(wx + k * 8, 30, 1, 66, '#3a2a2a')
            far.r(wx, 64, 34, 1, '#3a2a2a')
        for bx in range(0, W, 40):
            far.r(bx, 24, 4, HZ - 24, '#2a2a38')
        far.r(0, 30, W, 4, '#2a2a38')
    if P.get('mill'):
        far.r(0, 24, W, HZ - 24, '#1a0c08')
        for fx in (40, 200):
            far.r(fx, HZ - 60, 60, 60, '#3a2a28'); far.r(fx + 16, HZ - 40, 28, 30, '#ff5a1f'); far.r(fx + 20, HZ - 36, 20, 22, '#ffe066')
        far.poly([(130, 50), (160, 50), (150, 70), (140, 70)], '#5a5a6a', None)
        far.r(143, 70, 4, HZ - 70, '#ff9e3d'); far.r(144, 70, 2, HZ - 70, '#ffe066')
    L = [L_static(far, 0, HZ)]
    if P.get('chimneys'):
        ch = magic(640)
        for x in range(20, 640, 70):
            ch.r(x, HZ - 40, 12, 40, '#7a2a1a'); ch.r(x - 2, HZ - 42, 16, 3, '#5a1a10')
            for k in range(4):
                ch.disc(x + 6 + k * 4, HZ - 48 - k * 6, 4 + k, '#4a4a58')
        L.append(L_scroll(ch, HZ - 72, HZ, 22))
    if P.get('railing'):
        rl = magic(640)
        rl.r(0, HZ - 14, 640, 2, '#1b1030')
        for x in range(0, 640, 8):
            rl.r(x, HZ - 14, 1, 14, '#1b1030')
        for x in range(0, 640, 64):
            rl.r(x, HZ - 18, 3, 18, '#1b1030'); rl.disc(x + 1, HZ - 20, 2, '#1b1030')
        L.append(L_scroll(rl, HZ - 22, HZ + 1, 50))
    if P.get('belts'):
        bl = magic(640)
        for y in (HZ - 30,):
            bl.r(0, y, 640, 6, '#2a2a38')
            for x in range(0, 640, 10):
                bl.r(x, y + 1, 5, 4, '#5a5a6a')
            for x in range(30, 640, 90):
                bl.r(x, y - 10, 14, 10, '#8a5a2b'); bl.r(x, y - 10, 14, 1, '#c8862a')
        L.append(L_scroll(bl, HZ - 42, HZ - 22, 60))
    gd = magic(640)
    gd.r(0, HZ, 640, PT - HZ, P['ground'])
    if P.get('cobble'):
        for x in range(0, 640, 8):
            for y in range(HZ, PT, 6):
                gd.r(x + (y // 6 % 2) * 4, y, 7, 5, r.choice(['#3a3a48', '#4a4a58', '#34343f']))
    if P.get('plates'):
        for x in range(0, 640, 24):
            gd.r(x, HZ, 1, PT - HZ, '#1a1a22')
            for k in range(3):
                gd.p(x + 4 + k * 7, HZ + 4, '#8a8a98')
    if P.get('tiles'):
        for x in range(0, 640, 6):
            for y in range(HZ, PT, 5):
                gd.r(x + (y // 5 % 2) * 3, y, 5, 4, r.choice(['#5a1a10', '#6a2214']))
    if P.get('lines'):
        for x in range(0, 640, 30):
            gd.r(x, HZ + 26, 16, 2, '#ffd23f')
    gd.r(0, HZ, 640, 1, P['edge'])
    L.append(L_scroll(gd, HZ, PT, 50, transparent=False))
    return L


BRICK_V = [lambda: brick_world(dict(sky=['#9ab0c0', '#b8c8d0', '#d8e0e4'], seed=1212, cranes=True, water=14, ground='#5a5a64', edge='#8a8a98', lines=True)),
           lambda: brick_world(dict(sky=['#1a0c08', '#2a140c'], seed=1213, hall=True, belts=True, ground='#2a2a32', edge='#8a8a98', plates=True)),
           lambda: brick_world(dict(sky=['#0a0c14', '#121624', '#1a2034'], seed=1214, moon=(60, 40), warehouses=True, chimneys=True, lit=0.25, ground='#5a1a10', edge='#3a8a6a', tiles=True)),
           lambda: brick_world(dict(sky=['#1a0804', '#2a0c06'], seed=1215, mill=True, ground='#2a2a32', edge='#ff5a1f', plates=True))]


def ind_base():
    layers = brick_world(dict(sky=['#2a2a3a', '#3a3a4a', '#5a5a68', '#7a7a88'], seed=1211, warehouses=True, water=16, railing=True, lit=0.5, ground='#3a3a48', edge='#5a5a6a', cobble=True))
    fs = frames_sheet(lambda c, f: intro_ind(c, f), 8, (0, 0)); fs.pop('extra', None)
    c = magic(); props_ind(c); box = rgba(c.im).getbbox()
    fs['props'] = {'src': b64(rgba(c.im, box)), 'x': box[0], 'y': box[1]}
    return {'id': '12-1', 'layers': layers, 'hero': kraft_sheet(), 'enemies': enemies_sheet(), 'notes': notes_sheet(), 'buddy': pyro_buddy(), 'intro': fs}


if __name__ == '__main__':
    for nm in sys.argv[1:]:
        if nm == 'pause':
            print(nm, round(pause_ind(), 1))
        else:
            key, bpm, secs, seed = SONGS[nm]
            print(nm, round(ind_song(key, bpm, secs, seed), 1), flush=True)
