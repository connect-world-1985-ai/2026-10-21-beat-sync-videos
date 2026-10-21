"""Video 1 — 人类之光 Light of Humanity. Epic cinematic bilingual title cards on Kevin MacLeod's "Crusade"."""
import sys, math, numpy as np
from PIL import Image, ImageDraw
from engine import *

W, H, FPS = 1920, 1080, 30
S = Sync("v1_crusade", FPS)
AUDIO = f"{ROOT}/2026-10-21-build/audio/v1_crusade.wav"
OUT = f"{ROOT}/2026-10-21-v1-light-of-humanity/2026-10-21-v1-light-of-humanity.mp4"
ATTR = 'Music: "Crusade" by Kevin MacLeod (incompetech.com) · Licensed under CC BY 3.0 · creativecommons.org/licenses/by/3.0'

LINES = [
 ("人类之光", "LIGHT OF HUMANITY"), ("在漫长的黑夜里", "In the long night"), ("我们抬头", "we looked up"),
 ("看见了星辰", "and saw the stars"), ("我们点燃火焰", "We kindled fire"), ("驱散寒冷与恐惧", "against cold and fear"),
 ("我们刻下符号", "We carved symbols"), ("让记忆跨越千年", "so memory could cross millennia"), ("我们筑起城市", "We raised cities"),
 ("修建道路与桥梁", "built roads and bridges"), ("我们追问", "We asked"), ("世界从何而来", "where the world came from"),
 ("答案藏在数字里", "Answers hid in numbers"), ("藏在望远镜里", "in telescopes"), ("藏在每一次失败里", "in every failure"),
 ("我们学会了", "We learned"), ("一起前行", "to move forward together"),
 # high section — one card per downbeat
 ("光", "LIGHT"), ("是勇气", "is courage"), ("是好奇", "is curiosity"), ("是怜悯", "is compassion"),
 ("我们驶向未知的海洋", "We sailed unknown seas"), ("我们治愈疾病", "We healed disease"), ("我们驯服闪电", "We tamed lightning"),
 ("我们飞上天空", "We took to the sky"), ("我们踏上月球", "We walked on the Moon"), ("我们连接彼此", "We connected each other"),
 ("七十亿个梦想", "Billions of dreams"), ("一个家园", "one home"), ("每一个孩子", "Every child"), ("都是一束光", "is a ray of light"),
 ("每一次相助", "Every helping hand"), ("都是一束光", "is a ray of light"), ("当黑暗再次来临", "When darkness returns"),
 ("我们不会熄灭", "we will not go out"), ("因为光", "Because light"), ("会传递", "is passed on"),
 ("从祖先", "from our ancestors"), ("到我们", "to us"), ("到未来", "to the future"), ("人类之光", "LIGHT OF HUMANITY"),
 ("永不熄灭", "NEVER FADES"),
 # outro (mid / low)
 ("向前", "Onward"), ("向上", "Upward"), ("向光", "Toward the light"), ("人类之光", "LIGHT OF HUMANITY"),
]

def spread(arr, n):
    """pick n events spread evenly over arr (all of them are real detected downbeats)."""
    idx = np.round(np.linspace(0, len(arr) - 1, n + 1)[:-1]).astype(int) if len(arr) > n else np.arange(len(arr))
    return list(arr[idx])

def build_schedule():
    d = S.down
    a = spread(d[d < 95.5], 17); a[0] = S.nearest(S.beats, 0.07)
    b = list(d[(d >= 95.5) & (d < 163)])[:25]
    c = spread(d[(d >= 163) & (d < 193)], 4)
    return a + b + c

STARTS = build_schedule()
print("cards", len(STARTS), "of", len(LINES), "last start", STARTS[-1])

# precomputed background maps (half resolution)
w2, h2 = W // 2, H // 2
yy, xx = np.mgrid[0:h2, 0:w2].astype(np.float32)
cx, cy = w2 / 2, h2 * 0.78
TH = np.arctan2(yy - cy, xx - cx); R = np.hypot(xx - cx, yy - cy) / w2
_by = np.linspace(0, 1, H)[:, None]; _bx = np.linspace(-1, 1, W)[None, :]
BAND = Image.fromarray(np.dstack([np.zeros((H, W, 3), np.uint8), (np.exp(-((_by - 0.5) / 0.2) ** 4) * np.exp(-(_bx / 0.7) ** 6) * 120).astype(np.uint8)]), "RGBA")
rng = np.random.default_rng(7)
NP = 260; PX = rng.uniform(0, W, NP); PY = rng.uniform(0, H, NP); PV = rng.uniform(15, 60, NP); PS = rng.uniform(1.5, 4.5, NP); PPH = rng.uniform(0, 6.28, NP)
PAL = [((6, 8, 24), (30, 20, 60)), ((12, 18, 50), (120, 60, 40)), ((25, 30, 75), (220, 130, 55)), ((40, 50, 100), (225, 160, 80)), ((20, 20, 40), (200, 120, 60))]

def sky(t):
    p = t / S.dur * (len(PAL) - 1); i = int(min(p, len(PAL) - 2)); f = ease_in_out(p - i)
    top = lerpc(PAL[i][0], PAL[i + 1][0], f); bot = lerpc(PAL[i][1], PAL[i + 1][1], f); return top, bot

def background(t):
    e = S.e(t); top, bot = sky(t)
    g = vgrad(w2, h2, top, bot, 0.8)
    rot = t * (0.03 + 0.08 * e)
    rays = (0.5 + 0.5 * np.cos(14 * TH + rot)) ** 6 * np.exp(-R * 1.6) * (0.25 + 0.75 * e)
    bage = S.beat_age(t, S.down); pulse = 0.35 * decay(bage, 3.5) * e
    glow = np.exp(-(R / (0.18 + 0.05 * e + 0.06 * pulse)) ** 2) * (0.7 + pulse)
    col = np.array([255, 220, 160], np.float32)
    g = g + (rays[..., None] * 110 + glow[..., None] * 170) * col / 255
    im = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR).convert("RGBA")
    return im, e

def particles(base, t, e):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    n = int(NP * (0.35 + 0.65 * e))
    zoom = 1 + 0.04 * math.sin(t * 0.1)
    for k in range(n):
        x = (PX[k] - W / 2) * zoom + W / 2 + 20 * math.sin(t * 0.3 + PPH[k]); y = (PY[k] - PV[k] * t) % H
        a = int(120 + 120 * math.sin(t * 2 + PPH[k]) ** 2); r = PS[k] * (0.8 + 0.6 * e)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 230, 180, a))
    base.alpha_composite(lay)

def frame(i):
    t = i / FPS
    base, e = background(t)
    particles(base, t, e)
    base.alpha_composite(BAND)
    k = int(np.searchsorted(np.round(np.array(STARTS) * FPS), i, side="right") - 1)
    if k >= 0:
        t0 = S.q(STARTS[k]); t1 = S.q(STARTS[k + 1]) if k + 1 < len(STARTS) else S.dur
        age = t - t0; span = t1 - t0
        zh, en = LINES[k]; big = zh in ("人类之光", "光", "永不熄灭")
        fs = 170 if big else 120
        zimg = text_img(zh, "serif_cjk", fs, (255, 250, 238, 255), stroke=3, stroke_fill=(70, 35, 5, 255), glow=14, glow_color=(120, 60, 10), spacing=18 if big else 6)
        slow = 1 + 0.06 * age / max(span, 1)                      # slow zoom
        s_in = lerp(1.35, 1.0, ease_out(age / 0.45))                # impact reveal
        out_a = clamp((t1 - t) / 0.25)
        a = clamp(age / 0.18) * out_a
        paste(base, zimg, W / 2, H * 0.43, s_in * slow, a)
        # English line lands on the next beat after the card start
        tb = [b for b in S.beats if S.q(b) > t0 + 0.05]
        te = S.q(tb[0]) if tb and tb[0] < t1 else t0 + 0.3
        if t >= te:
            eimg = text_img(en.upper() if big else en, "cinzel", 60 if big else 50, (255, 240, 215, 255), stroke=2, stroke_fill=(60, 30, 10, 255), spacing=8 if big else 3, glow=8, glow_color=(40, 20, 0))
            ae = ease_out((t - te) / 0.35) * out_a
            paste(base, eimg, W / 2, H * 0.60 + 20 * (1 - ae), slow, ae)
        # flash on card change, stronger in high-energy sections
        fl = (0.55 if S.level(t0) == "high" else 0.25) * decay(age, 7) * (0.4 + e)
        if fl > 0.01: base.alpha_composite(Image.new("RGBA", (W, H), (255, 240, 210, int(255 * clamp(fl)))))
    # letterbox + attribution
    d = ImageDraw.Draw(base); d.rectangle((0, 0, W, 70), fill=(0, 0, 0, 255)); d.rectangle((0, H - 70, W, H), fill=(0, 0, 0, 255))
    paste(base, text_img(ATTR, "sans_cjk_r", 20, (200, 200, 200, 200)), W / 2, H - 35)
    fade = clamp(t / 1.0) * clamp((S.dur - t) / 2.0)
    if fade < 1: base.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * (1 - fade)))))
    return base

if __name__ == "__main__":
    import os; os.makedirs(os.path.dirname(OUT), exist_ok=True)
    pv = (float(sys.argv[1]), float(sys.argv[2])) if len(sys.argv) > 2 else None
    out = OUT if not pv else "/tmp/bsv/v1_preview.mp4"
    render(out, W, H, FPS, S.dur, AUDIO, frame, preview=pv); print(out)
