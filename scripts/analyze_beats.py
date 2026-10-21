"""Beat / energy analysis with librosa. Usage: python analyze_beats.py audio out.json [plot.png]"""
import sys, json, numpy as np, librosa
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

def analyze(path, out_json, plot=None, start_bpm=120):
    y, sr = librosa.load(path, sr=22050, mono=True)
    hop = 512
    dur = len(y) / sr
    oenv = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop)
    tempo, beats = librosa.beat.beat_track(onset_envelope=oenv, sr=sr, hop_length=hop, start_bpm=start_bpm, units="frames")
    tempo = float(np.atleast_1d(tempo)[0])
    bt = librosa.frames_to_time(beats, sr=sr, hop_length=hop)
    # beat strength = max onset strength within +-2 frames
    bs = np.array([oenv[max(0, b-2):b+3].max() for b in beats])
    # downbeat phase: which beat index mod 4 has highest mean (low-freq weighted) strength
    S = np.abs(librosa.stft(y, hop_length=hop))
    low = librosa.onset.onset_strength(S=librosa.amplitude_to_db(S[:40]), sr=sr, hop_length=hop)
    lb = np.array([low[max(0, b-2):b+3].max() for b in beats])
    phase = int(np.argmax([lb[p::4].mean() + bs[p::4].mean() for p in range(4)]))
    downbeats = bt[phase::4]
    # strong hits: onset peaks above 92nd percentile, min spacing 0.25s
    peaks = librosa.util.peak_pick(oenv, pre_max=5, post_max=5, pre_avg=10, post_avg=10, delta=0.3, wait=6)
    thr = np.percentile(oenv[peaks], 85) if len(peaks) else 1e9
    hits = librosa.frames_to_time(peaks[oenv[peaks] >= thr], sr=sr, hop_length=hop)
    # energy (RMS) curve, 2 Hz, normalized 0..1
    rms = librosa.feature.rms(y=y, hop_length=hop)[0]
    rt = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop)
    grid = np.arange(0, dur, 0.5)
    e = np.interp(grid, rt, rms)
    k = 8; e = np.convolve(e, np.ones(k)/k, mode="same")
    e = (e - e.min()) / (np.ptp(e) + 1e-9)
    # sections: quantize energy to low/mid/high, merge segments < 6 s
    lvl = np.digitize(e, [0.33, 0.66])
    secs = []; s0 = 0
    for i in range(1, len(lvl)+1):
        if i == len(lvl) or lvl[i] != lvl[s0]:
            secs.append([grid[s0], grid[i-1]+0.5, int(lvl[s0])]); s0 = i
    merged = []
    for s in secs:
        if merged and (s[1]-s[0] < 6 or merged[-1][2] == s[2]):
            merged[-1][1] = s[1]
        else: merged.append(s)
    names = ["low", "mid", "high"]
    res = dict(file=path, duration=dur, tempo_bpm=tempo, beat_times=bt.round(4).tolist(),
               beat_strength=(bs/bs.max()).round(3).tolist(), downbeat_phase=phase,
               downbeat_times=downbeats.round(4).tolist(), strong_hits=hits.round(4).tolist(),
               energy_grid_hz=2, energy=e.round(3).tolist(),
               sections=[dict(start=round(a,2), end=round(b,2), level=names[l]) for a,b,l in merged])
    json.dump(res, open(out_json, "w"), indent=1)
    if plot:
        fig, ax = plt.subplots(2, 1, figsize=(18, 6))
        t = librosa.frames_to_time(np.arange(len(oenv)), sr=sr, hop_length=hop)
        w = (t < 20)
        ax[0].plot(t[w], oenv[w], lw=.8); ax[0].vlines(bt[bt<20], 0, oenv.max(), color="r", alpha=.5, label="beats")
        ax[0].vlines(downbeats[downbeats<20], 0, oenv.max(), color="k", lw=2, label="downbeats")
        ax[0].plot(hits[hits<20], [oenv.max()*0.95]*len(hits[hits<20]), "g*", label="strong hits")
        ax[0].legend(); ax[0].set_title(f"{path} first 20 s  tempo={tempo:.1f} BPM")
        ax[1].plot(grid, e); [ax[1].axvspan(s[0], s[1], color=["#ddf","#fdb","#f99"][s[2]], alpha=.5) for s in merged]
        ax[1].set_title("normalized energy + sections (blue low / orange mid / red high)")
        plt.tight_layout(); plt.savefig(plot, dpi=80)
    return res

if __name__ == "__main__":
    r = analyze(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    print(f"{r['file']}: {r['duration']:.1f}s tempo {r['tempo_bpm']:.1f} beats {len(r['beat_times'])} hits {len(r['strong_hits'])} sections {[(s['start'],s['level']) for s in r['sections']]}")
