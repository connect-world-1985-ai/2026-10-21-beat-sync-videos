"""Video 2 — Pastel Pop: bouncy anime-style kinetic typography on Kevin MacLeod's "Pixel Peeker Polka - faster"."""
import sys, math, numpy as np
from PIL import Image, ImageDraw
from engine import *

W, H, FPS = 1920, 1080, 30
S = Sync("v2_polka", FPS)
AUDIO = f"{ROOT}/2026-10-21-build/audio/v2_polka.wav"
OUT = f"{ROOT}/2026-10-21-v2-pastel-pop/2026-10-21-v2-pastel-pop.mp4"
ATTR = '♪ "Pixel Peeker Polka - faster" by Kevin MacLeod (incompetech.com) · CC BY 3.0 · creativecommons.org/licenses/by/3.0'

PHRASES = [
 "Hello! | おはよう! | 今日も | いい天気",
 "Let's | GO! | キラキラ | ☆ | 未来へ!",
 "Jump! | Jump! | ぴょん | ぴょん!",
 "笑顔で | Smile! | Happy | ♡ | Day!",
 "一、 | 二、 | 三、 | GO!",
 "Sugar | Sparkle | Star | ☆ | Power!",
 "がんばれ | がんばれ | 負けないで! | Fight!",
 "Dance | Dance | Dance | ♪ | ♪",
 "夢は | きっと | 叶う! | Dreams | Come | True!",
 "Rainbow | 彩虹 | にじいろ | ☆",
 "Mochi | Mochi | もちもち | Pudding!",
 "1 | 2 | 3 | 4 | Polka!",
 "ありがとう | Thank | You | 谢谢!",
 "Again! | もう一回! | Let's | GO!",
]
WORDS = [w.strip() for p in PHRASES for w in p.split("|")]
COLS = [(255, 105, 180), (120, 140, 255), (60, 200, 170), (255, 150, 60), (180, 100, 255), (255, 90, 120), (70, 170, 255)]

def build_schedule():
    ev = []
    for s in S.sections:
        b = S.schedule(S.beats, s["start"], s["end"], 1 if s["level"] == "high" else 2); ev += list(b)
    ev = sorted(set(round(x, 4) for x in ev)); ev = [x for x in ev if x < S.dur - 4.5]
    return ev
STARTS = build_schedule()
SF = np.round(np.array(STARTS) * FPS)

GRADS = [((255, 214, 232), (214, 226, 255)), ((210, 255, 236), (255, 236, 210)), ((236, 220, 255), (255, 220, 236)), ((255, 248, 205), (210, 240, 255))]
GIM = [to_img(vgrad(W, H, a, b)) for a, b in GRADS]
# dot tile layer
DOTS = Image.new("RGBA", (W + 240, H + 240), (0, 0, 0, 0)); dd = ImageDraw.Draw(DOTS)
for yy in range(0, H + 240, 120):
    for xx in range(0, W + 240, 120):
        o = 60 if (yy // 120) % 2 else 0; dd.ellipse((xx + o - 16, yy - 16, xx + o + 16, yy + 16), fill=(255, 255, 255, 110))
rng = np.random.default_rng(3)
SPK = rng.uniform(0, 1, (len(S.beats), 4, 3))

def star(d, x, y, r, col, a):
    pts = []
    for k in range(8):
        ang = k * math.pi / 4; rr = r if k % 2 == 0 else r * 0.28; pts.append((x + rr * math.cos(ang), y + rr * math.sin(ang)))
    d.polygon(pts, fill=col + (a,))

def word_img(w, col, size):
    fn = "fredoka" if all(ord(c) < 128 for c in w) else "sans_cjk_jp"
    return text_img(w, fn, size, col + (255,), stroke=14, stroke_fill=(255, 255, 255, 255))

def frame(i):
    t = i / FPS; e = S.e(t)
    tdb, kdb = S.last(S.down, t); kk = max(kdb, 0)
    g0, g1 = GIM[(kk // 4) % 4], GIM[(kk // 4 + 1) % 4]
    base = Image.blend(g0, g1, 0.5 + 0.5 * math.sin(t * 0.25)).copy()
    off = int((t * 60) % 120)
    base.alpha_composite(DOTS.crop((off, off, off + W, off + H)))
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    # sparkles spawned on each recent beat (more of them when energy is high)
    tb, kb = S.last(S.beats, t)
    for j in range(max(0, kb - 5), kb + 1):
        age = t - S.q(S.beats[j]); n = 2 + int(2 * e)
        for m in range(n):
            u = SPK[j, m]; x = u[0] * W; y = u[1] * H * 0.9; r = (30 + 50 * u[2]) * back_out(age / 0.25) * clamp(1 - age / 1.6)
            if r > 1: star(d, x, y - age * 40, r, COLS[(j + m) % len(COLS)] if m % 2 else (255, 255, 255), int(230 * clamp(1 - age / 1.6)))
    # ring burst on strong hits
    th, kh = S.last(S.hits, t); ah = t - S.q(th)
    if 0 <= ah < 0.6:
        rr = 200 + 900 * ease_out(ah / 0.6); d.ellipse((W / 2 - rr, H / 2 - rr, W / 2 + rr, H / 2 + rr), outline=(255, 255, 255, int(200 * (1 - ah / 0.6))), width=18)
    base.alpha_composite(lay)
    # the word
    k = int(np.searchsorted(SF, i, side="right") - 1)
    if k >= 0:
        age = t - S.q(STARTS[k]); w = WORDS[k % len(WORDS)]; col = COLS[k % len(COLS)]
        size = 260 if len(w) <= 4 else (200 if len(w) <= 7 else 150)
        im = word_img(w, col, size)
        sx = 0.45 + 0.55 * back_out(age / 0.22, 2.6); sy = sx * (1 + 0.18 * math.sin(age * 28) * decay(age, 7))  # squash & stretch
        bounce = -abs(math.sin(age * math.pi / 0.42)) * 30 * decay(age, 2)
        im2 = im.resize((max(1, int(im.width * sx)), max(1, int(im.height * sy))), Image.BILINEAR)
        rot = (6 if k % 2 else -6) * decay(age, 3)
        shadow = text_img(w, "fredoka" if all(ord(c) < 128 for c in w) else "sans_cjk_jp", size, (120, 60, 140, 90), stroke=14, stroke_fill=(120, 60, 140, 90))
        paste(base, shadow, W / 2 + 14, H / 2 + 18 + bounce, sx, 1.0, rot)
        paste(base, im2, W / 2, H / 2 + bounce, 1.0, 1.0, rot)
        # previous word slides away small at the top-left (gives a "lyric trail")
        if k > 0 and age < 0.3:
            pim = word_img(WORDS[(k - 1) % len(WORDS)], COLS[(k - 1) % len(COLS)], 90)
            paste(base, pim, W / 2 - 600 * ease_out(age / 0.3), H / 2 - 300, 1.0, 1 - age / 0.3)
    # beat dots indicator (4 dots, lights the current beat in the bar)
    if kb >= 0:
        pos = (kb - S.d["downbeat_phase"]) % 4; d2 = ImageDraw.Draw(base)
        for m in range(4):
            x = W / 2 - 90 + m * 60; r = 14 if m != pos else 14 + 8 * decay(t - S.q(tb), 6)
            d2.ellipse((x - r, H - 120 - r, x + r, H - 120 + r), fill=(255, 255, 255, 255) if m == pos else (255, 255, 255, 120))
    paste(base, text_img(ATTR, "sans_cjk_r", 22, (110, 70, 130, 255)), W / 2, H - 40)
    fade = clamp(t / 0.5) * clamp((S.dur - t) / 2.5)
    if fade < 1: base.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(255 * (1 - fade)))))
    return base

if __name__ == "__main__":
    import os; os.makedirs(os.path.dirname(OUT), exist_ok=True)
    pv = (float(sys.argv[1]), float(sys.argv[2])) if len(sys.argv) > 2 else None
    out = OUT if not pv else "/tmp/bsv/v2_preview.mp4"
    render(out, W, H, FPS, S.dur, AUDIO, frame, preview=pv); print(out)
