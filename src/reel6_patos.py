import sys, math
from engine import *

SEA = (14, 32, 58); SEA2 = (22, 52, 88); FOAM = (170, 205, 235)
DUCK = (255, 208, 60); TURTLE = (80, 150, 255); FROG = (90, 205, 110); BEAVER = (220, 80, 70)
LAND = (64, 74, 60); SHIP = (150, 158, 172); CONT = (210, 96, 60)

def ocean_bg(d, t):
    d.rectangle((0, 0, W, H), fill=(9, 18, 34, 255))
    for i in range(14):
        y = 160 + i * 120
        pts = [(x, y + 10 * math.sin(x / 70 + t * 1.3 + i)) for x in range(0, W + 30, 30)]
        d.line(pts, fill=(18, 40, 70, 255), width=3)

def waves(d, y, t, amp=18, col=SEA2, alpha=255):
    pts = [(x, y + amp * math.sin(x / 90 + t * 2) + 0.4 * amp * math.sin(x / 37 - t * 3)) for x in range(-20, W + 40, 20)]
    d.polygon(pts + [(W + 40, H), (-20, H)], fill=col + (alpha,))
    d.line(pts, fill=FOAM + (alpha,), width=4)

def wave_y(x, y, t, amp=18):
    return y + amp * math.sin(x / 90 + t * 2) + 0.4 * amp * math.sin(x / 37 - t * 3)

def duck(d, x, y, s=1.0, col=DUCK, a=255):
    d.ellipse((x - 60 * s, y - 30 * s, x + 60 * s, y + 30 * s), fill=col + (a,))
    d.ellipse((x + 10 * s, y - 80 * s, x + 70 * s, y - 20 * s), fill=col + (a,))
    d.polygon([(x + 66 * s, y - 56 * s), (x + 100 * s, y - 48 * s), (x + 66 * s, y - 40 * s)], fill=(255, 130, 40, a))
    d.ellipse((x + 42 * s, y - 64 * s, x + 52 * s, y - 54 * s), fill=(20, 20, 20, a))

def turtle(d, x, y, s=1.0, a=255):
    for dx, dy in ((-50, 10), (50, 10), (-40, -20), (40, -20)):
        d.ellipse((x + dx * s - 14 * s, y + dy * s - 10 * s, x + dx * s + 14 * s, y + dy * s + 10 * s), fill=(60, 120, 220, a))
    d.ellipse((x + 52 * s, y - 16 * s, x + 84 * s, y + 10 * s), fill=(60, 120, 220, a))
    d.chord((x - 55 * s, y - 50 * s, x + 55 * s, y + 30 * s), 180, 360, fill=TURTLE + (a,))

def frog(d, x, y, s=1.0, a=255):
    d.ellipse((x - 55 * s, y - 35 * s, x + 55 * s, y + 30 * s), fill=FROG + (a,))
    for ex in (-28, 28):
        d.ellipse((x + ex * s - 18 * s, y - 60 * s, x + ex * s + 18 * s, y - 24 * s), fill=FROG + (a,))
        d.ellipse((x + ex * s - 7 * s, y - 50 * s, x + ex * s + 7 * s, y - 36 * s), fill=(20, 20, 20, a))

def beaver(d, x, y, s=1.0, a=255):
    d.ellipse((x - 100 * s, y - 10 * s, x - 30 * s, y + 25 * s), fill=(150, 60, 50, a))
    d.ellipse((x - 50 * s, y - 40 * s, x + 50 * s, y + 30 * s), fill=BEAVER + (a,))
    d.ellipse((x + 20 * s, y - 70 * s, x + 75 * s, y - 15 * s), fill=BEAVER + (a,))
    d.ellipse((x + 50 * s, y - 55 * s, x + 60 * s, y - 45 * s), fill=(20, 20, 20, a))

TOYS = [duck, turtle, frog, beaver]

def toy(d, k, x, y, s=1.0, a=255):
    if k == 0: duck(d, x, y, s, a=a)
    else: TOYS[k](d, x, y, s, a=a)

def s0(img, d, u, t):
    waves(d, 1000, t)
    for j, x in enumerate((260, 540, 820)):
        k = seg(u, 0.1 + 0.12 * j, 0.3 + 0.12 * j)
        y0 = lerp(560, wave_y(x, 1000, t) - 10, k)
        if k > 0.01: duck(d, x, y0, 1.1, a=int(255 * min(1, k * 2)))
    text_c(d, 200, "MILHARES DE PATINHOS", F_HOOK, WHITE, maxw=1040)
    text_c(d, 300, "CAÍRAM NO MAR", F_HOOK, WHITE, maxw=1040)
    text_c(d, 400, "E VIRARAM CIÊNCIA", F_HOOK, ACC, maxw=1040, alpha=seg(u, 0.12, 0.25))
    return img

def s1(img, d, u, t):
    roll = 6 * math.sin(t * 2.2)
    waves(d, 960, t, amp=34)
    cx, cy = W / 2, 900
    hull = [(cx - 330, cy - 40), (cx + 330, cy - 40), (cx + 270, cy + 50), (cx - 280, cy + 50)]
    rot = lambda p: (cx + (p[0] - cx) * math.cos(math.radians(roll)) - (p[1] - cy) * math.sin(math.radians(roll)),
                     cy + (p[0] - cx) * math.sin(math.radians(roll)) + (p[1] - cy) * math.cos(math.radians(roll)))
    d.polygon([rot(p) for p in hull], fill=SHIP + (255,))
    for i in range(6):
        x0 = cx - 280 + i * 92
        fall = seg(u, 0.4, 0.8) if i == 4 else 0
        box = [(x0, cy - 120), (x0 + 84, cy - 120), (x0 + 84, cy - 42), (x0, cy - 42)]
        box = [rot(p) for p in box]
        box = [(p[0] + 260 * fall, p[1] + 240 * fall * fall) for p in box]
        d.polygon(box, fill=(CONT if i != 4 else (230, 150, 60)) + (255,))
    # chuva
    for i in range(40):
        x = (i * 97 + t * 400) % W; y = (i * 173 + t * 900) % 700 + 450
        d.line((x, y, x - 12, y + 36), fill=(150, 170, 200, 140), width=2)
    label(d, 300, "PACÍFICO NORTE · JAN/1992", ACC, seg(u, 0, 0.12))
    text_c(d, 380, "tempestade derruba contêineres", F_MID, WHITE, alpha=seg(u, 0.15, 0.3))
    return img

def s2(img, d, u, t):
    names = ["patinhos", "tartarugas", "sapos", "castores"]
    for k in range(4):
        a = seg(u, 0.2 + 0.12 * k, 0.32 + 0.12 * k)
        x = 180 + k * 240; y = 900 + 12 * math.sin(t * 3 + k)
        if a > 0.01:
            toy(d, k, x, y, 0.95, a=int(255 * a))
            text_c(d, 1010, names[k], F_MID, WHITE, alpha=a, x=x)
    text_c(d, 560, "≈ 28.800", F_BIG, ACC, alpha=seg(u, 0.0, 0.15))
    label(d, 300, "UM SÓ CONTÊINER", ACC, seg(u, 0, 0.12))
    text_c(d, 700, "brinquedos de banho", F_MID, WHITE, alpha=seg(u, 0.1, 0.25))
    return img

# mapa esquemático do Pacífico Norte (sem escala)
SPILL = (330, 900); SITKA = (870, 600)
def coast(d, a=255):
    d.polygon([(700, 380), (1080, 380), (1080, 1100), (980, 1100), (930, 900), (900, 760), (860, 640), (760, 520)], fill=LAND + (a,))
    d.polygon([(0, 380), (180, 380), (150, 560), (90, 760), (0, 820)], fill=LAND + (a,))
    d.line([(180, 380), (700, 380)], fill=(80, 90, 76, a), width=4)

def s3(img, d, u, t):
    coast(d)
    d.ellipse((SPILL[0] - 14, SPILL[1] - 14, SPILL[0] + 14, SPILL[1] + 14), fill=(235, 77, 75, 255))
    text_c(d, SPILL[1] + 30, "queda", F_MID, (235, 120, 110), x=SPILL[0])
    k = seg(u, 0.1, 0.75)
    n = 40
    pts = [(lerp(SPILL[0], SITKA[0], z), lerp(SPILL[1], SITKA[1], z) - 160 * math.sin(math.pi * z)) for z in [i / n for i in range(n + 1)]]
    m = max(1, int(n * k))
    d.line(pts[:m + 1], fill=ACC + (255,), width=8)
    duck(d, pts[m][0], pts[m][1] - 10, 0.45)
    a2 = seg(u, 0.7, 0.85)
    d.ellipse((SITKA[0] - 16, SITKA[1] - 16, SITKA[0] + 16, SITKA[1] + 16), fill=ACC + (int(255 * a2),))
    text_c(d, SITKA[1] - 90, "Sitka, Alasca", F_MID, ACC, alpha=a2, x=SITKA[0] - 60)
    label(d, 220, "AINDA EM 1992", ACC, seg(u, 0, 0.12))
    text_c(d, 300, "mapa esquemático, sem escala", F_SMALL, GRAY, alpha=seg(u, 0, 0.12))
    return img

def s4(img, d, u, t):
    coast(d)
    pins = [(760, 530), (820, 590), (880, 680), (905, 780), (935, 900), (960, 1000), (130, 560), (95, 740)]
    for i, (x, y) in enumerate(pins):
        a = seg(u, 0.15 + 0.08 * i, 0.25 + 0.08 * i)
        d.ellipse((x - 14, y - 14, x + 14, y + 14), fill=(255, 255, 255, int(255 * a)))
        d.line((x, y - 14, x, y - 50), fill=(255, 255, 255, int(255 * a)), width=4)
    label(d, 220, "ACHADOS NA PRAIA", ACC, seg(u, 0, 0.12))
    text_c(d, 300, "Ebbesmeyer e Ingraham", F_MID, WHITE, alpha=seg(u, 0.05, 0.2))
    return img

def s5(img, d, u, t):
    coast(d, 200)
    k = seg(u, 0.1, 0.8)
    for j in range(6):
        pts = []
        for i in range(31):
            z = i / 30 * k
            pts.append((lerp(SPILL[0], 880 + j * 14, z) + 30 * math.sin(z * 6 + j), lerp(SPILL[1], 560 + j * 80, z) - 140 * math.sin(math.pi * z)))
        d.line(pts, fill=(120, 190, 255, 220), width=4)
    for (x, y) in [(820, 590), (880, 680), (905, 780)]:
        d.ellipse((x - 12, y - 12, x + 12, y + 12), fill=(255, 255, 255, int(255 * seg(u, 0.5, 0.7))))
    label(d, 220, "SIMULADOR × ACHADOS", BLUE, seg(u, 0, 0.12))
    text_c(d, 300, "correntes de superfície", F_MID, WHITE, alpha=seg(u, 0.05, 0.2))
    return img

def s6(img, d, u, t):
    cx, cy, rx, ry = W / 2, 860, 380, 230
    d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), outline=(90, 160, 255, 255), width=8)
    for i in range(8):
        a = i / 8 * 2 * math.pi
        x, y = cx + rx * math.cos(a), cy + ry * math.sin(a)
        dx, dy = -math.sin(a) * 26, math.cos(a) * 26 * ry / rx
        d.line((x - dx, y - dy, x + dx, y + dy), fill=(90, 160, 255, 255), width=8)
    ang = -seg(u, 0.1, 0.95) * 2 * math.pi + math.pi / 2
    duck(d, cx + rx * math.cos(ang), cy - ry * math.sin(ang) - 10, 0.55)
    text_c(d, cy - 40, "≈ 3 anos", F_BIG, ACC, alpha=seg(u, 0.3, 0.45))
    text_c(d, cy + 90, "por volta, em média", F_MID, WHITE, alpha=seg(u, 0.35, 0.5))
    label(d, 220, "GIRO SUBÁRTICO", BLUE, seg(u, 0, 0.12))
    text_c(d, 300, "do Pacífico Norte", F_MID, WHITE, alpha=seg(u, 0.05, 0.2))
    return img

def s7(img, d, u, t):
    cx, cy, rx, ry = W / 2, 900, 340, 200
    d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), outline=(90, 160, 255, 200), width=6)
    k1 = seg(u, 0.15, 0.6); k2 = seg(u, 0.35, 0.8)
    p1 = (lerp(cx + 200, cx + 260, k1), lerp(cy - 160, 520, k1))
    d.line((cx + 200, cy - 160, p1[0], p1[1]), fill=ACC + (255,), width=6)
    duck(d, p1[0], p1[1], 0.4)
    p2 = (lerp(cx - 200, cx - 280, k2), lerp(cy + 160, 1150, k2))
    d.line((cx - 200, cy + 160, p2[0], p2[1]), fill=ACC + (255,), width=6)
    turtle(d, p2[0], p2[1], 0.45)
    text_c(d, 430, "rumo ao Ártico", F_MID, WHITE, alpha=seg(u, 0.4, 0.55), x=cx + 220)
    label(d, 220, "ALGUNS ESCAPARAM", ACC, seg(u, 0, 0.12))
    return img

def s8(img, d, u, t):
    waves(d, 1050, t, amp=12)
    for i in range(30):
        a = 255 if i < 1 else 60
        x = 140 + (i % 10) * 90; y = 620 + (i // 10) * 110
        d.ellipse((x - 26, y - 26, x + 26, y + 26), fill=(DUCK if i < 1 else (90, 100, 120)) + (int(a * seg(u, 0.1, 0.3)),))
    label(d, 220, "RESSALVA", RED, seg(u, 0, 0.12))
    text_c(d, 300, "foi um acidente: plástico no mar", F_MID, WHITE, alpha=seg(u, 0.45, 0.6))
    text_c(d, 960, "só uma pequena parte foi achada", F_MID, ACC, alpha=seg(u, 0.15, 0.3))
    return img

def s9(img, d, u, t):
    waves(d, 1060, t, amp=12)
    duck(d, W / 2, wave_y(W / 2, 1060, t) - 10, 1.2)
    text_c(d, 560, "MANDA PRA ALGUÉM", F_LBL, WHITE, alpha=seg(u, 0, 0.2))
    text_c(d, 660, "@parecefakeereal", F_LOGO, ACC, alpha=seg(u, 0.1, 0.35))
    text_c(d, 760, "Parece fake. É real.", F_MID, WHITE, alpha=seg(u, 0.25, 0.5))
    return img

CHUNKS = [
 ("Milhares de patinhos de plástico caíram no mar. E viraram ciência.", "Milhares de patinhos de plástico caíram no mar. E viraram ciência.", s0),
 ("Em 1992, uma tempestade no Pacífico Norte derrubou contêineres de um navio.", "Em mil novecentos e noventa e dois, uma tempestade no Pacífico Norte derrubou contêineres de um navio.", s1),
 ("Num deles, uns 28.800 brinquedos de banho.", "Num deles, uns vinte e oito mil e oitocentos brinquedos de banho.", s2),
 ("No mesmo ano, milhares chegaram às praias perto de Sitka, no Alasca.", "No mesmo ano, milhares chegaram às praias perto de Sitka, no Alasca.", s3),
 ("Os oceanógrafos Ebbesmeyer e Ingraham juntaram relatos de quem os achava na areia.", "Os oceanógrafos Ebbesmeyer e Ingraham juntaram os relatos de quem os achava na areia.", s4),
 ("E usaram os achados para calibrar um simulador de correntes.", "E usaram esses achados para calibrar um simulador de correntes.", s5),
 ("Com outros objetos à deriva: uns 3 anos, em média, para dar a volta no giro do Pacífico Norte.", "Com outros objetos à deriva, a conta fechou: uns três anos, em média, para dar a volta no giro do Pacífico Norte.", s6),
 ("Alguns escaparam do circuito, rumo ao Ártico e a outras correntes.", "Alguns escaparam do circuito, rumo ao Ártico e a outras correntes.", s7),
 ("Ressalva: só uma pequena parte foi achada. E foi um acidente: plástico no mar.", "Ressalva: só uma pequena parte foi achada. E foi um acidente: plástico no mar.", s8),
 ("Manda pra quem ainda toma banho com patinho.", "Manda pra quem ainda toma banho com patinho.", s9),
]

if __name__ == "__main__":
    wd = os.path.join(os.environ.get("WORK_DIR", "/tmp/reelwork"), "reel6")
    note = "Animação autoral, sem escala · locução sintética"
    kw = dict(voice="M3", speed=float(os.environ.get("SPEED", "1.2")), bg_fn=ocean_bg)
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        render(CHUNKS, wd, None, note, previews=[0.03, 0.12, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.88, 0.95, 0.99], **kw)
    else:
        render(CHUNKS, wd, sys.argv[1], note, **kw)
