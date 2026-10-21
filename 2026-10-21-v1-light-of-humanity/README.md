# 2026-10-21 · Video 1 — 人类之光 Light of Humanity

`2026-10-21-v1-light-of-humanity.mp4` — 3:19 (198.7 s), 1920x1080, 30 fps. Style: grand, cinematic, bilingual (Chinese + English) manifesto in the spirit of "人类之光": night-to-dawn gradient sky, rotating god-rays, glowing sun, drifting golden dust, slow zooms, white flashes on big hits, letterbox bars.

## Music
| Field | Value |
|---|---|
| Title | Crusade |
| Artist | Kevin MacLeod (incompetech.com) |
| Source page | https://commons.wikimedia.org/wiki/File:Crusade_(ISRC_USUAN1100884).mp3 |
| Direct download | https://upload.wikimedia.org/wikipedia/commons/5/55/Crusade_%28ISRC_USUAN1100884%29.mp3 |
| License | CC BY 3.0 — https://creativecommons.org/licenses/by/3.0/ |
| Attribution (required, burned into the video) | "Crusade" Kevin MacLeod (incompetech.com) · Licensed under Creative Commons: By Attribution 3.0 · http://creativecommons.org/licenses/by/3.0/ |

Used in full (198.7 s) so the piece ends naturally — slightly over the 2–3 min target.

## Beat-sync approach
* librosa: tempo **89.1 BPM**, 293 beats; downbeat phase = beat index mod 4 with the strongest low-frequency onsets; RMS energy → low/mid/high sections (low 0–2 s, mid 2–96 s, **high 96–163 s**, mid 163–185.5 s, low after).
* 46 bilingual cards. Mid section: 17 cards spread over the detected downbeats (one every 2 downbeats ≈ 5.4 s). **High section: a new card on every downbeat (≈ 2.7 s)**. Outro: 4 cards spread over the remaining downbeats.
* On each card's downbeat: the Chinese line slams in (scale 1.35 → 1.0, ease-out) + white flash (stronger in high sections) + sun-glow pulse; the English line lands on the **next detected beat**. Ray rotation speed, ray brightness and particle count follow the RMS energy curve, so the visuals swell with the orchestra.
* Verification (`scripts/verify.py v1` → `verify_v1.json`): 198.73 s, 46.0 MB, H.264 1920x1080 30 fps + AAC; 45 scheduled text/scene changes checked in the decoded mp4; the visual change starts within ±1 frame of the scheduled beat in **100.0%** of them (onset offset histogram in frames: {'0': 45}).

Files: `2026-10-21-v1-contact-sheet.png` (20 frames), `2026-10-21-v1-beat-check.png` (frame before / on the beat pairs), `verify_v1.json`. Script: `scripts/v1_light_of_humanity.py`.
