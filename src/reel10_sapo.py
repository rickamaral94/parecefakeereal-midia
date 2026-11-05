import sys, math, random
from engine import *

FROG = (150, 120, 70); FROG_D = (100, 78, 44); MASK = (60, 40, 28)
ICE = (170, 220, 255); ICE_D = (110, 170, 230); LIVER = (150, 60, 60); SUGAR = (255, 230, 120)
SNOW = (220, 232, 245)

def winter_bg(d, t):
    d.rectangle((0, 0, W, H), fill=(10, 14, 24, 255))
    r = random.Random(3)
    for i in range(90):
        x = (r.random() * W + 20 * math.sin(t + i)) % W
        y = (r.random() * H + t * (40 + 40 * r.random())) % H
        s = 2 + 3 * r.random()
        d.ellipse((x, y, x + s, y + s), fill=SNOW + (120,))
    d.rectangle((0, 1150, W, H), fill=(22, 26, 36, 255))

def frog(d, cx, cy, s=1.0, ice=0.0, hop=0.0, a=255):
    cy = cy - hop * 80 * s
    col = tuple(int(lerp(c, i, ice * 0.6)) for c, i in zip(FROG, ICE))
    cold = tuple(int(lerp(c, i, ice * 0.6)) for c, i in zip(FROG_D, ICE_D))
    # patas traseiras
    for sx in (-1, 1):
        d.ellipse((cx + sx * 150 * s - 70 * s, cy + 30 * s, cx + sx * 150 * s + 70 * s, cy + 110 * s), fill=cold + (a,))
        d.ellipse((cx + sx * 210 * s - 50 * s, cy + 90 * s, cx + sx * 210 * s + 50 * s, cy + 125 * s), fill=cold + (a,))
    d.ellipse((cx - 170 * s, cy - 90 * s, cx + 170 * s, cy + 110 * s), fill=col + (a,))
    d.ellipse((cx - 120 * s, cy - 150 * s, cx + 120 * s, cy + 10 * s), fill=col + (a,))
    # "máscara" escura típica da espécie
    d.polygon([(cx - 115 * s, cy - 85 * s), (cx - 40 * s, cy - 95 * s), (cx - 50 * s, cy - 55 * s), (cx - 110 * s, cy - 50 * s)], fill=MASK + (a,))
    d.polygon([(cx + 115 * s, cy - 85 * s), (cx + 40 * s, cy - 95 * s), (cx + 50 * s, cy - 55 * s), (cx + 110 * s, cy - 50 * s)], fill=MASK + (a,))
    for sx in (-1, 1):
        ex, ey = cx + sx * 70 * s, cy - 140 * s
        d.ellipse((ex - 38 * s, ey - 38 * s, ex + 38 * s, ey + 38 * s), fill=col + (a,))
        d.ellipse((ex - 22 * s, ey - 22 * s, ex + 22 * s, ey + 22 * s), fill=(20, 20, 24, a))
        d.ellipse((ex - 6 * s, ey - 14 * s, ex + 4 * s, ey - 4 * s), fill=(255, 255, 255, a))
        d.ellipse((cx + sx * 110 * s - 35 * s, cy + 80 * s, cx + sx * 110 * s + 35 * s, cy + 115 * s), fill=cold + (a,))
    if ice > 0.02:
        r = random.Random(11)
        for i in range(int(30 * ice)):
            x = cx + (r.random() - 0.5) * 360 * s; y = cy - 40 * s + (r.random() - 0.5) * 220 * s
            L = (12 + 22 * r.random()) * s
            for k in range(3):
                an = k * math.pi / 3
                d.line((x - L * math.cos(an), y - L * math.sin(an), x + L * math.cos(an), y + L * math.sin(an)), fill=ICE + (int(a * 0.8),), width=max(2, int(3 * s)))

def crystal(d, x, y, L, a=255):
    for k in range(3):
        an = k * math.pi / 3
        d.line((x - L * math.cos(an), y - L * math.sin(an), x + L * math.cos(an), y + L * math.sin(an)), fill=ICE + (a,), width=5)

def s0(img, d, u, t):
    ice = 0.5 + 0.5 * math.sin(t * 1.6)
    frog(d, W / 2, 880, 1.3, ice=ice, hop=max(0, math.sin(t * 3)) * (1 - ice))
    text_c(d, 200, "ESSE SAPO", F_HOOK, WHITE, maxw=1040)
    text_c(d, 300, "CONGELA", F_HOOK, ICE, maxw=1040)
    text_c(d, 400, "E VOLTA A PULAR", F_HOOK, ACC, maxw=1040, alpha=seg(u, 0.35, 0.5))
    return img

def s1(img, d, u, t):
    frog(d, W / 2, 900, 1.2)
    label(d, 220, "NA VERDADE, É UMA RÃ", ACC, seg(u, 0, 0.12))
    text_c(d, 320, "rã-da-madeira (Rana sylvatica)", F_MID, WHITE, alpha=seg(u, 0.15, 0.3))
    text_c(d, 390, "Alasca · Canadá · norte dos EUA", F_MID, GRAY, alpha=seg(u, 0.45, 0.6))
    return img

def s2(img, d, u, t):
    frog(d, W / 2, 900, 1.2, ice=0.15 * seg(u, 0.3, 1))
    k = seg(u, 0.1, 0.6)
    crystal(d, lerp(180, 360, k), lerp(600, 840, k), 30)
    label(d, 220, "COMEÇA PELA PELE", ICE, seg(u, 0, 0.12))
    text_c(d, 320, "um cristal de gelo encosta", F_MID, WHITE, alpha=seg(u, 0.2, 0.35))
    return img

def s3(img, d, u, t):
    cx, cy = W / 2, 860
    d.ellipse((cx - 260, cy - 200, cx + 260, cy + 220), outline=FROG + (255,), width=8)
    d.ellipse((cx - 110, cy - 40, cx + 60, cy + 80), fill=LIVER + (255,))
    text_c(d, cy - 5, "fígado", F_SMALL, WHITE, x=cx - 25)
    k = seg(u, 0.3, 1)
    r = random.Random(5)
    for i in range(18):
        ang = r.random() * 2 * math.pi; rr = 60 + 190 * ((k + r.random()) % 1.0) * (1 if u > 0.3 else 0)
        x, y = cx - 25 + rr * math.cos(ang), cy + 20 + rr * 0.8 * math.sin(ang)
        d.ellipse((x - 10, y - 10, x + 10, y + 10), fill=SUGAR + (255,))
    label(d, 220, "GLICOGÊNIO → GLICOSE", SUGAR, seg(u, 0, 0.12))
    text_c(d, 320, "o sangue espalha o açúcar", F_MID, WHITE, alpha=seg(u, 0.35, 0.5))
    return img

def s4(img, d, u, t):
    cx, cy = W / 2, 860
    k = seg(u, 0.2, 0.8)
    d.rounded_rectangle((cx - 300, cy - 230, cx + 300, cy + 230), 80, fill=ICE_D + (int(160 * k),))
    for i in range(int(16 * k)):
        r = random.Random(i)
        crystal(d, cx - 270 + r.random() * 540, cy - 200 + r.random() * 400, 18, 220)
    for j, (ox, oy) in enumerate([(-110, -60), (100, -50), (0, 90)]):
        d.ellipse((cx + ox - 80, cy + oy - 60, cx + ox + 80, cy + oy + 60), fill=(200, 120, 110, 255))
        for q in range(4):
            r = random.Random(j * 10 + q)
            x = cx + ox + (r.random() - 0.5) * 100; y = cy + oy + (r.random() - 0.5) * 70
            d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=SUGAR + (255,))
    label(d, 220, "GELO POR FORA", ICE, seg(u, 0, 0.12))
    text_c(d, 320, "glicose protege por dentro", F_MID, SUGAR, alpha=seg(u, 0.3, 0.45))
    text_c(d, 1110, "esquema, sem escala", F_SMALL, GRAY)
    return img

def s5(img, d, u, t):
    cx, cy, R = W / 2, 860, 230
    k = seg(u, 0.1, 0.7)
    d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(60, 70, 90, 255))
    d.pieslice((cx - R, cy - R, cx + R, cy + R), -90, -90 + 240 * k, fill=ICE + (255,))
    text_c(d, cy - 50, "até ~2/3", F_LBL, (20, 30, 50), alpha=seg(u, 0.6, 0.75))
    label(d, 220, "DA ÁGUA DO CORPO", ICE, seg(u, 0, 0.12))
    text_c(d, 320, "vira gelo", F_MID, WHITE, alpha=seg(u, 0.2, 0.35))
    return img

def s6(img, d, u, t):
    frog(d, W / 2, 1000, 0.8, ice=1.0)
    k = seg(u, 0.1, 0.8)
    pts = []
    for i in range(61):
        x = 140 + i * 13.3
        beat = math.exp(-((i % 15) - 7) ** 2 / 2) * 90 * (1 - k) if x < lerp(W - 140, 140, 0) else 0
        pts.append((x, 620 - beat))
    d.line(pts, fill=RED + (255,), width=6)
    label(d, 220, "O CORAÇÃO PARA", RED, seg(u, 0, 0.12))
    text_c(d, 320, "ela parece morta", F_MID, WHITE, alpha=seg(u, 0.45, 0.6))
    return img

def s7(img, d, u, t):
    text_c(d, 560, "−16 °C", F_BIG, ICE, alpha=seg(u, 0.1, 0.25), maxw=1040)
    text_c(d, 720, "rãs do Alasca, em laboratório", F_MID, WHITE, alpha=seg(u, 0.25, 0.4))
    frog(d, W / 2, 1060, 0.55, ice=1.0)
    label(d, 220, "RECORDE DO NORTE", ACC, seg(u, 0, 0.12))
    return img

def s8(img, d, u, t):
    ice = 1 - seg(u, 0.05, 0.5)
    hop = max(0, math.sin(t * 4)) * seg(u, 0.55, 0.7)
    frog(d, W / 2, 900, 1.1, ice=ice, hop=hop)
    label(d, 220, "NO DEGELO", GREEN, seg(u, 0, 0.12))
    text_c(d, 320, "de pé em ~2 dias", F_MID, WHITE, alpha=seg(u, 0.45, 0.6))
    return img

def s9(img, d, u, t):
    frog(d, W / 2, 980, 0.9, ice=0.6)
    label(d, 220, "RESSALVA", RED, seg(u, 0, 0.12))
    text_c(d, 320, "há limite de frio e de gelo", F_MID, WHITE, alpha=seg(u, 0.05, 0.2))
    text_c(d, 390, "e muda entre populações", F_MID, GRAY, alpha=seg(u, 0.4, 0.55))
    return img

def s10(img, d, u, t):
    frog(d, W / 2, 1060, 0.7, hop=max(0, math.sin(t * 4)))
    text_c(d, 440, "SEGUE PRA MAIS", F_LBL, WHITE, alpha=seg(u, 0, 0.2))
    text_c(d, 530, "CIÊNCIA ASSIM", F_LBL, WHITE, alpha=seg(u, 0.05, 0.25))
    text_c(d, 660, "@parecefakeereal", F_LOGO, ACC, alpha=seg(u, 0.2, 0.4))
    return img

CHUNKS = [
 ("Esse sapo congela no inverno — e volta a pular na primavera.", "Esse sapo congela no inverno, e volta a pular na primavera.", s0),
 ("Na verdade é uma rã: a rã-da-madeira, da América do Norte.", "Na verdade, é uma rã: a rã-da-madeira, da América do Norte.", s1),
 ("O congelamento começa quando um cristal de gelo toca a pele.", "O congelamento começa quando um cristal de gelo toca a pele.", s2),
 ("Em minutos, o fígado transforma glicogênio em glicose, que o sangue espalha.", "Em minutos, o fígado transforma glicogênio em glicose, que o sangue espalha.", s3),
 ("A glicose protege as células. O gelo fica fora: na cavidade do corpo e sob a pele.", "A glicose protege as células. O gelo fica fora: na cavidade do corpo e sob a pele.", s4),
 ("Até cerca de dois terços da água do corpo vira gelo.", "Até cerca de dois terços da água do corpo vira gelo.", s5),
 ("O coração desacelera e para. Ela parece morta.", "O coração desacelera e para. Ela parece morta.", s6),
 ("Em laboratório, rãs do Alasca aguentaram −16 °C.", "Em laboratório, rãs do Alasca aguentaram menos dezesseis graus.", s7),
 ("No degelo, o coração volta a bater. Em cerca de 2 dias, estavam de pé.", "No degelo, o coração volta a bater. Em cerca de dois dias, estavam de pé.", s8),
 ("Ressalva: há limite de frio e de gelo, que muda entre populações.", "Ressalva: há limite de frio e de gelo, que muda entre populações.", s9),
 ("Segue @parecefakeereal pra mais ciência assim.", "Segue o Parece Fake e Real pra mais ciência assim.", s10),
]

if __name__ == "__main__":
    wd = os.path.join(os.environ.get("WORK_DIR", "/tmp/reelwork"), "reel10")
    note = "Animação autoral, sem escala · locução sintética"
    kw = dict(voice="M4", speed=float(os.environ.get("SPEED", "1.25")), bg_fn=winter_bg)
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        render(CHUNKS, wd, None, note, previews=[0.01, 0.08, 0.16, 0.25, 0.34, 0.43, 0.52, 0.6, 0.7, 0.8, 0.9, 0.98], **kw)
    else:
        render(CHUNKS, wd, sys.argv[1], note, **kw)
