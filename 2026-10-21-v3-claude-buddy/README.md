# 2026-10-21 · Video 3 — Little Buddy Codes! (cartoon Claude Code mascot)

`2026-10-21-v3-claude-buddy.mp4` — 2:48 (168 s), 1920x1080, 30 fps. Style: playful flat cartoon on a warm grid background. An **original, hand-coded homage** (Pillow rectangles, not Anthropic artwork) to the small blocky creature in the Claude Code CLI welcome banner: chunky terracotta body, two pixel eyes, stubby arms, four legs. It bounces on every beat, blinks, types on a little keyboard (keys light up on beats), shows a thought bubble while Claude thinks, and dances in the high-energy section with confetti. The frame carries "Original fan cartoon, not affiliated with Anthropic".

Scenes (each change lands on a detected beat; scene starts are aligned to downbeats / section boundaries):
1. Meet Little Buddy (hops in) · 2. `claude --dangerously-skip-permissions` + welcome banner (Claude Code v2.1.197, Sonnet 5 · Claude Pro) · 3. typing Round-1 prompt **one word per beat** · 4. "✻ Choreographing…" spinner cycling ✻ ✳ ✢ · per beat · 5. `● Write(guess.py)` with one green diff line per beat, "✻ Sautéed for 6s" · 6. Round 2 prompt (multi-turn), "✢ Marinating…" · 7. **high section**: `● Bash(python3 capture_test.py)` printing Fibonacci numbers one per beat, then playing guess.py · 8. `/model` menu: the cursor moves down one option per beat to Opus 4.8, "Yes, switch to Opus 4.8", "Set model to Opus 4.8 for this session only" · 9. Success checklist + "Little Buddy, big help / 小小伙伴，大大帮手".

Terminal text source: the real tmux `claudedemo` session logs in `/workspace/2026-10-21-claude-interactive-demo/` (read only; the session was not touched) — prompts, model menu entries (Sonnet 5, Fable 5.1, Opus 4.8, Haiku 4.5), spinner words, guess.py code, capture_test.py output. The guess.py play-through (50 → Higher! … Correct!) is a **dramatization** using the program's real strings; it was not captured from the log.

## Music
| Field | Value |
|---|---|
| Title | Monkeys Spinning Monkeys |
| Artist | Kevin MacLeod (incompetech.com) |
| Source page | https://commons.wikimedia.org/wiki/File:Monkeys_Spinning_Monkeys_(ISRC_USUAN1400011).mp3 |
| Direct download | https://upload.wikimedia.org/wikipedia/commons/e/e9/Monkeys_Spinning_Monkeys_%28ISRC_USUAN1400011%29.mp3 |
| License | CC BY 3.0 — https://creativecommons.org/licenses/by/3.0/ |
| Attribution (required, burned into the video) | "Monkeys Spinning Monkeys" Kevin MacLeod (incompetech.com) · Licensed under Creative Commons: By Attribution 3.0 · http://creativecommons.org/licenses/by/3.0/ |

The 125 s track is described as "loopable"; it is played twice with a 1.5 s triangular crossfade, cut to 168 s with a 4 s fade-out (`scripts/prep_audio.sh`). Beats were re-detected on the looped audio, so the seam has no grid drift.

## Beat-sync approach
* **143.6 BPM**, 398 beats, 98.2% within 50 ms of an onset (pizzicato makes beats very clear).
* A small "op script" (`OPS` in the script) is compiled onto the beat list: every op (append a line, type a word, move the menu cursor, spin) consumes one detected beat; `sync` waits for the next downbeat, `until t` waits for a section boundary (mid 10.5 s, high 74 s, mid 135 s).
* Mascot hop height and confetti density scale with RMS energy; confetti bursts upward on strong onsets.
* Verification (`scripts/verify.py v3` → `verify_v3.json`): 168.0 s, 26.0 MB, H.264 1920x1080 30 fps + AAC; 131 scheduled text/scene changes checked in the decoded mp4; the visual change starts within ±1 frame of the scheduled beat in **100.0%** of them (onset offset histogram in frames: {'0': 131}).

Files: `2026-10-21-v3-contact-sheet.png`, `2026-10-21-v3-beat-check.png`, `verify_v3.json`. Script: `scripts/v3_claude_buddy.py`.
