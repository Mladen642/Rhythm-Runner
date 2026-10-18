import base64, io, json, math, random
import numpy as np
from PIL import Image
from anim import *

HZ, PT, GY = 126, 180, 166
LANE_COL = ['#5ef2ff', '#ff4fa3', '#ffe066']


def rgba(im, box=None):
    a = np.array(im.convert('RGB'))
    alpha = np.where((a[:, :, 0] == 0) & (a[:, :, 1] == 255) & (a[:, :, 2] == 1), 0, 255).astype('uint8')
    out = Image.fromarray(np.dstack([a, alpha]), 'RGBA')
    return out.crop(box) if box else out


def b64(im):
    buf = io.BytesIO(); im.save(buf, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()


def magic(w=W):
    return strip_canvas(w)


def bbox_union(ims):
    box = None
    for im in ims:
        bb = rgba(im).getbbox()
        if bb:
            box = bb if box is None else (min(box[0], bb[0]), min(box[1], bb[1]), max(box[2], bb[2]), max(box[3], bb[3]))
    return box


def rim(img, col):
    a = np.array(img)
    m = a[:, :, 3] > 0
    d = m.copy()
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            d |= np.roll(np.roll(m, dy, 0), dx, 1)
    r = d & ~m
    c = C(col)
    a[r] = [c[0], c[1], c[2], 255]
    return Image.fromarray(a, 'RGBA')


def L_static(cv, y0, y1):
    return {'type': 'static', 'src': b64(cv.im.crop((0, y0, W, y1))), 'y': y0}


def L_scroll(st, y0, y1, speed, transparent=True):
    im = rgba(st.im, (0, y0, 640, y1)) if transparent else st.im.crop((0, y0, 640, y1))
    return {'type': 'scroll', 'src': b64(im), 'y': y0, 'speed': speed}


# ---------------- worlds ----------------
def world_synth():
    far = Cv()
    sky(far, 0, HZ, ['#140a33', '#22104d', '#3a1462', '#5e1a72', '#8a2178', '#c22e74'])
    rowc = {y: far.get(5, y) for y in range(0, HZ)}
    r = random.Random(7)
    for _ in range(80):
        far.p(r.randrange(W), r.randrange(26, HZ - 30), '#ffffff' if r.random() < .4 else '#b59cff')
    cx, cy, rad = 232, HZ - 12, 30
    bands = ['#ffe066', '#ffc24a', '#ff9a4d', '#ff7062', '#ff4fa3']
    for y in range(cy - rad, HZ):
        dy = y - cy
        if abs(dy) <= rad:
            s_ = int(math.sqrt(rad * rad - dy * dy) + 0.35)
            k = min(4, int((y - (cy - rad)) / ((HZ - (cy - rad)) / 5)))
            far.r(cx - s_, y, 2 * s_ + 1, 1, bands[k])
    for g_, gh in [(HZ - 19, 1), (HZ - 14, 1), (HZ - 10, 2), (HZ - 6, 2), (HZ - 2, 2)]:
        for y in range(g_, g_ + gh):
            far.r(cx - rad - 1, y, 2 * rad + 3, 1, rowc[y])
    sk = magic(640)
    x = 0
    while x < 640:
        w = r.randrange(8, 20); h = r.randrange(10, 30)
        sk.r(x, HZ - h, w, h, '#12082a'); sk.r(x, HZ - h, w, 1, '#2e1658')
        for wy in range(HZ - h + 3, HZ - 2, 4):
            for wx in range(x + 2, x + w - 2, 3):
                if r.random() < .33:
                    sp(sk, wx, wy, '#5ef2ff' if r.random() < .6 else '#ff7ac8')
        x += w + r.randrange(1, 6)
    GH = PT - HZ
    grid = Image.new('RGB', (W, GH * 12))
    for k in range(12):
        cv = Cv()
        cv.r(0, HZ, W, GH, '#10061f')
        vx, vy = 160, HZ - 8
        for bx in range(-560 - k * 3, W + 600, 36):
            xt = vx + (bx - vx) * (HZ - vy) / (PT - 1 - vy)
            cv.line([(xt, HZ), (bx, PT - 1)], '#5c1a63')
        offs = [1, 3, 6, 10, 15, 21, 28, 36, 45, 55]
        for j in range(len(offs) - 1):
            y = HZ + offs[j] + int((offs[j + 1] - offs[j]) * k / 12)
            if y < PT:
                cv.r(0, y, W, 1, '#a8267c')
        cv.r(0, HZ, W, 1, '#ff4fa3')
        grid.paste(cv.im.crop((0, HZ, W, PT)), (0, k * GH))
    bl = magic(640); blimp(bl, 100, 4); blimp(bl, 420, 8)
    return [L_static(far, 0, HZ), L_scroll(bl, 0, 28, 8) | {'y': 30}, L_scroll(sk, HZ - 32, HZ, 15),
            {'type': 'frames', 'src': b64(grid), 'y': HZ, 'h': GH, 'n': 12, 'fps': 25}]


def world_rock():
    far = Cv()
    sky(far, 0, HZ, ['#2a1550', '#4f1f63', '#80295f', '#b8384f', '#e8583d', '#ff8f3d'])
    far.disc(252, HZ, 24, '#ffd23f', ymax=HZ - 1)
    for g_ in [HZ - 10, HZ - 6, HZ - 3]:
        far.r(226, g_, 52, 1, '#ff8f3d')
    o = HZ - 104
    far.poly([(0, HZ), (0, 86 + o), (20, 84 + o), (26, 78 + o), (60, 78 + o), (66, 86 + o), (90, 88 + o), (96, 82 + o),
              (130, 82 + o), (136, 90 + o), (170, 92 + o), (176, HZ)], '#5a2350', None)
    far.poly([(150, HZ), (160, 90 + o), (196, 90 + o), (204, 98 + o), (232, 98 + o), (236, HZ)], '#7a2e2e', None)
    far.poly([(280, HZ), (290, 88 + o), (320, 86 + o), (320, HZ)], '#7a2e2e', None)
    far.r(0, HZ, W, 6, '#c9743a')
    r = random.Random(3)
    for _ in range(90):
        far.p(r.randrange(W), r.randrange(HZ, HZ + 6), '#a85a2e')
    eg = magic(640); eagle(eg, 100, 14); eagle(eg, 400, 20)
    pl = magic(640)
    poles = list(range(16, 640, 80))
    for x in poles:
        pl.r(x, HZ - 42, 2, 44, '#2a1630'); pl.r(x - 5, HZ - 38, 12, 1, '#2a1630')
    for a, b in zip(poles, poles[1:] + [poles[0] + 640]):
        for x in range(a + 7, b - 5):
            sp(pl, x % 640, HZ - 38 + int(6 * math.sin(math.pi * (x - a) / (b - a))), '#2a1630')
    for x in [40, 150, 260, 370, 480, 590]:
        c = '#24442e'
        pl.r(x, HZ - 10, 3, 12, c); pl.r(x - 3, HZ - 6, 3, 1, c); pl.r(x - 3, HZ - 9, 1, 3, c)
        pl.r(x + 3, HZ - 4, 3, 1, c); pl.r(x + 5, HZ - 7, 1, 3, c)
    rd = magic(640)
    rd.r(0, HZ + 6, 640, PT - HZ - 6, '#2b2433'); rd.r(0, HZ + 6, 640, 1, '#e8d8b0')
    for _ in range(300):
        sp(rd, r.randrange(640), r.randrange(HZ + 8, PT), '#362d42')
    for x in range(4, 640, 20):
        rd.r(x, HZ + 22, 10, 2, '#ffd23f')
    return [L_static(far, 0, HZ + 6), L_scroll(eg, 0, 30, 20) | {'y': 28}, L_scroll(pl, HZ - 44, HZ + 2, 25),
            L_scroll(rd, HZ + 6, PT, 50, transparent=False)]


def world_metal():
    far = Cv()
    sky(far, 0, HZ, ['#0e0207', '#1f040d', '#360812', '#541015', '#7a1a17', '#a82c19'])
    r = random.Random(5)
    for _ in range(40):
        far.p(r.randrange(W), r.randrange(28, HZ - 2), '#ff7a1a' if r.random() < .6 else '#ffb02e')
    fct = min(1.0, (HZ - 28) / 84)
    cs = '#150409'

    def Y(v):
        return HZ - int(v * fct)
    far.r(36, Y(48), 44, int(48 * fct) + 1, cs)
    for x in range(36, 80, 6):
        far.r(x, Y(52), 3, 4, cs)
    far.r(22, Y(62), 14, int(62 * fct) + 1, cs)
    far.poly([(20, Y(62)), (29, Y(82)), (38, Y(62))], cs, None)
    far.r(80, Y(68), 14, int(68 * fct) + 1, cs)
    far.poly([(78, Y(68)), (87, Y(90)), (96, Y(68))], cs, None)
    for wx, wv in [(28, 54), (28, 44), (86, 60), (86, 50), (46, 38), (58, 38), (70, 38)]:
        far.r(wx, Y(wv), 2, 3, '#ff7a1a')
    far.r(0, HZ, W, GY - HZ, '#ff5a1f')
    for y in [HZ, HZ + 1, HZ + 2]:
        for x in range(W):
            if (x + y) % 2 == 0 or y == HZ:
                far.p(x, y, '#a3200f')
    bt = magic(640); batswarm(bt, 120, 14, 10, 2); batswarm(bt, 430, 18, 8, 3)
    lv = magic(640)
    for _ in range(110):
        lv.r(r.randrange(640), r.randrange(HZ + 3, GY), r.randrange(2, 6), 1, '#ffe066' if r.random() < .2 else '#ffb02e')
    br = magic(640)
    br.r(0, GY, 640, PT - GY, '#5a4f66'); br.r(0, GY, 640, 1, '#a89cb8')
    mid = GY + 5
    br.r(0, mid, 640, 1, '#2e2838'); br.r(0, PT - 1, 640, 1, '#2e2838')
    for x in range(0, 640, 16):
        br.r(x, GY + 1, 1, mid - GY - 1, '#2e2838'); br.r(x + 8, mid + 1, 1, PT - mid - 2, '#2e2838')
    return [L_static(far, 0, GY), L_scroll(bt, 0, 30, 30) | {'y': 30}, L_scroll(lv, HZ + 3, GY, 12),
            L_scroll(br, GY, PT, 50, transparent=False)]


def world_goth():
    far = Cv()
    sky(far, 0, HZ, ['#07040e', '#110822', '#1c0d33', '#2a1245', '#3a1a52'])
    r = random.Random(1)
    for _ in range(40):
        far.p(r.randrange(W), r.randrange(26, HZ - 30), '#6a5a8a')
    for a in range(0, 360, 8):
        far.p(246 + 21 * math.cos(math.radians(a)), 50 + 21 * math.sin(math.radians(a)), '#4a3a6e')
    far.disc(246, 50, 16, '#e8e6f4'); far.disc(240, 45, 3, '#c8c4dc'); far.disc(252, 56, 4, '#c8c4dc')
    cs = '#0a0612'
    far.r(36, HZ - 40, 58, 40, cs); far.r(56, HZ - 54, 18, 54, cs)
    far.poly([(56, HZ - 54), (65, HZ - 70), (74, HZ - 54)], cs, None)
    far.poly([(34, HZ - 40), (40, HZ - 56), (46, HZ - 40)], cs, None)
    far.poly([(84, HZ - 40), (90, HZ - 56), (96, HZ - 40)], cs, None)
    far.disc(65, HZ - 30, 5, '#5a2a8e'); far.disc(65, HZ - 30, 3, '#b06bff')
    for tx in (150, 292):
        far.line([(tx, HZ), (tx, HZ - 30)], '#120a1c', 3)
        for bx, by, ex, ey_ in [(0, -20, -10, -30), (0, -26, 9, -36), (0, -14, 8, -20)]:
            far.line([(tx + bx, HZ + by), (tx + ex, HZ + ey_)], '#120a1c', 1)
    far.r(0, HZ, W, PT - HZ, '#120d1c'); far.r(0, HZ, W, 1, '#2a2238')
    fe = magic(640)
    for x in range(0, 640, 8):
        fe.r(x, HZ - 10, 1, 10, '#1b1428'); sp(fe, x, HZ - 11, '#3a3050')
    fe.r(0, HZ - 8, 640, 1, '#1b1428'); fe.r(0, HZ - 3, 640, 1, '#1b1428')
    for gx in range(12, 640, 40):
        if r.random() < .5:
            fe.r(gx, HZ - 6, 7, 9, K); fe.r(gx + 1, HZ - 5, 5, 8, '#3a3448'); fe.r(gx + 1, HZ - 5, 5, 1, '#5a5470')
        else:
            fe.r(gx + 2, HZ - 9, 3, 12, '#3a3448'); fe.r(gx, HZ - 6, 7, 3, '#3a3448')
    gr = magic(640)
    for _ in range(140):
        sp(gr, r.randrange(640), r.randrange(HZ + 2, PT), '#2a2238')
    fg = magic(640)
    for y in range(HZ - 8, HZ + 9):
        for x in range(640):
            if (x * 7 + y * 13) % 15 == 0:
                sp(fg, x, y, '#8a84a8')
    for x0, y0 in [(140, HZ - 4), (330, HZ - 10), (520, HZ - 2)]:
        for a in range(0, 360, 45):
            sp(fg, x0 + 4 * math.cos(math.radians(a)), y0 + 4 * math.sin(math.radians(a)), '#2a5a3a')
        fg.disc(x0, y0, 2, '#7cf06a'); sp(fg, x0, y0, '#ffffff')
    return [L_static(far, 0, PT), L_scroll(gr, HZ + 2, PT, 50), L_scroll(fe, HZ - 12, HZ + 4, 25), L_scroll(fg, HZ - 8, HZ + 9, 12)]


def world_power():
    far = Cv()
    sky(far, 0, 24, ['#1a2a6e'])
    bg_power(far, HZ, PT, seed=5)
    dr = magic(640); dragon_far(dr, 200, 12); dragon_far(dr, 470, 16, '#3a3f6a')
    r = random.Random(4)
    fl = magic(640)
    P0 = PT - 16
    fl.r(0, HZ + 1, 640, P0 - HZ - 1, '#4a8a3a')
    for _ in range(90):
        sp(fl, r.randrange(640), r.randrange(HZ + 2, P0 - 2), r.choice(['#ffd23f', '#ffffff', '#ff7ac8']))
    pa = magic(640)
    pa.r(0, P0, 640, 10, '#a8865a'); pa.r(0, P0, 640, 1, '#6a9a4a'); pa.r(0, P0 + 10, 640, 1, '#6a9a4a')
    for _ in range(80):
        pa.r(r.randrange(640), r.randrange(P0 + 1, P0 + 9), 2, 1, '#8a6a4a')
    return [L_static(far, 0, PT), L_scroll(dr, 0, 26, 10) | {'y': 26}, L_scroll(fl, HZ + 1, P0, 30, transparent=False),
            L_scroll(pa, P0, P0 + 11, 50, transparent=False)]


# ---------------- heroes ----------------
def hero_sheet(draw, n, cw, ch, ax, ay, fps, hx):
    sheet = Image.new('RGBA', (cw * n, ch))
    tips = []
    for f in range(n):
        c = magic()
        hi, lo = draw(c, ax, ay, f)
        sheet.paste(rgba(c.im, (0, 0, cw, ch)), (f * cw, 0))
        tips.append([round(hi[0] - ax), round(hi[1] - ay), round(lo[0] - ax), round(lo[1] - ay)])
    return {'src': b64(sheet), 'n': n, 'cw': cw, 'ch': ch, 'ax': ax, 'ay': ay, 'fps': fps, 'x': hx, 'tips': tips}


def girl_draw(c, x, gy, f):
    t = girl_anim(c, x, gy, f)
    return t, t


def gh_draw(spr, pal, gb, gd, tail=None):
    def d(c, x, gy, f):
        hi, lo, _ = gh_anim(c, x, gy, f, spr, pal, gb, gd, tail=tail)
        return hi, lo
    return d


def dwarf_body(c, x, gy, f, pal=DA, cycle=8):
    p = f * 2 * math.pi / cycle
    bob = 1 if math.cos(2 * p) > 0 else 0
    y = gy - 22 + bob
    run_legs(c, [(x + 6, y + 17), (x + 11, y + 17)], p, 1.6, 1.6, pal['P'], pal['B'], 5)
    c.spr(DWARF[:17], pal, x, y)
    return (x + 16, y + 11), (x + 16, y + 11)


def hammer_sheet(angles):
    sheet = Image.new('RGBA', (64 * len(angles), 64))
    heads = []
    for i, a in enumerate(angles):
        c = magic()
        hd = hammer(c, 32, 32, a, 16)
        sheet.paste(rgba(c.im, (0, 0, 64, 64)), (i * 64, 0))
        heads.append([round(hd[0] - 32), round(hd[1] - 32)])
    return {'src': b64(sheet), 'angles': angles, 'heads': heads}


# ---------------- enemies ----------------
def spr_air(S, P):
    return lambda c, fl: c.spr(S, P, 16 - sw(S) // 2, 12 - len(S) // 2, flash=fl)


def spr_ground(S, P):
    return lambda c, fl: c.spr(S, P, 16 - sw(S) // 2, 24 - len(S), flash=fl)


def fire_air(c, fl):
    fireball(c, 13, 12)
    if fl:
        c.disc(13, 12, 4, '#ffffff')


def wyv_air(c, fl):
    wyvern(c, 16, 14, fl)


def enemy_sheet(draws):
    sheet = Image.new('RGBA', (32 * 6, 24))
    for l, d in enumerate(draws):
        for k, fl in enumerate((None, '#ffffff')):
            c = magic()
            d(c, fl)
            sheet.paste(rim(rgba(c.im, (0, 0, 32, 24)), LANE_COL[l]), ((l * 2 + k) * 32, 0))
    return {'src': b64(sheet), 'anch': [[16, 12], [16, 12], [16, 23]]}


def note_sheet(kind, cols):
    sheet = Image.new('RGBA', (40, 20))
    for k, col in enumerate(cols):
        c = magic(); notesprite(c, kind, 2, 2, col)
        sheet.paste(rgba(c.im, (0, 0, 20, 20)), (k * 20, 0))
    return b64(sheet)


# ---------------- buddies ----------------
def frames_sheet(draw, n, ref):
    ims = []
    extra = []
    for f in range(n):
        c = magic()
        extra.append(draw(c, f))
        ims.append(c.im)
    box = bbox_union(ims)
    w, h = box[2] - box[0], box[3] - box[1]
    sheet = Image.new('RGBA', (w * n, h))
    for f, im in enumerate(ims):
        sheet.paste(rgba(im, box), (f * w, 0))
    return {'src': b64(sheet), 'n': n, 'cw': w, 'ch': h, 'ox': ref[0] - box[0], 'oy': ref[1] - box[1], 'extra': extra}


def boar_frame(c, x, gy, ph):
    for k in range(4):
        c.disc(x - 6 - k * 12, gy - 6 - k * 2, 6 - k, '#8a7f99')
    legs = [((x + 14, gy - 12), (x + 2, gy - 2)), ((x + 20, gy - 12), (x + 14, gy)), ((x + 46, gy - 12), (x + 58, gy - 3)), ((x + 52, gy - 12), (x + 64, gy - 6))]
    for i, (a, b) in enumerate(legs):
        sw_ = 5 * math.sin(ph + i * 1.6)
        b = (b[0] + sw_, b[1] - abs(sw_) * 0.4)
        c.line([a, b], K, 5); c.line([a, b], '#4a2a1a', 3)
    bob = int(round(math.sin(ph * 2)))
    c.poly([(x + 4, gy - 18 + bob), (x + 14, gy - 30 + bob), (x + 40, gy - 32 + bob), (x + 56, gy - 26 + bob), (x + 62, gy - 18 + bob), (x + 58, gy - 10 + bob), (x + 10, gy - 9 + bob)], '#6b3f2a')
    for i in range(9):
        bx = x + 10 + i * 5
        c.poly([(bx, gy - 29 + bob), (bx + 2, gy - 36 + bob), (bx + 4, gy - 30 + bob)], '#3a2216', None)
    c.poly([(x + 52, gy - 28 + bob), (x + 66, gy - 26 + bob), (x + 74, gy - 18 + bob), (x + 72, gy - 12 + bob), (x + 60, gy - 11 + bob), (x + 54, gy - 16 + bob)], '#7a4a32')
    c.r(x + 70, gy - 19 + bob, 6, 6, K); c.r(x + 71, gy - 18 + bob, 4, 4, '#d68a7a')
    c.poly([(x + 66, gy - 13 + bob), (x + 74, gy - 22 + bob), (x + 70, gy - 12 + bob)], '#f4ead0')
    c.r(x + 61, gy - 24 + bob, 2, 2, '#ff3b3b')
    head = dwarf(c, x + 24, gy - 26 + bob, DK, ang=95, L=20, crown=True)
    c.poly([(x + 18, gy - 33 + bob), (x + 44, gy - 33 + bob), (x + 46, gy - 21 + bob), (x + 16, gy - 21 + bob)], '#c2260f')
    c.r(x + 17, gy - 24 + bob, 29, 2, '#ffd23f')
    return [round(head[0]), round(head[1])]


def buddy_synth():
    A = json.load(open('assets3.json'))['S']
    return {'kind': 'laser', 'name': 'KEYTAR HERO', 'say': 'TOTALLY RADICAL!', 'sfx': 'keytar', 'pitch': 1.5, 'rate': 1.15, 'src': A['keytar'], 'o': A['keytar_o']}


def buddy_rock():
    fs = frames_sheet(lambda c, f: biker_anim(c, 100, 40, f), 8, (100, 40 + 41))
    fs.update({'kind': 'sweep', 'name': 'THE BIKER', 'say': 'OUTTA MY WAY!', 'sfx': 'biker', 'pitch': 0.6, 'rate': 1.0, 'front': 64, 'speed': 210})
    return fs


def buddy_metal():
    fs = frames_sheet(lambda c, f: boar_frame(c, 100, 100, f * 2 * math.pi / 6), 6, (100, 100))
    fs.update({'kind': 'sweep', 'name': 'THE BOAR KING', 'say': 'FOR THE FORGE!', 'sfx': 'boar', 'pitch': 0.4, 'rate': 0.85, 'front': 76, 'speed': 170, 'bolts': True})
    fs['heads'] = [[h[0] - 100, h[1] - 100] for h in fs.pop('extra')]
    return fs


def buddy_goth():
    angs = [70, 80, 92, 104, 116, 90, 64, 38, 12, -14, -40]
    fs = frames_sheet(lambda c, f: reaper_anim(c, 90, 60, f, angs[f]), len(angs), (90, 60))
    fs.update({'kind': 'slash', 'name': 'THE REAPER', 'say': 'YOUR TIME IS UP.', 'sfx': 'reaper', 'pitch': 0.1, 'rate': 0.7})
    return fs


def buddy_power():
    gear = [('#d0802a', '#2a2238'), ('#ffd23f', '#5a2a3a'), ('#2a1f3a', '#2a4a6a'), ('#e8e0c8', '#3a3a48')]

    def d(c, f):
        for k, (hair, shirt) in enumerate(gear):
            headbanger_anim(c, 40 + k * 26, 100, hair, shirt, (f * 45 + k * 70) % 360, (f // 2 + k) % 2)
    fs = frames_sheet(d, 8, (40, 100))
    fs.update({'kind': 'sweep', 'name': 'THE HEADBANGERS', 'say': 'HEADBANG!!!', 'sfx': 'headbang', 'pitch': 1.1, 'rate': 1.3, 'front': 3 * 26 + 22, 'speed': 150})
    return fs


# ---------------- mini bosses ----------------
def miniboss(fn, name, t0, ref_gy=150):
    c = magic(); fn(c, 40, ref_gy)
    box = rgba(c.im).getbbox()
    im = rgba(c.im, box)
    a = np.array(im).astype(float)
    m = a[:, :, 3] > 0
    a[m, :3] = a[m, :3] * 0.3 + 255 * 0.7
    fl = Image.fromarray(a.astype('uint8'), 'RGBA')
    return {'name': name, 't0': t0, 'src': b64(im), 'flash': b64(fl), 'ox': 40 - box[0], 'oy': ref_gy - box[1], 'w': im.width, 'h': im.height}


def cut(chart, t0, a=0.6, b=10.0):
    return [n for n in chart if not (t0 - a <= n['t'] <= t0 + b)]


# ---------------- stages ----------------
def stage(sid, genre, place, track, acc, song, chart, world, hero, enemies, notes, buddy, attack='waves', hammer_=None, mb=None):
    ch = json.load(open(chart))
    if mb:
        ch = cut(ch, mb['t0'])
    d = {'id': sid, 'genre': genre, 'place': place, 'track': track, 'acc': acc, 'song': song,
         'chart': ch, 'layers': world, 'hero': hero, 'enemies': enemies, 'notes': notes,
         'buddy': buddy, 'attack': attack}
    if hammer_:
        d['hammer'] = hammer_
    if mb:
        d['miniboss'] = mb
    return d


STAGES = [
    stage('1-1', 'SYNTHPOP', 'NEON CITY', 'NEON SKATE', '#ff4fa3', 'synth', 'chart_easy.json', world_synth(),
          hero_sheet(girl_draw, 20, 36, 38, 6, 35, 25, 38),
          enemy_sheet([spr_air(DRONE, DPAL), spr_air(CASS, CPAL), spr_ground(CASS[:11] + ["...KK......KK...", "..KKK.....KKK.."], dict(CPAL, C='#ffd23f', L='#ff4fa3', c='#b8901f'))]),
          note_sheet('eighth', ['#ff4fa3', '#5ef2ff']), buddy_synth(), mb=miniboss(boombox, 'BOOMBOX BRUTE', 48.0)),
    stage('2-1', 'ROCK', 'SUNSET HIGHWAY', 'SUNSET HIGHWAY', '#ff9e3d', 'rock', 'chart_rock.json', world_rock(),
          hero_sheet(gh_draw(ROCKER, RA, '#e8344e', '#9e1c35', (RA['H'], 8)), 12, 50, 32, 12, 30, 22, 34),
          enemy_sheet([spr_air(BAT, BPAL), spr_air(DRONE, ODPAL), spr_ground(AMP, APAL)]),
          note_sheet('beam', ['#ff9e3d', '#ffe066']), buddy_rock()),
    stage('3-1', 'METAL', 'MOLTEN KEEP', 'FORGE OF FURY', '#ff3b3b', 'metal', 'chart_metal.json', world_metal(),
          hero_sheet(dwarf_body, 8, 30, 26, 6, 24, 20, 40),
          enemy_sheet([spr_air(BAT, BBPAL), fire_air, spr_ground(SKEL, SPAL)]),
          note_sheet('drum', ['#ff3b3b', '#ffffff']), buddy_metal(), attack='hammer', hammer_=hammer_sheet([70, -20, 0, 30, 50]), mb=miniboss(troll, 'TROLL DRUMMER', 38.4)),
    stage('4-1', 'GOTH ROCK', 'RAVENMOOR', 'MOONLIT GRAVES', '#b06bff', 'goth', 'chart_goth.json', world_goth(),
          hero_sheet(gh_draw(GOTHSPR, GTPAL, '#7a3ab0', '#2a1f3a'), 12, 50, 32, 12, 30, 20, 34),
          enemy_sheet([spr_air(GHOST, GHPAL), spr_air(BAT, PBAT), spr_ground(SKEL, GHOUL)]),
          note_sheet('half', ['#b06bff', '#e8e6f4']), buddy_goth()),
    stage('5-1', 'POWER METAL', 'SKY CITADEL', 'DAWN OF STEEL', '#ffd23f', 'power', 'chart_power.json', world_power(),
          hero_sheet(gh_draw(ROCKER, PWPAL, '#c8ccd8', '#5a5f7a', ('#b0661e', 16)), 12, 54, 34, 14, 32, 24, 34),
          enemy_sheet([wyv_air, spr_air(DRONE, {'K': K, 'C': '#e8344e', 'Y': '#ffe066', 'F': '#ff9e3d'}), spr_ground(KNIGHT, KPAL)]),
          note_sheet('six', ['#ffd23f', '#7fd8ff']), buddy_power()),
]
FONTJS = {k: v for k, v in gen2.FONT.items()}
FONTJS['%'] = "##..#/##..#/...#./..#../.#.../#..##/#..##".split('/')
json.dump({'stages': STAGES, 'font': FONTJS}, open('stages2.json', 'w'), separators=(',', ':'))
for s in STAGES:
    print(s['id'], len(s['chart']), 'notes', 'buddy', s['buddy']['kind'])
import os
print('stages2.json', round(os.path.getsize('stages2.json') / 1e3), 'kB')
