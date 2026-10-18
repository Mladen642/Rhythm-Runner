import math, random
import numpy as np
from PIL import Image
from anim import *
from stage_assets2 import magic, rgba, b64, L_scroll, L_static, W, frames_sheet
from gen3a import batswarm, fog
HZ, PT, GY = 126, 180, 166


def stars(c, n, seed, y1, col='#b8b4d4'):
    r = random.Random(seed)
    for _ in range(n):
        c.p(r.randrange(W), r.randrange(26, y1), '#ffffff' if r.random() < .4 else col)


# ======================= goth worlds =======================
def goth_world(P):
    far = Cv()
    sky(far, 0, HZ, P['sky'])
    r = random.Random(P.get('seed', 4))
    stars(far, P.get('stars', 40), P.get('seed', 4), HZ - 30, '#6a5a8a')
    mx, my, mr, mc = P.get('moon', (246, 50, 16, '#e8e6f4'))
    for a in range(0, 360, 8):
        far.p(mx + (mr + 5) * math.cos(math.radians(a)), my + (mr + 5) * math.sin(math.radians(a)), '#4a3a6e')
    far.disc(mx, my, mr, mc); far.disc(mx - 6, my - 5, 3, '#c8c4dc' if mc == '#e8e6f4' else '#a3200f')
    cs = P.get('sil', '#0a0612')
    if P.get('cathedral'):
        far.r(60, HZ - 60, 110, 60, cs)
        for sx in (60, 158):
            far.r(sx, HZ - 84, 14, 84, cs); far.poly([(sx, HZ - 84), (sx + 7, HZ - 108), (sx + 14, HZ - 84)], cs, None)
        far.poly([(100, HZ - 60), (115, HZ - 92), (130, HZ - 60)], cs, None)
        far.disc(115, HZ - 44, 11, '#2a0a3a')
        for k in range(8):
            a = k * math.pi / 4
            far.line([(115, HZ - 44), (115 + 10 * math.cos(a), HZ - 44 + 10 * math.sin(a))], ['#ff3b6b', '#5ef2ff', '#ffd23f', '#b06bff'][k % 4])
        far.disc(115, HZ - 44, 3, '#ffe066')
        for wx in (80, 92, 138, 150):
            far.r(wx, HZ - 34, 5, 14, '#2a0a3a'); far.r(wx + 1, HZ - 33, 3, 6, ['#b06bff', '#ff3b6b'][wx % 2]); far.r(wx + 1, HZ - 27, 3, 6, '#5ef2ff')
    if P.get('crypts'):
        for cx in (30, 120, 210, 280):
            far.r(cx, HZ - 22, 26, 22, cs); far.poly([(cx - 2, HZ - 22), (cx + 13, HZ - 32), (cx + 28, HZ - 22)], cs, None)
            far.r(cx + 10, HZ - 14, 6, 14, '#05030a'); far.r(cx + 12, HZ - 36, 2, 6, cs); far.r(cx + 10, HZ - 34, 6, 2, cs)
    if P.get('manor'):
        far.r(120, HZ - 56, 120, 56, cs); far.poly([(116, HZ - 56), (180, HZ - 84), (244, HZ - 56)], cs, None)
        far.r(140, HZ - 76, 10, 20, cs); far.r(210, HZ - 72, 10, 16, cs)
        for wx in range(132, 236, 16):
            for wy in (HZ - 46, HZ - 26):
                lit = r.random() < 0.45
                far.r(wx, wy, 6, 9, '#ffb02e' if lit else '#1b1424'); far.r(wx + 2, wy, 1, 9, cs)
    if P.get('ballroom'):
        far.r(0, 24, W, HZ - 24, '#1a0610')
        for wx in (40, 140, 240):
            far.r(wx, 40, 40, 70, '#05030a'); far.disc(wx + 20, 40, 20, '#05030a', ymax=40)
            far.r(wx + 2, 42, 36, 66, '#14102a'); far.disc(wx + 20, 60, 9, '#e8e6f4' if wx != 140 else '#c2260f')
            far.r(wx + 19, 42, 2, 66, '#05030a'); far.r(wx + 2, 74, 36, 2, '#05030a')
            for k in range(6):
                far.r(wx - 8 + (k % 2), 30 + k * 14, 8, 14, '#8a0a1e' if k % 2 else '#a3102a')
                far.r(wx + 40 + (k % 2), 30 + k * 14, 8, 14, '#8a0a1e' if k % 2 else '#a3102a')
    far.r(0, HZ, W, PT - HZ, P.get('ground', '#120d1c')); far.r(0, HZ, W, 1, '#2a2238')
    layers = [L_static(far, 0, PT)]
    if P.get('chandeliers'):
        ch = magic(640)
        for cx in (80, 300, 520):
            ch.line([(cx, 24), (cx, 40)], '#5a4a30'); ch.r(cx - 16, 40, 33, 3, '#c98a1a')
            for k in range(5):
                ch.r(cx - 16 + k * 8, 34, 1, 6, '#f4f0e0'); ch.p(cx - 16 + k * 8, 33, '#ffe066')
        layers.append(L_scroll(ch, 24, 48, 18))
    if P.get('bats'):
        bt = magic(640); batswarm(bt, 120, 14, 10, 2); batswarm(bt, 430, 18, 8, 3)
        layers.append(L_scroll(bt, 0, 30, 30) | {'y': 34})
    gr = magic(640)
    for _ in range(140):
        sp(gr, r.randrange(640), r.randrange(HZ + 2, PT), P.get('ground_dot', '#2a2238'))
    if P.get('carpet'):
        gr.r(0, HZ + 18, 640, 26, '#5a0a18'); gr.r(0, HZ + 18, 640, 1, '#c98a1a'); gr.r(0, HZ + 43, 640, 1, '#c98a1a')
    layers.append(L_scroll(gr, HZ + 2, PT, 50))
    if P.get('fence', True):
        fe = magic(640)
        for x in range(0, 640, 8):
            fe.r(x, HZ - 10, 1, 10, '#1b1428'); sp(fe, x, HZ - 11, '#3a3050')
        fe.r(0, HZ - 8, 640, 1, '#1b1428'); fe.r(0, HZ - 3, 640, 1, '#1b1428')
        for gx in range(12, 640, 40):
            if r.random() < .5:
                fe.r(gx, HZ - 6, 7, 9, K); fe.r(gx + 1, HZ - 5, 5, 8, '#3a3448'); fe.r(gx + 1, HZ - 5, 5, 1, '#5a5470')
            else:
                fe.r(gx + 2, HZ - 9, 3, 12, '#3a3448'); fe.r(gx, HZ - 6, 7, 3, '#3a3448')
        layers.append(L_scroll(fe, HZ - 12, HZ + 4, 25))
    if P.get('fog', True):
        fg = magic(640)
        for y in range(HZ - 8, HZ + 9):
            for x in range(640):
                if (x * 7 + y * 13) % 15 == 0:
                    sp(fg, x, y, P.get('fogc', '#8a84a8'))
        layers.append(L_scroll(fg, HZ - 8, HZ + 9, 12))
    return layers


GOTH_V = [
    dict(sky=['#05030c', '#0d0820', '#160d30', '#201240', '#2a1650'], cathedral=True, stars=60, seed=41),
    dict(sky=['#040806', '#081210', '#0c1a16', '#10221c', '#142a22'], crypts=True, moon=(70, 46, 14, '#d8f0d8'), fogc='#6a8a7a', seed=42, stars=30),
    dict(sky=['#06060a', '#0e0e16', '#161622', '#1e1e2e', '#26263a'], manor=True, stars=0, moon=(260, 40, 12, '#c8c8d8'), seed=43),
    dict(sky=['#0a0204', '#160408', '#22060c'], ballroom=True, chandeliers=True, fence=False, fog=False, carpet=True, ground='#1a0a10', ground_dot='#3a1020',
         moon=(160, 60, 0, '#c2260f'), stars=0, seed=44),
]


# ======================= chapter 5 art =======================
SKIN, SKIN_D = '#6b4226', '#4a2c18'
JEANS, JEANS_D = '#3a5a9a', '#2a4270'
CAP, CAP_D = '#e8344e', '#9e1c35'


def mc(c, x, gy, f, pose='run', pal=None):
    pal = pal or {}
    skin, skin_d = pal.get('skin', SKIN), pal.get('skin_d', SKIN_D)
    shirt, shirt_d = pal.get('shirt', '#f4f4f4'), pal.get('shirt_d', '#c8c8d8')
    cap, cap_d = pal.get('cap', CAP), pal.get('cap_d', CAP_D)
    jeans, jeans_d = pal.get('jeans', JEANS), pal.get('jeans_d', JEANS_D)
    p = f / 8 * 2 * math.pi
    bob = 1 if (pose == 'run' and f % 4 in (1, 2)) or (pose != 'run' and f % 2) else 0
    hip = (x, gy - 13 + bob)
    legs = []
    if pose == 'run':
        for side, ph in ((0, p), (1, p + math.pi)):
            fx = x + 6 * math.sin(ph); fy = gy - max(0, 3 * math.cos(ph))
            kx = (hip[0] + fx) / 2 + 2 + 2 * math.sin(ph); ky = (hip[1] + fy) / 2
            legs.append((side, fx, fy, kx, ky))
    else:
        legs = [(0, x - 3, gy, x - 3, gy - 6), (1, x + 3, gy, x + 3, gy - 6)]
    for side, fx, fy, kx, ky in legs:
        col = jeans_d if side == 0 else jeans
        c.line([hip, (kx, ky), (fx, fy - 2)], K, 6); c.line([hip, (kx, ky), (fx, fy - 2)], col, 4)
        c.r(fx - 2, fy - 3, 7, 3, K); c.r(fx - 1, fy - 2, 6, 1, '#f4f4f4'); c.p(fx + 4, fy - 2, '#e8344e')
    ty = gy - 26 + bob
    if pose == 'run':
        bh = (x - 4 - 3 * math.sin(p), ty + 10)
    else:
        bh = (x - 6, ty + 4 - (f % 4) * 2)
    c.line([(x - 3, ty + 2), bh], K, 4); c.line([(x - 3, ty + 2), bh], skin_d, 2)
    c.r(x - 5, ty, 11, 14, K); c.r(x - 4, ty + 1, 9, 12, shirt); c.r(x + 3, ty + 1, 2, 12, shirt_d)
    c.r(x - 4, ty + 1, 2, 2, skin); c.r(x + 3, ty + 1, 2, 2, skin)
    c.r(x - 2, ty + 2, 5, 1, '#ffd23f'); c.p(x, ty + 3, '#ffd23f')
    c.r(x - 4, ty + 12, 9, 2, '#1b1030')
    if pose == 'run':
        hand, mic_h = (x + 10, ty + 5), (x + 12, ty + 1)
        c.line([(x + 3, ty + 2), (x + 7, ty + 7), hand], K, 4); c.line([(x + 3, ty + 2), (x + 7, ty + 7), hand], skin, 2)
    else:
        hand, mic_h = (x + 5, ty - 2), (x + 6, ty - 5)
        c.line([(x + 3, ty + 2), (x + 7, ty + 4), hand], K, 4); c.line([(x + 3, ty + 2), (x + 7, ty + 4), hand], skin, 2)
    c.r(hand[0] - 1, hand[1] - 4, 3, 6, K); c.r(hand[0], hand[1] - 3, 1, 4, '#3a3550')
    c.disc(mic_h[0], mic_h[1], 3, K); c.disc(mic_h[0], mic_h[1], 2, '#c8ccd8'); c.p(mic_h[0] - 1, mic_h[1] - 1, '#ffffff')
    hy = ty - 11
    c.r(x - 4, hy, 10, 11, K); c.r(x - 3, hy + 1, 8, 9, skin); c.r(x - 3, hy + 8, 8, 2, skin_d)
    c.p(x + 2, hy + 4, '#ffffff'); c.p(x + 3, hy + 4, K); c.r(x + 1, hy + 3, 3, 1, '#1b1030')
    c.r(x + 2, hy + 7, 3, 1, '#2a1610'); c.p(x - 2, hy + 4, skin_d); c.p(x - 2, hy + 5, skin_d)
    c.r(x - 4, hy - 2, 10, 5, K); c.r(x - 3, hy - 1, 8, 3, cap); c.p(x + 1, hy - 2, cap_d); c.r(x + 3, hy, 2, 1, '#ffffff')
    c.r(x - 9, hy + 1, 6, 3, K); c.r(x - 8, hy + 2, 5, 1, cap_d)
    return (mic_h[0] - x, mic_h[1] - gy, hand[0] - x, hand[1] - gy)


def mc_sheet():
    cw, ch, ax, ay, n = 40, 46, 16, 44, 8
    sheet = Image.new('RGBA', (cw * n, ch))
    tips = []
    for f in range(n):
        c = magic(64); t = mc(c, ax, ay, f)
        sheet.paste(rgba(c.im, (0, 0, cw, ch)), (f * cw, 0)); tips.append(list(t))
    return {'src': b64(sheet), 'n': n, 'cw': cw, 'ch': ch, 'ax': ax, 'ay': ay, 'fps': 11, 'x': 38, 'tips': tips}


def rim(img, col):
    a = np.array(img); m = a[:, :, 3] > 0
    edge = np.zeros_like(m)
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        edge |= np.roll(np.roll(m, dy, 0), dx, 1)
    edge &= ~m
    out = a.copy(); c = C(col); out[edge, 0], out[edge, 1], out[edge, 2], out[edge, 3] = c[0], c[1], c[2], 255
    return Image.fromarray(out, 'RGBA')


def flash(img):
    a = np.array(img).astype(float); m = a[:, :, 3] > 0; a[m, :3] = a[m, :3] * 0.3 + 255 * 0.7
    return Image.fromarray(a.astype('uint8'), 'RGBA')


def enemy_spray(c):
    c.r(11, 5, 10, 15, K); c.r(12, 6, 8, 13, '#e8344e'); c.r(12, 10, 8, 4, '#f4f4f4'); c.r(14, 3, 4, 3, K); c.r(15, 2, 2, 2, '#c8ccd8')
    c.r(14, 8, 1, 1, K); c.r(17, 8, 1, 1, K); c.line([(13, 7), (15, 8)], K); c.line([(19, 7), (17, 8)], K)
    c.r(4, 4, 7, 1, '#c8ccd8'); c.r(21, 4, 7, 1, '#c8ccd8'); c.r(15, 0, 2, 2, '#c8ccd8')
    for k in range(3):
        c.p(22 + k * 2, 13 + k, '#ff7ac8')


def enemy_pigeon(c):
    c.disc(15, 13, 6, K); c.disc(15, 13, 5, '#8a8a98'); c.disc(21, 9, 4, K); c.disc(21, 9, 3, '#a8a8b8')
    c.p(22, 8, '#ff3b3b'); c.r(24, 9, 3, 2, '#ff9e3d'); c.r(18, 5, 6, 2, '#5ef2ff'); c.r(17, 6, 1, 4, '#1b1030'); c.r(24, 6, 1, 4, '#1b1030')
    c.poly([(9, 10), (2, 5), (12, 14)], '#6a6a78', None); c.r(10, 15, 6, 2, '#5a8a6a'); c.r(13, 19, 1, 3, '#ff9e3d'); c.r(17, 19, 1, 3, '#ff9e3d')


def enemy_trash(c):
    c.r(8, 8, 16, 15, K); c.r(9, 9, 14, 13, '#8a8a98')
    for x in (11, 15, 19):
        c.r(x, 10, 1, 11, '#6a6a78')
    c.r(6, 3, 20, 4, K); c.r(7, 4, 18, 2, '#a8a8b8'); c.r(14, 1, 4, 2, K)
    c.r(11, 7, 3, 2, '#ffe066'); c.r(18, 7, 3, 2, '#ffe066'); c.p(12, 7, K); c.p(19, 7, K)
    c.r(10, 22, 2, 2, K); c.r(20, 22, 2, 2, K); c.p(4, 12, '#5a8a3a'); c.r(3, 13, 3, 2, '#7a5a3a')


def enemies_sheet():
    out = Image.new('RGBA', (32 * 6, 24))
    for l, (fn, col) in enumerate(((enemy_spray, '#5ef2ff'), (enemy_pigeon, '#ff4fa3'), (enemy_trash, '#ffe066'))):
        c = magic(64); fn(c); im = rim(rgba(c.im, (0, 0, 32, 24)), col)
        out.paste(im, (l * 64, 0)); out.paste(flash(im), (l * 64 + 32, 0))
    return {'src': b64(out), 'anch': [[16, 12], [16, 12], [16, 23]]}


def notes_sheet():
    out = Image.new('RGBA', (40, 20))
    c = magic(64)
    c.disc(10, 6, 5, K); c.disc(10, 6, 4, '#c8ccd8'); c.p(8, 4, '#ffffff'); c.r(9, 10, 3, 8, K); c.r(10, 11, 1, 6, '#5a5670')
    out.paste(rgba(c.im, (0, 0, 20, 20)), (0, 0))
    c = magic(64)
    c.disc(10, 10, 8, K); c.disc(10, 10, 7, '#1b1424'); c.disc(10, 10, 3, '#ff3b3b'); c.p(10, 10, '#ffffff')
    for a in range(0, 360, 40):
        c.p(10 + 5 * math.cos(math.radians(a)), 10 + 5 * math.sin(math.radians(a)), '#3a3050')
    out.paste(rgba(c.im, (0, 0, 20, 20)), (20, 0))
    return b64(out)


def dj(c, x, gy, f):
    c.r(x - 12, gy - 6, 24, 6, K); c.r(x - 11, gy - 5, 22, 4, '#2a2238'); c.disc(x - 5, gy - 6, 4, K); c.disc(x - 5, gy - 6, 3, '#05030a')
    c.disc(x + 6, gy - 6, 4, K); c.disc(x + 6, gy - 6, 3, '#05030a'); c.p(x - 5 + (f % 2), gy - 7, '#ff3b3b')
    c.r(x - 6, gy - 22, 12, 15, K); c.r(x - 5, gy - 21, 10, 13, '#7a3cc8'); c.r(x - 1, gy - 21, 2, 8, '#5a2a8e')
    c.r(x - 5, gy - 32, 10, 10, K); c.r(x - 4, gy - 31, 8, 8, '#8a5a3a'); c.r(x - 4, gy - 28, 8, 2, K); c.r(x - 3, gy - 28, 2, 1, '#5ef2ff'); c.r(x + 1, gy - 28, 2, 1, '#5ef2ff')
    c.r(x - 2, gy - 25, 4, 1, '#3a1a10'); c.r(x - 6, gy - 32, 12, 2, '#1b1030'); c.r(x - 7, gy - 30, 2, 5, '#1b1030'); c.r(x + 5, gy - 30, 2, 5, '#1b1030')
    hx = x - 5 + [0, 3, 1, 4][f % 4]
    c.line([(x - 4, gy - 18), (hx, gy - 9)], K, 3); c.line([(x - 4, gy - 18), (hx, gy - 9)], '#8a5a3a', 1)
    c.line([(x + 4, gy - 18), (x + 8, gy - 12 - (f % 2) * 4)], K, 3); c.line([(x + 4, gy - 18), (x + 8, gy - 12 - (f % 2) * 4)], '#8a5a3a', 1)


def dj_buddy():
    cw, ch, n = 34, 36, 4
    sheet = Image.new('RGBA', (cw * n, ch))
    for f in range(n):
        c = magic(64); dj(c, cw // 2, ch - 1, f); sheet.paste(rgba(c.im, (0, 0, cw, ch)), (f * cw, 0))
    return {'kind': 'drop', 'name': 'DJ SUBWOOFER', 'sfx': 'dj', 'say': 'DROP THE BASS!', 'pitch': 0.8, 'rate': 1.1,
            'src': b64(sheet), 'n': n, 'cw': cw, 'ch': ch, 'ox': cw // 2, 'oy': ch - 1}


def stoop(c, x, gy):
    c.r(x, gy - 6, 44, 6, '#8a4a3a'); c.r(x + 10, gy - 12, 34, 6, '#9a5a4a'); c.r(x + 20, gy - 18, 24, 6, '#aa6a5a')
    for k in range(3):
        c.r(x + k * 10, gy - 6 - k * 6, 44 - k * 10, 1, '#c88a7a')
    c.r(x + 44, gy - 60, 3, 60, '#4a2a20'); c.r(x + 47, gy - 60, 30, 60, '#7a3a2a')
    for wy in range(gy - 54, gy - 10, 8):
        for wx in range(x + 50, x + 76, 6):
            c.r(wx, wy, 4, 1, '#5a2a20')


def boombox_small(c, x, y, f):
    c.r(x, y - 12, 26, 12, K); c.r(x + 1, y - 11, 24, 10, '#c8ccd8'); s = 1 + f % 2
    c.disc(x + 6, y - 6, 3 + s // 2, K); c.disc(x + 20, y - 6, 3 + s // 2, K); c.disc(x + 6, y - 6, 1, '#ff4fa3'); c.disc(x + 20, y - 6, 1, '#ff4fa3')
    c.r(x + 10, y - 10, 6, 3, '#5ef2ff'); c.r(x + 4, y - 15, 18, 2, K)


def intro_rap(c, f):
    stoop(c, 140, GY)
    boombox_small(c, 158, GY - 18, f)
    mc(c, 120, GY, f, pose='idle')
    friend = {'skin': '#a0703a', 'skin_d': '#7a5028', 'shirt': '#3a8a5a', 'shirt_d': '#2a6a42', 'cap': '#1b1030', 'cap_d': '#05030a', 'jeans': '#2a2a3a', 'jeans_d': '#1a1a28'}
    mc(c, 186, GY - 12, (f + 1) % 8, pose='idle', pal=friend)
    if f % 8 in (1, 2):
        text(c, 'YO!', 108, GY - 50, '#ffe066', 1, K)
    if f % 8 in (5, 6):
        text(c, 'BOOTS N CATS!', 168, GY - 62, '#ffffff', 1, K)
    for k in range(3):
        if (f + k) % 3 == 0:
            c.p(171 + k * 4, GY - 36 - k * 3, '#ff4fa3')


def props_rap(c):
    stoop(c, 140, GY); boombox_small(c, 158, GY - 18, 0)
    friend = {'skin': '#a0703a', 'skin_d': '#7a5028', 'shirt': '#3a8a5a', 'shirt_d': '#2a6a42', 'cap': '#1b1030', 'cap_d': '#05030a', 'jeans': '#2a2a3a', 'jeans_d': '#1a1a28'}
    mc(c, 186, GY - 12, 0, pose='idle', pal=friend)


def golem(c, x, gy):
    for row in range(10):
        y = gy - 62 + row * 5
        w = 30 if row < 3 else 40
        x0 = x - w // 2
        c.r(x0 - 1, y - 1, w + 2, 6, K)
        for bx in range(x0 + (0 if row % 2 else -4), x0 + w, 8):
            c.r(max(x0, bx), y, min(7, x0 + w - max(x0, bx)), 4, ['#8a4a3a', '#9a5a46', '#7a3a2a'][(bx + row) % 3])
    c.r(x - 9, gy - 56, 6, 3, '#ffe066'); c.r(x + 3, gy - 56, 6, 3, '#ffe066'); c.r(x - 7, gy - 55, 2, 1, '#ff3b3b'); c.r(x + 5, gy - 55, 2, 1, '#ff3b3b')
    c.r(x - 6, gy - 49, 12, 2, K)
    for side in (-1, 1):
        ax = x + side * 22
        for k in range(5):
            c.r(ax - 4, gy - 42 + k * 6, 8, 6, K); c.r(ax - 3, gy - 41 + k * 6, 6, 4, '#8a4a3a')
    c.r(x - 14, gy - 12, 10, 12, K); c.r(x + 4, gy - 12, 10, 12, K); c.r(x - 13, gy - 11, 8, 10, '#7a3a2a'); c.r(x + 5, gy - 11, 8, 10, '#7a3a2a')
    c.line([(x - 14, gy - 34), (x - 6, gy - 40), (x + 2, gy - 32), (x + 12, gy - 38)], '#ff4fa3', 2)
    c.line([(x - 12, gy - 26), (x - 2, gy - 22), (x + 10, gy - 28)], '#5ef2ff', 2)
    text(c, 'TAG', x - 8, gy - 20, '#ffe066', 1, None)


def autotuner(c, x, gy):
    x0, top = x, gy - 104
    c.r(x0, top, 86, 88, K); c.r(x0 + 1, top + 1, 84, 86, '#3a3a48'); c.r(x0 + 1, top + 1, 84, 4, '#5a5a6a')
    for sy in (top + 6, top + 80):
        for sx in (x0 + 4, x0 + 80):
            c.disc(sx, sy, 1, '#8a8a98')
    c.r(x0 + 8, top + 10, 70, 22, K); c.r(x0 + 9, top + 11, 68, 20, '#0a1410')
    for side, ex in ((0, x0 + 14), (1, x0 + 50)):
        for b in range(6):
            h = 4 + (b * 3 + side * 5) % 12
            c.r(ex + b * 4, top + 28 - h, 3, h, '#7cf06a' if h < 11 else '#ff3b3b')
    c.line([(x0 + 14, top + 13), (x0 + 36, top + 18)], '#ff3b3b', 2); c.line([(x0 + 72, top + 13), (x0 + 50, top + 18)], '#ff3b3b', 2)
    c.disc(x0 + 43, top + 50, 15, K); c.disc(x0 + 43, top + 50, 14, '#c8ccd8'); c.disc(x0 + 43, top + 50, 10, '#8a8a98')
    c.line([(x0 + 43, top + 50), (x0 + 53, top + 42)], '#ff3b3b', 2)
    for k in range(9):
        a = math.radians(200 + k * 17.5)
        c.p(x0 + 43 + 13 * math.cos(a), top + 50 + 13 * math.sin(a), '#1b1030')
    for sx in (x0 + 15, x0 + 71):
        c.disc(sx, top + 52, 10, K); c.disc(sx, top + 52, 9, '#1b1424'); c.disc(sx, top + 52, 4, '#3a3550')
    c.r(x0 + 10, top + 70, 66, 10, K)
    for k in range(10):
        c.r(x0 + 11 + k * 6.5, top + 71, 5, 8, '#f4f4f4' if k % 3 else '#1b1030')
    text(c, 'AUTO', x0 + 30, top + 2, '#ffe066', 1, None)
    for k, col in enumerate(('#5ef2ff', '#ff4fa3', '#ffe066', '#7cf06a')):
        cx = x0 + 14 + k * 20
        c.line([(cx, gy - 16), (cx - 4, gy - 8), (cx + 2, gy)], col, 3)
    c.r(x0 + 40, top - 14, 3, 14, '#8a8a98'); c.disc(x0 + 41, top - 16, 3, '#ff3b3b')


def rap_world(P):
    far = Cv()
    sky(far, 0, HZ, P['sky'])
    r = random.Random(P.get('seed', 5))
    if P.get('stars'):
        stars(far, P['stars'], P.get('seed', 5), HZ - 40)
    if P.get('sun'):
        cx, cy, col = P['sun']; far.disc(cx, cy, 22, col, ymax=HZ - 1)
    if P.get('tower'):
        tx = 230
        far.line([(tx, HZ), (tx + 12, 30)], '#1a0f24', 3); far.line([(tx + 24, HZ), (tx + 12, 30)], '#1a0f24', 3)
        for y in range(40, HZ, 12):
            far.line([(tx + 12 - (y - 30) * 0.12, y), (tx + 12 + (y - 30) * 0.12, y)], '#1a0f24')
        for rr in (8, 16, 24):
            for a in range(200, 340, 6):
                far.p(tx + 12 + rr * math.cos(math.radians(a)), 30 + rr * math.sin(math.radians(a)), '#ff4fa3')
        far.disc(tx + 12, 30, 2, '#ff3b3b')
    if P.get('wall'):
        wc, gc = P['wall']
        far.r(0, 24, W, HZ - 24, wc)
        step = P.get('tile', 8)
        for y in range(24, HZ, step):
            far.r(0, y, W, 1, gc)
            for x in range((y // step % 2) * (step // 2), W, step):
                far.r(x, y, 1, step, gc)
        for px, col in P.get('posters', []):
            far.r(px, 50, 26, 34, K); far.r(px + 1, 51, 24, 32, col); far.r(px + 4, 56, 18, 8, '#f4f4f4'); far.r(px + 4, 68, 18, 2, '#1b1030'); far.r(px + 4, 72, 12, 2, '#1b1030')
    if P.get('graffiti'):
        for gx, cols in ((20, ('#ff4fa3', '#ffe066')), (120, ('#5ef2ff', '#7cf06a')), (220, ('#ffe066', '#ff3b3b'))):
            for k in range(5):
                far.line([(gx + k * 14, 70 + (k % 2) * 10), (gx + k * 14 + 10, 60 + ((k + 1) % 2) * 14)], cols[k % 2], 3)
            far.line([(gx, 90), (gx + 70, 88)], cols[1], 2)
    sk = magic(640)
    x = 0
    while x < 640 and P.get('skyline', True):
        w = r.randrange(16, 34); h = r.randrange(P.get('hmin', 24), P.get('hmax', 60))
        sk.r(x, HZ - h, w, h, P.get('bld', '#140a20'))
        for wy in range(HZ - h + 4, HZ - 3, 5):
            for wx in range(x + 3, x + w - 2, 4):
                if r.random() < P.get('wd', .3):
                    sk.r(wx, wy, 2, 2, r.choice(P.get('win', ['#ffd23f', '#ffb02e'])))
        if r.random() < 0.35:
            sk.r(x + w // 2 - 5, HZ - h - 10, 10, 8, P.get('bld', '#140a20')); sk.r(x + w // 2 - 3, HZ - h - 3, 1, 3, P.get('bld', '#140a20')); sk.r(x + w // 2 + 3, HZ - h - 3, 1, 3, P.get('bld', '#140a20'))
        x += w + r.randrange(1, 5)
    layers = [L_static(far, 0, HZ)]
    if P.get('skyline', True):
        layers.append(L_scroll(sk, HZ - P.get('hmax', 60) - 12, HZ, 12))
    if P.get('train'):
        tr = magic(640)
        tr.r(0, HZ - 40, 640, 30, '#8a8a98'); tr.r(0, HZ - 40, 640, 2, '#c8ccd8'); tr.r(0, HZ - 12, 640, 2, '#5a5a6a')
        for wx in range(6, 640, 22):
            tr.r(wx, HZ - 34, 16, 12, '#1b2a3a'); tr.r(wx + 1, HZ - 33, 6, 4, '#5a8ab8')
        for gx in range(0, 640, 90):
            tr.line([(gx + 10, HZ - 20), (gx + 40, HZ - 26), (gx + 60, HZ - 18)], ['#ff4fa3', '#ffe066', '#5ef2ff'][gx // 90 % 3], 2)
        layers.append(L_scroll(tr, HZ - 42, HZ - 8, 150))
    if P.get('fence'):
        fe = magic(640)
        for x in range(0, 640, 4):
            for y in range(HZ - 40, HZ, 4):
                fe.p(x + (y // 4 % 2) * 2, y, '#5a5a6a')
        for px in range(30, 640, 160):
            fe.r(px, HZ - 70, 3, 70, '#3a3a48'); fe.r(px - 14, HZ - 74, 30, 18, K); fe.r(px - 13, HZ - 73, 28, 16, '#f4f4f4'); fe.r(px - 4, HZ - 60, 10, 2, '#ff9e3d')
            fe.disc(px + 1, HZ - 56, 4, '#ff9e3d', ymax=HZ - 56)
        for lx in range(110, 640, 200):
            fe.r(lx, HZ - 80, 2, 80, '#2a2a38'); fe.r(lx - 4, HZ - 82, 10, 3, '#3a3a48'); fe.disc(lx + 1, HZ - 78, 2, '#ffe066')
        layers.append(L_scroll(fe, HZ - 84, HZ, 25))
    if P.get('roof'):
        rf = magic(640)
        for ax in range(20, 640, 120):
            rf.r(ax, HZ - 14, 22, 14, K); rf.r(ax + 1, HZ - 13, 20, 12, '#5a5a6a'); rf.r(ax + 4, HZ - 10, 14, 1, '#3a3a48'); rf.r(ax + 4, HZ - 6, 14, 1, '#3a3a48')
            rf.r(ax + 60, HZ - 20, 3, 20, '#3a3a48'); rf.r(ax + 56, HZ - 22, 11, 3, '#5a5a6a')
        layers.append(L_scroll(rf, HZ - 24, HZ, 25))
    if P.get('fire_escape'):
        fe2 = magic(640)
        for fx in range(40, 640, 150):
            for k in range(3):
                y = 40 + k * 26
                fe2.r(fx, y, 40, 2, '#1b1424'); fe2.line([(fx + 4, y), (fx + 30, y + 26)], '#1b1424')
                for rx in range(fx, fx + 40, 4):
                    fe2.r(rx, y - 8, 1, 8, '#1b1424')
        layers.append(L_scroll(fe2, 30, HZ, 20))
    gd = magic(640)
    gd.r(0, HZ, 640, PT - HZ, P['ground']); gd.r(0, HZ, 640, 1, P['edge'])
    for _ in range(260):
        sp(gd, r.randrange(640), r.randrange(HZ + 2, PT), P['dot'])
    if P.get('stripe'):
        gd.r(0, HZ + 4, 640, 3, P['stripe'])
    if P.get('court'):
        for x in range(0, 640, 160):
            gd.r(x, HZ + 2, 2, PT - HZ, '#f4f4f4'); gd.disc(x + 80, HZ + 30, 18, '#f4f4f4'); gd.disc(x + 80, HZ + 30, 16, P['ground'])
    if P.get('wet'):
        for _ in range(70):
            gd.r(r.randrange(640), r.randrange(HZ + 6, PT), r.randrange(3, 9), 1, r.choice(P['wet']))
    if P.get('checker'):
        for x in range(0, 640, 12):
            for y in range(HZ + 2, PT, 12):
                if (x // 12 + y // 12) % 2:
                    gd.r(x, y, 12, 12, P['checker'])
    layers.append(L_scroll(gd, HZ, PT, 50, transparent=False))
    return layers


RAP_V = [
    dict(sky=['#2a1240', '#4a1a52', '#7a2a5a', '#c04a4a', '#ff8a4a'], sun=(240, HZ + 4, '#ffb02e'), roof=True, ground='#4a4a58', edge='#8a8a98', dot='#5a5a6a', seed=51),
    dict(sky=['#1a2a2a', '#1a2a2a'], wall=('#c8d8d0', '#8aa8a0'), posters=[(40, '#ff4fa3'), (150, '#5ef2ff'), (260, '#ffe066')], skyline=False, train=True,
         ground='#5a5a6a', edge='#c8ccd8', dot='#4a4a58', stripe='#ffd23f', seed=52),
    dict(sky=['#05061a', '#0a0c26', '#10122e', '#161838'], stars=60, fence=True, hmin=20, hmax=50, ground='#2a4a3a', edge='#f4f4f4', dot='#22403a', court=True, seed=53),
    dict(sky=['#0a0608', '#120a0c'], wall=('#5a2a22', '#3a1a14'), tile=10, graffiti=True, fire_escape=True, skyline=False, ground='#1c1a22', edge='#3a3a48', dot='#26242e',
         wet=['#ff4fa3', '#5ef2ff', '#3a3a5a'], seed=54),
    dict(sky=['#0a0418', '#14082a', '#200c3a', '#2c1048'], stars=40, tower=True, hmin=20, hmax=46, bld='#0a0418', win=['#ff4fa3', '#5ef2ff'], wd=.4,
         ground='#14082a', edge='#ff4fa3', dot='#200c3a', checker='#1e0e3a', seed=55),
]


def rap_base():
    layers = rap_world(RAP_V[0])
    fs = frames_sheet(lambda c, f: intro_rap(c, f), 8, (0, 0)); fs.pop('extra', None)
    c = magic(); props_rap(c); box = rgba(c.im).getbbox()
    fs['props'] = {'src': b64(rgba(c.im, box)), 'x': box[0], 'y': box[1]}
    return {'id': '5-1', 'layers': layers, 'hero': mc_sheet(), 'enemies': enemies_sheet(), 'notes': notes_sheet(), 'buddy': dj_buddy(), 'intro': fs,
            'amb': {'stars': False}}


if __name__ == '__main__':
    import json
    b = rap_base()
    im = Image.new('RGBA', (320, 180), (0, 0, 0, 255))
    import base64, io
    dec = lambda s: Image.open(io.BytesIO(base64.b64decode(s.split(',')[1]))).convert('RGBA')
    tiles = []
    for P in RAP_V + GOTH_V:
        cv = Image.new('RGBA', (320, 180), (0, 0, 0, 255))
        for L in (rap_world(P) if P in RAP_V else goth_world(P)):
            i2 = dec(L['src'])
            if L['type'] == 'scroll':
                i2 = i2.crop((0, 0, 320, i2.height))
            cv.alpha_composite(i2, (0, L['y']))
        tiles.append(cv)
    hero = dec(b['hero']['src']); en = dec(b['enemies']['src']); nt = dec(b['notes']); bd = dec(b['buddy']['src']); it = dec(b['intro']['src'])
    c = magic(); golem(c, 60, 120); autotuner(c, 140, 170)
    misc = Image.new('RGBA', (320, 180), (40, 30, 60, 255))
    misc.alpha_composite(hero.resize((hero.width * 2 // 2, hero.height)), (0, 0)); misc.alpha_composite(en, (0, 50)); misc.alpha_composite(nt, (200, 50))
    misc.alpha_composite(bd, (0, 80)); misc.alpha_composite(rgba(c.im), (0, 0))
    tiles.append(misc)
    fr = it.crop((0, 0, it.width // 8, it.height)); tiles.append(Image.new('RGBA', (320, 180), (40, 30, 60, 255))); tiles[-1].alpha_composite(fr, (0, 0))
    s = Image.new('RGB', (960, 180 * 4), 'white')
    for i, t in enumerate(tiles[:12]):
        s.paste(t.convert('RGB'), ((i % 3) * 320, (i // 3) * 180))
    s.resize((1440, 1080), Image.NEAREST).save('newart_preview.png')
    print('ok')
