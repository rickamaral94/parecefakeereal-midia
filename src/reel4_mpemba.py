import sys, math
from engine import *

HOT = (240, 96, 64); COLD = (90, 170, 255); ICE = (200, 230, 255)

def tray(d, cx, cy, col, frozen=0.0, steam=0.0, t=0.0, w=300):
    """Forminha vista de lado com líquido; frozen 0→1 vira gelo; steam mostra vapor."""
    d.rounded_rectangle((cx - w / 2, cy - 70, cx + w / 2, cy + 70), 22, outline=(200, 205, 215, 255), width=6)
    c = tuple(int(lerp(a, b, frozen)) for a, b in zip(col, ICE))
    d.rounded_rectangle((cx - w / 2 + 12, cy - 30, cx + w / 2 - 12, cy + 58), 14, fill=c + (255,))
    if frozen > 0.5:
        for k in range(3):
            x = cx - w / 2 + 50 + k * (w - 100) / 2
            d.line((x - 18, cy - 10, x + 18, cy + 30), fill=(255, 255, 255, int(200 * frozen)), width=4)
    if steam > 0:
        for k in range(3):
            x = cx - 70 + k * 70
            pts = [(x + 14 * math.sin(t * 3 + j * 0.6 + k), cy - 60 - j * 22) for j in range(8)]
            d.line(pts, fill=(255, 255, 255, int(120 * steam)), width=6)

def thermo(d, x, y, level, col, k=1.0):
    a = int(255 * k)
    d.rounded_rectangle((x - 18, y - 200, x + 18, y + 20), 18, outline=WHITE + (a,), width=4)
    d.ellipse((x - 32, y, x + 32, y + 64), fill=col + (a,))
    d.rectangle((x - 9, y - 190 * level + 10, x + 9, y + 20), fill=col + (a,))

def freezer(d):
    d.rounded_rectangle((110, 560, W - 110, 1130), 36, outline=(150, 160, 175, 255), width=8)
    d.rounded_rectangle((130, 580, W - 130, 1110), 28, fill=(24, 30, 44, 255))
    for k in range(6):
        d.line((150, 620 + k * 90, W - 150, 620 + k * 90), fill=(60, 72, 92, 160), width=2)

def s0(img, d, u, t):
    freezer(d)
    tray(d, 330, 860, HOT, frozen=seg(u, 0.45, 0.9), steam=1 - seg(u, 0.3, 0.6), t=t, w=340)
    tray(d, 750, 860, COLD, frozen=0.0, t=t, w=340)
    d.text((750 - d.textlength("FRIA", font=F_MID) / 2, 676), "FRIA", font=F_MID, fill=COLD + (255,))
    d.text((330 - d.textlength("QUENTE", font=F_MID) / 2, 676), "QUENTE", font=F_MID, fill=HOT + (255,))
    text_c(d, 200, "ELE JUROU:", F_HOOK, WHITE, maxw=1040)
    text_c(d, 300, "A ÁGUA QUENTE", F_HOOK, ACC, maxw=1040)
    text_c(d, 400, "CONGELOU ANTES", F_HOOK, ACC, maxw=1040)
    return img

def s1(img, d, u, t):
    # escola + caderno, Tanzânia 1963
    k = seg(u, 0.0, 0.2)
    d.rounded_rectangle((200, 620, W - 200, 1080), 30, fill=(250, 244, 226, int(255 * k)))
    for j in range(7):
        d.line((240, 700 + j * 52, W - 240, 700 + j * 52), fill=(150, 180, 220, int(200 * k)), width=3)
    d.line((300, 640, 300, 1060), fill=(230, 110, 110, int(200 * k)), width=3)
    # tigela de mistura quente
    kk = seg(u, 0.35, 0.6)
    d.chord((W / 2 - 150, 780, W / 2 + 150, 1000), 0, 180, fill=HOT + (int(255 * kk),))
    for j in range(3):
        x = W / 2 - 60 + j * 60
        pts = [(x + 12 * math.sin(t * 3 + i * 0.7 + j), 870 - i * 20) for i in range(6)]
        d.line(pts, fill=(120, 120, 130, int(200 * kk)), width=5)
    label(d, 300, "TANZÂNIA · 1963", ACC, seg(u, 0, 0.15))
    text_c(d, 380, "Erasto Mpemba, estudante", F_MID, WHITE, alpha=seg(u, 0.15, 0.3))
    return img

def s2(img, d, u, t):
    freezer(d)
    tray(d, 330, 860, HOT, frozen=seg(u, 0.3, 0.75), t=t, w=340)
    tray(d, 750, 860, COLD, frozen=0.15 * seg(u, 0.3, 0.75), t=t, w=340)
    d.text((330 - d.textlength("dele", font=F_MID) / 2, 676), "dele", font=F_MID, fill=HOT + (255,))
    d.text((750 - d.textlength("do colega", font=F_MID) / 2, 676), "do colega", font=F_MID, fill=COLD + (255,))
    label(d, 300, "O RELATO", ACC, seg(u, 0, 0.15))
    text_c(d, 380, "a quente congelou antes", F_MID, WHITE, alpha=seg(u, 0.6, 0.75))
    return img

def s3(img, d, u, t):
    k = seg(u, 0.05, 0.3)
    y = lerp(760, 680, k)
    d.rounded_rectangle((220, y, W - 220, y + 420), 22, fill=(236, 238, 242, int(255 * k)))
    d.rectangle((220, y, W - 220, y + 80), fill=(60, 90, 150, int(255 * k)))
    tw = d.textlength("Physics Education", font=F_SMALL)
    d.text(((W - tw) / 2, y + 22), "Physics Education", font=F_SMALL, fill=(255, 255, 255, int(255 * k)))
    d.text(((W - d.textlength("1969", font=F_LBL)) / 2, y + 110), "1969", font=F_LBL, fill=(30, 34, 44, int(255 * k)))
    for j in range(4):
        d.rounded_rectangle((280, y + 220 + j * 40, W - 280 - (j % 2) * 120, y + 236 + j * 40), 8, fill=(170, 175, 185, int(255 * k)))
    label(d, 300, "EFEITO MPEMBA", ACC, seg(u, 0.5, 0.65))
    text_c(d, 380, "relato com o professor Denis Osborne", F_MID, WHITE, alpha=seg(u, 0.2, 0.35))
    return img

def s4(img, d, u, t):
    items = [("evaporação", HOT), ("impurezas", GREEN), ("super-resfriamento", COLD)]
    for j, (txt, col) in enumerate(items):
        k = seg(u, 0.1 + 0.17 * j, 0.25 + 0.17 * j)
        y = 600 + j * 135
        d.rounded_rectangle((150, y, W - 150, y + 105), 26, fill=col + (int(60 * k),), outline=col + (int(255 * k),), width=4)
        text_c(d, y + 28, txt, F_MID, WHITE, alpha=k)
    label(d, 300, "DIFÍCIL DE REPETIR", RED, seg(u, 0, 0.12))
    return img

def s5(img, d, u, t):
    k = seg(u, 0.05, 0.25)
    d.rounded_rectangle((180, 600, W - 180, 1020), 26, fill=(236, 238, 242, int(255 * k)))
    d.text(((W - d.textlength("Scientific Reports · 2016", font=F_SMALL)) / 2, 630), "Scientific Reports · 2016", font=F_SMALL, fill=(60, 66, 80, int(255 * k)))
    for j in range(3):
        d.rounded_rectangle((240, 700 + j * 44, W - 240 - j * 90, 718 + j * 44), 8, fill=(170, 175, 185, int(255 * k)))
    k2 = seg(u, 0.4, 0.6)
    s = lerp(1.25, 1.0, k2)
    cx, cy = W / 2, 910
    d.rounded_rectangle((cx - 300 * s, cy - 55 * s, cx + 300 * s, cy + 55 * s), int(16 * s), outline=RED + (int(255 * k2),), width=8)
    f = F("Black", int(56 * s))
    txt = "NÃO CONFIRMADO"
    d.text((cx - d.textlength(txt, font=f) / 2, cy - 36 * s), txt, font=f, fill=RED + (int(255 * k2),))
    label(d, 300, "O CONTRA", RED, seg(u, 0, 0.12))
    text_c(d, 380, "na água, em testes controlados", F_MID, WHITE, alpha=seg(u, 0.6, 0.75))
    return img

def landscape(d, k):
    pts = []
    for i in range(61):
        x = 120 + i * (W - 240) / 60
        z = (i - 30) / 30
        y = 780 - 260 * math.exp(-((z + 0.45) / 0.22) ** 2) * 0 + 240 * (z * z) - 140 * math.exp(-((z - 0.5) / 0.18) ** 2) + 120 * math.exp(-((z + 0.1) / 0.15) ** 2)
        pts.append((x, y))
    d.line(pts, fill=BLUE + (int(255 * k),), width=7)
    return pts

def s6(img, d, u, t):
    k = seg(u, 0.0, 0.15)
    pts = landscape(d, k)
    target = pts[45]
    # bola quente: atalho direto; bola morna: fica presa na barreira
    kh = seg(u, 0.3, 0.6)
    hx = lerp(pts[58][0], target[0], kh); hy = lerp(pts[58][1], target[1], kh) - 26
    wx = lerp(pts[8][0], pts[24][0], seg(u, 0.3, 0.9)); wy = lerp(pts[8][1], pts[24][1], seg(u, 0.3, 0.9)) - 26
    d.ellipse((hx - 24, hy - 24, hx + 24, hy + 24), fill=HOT + (int(255 * k),))
    d.ellipse((wx - 24, wy - 24, wx + 24, wy + 24), fill=(255, 170, 120, int(255 * k)))
    d.text((pts[58][0] - 110, pts[58][1] - 120), "mais quente", font=F_SMALL, fill=HOT + (int(255 * k),))
    d.text((pts[6][0] - 10, pts[6][1] - 120), "menos quente", font=F_SMALL, fill=(255, 170, 120, int(255 * k)))
    text_c(d, 1080, "esfriou mais rápido", F_MID, GREEN, alpha=seg(u, 0.6, 0.75))
    label(d, 300, "NATURE · 2020", ACC, seg(u, 0, 0.12))
    text_c(d, 380, "microesferas de vidro, não água", F_MID, WHITE, alpha=seg(u, 0.12, 0.25))
    return img

def s7(img, d, u, t):
    k1 = seg(u, 0.0, 0.2); k2 = seg(u, 0.3, 0.5)
    d.rounded_rectangle((140, 560, W - 140, 720), 26, fill=(20, 52, 36, int(230 * k1)))
    text_c(d, 605, "Em alguns sistemas: ✓", F_LBL, GREEN, alpha=k1)
    d.rounded_rectangle((140, 780, W - 140, 940), 26, fill=(60, 50, 20, int(230 * k2)))
    text_c(d, 825, "Na água: em aberto", F_LBL, ACC, alpha=k2)
    label(d, 300, "VEREDITO", ACC, seg(u, 0, 0.12))
    return img

def s8(img, d, u, t):
    tray(d, 330, 520, HOT, t=t, w=260); tray(d, 750, 520, COLD, t=t, w=260)
    text_c(d, 660, "QUAL CONGELA ANTES?", F_LBL, WHITE, alpha=seg(u, 0, 0.2))
    text_c(d, 760, "@parecefakeereal", F_LOGO, ACC, alpha=seg(u, 0.1, 0.35))
    text_c(d, 860, "Parece fake. É real?", F_MID, WHITE, alpha=seg(u, 0.25, 0.5))
    return img

CHUNKS = [
 ("Um estudante jurou: a água quente congelou primeiro.", "Um estudante jurou: a água quente congelou primeiro.", s0),
 ("Tanzânia, 1963: Erasto Mpemba pôs uma mistura de sorvete ainda quente no congelador.", "Tanzânia, mil novecentos e sessenta e três. Erasto Mpemba pôs uma mistura de sorvete ainda quente no congelador.", s1),
 ("Segundo ele, a mistura quente congelou antes da de um colega.", "Segundo ele, a mistura quente congelou antes da de um colega.", s2),
 ("Em 1969, publicou o relato com o professor Denis Osborne. Nascia o efeito Mpemba.", "Em mil novecentos e sessenta e nove, publicou o relato com o professor Denis Osborne. Nascia o efeito Mpemba.", s3),
 ("Mas é difícil repetir: evaporação, impurezas e super-resfriamento mudam o resultado.", "Mas é difícil repetir. Evaporação, impurezas e super-resfriamento mudam o resultado.", s4),
 ("Em 2016, um estudo na Scientific Reports não achou evidência convincente do efeito na água.", "Em dois mil e dezesseis, um estudo não achou evidência convincente do efeito na água.", s5),
 ("Em 2020, na Nature: com microesferas de vidro, as mais quentes esfriaram mais rápido que as menos quentes.", "Já em dois mil e vinte, na revista Nature, microesferas de vidro mais quentes esfriaram mais rápido que as menos quentes.", s6),
 ("Isso não prova que acontece no seu congelador. Na água, a briga continua.", "Isso não prova que acontece no seu congelador. Na água, a briga continua.", s7),
 ("E você? Comenta: a quente congela antes?", "E você? Comenta: a quente congela antes?", s8),
]

if __name__ == "__main__":
    import os; wd = os.path.join(os.environ.get("WORK_DIR", "/tmp/reelwork"), "reel4")
    note = "Animação autoral, sem escala · locução sintética"
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        render(CHUNKS, wd, None, note, voice="M4", speed=1.24, previews=[0.03, 0.14, 0.27, 0.38, 0.5, 0.6, 0.72, 0.85, 0.97])
    else:
        render(CHUNKS, wd, sys.argv[1], note, voice="M4", speed=1.24)
