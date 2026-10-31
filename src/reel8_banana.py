import sys, math, random
from engine import *

YEL = (250, 214, 70); YEL_D = (196, 156, 40); BROWN = (90, 64, 30)
K = (150, 120, 255); K40 = (255, 120, 90); BETA = (120, 220, 255); GAMMA = (190, 255, 140)

def kitchen_bg(d, t):
    d.rectangle((0, 0, W, H), fill=(14, 16, 24, 255))
    for i in range(0, W, 90):
        d.line((i, 0, i, H), fill=(19, 22, 32, 255), width=2)
    for j in range(0, H, 90):
        d.line((0, j, W, j), fill=(19, 22, 32, 255), width=2)

def banana(d, cx, cy, s=1.0, ang=0.0, a=255):
    c, sn = math.cos(ang), math.sin(ang)
    P = lambda px, py: (cx + (px * c - py * sn) * s, cy + (px * sn + py * c) * s)
    outer = [P(-200 + 400 * k / 30, -80 * math.sin(math.pi * k / 30) + 30) for k in range(31)]
    inner = [P(200 - 400 * k / 30, -40 * math.sin(math.pi * k / 30) + 70) for k in range(31)]
    d.polygon(outer + inner, fill=YEL + (a,))
    d.line(outer, fill=YEL_D + (a,), width=max(2, int(6 * s)))
    d.line([P(-170 + 340 * k / 20, -55 * math.sin(math.pi * k / 20) + 48) for k in range(21)], fill=YEL_D + (a,), width=max(1, int(3 * s)))
    a0 = P(200, 60); a1 = P(230, 40)
    d.line((a0, a1), fill=BROWN + (a,), width=max(3, int(14 * s)))
    b0 = P(-200, 50)
    d.ellipse((b0[0] - 8 * s, b0[1] - 8 * s, b0[0] + 8 * s, b0[1] + 8 * s), fill=BROWN + (a,))

def atom(d, x, y, r, col, a=255, lbl=None, f=None):
    d.ellipse((x - r, y - r, x + r, y + r), fill=col + (a,))
    if lbl and f:
        w = d.textlength(lbl, font=f)
        d.text((x - w / 2, y - f.getbbox("Ág")[3] / 2 - 4), lbl, font=f, fill=(20, 20, 30, a))

def ray(d, x0, y0, ang, L, col, a=255, wiggle=False, t=0):
    pts = []
    for k in range(21):
        s = L * k / 20
        off = 10 * math.sin(k * 1.4 + t * 10) if wiggle else 0
        pts.append((x0 + s * math.cos(ang) - off * math.sin(ang), y0 + s * math.sin(ang) + off * math.cos(ang)))
    d.line(pts, fill=col + (a,), width=5)

F_ATOM = F("Black", 28)

def s0(img, d, u, t):
    banana(d, W / 2, 900 + 10 * math.sin(t * 2), 1.4, -0.15)
    k = seg(u, 0.3, 0.9)
    if k > 0.05:
        for i in range(6):
            ang = -math.pi / 2 + (i - 2.5) * 0.45
            ray(d, W / 2 + 90 * math.cos(ang), 860 + 90 * math.sin(ang), ang, lerp(0, 220, k), BETA, int(220 * k), True, t)
    text_c(d, 180, "A BANANA DA", F_HOOK, WHITE, maxw=1040)
    text_c(d, 280, "SUA FRUTEIRA", F_HOOK, WHITE, maxw=1040)
    text_c(d, 380, "É RADIOATIVA.", F_HOOK, ACC, maxw=1040, alpha=seg(u, 0.1, 0.25))
    return img

def s1(img, d, u, t):
    banana(d, W / 2, 900, 1.2, -0.15)
    label(d, 240, "RADIOATIVIDADE NATURAL", GREEN, seg(u, 0, 0.12))
    text_c(d, 340, "em quantidade ínfima", F_MID, WHITE, alpha=seg(u, 0.2, 0.35))
    text_c(d, 410, "sem risco", F_MID, GREEN, alpha=seg(u, 0.45, 0.6))
    return img

def s2(img, d, u, t):
    banana(d, W / 2, 1020, 0.9, -0.15, a=int(255 * (1 - 0.5 * seg(u, 0.3, 0.6))))
    rnd = random.Random(4)
    k = seg(u, 0.25, 0.6)
    for i in range(14):
        x = 300 + rnd.random() * 480; y = 640 + rnd.random() * 240
        atom(d, x, y, 34 * k, K, int(255 * k), "K", F_ATOM)
    label(d, 240, "POTÁSSIO", K, seg(u, 0, 0.12))
    text_c(d, 340, "cerca de 450 mg por banana", F_MID, WHITE, alpha=seg(u, 0.5, 0.65))
    return img

def s3(img, d, u, t):
    k = seg(u, 0.05, 0.4)
    n = 0
    for r in range(7):
        for c in range(9):
            x = 160 + c * 95; y = 560 + r * 75
            hot = (r, c) == (3, 4)
            col = K40 if (hot and u > 0.45) else K
            rr = 30 if not (hot and u > 0.45) else 30 + 6 * math.sin(t * 8)
            atom(d, x, y, rr * k, col, int(255 * k))
    label(d, 240, "QUASE TODO É ESTÁVEL", K, seg(u, 0, 0.12))
    text_c(d, 340, "≈ 1 em cada 8.500 átomos", F_MID, WHITE, alpha=seg(u, 0.4, 0.55))
    text_c(d, 1110, "potássio-40", F_LBL, K40, alpha=seg(u, 0.5, 0.65))
    return img

def s4(img, d, u, t):
    cx, cy = W / 2, 820
    atom(d, cx, cy, 80, K40, 255, "K-40", F_MID)
    k = seg(u, 0.25, 0.75)
    for i in range(3):
        ang = -0.6 + i * 1.9 + t * 0.2
        r = 70 + 330 * ((k + i * 0.33) % 1.0) * (1 if u > 0.25 else 0)
        x, y = cx + r * math.cos(ang), cy + r * math.sin(ang)
        d.ellipse((x - 12, y - 12, x + 12, y + 12), fill=BETA + (255,))
    ray(d, cx + 70, cy + 40, 0.5, lerp(0, 380, seg(u, 0.5, 0.9)), GAMMA, 255, True, t)
    label(d, 240, "ELE DECAI", K40, seg(u, 0, 0.12))
    text_c(d, 330, "elétrons (beta)", F_MID, BETA, alpha=seg(u, 0.25, 0.4))
    text_c(d, 400, "e, às vezes, raios gama", F_MID, GAMMA, alpha=seg(u, 0.5, 0.65))
    return img

def s5(img, d, u, t):
    k = seg(u, 0.1, 0.8)
    x0, x1 = 140, W - 140
    d.line((x0, 900, x1, 900), fill=GRAY + (255,), width=6)
    xx = lerp(x0, x1, k)
    d.ellipse((xx - 18, 882, xx + 18, 918), fill=K40 + (255,))
    text_c(d, 960, "metade decai em", F_MID, WHITE, alpha=seg(u, 0.3, 0.45))
    text_c(d, 600, "~1,3 BILHÃO", F_BIG, ACC, alpha=seg(u, 0.1, 0.25), maxw=1040)
    text_c(d, 740, "de anos", F_LBL, WHITE, alpha=seg(u, 0.15, 0.3))
    label(d, 240, "MEIA-VIDA LONGA", ACC, seg(u, 0, 0.12))
    return img

def s6(img, d, u, t):
    banana(d, 300, 880, 0.6, -0.15)
    k = seg(u, 0.3, 0.7)
    d.rounded_rectangle((560, 760, 960, 1000), 30, outline=WHITE + (255,), width=5)
    text_c(d, 790, "0,1 µSv", F_LBL, ACC, x=760, alpha=seg(u, 0.1, 0.25))
    text_c(d, 880, "≈ 1/100 da dose", F_SMALL, WHITE, x=760, alpha=k)
    text_c(d, 925, "natural de um dia", F_SMALL, WHITE, x=760, alpha=k)
    label(d, 240, "COMER UMA BANANA", ACC, seg(u, 0, 0.12))
    text_c(d, 330, "estimativa da EPA (EUA)", F_MID, WHITE, alpha=seg(u, 0.05, 0.2))
    return img

def s7(img, d, u, t):
    # corpo como silhueta simples com fluxo de potássio entrando e saindo
    cx = W / 2
    d.ellipse((cx - 70, 560, cx + 70, 700), fill=(70, 78, 96, 255))
    d.rounded_rectangle((cx - 130, 710, cx + 130, 1060), 60, fill=(70, 78, 96, 255))
    for i in range(5):
        p = ((t * 0.5 + i / 5) % 1.0)
        atom(d, lerp(160, cx - 130, p), 800, 18, K, 255)
        atom(d, lerp(cx + 130, W - 160, p), 960, 18, K, 255)
    text_c(d, 740, "entra", F_SMALL, WHITE, x=230)
    text_c(d, 1000, "sai", F_SMALL, WHITE, x=W - 230)
    label(d, 240, "O CORPO REGULA", GREEN, seg(u, 0, 0.12))
    text_c(d, 330, "o excesso de potássio sai", F_MID, WHITE, alpha=seg(u, 0.2, 0.35))
    text_c(d, 400, "não acumula", F_MID, GREEN, alpha=seg(u, 0.45, 0.6))
    return img

def s8(img, d, u, t):
    cx = W / 2
    d.ellipse((cx - 70, 560, cx + 70, 700), fill=(70, 78, 96, 255))
    d.rounded_rectangle((cx - 130, 710, cx + 130, 1060), 60, fill=(70, 78, 96, 255))
    rnd = random.Random(9)
    k = seg(u, 0.2, 0.6)
    for i in range(10):
        x = cx - 100 + rnd.random() * 200; y = 740 + rnd.random() * 290
        r = 8 + 3 * math.sin(t * 6 + i)
        d.ellipse((x - r, y - r, x + r, y + r), fill=K40 + (int(255 * k),))
    label(d, 240, "E VOCÊ TAMBÉM", ACC, seg(u, 0, 0.12))
    text_c(d, 330, "o corpo humano tem potássio-40", F_MID, WHITE, alpha=seg(u, 0.25, 0.4))
    return img

def s9(img, d, u, t):
    banana(d, W / 2, 1040, 0.9, -0.15)
    label(d, 240, "RESSALVA", RED, seg(u, 0, 0.12))
    text_c(d, 340, "a dose varia; o número é", F_MID, WHITE, alpha=seg(u, 0.05, 0.2))
    text_c(d, 400, "uma estimativa média", F_MID, WHITE, alpha=seg(u, 0.05, 0.2))
    text_c(d, 500, "curiosidade de física,", F_MID, GRAY, alpha=seg(u, 0.4, 0.55))
    text_c(d, 560, "não conselho de saúde", F_MID, GRAY, alpha=seg(u, 0.4, 0.55))
    return img

def s10(img, d, u, t):
    banana(d, W / 2, 1050, 0.9, -0.15)
    text_c(d, 520, "MANDA PRA QUEM", F_LBL, WHITE, alpha=seg(u, 0, 0.2))
    text_c(d, 610, "COME BANANA", F_LBL, ACC, alpha=seg(u, 0.05, 0.25))
    text_c(d, 740, "@parecefakeereal", F_LOGO, ACC, alpha=seg(u, 0.2, 0.4))
    return img

CHUNKS = [
 ("A banana da sua fruteira é radioativa.", "A banana da sua fruteira é radioativa.", s0),
 ("Natural e em dose ínfima. Sem risco.", "Natural e em dose ínfima. Sem risco.", s1),
 ("Vem do potássio: cerca de 450 mg por banana.", "Vem do potássio: cerca de quatrocentos e cinquenta miligramas por banana.", s2),
 ("Só cerca de 0,012% dele é potássio-40, um isótopo instável.", "Só cerca de zero vírgula zero doze por cento dele é potássio quarenta, um isótopo instável.", s3),
 ("Ele decai e solta elétrons e, às vezes, raios gama.", "Ele decai e solta elétrons e, às vezes, raios gama.", s4),
 ("Bem devagar: metade leva cerca de 1,3 bilhão de anos.", "Bem devagar: metade leva cerca de um vírgula três bilhão de anos.", s5),
 ("A EPA estima 0,1 µSv por banana: 1/100 da radiação natural de um dia.", "A agência ambiental americana estima zero vírgula um microsievert por banana: um centésimo da radiação natural de um dia.", s6),
 ("O corpo regula o potássio: o excesso sai, não acumula.", "O corpo regula o potássio: o excesso sai, não acumula.", s7),
 ("Aliás, você também tem potássio-40. É levemente radioativo.", "Aliás, você também tem potássio quarenta. É levemente radioativo.", s8),
 ("Ressalva: é estimativa média. Curiosidade, não conselho de saúde.", "Ressalva: é estimativa média. Curiosidade, não conselho de saúde.", s9),
 ("Manda pra quem come banana.", "Manda pra quem come banana.", s10),
]

if __name__ == "__main__":
    wd = os.path.join(os.environ.get("WORK_DIR", "/tmp/reelwork"), "reel8")
    note = "Animação autoral, sem escala · locução sintética"
    kw = dict(voice="M4", speed=float(os.environ.get("SPEED", "1.2")), bg_fn=kitchen_bg)
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        render(CHUNKS, wd, None, note, previews=[0.02, 0.1, 0.18, 0.27, 0.36, 0.45, 0.55, 0.64, 0.73, 0.82, 0.9, 0.98], **kw)
    else:
        render(CHUNKS, wd, sys.argv[1], note, **kw)
