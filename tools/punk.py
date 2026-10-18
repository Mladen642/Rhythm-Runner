import math, random, sys
from PIL import Image
from songlib import *
from songs4 import song, M
from songs3 import loop_song
from anim import *
from stage_assets2 import magic, rgba, b64, L_scroll, L_static, W, frames_sheet
from new_art import rim, flash
from country import CT
HZ, PT, GY = 126, 180, 166


def punk_mel(chords, seed, up=12):
    rng = random.Random(seed)
    RH = [[4, 4, 4, 4], [2, 2, 4, 4, 4], [4, 2, 2, 8], [2, 2, 2, 2, 4, 4], [6, 2, 4, 4]]
    out = []
    for ch in chords:
        tones = CT[ch]; rh = rng.choice(RH); pos = 0; notes = []
        for i, ln in enumerate(rh):
            idx = rng.choice([0, 0, 2, 1, 2]) if i else 0
            notes.append((pos, ln, tones[idx] + up)); pos += ln
        out.append(notes)
    return out


def chant(chords, up=12):
    return [[(0, 4, CT[c][0] + up), (4, 4, CT[c][0] + up), (8, 4, CT[c][2] + up), (12, 4, CT[c][1] + up)] for c in chords]


def punk_song(name, bpm, plan, seed):
    secs = []
    for sec, chords, kind in plan:
        if kind == 'verse':
            secs.append((sec, chords, punk_mel(chords, seed + len(secs)), 'drive', {}))
        elif kind == 'chorus':
            secs.append((sec, chords, chant(chords), 'chorus', {'hey': True}))
        elif kind == 'intro':
            secs.append((sec, chords, None, 'riff', {}))
        elif kind == 'break':
            secs.append((sec, chords, None, 'half', {'hey': True}))
        else:
            secs.append((sec, chords, [[(0, 14, CT[c][0] + 12)] for c in chords], 'chorus', {'fills': False}))
    return song(name, bpm, secs, 'rock', None, seed)


P1 = ['E', 'A', 'D', 'A'] * 2; Q1 = ['A', 'D', 'E', 'E'] * 2
P2 = ['G', 'C', 'D', 'C'] * 2; Q2 = ['C', 'D', 'G', 'G'] * 2
P3 = ['A', 'D', 'E', 'D'] * 2; Q3 = ['D', 'E', 'A', 'A'] * 2
P4 = ['C', 'G', 'A', 'F'] * 2; Q4 = ['F', 'G', 'C', 'C'] * 2
P5 = ['Em', 'C', 'G', 'D'] * 2; Q5 = ['C', 'D', 'Em', 'Em'] * 2
SONGS = {
    'skate': ('c11_skate', 176, [('intro', P1[:4], 'intro'), ('verse', P1, 'verse'), ('chorus', Q1, 'chorus'), ('verse', P1, 'verse'), ('chorus', Q1, 'chorus'), ('chorus', Q1, 'chorus'), ('outro', ['A', 'D', 'E', 'E'], 'outro')], 1101),
    'basement': ('c11_basement', 184, [('intro', P2[:4], 'intro'), ('verse', P2, 'verse'), ('chorus', Q2, 'chorus'), ('verse', P2, 'verse'), ('chorus', Q2, 'chorus'), ('chorus', Q2, 'chorus'), ('outro', ['C', 'D', 'G', 'G'], 'outro')], 1102),
    'mall': ('c11_mall', 188, [('intro', P3[:4], 'intro'), ('verse', P3, 'verse'), ('chorus', Q3, 'chorus'), ('breakdown', P3, 'break'), ('chorus', Q3, 'chorus'), ('chorus', Q3, 'chorus'), ('outro', ['D', 'E', 'A', 'A'], 'outro')], 1103),
    'junkyard': ('c11_junkyard', 192, [('intro', P4[:4], 'intro'), ('verse', P4, 'verse'), ('chorus', Q4, 'chorus'), ('verse', P4, 'verse'), ('chorus', Q4, 'chorus'), ('chorus_last', Q4, 'chorus'), ('outro', ['F', 'G', 'C', 'C'], 'outro')], 1104),
    'ceo': ('c11_ceo', 196, [('intro', ['Em'] * 4, 'intro'), ('verse', P5, 'verse'), ('chorus', Q5, 'chorus'), ('verse_rev', P5, 'verse'), ('chorus_cor', Q5, 'chorus'),
                             ('verse', P5, 'verse'), ('finale', ['Em', 'Em', 'C', 'C', 'G', 'G', 'D', 'D'], 'break'), ('outro', ['C', 'D', 'Em', 'Em'], 'outro')], 1105),
}


def pause_punk():
    m = M('E5:8 B4:8', 'A4:8 E5:8', 'D5:8 A4:8', 'B4:14')
    return loop_song('c11_pause', 100, ['Em', 'C', 'G', 'D'], m, 4, 1106, soft=True)


# ======================= art =======================
def spike(c, x, gy, f, pose='run'):
    p = f / 8 * 2 * math.pi
    bob = 1 if (pose == 'run' and f % 4 in (1, 2)) or (pose != 'run' and f % 2) else 0
    hip = (x, gy - 13 + bob)
    for side, ph in ((0, p), (1, p + math.pi)):
        if pose == 'run':
            fx = x + 6 * math.sin(ph); fy = gy - max(0, 3 * math.cos(ph)); kx = (hip[0] + fx) / 2 + 2 + 2 * math.sin(ph); ky = (hip[1] + fy) / 2
        else:
            fx = x - 3 + side * 6; fy = gy; kx = fx; ky = gy - 7
        c.line([hip, (kx, ky), (fx, fy - 3)], K, 5); c.line([hip, (kx, ky), (fx, fy - 3)], '#3a4a6a' if side == 0 else '#4a5a8a', 3)
        c.p(kx, ky, '#f2b98c'); c.r(fx - 2, fy - 5, 6, 5, K); c.r(fx - 1, fy - 4, 4, 3, '#1b1030'); c.r(fx - 1, fy - 1, 5, 1, '#c8ccd8')
    ty = gy - 26 + bob
    c.r(x - 5, ty, 11, 14, K); c.r(x - 4, ty + 1, 9, 12, '#1b1424'); c.r(x - 1, ty + 1, 3, 12, '#c2260f')
    for k in range(4):
        c.p(x - 3 + (k % 2) * 7, ty + 2 + k * 3, '#c8ccd8')
    c.line([(x - 3, ty + 2), (x - 6, ty + 9)], K, 4); c.line([(x - 3, ty + 2), (x - 6, ty + 9)], '#1b1424', 2)
    hy = ty - 10
    c.r(x - 4, hy, 10, 10, K); c.r(x - 3, hy + 1, 8, 8, '#f2b98c'); c.p(x + 2, hy + 4, K); c.r(x + 1, hy + 3, 3, 1, '#1b1030'); c.r(x + 1, hy + 7, 3, 1, '#8a2a2a'); c.p(x + 4, hy + 5, '#c8ccd8')
    for k in range(5):
        c.r(x - 3 + k * 2, hy - 2 - (4 - abs(k - 2)) * 2, 2, 3 + (4 - abs(k - 2)) * 2, '#7cf06a'); c.p(x - 3 + k * 2, hy - 2 - (4 - abs(k - 2)) * 2, '#3a8a2a')
    c.poly([(x + 2, ty + 2), (x + 18, ty - 6), (x + 19, ty - 3), (x + 4, ty + 6)], '#3a3a48', None); c.r(x + 2, ty + 4, 8, 8, K); c.r(x + 3, ty + 5, 6, 6, '#e8344e')
    c.r(x + 17, ty - 8, 4, 4, K); c.line([(x + 3, ty + 3), (x + 8, ty + 6)], K, 3); c.line([(x + 3, ty + 3), (x + 8, ty + 6)], '#f2b98c', 1)
    return (19, ty - 6 - gy, 7, ty + 8 - gy)


def spike_sheet():
    cw, ch, ax, ay, n = 44, 50, 16, 48, 8
    sheet = Image.new('RGBA', (cw * n, ch)); tips = []
    for f in range(n):
        c = magic(64); t = spike(c, ax, ay, f); sheet.paste(rgba(c.im, (0, 0, cw, ch)), (f * cw, 0)); tips.append(list(t))
    return {'src': b64(sheet), 'n': n, 'cw': cw, 'ch': ch, 'ax': ax, 'ay': ay, 'fps': 13, 'x': 38, 'tips': tips}


def e_drone(c):
    c.r(10, 9, 12, 7, K); c.r(11, 10, 10, 5, '#3a3a48'); c.disc(16, 12, 2, '#ff3b3b'); c.r(4, 6, 8, 1, '#8a8a98'); c.r(20, 6, 8, 1, '#8a8a98')
    c.r(7, 7, 2, 3, K); c.r(23, 7, 2, 3, K); text(c, 'SEC', 9, 16, '#ffe066', 1, None)


def e_briefcase(c):
    c.r(7, 8, 18, 12, K); c.r(8, 9, 16, 10, '#5a3418'); c.r(13, 5, 6, 4, K); c.r(14, 6, 4, 2, '#5a3418')
    c.r(11, 11, 3, 2, '#f4f4f4'); c.r(18, 11, 3, 2, '#f4f4f4'); c.p(12, 12, K); c.p(19, 12, K); c.r(12, 15, 8, 1, K)
    c.poly([(7, 12), (1, 8), (4, 15)], '#f4f4f4', None); c.poly([(25, 12), (31, 8), (28, 15)], '#f4f4f4', None); c.r(15, 16, 2, 2, '#ffd23f')


def e_cone(c):
    c.poly([(10, 22), (16, 3), (22, 22)], '#ff7a1a', None); c.line([(10, 22), (16, 3), (22, 22), (10, 22)], K)
    c.r(12, 11, 9, 2, '#f4f4f4'); c.r(11, 17, 11, 2, '#f4f4f4'); c.r(8, 21, 16, 2, K)
    c.p(14, 8, K); c.p(18, 8, K); c.r(14, 14, 4, 1, K)


def enemies_sheet():
    out = Image.new('RGBA', (32 * 6, 24))
    for l, (fn, col) in enumerate(((e_drone, '#5ef2ff'), (e_briefcase, '#ff4fa3'), (e_cone, '#ffe066'))):
        c = magic(64); fn(c); im = rim(rgba(c.im, (0, 0, 32, 24)), col)
        out.paste(im, (l * 64, 0)); out.paste(flash(im), (l * 64 + 32, 0))
    return {'src': b64(out), 'anch': [[16, 12], [16, 12], [16, 23]]}


def notes_sheet():
    out = Image.new('RGBA', (40, 20))
    c = magic(64); c.line([(4, 14), (15, 4)], '#c8ccd8', 2); c.disc(4, 15, 2, K); c.line([(5, 15), (16, 6), (14, 3)], '#c8ccd8', 1); c.r(13, 2, 4, 3, '#ffd23f')
    out.paste(rgba(c.im, (0, 0, 20, 20)), (0, 0))
    c = magic(64)
    for k in range(5):
        a = -math.pi / 2 + k * 2 * math.pi / 5; c.line([(10, 10), (10 + 8 * math.cos(a), 10 + 8 * math.sin(a))], '#7cf06a', 2)
    c.disc(10, 10, 3, '#7cf06a')
    out.paste(rgba(c.im, (0, 0, 20, 20)), (20, 0))
    return b64(out)


def cart(c, x, gy, f):
    c.r(x, gy - 22, 44, 14, K); c.r(x + 1, gy - 21, 42, 12, '#8a8a98')
    for k in range(6):
        c.r(x + 3 + k * 7, gy - 21, 1, 12, '#5a5a6a')
    c.line([(x + 44, gy - 22), (x + 52, gy - 30)], K, 2)
    for wx in (x + 6, x + 38):
        c.disc(wx, gy - 3, 3, K); c.disc(wx, gy - 3, 1, '#c8ccd8')
    c.r(x + 4, gy - 9, 36, 2, '#5a5a6a')
    for i, (hair, shirt) in enumerate((('#7cf06a', '#1b1424'), ('#ff4fa3', '#c2260f'), ('#5ef2ff', '#3a3a48'))):
        px = x + 8 + i * 13; bob = (f + i) % 2
        c.r(px - 3, gy - 32 - bob, 7, 11, K); c.r(px - 2, gy - 31 - bob, 5, 9, shirt)
        c.r(px - 3, gy - 39 - bob, 7, 7, K); c.r(px - 2, gy - 38 - bob, 5, 5, '#f2b98c')
        for k in range(3):
            c.r(px - 2 + k * 2, gy - 43 - bob - (1 - abs(k - 1)) * 2, 1, 4 + (1 - abs(k - 1)) * 2, hair)
        c.line([(px + 2, gy - 30 - bob), (px + 6, gy - 40 - bob - (f + i) % 3)], K, 2)


def cart_buddy():
    cw, ch, n = 60, 48, 4
    sheet = Image.new('RGBA', (cw * n, ch))
    for f in range(n):
        c = magic(64); cart(c, 2, ch - 1, f); sheet.paste(rgba(c.im, (0, 0, cw, ch)), (f * cw, 0))
    return {'kind': 'sweep', 'name': 'THE CART CREW', 'sfx': 'cart', 'say': 'OI OI OI!', 'pitch': 0.8, 'rate': 1.3, 'speed': 210,
            'src': b64(sheet), 'n': n, 'cw': cw, 'ch': ch, 'ox': 10, 'oy': ch - 1, 'front': 54, 'bolts': False}


def mall_cop(c, x, gy):
    c.r(x - 20, gy - 6, 40, 4, K); c.disc(x - 14, gy - 3, 4, K); c.disc(x + 14, gy - 3, 4, K); c.r(x - 2, gy - 30, 4, 26, '#3a3a48')
    c.r(x - 16, gy - 64, 32, 34, K); c.r(x - 15, gy - 63, 30, 32, '#5a6aa8'); c.r(x - 4, gy - 60, 8, 6, '#ffd23f'); text(c, 'COP', x - 9, gy - 50, '#ffffff', 1, None)
    c.r(x - 10, gy - 78, 20, 14, K); c.r(x - 9, gy - 77, 18, 12, '#8a8a98'); c.r(x - 7, gy - 73, 14, 3, '#ff3b3b')
    c.r(x - 12, gy - 82, 24, 5, K); c.r(x - 11, gy - 81, 22, 3, '#2a3a6a')
    c.line([(x + 16, gy - 56), (x + 26, gy - 44)], K, 4); c.r(x + 24, gy - 46, 4, 14, '#1b1030')


def ceo(c, x, gy):
    x0 = x
    c.r(x0, gy - 80, 80, 74, K); c.r(x0 + 1, gy - 79, 78, 72, '#2a2a38')
    c.poly([(x0 + 30, gy - 79), (x0 + 40, gy - 50), (x0 + 50, gy - 79)], '#f4f4f4', None); c.poly([(x0 + 37, gy - 79), (x0 + 40, gy - 54), (x0 + 43, gy - 79)], '#c2260f', None)
    c.r(x0 + 20, gy - 112, 40, 34, K); c.r(x0 + 21, gy - 111, 38, 32, '#8a8a98')
    c.r(x0 + 25, gy - 102, 12, 6, '#ffd23f'); c.r(x0 + 43, gy - 102, 12, 6, '#ffd23f'); text(c, 'S', x0 + 28, gy - 103, K, 1, None); text(c, 'S', x0 + 46, gy - 103, K, 1, None)
    c.r(x0 + 28, gy - 90, 24, 3, K); c.r(x0 + 18, gy - 116, 44, 5, K); c.r(x0 + 24, gy - 126, 32, 10, K); c.r(x0 + 25, gy - 125, 30, 8, '#1b1424')
    c.r(x0 - 10, gy - 60, 12, 30, K); c.r(x0 - 9, gy - 59, 10, 28, '#2a2a38'); c.r(x0 - 26, gy - 34, 26, 18, K); c.r(x0 - 25, gy - 33, 24, 16, '#5a3418'); c.r(x0 - 16, gy - 38, 8, 4, K)
    for k in range(4):
        c.r(x0 + 6 + k * 18, gy - 40, 12, 6, '#3a7a3a'); text(c, 'S', x0 + 9 + k * 18, gy - 40, '#7cf06a', 1, None)
    text(c, 'CEO', x0 + 31, gy - 70, '#ffd23f', 1, None)
    c.r(x0 + 10, gy - 6, 22, 6, K); c.r(x0 + 48, gy - 6, 22, 6, K)


def intro_punk(c, f):
    c.r(122, GY - 4, 30, 4, K); c.r(123, GY - 3, 28, 2, '#c2260f'); c.disc(126, GY - 1, 2, '#f4f4f4'); c.disc(148, GY - 1, 2, '#f4f4f4')
    c.r(170, GY - 26, 18, 26, K); c.r(171, GY - 25, 16, 24, '#5a5a6a')
    for k in range(3):
        c.r(173 + k * 5, GY - 22, 1, 20, '#3a3a48')
    h = 8 + (f % 3) * 3
    c.poly([(172, GY - 26), (176, GY - 26 - h), (179, GY - 30), (182, GY - 26 - h - 2), (186, GY - 26)], '#ff5a1f', None)
    spike(c, 145, GY - 4, f, pose='idle')
    if f % 8 in (2, 3):
        text(c, 'OI!', 132, GY - 64, '#7cf06a', 2, K)


def props_punk(c):
    c.r(170, GY - 26, 18, 26, K); c.r(171, GY - 25, 16, 24, '#5a5a6a')
    c.poly([(172, GY - 26), (176, GY - 34), (179, GY - 30), (182, GY - 36), (186, GY - 26)], '#ff5a1f', None)


def punk_world(P):
    far = Cv()
    sky(far, 0, HZ, P['sky'])
    r = random.Random(P['seed'])
    if P.get('skyline'):
        x = 0
        while x < W:
            w = r.randrange(20, 40); h = r.randrange(40, 96)
            far.r(x, HZ - h, w, h, P['skyline'])
            for wy in range(HZ - h + 4, HZ - 4, 6):
                for wx in range(x + 3, x + w - 3, 5):
                    if r.random() < 0.3:
                        far.r(wx, wy, 2, 3, '#ffd23f' if not P.get('corp') else '#9af8ff')
            x += w + 1
    if P.get('wall'):
        far.r(0, 24, W, HZ - 24, P['wall'])
        for y in range(24, HZ, 8):
            for x in range((y // 8 % 2) * 8, W, 16):
                far.r(x, y, 15, 1, P['wall_d']); far.r(x, y, 1, 8, P['wall_d'])
    if P.get('posters'):
        for px in range(10, W, 50):
            col = r.choice(['#ff4fa3', '#ffe066', '#7cf06a', '#5ef2ff', '#f4f4f4'])
            far.r(px, 40 + r.randrange(20), 30, 40, col); far.r(px + 4, 46 + r.randrange(20), 22, 4, K); text(far, r.choice(['OI', 'RIOT', 'NOISE', 'GIG']), px + 4, 60 + r.randrange(10), K, 1, None)
    if P.get('mall'):
        for sx in range(0, W, 64):
            far.r(sx + 4, 40, 56, 60, K); far.r(sx + 5, 41, 54, 58, '#c8d8f0'); far.r(sx + 5, 41, 54, 10, r.choice(['#ff4fa3', '#5ef2ff', '#ffe066']))
            text(far, r.choice(['SALE', 'SHOE', 'TOYS', 'FOOD']), sx + 18, 43, K, 1, None)
    L = [L_static(far, 0, HZ)]
    st = magic(640)
    if P.get('ramps'):
        for x in range(20, 640, 160):
            st.poly([(x, HZ), (x + 40, HZ - 26), (x + 40, HZ)], '#8a8a98', None); st.line([(x, HZ), (x + 40, HZ - 26)], '#c8ccd8', 2)
        for x in range(0, 640, 4):
            for y in range(HZ - 40, HZ - 26, 4):
                st.p(x + (y // 4 % 2) * 2, y, '#5a5a6a')
    if P.get('crowd'):
        for x in range(0, 640, 7):
            h = 8 + (x * 13) % 6
            st.disc(x + 3, HZ - h - 2, 2, '#0a0610'); st.r(x + 1, HZ - h, 5, h, '#0a0610')
            if (x // 7) % 3 == 0:
                st.r(x + 1, HZ - h - 9, 1, 7, '#0a0610')
    if P.get('junk'):
        for x in range(10, 640, 70):
            for k in range(3):
                st.r(x, HZ - 12 - k * 10, 50, 10, K); st.r(x + 1, HZ - 11 - k * 10, 48, 8, r.choice(['#8a3a2a', '#3a5a8a', '#6a6a3a']))
                st.r(x + 6, HZ - 9 - k * 10, 10, 4, '#2a2a38')
        for x in range(50, 640, 140):
            st.r(x, HZ - 18, 12, 18, '#3a3a48'); st.disc(x + 6, HZ - 22, 4, '#ff7a1a')
    L.append(L_scroll(st, HZ - 50, HZ + 2, 25))
    gd = magic(640)
    gd.r(0, HZ, 640, PT - HZ, P['ground']); gd.r(0, HZ, 640, 1, P['edge'])
    for _ in range(260):
        sp(gd, r.randrange(640), r.randrange(HZ + 2, PT), P['dot'])
    if P.get('tags'):
        for x in range(20, 640, 100):
            gd.line([(x, HZ + 20), (x + 20, HZ + 12), (x + 40, HZ + 24)], r.choice(['#ff4fa3', '#7cf06a', '#5ef2ff']), 2)
    if P.get('tiles'):
        for x in range(0, 640, 20):
            gd.r(x, HZ, 1, PT - HZ, P['dot'])
    L.append(L_scroll(gd, HZ, PT, 55, transparent=False))
    return L


PUNK_V = [lambda: punk_world(dict(sky=['#0a0608', '#120a0e'], seed=1112, wall='#2a1a22', wall_d='#1a0a12', posters=True, crowd=True, ground='#1a1418', edge='#c2260f', dot='#2a2228')),
          lambda: punk_world(dict(sky=['#e8e0d0', '#f4f0e8'], seed=1113, mall=True, ground='#c8c0b0', edge='#8a8a98', dot='#b0a898', tiles=True)),
          lambda: punk_world(dict(sky=['#3a1a1a', '#5a2a1a', '#8a3a1a', '#b85a2a'], seed=1114, skyline='#1a0a0a', junk=True, ground='#3a2a1a', edge='#5a3a2a', dot='#2a1a10')),
          lambda: punk_world(dict(sky=['#0a1a2a', '#14304a', '#1e4a6a', '#2a6a8a'], seed=1115, skyline='#0a141e', corp=True, ground='#3a4a5a', edge='#9af8ff', dot='#2a3a4a', tiles=True))]


def punk_base():
    layers = punk_world(dict(sky=['#2a1a3a', '#4a2a4a', '#6a3a4a', '#8a4a4a'], seed=1111, skyline='#1a0e1e', ramps=True, ground='#5a5a6a', edge='#8a8a98', dot='#4a4a58', tags=True))
    fs = frames_sheet(lambda c, f: intro_punk(c, f), 8, (0, 0)); fs.pop('extra', None)
    c = magic(); props_punk(c); box = rgba(c.im).getbbox()
    fs['props'] = {'src': b64(rgba(c.im, box)), 'x': box[0], 'y': box[1]}
    return {'id': '11-1', 'layers': layers, 'hero': spike_sheet(), 'enemies': enemies_sheet(), 'notes': notes_sheet(), 'buddy': cart_buddy(), 'intro': fs}


if __name__ == '__main__':
    for nm in sys.argv[1:]:
        if nm == 'pause':
            print(nm, round(pause_punk(), 1))
        else:
            key, bpm, plan, seed = SONGS[nm]
            print(nm, round(punk_song(key, bpm, plan, seed), 1), flush=True)
