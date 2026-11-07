import sys, math, random
from engine import *

WATER = (110, 190, 255); WATER_L = (190, 230, 255); VAPOR = (225, 240, 255)
PAN = (58, 62, 72); PAN_L = (92, 98, 110); HOT = (255, 110, 50); FLAME = (255, 150, 60)
PAN_Y = 1080  # topo da chapa

def mix(c, k, base=(20, 18, 26)):
    k = clamp(k)
    return tuple(int(lerp(b, x, k)) for b, x in zip(base, c)) + (255,)

def kitchen_bg(d, t):
    for y in range(0, H, 40):
        k = y / H
        d.rectangle((0, y, W, y + 40), fill=(int(lerp(20, 12, k)), int(lerp(18, 12, k)), int(lerp(26, 18, k)), 255))

def pan(d, t, heat=1.0, y=PAN_Y, x0=90, x1=990):
    # chama embaixo
    r = random.Random(3)
    for i in range(16):
        x = x0 + 60 + i * (x1 - x0 - 120) / 15
        h = (40 + 30 * r.random()) * (0.7 + 0.3 * math.sin(t * 9 + i)) * heat
        d.polygon([(x - 18, y + 90), (x, y + 90 - h - 40), (x + 18, y + 90)], fill=FLAME + (int(200 * heat),))
    d.rounded_rectangle((x0, y, x1, y + 50), 14, fill=PAN + (255,))
    # brilho de calor na superfície
    a = int(160 * heat)
    if a > 5:
        d.rectangle((x0 + 10, y, x1 - 10, y + 6), fill=HOT + (a,))
    d.rounded_rectangle((x1 - 10, y + 8, x1 + 90, y + 34), 10, fill=PAN_L + (255,))

def drop(d, cx, by, w=150, h=110, lift=0, a=255):
    """Gota apoiada (by = base). lift = altura do colchão de vapor (px)."""
    y1 = by - lift
    d.ellipse((cx - w / 2, y1 - h, cx + w / 2, y1), fill=WATER + (a,))
    d.ellipse((cx - w * 0.28, y1 - h * 0.85, cx - w * 0.05, y1 - h * 0.6), fill=WATER_L + (int(a * 0.9),))

def flat_drop(d, cx, by, w, h, a=255):
    d.ellipse((cx - w / 2, by - h, cx + w / 2, by + 6), fill=WATER + (a,))

def steam(d, t, cx, cy, n=6, a=200, spread=80):
    ks = sorted(((t * 0.9 + i / n) % 1.0, i) for i in range(n))[::-1]
    for k, i in ks:
        x = cx + spread * math.sin(i * 2.1 + t * 2) * k
        y = cy - k * 260
        r = (16 + 30 * k) * (1 - 0.6 * max(0, k - 0.7) / 0.3)
        d.ellipse((x - r, y - r, x + r, y + r), fill=mix(VAPOR, 0.45 + 0.5 * (1 - k)))

def cushion(d, cx, by, w, lift, t, a=255):
    """Colchão de vapor sob a gota, com setas de escape."""
    d.rectangle((cx - w / 2, by - lift, cx + w / 2, by), fill=VAPOR + (int(a * 0.55),))
    for s in (-1, 1):
        k = (t * 1.5) % 1.0
        x = cx + s * (w / 2 + 10 + 60 * k)
        d.line((cx + s * w / 2, by - lift / 2, x, by - lift / 2), fill=mix(VAPOR, (a / 255) * (1 - k)), width=5)

def thermo(d, x, y, frac, txt, a=1.0):
    d.rounded_rectangle((x - 22, y, x + 22, y + 300), 22, outline=WHITE + (int(255 * a),), width=5)
    d.ellipse((x - 40, y + 280, x + 40, y + 360), fill=HOT + (int(255 * a),))
    top = y + 300 - 280 * frac
    d.rectangle((x - 10, top, x + 10, y + 300), fill=HOT + (int(255 * a),))
    text_c(d, y + 380, txt, F_MID, HOT, alpha=a, x=x, maxw=400)

def s0(img, d, u, t):
    pan(d, t)
    bob = 8 * math.sin(t * 7)
    cx = W / 2 + 140 * math.sin(t * 1.6)
    cushion(d, cx, PAN_Y, 120, 18, t)
    drop(d, cx, PAN_Y, lift=18 + bob)
    text_c(d, 220, "A GOTA", F_HOOK, WHITE, maxw=1040)
    text_c(d, 320, "NÃO FERVE", F_HOOK, ACC, maxw=1040)
    text_c(d, 420, "ELA FLUTUA", F_HOOK, WATER_L, maxw=1040, alpha=seg(u, 0.12, 0.25))
    return img

def s1(img, d, u, t):
    pan(d, t)
    drop(d, W / 2, PAN_Y, lift=18 + 6 * math.sin(t * 7))
    label(d, 220, "PARECE AO CONTRÁRIO", ACC, seg(u, 0, 0.12))
    text_c(d, 320, "chapa mais quente,", F_MID, WHITE, alpha=seg(u, 0.2, 0.35))
    text_c(d, 390, "gota que dura mais", F_MID, WATER_L, alpha=seg(u, 0.4, 0.55))
    text_c(d, 470, "(numa certa faixa de temperatura)", F_SMALL, GRAY, alpha=seg(u, 0.5, 0.65))
    return img

def s2(img, d, u, t):
    pan(d, t, heat=0.35)
    k = seg(u, 0.15, 0.9)
    flat_drop(d, W / 2, PAN_Y, 260 * (1 - 0.7 * k) + 10, 40 * (1 - k) + 4, a=int(255 * (1 - 0.6 * k)))
    for j in range(5):
        x = W / 2 - 100 + j * 50
        steam(d, t + j * 0.3, x, PAN_Y - 30, n=3, a=230, spread=30)
    thermo(d, 900, 520, 0.25, "pouco acima de 100 °C", seg(u, 0, 0.15))
    label(d, 220, "CHAPA MENOS QUENTE", ACC, seg(u, 0, 0.12))
    text_c(d, 320, "a gota encosta e chia", F_MID, WHITE, alpha=seg(u, 0.15, 0.3))
    text_c(d, 390, "some em segundos", F_MID, RED, alpha=seg(u, 0.45, 0.6))
    return img

def s3(img, d, u, t):
    pan(d, t)
    cx = W / 2 - 120 + 240 * (0.5 + 0.5 * math.sin(t * 1.3))
    cushion(d, cx, PAN_Y, 110, 16, t)
    drop(d, cx, PAN_Y, 140, 105, lift=16 + 6 * math.sin(t * 8))
    thermo(d, 900, 520, 0.7, "perto de 200 °C", seg(u, 0, 0.15))
    label(d, 220, "CHAPA BEM QUENTE", ACC, seg(u, 0, 0.12))
    text_c(d, 320, "vira bolinha e dança", F_MID, WHITE, alpha=seg(u, 0.2, 0.35))
    text_c(d, 390, "mais de 1 minuto", F_MID, GREEN, alpha=seg(u, 0.5, 0.65))
    return img

def zoom_scene(d, u, t, lift_k=1.0, show_arrows=False):
    # visão ampliada: base da gota sobre a chapa
    y = 1100
    d.rectangle((0, y, W, y + 120), fill=PAN + (255,))
    d.rectangle((0, y, W, y + 8), fill=HOT + (170,))
    lift = 70 * lift_k
    d.rectangle((120, y - lift, W - 120, y), fill=VAPOR + (140,))
    d.ellipse((60, 560, W - 60, y - lift + 40), fill=WATER + (255,))
    d.ellipse((220, 620, 420, 760), fill=WATER_L + (200,))
    if show_arrows:
        r = random.Random(4)
        for i in range(9):
            x = 170 + i * 92
            k = (t * 1.2 + r.random()) % 1.0
            yy = y - 6 - k * (lift - 10)
            d.line((x, y - 6, x, yy), fill=mix(WHITE, 0.4 + 0.6 * (1 - k), (200, 215, 230)), width=6)
    return y, lift

def s4(img, d, u, t):
    y, lift = zoom_scene(d, u, t, lift_k=seg(u, 0.25, 0.7), show_arrows=True)
    label(d, 220, "ZOOM NA BASE", ACC, seg(u, 0, 0.12))
    text_c(d, 320, "a parte de baixo", F_MID, WHITE, alpha=seg(u, 0.15, 0.3))
    text_c(d, 390, "vira vapor na hora", F_MID, VAPOR, alpha=seg(u, 0.35, 0.5))
    text_c(d, 480, "esquema, sem escala", F_SMALL, GRAY)
    return img

def s5(img, d, u, t):
    y, lift = zoom_scene(d, u, t, show_arrows=True)
    k = seg(u, 0.3, 0.5)
    d.line((W - 90, y - lift, W - 90, y), fill=ACC + (int(255 * k),), width=6)
    text_c(d, 390, "menos de 0,2 mm", F_MID, ACC, alpha=k)
    label(d, 220, "COLCHÃO DE VAPOR", VAPOR, seg(u, 0, 0.12))
    text_c(d, 320, "fino, mas segura a gota", F_MID, WHITE, alpha=seg(u, 0.15, 0.3))
    text_c(d, 480, "esquema, sem escala", F_SMALL, GRAY)
    return img

def s6(img, d, u, t):
    y, lift = zoom_scene(d, u, t)
    # calor tentando subir e sendo barrado
    for i in range(7):
        x = 200 + i * 115
        k = (t * 1.4 + i * 0.13) % 1.0
        yy = y - k * lift
        d.ellipse((x - 12, yy - 12, x + 12, yy + 12), fill=mix(HOT, 1 - 0.7 * k, (200, 215, 230)))
    label(d, 220, "ISOLANTE", ACC, seg(u, 0, 0.12))
    text_c(d, 320, "vapor conduz calor", F_MID, WHITE, alpha=seg(u, 0.15, 0.3))
    text_c(d, 390, "bem pior que a água", F_MID, HOT, alpha=seg(u, 0.35, 0.5))
    text_c(d, 480, "esquema, sem escala", F_SMALL, GRAY)
    return img

def s7(img, d, u, t):
    pan(d, t)
    for j, ph in enumerate((0.0, 2.1, 4.2)):
        cx = W / 2 + 330 * math.sin(t * (1.8 + 0.4 * j) + ph)
        cushion(d, cx, PAN_Y, 70, 12, t + j)
        drop(d, cx, PAN_Y, 90, 70, lift=12 + 5 * math.sin(t * 9 + j))
    label(d, 220, "QUASE SEM ATRITO", ACC, seg(u, 0, 0.12))
    text_c(d, 320, "as gotas deslizam", F_MID, WHITE, alpha=seg(u, 0.2, 0.35))
    text_c(d, 390, "para todo lado", F_MID, WATER_L, alpha=seg(u, 0.4, 0.55))
    return img

def s8(img, d, u, t):
    # página de livro antigo
    k = seg(u, 0.05, 0.3)
    d.rounded_rectangle((260, 560, 820, 1160), 20, fill=(220, 200, 160, int(255 * k)))
    for i in range(9):
        d.line((320, 660 + i * 50, 760 - (i % 3) * 60, 660 + i * 50), fill=(120, 100, 70, int(255 * k)), width=6)
    drop(d, 540, 1120, 120, 90, lift=10, a=int(255 * k))
    label(d, 220, "EFEITO LEIDENFROST", ACC, seg(u, 0, 0.12))
    text_c(d, 320, "descrito em 1756", F_MID, WHITE, alpha=seg(u, 0.3, 0.45))
    return img

def s9(img, d, u, t):
    pan(d, t, heat=0.8)
    drop(d, W / 2, PAN_Y, lift=14 + 5 * math.sin(t * 7))
    label(d, 220, "RESSALVA", RED, seg(u, 0, 0.12))
    text_c(d, 320, "não há um número único:", F_MID, WHITE, alpha=seg(u, 0.15, 0.3))
    text_c(d, 390, "muda com a superfície", F_MID, ACC, alpha=seg(u, 0.35, 0.5))
    text_c(d, 460, "e com a água", F_MID, ACC, alpha=seg(u, 0.45, 0.6))
    return img

def s10(img, d, u, t):
    pan(d, t)
    k = seg(u, 0.1, 0.3)
    cx, cy = W / 2, 760
    d.regular_polygon((cx, cy, 190), 3, rotation=0, fill=ACC + (int(255 * k),))
    text_c(d, cy - 40, "!", F_BIG, BG, alpha=k)
    label(d, 220, "CUIDADO", RED, seg(u, 0, 0.12))
    text_c(d, 320, "vapor e chapa queimam", F_MID, WHITE, alpha=seg(u, 0.2, 0.35))
    text_c(d, 390, "nunca teste com óleo", F_MID, RED, alpha=seg(u, 0.45, 0.6))
    return img

def s11(img, d, u, t):
    pan(d, t)
    cx = W / 2 + 200 * math.sin(t * 1.6)
    cushion(d, cx, PAN_Y, 100, 14, t)
    drop(d, cx, PAN_Y, 130, 95, lift=14 + 5 * math.sin(t * 8))
    text_c(d, 440, "SEGUE PRA MAIS", F_LBL, WHITE, alpha=seg(u, 0, 0.2))
    text_c(d, 530, "FÍSICA QUE PARECE", F_LBL, WHITE, alpha=seg(u, 0.05, 0.25))
    text_c(d, 620, "TRUQUE", F_LBL, ACC, alpha=seg(u, 0.1, 0.3))
    text_c(d, 760, "@parecefakeereal", F_LOGO, ACC, alpha=seg(u, 0.25, 0.45))
    return img

CHUNKS = [
 ("Numa frigideira bem quente, a gota de água não ferve na hora: ela flutua.", "Numa frigideira bem quente, a gota de água não ferve na hora: ela flutua.", s0),
 ("E, numa certa faixa, quanto mais quente a chapa, mais a gota dura.", "E, numa certa faixa, quanto mais quente a chapa, mais ela dura.", s1),
 ("Pouco acima de 100 °C, a gota encosta, chia e some em segundos.", "Pouco acima de cem graus, a gota encosta, chia e some em segundos.", s2),
 ("Perto de 200 °C, vira uma bolinha que dança por mais de um minuto.", "Perto de duzentos graus, vira uma bolinha que dança por mais de um minuto.", s3),
 ("O segredo: a parte de baixo da gota vira vapor na hora.", "O segredo: a parte de baixo da gota vira vapor na hora.", s4),
 ("Esse vapor vira um colchão finíssimo sob a gota.", "Esse vapor vira um colchão finíssimo sob a gota.", s5),
 ("E vapor conduz calor bem pior que água: isola a gota.", "E vapor conduz calor bem pior que água: isola a gota.", s6),
 ("Quase sem atrito, as gotas deslizam para todo lado.", "Quase sem atrito, as gotas deslizam para todo lado.", s7),
 ("É o efeito Leidenfrost, descrito em 1756.", "É o efeito Láidenfrost, descrito em mil setecentos e cinquenta e seis.", s8),
 ("A temperatura exata muda com a superfície e com a água.", "A temperatura exata muda com a superfície e com a água.", s9),
 ("Cuidado: chapa e vapor queimam. Nunca teste com óleo.", "Cuidado: chapa e vapor queimam. Nunca teste com óleo.", s10),
 ("Segue pra mais física que parece truque.", "Segue pra mais física que parece truque.", s11),
]

if __name__ == "__main__":
    wd = os.path.join(os.environ.get("WORK_DIR", "/tmp/reelwork"), "reel12")
    note = "Animação autoral, sem escala · locução sintética"
    kw = dict(voice="M4", speed=float(os.environ.get("SPEED", "1.25")), bg_fn=kitchen_bg)
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        render(CHUNKS, wd, None, note, previews=[0.01, 0.08, 0.16, 0.24, 0.32, 0.4, 0.48, 0.56, 0.64, 0.74, 0.86, 0.97], **kw)
    else:
        render(CHUNKS, wd, sys.argv[1], note, **kw)
