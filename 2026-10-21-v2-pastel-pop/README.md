# 2026-10-21 · Video 2 — Pastel Pop (anime-style kinetic typography)

`2026-10-21-v2-pastel-pop.mp4` — 2:32 (152 s), 1920x1080, 30 fps. Style: bright pastel gradients, scrolling polka dots, 4-point sparkles, bouncy squash-and-stretch words in English / Japanese / a bit of Chinese ("Hello! · おはよう! · キラキラ · がんばれ · 夢は きっと 叶う!"), ring bursts on strong hits, a 4-dot bar counter at the bottom.

## Music
| Field | Value |
|---|---|
| Title | Pixel Peeker Polka - faster |
| Artist | Kevin MacLeod (incompetech.com) |
| Source page | https://commons.wikimedia.org/wiki/File:Pixel_Peeker_Polka_-_faster_(ISRC_USUAN1100833).mp3 |
| Direct download | https://upload.wikimedia.org/wikipedia/commons/9/9b/Pixel_Peeker_Polka_-_faster_%28ISRC_USUAN1100833%29.mp3 |
| License | CC BY 3.0 — https://creativecommons.org/licenses/by/3.0/ |
| Attribution (required, burned into the video) | "Pixel Peeker Polka - faster" Kevin MacLeod (incompetech.com) · Licensed under Creative Commons: By Attribution 3.0 · http://creativecommons.org/licenses/by/3.0/ |

Honest note: no verifiable CC0/CC BY *J-pop/anime* track was reachable from this machine (Pixabay CDN, FreePD, archive.org and incompetech.com were blocked or timed out); this bright "8-bit-sounding electronic polka" was the closest upbeat, cute-sounding track with a verified license. Trimmed to 152 s with a 5 s fade-out.

## Beat-sync approach
* librosa: **143.6 BPM**, 358 beats in the trimmed audio, 92.2% of beats within 50 ms of an audio onset.
* Energy sections decide the word rate: **high sections = one word per beat (0.42 s), mid sections = one word per 2 beats**. 262 word changes in total.
* Each word appears on its beat frame at 45% size and overshoots to full size (back-out easing, squash & stretch, ±6° tilt), sparkles spawn on every beat (more when energy is high), a white ring bursts on each strong onset, the background gradient changes every 4 downbeats.
* Verification (`scripts/verify.py v2` → `verify_v2.json`): 152.0 s, 32.6 MB, H.264 1920x1080 30 fps + AAC; 262 scheduled text/scene changes checked in the decoded mp4; the visual change starts within ±1 frame of the scheduled beat in **97.7%** of them (onset offset histogram in frames: {'-3': 1, '-2': 4, '0': 236, '1': 20, '2': 1}). The few non-zero offsets are frames where a strong-hit ring burst or sparkle spawn just before the word change dominates the frame difference.

Files: `2026-10-21-v2-contact-sheet.png`, `2026-10-21-v2-beat-check.png`, `verify_v2.json`. Script: `scripts/v2_pastel_pop.py`.
