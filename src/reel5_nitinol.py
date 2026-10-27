import sys, math
from engine import *

WIRE = (190, 198, 212); NI = (120, 200, 170); TI = (170, 150, 230); HOT = (255, 120, 60)

def wire(d, x0, x1, y, crumple, t=0.0, col=WIRE, width=14, alpha=255, seed=3):
    """Fio que vai de amassado (crumple=1) a reto (crumple=0)."""
    pts = []
    n = 80
    for i in range(n + 1):
        z = i / n
        x = lerp(x0, x1, z)
        off = (90 * math.sin(z * 19 + seed) + 60 * math.sin(z * 41 + 2 * seed) + 40 * math.sin(z * 7)) * crumple
        xo = 40 * math.sin(z * 23 + seed) * crumple
        pts.append((x + xo, y + off))
    d.line(pts, fill=col + (alpha,), width=width, joint="curve")

def flame(d, cx, cy, k, t):
    if k <= 0.01: return
    a = int(255 * k)
    fl = 1 + 0.08 * math.sin(t * 20)
    d.ellipse((cx - 36, cy - 110 * fl, cx + 36, cy + 10), fill=(255, 150, 50, a))
    d.ellipse((cx - 18, cy - 60 * fl, cx + 18, cy + 6), fill=(255, 235, 140, a))
    d.rounded_rectangle((cx - 40, cy + 10, cx + 40, cy + 120), 12, fill=(120, 126, 140, a))

def s0(img, d, u, t):
    k = seg(u, 0.35, 0.85)
    img = glow(img, W / 2, 900, 220, 0.6 * seg(u, 0.25, 0.4) * (1 - seg(u, 0.85, 1.0)), HOT)
    d = ImageDraw.Draw(img)
    wire(d, 200, W - 200, 820, 1 - k, t)
    flame(d, W / 2, 1010, seg(u, 0.2, 0.35) * (1 - seg(u, 0.9, 1.0)), t)
    text_c(d, 200, "POR QUE ESSE FIO", F_HOOK, WHITE, maxw=1040)
    text_c(d, 300, "VOLTA A SER RETO", F_HOOK, ACC, maxw=1040)
    text_c(d, 400, "SÓ COM CALOR?", F_HOOK, ACC, maxw=1040)
    return img

def atoms(d, k, t, cx=W / 2, cy=840, n=6, gap=90, shear=0.0, alpha=1.0):
    for r in range(n):
        for c in range(n):
            x = cx + (c - (n - 1) / 2) * gap + shear * (r - (n - 1) / 2) * gap * (1 if (r // 2) % 2 == 0 else -1) * 0
            y = cy + (r - (n - 1) / 2) * gap
            col = NI if (r + c) % 2 == 0 else TI
            j = seg(k, (r * n + c) / (n * n) * 0.6, (r * n + c) / (n * n) * 0.6 + 0.3)
            rr = 34 * j
            d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=col + (int(255 * j * alpha),))

def s1(img, d, u, t):
    atoms(d, seg(u, 0.05, 0.8), t)
    label(d, 300, "NITINOL", ACC, seg(u, 0, 0.15))
    text_c(d, 1150, "níquel", F_MID, NI, alpha=seg(u, 0.4, 0.55), x=W / 2 - 160)
    text_c(d, 1150, "titânio", F_MID, TI, alpha=seg(u, 0.5, 0.65), x=W / 2 + 160)
    text_c(d, 380, "liga de níquel e titânio, ~meio a meio", F_MID, WHITE, alpha=seg(u, 0.2, 0.35))
    return img

def s2(img, d, u, t):
    parts = [("Ni", NI), ("Ti", TI), ("NOL", ACC)]
    for j, (txt, col) in enumerate(parts):
        k = seg(u, 0.1 + 0.15 * j, 0.25 + 0.15 * j)
        x = W / 2 + (j - 1) * 290
        d.rounded_rectangle((x - 130, 640, x + 130, 840), 30, fill=col + (int(70 * k),), outline=col + (int(255 * k),), width=5)
        tw = d.textlength(txt, font=F_BIG)
        d.text((x - tw / 2, 670), txt, font=F_BIG, fill=WHITE + (int(255 * k),))
    text_c(d, 900, "Naval Ordnance Laboratory", F_MID, ACC, alpha=seg(u, 0.5, 0.65))
    text_c(d, 970, "laboratório da Marinha dos EUA", F_MID, WHITE, alpha=seg(u, 0.55, 0.7))
    label(d, 300, "EUA · 1961", ACC, seg(u, 0, 0.15))
    return img

def s3(img, d, u, t):
    k = seg(u, 0.35, 0.85)
    fk = seg(u, 0.2, 0.35)
    img = glow(img, W / 2, 900, 200, 0.5 * fk, HOT)
    d = ImageDraw.Draw(img)
    # tira em sanfona que se estica
    x0, x1 = lerp(380, 180, k), lerp(W - 380, W - 180, k)
    pts = []
    for i in range(41):
        z = i / 40
        pts.append((lerp(x0, x1, z), 820 + (1 - k) * 70 * (1 if i % 2 else -1)))
    d.line(pts, fill=WIRE + (255,), width=26, joint="curve")
    flame(d, W / 2, 1000, fk, t)
    label(d, 300, "O RELATO", ACC, seg(u, 0, 0.12))
    text_c(d, 380, "isqueiro de cachimbo + tira amassada", F_MID, WHITE, alpha=seg(u, 0.1, 0.25))
    return img

def lattice(d, cx, cy, mode, k, gap=80, n=5):
    """mode 'mart': colunas inclinadas alternadas (maclas); 'aus': grade quadrada."""
    for r in range(n):
        for c in range(n):
            tilt = (1 if (r // 1) % 2 == 0 else -1) * 0.45 if mode == "mart" else 0
            x = cx + (c - (n - 1) / 2) * gap + tilt * gap * 0.5
            y = cy + (r - (n - 1) / 2) * gap
            col = NI if (r + c) % 2 == 0 else TI
            d.ellipse((x - 24, y - 24, x + 24, y + 24), fill=col + (int(255 * k),))

def s4(img, d, u, t):
    k = seg(u, 0.0, 0.2)
    # rede em maclas: fileiras deslocadas em zigue-zague, sem perder vizinhos
    n, gap = 6, 95
    sh = seg(u, 0.35, 0.7)
    for r in range(n):
        for c in range(n):
            sgn = 1 if r % 2 == 0 else -1
            x = W / 2 + (c - (n - 1) / 2) * gap + sgn * sh * 28
            y = 860 + (r - (n - 1) / 2) * gap
            if c < n - 1:
                x2 = W / 2 + (c + 1 - (n - 1) / 2) * gap + sgn * sh * 28
                d.line((x, y, x2, y), fill=(90, 96, 110, int(200 * k)), width=4)
            if r < n - 1:
                x3 = W / 2 + (c - (n - 1) / 2) * gap - sgn * sh * 28
                d.line((x, y, x3, y + gap), fill=(90, 96, 110, int(200 * k)), width=4)
    for r in range(n):
        for c in range(n):
            sgn = 1 if r % 2 == 0 else -1
            x = W / 2 + (c - (n - 1) / 2) * gap + sgn * sh * 28
            y = 860 + (r - (n - 1) / 2) * gap
            col = NI if (r + c) % 2 == 0 else TI
            d.ellipse((x - 26, y - 26, x + 26, y + 26), fill=col + (int(255 * k),))
    label(d, 300, "FRIO: MARTENSITA", BLUE, seg(u, 0, 0.12))
    text_c(d, 380, "átomos mudam de orientação, sem trocar de vizinhos", F_MID, WHITE, alpha=seg(u, 0.4, 0.55))
    return img

def s5(img, d, u, t):
    k = seg(u, 0.0, 0.2)
    sh = 1 - seg(u, 0.2, 0.6)
    n, gap = 6, 95
    img = glow(img, W / 2, 860, 300, 0.35 * seg(u, 0.15, 0.4), HOT)
    d = ImageDraw.Draw(img)
    for r in range(n):
        for c in range(n):
            sgn = 1 if r % 2 == 0 else -1
            x = W / 2 + (c - (n - 1) / 2) * gap + sgn * sh * 28
            y = 860 + (r - (n - 1) / 2) * gap
            col = NI if (r + c) % 2 == 0 else TI
            d.ellipse((x - 26, y - 26, x + 26, y + 26), fill=col + (int(255 * k),))
    label(d, 300, "QUENTE: AUSTENITA", HOT, seg(u, 0, 0.12))
    text_c(d, 380, "a estrutura se refaz no formato memorizado", F_MID, WHITE, alpha=seg(u, 0.5, 0.65))
    return img

def s6(img, d, u, t):
    k = seg(u, 0.0, 0.2)
    # forno
    d.rounded_rectangle((200, 600, W - 200, 1060), 36, outline=(150, 160, 175, int(255 * k)), width=8)
    d.rounded_rectangle((225, 625, W - 225, 1035), 28, fill=(60, 30, 20, int(255 * k)))
    img = glow(img, W / 2, 830, 260, 0.5 * seg(u, 0.15, 0.4), HOT)
    d = ImageDraw.Draw(img)
    wire(d, 300, W - 300, 830, 0, t, alpha=int(255 * k))
    text_c(d, 700, "400–500 °C", F_LBL, ACC, alpha=seg(u, 0.25, 0.4))
    text_c(d, 940, "por alguns minutos", F_MID, WHITE, alpha=seg(u, 0.35, 0.5))
    label(d, 300, "GRAVANDO A FORMA", ACC, seg(u, 0, 0.12))
    return img

def s7(img, d, u, t):
    k1 = seg(u, 0.05, 0.25); k2 = seg(u, 0.35, 0.55)
    # aparelho ortodôntico: arco com braquetes
    cx, cy = W / 2 - 230, 840
    pts = [(cx + 170 * math.cos(a), cy + 120 * math.sin(a)) for a in [math.pi + i * math.pi / 20 for i in range(21)]]
    d.line(pts, fill=WIRE + (int(255 * k1),), width=8)
    for i in range(0, 21, 4):
        x, y = pts[i]
        d.rounded_rectangle((x - 16, y - 16, x + 16, y + 16), 6, fill=(220, 224, 232, int(255 * k1)))
    text_c(d, 960, "ortodontia", F_MID, WHITE, alpha=k1, x=W / 2 - 230)
    # stent: tubo em malha
    sx, sy = W / 2 + 230, 820
    for i in range(9):
        x = sx - 160 + i * 40
        d.line((x, sy - 60, x + 40, sy + 60), fill=WIRE + (int(255 * k2),), width=5)
        d.line((x + 40, sy - 60, x, sy + 60), fill=WIRE + (int(255 * k2),), width=5)
    d.line((sx - 160, sy - 60, sx + 200, sy - 60), fill=WIRE + (int(255 * k2),), width=4)
    d.line((sx - 160, sy + 60, sx + 200, sy + 60), fill=WIRE + (int(255 * k2),), width=4)
    text_c(d, 960, "stents", F_MID, WHITE, alpha=k2, x=W / 2 + 250)
    label(d, 300, "ONDE ESTÁ HOJE", ACC, seg(u, 0, 0.12))
    return img

def s8(img, d, u, t):
    k = seg(u, 0.0, 0.2)
    wire(d, 200, W - 200, 760, 0, t, col=(120, 170, 255), alpha=int(255 * k))
    text_c(d, 860, "esfriou: continua reto", F_MID, BLUE, alpha=seg(u, 0.2, 0.35))
    label(d, 300, "E AO ESFRIAR?", BLUE, seg(u, 0, 0.12))
    return img

def s9(img, d, u, t):
    wire(d, 200, W - 200, 560, 0, t)
    text_c(d, 660, "SALVA PRA LEMBRAR", F_LBL, WHITE, alpha=seg(u, 0, 0.2))
    text_c(d, 760, "@parecefakeereal", F_LOGO, ACC, alpha=seg(u, 0.1, 0.35))
    text_c(d, 860, "Parece fake. É real.", F_MID, WHITE, alpha=seg(u, 0.25, 0.5))
    return img

CHUNKS = [
 ("Por que esse fio amassado volta a ficar reto só com calor?", "Por que esse fio amassado volta a ficar reto só com calor?", s0),
 ("Ele é de nitinol: uma liga de níquel e titânio, quase meio a meio.", "Ele é de nitinol: uma liga de níquel e titânio, quase meio a meio.", s1),
 ("O nome vem de Ni, Ti e NOL, o laboratório naval dos EUA onde o efeito foi notado em 1961.", "O nome vem de níquel, titânio e da sigla do laboratório naval dos Estados Unidos onde o efeito foi notado, em mil novecentos e sessenta e um.", s2),
 ("Segundo o relato, alguém aqueceu uma tira amassada com o isqueiro do cachimbo. E ela se esticou.", "Segundo o relato, alguém aqueceu uma tira amassada com o isqueiro do cachimbo. E ela se esticou.", s3),
 ("Frio, o metal está numa fase chamada martensita. Ao dobrar, os átomos mudam de orientação, sem trocar de vizinhos.", "Frio, o metal está numa fase chamada martensita. Ao dobrar, os átomos mudam de orientação, sem trocar de vizinhos.", s4),
 ("Aquecido, vira austenita: a estrutura se refaz no formato memorizado.", "Aquecido, ele vira austenita, e a estrutura se refaz no formato memorizado.", s5),
 ("Esse formato é gravado antes, a uns 400 a 500 °C, por alguns minutos.", "Esse formato é gravado antes, num forno a uns quatrocentos a quinhentos graus, por alguns minutos.", s6),
 ("Hoje o nitinol aparece em fios de aparelho ortodôntico e em stents.", "Hoje o nitinol aparece em fios de aparelho ortodôntico e em stents.", s7),
 ("E ao esfriar de novo? Ele não se amassa sozinho: continua reto.", "E ao esfriar de novo? Ele não se amassa sozinho. Continua reto.", s8),
 ("Salva pra lembrar do metal que tem memória.", "Salva pra lembrar do metal que tem memória.", s9),
]

if __name__ == "__main__":
    wd = os.path.join(os.environ.get("WORK_DIR", "/tmp/reelwork"), "reel5")
    note = "Animação autoral, sem escala · locução sintética"
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        render(CHUNKS, wd, None, note, voice="M3", speed=1.22, previews=[0.03, 0.12, 0.22, 0.32, 0.43, 0.55, 0.65, 0.75, 0.86, 0.95, 0.99])
    else:
        render(CHUNKS, wd, sys.argv[1], note, voice="M3", speed=1.22)
