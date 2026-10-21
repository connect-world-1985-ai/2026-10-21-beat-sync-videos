"""Video 3 — "Little Buddy Codes!": an original cartoon homage to the small block creature in the Claude Code
CLI welcome banner, operating Claude Code. Music: Kevin MacLeod "Monkeys Spinning Monkeys" (looped once).
Terminal text is taken from the real tmux `claudedemo` session logs (read-only) in
/workspace/2026-10-21-claude-interactive-demo/ ; the guess.py game run near the end is a dramatization that
uses the real program's strings."""
import sys, math, numpy as np
from PIL import Image, ImageDraw
from engine import *

W, H, FPS = 1920, 1080, 30
S = Sync("v3_monkeys_loop", FPS)
AUDIO = f"{ROOT}/2026-10-21-build/audio/v3_monkeys_loop.wav"
OUT = f"{ROOT}/2026-10-21-v3-claude-buddy/2026-10-21-v3-claude-buddy.mp4"
ATTR = '♪ "Monkeys Spinning Monkeys" by Kevin MacLeod (incompetech.com) · CC BY 3.0 · creativecommons.org/licenses/by/3.0 · Original fan cartoon, not affiliated with Anthropic'
ORANGE = (217, 119, 87); WHITE = (235, 235, 235); GRAY = (140, 140, 150); GREEN = (110, 200, 120); BLUE = (120, 170, 255); YEL = (240, 200, 90)

GUESS = ['def play():', '    number = random.randint(1, 100)', '    attempts = 0', '    print("Guess a number between 1 and 100.")',
         '    while True:', '        raw = input("Your guess: ")', '        try:', '            guess = int(raw)', '        except ValueError:',
         '            print("Please enter a whole number.")', '            continue', '        attempts += 1', '        if guess < number:',
         '            print("Higher!")', '        elif guess > number:', '            print("Lower!")', '        else:',
         '            print(f"Correct! You got it in {attempts} attempts.")', '            break']
P1 = "Build a tiny interactive number-guessing game in Python called guess.py: pick a random number 1-100, read guesses from input, say higher/lower, and count attempts. Keep it short."
P2 = "Now add input validation and ask to play again at the end."

# ---- op script: each op fires on one detected beat; ("until", t) waits for the first beat >= t ----
OPS = []
def op(kind, *a): OPS.append((kind, a))
op("title", "Meet Little Buddy!", "认识小伙伴！"); op("mood", "hop")
op("until", 4.0); op("title", "It lives in your terminal", "它住在你的终端里")
op("until", 10.4); op("title", "Step 1 · Start Claude Code", "第一步 · 启动 Claude Code"); op("mood", "idle")
op("line", "$ claude --dangerously-skip-permissions", WHITE); op("wait", 2)
for l, c in [("  ✻ Welcome to Claude Code v2.1.197", ORANGE), ("    Sonnet 5 · Claude Pro", GRAY),
             ("    /workspace/2026-10-21-claude-interactive-demo", GRAY), ("", GRAY)]:
    op("line", l, c)
op("wait", 3); op("sync")
op("title", "Step 2 · Type a prompt", "第二步 · 输入提示词"); op("mood", "typing"); op("line", "❯ ", WHITE)
for w in P1.split(" "): op("type", w + " ")
op("sync"); op("title", "Step 3 · Claude thinks…", "第三步 · Claude 思考中…"); op("mood", "think")
for k in range(8): op("spin", ["✻", "✳", "✢", "·"][k % 4] + " Choreographing…")
op("sync"); op("title", "Step 4 · It writes the file", "第四步 · 写入文件"); op("mood", "typing"); op("set_last", "● Write(guess.py)", GREEN)
op("line", "  └ Writing guess.py…", GRAY)
op("clear"); op("line", "● Write(guess.py)", GREEN)
for k, l in enumerate(GUESS): op("line", f"{k + 4:>3} + {l}", GREEN)
op("line", "✻ Sautéed for 6s", ORANGE); op("line", "● Created guess.py.", WHITE); op("mood", "happy"); op("wait", 3)
op("until", 66); op("clear"); op("title", "Round 2 · Keep the conversation going", "第二轮 · 继续多轮对话"); op("mood", "typing"); op("line", "❯ ", WHITE)
for w in P2.split(" "): op("type", w + " ")
op("line", "✢ Marinating…", ORANGE); op("wait", 2)
op("line", "● Updated guess.py: friendly reprompts + \"Play again? (y/n)\"", WHITE)
op("until", 74); op("clear"); op("title", "Step 5 · Run the code!", "第五步 · 运行代码！"); op("mood", "dance")
op("line", "● Bash(python3 capture_test.py)", GREEN)
for k, v in enumerate([0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]): op("line", f"  └ {v}" if k == 0 else f"    {v}", WHITE)
op("line", "  Fibonacci ✔ — the output matches", GREEN); op("wait", 2)
op("sync"); op("clear"); op("title", "Play the game it built", "玩一玩它写的游戏"); op("line", "$ python3 guess.py", WHITE)
for l in ["Guess a number between 1 and 100.", "Your guess: 50", "Higher!", "Your guess: 75", "Lower!", "Your guess: 62", "Higher!",
          "Your guess: 68", "Lower!", "Your guess: 65", "Correct! You got it in 5 attempts.", "Play again? (y/n): n"]:
    op("line", l, GREEN if l.startswith("Correct") else WHITE)
op("wait", 2); op("sync"); op("clear"); op("title", "Step 6 · Switch models with /model", "第六步 · 用 /model 切换模型"); op("mood", "typing")
op("line", "❯ /model", WHITE); op("wait", 1)
MENU = [" 1. Default (recommended)  Sonnet 5 · Efficient for routine tasks", " 2. Sonnet   Sonnet 5", " 3. Fable    Fable 5.1 · Most capable for your hardest tasks",
        " 4. Opus     Opus 4.8 · Best for everyday, complex tasks", " 5. Haiku    Haiku 4.5 · Fastest for quick answers"]
for sel in [0, 1, 2, 3, 3]: op("menu", sel, MENU)
op("line", "❯ 1. Yes, switch to Opus 4.8", ORANGE); op("wait", 2)
op("line", "  └ Set model to Opus 4.8 for this session only", GRAY); op("mood", "happy"); op("wait", 3)
op("line", "❯ Which model are you right now? One line.", WHITE); op("line", "✻ Marinating…", ORANGE); op("wait", 2)
op("until", 135); op("clear"); op("title", "Success!", "成功！多轮交互 · 写代码 · 跑代码"); op("mood", "dance")
for l, c in [("● Added README.md.", WHITE), ("✻ Cooked for 4s", ORANGE), ("● Done — greetings.py now has greet(name=\"World\")", WHITE),
             ("✻ Baked for 12s", ORANGE), ("", WHITE), ("  ✔ 3 rounds of multi-turn prompts", GREEN), ("  ✔ files written and edited", GREEN),
             ("  ✔ code run, output checked", GREEN), ("  ✔ model switched: Sonnet 5 → Opus 4.8", GREEN)]:
    op("line", l, c); op("wait", 1)
op("until", 155); op("title", "Little Buddy, big help", "小小伙伴，大大帮手"); op("mood", "hop")

def build():
    beats = list(S.beats); snaps = []; times = []
    lines, title, mood = [], ("", ""), "idle"; bi = 0; menu_on = False
    def emit():
        snaps.append((tuple(lines), title, mood)); times.append(beats[min(bi, len(beats) - 1)])
    for kind, a in OPS:
        if kind == "until":
            while bi < len(beats) and beats[bi] < a[0]: bi += 1
            continue
        if kind == "sync":
            nd = [x for x in S.down if x >= beats[min(bi, len(beats) - 1)] - 1e-6]
            if nd:
                while bi < len(beats) and beats[bi] < nd[0] - 1e-6: bi += 1
            continue
        if kind == "wait": bi += a[0]; continue
        if kind == "title": title = a; emit(); continue          # title/mood change share the beat of the next op
        if kind == "mood": mood = a[0]; continue
        if kind == "line": lines.append((a[0], a[1]))
        elif kind == "type":
            if len(lines[-1][0]) + len(a[0]) > 70: lines.append(("  " + a[0], WHITE))
            else: lines[-1] = (lines[-1][0] + a[0], WHITE)
        elif kind == "spin":
            if lines and lines[-1][0][:1] in "✻✳✢·": lines[-1] = (a[0], ORANGE)
            else: lines.append((a[0], ORANGE))
        elif kind == "set_last": lines[-1] = (a[0], a[1])
        elif kind == "clear": lines = []; emit(); continue
        elif kind == "menu":
            sel, menu = a
            if menu_on: lines = lines[:-len(menu)]
            lines += [(("❯" if j == sel else " ") + m[1:], ORANGE if j == sel else GRAY) for j, m in enumerate(menu)]
        menu_on = (kind == "menu")
        emit(); bi += 1
    return np.round(np.array(times) * FPS), snaps
SF, SNAPS = build()
print("ops->snapshots", len(SNAPS), "last beat time", SF[-1] / FPS)

BG = to_img(vgrad(W, H, (250, 240, 228), (240, 222, 205)))
dg = ImageDraw.Draw(BG)
for x in range(0, W, 60): dg.line((x, 0, x, H), fill=(235, 220, 205, 255))
for y in range(0, H, 60): dg.line((0, y, W, y), fill=(235, 220, 205, 255))
TX0, TY0, TX1, TY1 = 640, 140, 1880, 980
rng = np.random.default_rng(11); CONF = rng.uniform(0, 1, (400, 5))

def mascot(d, cx, by, sc, squash, blink, arm, mood, t):
    """Original blocky critter: chunky body, two pixel eyes, stubby arms, four legs. (cx, by) = bottom center."""
    u = 14 * sc; bw, bh = 15 * u * (1 + 0.12 * squash), 10 * u * (1 - 0.12 * squash)
    x0, y0 = cx - bw / 2, by - 2.2 * u - bh
    for k in range(4):  # legs
        lx = x0 + bw * (0.12 + 0.23 * k); lh = 2.2 * u * (1 - 0.3 * max(0, squash))
        d.rectangle((lx, by - lh, lx + 1.6 * u, by), fill=(190, 100, 72))
    d.rectangle((x0, y0, x0 + bw, y0 + bh), fill=ORANGE)
    d.rectangle((x0, y0 + bh * 0.82, x0 + bw, y0 + bh), fill=(200, 105, 76))
    ay = y0 + bh * 0.45
    la = -arm * 1.2 * u; ra = arm * 1.2 * u
    d.rectangle((x0 - 2.2 * u, ay + la, x0, ay + 1.8 * u + la), fill=ORANGE)
    d.rectangle((x0 + bw, ay + ra, x0 + bw + 2.2 * u, ay + 1.8 * u + ra), fill=ORANGE)
    ex = [cx - bw * 0.22, cx + bw * 0.22]; ey = y0 + bh * 0.38
    for x in ex:
        if blink: d.rectangle((x - 0.9 * u, ey + 0.6 * u, x + 0.9 * u, ey + 1.0 * u), fill=(40, 28, 28))
        elif mood == "happy" or mood == "dance": d.line((x - u, ey + 1.2 * u, x, ey, x + u, ey + 1.2 * u), fill=(40, 28, 28), width=int(0.6 * u))
        else: d.rectangle((x - 0.7 * u, ey - 0.6 * u, x + 0.7 * u, ey + 1.4 * u), fill=(40, 28, 28))
    if mood in ("happy", "dance", "hop"):
        d.rectangle((cx - 0.9 * u, ey + 2.4 * u, cx + 0.9 * u, ey + 3.0 * u), fill=(120, 50, 40))
    if mood == "think":
        for k, r in enumerate([0.5, 0.8, 1.2]):
            bx = x0 + bw + (1.5 + 1.6 * k) * u; byy = y0 - (1 + 1.6 * k) * u - 4 * math.sin(t * 4 + k)
            d.ellipse((bx - r * u, byy - r * u, bx + r * u, byy + r * u), fill=(255, 255, 255), outline=(120, 120, 120), width=3)
    return (x0, y0, bw, bh)

def frame(i):
    t = i / FPS; e = S.e(t); base = BG.copy(); d = ImageDraw.Draw(base)
    k = int(np.searchsorted(SF, i, side="right") - 1); lines, title, mood = SNAPS[max(k, 0)]
    tchg = SF[max(k, 0)] / FPS; ag = t - tchg
    # terminal window
    d.rounded_rectangle((TX0 + 12, TY0 + 16, TX1 + 12, TY1 + 16), 26, fill=(200, 180, 165))
    d.rounded_rectangle((TX0, TY0, TX1, TY1), 26, fill=(28, 28, 34))
    d.rounded_rectangle((TX0, TY0, TX1, TY0 + 56), 26, fill=(52, 52, 60)); d.rectangle((TX0, TY0 + 30, TX1, TY0 + 56), fill=(52, 52, 60))
    for j, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]): d.ellipse((TX0 + 24 + 36 * j, TY0 + 16, TX0 + 48 + 36 * j, TY0 + 40), fill=c)
    paste(base, text_img("claude — ~/2026-10-21-claude-interactive-demo", "dvmono", 22, (200, 200, 205, 255)), (TX0 + TX1) / 2, TY0 + 28)
    LH = 37; maxl = 20; shown = lines[-maxl:]
    for j, (txt, col) in enumerate(shown):
        y = TY0 + 80 + j * LH; newest = (j == len(shown) - 1 and k >= 0)
        if txt and txt.split()[0].isdigit() and "+" in txt[:6]: d.rectangle((TX0 + 20, y, TX1 - 20, y + LH - 4), fill=(28, 60, 36))
        im = text_img(txt[:74] if txt else " ", "dvmono", 26, col + (255,))
        dx = 18 * (1 - ease_out(ag / 0.12)) if newest else 0
        base.alpha_composite(im, (int(TX0 + 34 + dx), int(y - 4)))
    if lines and (int(t * 2.4) % 2 == 0):
        last = shown[-1][0][:74]; cw = font("dvmono", 26).getlength(last)
        yy = TY0 + 80 + (len(shown) - 1) * LH; d.rectangle((TX0 + 40 + cw, yy + 2, TX0 + 54 + cw, yy + 32), fill=(220, 220, 220))
    # title caption (changes on beats)
    if title[0]:
        s = back_out(ag / 0.25) if ag < 0.4 and k >= 0 else 1
        words = title[0].split(" "); rows = [""]
        for w_ in words:
            if len(rows[-1]) + len(w_) > 18: rows.append(w_)
            else: rows[-1] = (rows[-1] + " " + w_).strip()
        for r_, row in enumerate(rows):
            paste(base, text_img(row, "fredoka", 54, (60, 40, 40, 255)), 320, 250 + r_ * 66 - 33 * (len(rows) - 1), s)
        paste(base, text_img(title[1], "sans_cjk", 38, ORANGE + (255,)), 320, 260 + 33 * len(rows) + 30, s)
    # mascot: bounce on every beat; intensity follows energy
    ba = S.beat_age(t); tb, kb = S.last(S.beats, t)
    hop = {"hop": 90, "dance": 70, "happy": 40, "typing": 14, "think": 6, "idle": 20}[mood] * (0.5 + 0.8 * e)
    y_off = -hop * max(0, math.sin(clamp(ba / 0.40) * math.pi)) if ba < 0.4 else 0
    squash = 0.8 * decay(ba, 14) - (0.3 if 0.05 < ba < 0.3 else 0)
    blink = (int(t * 10) % 37) == 0
    arm = (1 if kb % 2 else -1) if mood in ("typing", "dance", "hop") else 0.2 * math.sin(t * 3)
    sway = 30 * math.sin(t * math.pi * 143.6 / 120) if mood == "dance" else 0
    cx, by = 330 + sway, 820 + y_off
    d.ellipse((cx - 190, 830, cx + 190, 862), fill=(215, 195, 178))
    mascot(d, cx, by, 1.3, squash, blink, arm, mood, t)
    d.rounded_rectangle((150, 880, 520, 930), 12, fill=(70, 70, 80))  # little keyboard
    for j in range(8):
        lit = (mood == "typing" and (kb + j) % 5 == 0 and ba < 0.2)
        d.rounded_rectangle((165 + j * 44, 890, 200 + j * 44, 920), 6, fill=(250, 200, 120) if lit else (110, 110, 125))
    # confetti in high-energy / success sections, bursts on strong hits
    if mood == "dance" or S.level(t) == "high":
        th, kh = S.last(S.hits, t); ah = t - S.q(th)
        n = int(80 + 140 * e)
        for m in range(n):
            c = CONF[m]; y = ((c[1] * H + t * (120 + 200 * c[2])) % (H + 40)) - 20; x = c[0] * W + 30 * math.sin(t * 2 + c[3] * 6)
            if ah < 0.5: y -= 60 * (1 - ah / 0.5) * c[4]
            col = [ORANGE, (90, 160, 250), (250, 200, 80), (120, 200, 140), (240, 120, 170)][m % 5]
            d.rectangle((x, y, x + 10 + 8 * c[4], y + 6), fill=col)
    paste(base, text_img(ATTR, "sans_cjk_r", 20, (120, 100, 90, 255)), W / 2, H - 28)
    fade = clamp(t / 0.6) * clamp((S.dur - t) / 2.0)
    if fade < 1: base.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * (1 - fade)))))
    return base

if __name__ == "__main__":
    import os; os.makedirs(os.path.dirname(OUT), exist_ok=True)
    pv = (float(sys.argv[1]), float(sys.argv[2])) if len(sys.argv) > 2 else None
    out = OUT if not pv else "/tmp/bsv/v3_preview.mp4"
    render(out, W, H, FPS, S.dur, AUDIO, frame, preview=pv); print(out)
