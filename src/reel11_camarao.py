import sys, math, random
from engine import *

SHRIMP = (235, 120, 90); SHRIMP_D = (190, 80, 62); CLAW = (245, 150, 110)
WATER = (120, 200, 255); VAPOR = (215, 240, 255); SHOCK = (180, 230, 255); FLASH = (255, 245, 200)

def sea_bg(d, t):
    for y in range(0, H, 40):
        k = y / H
        d.rectangle((0, y, W, y + 40), fill=(int(lerp(10, 4, k)), int(lerp(42, 14, k)), int(lerp(70, 30, k)), 255))
    r = random.Random(5)
    for i in range(55):
        x = (r.random() * W + 18 * math.sin(t * 0.8 + i)) % W
        y = (r.random() * H - t * (25 + 35 * r.random())) % H
        s = 2 + 4 * r.random()
        d.ellipse((x, y, x + s, y + s), outline=(140, 200, 240, 110), width=1)
    d.rectangle((0, 1240, W, H), fill=(26, 30, 34, 255))

def shrimp(d, cx, cy, s=1.0, open_k=1.0, a=255):
    """Camarão visto de lado, cabeça à direita, garra grande à frente."""
    # cauda e segmentos do abdômen (da esquerda para a direita)
    d.polygon([(cx - 330 * s, cy - 20 * s), (cx - 400 * s, cy - 70 * s), (cx - 400 * s, cy + 50 * s)], fill=SHRIMP_D + (a,))
    for i in range(5):
        x0 = cx - 320 * s + i * 62 * s
        h = (48 + i * 8) * s
        d.ellipse((x0, cy - h, x0 + 80 * s, cy + h * 0.8), fill=(SHRIMP if i % 2 == 0 else SHRIMP_D) + (a,))
    # cefalotórax
    d.ellipse((cx - 30 * s, cy - 85 * s, cx + 170 * s, cy + 70 * s), fill=SHRIMP + (a,))
    # olho e antenas
    d.ellipse((cx + 130 * s, cy - 70 * s, cx + 160 * s, cy - 40 * s), fill=(20, 20, 24, a))
    d.line((cx + 160 * s, cy - 60 * s, cx + 330 * s, cy - 190 * s), fill=SHRIMP_D + (a,), width=max(2, int(4 * s)))
    d.line((cx + 160 * s, cy - 50 * s, cx + 360 * s, cy - 120 * s), fill=SHRIMP_D + (a,), width=max(2, int(4 * s)))
    # patas
    for i in range(4):
        x = cx - 10 * s + i * 40 * s
        d.line((x, cy + 50 * s, x - 20 * s, cy + 120 * s), fill=SHRIMP_D + (a,), width=max(2, int(5 * s)))
    # garra grande (gatilho): base + dedo fixo + dedo móvel (dáctilo)
    bx, by = cx + 150 * s, cy + 40 * s
    d.ellipse((bx - 40 * s, by - 60 * s, bx + 200 * s, by + 60 * s), fill=CLAW + (a,))
    tip = (bx + 330 * s, by + 10 * s)
    d.polygon([(bx + 180 * s, by + 5 * s), tip, (bx + 180 * s, by + 50 * s)], fill=CLAW + (a,))
    ang = math.radians(-50 * open_k)
    L = 160 * s
    px, py = bx + 185 * s, by - 10 * s
    ex, ey = px + L * math.cos(ang), py + L * math.sin(ang)
    d.line((px, py, ex, ey), fill=SHRIMP_D + (a,), width=max(3, int(26 * s)))
    return tip

def bubble(d, x, y, r, a=255):
    if r <= 1: return
    d.ellipse((x - r, y - r, x + r, y + r), fill=VAPOR + (int(a * 0.35),), outline=VAPOR + (a,), width=4)
    d.ellipse((x - r * 0.5, y - r * 0.6, x - r * 0.2, y - r * 0.3), fill=(255, 255, 255, int(a * 0.8)))

def rings(d, x, y, k, n=3, a=255):
    for j in range(n):
        kk = (k + j / n) % 1.0
        rr = 30 + kk * 520
        d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=SHOCK + (int(a * (1 - kk)),), width=6)

def snap_cycle(t, period=1.6):
    """0..1 dentro do ciclo: abre, fecha rápido, jato, bolha cresce, colapsa."""
    return (t % period) / period

def s0(img, d, u, t):
    c = snap_cycle(t)
    open_k = 1.0 if c < 0.3 else max(0.0, 1 - (c - 0.3) / 0.04)
    tip = shrimp(d, 440, 960, 1.0, open_k)
    if c > 0.34:
        k = (c - 0.34) / 0.66
        rings(d, tip[0] + 60, tip[1], k, n=2, a=int(255 * (1 - k)))
    text_c(d, 210, "UM CAMARÃO", F_HOOK, WHITE, maxw=1040)
    text_c(d, 310, "DE POUCOS cm", F_HOOK, ACC, maxw=1040)
    text_c(d, 410, "E UM ESTALO GIGANTE", F_HOOK, SHOCK, maxw=1040, alpha=seg(u, 0.3, 0.45))
    return img

def s1(img, d, u, t):
    tip = shrimp(d, 440, 960, 1.0, 1.0)
    k = seg(u, 0.3, 0.6)
    d.ellipse((tip[0] - 250, tip[1] - 170, tip[0] + 40, tip[1] + 120), outline=ACC + (int(255 * k),), width=6)
    label(d, 220, "CAMARÃO-PISTOLA", ACC, seg(u, 0, 0.12))
    text_c(d, 320, "uma garra enorme = gatilho", F_MID, WHITE, alpha=seg(u, 0.2, 0.35))
    return img

def s2(img, d, u, t):
    open_k = 1.0 - seg(u, 0.2, 0.3) + seg(u, 0.6, 0.7)
    shrimp(d, 440, 960, 1.0, open_k)
    label(d, 220, "A IDEIA ANTIGA", GRAY, seg(u, 0, 0.12))
    text_c(d, 320, "as partes da garra batendo", F_MID, WHITE, alpha=seg(u, 0.15, 0.3))
    k = seg(u, 0.55, 0.7)
    if k > 0:
        cx, cy = 820, 640
        d.line((cx - 70, cy - 70, cx + 70, cy + 70), fill=RED + (int(255 * k),), width=16)
        d.line((cx + 70, cy - 70, cx - 70, cy + 70), fill=RED + (int(255 * k),), width=16)
    return img

def s3(img, d, u, t):
    # moldura de câmera e fotogramas
    cx, cy = W / 2, 860
    d.rounded_rectangle((cx - 300, cy - 180, cx + 300, cy + 180), 40, outline=WHITE + (255,), width=8)
    d.ellipse((cx - 120, cy - 120, cx + 120, cy + 120), outline=BLUE + (255,), width=10)
    d.ellipse((cx - 60, cy - 60, cx + 60, cy + 60), fill=BLUE + (160,))
    k = seg(u, 0.2, 1)
    for i in range(6):
        x = 120 + ((i * 160 + k * 600) % 960)
        d.rectangle((x, 1110, x + 120, 1190), outline=GRAY + (255,), width=4)
    label(d, 220, "ANO 2000", ACC, seg(u, 0, 0.12))
    text_c(d, 320, "câmera ultrarrápida", F_MID, WHITE, alpha=seg(u, 0.2, 0.35))
    return img

def s4(img, d, u, t):
    open_k = 1.0 - seg(u, 0.15, 0.22)
    tip = shrimp(d, 380, 960, 0.9, open_k)
    k = seg(u, 0.22, 0.8)
    if k > 0:
        x1 = tip[0] + 20 + k * 520
        for j in range(5):
            yy = tip[1] - 24 + j * 12
            d.line((tip[0] + 20, yy, x1 - j * 30, yy), fill=WATER + (220,), width=6)
    label(d, 220, "A GARRA FECHA", ACC, seg(u, 0, 0.12))
    text_c(d, 320, "e dispara um jato de água", F_MID, WATER, alpha=seg(u, 0.25, 0.4))
    return img

def s5(img, d, u, t):
    tip = shrimp(d, 320, 1000, 0.75, 0.0)
    x = tip[0] + 230
    for j in range(4):
        yy = tip[1] - 18 + j * 12
        d.line((tip[0] + 10, yy, x - 60, yy), fill=WATER + (160,), width=5)
    r = 30 + 80 * seg(u, 0.15, 0.7)
    bubble(d, x, tip[1], r)
    label(d, 220, "CAVITAÇÃO", VAPOR, seg(u, 0, 0.12))
    text_c(d, 320, "pressão despenca:", F_MID, WHITE, alpha=seg(u, 0.15, 0.3))
    text_c(d, 390, "nasce uma bolha de vapor", F_MID, VAPOR, alpha=seg(u, 0.35, 0.5))
    text_c(d, 1160, "esquema, sem escala", F_SMALL, GRAY)
    return img

def s6(img, d, u, t):
    tip = shrimp(d, 320, 1000, 0.75, 0.0)
    x, y = tip[0] + 230, tip[1]
    r = 110 * (1 - seg(u, 0.1, 0.35))
    bubble(d, x, y, r)
    if u > 0.35:
        rings(d, x, y, ((u - 0.35) * 2.2) % 1.0, n=3)
    label(d, 220, "O ESTALO É AQUI", ACC, seg(u, 0, 0.12))
    text_c(d, 320, "no colapso da bolha", F_MID, WHITE, alpha=seg(u, 0.25, 0.4))
    text_c(d, 390, "não no fechar da garra", F_MID, GRAY, alpha=seg(u, 0.5, 0.65))
    return img

def s7(img, d, u, t):
    x, y = 340, 900
    rings(d, x, y, (t * 0.7) % 1.0, n=3)
    # presa pequena (peixinho) que fica atordoada
    k = seg(u, 0.3, 0.6)
    px, py = 820, 900 + 40 * k
    d.ellipse((px - 70, py - 30, px + 70, py + 30), fill=(170, 200, 120, 255))
    d.polygon([(px + 60, py), (px + 120, py - 40), (px + 120, py + 40)], fill=(140, 170, 100, 255))
    if k > 0.5:
        for j in range(3):
            sx = px - 40 + j * 40
            yy = py - 80 - 10 * math.sin(t * 6 + j)
            d.ellipse((sx - 9, yy - 9, sx + 9, yy + 9), fill=ACC + (255,))
    label(d, 220, "ONDA DE CHOQUE", SHOCK, seg(u, 0, 0.12))
    text_c(d, 320, "atordoa ou mata presas pequenas", F_MID, WHITE, alpha=seg(u, 0.2, 0.35))
    return img

def s8(img, d, u, t):
    x, y = W / 2, 860
    k = seg(u, 0.15, 0.3) * (1 - seg(u, 0.4, 0.6))
    img = glow(img, x, y, 160, k, FLASH)
    d = ImageDraw.Draw(img)
    bubble(d, x, y, 90 * (1 - seg(u, 0.05, 0.2)))
    label(d, 220, "UM FLASH DE LUZ", FLASH, seg(u, 0, 0.12))
    text_c(d, 320, "fraco demais para o olho humano", F_MID, WHITE, alpha=seg(u, 0.35, 0.5))
    text_c(d, 1160, "brilho exagerado na animação", F_SMALL, GRAY)
    return img

def s9(img, d, u, t):
    r = random.Random(9)
    for i in range(14):
        x, y = 100 + r.random() * 880, 700 + r.random() * 500
        kk = (t * (0.6 + r.random()) + r.random()) % 1.0
        rr = 10 + kk * 90
        d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=SHOCK + (int(200 * (1 - kk)),), width=3)
    pts = [(120 + i * 14, 560 + 40 * math.sin(i * 1.7 + t * 9) * random.Random(i).random()) for i in range(61)]
    d.line(pts, fill=WATER + (255,), width=4)
    label(d, 220, "EM COLÔNIAS", ACC, seg(u, 0, 0.12))
    text_c(d, 320, "um chiado constante", F_MID, WHITE, alpha=seg(u, 0.2, 0.35))
    text_c(d, 390, "que atrapalha sonares", F_MID, GRAY, alpha=seg(u, 0.45, 0.6))
    return img

def s10(img, d, u, t):
    text_c(d, 560, "~200 dB", F_BIG, SHOCK, alpha=seg(u, 0.1, 0.25), maxw=1040)
    text_c(d, 720, "medidos na água", F_MID, WHITE, alpha=seg(u, 0.2, 0.35))
    label(d, 220, "RESSALVA", RED, seg(u, 0, 0.12))
    text_c(d, 870, "dB na água ≠ dB no ar:", F_MID, ACC, alpha=seg(u, 0.45, 0.6))
    text_c(d, 940, "a referência é outra", F_MID, GRAY, alpha=seg(u, 0.55, 0.7))
    return img

def s11(img, d, u, t):
    shrimp(d, 440, 1060, 0.7, 0.5 + 0.5 * math.sin(t * 3))
    text_c(d, 440, "SALVA PRA LEMBRAR", F_LBL, WHITE, alpha=seg(u, 0, 0.2))
    text_c(d, 530, "DO CAMARÃO QUE", F_LBL, WHITE, alpha=seg(u, 0.05, 0.25))
    text_c(d, 620, "ATIRA BOLHAS", F_LBL, ACC, alpha=seg(u, 0.1, 0.3))
    text_c(d, 760, "@parecefakeereal", F_LOGO, ACC, alpha=seg(u, 0.25, 0.45))
    return img

CHUNKS = [
 ("Como um camarão de poucos centímetros faz um dos sons mais altos do mar?", "Como um camarão de poucos centímetros faz um dos sons mais altos do mar?", s0),
 ("É o camarão-pistola: uma garra enorme funciona como gatilho.", "É o camarão pistola: uma garra enorme funciona como gatilho.", s1),
 ("Por muito tempo, achou-se que o estalo vinha da garra batendo.", "Por muito tempo, achou-se que o estalo vinha da garra batendo.", s2),
 ("Em 2000, câmeras ultrarrápidas mostraram outra coisa.", "Em dois mil, câmeras ultrarrápidas mostraram outra coisa.", s3),
 ("A garra fecha tão rápido que dispara um jato de água.", "A garra fecha tão rápido que dispara um jato de água.", s4),
 ("No jato, a pressão cai tanto que nasce uma bolha de vapor: é a cavitação.", "No jato, a pressão cai tanto que nasce uma bolha de vapor: é a cavitação.", s5),
 ("O estalo vem do colapso dessa bolha, não do fechar da garra.", "O estalo vem do colapso dessa bolha, não do fechar da garra.", s6),
 ("O colapso gera uma onda de choque que atordoa ou mata presas pequenas.", "O colapso gera uma onda de choque, que atordoa ou mata presas pequenas.", s7),
 ("E solta um flash de luz, fraco demais para o olho humano.", "E solta um flash de luz, fraco demais para o olho humano.", s8),
 ("Em colônias, os estalos viram um chiado constante que atrapalha sonares.", "Em colônias, os estalos viram um chiado constante, que atrapalha sonares.", s9),
 ("Na água, o estalo chega a cerca de 200 dB — escala diferente da do ar.", "Na água, o estalo chega a cerca de duzentos decibéis, numa escala diferente da do ar.", s10),
 ("Salva pra lembrar do camarão que atira bolhas.", "Salva pra lembrar do camarão que atira bolhas.", s11),
]

if __name__ == "__main__":
    wd = os.path.join(os.environ.get("WORK_DIR", "/tmp/reelwork"), "reel11")
    note = "Animação autoral, sem escala · locução sintética"
    kw = dict(voice="M3", speed=float(os.environ.get("SPEED", "1.25")), bg_fn=sea_bg)
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        render(CHUNKS, wd, None, note, previews=[0.01, 0.08, 0.16, 0.24, 0.32, 0.4, 0.48, 0.56, 0.64, 0.74, 0.86, 0.97], **kw)
    else:
        render(CHUNKS, wd, sys.argv[1], note, **kw)
