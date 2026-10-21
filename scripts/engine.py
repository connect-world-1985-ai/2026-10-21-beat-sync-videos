"""Shared rendering engine: sync data, text cache, easing, parallel ffmpeg render."""
import json, os, subprocess, math, functools, multiprocessing as mp
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = "/usr/share/fonts/truetype/sand-box/google"
FONTS = {
    "serif_cjk": ("/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc", 2, None),
    "serif_cjk_r": ("/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc", 2, None),
    "sans_cjk": ("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 2, None),
    "sans_cjk_jp": ("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 0, None),
    "sans_cjk_r": ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 2, None),
    "cinzel": (f"{G}/Cinzel/Cinzel-VariableFont_wght.ttf", 0, 700),
    "fredoka": (f"{G}/Fredoka/Fredoka-VariableFont_wdth,wght.ttf", 0, None),
    "pixel": (f"{G}/Press Start 2P/PressStart2P-Regular.ttf", 0, None),
    "mono": (f"{G}/JetBrains Mono/JetBrainsMono-VariableFont_wght.ttf", 0, 500),
    "mono_cjk": ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 7, None),
    "dvmono": ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 0, None),
    "dvmono_b": ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 0, None),
    "bangers": (f"{G}/Bangers/Bangers-Regular.ttf", 0, None),
}

@functools.lru_cache(maxsize=256)
def font(name, size):
    path, idx, wght = FONTS[name]
    f = ImageFont.truetype(path, size, index=idx)
    if wght is not None:
        try:
            axes = f.get_variation_axes(); f.set_variation_by_axes([wght] + [a["default"] for a in axes[1:]])
        except Exception: pass
    if name == "fredoka":
        try: f.set_variation_by_name("Bold")
        except Exception: pass
    return f

@functools.lru_cache(maxsize=2048)
def text_img(text, fname, size, fill=(255, 255, 255, 255), stroke=0, stroke_fill=(0, 0, 0, 255), spacing=0, glow=0, glow_color=None):
    """Render text to a tight RGBA image (optionally with soft glow)."""
    f = font(fname, size)
    pad = stroke + glow * 2 + 4
    if spacing:
        widths = [f.getbbox(ch)[2] for ch in text]
        w = int(sum(widths) + spacing * (len(text) - 1)) + 2 * pad
    else:
        b = f.getbbox(text, stroke_width=stroke); w = b[2] + 2 * pad
    asc, desc = f.getmetrics(); h = asc + desc + 2 * pad
    im = Image.new("RGBA", (max(w, 1), h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if spacing:
        x = pad
        for ch, cw in zip(text, widths):
            d.text((x, pad), ch, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill); x += cw + spacing
    else:
        d.text((pad, pad), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    if glow:
        a = im.split()[3].filter(ImageFilter.GaussianBlur(glow))
        gc = glow_color or fill[:3]
        g = Image.new("RGBA", im.size, gc + (0,)); g.putalpha(a.point(lambda v: min(255, int(v * 1.6))))
        g.alpha_composite(im); im = g
    return im

def paste(base, im, cx, cy, scale=1.0, alpha=1.0, rot=0.0):
    """Alpha-composite RGBA `im` centered at (cx, cy) onto RGBA `base`."""
    if alpha <= 0.003: return
    if abs(scale - 1) > 1e-3:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if rot: im = im.rotate(rot, resample=Image.BILINEAR, expand=True)
    if alpha < 0.999:
        a = im.split()[3].point(lambda v: int(v * alpha)); im = im.copy(); im.putalpha(a)
    base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2))) if _fits(base, im, cx, cy) else _safe_paste(base, im, cx, cy)

def _fits(base, im, cx, cy):
    x, y = int(cx - im.width / 2), int(cy - im.height / 2)
    return x >= 0 and y >= 0 and x + im.width <= base.width and y + im.height <= base.height

def _safe_paste(base, im, cx, cy):
    x, y = int(cx - im.width / 2), int(cy - im.height / 2)
    l, t = max(0, -x), max(0, -y); r, b = min(im.width, base.width - x), min(im.height, base.height - y)
    if r > l and b > t: base.alpha_composite(im.crop((l, t, r, b)), (x + l, y + t))

# easing
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def ease_in_out(x): x = clamp(x); return 3 * x * x - 2 * x * x * x
def back_out(x, s=1.9): x = clamp(x) - 1; return 1 + (s + 1) * x ** 3 + s * x ** 2
def decay(age, k): return math.exp(-k * age) if age >= 0 else 0.0
def lerp(a, b, t): return a + (b - a) * t
def lerpc(c1, c2, t): return tuple(int(lerp(a, b, t)) for a, b in zip(c1, c2))

class Sync:
    """Beat/energy data loaded from analysis JSON(s)."""
    def __init__(self, name, fps, override=None):
        d = json.load(open(f"{ROOT}/2026-10-21-analysis/{name}.json"))
        if override: d.update(override)
        self.d = d; self.fps = fps; self.dur = d["duration"]
        self.beats = np.array(d["beat_times"]); self.down = np.array(d["downbeat_times"])
        self.hits = np.array(d["strong_hits"]); self.energy = np.array(d["energy"])
        self.bstr = np.array(d["beat_strength"]) if len(d["beat_strength"]) == len(self.beats) else np.ones(len(self.beats))
        self.sections = d["sections"]
    def f(self, t):  # frame index of a time (text changes land exactly on this frame)
        return int(round(t * self.fps))
    def q(self, t):  # quantize time to frame grid
        return self.f(t) / self.fps
    def e(self, t):
        i = t * 2.0; i0 = int(clamp(math.floor(i), 0, len(self.energy) - 1)); i1 = min(i0 + 1, len(self.energy) - 1)
        return float(lerp(self.energy[i0], self.energy[i1], i - math.floor(i)))
    def last(self, arr, t):
        """(time, index) of most recent event in arr at or before t (frame-quantized)."""
        k = np.searchsorted(np.round(arr * self.fps), round(t * self.fps), side="right") - 1
        return (float(arr[k]), int(k)) if k >= 0 else (-1e9, -1)
    def beat_age(self, t, arr=None):
        arr = self.beats if arr is None else arr
        tb, k = self.last(arr, t); return (t - self.q(tb)) if k >= 0 else 1e9
    def level(self, t):
        for s in self.sections:
            if s["start"] <= t < s["end"]: return s["level"]
        return self.sections[-1]["level"]
    def nearest(self, arr, t):
        return float(arr[np.argmin(np.abs(arr - t))])
    def schedule(self, arr, start, end, every=1):
        a = arr[(arr >= start - 1e-6) & (arr < end)]; return a[::every]

# ---------- parallel render ----------
_FRAME_FN = None
def _worker(args):
    k, i0, i1, W, H, fps, path = args
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
           "-c:v", "libx264", "-preset", "medium", "-crf", os.environ.get("CRF", "23"), "-pix_fmt", "yuv420p", "-g", str(fps * 2), path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(i0, i1):
        fr = _FRAME_FN(i)
        if isinstance(fr, Image.Image): fr = np.asarray(fr.convert("RGB"))
        p.stdin.write(np.ascontiguousarray(fr, dtype=np.uint8).tobytes())
    p.stdin.close(); p.wait(); return k

def render(out, W, H, fps, dur, audio, frame_fn, workers=8, preview=None):
    """Render frames in parallel chunks, concat, mux AAC audio. preview=(t0,t1) renders a slice."""
    global _FRAME_FN; _FRAME_FN = frame_fn
    n = int(round(dur * fps)); f0, f1 = (0, n) if not preview else (int(preview[0] * fps), int(preview[1] * fps))
    tmp = out + ".parts"; os.makedirs(tmp, exist_ok=True)
    chunks = np.linspace(f0, f1, workers * 3 + 1).astype(int)
    jobs = [(k, chunks[k], chunks[k + 1], W, H, fps, f"{tmp}/p{k:03d}.mp4") for k in range(len(chunks) - 1) if chunks[k + 1] > chunks[k]]
    with mp.get_context("fork").Pool(workers) as pool:
        for k in pool.imap_unordered(_worker, jobs): pass
    with open(f"{tmp}/list.txt", "w") as fh:
        for j in jobs: fh.write(f"file '{os.path.abspath(j[6])}'\n")
    ss = ["-ss", str(f0 / fps), "-t", str((f1 - f0) / fps)]
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{tmp}/list.txt", *ss, "-i", audio,
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out], check=True)
    subprocess.run(["rm", "-rf", tmp])
    return out

# ---------- shared visual helpers ----------
def vgrad(W, H, top, bottom, gamma=1.0):
    t = (np.linspace(0, 1, H) ** gamma)[:, None, None]
    return (np.array(top, float)[None, None] * (1 - t) + np.array(bottom, float)[None, None] * t) * np.ones((1, W, 1))

def to_img(arr):
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB").convert("RGBA")

def wrap_cjk(s, n):
    return [s[i:i + n] for i in range(0, len(s), n)]
