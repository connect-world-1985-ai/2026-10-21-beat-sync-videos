#!/usr/bin/env bash
# Build the final soundtrack for each video from the downloaded CC BY tracks.
set -euo pipefail
cd "$(dirname "$0")/.."
M=2026-10-21-music; O=2026-10-21-build/audio; mkdir -p $O
# V1: Crusade, full length
ffmpeg -loglevel error -y -i $M/crusade.mp3 -ar 44100 -ac 2 $O/v1_crusade.wav
# V2: Pixel Peeker Polka (faster), first 152 s with 5 s fade-out
ffmpeg -loglevel error -y -i $M/pixel_peeker_polka_faster.mp3 -af "atrim=0:152,afade=t=out:st=147:d=5" -ar 44100 -ac 2 $O/v2_polka.wav
# V3: Monkeys Spinning Monkeys (loopable) looped once with a 1.5 s crossfade, cut to 168 s, 4 s fade-out
ffmpeg -loglevel error -y -i $M/monkeys_spinning_monkeys.mp3 -i $M/monkeys_spinning_monkeys.mp3 \
  -filter_complex "[0][1]acrossfade=d=1.5:c1=tri:c2=tri,atrim=0:168,afade=t=out:st=164:d=4" -ar 44100 -ac 2 $O/v3_monkeys_loop.wav
# V4: Impact Lento -> 6 s crossfade -> Living Voyage
ffmpeg -loglevel error -y -i $M/impact_lento.mp3 -i $M/living_voyage.oga \
  -filter_complex "[0][1]acrossfade=d=6:c1=qsin:c2=qsin" -ar 44100 -ac 2 $O/v4_history.wav
for f in $O/*.wav; do echo "$f $(ffprobe -v error -show_entries format=duration -of csv=p=0 $f)"; done
