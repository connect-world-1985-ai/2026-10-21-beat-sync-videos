"""Video 4 — 人类的史诗 The Human Epic: ~6:53 bilingual history of humankind, chapter cards on big hits.
Music: Kevin MacLeod "Impact Lento" -> 6 s crossfade -> "Living Voyage" (both CC BY 3.0).
All visuals are procedural (Pillow/numpy) — no external images."""
import sys, math, json, numpy as np
from PIL import Image, ImageDraw, ImageFilter
from engine import *

W, H, FPS = 1920, 1080, 30
OFF = 210.573075 - 6.0           # Living Voyage starts here in the mixed soundtrack
def _merge():
    a = json.load(open(f"{ROOT}/2026-10-21-analysis/impact_lento.json")); b = json.load(open(f"{ROOT}/2026-10-21-analysis/living_voyage.json"))
    cut = OFF + 3.0
    m = lambda k: [x for x in a[k] if x < cut] + [x + OFF for x in b[k] if x + OFF >= cut]
    bt = m("beat_times")
    return dict(beat_times=bt, downbeat_times=m("downbeat_times"), strong_hits=m("strong_hits"), beat_strength=[1.0] * len(bt))
S = Sync("v4_history", FPS, override=_merge())
AUDIO = f"{ROOT}/2026-10-21-build/audio/v4_history.wav"
OUT = f"{ROOT}/2026-10-21-v4-human-epic/2026-10-21-v4-human-epic.mp4"
ATTR = 'Music: "Impact Lento" & "Living Voyage" by Kevin MacLeod (incompetech.com) · CC BY 3.0 · creativecommons.org/licenses/by/3.0 · All visuals procedurally generated'

CH = [  # (date_zh, date_en, title_zh, title_en, detail_zh, detail_en, motif, palette(top,bottom), particle)
 ("", "", "人类的史诗", "THE HUMAN EPIC", "从第一块石器到人工智能", "From the first stone tool to artificial intelligence", "dawn", ((5, 8, 25), (60, 40, 70)), "stars"),
 ("约330万年前", "c. 3.3 million years ago", "最早的石器", "The First Stone Tools", "肯尼亚洛迈奎遗址：已知最古老的石器", "Lomekwi, Kenya: the oldest known stone tools", "stones", ((30, 20, 12), (110, 70, 40)), "dust"),
 ("约200万年前", "c. 2 million years ago", "直立人走出非洲", "Homo erectus Leaves Africa", "约180万年前已到达今格鲁吉亚的德马尼西", "Reaching Dmanisi, Georgia, by c. 1.8 million years ago", "walkers", ((40, 25, 15), (170, 100, 50)), "dust"),
 ("约100万年前", "c. 1 million years ago", "掌握火", "Mastering Fire", "南非奇迹洞：早期用火的证据", "Wonderwerk Cave, South Africa: early evidence of fire use", "fire", ((10, 5, 5), (70, 20, 10)), "embers"),
 ("约30万年前", "c. 300,000 years ago", "智人登场", "Homo sapiens Appears", "摩洛哥杰贝尔依罗：已知最早的智人化石", "Jebel Irhoud, Morocco: the earliest known Homo sapiens fossils", "footprints", ((25, 18, 12), (120, 90, 60)), "dust"),
 ("约7万–5万年前", "c. 70,000–50,000 years ago", "走向世界", "Out of Africa", "现代人类扩散到亚洲和澳洲，后来到达欧洲与美洲", "Modern humans spread to Asia and Australia, later Europe and the Americas", "migration", ((8, 15, 35), (40, 70, 110)), "stars"),
 ("约4万多年前起", "From c. 40,000+ years ago", "洞穴艺术", "Cave Art", "苏拉威西与欧洲的洞穴里留下手印与动物画", "Hand stencils and animals painted in caves of Sulawesi and Europe", "hands", ((30, 15, 8), (90, 45, 25)), "embers"),
 ("约1.2万–1万年前", "c. 12,000–10,000 years ago", "农业革命", "The Agricultural Revolution", "新月沃地种植小麦；中国驯化水稻与粟", "Wheat in the Fertile Crescent; rice and millet in China", "wheat", ((40, 60, 90), (210, 170, 90)), "dust"),
 ("约公元前3200年", "c. 3200 BCE", "文字诞生", "Writing Is Born", "美索不达米亚的楔形文字，埃及的象形文字", "Cuneiform in Mesopotamia, hieroglyphs in Egypt", "cuneiform", ((35, 25, 15), (140, 110, 70)), "dust"),
 ("约公元前2560年", "c. 2560 BCE", "古代文明", "Ancient Civilizations", "吉萨大金字塔建成；印度河流域城市繁荣", "The Great Pyramid of Giza; Indus Valley cities thrive", "pyramids", ((40, 30, 60), (230, 150, 70)), "dust"),
 ("约公元前1250年", "c. 1250 BCE", "甲骨文", "Oracle Bone Script", "商朝晚期：中国已知最早的成体系文字", "Late Shang China: the earliest known mature Chinese writing", "oracle", ((20, 15, 10), (100, 75, 45)), "embers"),
 ("约公元前6–4世纪", "c. 6th–4th century BCE", "思想的轴心时代", "The Axial Age of Ideas", "孔子、老子、佛陀、苏格拉底", "Confucius, Laozi, the Buddha, Socrates", "columns", ((20, 25, 50), (150, 140, 170)), "stars"),
 ("公元前221年", "221 BCE", "帝国时代", "The Age of Empires", "秦统一中国；公元前27年罗马帝国建立", "Qin unifies China; the Roman Empire begins in 27 BCE", "wall", ((40, 20, 20), (200, 90, 50)), "dust"),
 ("约公元105年", "c. 105 CE", "造纸术", "Paper", "东汉蔡伦改进造纸术", "Cai Lun of the Eastern Han improves papermaking", "paper", ((40, 35, 30), (190, 170, 140)), "dust"),
 ("约1040年代 · 约1450年", "c. 1040s · c. 1450", "印刷术", "Printing", "毕昇发明活字印刷；古腾堡印刷机在欧洲传播知识", "Bi Sheng's movable type; Gutenberg's press spreads knowledge in Europe", "type", ((25, 20, 20), (120, 80, 60)), "dust"),
 ("1543–1687年", "1543–1687", "科学革命", "The Scientific Revolution", "从哥白尼《天体运行论》到牛顿《原理》", "From Copernicus's De revolutionibus to Newton's Principia", "orbits", ((5, 10, 30), (30, 50, 100)), "stars"),
 ("约1760–1840年", "c. 1760–1840", "工业革命", "The Industrial Revolution", "瓦特改良蒸汽机；工厂与铁路兴起", "Watt's improved steam engine; factories and railways rise", "gears", ((30, 28, 30), (120, 90, 70)), "embers"),
 ("1831年 · 1879年", "1831 · 1879", "电气时代", "The Age of Electricity", "法拉第发现电磁感应；爱迪生推出实用白炽灯", "Faraday discovers induction; Edison's practical light bulb", "bulb", ((10, 10, 30), (60, 50, 120)), "sparks"),
 ("1903年", "1903", "飞上天空", "Taking Flight", "莱特兄弟完成首次有动力的载人飞行", "The Wright brothers' first powered, piloted flight", "plane", ((60, 120, 190), (220, 230, 240)), "clouds"),
 ("1945–1946年", "1945–1946", "电子计算机", "The Electronic Computer", "ENIAC：早期的通用电子计算机", "ENIAC: an early general-purpose electronic computer", "circuit", ((5, 25, 20), (20, 80, 60)), "bits"),
 ("1957年 · 1969年", "1957 · 1969", "走向太空", "Into Space", "斯普特尼克1号进入轨道；阿波罗11号登月", "Sputnik 1 reaches orbit; Apollo 11 lands on the Moon", "rocket", ((0, 0, 10), (20, 20, 50)), "stars"),
 ("1969年 · 1989年", "1969 · 1989", "互联网", "The Internet", "ARPANET 首次联网；伯纳斯-李提出万维网", "ARPANET's first link; Tim Berners-Lee proposes the World Wide Web", "network", ((5, 10, 30), (20, 60, 110)), "bits"),
 ("2010年代至今", "2010s – today", "人工智能", "Artificial Intelligence", "深度学习取得突破，大语言模型走进日常", "Deep learning breakthroughs; large language models enter daily life", "neural", ((10, 5, 30), (70, 30, 110)), "bits"),
 ("下一章", "The next chapter", "由我们共同书写", "IS OURS TO WRITE", "人类的史诗，未完待续", "The human epic continues", "dawn", ((20, 30, 70), (240, 170, 90)), "stars"),
]

def chapter_starts():
    hits = S.hits; down = S.down
    def snap(tgt):
        h = hits[np.abs(hits - tgt) < 2.5]
        if len(h): return float(h[np.argmin(np.abs(h - tgt))]), "hit"
        dn = S.nearest(down, tgt)
        if abs(dn - tgt) < 3: return dn, "downbeat"
        bn = S.nearest(S.beats, tgt)
        if abs(bn - tgt) < 3: return bn, "beat"
        g = json.load(open(f"{ROOT}/2026-10-21-analysis/v4_gap_onsets.json")); go = np.array(g["onsets"]); gs = np.array(g["strength"])
        m_ = np.abs(go - tgt) < 4
        if m_.any(): return float(go[m_][np.argmax(gs[m_])]), "onset (beat tracker found no beats here)"
        return tgt, "free (no beat detected nearby)"
    p1 = np.linspace(0, OFF, 13)[:-1]; p2 = np.linspace(OFF + 4, S.dur - 22, 12)
    out = [(S.nearest(S.beats, 0.6) if S.beats[0] < 3 else 0.5, "start")]
    for tg in list(p1[1:]) + list(p2):
        out.append(snap(tg))
    return out
STARTS = chapter_starts(); ST = [s for s, _ in STARTS]; STF = np.round(np.array(ST) * FPS)

# ---------- procedural motifs (static layer, 1.15x canvas, drawn once per chapter) ----------
MW, MH = int(W * 1.15), int(H * 1.15); mcx, mcy = MW / 2, MH / 2
def M(): im = Image.new("RGBA", (MW, MH), (0, 0, 0, 0)); return im, ImageDraw.Draw(im)
def glowify(im, r=18, k=1.0):
    g = im.filter(ImageFilter.GaussianBlur(r)); out = Image.new("RGBA", im.size, (0, 0, 0, 0)); out.alpha_composite(g); out.alpha_composite(g if k > 1 else Image.new("RGBA", im.size)); out.alpha_composite(im); return out
R = np.random.default_rng(42)
def m_dawn(c):
    im, d = M(); r = MW * 0.9
    for k in range(30): d.ellipse((mcx - r - k * 3, MH * 0.92 - k * 3, mcx + r + k * 3, MH * 0.92 + 2 * r), outline=(255, 190, 120, max(0, 120 - k * 4)), width=3)
    d.ellipse((mcx - r, MH * 0.92, mcx + r, MH * 0.92 + 2 * r), fill=(10, 20, 45, 255))
    return glowify(im, 20)
def m_stones(c):
    im, d = M()
    for k in range(5):
        x = MW * (0.2 + 0.15 * k); y = MH * (0.62 + 0.05 * (k % 2)); s = 80 + 30 * (k % 3)
        pts = [(x, y - 1.6 * s), (x + 0.8 * s, y - 0.2 * s), (x + 0.4 * s, y + 0.9 * s), (x - 0.5 * s, y + 0.8 * s), (x - 0.8 * s, y - 0.3 * s)]
        d.polygon(pts, fill=(150, 120, 90, 200), outline=(230, 200, 160, 255))
        for j in range(4): d.line((x + R.uniform(-.5, .5) * s, y - s, x + R.uniform(-.5, .5) * s, y + .6 * s), fill=(90, 70, 50, 200), width=3)
    return im
def figure(d, x, y, s, ph, col):
    d.ellipse((x - .12 * s, y - 1.0 * s, x + .12 * s, y - .76 * s), fill=col)
    d.line((x, y - .76 * s, x + .05 * s, y - .35 * s), fill=col, width=int(.08 * s))
    for sg in (1, -1):
        d.line((x + .05 * s, y - .35 * s, x + sg * .2 * s * math.sin(ph), y), fill=col, width=int(.08 * s))
        d.line((x, y - .65 * s, x - sg * .18 * s * math.sin(ph), y - .4 * s), fill=col, width=int(.06 * s))
def m_walkers(c):
    im, d = M(); d.line((0, MH * .72, MW, MH * .72), fill=(255, 200, 140, 120), width=3); return im
def m_fire(c): im, d = M(); d.ellipse((mcx - 260, MH * .78, mcx + 260, MH * .78 + 60), fill=(40, 20, 10, 255)); return im
def m_footprints(c):
    im, d = M()
    for k in range(9):
        x = MW * .15 + k * 190; y = MH * .7 + (40 if k % 2 else -40)
        d.ellipse((x - 30, y - 60, x + 30, y + 40), fill=(200, 160, 120, 170)); [d.ellipse((x - 30 + j * 15, y - 85, x - 18 + j * 15, y - 70), fill=(200, 160, 120, 170)) for j in range(5)]
    return im
def m_migration(c):
    im, d = M(); src = (MW * .52, MH * .62)
    for k in range(700):
        a = R.uniform(0, 6.283); rr = R.uniform(0, 1) ** .5 * MH * .45; x = mcx + rr * math.cos(a) * 1.8; y = mcy + rr * math.sin(a)
        d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(140, 180, 230, 120))
    for tx, ty in [(.75, .35), (.88, .7), (.35, .3), (.15, .4), (.62, .25)]:
        pts = [(src[0] + (tx * MW - src[0]) * u, src[1] + (ty * MH - src[1]) * u - math.sin(u * math.pi) * 120) for u in np.linspace(0, 1, 40)]
        d.line(pts, fill=(255, 200, 120, 220), width=5); d.ellipse((tx * MW - 10, ty * MH - 10, tx * MW + 10, ty * MH + 10), fill=(255, 220, 160, 255))
    d.ellipse((src[0] - 16, src[1] - 16, src[0] + 16, src[1] + 16), fill=(255, 150, 80, 255)); return glowify(im, 8)
def m_hands(c):
    im, d = M()
    for k, (x, y, s, rot) in enumerate([(.25, .4, 1.1, -15), (.75, .45, 1.0, 12), (.5, .3, .8, 0), (.4, .7, .7, 20), (.65, .72, .9, -8)]):
        h = Image.new("RGBA", (400, 500), (0, 0, 0, 0)); hd = ImageDraw.Draw(h)
        hd.ellipse((110, 220, 290, 420), fill=(200, 90, 50, 150))
        for j, (fx, fl) in enumerate([(105, 150), (150, 210), (195, 230), (240, 205), (290, 140)]): hd.rounded_rectangle((fx - 22, 300 - fl, fx + 22, 320), 22, fill=(200, 90, 50, 150))
        h = h.filter(ImageFilter.GaussianBlur(6)).rotate(rot, expand=True).resize((int(400 * s), int(500 * s)))
        im.alpha_composite(h, (int(x * MW - h.width / 2), int(y * MH - h.height / 2)))
    return im
def m_wheat(c):
    im, d = M()
    for k in range(40):
        x = MW * k / 40 + 20; top = MH * (.45 + .08 * math.sin(k)); d.line((x, MH, x + 20, top), fill=(220, 180, 90, 200), width=4)
        for j in range(7): yy = top + j * 22; d.ellipse((x + 20 - 14, yy, x + 20, yy + 26), fill=(240, 200, 100, 220)); d.ellipse((x + 20, yy + 8, x + 34, yy + 34), fill=(240, 200, 100, 220))
    return im
def m_cuneiform(c):
    im, d = M(); d.rounded_rectangle((mcx - 520, mcy - 330, mcx + 520, mcy + 330), 60, fill=(150, 110, 70, 160))
    for row in range(9):
        for col in range(18):
            if R.random() < .75:
                x = mcx - 470 + col * 55; y = mcy - 290 + row * 66; dx = R.choice([0, 1])
                d.polygon([(x, y), (x + 22, y), (x + 11, y + 14)], fill=(70, 45, 25, 230)); d.line((x + 11, y + 10, x + 11 + dx * 18, y + 44), fill=(70, 45, 25, 230), width=4)
    return im
def m_pyramids(c):
    im, d = M(); g = MH * .8
    for x, s in [(.3, 380), (.58, 300), (.78, 200)]: d.polygon([(x * MW - s, g), (x * MW, g - s * .95), (x * MW + s, g)], fill=(200, 150, 80, 230)); d.polygon([(x * MW, g - s * .95), (x * MW + s, g), (x * MW + s * .3, g)], fill=(150, 100, 50, 230))
    d.rectangle((0, g, MW, MH), fill=(120, 85, 45, 230)); d.ellipse((MW * .82, MH * .15, MW * .82 + 160, MH * .15 + 160), fill=(255, 220, 150, 230)); return im
def m_oracle(c):
    im, d = M(); d.rounded_rectangle((mcx - 420, mcy - 300, mcx + 420, mcy + 300), 200, fill=(210, 190, 150, 170))
    for k in range(14): x = mcx + R.uniform(-350, 350); y = mcy + R.uniform(-230, 230); d.line((x, y, x + R.uniform(-60, 60), y + R.uniform(-60, 60)), fill=(90, 60, 30, 200), width=4)
    for k, ch in enumerate("甲骨文字"): paste(im, text_img(ch, "serif_cjk", 150, (110, 70, 35, 200)), mcx - 270 + k * 180, mcy)
    return im
def m_columns(c):
    im, d = M(); base = MH * .82
    d.polygon([(mcx - 560, MH * .3), (mcx, MH * .15), (mcx + 560, MH * .3)], fill=(220, 215, 230, 200)); d.rectangle((mcx - 560, MH * .3, mcx + 560, MH * .34), fill=(220, 215, 230, 200))
    for k in range(7):
        x = mcx - 480 + k * 160; d.rectangle((x - 40, MH * .34, x + 40, base), fill=(210, 205, 220, 190))
        for j in range(4): d.line((x - 30 + j * 20, MH * .35, x - 30 + j * 20, base), fill=(170, 165, 185, 200), width=3)
    d.rectangle((mcx - 600, base, mcx + 600, base + 40), fill=(220, 215, 230, 200)); return im
def m_wall(c):
    im, d = M()
    for layer, (col, amp, yb) in enumerate([((90, 50, 50, 200), 160, .62), ((60, 35, 35, 230), 120, .75)]):
        pts = [(x, MH * yb - amp * (0.5 + 0.5 * math.sin(x / 210 + layer * 2)) * (0.6 + 0.4 * math.sin(x / 77))) for x in range(0, MW + 20, 20)]
        d.polygon(pts + [(MW, MH), (0, MH)], fill=col)
        if layer == 0:
            d.line(pts, fill=(230, 180, 120, 255), width=10)
            for x, y in pts[::6]: d.rectangle((x - 18, y - 46, x + 18, y), fill=(230, 180, 120, 255))
    return im
def m_paper(c):
    im, d = M()
    for k in range(7):
        sh = Image.new("RGBA", (520, 680), (245, 235, 210, 170)); sd = ImageDraw.Draw(sh)
        for j in range(12): sd.line((50, 80 + j * 48, 470, 80 + j * 48), fill=(200, 180, 150, 200), width=3)
        sh = sh.rotate(-20 + k * 7, expand=True); im.alpha_composite(sh, (int(mcx - sh.width / 2 + (k - 3) * 90), int(mcy - sh.height / 2 + abs(k - 3) * 20)))
    return im
def m_type(c):
    im, d = M(); chars = "天地人和光明文字书知识山水日月星云火木金土心智"
    for row in range(6):
        for col in range(12):
            x = mcx - 660 + col * 120; y = mcy - 330 + row * 120; d.rounded_rectangle((x, y, x + 105, y + 105), 10, fill=(150, 110, 80, 170))
            paste(im, text_img(chars[(row * 12 + col * 7) % len(chars)], "serif_cjk", 70, (60, 35, 20, 230)), x + 52, y + 55)
    return im
def m_orbits(c):
    im, d = M()
    for r in [140, 230, 330, 440, 560]: d.ellipse((mcx - r * 1.4, mcy - r * .6, mcx + r * 1.4, mcy + r * .6), outline=(150, 180, 255, 120), width=3)
    d.ellipse((mcx - 70, mcy - 70, mcx + 70, mcy + 70), fill=(255, 220, 130, 255)); return glowify(im, 14)
def gear(n, r):
    g = Image.new("RGBA", (int(2.5 * r), int(2.5 * r)), (0, 0, 0, 0)); gd = ImageDraw.Draw(g); c = 1.25 * r
    pts = []
    for k in range(n * 2):
        a0 = k * math.pi / n; rr = r * (1.18 if k % 2 == 0 else 0.95)
        pts += [(c + rr * math.cos(a0), c + rr * math.sin(a0)), (c + rr * math.cos(a0 + math.pi / n * .8), c + rr * math.sin(a0 + math.pi / n * .8))]
    gd.polygon(pts, fill=(170, 140, 110, 210)); gd.ellipse((c - .35 * r, c - .35 * r, c + .35 * r, c + .35 * r), fill=(0, 0, 0, 0)); return g
GEARS = [(gear(14, 260), .38, .5, 1), (gear(10, 180), .62, .38, -1.4), (gear(8, 130), .66, .72, 1.75)]
def m_gears(c): return M()[0]
def m_bulb(c):
    im, d = M(); d.ellipse((mcx - 220, mcy - 330, mcx + 220, mcy + 110), fill=(255, 230, 150, 120), outline=(255, 240, 200, 255), width=6)
    d.rectangle((mcx - 90, mcy + 110, mcx + 90, mcy + 230), fill=(170, 170, 180, 230))
    for j in range(4): d.line((mcx - 90, mcy + 130 + j * 26, mcx + 90, mcy + 130 + j * 26), fill=(110, 110, 120, 255), width=6)
    d.line([(mcx - 60, mcy + 100), (mcx - 40, mcy - 120), (mcx, mcy - 60), (mcx + 40, mcy - 120), (mcx + 60, mcy + 100)], fill=(255, 250, 220, 255), width=6)
    return glowify(im, 25)
def m_plane(c):
    im, d = M(); x, y = mcx, mcy
    for dy in (-60, 60): d.rectangle((x - 360, y + dy - 12, x + 360, y + dy + 12), fill=(80, 70, 60, 230))
    for dx in (-300, -100, 100, 300): d.line((x + dx, y - 60, x + dx, y + 60), fill=(80, 70, 60, 230), width=6)
    d.rectangle((x - 40, y - 20, x + 380, y + 4), fill=(80, 70, 60, 230)); d.polygon([(x + 380, y - 70), (x + 450, y - 70), (x + 450, y + 40), (x + 380, y + 20)], fill=(80, 70, 60, 230))
    for k in range(6): d.line((x - 700, y - 100 + k * 40, x - 420, y - 100 + k * 40), fill=(255, 255, 255, 150), width=4)
    return im
def m_circuit(c):
    im, d = M()
    for k in range(90):
        x = R.integers(0, MW // 40) * 40; y = R.integers(0, MH // 40) * 40; pts = [(x, y)]
        for j in range(4):
            x += R.choice([-1, 1]) * R.integers(1, 6) * 40 if j % 2 == 0 else 0; y += R.choice([-1, 1]) * R.integers(1, 5) * 40 if j % 2 else 0; pts.append((x, y))
        d.line(pts, fill=(80, 220, 160, 140), width=4); d.ellipse((x - 8, y - 8, x + 8, y + 8), fill=(120, 255, 200, 200))
    d.rounded_rectangle((mcx - 200, mcy - 200, mcx + 200, mcy + 200), 20, fill=(15, 40, 35, 240), outline=(120, 255, 200, 255), width=6)
    return glowify(im, 6)
def m_rocket(c):
    im, d = M(); d.ellipse((MW * .68, MH * .12, MW * .68 + 300, MH * .12 + 300), fill=(220, 220, 210, 240))
    for k in range(9): x = MW * .68 + R.uniform(40, 260); y = MH * .12 + R.uniform(40, 260); r = R.uniform(10, 35); d.ellipse((x - r, y - r, x + r, y + r), fill=(180, 180, 170, 240))
    x, y = MW * .32, MH * .62
    d.polygon([(x, y - 330), (x + 70, y - 200), (x + 70, y + 120), (x - 70, y + 120), (x - 70, y - 200)], fill=(235, 235, 240, 255))
    d.polygon([(x - 70, y + 20), (x - 150, y + 160), (x - 70, y + 120)], fill=(200, 60, 50, 255)); d.polygon([(x + 70, y + 20), (x + 150, y + 160), (x + 70, y + 120)], fill=(200, 60, 50, 255))
    d.ellipse((x - 30, y - 170, x + 30, y - 110), fill=(80, 140, 220, 255)); return im
NODES = R.uniform([0.12, 0.15], [0.88, 0.85], (26, 2)); EDGES = [(i, j) for i in range(26) for j in range(i + 1, 26) if np.hypot(*(NODES[i] - NODES[j])) < 0.26]
def m_network(c):
    im, d = M()
    for i, j in EDGES: d.line((NODES[i][0] * MW, NODES[i][1] * MH, NODES[j][0] * MW, NODES[j][1] * MH), fill=(100, 170, 255, 120), width=3)
    for x, y in NODES: d.ellipse((x * MW - 12, y * MH - 12, x * MW + 12, y * MH + 12), fill=(160, 210, 255, 255))
    return glowify(im, 8)
LAY = [5, 8, 8, 5]; LX = [.22, .41, .59, .78]
def lnodes(): return [[(LX[l] * MW, MH * (.5 + (k - (n - 1) / 2) * .09)) for k in range(n)] for l, n in enumerate(LAY)]
def m_neural(c):
    im, d = M(); ns = lnodes()
    for l in range(3):
        for a in ns[l]:
            for b in ns[l + 1]: d.line((a, b), fill=(190, 130, 255, 70), width=2)
    for layer in ns:
        for x, y in layer: d.ellipse((x - 22, y - 22, x + 22, y + 22), fill=(220, 180, 255, 255))
    return glowify(im, 10)
MOTIFS = {k[2:]: v for k, v in globals().items() if k.startswith("m_")}
_cache = {}
def motif(k):
    if k not in _cache: _cache[k] = MOTIFS[CH[k][6]](CH[k])
    return _cache[k]
BGS = {}
def bg(k):
    if k not in BGS: BGS[k] = to_img(vgrad(W, H, *CH[k][7], gamma=1.2))
    return BGS[k]
yy, xx = np.mgrid[0:H, 0:W]; V = np.clip((np.hypot((xx - W / 2) / W, (yy - H / 2) / H) - .25) * 1.6, 0, 1) ** 1.5
VIG = Image.fromarray(np.dstack([np.zeros((H, W, 3), np.uint8), (V * 235).astype(np.uint8)]), "RGBA"); del xx, yy, V
_by = np.linspace(0, 1, H)[:, None]; _bx = np.linspace(-1, 1, W)[None, :]
_band = np.exp(-((_by - 0.5) / 0.26) ** 4) * np.exp(-(_bx / 0.75) ** 6) * 150
BAND = Image.fromarray(np.dstack([np.zeros((H, W, 3), np.uint8), _band.astype(np.uint8)]), "RGBA")
PR = np.random.default_rng(5).uniform(0, 1, (300, 4))

def animated(d, base, k, t, age, e, pulse):
    m = CH[k][6]
    if m == "walkers":
        for j in range(5):
            x = ((age * 70 + j * 260) % (W + 300)) - 150; figure(d, x, H * .68, 170 - j * 8, age * 6 + j, (30, 20, 12, 255))
    elif m == "fire":
        for j in range(18):
            ph = t * (5 + j % 5) + j; h = (260 + 140 * math.sin(ph) * .5 + 120 * pulse) * (1 - abs(j - 9) / 11)
            x = W / 2 + (j - 9) * 26; col = [(255, 210, 90, 200), (255, 140, 40, 170), (230, 70, 20, 150)][j % 3]
            d.polygon([(x - 40, H * .74), (x + 8 * math.sin(ph * 1.3), H * .74 - h), (x + 40, H * .74)], fill=col)
    elif m == "gears":
        for g, gx, gy, sp in GEARS:
            r = g.rotate(age * 25 * sp + 8 * pulse * sp, resample=Image.BILINEAR); base.alpha_composite(r, (int(gx * W - r.width / 2), int(gy * H - r.height / 2)))
    elif m == "orbits":
        for j, r in enumerate([140, 230, 330, 440, 560]):
            a = age * (1.2 / (j + 1)) + j; x = W / 2 + r * 1.4 / 1.15 * math.cos(a); y = H / 2 + r * .6 / 1.15 * math.sin(a); s = 12 + 4 * j
            d.ellipse((x - s, y - s, x + s, y + s), fill=(180, 210, 255, 255))
    elif m == "rocket":
        y = -age * 12
        for j in range(12): fx = W * .32 / 1.15 + 140 * 0 + R.normal(0, 1) * 0; d.ellipse((W * .29 - 40 + 30 * math.sin(t * 20 + j), H * .66 + y + j * 30, W * .29 + 40, H * .66 + y + j * 30 + 70), fill=(255, 170 - j * 10, 60, max(0, 220 - j * 18)))
    elif m == "network":
        for q, (i, j) in enumerate(EDGES[::2]):
            u = (age * .7 + q * .13) % 1; x = lerp(NODES[i][0], NODES[j][0], u) * W; y = lerp(NODES[i][1], NODES[j][1], u) * H
            d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=(255, 255, 255, 230))
    elif m == "neural":
        ns = lnodes(); tb, kb = S.last(S.beats, t)
        for l, layer in enumerate(ns):
            for q, (x, y) in enumerate(layer):
                if (q * 3 + l + kb) % 4 == 0 and (t - S.q(tb)) < .35:
                    x2, y2 = (x - MW / 2) / 1.15 + W / 2, (y - MH / 2) / 1.15 + H / 2; d.ellipse((x2 - 30, y2 - 30, x2 + 30, y2 + 30), fill=(255, 240, 255, 200))
    elif m == "bulb" and pulse > .3:
        d.line([(W * .7, 0), (W * .66, H * .3), (W * .72, H * .3), (W * .64, H * .65)], fill=(220, 230, 255, int(255 * pulse)), width=10)

def particles(d, kind, t, e):
    n = int(80 + 180 * e)
    for j in range(n):
        p = PR[j]
        if kind in ("stars", "bits"):
            x, y = p[0] * W, p[1] * H; a = int(120 + 120 * math.sin(t * (1 + 2 * p[2]) + p[3] * 6))
            if kind == "bits": paste_txt = None; d.text((x, (y + t * 40 * p[2]) % H), "01"[j % 2], fill=(120, 255, 190, a // 2))
            else: s = 1 + 2.5 * p[2]; d.ellipse((x - s, y - s, x + s, y + s), fill=(255, 255, 255, a))
        elif kind in ("embers", "sparks"):
            y = H - ((t * (60 + 120 * p[2]) + p[1] * H) % H); x = p[0] * W + 30 * math.sin(t + p[3] * 6); s = 2 + 3 * p[2]
            d.ellipse((x - s, y - s, x + s, y + s), fill=(255, 170, 60, 200) if kind == "embers" else (200, 220, 255, 220))
        elif kind == "clouds":
            x = ((p[0] * W - t * 60 * (0.5 + p[2])) % (W + 400)) - 200; y = p[1] * H * .6; s = 40 + 60 * p[2]
            if j < 16: d.ellipse((x - s * 2, y - s, x + s * 2, y + s), fill=(255, 255, 255, 55))
        else:
            x = (p[0] * W + t * 15 * p[2]) % W; y = (p[1] * H + 10 * math.sin(t + p[3] * 6)); s = 1.5 + 2 * p[2]
            d.ellipse((x - s, y - s, x + s, y + s), fill=(255, 220, 170, 110))

def layer_for(k, t, e, pulse):
    t0 = S.q(ST[k]); age = t - t0; t1 = S.q(ST[k + 1]) if k + 1 < len(ST) else S.dur; span = t1 - t0
    base = bg(k).copy(); m = motif(k)
    z = 1 / 1.15 * (1 + 0.1 * age / span + 0.02 * pulse)        # slow zoom + beat pulse
    mw, mh = int(MW * z), int(MH * z); mi = m.resize((mw, mh), Image.BILINEAR)
    a = ease_out(age / 1.2)
    if a < 1: mi.putalpha(mi.split()[3].point(lambda v: int(v * a)))
    base.alpha_composite(mi, (int(W / 2 - mw / 2), int(H / 2 - mh / 2)))
    d = ImageDraw.Draw(base); particles(d, CH[k][8], t, e); animated(d, base, k, t, age, e, pulse)
    return base

def frame(i):
    t = i / FPS; e = S.e(t)
    k = int(np.searchsorted(STF, i, side="right") - 1); k = max(k, 0)
    t0 = S.q(ST[k]); age = t - t0; t1 = S.q(ST[k + 1]) if k + 1 < len(ST) else S.dur
    pulse = decay(S.beat_age(t), 5) * (0.4 + e)
    base = layer_for(k, t, e, pulse)
    if age < 0.6 and k > 0:   # cross-dissolve from previous chapter, starting exactly on the hit
        prev = layer_for(k - 1, t, e, pulse); base = Image.blend(prev, base, ease_in_out(age / 0.6))
    base.alpha_composite(VIG); base.alpha_composite(BAND)
    dz, de, tz, te, xz, xe = CH[k][:6]
    # beat-anchored reveal sequence inside a chapter: title on the hit, then each line on the following downbeats
    downs = [S.q(x) for x in S.down if S.q(x) > t0 + 0.3 and S.q(x) < t1]
    tl = [t0] + downs[:4] + [t0 + 9] * 4
    big = k in (0, len(CH) - 1)
    # chapter title (zh) slams in on the hit
    s_in = lerp(1.5, 1.0, ease_out(age / 0.5)); a = clamp(age / 0.15) * clamp((t1 - t) / 0.4)
    zimg = text_img(tz, "serif_cjk", 150 if big else 128, (255, 246, 228, 255), stroke=2, stroke_fill=(40, 20, 0, 255), spacing=14 if big else 4, glow=16, glow_color=(255, 170, 70))
    paste(base, zimg, W / 2, H * .40, s_in * (1 + 0.04 * age / max(t1 - t0, 1)), a)
    seq = [("date", tl[1]), ("en", tl[2]), ("detail", tl[3])] if dz else [("en", tl[1]), ("detail", tl[2])]
    for kind, ts in seq:
        if t < ts: continue
        ag = t - ts; aa = ease_out(ag / 0.4) * clamp((t1 - t) / 0.4); dy = 20 * (1 - ease_out(ag / 0.4))
        if kind == "date":
            paste(base, text_img(f"{dz}  ·  {de}", "serif_cjk", 46, (255, 210, 140, 255), stroke=2, stroke_fill=(30, 15, 0, 255), spacing=0), W / 2, H * .24 + dy, 1, aa)
        elif kind == "en":
            paste(base, text_img(te.upper() if big else te, "cinzel", 62 if big else 56, (255, 240, 215, 255), stroke=2, stroke_fill=(30, 15, 0, 255), spacing=4, glow=8, glow_color=(0, 0, 0)), W / 2, H * .56 + dy, 1, aa)
        else:
            paste(base, text_img(xz, "sans_cjk", 40, (255, 255, 255, 255), stroke=2, stroke_fill=(0, 0, 0, 255)), W / 2, H * .72 + dy, 1, aa)
            paste(base, text_img(xe, "sans_cjk_r", 32, (225, 225, 225, 255), stroke=2, stroke_fill=(0, 0, 0, 255)), W / 2, H * .78 + dy, 1, aa)
    if k > 0 and not big:
        paste(base, text_img(f"CHAPTER {k:02d}", "cinzel", 30, (255, 220, 170, 200), spacing=6), W / 2, H * .12, 1, clamp(age / 0.3) * clamp((t1 - t) / 0.4))
    # flash on the chapter hit (brighter in high-energy sections)
    fl = (0.7 if S.level(t0) == "high" else 0.4) * decay(age, 6) * (0.5 + e)
    if k > 0 and fl > 0.01: base.alpha_composite(Image.new("RGBA", (W, H), (255, 240, 220, int(255 * clamp(fl)))))
    # era timeline: one tick per chapter, current tick pulses on beats
    d = ImageDraw.Draw(base); x0, x1, ty = 160, 1760, 1000
    d.line((x0, ty, x1, ty), fill=(255, 255, 255, 90), width=3)
    prog = k + clamp(age / max(t1 - t0, 1)); d.line((x0, ty, x0 + (x1 - x0) * prog / (len(CH) - 1), ty), fill=(255, 200, 120, 255), width=5)
    for j in range(len(CH)):
        x = x0 + (x1 - x0) * j / (len(CH) - 1); r = 6 if j != k else 9 + 7 * pulse
        d.ellipse((x - r, ty - r, x + r, ty + r), fill=(255, 210, 140, 255) if j <= k else (255, 255, 255, 120))
    paste(base, text_img(ATTR, "sans_cjk_r", 19, (200, 200, 200, 210)), W / 2, H - 38)
    fade = clamp(t / 1.5) * clamp((S.dur - t) / 3.0)
    if fade < 1: base.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * (1 - fade)))))
    return base

if __name__ == "__main__":
    import os; os.makedirs(os.path.dirname(OUT), exist_ok=True)
    print("chapters", [(round(s, 2), how) for s, how in STARTS])
    pv = (float(sys.argv[1]), float(sys.argv[2])) if len(sys.argv) > 2 else None
    out = OUT if not pv else "/tmp/bsv/v4_preview.mp4"
    render(out, W, H, FPS, S.dur, AUDIO, frame, preview=pv); print(out)
