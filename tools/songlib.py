import json
import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter

SR = 44100
NOTE = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8,
        'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}


def n(s):
    return 12 * (int(s[-1]) + 1) + NOTE[s[:-1]]


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def polyblep(t, dt):
    out = np.zeros_like(t)
    m = t < dt
    x = t[m] / dt[m]
    out[m] = x + x - x * x - 1
    m = t > 1 - dt
    x = (t[m] - 1) / dt[m]
    out[m] = x * x + x + x + 1
    return out


def pulse(freq, duty):
    dt = freq / SR
    ph = np.cumsum(dt) % 1.0
    y = np.where(ph < duty, 1.0, -1.0)
    y += polyblep(ph, dt)
    y -= polyblep((ph + 1 - duty) % 1.0, dt)
    return y


def tri(freq):
    ph = np.cumsum(freq / SR) % 1.0
    return np.round((4 * np.abs(ph - 0.5) - 1) * 7.5) / 7.5


def adsr(hold, a, d, s, r):
    nh, nr = int(hold * SR), int(r * SR)
    t = np.arange(nh + nr) / SR
    e = np.full(len(t), s)
    if a > 0:
        m = t < a
        e[m] = t[m] / a
    m = (t >= a) & (t < a + d)
    e[m] = 1 - (1 - s) * (t[m] - a) / d
    lvl = (hold / a if hold < a else (1 - (1 - s) * (hold - a) / d if hold < a + d else s))
    m = t >= hold
    e[m] = lvl * np.maximum(0, 1 - (t[m] - hold) / r) if r > 0 else 0
    return np.round(e * 15) / 15


class Song:
    def __init__(self, bpm, bars, seed=7, tail=4.0):
        self.bpm = bpm
        self.STEP = 60 / bpm / 4
        self.BAR = 16 * self.STEP
        self.N = int(SR * (bars * self.BAR + tail))
        self.L = np.zeros(self.N); self.R = np.zeros(self.N); self.ECHO = np.zeros(self.N)
        self.rng = np.random.default_rng(seed)
        self.metal = self.rng.uniform(-1, 1, 93)
        self.ev = {'lead': [], 'kick': [], 'snare': [], 'crash': [], 'marks': {}}

    def T(self, bar, step=0):
        return bar * self.BAR + step * self.STEP

    def add(self, y, t0, gain, pan=0.0, bus=None):
        i0 = int(round(t0 * SR))
        if i0 >= self.N:
            return
        y = y[:self.N - i0]
        if bus is not None:
            bus[i0:i0 + len(y)] += y * gain
            return
        ang = (pan + 1) * np.pi / 4
        self.L[i0:i0 + len(y)] += y * gain * np.cos(ang)
        self.R[i0:i0 + len(y)] += y * gain * np.sin(ang)

    def noise(self, k, hold):
        v = self.rng.uniform(-1, 1, k // hold + 2)
        return np.repeat(v, hold)[:k]

    # ---------- voices ----------
    def lead(self, m, t0, dur, gain=0.2, duty=0.25, vib=0.004, rec=True, echo=True, pan=0.0, a=0.004, s=0.7):
        if rec:
            self.ev['lead'].append((t0, dur, m))
        e = adsr(dur * 0.92, a, 0.12, s, 0.06)
        t = np.arange(len(e)) / SR
        v = 1 + vib * np.sin(2 * np.pi * 6 * t) * np.clip((t - 0.15) / 0.2, 0, 1)
        y = pulse(mtof(m) * v, duty) * e
        if echo:
            self.add(y, t0, gain, bus=self.ECHO)
        else:
            self.add(y, t0, gain, pan)

    def arp(self, m, t0, gain=0.07, pan=-0.45, duty=0.125, length=None):
        e = adsr((length or self.STEP) * 0.9, 0.002, 0.09, 0.3, 0.03)
        self.add(pulse(np.full(len(e), mtof(m)), duty) * e, t0, gain, pan)

    def bass(self, m, t0, dur, gain=0.28, bright=0.22):
        e = adsr(dur * 0.85, 0.002, 0.08, 0.8, 0.02)
        f = np.full(len(e), mtof(m))
        self.add((tri(f) + bright * pulse(f, 0.5)) * e, t0, gain)

    def power(self, root, t0, dur, gain=0.11, mute=False, pan=0.0):
        hold = min(dur * 0.9, 0.07) if mute else dur * 0.92
        e = adsr(hold, 0.002, 0.05, 0.85, 0.04 if mute else 0.08)
        y = np.zeros(len(e))
        for k, iv in enumerate((0, 7, 12)):
            f = np.full(len(e), mtof(root + iv)) * (1 + 0.002 * (k - 1))
            y += pulse(f, 0.5) * (1.0 if k < 2 else 0.6)
        y = np.tanh(y * 1.8) / np.tanh(1.8 * 2.6)
        a = np.exp(-2 * np.pi * (3200 if mute else 5200) / SR)
        y = lfilter([1 - a], [1, -a], y)
        self.add(y * e, t0, gain * (0.85 if mute else 1.0), pan)

    def organ(self, ms, t0, dur, gain=0.03, pan_spread=0.35, rate=5.0):
        e = adsr(dur, 0.12, 0.2, 0.75, 0.3)
        t = np.arange(len(e)) / SR
        for i, m in enumerate(ms):
            trem = 1 + 0.2 * np.sin(2 * np.pi * rate * t + i)
            f = np.full(len(e), mtof(m))
            y = (pulse(f * 1.002, 0.25) + pulse(f * 0.998, 0.125)) * 0.5 * e * trem
            self.add(y, t0, gain, pan_spread if i % 2 else -pan_spread)

    def bell(self, m, t0, gain=0.05, pan=0.3):
        k = int(0.6 * SR)
        t = np.arange(k) / SR
        f = np.full(k, mtof(m))
        y = (tri(f) * 0.7 + pulse(f * 2.001, 0.125) * 0.3) * np.exp(-t * 6)
        self.add(y, t0, gain, pan)

    # ---------- drums ----------
    def kick(self, t0, gain=0.55, rec=True):
        if rec:
            self.ev['kick'].append(t0)
        k = int(0.2 * SR); t = np.arange(k) / SR
        f = 42 + 120 * np.exp(-t * 32)
        self.add(tri(f) * np.exp(-t * 14) + self.noise(k, 2) * np.exp(-t * 380) * 0.35, t0, gain)

    def snare(self, t0, gain=0.3, clap=False, rec=True):
        if rec:
            self.ev['snare'].append(t0)
        k = int(0.18 * SR); t = np.arange(k) / SR
        y = self.noise(k, 3) * np.exp(-t * 20) + 0.45 * tri(np.full(k, 185.0)) * np.exp(-t * 38)
        if clap:
            for off in (0.011, 0.022):
                j = int(off * SR)
                y[j:] += self.noise(k - j, 2) * np.exp(-t[:k - j] * 60) * 0.6
        self.add(y, t0, gain, 0.1)

    def tom(self, t0, m=45, gain=0.35):
        k = int(0.3 * SR); t = np.arange(k) / SR
        f = mtof(m) * (1 + 0.6 * np.exp(-t * 18))
        self.add(tri(f) * np.exp(-t * 9), t0, gain, -0.2)

    def hat(self, t0, gain=0.07, open_=False):
        k = int((0.14 if open_ else 0.04) * SR); t = np.arange(k) / SR
        self.add(np.resize(self.metal, k) * np.exp(-t * (22 if open_ else 110)), t0, gain, 0.3)

    def crash(self, t0, gain=0.11, rec=True):
        if rec:
            self.ev['crash'].append(t0)
        k = int(1.4 * SR); t = np.arange(k) / SR
        self.add((self.noise(k, 1) * 0.6 + np.resize(self.metal, k) * 0.4) * np.exp(-t * 3.2), t0, gain, -0.2)

    def mark(self, name, t):
        self.ev['marks'].setdefault(name, []).append(t)

    # ---------- output ----------
    def finish(self, name, end_t, echo_steps=3, fb=(0.32, 0.18, 0.1), lowpass=14000):
        d = int(echo_steps * self.STEP * SR)
        self.L += self.ECHO * 0.75; self.R += self.ECHO * 0.75
        for i, (gn, side) in enumerate(zip(fb, ('R', 'L', 'R')), start=1):
            sh = np.zeros(self.N); sh[i * d:] = self.ECHO[:self.N - i * d]
            if side == 'R':
                self.R += sh * gn
            else:
                self.L += sh * gn
        st = np.stack([self.L, self.R], axis=1)
        a = np.exp(-2 * np.pi * lowpass / SR)
        st = lfilter([1 - a], [1, -a], st, axis=0)
        st -= st.mean(axis=0)
        st = np.tanh(st / np.max(np.abs(st)) * 1.15)
        st = st / np.max(np.abs(st)) * 0.89
        end = int(SR * (end_t + 2.2)); fade = int(SR * 0.4)
        st = st[:end]; st[-fade:] *= np.linspace(1, 0, fade)[:, None]
        wavfile.write(f'{name}.wav', SR, (st * 32767).astype(np.int16))
        self.ev['end'] = end_t; self.ev['step'] = self.STEP; self.ev['bpm'] = self.bpm
        json.dump(self.ev, open(f'{name}_events.json', 'w'))
        return len(st) / SR


# ================= v2 additions: reverb, chorus, shouts, fills, harmony =================
from scipy.signal import butter


def comb(x, d, g):
    y = np.zeros_like(x)
    for i in range(0, len(x), d):
        j = min(i + d, len(x))
        prev_x = x[i - d:j - d] if i >= d else np.concatenate([np.zeros(d - i), x[:j - d]]) if j - d > 0 else np.zeros(j - i)
        prev_y = y[i - d:j - d] if i >= d else np.zeros(j - i)
        if len(prev_x) < j - i:
            prev_x = np.concatenate([np.zeros(j - i - len(prev_x)), prev_x])
        y[i:j] = prev_x + g * prev_y
    return y


def allpass(x, d, g):
    y = np.zeros_like(x)
    for i in range(0, len(x), d):
        j = min(i + d, len(x))
        px = x[i - d:j - d] if i >= d else np.zeros(j - i)
        py = y[i - d:j - d] if i >= d else np.zeros(j - i)
        y[i:j] = -g * x[i:j] + px + g * py
    return y


def reverb(x, delays=(1557, 1617, 1491, 1422), g=0.82):
    out = sum(comb(x, d, g) for d in delays) / len(delays)
    for d in (225, 556):
        out = allpass(out, d, 0.5)
    return out


class Song2(Song):
    def __init__(self, bpm, bars, seed=7, tail=4.0):
        super().__init__(bpm, bars, seed, tail)
        self.REV = np.zeros(self.N)
        self.CHO = np.zeros(self.N)

    def send(self, y, t0, gain, amt):
        if amt > 0:
            self.add(y, t0, gain * amt, bus=self.REV)

    def lead2(self, m, t0, dur, gain=0.19, duty=0.25, vib=0.004, rec=True, rev=0.3, pan=0.0, echo=True):
        if rec:
            self.ev['lead'].append((t0, dur, m))
        e = adsr(dur * 0.92, 0.004, 0.12, 0.72, 0.07)
        t = np.arange(len(e)) / SR
        v = 1 + vib * np.sin(2 * np.pi * 5.5 * t) * np.clip((t - 0.12) / 0.2, 0, 1)
        y = pulse(mtof(m) * v, duty) * e
        if echo:
            self.add(y, t0, gain, bus=self.ECHO)
        else:
            self.add(y, t0, gain, pan)
        self.send(y, t0, gain, rev)

    def pad(self, ms, t0, dur, gain=0.03, rate=4.0, rev=0.5, duty=0.25):
        e = adsr(dur, 0.18, 0.25, 0.75, 0.35)
        t = np.arange(len(e)) / SR
        for i, m in enumerate(ms):
            trem = 1 + 0.18 * np.sin(2 * np.pi * rate * t + i)
            f = np.full(len(e), mtof(m))
            y = (pulse(f * 1.003, duty) + pulse(f * 0.997, 0.5)) * 0.5 * e * trem
            self.add(y, t0, gain, 0.4 if i % 2 else -0.4)
            self.send(y, t0, gain, rev)

    def chorus_gtr(self, m, t0, dur, gain=0.07):
        e = adsr(dur * 0.9, 0.003, 0.15, 0.4, 0.1)
        y = pulse(np.full(len(e), mtof(m)), 0.18) * e
        self.add(y, t0, gain, bus=self.CHO)
        self.send(y, t0, gain, 0.4)

    def hey(self, t0, gain=0.22):
        k = int(0.2 * SR); t = np.arange(k) / SR
        b, a = butter(2, [700 / (SR / 2), 1700 / (SR / 2)], btype='band')
        nz = lfilter(b, a, self.noise(k, 1))
        f = 190 * (1 - 0.15 * t / 0.2)
        y = (nz * 2.5 + 0.5 * pulse(f, 0.3) + 0.3 * pulse(f * 1.5, 0.3)) * np.exp(-t * 9) * np.clip(t / 0.01, 0, 1)
        for pan in (-0.4, 0.0, 0.4):
            self.add(y, t0 + 0.006 * (pan + 0.4) * 2, gain * 0.5, pan)
        self.send(y, t0, gain, 0.4)

    def fill(self, bar, kind='snare', gain=0.28, start=8):
        t = self.T(bar)
        for s in range(start, 16):
            if kind == 'snare':
                self.snare(t + s * self.STEP, gain=0.12 + gain * (s - start) / (16 - start), rec=(s % 4 == 0))
            else:
                self.tom(t + s * self.STEP, 50 - (s - start), gain=0.3)

    def finish2(self, name, end_t, rev_wet=0.22, cho=False, **kw):
        if cho:
            n_ = np.arange(self.N)
            for side, ph in (('L', 0.0), ('R', 1.7)):
                dly = (0.012 + 0.004 * np.sin(2 * np.pi * 0.8 * n_ / SR + ph)) * SR
                y = np.interp(n_ - dly, n_, self.CHO)
                if side == 'L':
                    self.L += y + self.CHO * 0.4
                else:
                    self.R += y + self.CHO * 0.4
        wl = reverb(self.REV, (1557, 1617, 1491, 1422))
        wr = reverb(self.REV, (1617, 1557, 1356, 1277))
        self.L += wl * rev_wet * 3; self.R += wr * rev_wet * 3
        return self.finish(name, end_t, **kw)


SCALES = {'Am': [9, 11, 0, 2, 4, 5, 7], 'A': [9, 11, 1, 2, 4, 6, 7], 'Em': [4, 6, 7, 9, 11, 0, 2], 'Dm': [2, 4, 5, 7, 9, 10, 0]}


def third_below(m, key):
    sc = SCALES[key]
    pc = m % 12
    if pc not in sc:
        return m - 4
    i = sc.index(pc)
    tpc = sc[(i - 2) % 7]
    d = (pc - tpc) % 12
    return m - d
