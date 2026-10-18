import math, random
from anim import *
from stage_assets2 import magic, rgba, b64, L_scroll, L_static, W, world_power
from gen3a import blimp, hovercar, dragon_far, birds, waterfall
from chapter_worlds import rock_world, metal_world, ROCK_V, METAL_V
from new_art import goth_world, GOTH_V
HZ, PT, GY = 126, 180, 166


def palm(c, x, y, h, col):
    for k in range(h):
        c.r(x + int(math.sin(k / 9) * 3), y - k, 3, 1, col)
    tx, ty = x + int(math.sin(h / 9) * 3) + 1, y - h
    for a in (-160, -130, -95, -60, -25, 10):
        r_ = math.radians(a)
        pts = [(tx + i * math.cos(r_), ty + i * math.sin(r_) + (i * i) / 40) for i in range(0, 16, 3)]
        c.line(pts, col, 2)


# ======================= chapter 1: distinct synthwave places =======================
def beach_world():
    far = Cv()
    sky(far, 0, HZ, ['#1a0a3a', '#3a1260', '#6a1a7a', '#a8287a', '#e0487a', '#ff7a6a'])
    r = random.Random(61)
    for _ in range(40):
        far.p(r.randrange(W), r.randrange(26, 60), '#ffffff')
    far.disc(160, HZ - 30, 28, '#ffb02e', ymax=HZ - 24)
    for y, gh in [(HZ - 44, 1), (HZ - 38, 2), (HZ - 32, 2)]:
        far.r(130, y, 62, gh, far.get(5, y))
    far.r(0, HZ - 24, W, 24, '#1a0a4a')
    for y in range(HZ - 24, HZ, 2):
        w = 30 + (y - (HZ - 24)) * 2
        far.r(160 - w // 2, y, w, 1, ['#ff7a6a', '#ffb02e', '#ff4fa3'][y % 3])
    far.r(0, HZ - 24, W, 1, '#ff7ac8')
    far.r(230, HZ - 34, 90, 3, '#2a1040')
    for px in range(232, 320, 10):
        far.r(px, HZ - 31, 2, 9, '#2a1040'); far.p(px, HZ - 36, '#ffe066')
    layers = [L_static(far, 0, HZ)]
    pm = magic(640)
    for x in range(20, 640, 70):
        palm(pm, x, HZ + 2, 30 + (x * 7) % 16, '#12062a')
    layers.append(L_scroll(pm, HZ - 60, HZ + 4, 22))
    bw = magic(640)
    bw.r(0, HZ, 640, PT - HZ, '#3a1a2a')
    for y in range(HZ + 2, PT, 6):
        bw.r(0, y, 640, 1, '#2a1020')
    for x in range(0, 640, 14):
        bw.r(x, HZ, 1, PT - HZ, '#2a1020')
    bw.r(0, HZ, 640, 2, '#ff4fa3'); bw.r(0, PT - 3, 640, 1, '#5ef2ff')
    for x in range(10, 640, 60):
        bw.r(x, HZ - 14, 2, 14, '#2a1040'); bw.disc(x + 1, HZ - 15, 2, '#ffe066')
    layers.append(L_scroll(bw, HZ - 18, PT, 50))
    return layers


def arcade_world():
    far = Cv()
    far.r(0, 0, W, HZ, '#0a0618')
    for y in range(24, HZ, 4):
        far.r(0, y, W, 1, '#120a24')
    for x in range(0, W, 40):
        far.r(x + 4, 28, 32, 2, ['#ff4fa3', '#5ef2ff', '#ffe066'][x // 40 % 3])
    layers = [L_static(far, 0, HZ)]
    cb = magic(640)
    r = random.Random(62)
    for x in range(8, 640, 36):
        col = r.choice(['#5a2a8e', '#2a5a8e', '#8e2a5a', '#2a8e5a'])
        cb.r(x, HZ - 70, 28, 70, K); cb.r(x + 1, HZ - 69, 26, 68, col)
        cb.r(x + 1, HZ - 69, 26, 8, r.choice(['#ff4fa3', '#ffe066', '#5ef2ff'])); ctext(cb, r.choice(['GO', 'HI', 'UP', '1P']), x + 14, HZ - 68, K, 1, None)
        cb.r(x + 4, HZ - 58, 20, 18, K); cb.r(x + 5, HZ - 57, 18, 16, r.choice(['#1a3a2a', '#2a1a3a', '#3a2a1a']))
        for k in range(4):
            cb.r(x + 6 + r.randrange(14), HZ - 56 + r.randrange(14), 2, 2, r.choice(['#7cf06a', '#ff4fa3', '#ffe066', '#5ef2ff']))
        cb.r(x + 3, HZ - 36, 22, 6, '#1b1030'); cb.disc(x + 9, HZ - 34, 2, '#ff3b3b'); cb.disc(x + 17, HZ - 34, 1, '#ffe066'); cb.disc(x + 21, HZ - 34, 1, '#5ef2ff')
    layers.append(L_scroll(cb, HZ - 72, HZ, 25))
    cp = magic(640)
    cp.r(0, HZ, 640, PT - HZ, '#140a28')
    for _ in range(420):
        x, y = r.randrange(640), r.randrange(HZ + 2, PT)
        cp.r(x, y, 2, 1, r.choice(['#ff4fa3', '#5ef2ff', '#ffe066', '#7cf06a', '#2a1a48']))
    cp.r(0, HZ, 640, 1, '#ffe066')
    layers.append(L_scroll(cp, HZ, PT, 50, transparent=False))
    return layers


def tunnel_world():
    far = Cv()
    far.r(0, 0, W, HZ, '#05030c')
    cx, cy = 160, HZ - 24
    for k, col in enumerate(['#ff4fa3', '#5ef2ff', '#ff4fa3', '#5ef2ff', '#ffe066']):
        w = 40 + k * 60; h = 20 + k * 22
        x0, y0 = cx - w // 2, cy - h // 2
        far.r(x0, max(24, y0), w, 1, col); far.r(x0, min(HZ - 1, y0 + h), w, 1, col)
        if y0 > 24:
            far.r(x0, y0, 1, h, col); far.r(x0 + w, y0, 1, h, col)
    far.disc(cx, cy, 6, '#ffffff'); far.disc(cx, cy, 3, '#ffe066')
    layers = [L_static(far, 0, HZ)]
    lt = magic(640)
    for x in range(0, 640, 24):
        lt.r(x, 30, 14, 2, '#ffe066'); lt.r(x + 6, HZ - 8, 10, 2, '#ff4fa3')
    layers.append(L_scroll(lt, 28, HZ, 140))
    rd = magic(640)
    rd.r(0, HZ, 640, PT - HZ, '#0a0814'); rd.r(0, HZ, 640, 1, '#5ef2ff')
    for x in range(0, 640, 30):
        rd.r(x, HZ + 26, 16, 2, '#ffe066')
    for x in range(0, 640, 8):
        rd.r(x, PT - 4, 4, 2, '#ff4fa3')
    layers.append(L_scroll(rd, HZ, PT, 70, transparent=False))
    return layers


# ======================= chapters 2-4: distinct grounds =======================
def rock_trail():
    L = [l for l in rock_world(ROCK_V[0]) if l['y'] != HZ - 46]
    rd = magic(640)
    r = random.Random(71)
    rd.r(0, HZ + 6, 640, PT - HZ - 6, '#b0703a'); rd.r(0, HZ + 6, 640, 1, '#d8a060')
    for _ in range(300):
        sp(rd, r.randrange(640), r.randrange(HZ + 8, PT), r.choice(['#8a5028', '#c88a4a']))
    for y in (HZ + 24, HZ + 32):
        for x in range(0, 640, 3):
            if (x // 3) % 3:
                rd.p(x, y, '#8a5028')
    for x in range(30, 640, 90):
        rd.disc(x, PT - 6, 4, '#7a4a28'); rd.disc(x - 1, PT - 7, 2, '#a86a3a')
    L[-1] = L_scroll(rd, HZ + 6, PT, 50, transparent=False)
    arch = magic(640)
    for ax in (100, 420):
        arch.r(ax, HZ - 40, 10, 42, '#6a2a1a'); arch.r(ax + 50, HZ - 40, 10, 42, '#6a2a1a'); arch.r(ax, HZ - 48, 60, 10, '#6a2a1a')
        arch.r(ax + 2, HZ - 46, 56, 2, '#8a3a2a')
    L.insert(-1, L_scroll(arch, HZ - 50, HZ + 2, 25))
    return L


def rock_bridge():
    L = rock_world(ROCK_V[2])
    gd = magic(640)
    for x in range(0, 640, 40):
        gd.line([(x, HZ - 30), (x + 20, HZ + 4)], '#3a3a48', 2); gd.line([(x + 40, HZ - 30), (x + 20, HZ + 4)], '#3a3a48', 2)
    gd.r(0, HZ - 32, 640, 3, '#4a4a58'); gd.r(0, HZ + 3, 640, 3, '#4a4a58')
    L.insert(-1, L_scroll(gd, HZ - 34, HZ + 7, 50))
    return L


def metal_floor(P, style):
    L = metal_world(P)
    br = magic(640)
    r = random.Random(81)
    if style == 'grate':
        br.r(0, GY, 640, PT - GY, '#2a2a30')
        for x in range(0, 640, 4):
            br.r(x, GY, 1, PT - GY, '#14141a')
        for y in range(GY, PT, 4):
            br.r(0, y, 640, 1, '#14141a')
        br.r(0, GY, 640, 1, '#8a8a98')
    elif style == 'crystal':
        br.r(0, GY, 640, PT - GY, '#14262a'); br.r(0, GY, 640, 1, '#2fd8c8')
        for x in range(10, 640, 34):
            h = 6 + (x * 7) % 8
            br.poly([(x, GY + 1), (x + 4, GY - h), (x + 8, GY + 1)], '#2fd8c8', None); br.p(x + 4, GY - h + 2, '#ffffff')
    elif style == 'basalt':
        br.r(0, GY, 640, PT - GY, '#1a1214')
        for x in range(0, 640, 12):
            for y in range(GY, PT, 7):
                o = 6 if (y // 7) % 2 else 0
                br.r(x + o, y, 11, 1, '#3a1a14'); br.r(x + o, y, 1, 7, '#3a1a14')
        br.r(0, GY, 640, 1, '#ff5a1f')
    elif style == 'gold':
        br.r(0, GY, 640, PT - GY, '#c98a1a')
        for _ in range(500):
            br.r(r.randrange(640), r.randrange(GY, PT), 3, 2, r.choice(['#ffd23f', '#ffe066', '#a8700a']))
        br.r(0, GY, 640, 1, '#fff3b0')
    L[-1] = L_scroll(br, GY - 14 if style == 'crystal' else GY, PT, 50)
    return L


def goth_cathedral():
    L = goth_world(dict(GOTH_V[0], fence=False, fog=False))
    fl = magic(640)
    fl.r(0, HZ, 640, PT - HZ, '#1a1424')
    for x in range(0, 640, 16):
        for y in range(HZ, PT, 8):
            o = 8 if (y // 8) % 2 else 0
            fl.r(x + o, y, 15, 1, '#2a2238'); fl.r(x + o, y, 1, 8, '#2a2238')
    for x in range(20, 640, 80):
        fl.r(x, HZ - 12, 3, 12, '#5a4a30'); fl.r(x - 2, HZ - 12, 7, 1, '#5a4a30'); fl.r(x, HZ - 16, 3, 4, '#f4f0e0'); fl.p(x + 1, HZ - 18, '#ffb02e'); fl.p(x + 1, HZ - 19, '#ffe066')
    L.append(L_scroll(fl, HZ - 20, PT, 50))
    return L


def goth_manor():
    L = [l for l in goth_world(GOTH_V[2]) if l['y'] != HZ - 12]
    pa = magic(640)
    r = random.Random(91)
    pa.r(0, HZ + 4, 640, PT - HZ - 4, '#1a1612')
    for _ in range(80):
        pa.r(r.randrange(640), r.randrange(HZ + 8, PT), r.randrange(4, 12), 1, '#3a4a6a')
    for x in range(30, 640, 110):
        pa.r(x, HZ - 26, 2, 30, '#0a0806'); pa.r(x - 3, HZ - 30, 8, 6, K); pa.r(x - 2, HZ - 29, 6, 4, '#ffb02e'); pa.p(x, HZ - 32, '#0a0806')
    L.append(L_scroll(pa, HZ - 32, PT, 50))
    return L


# ======================= chapter 6: power metal =======================
def clouds_strip(y0, y1, col1, col2, step=70):
    cl = magic(640)
    for cx in range(20, 640, step):
        cy = y0 + 10 + (cx * 7) % max(1, (y1 - y0 - 20))
        for dx, rr in [(-10, 6), (0, 8), (10, 6), (18, 4)]:
            cl.disc(cx + dx, cy, rr, col1)
        for dx, rr in [(-10, 4), (0, 6), (10, 4)]:
            cl.disc(cx + dx, cy - 1, rr, col2)
    return L_scroll(cl, y0, y1, 8)


def power_v0():
    L = world_power()
    bd = magic(640); birds(bd, 150, 56, 7, 2, '#2a2f5a'); birds(bd, 450, 46, 5, 4, '#2a2f5a')
    wf = magic(W); waterfall(wf, 104, HZ - 38, HZ - 6)
    return [L[0], {'type': 'static', 'src': b64(rgba(wf.im)), 'y': 0}, clouds_strip(26, 66, '#c8c0d8', '#f4f0e8')] + L[1:] + [L_scroll(bd, 36, 66, 30)]


POWER_AMB0 = {'waterfall': [104, HZ - 38, HZ - 6], 'flags': [[tx + 5, HZ - 39 - th] for tx, th in [(266, 26), (282, 40), (300, 30)]]}


def power_islands():
    far = Cv()
    sky(far, 0, HZ, ['#3a6ad8', '#5a8ae8', '#7aa8f0', '#a8c8f8', '#d8e8ff'])
    for ix, iy, w in [(40, 60, 60), (150, 44, 80), (250, 70, 50)]:
        far.poly([(ix, iy), (ix + w, iy), (ix + w - 10, iy + 16), (ix + w // 2, iy + 30), (ix + 10, iy + 16)], '#6a5a4a', None)
        far.r(ix, iy - 3, w, 4, '#4a8a3a'); far.r(ix, iy - 3, w, 1, '#7ac85a')
        far.r(ix + w // 2 - 2, iy + 16, 4, HZ - iy - 16, '#e8f4ff'); far.r(ix + w // 2 - 1, iy + 16, 1, HZ - iy - 16, '#ffffff')
        far.r(ix + 10, iy - 14, 6, 11, '#c8c0d8'); far.poly([(ix + 9, iy - 14), (ix + 13, iy - 20), (ix + 17, iy - 14)], '#5a6fa8', None)
    far.r(0, HZ, W, PT - HZ, '#e8f0ff')
    L = [L_static(far, 0, PT), clouds_strip(24, 60, '#e8f0ff', '#ffffff', 90)]
    L.append(clouds_strip(HZ + 4, PT - 4, '#c8d8f0', '#f4f8ff', 50) | {'speed': 18})
    br = magic(640)
    br.r(0, GY - 3, 640, 6, '#8a5a2b')
    for x in range(0, 640, 6):
        br.r(x, GY - 3, 1, 6, '#5a3a1a')
    for x in range(0, 640, 30):
        br.r(x, GY - 16, 2, 14, '#5a3a1a')
    br.line([(x, GY - 14 + int(3 * math.sin(x / 10))) for x in range(0, 640, 4)], '#c8a060')
    L.append(L_scroll(br, GY - 18, GY + 4, 50))
    return L


def power_labyrinth():
    far = Cv()
    sky(far, 0, HZ, ['#2a1a1a', '#3a2a22', '#4a3a2a', '#5a4a32'])
    for x in range(0, W, 46):
        h = 50 + (x * 13) % 30
        far.r(x, HZ - h, 40, h, '#4a4048'); far.r(x, HZ - h, 40, 2, '#6a6068')
        for y in range(HZ - h + 6, HZ, 6):
            far.r(x, y, 40, 1, '#3a3038')
        far.r(x + 14, HZ - 24, 12, 24, '#1a1418'); far.disc(x + 20, HZ - 24, 6, '#1a1418')
    far.r(0, HZ, W, PT - HZ, '#a8865a')
    L = [L_static(far, 0, PT)]
    tc = magic(640)
    for x in range(20, 640, 80):
        tc.r(x, HZ - 40, 2, 12, '#3a2a1a'); tc.disc(x + 1, HZ - 43, 3, '#ff9e3d'); tc.p(x + 1, HZ - 46, '#ffe066')
    L.append(L_scroll(tc, HZ - 50, HZ - 26, 25))
    sd = magic(640); r = random.Random(101)
    sd.r(0, HZ, 640, PT - HZ, '#b8966a')
    for _ in range(300):
        sp(sd, r.randrange(640), r.randrange(HZ, PT), r.choice(['#a07a4a', '#c8a678']))
    for x in range(0, 640, 120):
        sd.r(x + 10, PT - 8, 12, 3, '#e8e0c8'); sd.disc(x + 26, PT - 7, 3, '#e8e0c8')
    L.append(L_scroll(sd, HZ, PT, 50, transparent=False))
    return L


def power_battlements():
    far = Cv()
    sky(far, 0, HZ, ['#1a1e2a', '#262c3a', '#323a4a', '#3e485a'])
    far.poly([(0, HZ), (40, HZ - 50), (90, HZ - 30), (150, HZ - 66), (220, HZ - 36), (280, HZ - 58), (320, HZ - 40), (320, HZ)], '#2a2f3a', None)
    far.r(0, HZ, W, PT - HZ, '#5a5a68')
    L = [L_static(far, 0, PT), clouds_strip(24, 70, '#3a3e4a', '#4a4e5a', 60)]
    bt = magic(640)
    bt.r(0, HZ - 22, 640, 24, '#6a6a78')
    for x in range(0, 640, 16):
        bt.r(x, HZ - 32, 9, 10, '#6a6a78'); bt.r(x, HZ - 32, 9, 1, '#8a8a98')
    for y in range(HZ - 22, HZ, 6):
        bt.r(0, y, 640, 1, '#4a4a58')
    for x in range(40, 640, 120):
        bt.r(x, HZ - 60, 2, 30, '#3a3a48'); bt.poly([(x + 2, HZ - 60), (x + 16, HZ - 56), (x + 2, HZ - 50)], '#c2260f', None)
    L.append(L_scroll(bt, HZ - 62, HZ + 2, 30))
    wk = magic(640)
    wk.r(0, HZ + 2, 640, PT - HZ - 2, '#5a5a68')
    for x in range(0, 640, 20):
        for y in range(HZ + 2, PT, 10):
            o = 10 if (y // 10) % 2 else 0
            wk.r(x + o, y, 19, 1, '#3a3a48'); wk.r(x + o, y, 1, 10, '#3a3a48')
    L.append(L_scroll(wk, HZ + 2, PT, 50, transparent=False))
    return L


def power_eye():
    far = Cv()
    sky(far, 0, HZ, ['#0a0418', '#14082a', '#200a3a', '#2a0c44'])
    cx, cy = 200, 60
    for arm in range(4):
        for t in range(0, 220, 2):
            a = arm * math.pi / 2 + t / 40
            rr = t * 0.6
            x, y = cx + rr * math.cos(a), cy + rr * 0.5 * math.sin(a)
            if 24 < y < HZ:
                far.p(x, y, ['#5a2a8e', '#3a1a6e', '#7a3aae'][t % 3])
    far.disc(cx, cy, 8, '#c8a8ff'); far.disc(cx, cy, 4, '#ffffff')
    far.r(0, HZ, W, PT - HZ, '#120a20')
    L = [L_static(far, 0, PT)]
    rk = magic(640); r = random.Random(111)
    for x in range(20, 640, 60):
        y = 40 + (x * 11) % 60
        rk.poly([(x, y), (x + 14, y - 4), (x + 20, y + 4), (x + 8, y + 10)], '#3a2a4a', None); rk.p(x + 8, y + 2, '#5ef2ff')
    L.append(L_scroll(rk, 30, HZ - 4, 16))
    pf = magic(640)
    pf.r(0, HZ + 6, 640, PT - HZ - 6, '#2a1a3a'); pf.r(0, HZ + 6, 640, 1, '#8a5aff')
    for x in range(10, 640, 26):
        pf.r(x, HZ + 14 + (x % 3) * 8, 6, 2, '#5ef2ff'); pf.r(x + 2, HZ + 12 + (x % 3) * 8, 2, 6, '#5ef2ff')
    L.append(L_scroll(pf, HZ + 6, PT, 50, transparent=False))
    return L
