#!/usr/bin/env bash
# Rebuild everything from the downloaded music: soundtracks -> beat analysis -> 4 videos -> verification.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m venv .venv && . .venv/bin/activate && pip install -q -r requirements.txt
./scripts/prep_audio.sh
mkdir -p /tmp/bsv && ffmpeg -loglevel error -y -i 2026-10-21-music/impact_lento.mp3 -ar 44100 -ac 2 /tmp/bsv/impact_lento.wav
# NOTE: run analyses sequentially — parallel runs corrupted numba's cache and segfaulted librosa's beat tracker.
for f in 2026-10-21-build/audio/*.wav /tmp/bsv/impact_lento.wav 2026-10-21-music/living_voyage.oga; do
  b=$(basename "${f%.*}"); python scripts/analyze_beats.py "$f" 2026-10-21-analysis/$b.json 2026-10-21-analysis/$b.png
done
cd scripts
python click_check.py; python gap_onsets.py
python v1_light_of_humanity.py; python v2_pastel_pop.py; python v3_claude_buddy.py; CRF=26 python v4_human_epic.py
for v in v1 v2 v3 v4; do python verify.py $v; done
