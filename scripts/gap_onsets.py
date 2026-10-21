"""V4: librosa's beat tracker finds no beats from ~176.6 s to ~213.9 s (Impact Lento's quiet ending + crossfade).
Detect raw onsets there so chapter cards can still land on a real audio event."""
import json, numpy as np, librosa
from engine import ROOT
t0, t1 = 176.6, 213.9
y, sr = librosa.load(f"{ROOT}/2026-10-21-build/audio/v4_history.wav", sr=22050, offset=t0, duration=t1 - t0)
o = librosa.onset.onset_strength(y=y, sr=sr); pk = librosa.onset.onset_detect(onset_envelope=o, sr=sr, units="frames")
json.dump({"range": [t0, t1], "onsets": (librosa.frames_to_time(pk, sr=sr) + t0).round(3).tolist(), "strength": o[pk].round(3).tolist()},
          open(f"{ROOT}/2026-10-21-analysis/v4_gap_onsets.json", "w"))
