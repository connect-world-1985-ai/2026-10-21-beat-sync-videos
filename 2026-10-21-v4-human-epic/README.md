# 2026-10-21 · Video 4 — 人类的史诗 The Human Epic

`2026-10-21-v4-human-epic.mp4` — **6:53 (413.2 s)**, 1920x1080, 30 fps, CRF 26 (61 MB). See the root README for the full chapter timeline, music choice and sources.

## Music
| Field | Value |
|---|---|
| Title | Impact Lento |
| Artist | Kevin MacLeod (incompetech.com) |
| Source page | https://commons.wikimedia.org/wiki/File:Impact_Lento_(ISRC_USUAN1100619).mp3 |
| Direct download | https://upload.wikimedia.org/wikipedia/commons/8/85/Impact_Lento_%28ISRC_USUAN1100619%29.mp3 |
| License | CC BY 3.0 — https://creativecommons.org/licenses/by/3.0/ |
| Attribution (required, burned into the video) | "Impact Lento" Kevin MacLeod (incompetech.com) · Licensed under Creative Commons: By Attribution 3.0 · http://creativecommons.org/licenses/by/3.0/ |

| Field | Value |
|---|---|
| Title | Living Voyage |
| Artist | Kevin MacLeod (incompetech.com) |
| Source page | https://commons.wikimedia.org/wiki/File:Living_Voyage_(MacLeod,_Kevin)_(ISRC_USUAN1100594).oga |
| Direct download | https://upload.wikimedia.org/wikipedia/commons/5/5f/Living_Voyage_%28MacLeod%2C_Kevin%29_%28ISRC_USUAN1100594%29.oga |
| License | CC BY 3.0 US — https://creativecommons.org/licenses/by/3.0/us/deed.en |
| Attribution (required, burned into the video) | "Living Voyage" Kevin MacLeod (incompetech.com) · Licensed under Creative Commons: By Attribution 3.0 · http://creativecommons.org/licenses/by/3.0/ |

Mixed: Impact Lento (210.6 s) → 6 s equal-power crossfade → Living Voyage (208.6 s).

## Beat-sync approach
* Each track was analysed separately (a single global tempo over the mix was wrong) and the beat lists merged at the crossfade (Living Voyage offset +204.573 s).
* 24 chapters: target times evenly spaced per track, then snapped to a **strong onset within ±2.5 s** if one exists ("big hit"), else the nearest downbeat (±3 s), else the nearest beat. In the 176–214 s gap (Impact Lento's quiet ending + crossfade) librosa found **no beats at all**, so chapter 12 snaps to the strongest raw onset there (211.03 s) and chapter 11 (3:07.5) is **not** on any detected beat.
* Inside a chapter: Chinese title + flash + cross-dissolve on the hit; date, English title and the detail captions each appear on the following downbeats; motifs pulse slightly on every beat; the current tick of the era timeline pulses on beats; slow 10% zoom across each chapter.
* Verification (`scripts/verify.py v4` → `verify_v4.json`): 413.16 s, 60.9 MB, H.264 1920x1080 30 fps + AAC; 23 scheduled text/scene changes checked in the decoded mp4; the visual change starts within ±1 frame of the scheduled beat in **100.0%** of them (onset offset histogram in frames: {'0': 23}). (only chapter starts are counted; sub-line reveals are on downbeats too.)

Visuals: 100% procedural (Pillow + numpy) — gradients, stone-tool polygons, walking stick figures, flames, footprints, migration arcs, hand stencils, wheat, cuneiform-like wedges, pyramids, an oracle-bone plate (with the typed characters 甲骨文字, not real inscriptions), temple columns, a wall on ridges, paper sheets, movable-type blocks, orbits, gears, a light bulb, a biplane, circuit traces, a rocket and Moon, a network graph and a neural net. **No external images were used**, so there are no image licenses to record.

Files: `2026-10-21-v4-contact-sheet.png`, `2026-10-21-v4-beat-check.png`, `verify_v4.json`. Script: `scripts/v4_human_epic.py`.
