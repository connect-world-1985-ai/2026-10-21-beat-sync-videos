"""Spot-check beat tracking: (1) 30 s click-track overlays (mp3) per soundtrack, (2) distance from each detected
beat to the nearest detected audio onset (ms)."""
import json, subprocess, numpy as np, librosa, soundfile as sf
from engine import ROOT
out = {}
for n in ["v1_crusade", "v2_polka", "v3_monkeys_loop", "impact_lento", "living_voyage"]:
    src = f"{ROOT}/2026-10-21-build/audio/{n}.wav" if n.startswith("v") else f"{ROOT}/2026-10-21-music/{n}." + ("oga" if n == "living_voyage" else "mp3")
    if n == "impact_lento": src = "/tmp/bsv/impact_lento.wav"
    y, sr = librosa.load(src, sr=22050)
    d = json.load(open(f"{ROOT}/2026-10-21-analysis/{n}.json")); bt = np.array(d["beat_times"]); db = np.array(d["downbeat_times"])
    on = librosa.onset.onset_detect(y=y, sr=sr, units="time")
    dist = np.array([np.min(np.abs(on - b)) for b in bt]) * 1000
    ibi = np.diff(bt)
    out[n] = dict(tempo_bpm=round(d["tempo_bpm"], 1), beats=len(bt), median_beat_to_onset_ms=round(float(np.median(dist)), 1),
                  pct_beats_within_50ms_of_onset=round(float(np.mean(dist < 50)) * 100, 1), ibi_std_ms=round(float(np.std(ibi)) * 1000, 1),
                  longest_gap_without_beats_s=round(float(ibi.max()), 2))
    seg = y[: sr * 30]
    clk = librosa.clicks(times=bt[bt < 30], sr=sr, length=len(seg), click_freq=1500) * 0.6 + librosa.clicks(times=db[db < 30], sr=sr, length=len(seg), click_freq=700, click_duration=0.15) * 0.8
    sf.write("/tmp/bsv/clk.wav", np.clip(seg * 0.8 + clk, -1, 1), sr)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", "/tmp/bsv/clk.wav", "-b:a", "128k", f"{ROOT}/2026-10-21-analysis/{n}_clicks_30s.mp3"], check=True)
json.dump(out, open(f"{ROOT}/2026-10-21-analysis/beat_tracking_stats.json", "w"), indent=1); print(json.dumps(out, indent=1))
