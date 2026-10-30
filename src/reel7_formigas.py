import sys, math, random
from engine import *

WATER = (16, 44, 70); WATER2 = (24, 62, 96); FOAM = (150, 195, 230)
ANT = (170, 52, 30); ANT_D = (110, 30, 18); AIR = (210, 235, 255)

def water_bg(d, t):
    d.rectangle((0, 0, W, H), fill=(10, 22, 36, 255))
    for i in range(14):
        y = 160 + i * 120
        pts = [(x, y + 8 * math.sin(x / 80 + t * 1.1 + i)) for x in range(0, W + 30, 30)]
        d.line(pts, fill=(18, 42, 66, 255), width=3)

def surface(d, y, t, amp=12, a=255):
    pts = [(x, y + amp * math.sin(x / 90 + t * 2) + 0.4 * amp * math.sin(x / 41 - t * 3)) for x in range(-20, W + 40, 20)]
    d.polygon(pts + [(W + 40, H), (-20, H)], fill=WATER2 + (a,))
    d.line(pts, fill=FOAM + (a,), width=4)

def ant(d, x, y, s=1.0, ang=0.0, a=255, t=0.0):
    c, sn = math.cos(ang), math.sin(ang)
    P = lambda px, py: (x + (px * c - py * sn) * s, y + (px * sn + py * c) * s)
    wig = 4 * math.sin(t * 12 + x * 0.05)
    for k, lx in enumerate((-10, 0, 10)):
        for side in (-1, 1):
            p0 = P(lx, 0); p1 = P(lx + (wig if side > 0 else -wig) + (k - 1) * 8, side * 26)
            d.line((p0, p1), fill=ANT_D + (a,), width=max(1, int(3 * s)))
    for (cx, rx, ry) in ((-26, 14, 11), (0, 11, 8), (24, 12, 10)):
        q = [P(cx + rx * math.cos(z / 8 * 2 * math.pi), ry * math.sin(z / 8 * 2 * math.pi)) for z in range(8)]
        d.polygon(q, fill=ANT + (a,))
    p0 = P(34, -4); p1 = P(50, -16); p2 = P(34, 4); p3 = P(50, 16)
    d.line((p0, p1), fill=ANT_D + (a,), width=max(1, int(3 * s)))
    d.line((p2, p3), fill=ANT_D + (a,), width=max(1, int(3 * s)))

def raft(d, cx, cy, rx, ry, t, n=70, a=255, seed=7):
    d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=(90, 30, 18, a))
    rnd = random.Random(seed)
    for i in range(n):
        r = math.sqrt(rnd.random()); th = rnd.random() * 2 * math.pi
        x = cx + 0.92 * rx * r * math.cos(th); y = cy + 0.85 * ry * r * math.sin(th)
        ant(d, x, y, 0.45, rnd.random() * 6.28, a, t)

def s0(img, d, u, t):
    surface(d, 1080, t)
    k = seg(u, 0.1, 0.6)
    raft(d, W / 2, 1080, lerp(80, 330, k), lerp(70, 70, k), t, n=int(lerp(12, 60, k)))
    text_c(d, 170, "COMO ESSAS", F_HOOK, WHITE, maxw=1040)
    text_c(d, 270, "FORMIGAS VIRAM", F_HOOK, WHITE, maxw=1040)
    text_c(d, 370, "UM BARCO", F_HOOK, ACC, maxw=1040)
    text_c(d, 470, "QUANDO A ÁGUA SOBE?", F_HOOK, WHITE, maxw=1040, alpha=seg(u, 0.1, 0.22))
    return img

def s1(img, d, u, t):
    lvl = lerp(1150, 900, seg(u, 0.1, 0.8))
    d.polygon([(250, 1150), (830, 1150), (640, 760), (440, 760)], fill=(120, 84, 56, 255))
    for i in range(10):
        ant(d, 470 + (i % 5) * 36, 800 + (i // 5) * 30 - 6 * math.sin(t * 3 + i), 0.5, 0.3 * i, 255, t)
    surface(d, lvl, t, amp=10, a=230)
    label(d, 240, "FORMIGA-DE-FOGO", ACC, seg(u, 0, 0.12))
    text_c(d, 330, "Solenopsis invicta", F_MID, WHITE, alpha=seg(u, 0.05, 0.2))
    text_c(d, 400, "nativa da América do Sul", F_MID, GRAY, alpha=seg(u, 0.15, 0.3))
    return img

def s2(img, d, u, t):
    surface(d, 1080, t)
    k = seg(u, 0.15, 0.6)
    y = lerp(520, 1030, k * k)
    d.ellipse((W / 2 - 150, y - 150, W / 2 + 150, y + 150), fill=(90, 30, 18, 255))
    rnd = random.Random(3)
    for i in range(40):
        th = rnd.random() * 6.28; r = 120 * math.sqrt(rnd.random())
        ant(d, W / 2 + r * math.cos(th), y + r * math.sin(th), 0.45, rnd.random() * 6.28, 255, t)
    label(d, 220, "TESTE NO LABORATÓRIO", BLUE, seg(u, 0, 0.12))
    text_c(d, 310, "até 7.000 formigas", F_LBL, ACC, alpha=seg(u, 0.1, 0.25))
    return img

def s3(img, d, u, t):
    surface(d, 1000, t, amp=8)
    k = seg(u, 0.05, 0.75)
    raft(d, W / 2, 1000, lerp(150, 430, k), lerp(150, 60, k), t, n=80)
    text_c(d, 470, "< 100 s", F_BIG, ACC, alpha=seg(u, 0.0, 0.15))
    label(d, 240, "DE BOLA A PANQUECA", ACC, seg(u, 0, 0.12))
    text_c(d, 640, "≈ 8 mm de espessura", F_MID, WHITE, alpha=seg(u, 0.55, 0.7))
    return img

def s4(img, d, u, t):
    k = seg(u, 0.1, 0.5)
    ant(d, lerp(260, 420, k), 820, 3.2, 0.0, 255, t)
    ant(d, lerp(820, 660, k), 880, 3.2, math.pi, 255, t)
    tags = [("mandíbulas", 380), ("garras", 470), ("almofadas adesivas", 560)]
    for i, (s, y) in enumerate(tags):
        text_c(d, 1000 + i * 70, s, F_MID, [ACC, WHITE, WHITE][i], alpha=seg(u, 0.35 + 0.12 * i, 0.47 + 0.12 * i))
    label(d, 240, "UMA SEGURA A OUTRA", ACC, seg(u, 0, 0.12))
    text_c(d, 330, "esquema, sem escala", F_SMALL, GRAY, alpha=seg(u, 0, 0.12))
    return img

def s5(img, d, u, t):
    surface(d, 1000, t, amp=6)
    # corte lateral da jangada
    d.rounded_rectangle((120, 900, W - 120, 1000), 40, fill=(90, 30, 18, 255))
    for i in range(14):
        ant(d, 170 + i * 57, 925 + 25 * (i % 2), 0.55, 0.0 if i % 2 else math.pi, 255, t)
    a = seg(u, 0.35, 0.6)
    rnd = random.Random(5)
    for i in range(22):
        x = 150 + rnd.random() * (W - 300); y = 985 + rnd.random() * 25
        r = 6 + rnd.random() * 8
        d.ellipse((x - r, y - r, x + r, y + r), outline=AIR + (int(255 * a),), width=3)
    label(d, 240, "REPELE A ÁGUA", BLUE, seg(u, 0, 0.12))
    text_c(d, 330, "e prende bolhas de ar", F_MID, WHITE, alpha=seg(u, 0.3, 0.45))
    text_c(d, 1090, "ar preso entre os corpos", F_MID, AIR, alpha=a)
    return img

def s6(img, d, u, t):
    surface(d, 1000, t, amp=6)
    d.rounded_rectangle((120, 890, W - 120, 1000), 40, fill=(90, 30, 18, 255))
    for i in range(14):
        ant(d, 170 + i * 57, 975, 0.5, 0.0, 255, t)
        if i != 7: ant(d, 170 + i * 57, 915, 0.5, math.pi, 255, t)
    k = seg(u, 0.5, 0.85)
    ant(d, 170 + 7 * 57, lerp(975, 915, k), 0.5, -math.pi / 2, 255, t)
    text_c(d, 1060, "camada de baixo", F_MID, ACC, alpha=seg(u, 0.1, 0.25))
    label(d, 240, "METADE SUSTENTA", ACC, seg(u, 0, 0.12))
    text_c(d, 330, "buraco? outra ocupa", F_MID, WHITE, alpha=seg(u, 0.5, 0.65))
    return img

def s7(img, d, u, t):
    surface(d, 1020, t, amp=14)
    x = lerp(300, 780, seg(u, 0, 1))
    raft(d, x, 1020 + 10 * math.sin(t * 2), 260, 55, t, n=50)
    for i in range(int(1 + 4 * seg(u, 0.1, 0.9))):
        cx = 180 + i * 180
        d.ellipse((cx - 40, 560 - 40, cx + 40, 560 + 40), outline=ACC + (255,), width=6)
        d.chord((cx - 40, 560 - 40, cx + 40, 560 + 40), 90, 270, fill=ACC + (255,))
    label(d, 240, "FLUTUA POR DIAS", ACC, seg(u, 0, 0.12))
    text_c(d, 700, "segundo os pesquisadores", F_MID, WHITE, alpha=seg(u, 0.2, 0.35))
    return img

def s8(img, d, u, t):
    k = seg(u, 0.45, 0.9)
    surface(d, 1000, t, amp=6)
    raft(d, W / 2, 1000 + 120 * k, 300, 55, t, n=50, a=int(255 * (1 - 0.6 * k)))
    label(d, 240, "RESSALVA", RED, seg(u, 0, 0.12))
    text_c(d, 330, "uma espécie, em laboratório", F_MID, WHITE, alpha=seg(u, 0.05, 0.2))
    text_c(d, 700, "com sabão na água, afunda", F_MID, ACC, alpha=seg(u, 0.4, 0.55))
    return img

def s9(img, d, u, t):
    surface(d, 1080, t, amp=10)
    raft(d, W / 2, 1080, 300, 60, t, n=50)
    text_c(d, 560, "SEGUE O PERFIL", F_LBL, WHITE, alpha=seg(u, 0, 0.2))
    text_c(d, 660, "@parecefakeereal", F_LOGO, ACC, alpha=seg(u, 0.1, 0.35))
    text_c(d, 760, "Parece fake. É real.", F_MID, WHITE, alpha=seg(u, 0.25, 0.5))
    return img

CHUNKS = [
 ("Como essas formigas viram um barco quando a água sobe?", "Como essas formigas viram um barco quando a água sobe?", s0),
 ("A formiga-de-fogo vem da América do Sul. Quando o ninho alaga, a colônia vira jangada.", "A formiga-de-fogo vem da América do Sul. Quando o ninho alaga, a colônia vira jangada.", s1),
 ("Na Georgia Tech, pesquisadores jogaram bolas de até 7.000 formigas na água.", "Na Georgia Tech, pesquisadores jogaram bolas de até sete mil formigas na água.", s2),
 ("Em menos de 100 segundos, a bola vira uma panqueca de uns 8 milímetros.", "Em menos de cem segundos, a bola vira uma panqueca de uns oito milímetros.", s3),
 ("Elas se seguram com mandíbulas, garras e almofadas adesivas nas patas.", "Elas se seguram com mandíbulas, garras e almofadas adesivas nas patas.", s4),
 ("Cada formiga repele um pouco a água. Juntas, prendem bolhas de ar.", "Cada formiga repele um pouco a água. Juntas, prendem bolhas de ar.", s5),
 ("Cerca de metade fica embaixo, sustentando o resto. Se uma sai, outra ocupa o lugar.", "Cerca de metade fica embaixo, sustentando o resto. Se uma sai, outra ocupa o lugar.", s6),
 ("Segundo os pesquisadores, a jangada flutua por dias.", "Segundo os pesquisadores, a jangada flutua por dias.", s7),
 ("Ressalva: vale para essa espécie, em laboratório. Com sabão na água, ela afunda.", "Ressalva: vale para essa espécie, em laboratório. Com sabão na água, ela afunda.", s8),
 ("Segue o perfil pra mais ciência que parece mentira.", "Segue o perfil pra mais ciência que parece mentira.", s9),
]

if __name__ == "__main__":
    wd = os.path.join(os.environ.get("WORK_DIR", "/tmp/reelwork"), "reel7")
    note = "Animação autoral, sem escala · locução sintética"
    kw = dict(voice="M4", speed=float(os.environ.get("SPEED", "1.2")), bg_fn=water_bg)
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        render(CHUNKS, wd, None, note, previews=[0.03, 0.12, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.88, 0.95, 0.99], **kw)
    else:
        render(CHUNKS, wd, sys.argv[1], note, **kw)
