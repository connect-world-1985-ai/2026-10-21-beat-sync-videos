# 2026-10-21 · Beat-Sync Videos — how far can an agent push music-synced video?

Four videos whose text, cuts and motion are driven by **librosa beat / onset / energy analysis** of royalty-free music, rendered frame by frame with **Pillow + numpy** and encoded with **ffmpeg** (H.264 CRF 23/26 + AAC 160k, 1920x1080, 30 fps). All code was written locally by the agent; no cloud agents, no stock footage, no AI image/video generators.

| # | Video | Length | Style | Music (Kevin MacLeod, CC BY 3.0) |
|---|---|---|---|---|
| 1 | [`2026-10-21-v1-light-of-humanity/`](2026-10-21-v1-light-of-humanity/) | 3:19 | 人类之光 Light of Humanity — epic cinematic bilingual title cards, god-rays, particles, flashes on big hits | Crusade |
| 2 | [`2026-10-21-v2-pastel-pop/`](2026-10-21-v2-pastel-pop/) | 2:32 | Anime-style pastel kinetic typography (EN/JA/ZH), bouncy words, sparkles | Pixel Peeker Polka – faster |
| 3 | [`2026-10-21-v3-claude-buddy/`](2026-10-21-v3-claude-buddy/) | 2:48 | Cartoon: an original blocky mascot (homage to the Claude Code CLI banner creature) operating Claude Code — prompt typing, thinking spinner, file write, running code, /model switch, success | Monkeys Spinning Monkeys (looped) |
| 4 | [`2026-10-21-v4-human-epic/`](2026-10-21-v4-human-epic/) | **6:53** | 人类的史诗 The Human Epic — 24 bilingual chapters from the first stone tools to AI | Impact Lento → Living Voyage |

Each folder has its own README (source, license, attribution, sync approach, contents), a 20-frame contact sheet, a beat-check sheet (frame before vs. frame on the beat at six change points) and `verify_*.json`.

## Music & licenses
All tracks: Kevin MacLeod (incompetech.com), downloaded from Wikimedia Commons, whose file pages state the license. Attribution is burned into every video.

| Track | Commons page | License |
|---|---|---|
| Crusade | https://commons.wikimedia.org/wiki/File:Crusade_(ISRC_USUAN1100884).mp3 | CC BY 3.0 |
| Pixel Peeker Polka – faster | https://commons.wikimedia.org/wiki/File:Pixel_Peeker_Polka_-_faster_(ISRC_USUAN1100833).mp3 | CC BY 3.0 |
| Monkeys Spinning Monkeys | https://commons.wikimedia.org/wiki/File:Monkeys_Spinning_Monkeys_(ISRC_USUAN1400011).mp3 | CC BY 3.0 |
| Impact Lento | https://commons.wikimedia.org/wiki/File:Impact_Lento_(ISRC_USUAN1100619).mp3 | CC BY 3.0 |
| Living Voyage | https://commons.wikimedia.org/wiki/File:Living_Voyage_(MacLeod,_Kevin)_(ISRC_USUAN1100594).oga | CC BY 3.0 US |

Required attribution format: *"Title" Kevin MacLeod (incompetech.com) · Licensed under Creative Commons: By Attribution 3.0 · http://creativecommons.org/licenses/by/3.0/*. CC BY allows redistribution, so the source audio is kept in `2026-10-21-music/` (plus `commons_metadata.json`, the raw license metadata from the Commons API).
Sources tried and skipped: incompetech.com, FreePD, archive.org (timed out from this machine), Pixabay CDN and Musopen (HTTP 403).

## Pipeline
1. `scripts/prep_audio.sh` builds the soundtracks (trim / fade / loop with crossfade / two-track crossfade).
2. `scripts/analyze_beats.py` (librosa 1.0): onset-strength envelope → `beat_track` (tempo + beat frames) → per-beat strength → **downbeat phase** (beat index mod 4 with the largest low-band + full-band onset strength) → **strong hits** (onset peaks above the 85th percentile) → **RMS energy curve** (2 Hz, smoothed, normalised) → low/mid/high **sections** (segments < 6 s merged). Output: `2026-10-21-analysis/*.json` + a plot (`*.png`: first 20 s beats/downbeats/hits + the energy/section curve).
3. Spot checks: `scripts/click_check.py` writes 30 s **click-track overlays** (`*_clicks_30s.mp3`, high click = beat, low click = downbeat) and `beat_tracking_stats.json`.
4. `scripts/engine.py`: cached text rendering (Noto Serif/Sans CJK, Cinzel, Fredoka, DejaVu Sans Mono), easing, the `Sync` helper (every event is quantised to `round(t·fps)`, so a change is exactly on the frame that contains the beat), and a parallel renderer (8 worker processes each pipe raw RGB frames into their own ffmpeg, then concat + mux audio).
5. `scripts/v1…v4_*.py` render the videos; `scripts/verify.py vN` runs ffprobe, decodes the mp4, measures frame-to-frame difference around every scheduled change, and writes the contact sheet + beat-check sheet.

Regenerate everything: `./scripts/regenerate.sh` (needs ffmpeg, fonts-noto-cjk and the Google fonts listed in `requirements.txt`). Render time on this 8-core box: V1 ≈ 2.5 min, V2 ≈ 1.7 min, V3 ≈ 0.7 min, V4 ≈ 4.2 min.

## Video 4 — 人类的史诗 The Human Epic (dedicated section)
**Approach.** 24 chapter cards over 6:53. Each chapter: on its hit the Chinese title slams in with a flash and a 0.6 s cross-dissolve from the previous chapter; then the date line, the English title and a bilingual detail caption each land on the following downbeats. A procedural motif for the era sits behind the text with a slow 10% zoom and a small pulse on every beat; era-specific particles (dust, embers, stars, sparks, clouds, binary digits) scale with RMS energy; an era timeline at the bottom fills up chapter by chapter and its current tick pulses on beats. Dates are deliberately conservative ("约 / c.", ranges) and stick to well-established milestones.

**Music choice and why.** Two verified CC BY tracks rather than self-composed music: a synthesised score would have sounded clearly worse than an orchestral recording, and the length target (5+ min) is met by crossfading two pieces. *Impact Lento* (slow, brooding, sparse) carries deep prehistory → the Axial Age; the crossfade lands on the empires chapter; *Living Voyage* ("earthy and yet urban… epic… major uplifting") carries the accelerating modern story from empires to AI. Each track was beat-analysed separately (one global tempo over the mix was wrong).

**Sources.** Music: see the table above. Visuals: 100% procedurally drawn by the scripts — **no external images**, so there is no image license to record. Facts: standard milestones as found in general references (Lomekwi 3 tools; Dmanisi; Wonderwerk Cave; Jebel Irhoud; out-of-Africa dispersal; Sulawesi/European cave art; Fertile Crescent and Chinese domestication; cuneiform; Great Pyramid; Shang oracle bones; Axial Age; Qin 221 BCE and Rome 27 BCE; Cai Lun 105 CE; Bi Sheng and Gutenberg; Copernicus 1543 to Newton 1687; Watt; Faraday 1831 and Edison 1879; Wright brothers 1903; ENIAC 1945–46; Sputnik 1957 and Apollo 11 1969; ARPANET 1969 and the Web proposal 1989; deep learning in the 2010s and LLMs). These were written from the agent's knowledge, not re-checked against a cited source for this video.

**Chapter timeline** (start time in the video, what the card was snapped to):

| # | Start | Snapped to | Date (zh / en) | Title (zh / en) | Motif |
|---|---|---|---|---|---|
| 00 | 0:00.50 | start | — | 人类的史诗 / THE HUMAN EPIC | dawn |
| 01 | 0:17.95 | downbeat | 约330万年前 / c. 3.3 million years ago | 最早的石器 / The First Stone Tools | stones |
| 02 | 0:33.16 | downbeat | 约200万年前 / c. 2 million years ago | 直立人走出非洲 / Homo erectus Leaves Africa | walkers |
| 03 | 0:51.92 | downbeat | 约100万年前 / c. 1 million years ago | 掌握火 / Mastering Fire | fire |
| 04 | 1:09.13 | downbeat | 约30万年前 / c. 300,000 years ago | 智人登场 / Homo sapiens Appears | footprints |
| 05 | 1:24.10 | strong hit | 约7万–5万年前 / c. 70,000–50,000 years ago | 走向世界 / Out of Africa | migration |
| 06 | 1:41.54 | downbeat | 约4万多年前起 / From c. 40,000+ years ago | 洞穴艺术 / Cave Art | hands |
| 07 | 1:58.68 | downbeat | 约1.2万–1万年前 / c. 12,000–10,000 years ago | 农业革命 / The Agricultural Revolution | wheat |
| 08 | 2:16.25 | downbeat | 约公元前3200年 / c. 3200 BCE | 文字诞生 / Writing Is Born | cuneiform |
| 09 | 2:33.79 | downbeat | 约公元前2560年 / c. 2560 BCE | 古代文明 / Ancient Civilizations | pyramids |
| 10 | 2:51.06 | downbeat | 约公元前1250年 / c. 1250 BCE | 甲骨文 / Oracle Bone Script | oracle |
| 11 | 3:07.53 | **none** (no beat or onset found) | 约公元前6–4世纪 / c. 6th–4th century BCE | 思想的轴心时代 / The Axial Age of Ideas | columns |
| 12 | 3:31.03 | strongest raw onset in the crossfade | 公元前221年 / 221 BCE | 帝国时代 / The Age of Empires | wall |
| 13 | 3:45.77 | downbeat | 约公元105年 / c. 105 CE | 造纸术 / Paper | paper |
| 14 | 4:01.52 | downbeat | 约1040年代 · 约1450年 / c. 1040s · c. 1450 | 印刷术 / Printing | type |
| 15 | 4:19.23 | downbeat | 1543–1687年 | 科学革命 / The Scientific Revolution | orbits |
| 16 | 4:36.93 | strong hit | 约1760–1840年 / c. 1760–1840 | 工业革命 / The Industrial Revolution | gears |
| 17 | 4:51.67 | strong hit | 1831年 · 1879年 | 电气时代 / The Age of Electricity | bulb |
| 18 | 5:08.16 | strong hit | 1903年 | 飞上天空 / Taking Flight | plane |
| 19 | 5:24.13 | strong hit | 1945–1946年 | 电子计算机 / The Electronic Computer | circuit |
| 20 | 5:41.85 | strong hit | 1957年 · 1969年 | 走向太空 / Into Space | rocket |
| 21 | 5:55.62 | strong hit | 1969年 · 1989年 | 互联网 / The Internet | network |
| 22 | 6:15.29 | downbeat | 2010年代至今 / 2010s – today | 人工智能 / Artificial Intelligence | neural |
| 23 | 6:31.03 | downbeat | 下一章 / The next chapter | 由我们共同书写 / IS OURS TO WRITE | dawn |

## Honest assessment of sync quality
**What works.**
* **Frame accuracy holds.** Every change is scheduled on `round(beat·30)`, and the decoded mp4s confirm it: the visual change starts on the scheduled frame (±1) for **100%** of changes in V1 (45), V3 (131) and V4 (23 chapters), and **97.7%** in V2 (262 word changes). V2's few misses are frames where a ring burst or sparkle from a strong hit just before the word change dominates the frame difference; the word itself is still on its beat.
* **There is no drift.** Beats are detected positions, not a fixed BPM grid, and the looped and crossfaded soundtracks were re-analysed after mixing, so nothing accumulates over 7 minutes.
* **Rhythmic tracks track well.** Monkeys Spinning Monkeys: 98% of beats within 50 ms of an onset. Pixel Peeker Polka and Living Voyage: about 92%. With these, the cuts read as clearly "on the beat".
* **Energy following works at section scale.** Card rate in V1 doubles in the high section, word rate in V2 doubles in high sections, and confetti, rays and particles swell with RMS.

**Limits and errors.**
* **The tempo for orchestral music is doubtful.** Impact Lento comes out as 123 BPM, and its 30 s click track sounds like a plausible but arbitrary pulse over sustained strings: only 77% of its beats sit near an onset. Crusade also has 76% (89 BPM). For slow orchestral music, librosa finds *a* pulse, not necessarily the conductor's.
* **Some stretches have no beats at all.** Nothing was detected from 176.6 s to 213.9 s in V4 (Impact Lento's soft ending plus the crossfade). Chapter 11 is not on any audio event, and chapter 12 falls back to a raw onset.
* **Downbeats are a heuristic.** "Strongest phase mod 4" assumes 4/4. The polka is really 2/4, so "downbeat" there means every other bar line. Nothing models meter changes or pickups.
* **"Big hits" are statistical.** The 85th-percentile onset peaks catch drum and brass accents, but also some loud string attacks. A human editor would pick fewer, more meaningful hits and would anticipate phrases, for example starting a reveal a few frames *before* a downbeat or holding a card across a phrase. The algorithm never does that.
* **The aesthetic ceiling is "polished motion-graphics template", not film.** The visuals are flat procedural shapes and gradients. There is no real imagery, depth of field, motion blur or 3D, and the typography uses fixed layouts. The V4 motifs are clearly symbolic, and the cuneiform and oracle-bone marks are decorative, not real inscriptions. V2 is cute but repetitive over 2.5 minutes. V3's mascot is simple pixel blocks with basic squash and stretch.
* **The genre fit is approximate.** I could not reach a verifiable CC0 or CC BY J-pop/anime track, so V2 uses an 8-bit polka.
