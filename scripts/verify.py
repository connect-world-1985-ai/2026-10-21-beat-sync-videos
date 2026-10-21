"""Verify a rendered video: ffprobe, beat-change detection in the decoded output, beat-time frames, contact sheet.
Usage: python verify.py v1|v2|v3|v4"""
import sys, json, subprocess, importlib, os, numpy as np
from PIL import Image, ImageDraw
from engine import ROOT, text_img

MOD = {"v1": "v1_light_of_humanity", "v2": "v2_pastel_pop", "v3": "v3_claude_buddy", "v4": "v4_human_epic"}
key = sys.argv[1]; m = importlib.import_module(MOD[key]); FPS = m.FPS
changes = {"v1": lambda: m.STARTS, "v2": lambda: m.STARTS, "v3": lambda: list(np.unique(m.SF) / FPS), "v4": lambda: m.ST}[key]()
changes = [float(c) for c in changes if c > 0.5]
out_dir = os.path.dirname(m.OUT); vid = m.OUT
pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size,bit_rate:stream=codec_name,width,height,r_frame_rate,nb_frames",
                                "-of", "json", vid], capture_output=True, text=True).stdout)
# decode small grayscale frames, compute frame-to-frame difference
w, h = 192, 108
raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", vid, "-vf", f"scale={w}:{h},format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.float32)
diff = np.r_[0, np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))]
res = []
for c in changes:
    f = int(round(c * FPS))
    if f + 2 >= len(diff): continue
    lo = max(0, f - 3); win = diff[lo:f + 4]; peak = int(np.argmax(win)) + lo
    base = float(np.median(diff[max(0, f - 15):max(1, f - 3)]))
    thr = base + 0.25 * (win.max() - base); onset = int(np.argmax(win >= thr)) + lo   # first frame where the change starts
    res.append(dict(t=round(c, 3), frame=f, diff_at=round(float(diff[f]), 2), baseline=round(base, 2), peak_frame=peak, peak_offset=peak - f, onset_frame=onset, offset_frames=onset - f))
offs = np.array([r["offset_frames"] for r in res]); poffs = np.array([r["peak_offset"] for r in res])
within1 = float(np.mean(np.abs(offs) <= 1)) if len(offs) else 0
# beat-tracker accuracy vs. onset peaks (how far each detected beat is from the nearest audio onset)
summary = dict(video=os.path.relpath(vid, ROOT), size_MB=round(int(pr["format"]["size"]) / 1e6, 1), duration_s=round(float(pr["format"]["duration"]), 2),
               streams=[{k: s.get(k) for k in ("codec_name", "width", "height", "r_frame_rate")} for s in pr["streams"]],
               scheduled_changes=len(changes), checked=len(res), visual_change_onset_within_1_frame=round(within1, 3),
               onset_offset_frames_histogram={int(k): int(v) for k, v in zip(*np.unique(offs, return_counts=True))},
               peak_offset_frames_histogram={int(k): int(v) for k, v in zip(*np.unique(poffs, return_counts=True))})
json.dump(dict(summary=summary, changes=res), open(f"{out_dir}/verify_{key}.json", "w"), indent=1)
print(json.dumps(summary, indent=1))
# frames at a few change times: (one frame before, the change frame) pairs
pairs = [res[i] for i in np.linspace(0, len(res) - 1, 6).astype(int)]
tiles = []
for r in pairs:
    for f in (r["frame"] - 1, r["frame"]):
        im = Image.fromarray(np.uint8(0) + 0, "L") if False else None
        png = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", f"{(f + 0.3) / FPS:.4f}", "-i", vid, "-vf", "scale=480:270", "-vframes", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
        import io; t = Image.open(io.BytesIO(png)).convert("RGB"); d = ImageDraw.Draw(t)
        d.rectangle((0, 0, 480, 26), fill=(0, 0, 0)); d.text((6, 6), f"frame {f}  t={f / FPS:.3f}s  {'BEFORE' if f < r['frame'] else 'ON BEAT'}", fill=(255, 255, 0))
        tiles.append(t)
sheet = Image.new("RGB", (480 * 4, 270 * 3 + 40), (20, 20, 20))
for i, t in enumerate(tiles): sheet.paste(t, ((i % 4) * 480, 40 + (i // 4) * 270))
ImageDraw.Draw(sheet).text((10, 12), f"{key}: beat-sync check — pairs of (frame before change, change frame). Visual-change onset within ±1 frame of scheduled beat: {within1 * 100:.0f}% of {len(res)}", fill=(255, 255, 255))
sheet.save(f"{out_dir}/2026-10-21-{key}-beat-check.png")
# contact sheet: 20 evenly spaced frames
n = 20; D = float(pr["format"]["duration"]); cs = Image.new("RGB", (5 * 384, 4 * 216 + 30), (15, 15, 15))
for i in range(n):
    ts = D * (i + 0.5) / n
    png = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", f"{ts:.2f}", "-i", vid, "-vf", "scale=384:216", "-vframes", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    t = Image.open(io.BytesIO(png)).convert("RGB"); ImageDraw.Draw(t).text((6, 6), f"{int(ts // 60)}:{ts % 60:05.2f}", fill=(255, 255, 0)); cs.paste(t, ((i % 5) * 384, 30 + (i // 5) * 216))
ImageDraw.Draw(cs).text((10, 8), f"{os.path.basename(vid)}  ·  {D:.1f}s  ·  contact sheet (20 evenly spaced frames)", fill=(255, 255, 255))
cs.save(f"{out_dir}/2026-10-21-{key}-contact-sheet.png")
