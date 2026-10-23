import sys, math
from engine import *

def leaf(d, x, y, ang, L, col):
    a = math.radians(ang)
    tipx, tipy = x + L * math.cos(a), y + L * math.sin(a)
    nx, ny = -math.sin(a) * L * 0.28, math.cos(a) * L * 0.28
    mx, my = (x + tipx) / 2, (y + tipy) / 2
    d.polygon([(x, y), (mx + nx, my + ny), (tipx, tipy), (mx - nx, my - ny)], fill=col)

def plant(d, cx, by, s=1.0, wilt=0.0, tomatoes=True, cut=False):
    # pot
    d.polygon([(cx - 130 * s, by), (cx + 130 * s, by), (cx + 100 * s, by + 170 * s), (cx - 100 * s, by + 170 * s)], fill=(176, 98, 62))
    d.rectangle((cx - 140 * s, by - 20 * s, cx + 140 * s, by + 10 * s), fill=(150, 82, 52))
    d.ellipse((cx - 125 * s, by - 32 * s, cx + 125 * s, by + 4 * s), fill=SOIL)
    top = by - 420 * s
    col = tuple(int(lerp(c1, c2, wilt)) for c1, c2 in zip(LEAF, (150, 150, 80)))
    d.line((cx, by - 10 * s, cx, top), fill=LEAF_D, width=int(16 * s))
    if cut:
        d.line((cx - 30 * s, by - 150 * s, cx + 30 * s, by - 170 * s), fill=BG, width=int(12 * s))
    for k, (yy, side) in enumerate([(0.25, 1), (0.4, -1), (0.55, 1), (0.7, -1), (0.85, 1), (0.95, -1)]):
        y = by - 10 * s - (by - 10 * s - top) * yy
        base = 0 if side > 0 else 180
        droop = 35 * wilt
        ang = base + (-25 - 0 + droop) * (1 if side > 0 else -1)
        leaf(d, cx, y, ang, 150 * s, col)
    if tomatoes:
        for (dx, dy) in [(-70, -230), (60, -300), (-40, -350)]:
            d.ellipse((cx + dx * s - 30 * s, by + dy * s - 30 * s, cx + dx * s + 30 * s, by + dy * s + 30 * s), fill=TOMATO)

def waves(d, cx, cy, t, n=3, col=ACC, r0=60, maxr=260, alpha=1.0):
    for k in range(n):
        ph = ((t * 0.8 + k / n) % 1)
        r = r0 + (maxr - r0) * ph
        a = int(255 * (1 - ph) * alpha)
        if a > 3:
            d.arc((cx - r, cy - r, cx + r, cy + r), -40, 40, fill=col + (a,), width=8)
            d.arc((cx - r, cy - r, cx + r, cy + r), 140, 220, fill=col + (a,), width=8)

def mute_icon(d, x, y, k):
    if k <= 0.01: return
    c = WHITE + (int(255 * k),)
    d.polygon([(x, y + 20), (x + 30, y + 20), (x + 70, y - 15), (x + 70, y + 95), (x + 30, y + 60), (x, y + 60)], fill=c)
    d.line((x + 95, y + 10, x + 155, y + 70), fill=RED + (int(255 * k),), width=12)
    d.line((x + 95, y + 70, x + 155, y + 10), fill=RED + (int(255 * k),), width=12)

def s0(img, d, u, t):
    plant(d, W / 2, 1060, 0.72)
    waves(d, W / 2, 880, t, alpha=1.0)
    text_c(d, 290, "ESSE TOMATEIRO ESTÁ", F_LBL, WHITE, maxw=1000)
    text_c(d, 370, "FAZENDO BARULHO", F_HOOK, ACC, maxw=1000)
    mute_icon(d, W / 2 - 80, 540, seg(u, 0.4, 0.6))
    return img

def s1(img, d, u, t):
    d.rounded_rectangle((200, 480, 880, 1140), 30, outline=(90, 100, 120), width=10, fill=(20, 24, 34, 255))
    for k in range(9):
        y = 520 + k * 68
        d.line((215, y, 245, y + 30), fill=(70, 78, 96), width=6); d.line((835, y, 865, y + 30), fill=(70, 78, 96), width=6)
    plant(d, W / 2, 960, 0.85)
    for side in (-1, 1):
        mx = W / 2 + side * 250
        k = seg(u, 0.2, 0.45)
        d.line((mx, 560, mx, lerp(560, 700, k)), fill=GRAY, width=8)
        d.rounded_rectangle((mx - 22, lerp(560, 700, k), mx + 22, lerp(560, 700, k) + 80), 12, fill=METAL)
    label(d, 300, "CÂMARA ACÚSTICA", ACC, seg(u, 0, 0.15))
    text_c(d, 380, "microfones de ultrassom", F_MID, WHITE, alpha=seg(u, 0.25, 0.4))
    return img

def s2(img, d, u, t):
    plant(d, 300, 1000, 0.7, wilt=seg(u, 0.1, 0.5) * 0.7, tomatoes=False)
    plant(d, 780, 1000, 0.7, tomatoes=False, cut=u > 0.55)
    # water drop crossed
    k1 = seg(u, 0.05, 0.2)
    if k1 > 0:
        cx, cy = 300, 560
        d.polygon([(cx, cy - 60), (cx - 40, cy + 10), (cx + 40, cy + 10)], fill=BLUE + (int(255 * k1),))
        d.ellipse((cx - 40, cy - 25, cx + 40, cy + 50), fill=BLUE + (int(255 * k1),))
        d.line((cx - 60, cy - 70, cx + 60, cy + 70), fill=RED + (int(255 * k1),), width=12)
    k2 = seg(u, 0.5, 0.65)
    if k2 > 0:
        x, y = 780 + lerp(200, 0, k2), 860
        d.ellipse((x - 70, y - 40, x - 20, y + 10), outline=WHITE + (int(255 * k2),), width=8)
        d.ellipse((x - 70, y + 20, x - 20, y + 70), outline=WHITE + (int(255 * k2),), width=8)
        d.line((x - 25, y + 0, x + 60, y + 40), fill=WHITE + (int(255 * k2),), width=8)
        d.line((x - 25, y + 40, x + 60, y + 0), fill=WHITE + (int(255 * k2),), width=8)
    text_c(d, 330, "dias sem água", F_MID, BLUE, alpha=k1, x=300, maxw=440)
    text_c(d, 330, "caule cortado", F_MID, WHITE, alpha=k2, x=780, maxw=440)
    return img

def s3(img, d, u, t):
    rows = [("saudável", "< 1 / hora", 1, GREEN), ("estressada", "~30–50 / hora", 40, RED)]
    for r, (name, txt, n, col) in enumerate(rows):
        y = 560 + r * 300
        d.text((120, y), name, font=F_LBL, fill=col + (255,))
        d.text((120, y + 80), txt, font=F_MID, fill=WHITE + (255,))
        shown = int(n * seg(u, 0.1, 0.85))
        for k in range(shown):
            cx = 620 + (k % 10) * 36; cy = y + 20 + (k // 10) * 40
            pop = 1 - clamp((u - (0.1 + 0.75 * k / max(1, n))) * 8)
            rr = 10 + 8 * pop
            d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=ACC)
    label(d, 300, "CLIQUES POR HORA", ACC, seg(u, 0, 0.12))
    return img

def s4(img, d, u, t):
    x0, x1, y = 120, 960, 760
    d.line((x0, y, x1, y), fill=WHITE, width=6)
    def X(khz): return x0 + (x1 - x0) * khz / 100
    for khz in (0, 20, 40, 60, 80, 100):
        d.line((X(khz), y - 15, X(khz), y + 15), fill=WHITE, width=4)
        lab = f"{khz}"; d.text((X(khz) - d.textlength(lab, font=F_SMALL) / 2, y + 30), lab, font=F_SMALL, fill=WHITE)
    d.text((x1 - 60, y + 80), "kHz", font=F_SMALL, fill=GRAY)
    k1 = seg(u, 0.05, 0.25)
    d.rounded_rectangle((X(0), y - 120, X(0) + (X(20) - X(0)) * k1, y - 50), 14, fill=BLUE + (int(230 * k1),))
    text_c(d, y - 200, "ouvido humano", F_MID, BLUE, alpha=k1, x=(X(0) + X(20)) / 2 + 60, maxw=400)
    k2 = seg(u, 0.25, 0.45)
    d.rounded_rectangle((X(40), y - 120, X(40) + (X(80) - X(40)) * k2, y - 50), 14, fill=ACC + (int(230 * k2),))
    text_c(d, y - 200, "plantas", F_MID, ACC, alpha=k2, x=(X(40) + X(80)) / 2)
    k3 = seg(u, 0.6, 0.75)
    if k3 > 0:
        bx, by = W / 2, 1010
        c = WHITE + (int(255 * k3),)
        d.polygon([(bx - 170, by - 10), (bx - 60, by - 50), (bx - 20, by), (bx, by - 40), (bx + 20, by), (bx + 60, by - 50), (bx + 170, by - 10), (bx + 40, by + 30), (bx, by + 60), (bx - 40, by + 30)], fill=c)
        text_c(d, 1080, "morcegos e alguns insetos escutam", F_SMALL, WHITE, alpha=k3)
    label(d, 300, "40 A 80 kHz", ACC, seg(u, 0, 0.12))
    return img

def s5(img, d, u, t):
    plant(d, W / 2, 1010, 1.0, tomatoes=False)
    for k, (dx, dy) in enumerate([(-160, 560), (150, 640), (-120, 760), (170, 820)]):
        ph = (t * 1.3 + k * 0.37) % 1
        if ph < 0.35:
            a = int(255 * (1 - ph / 0.35))
            d.text((W / 2 + dx - 40, dy), "clic", font=F_MID, fill=ACC + (a,))
    label(d, 300, "ANTES DE MURCHAR", ACC, seg(u, 0, 0.15))
    text_c(d, 380, "planta ainda verde, já emitindo cliques", F_MID, WHITE, alpha=seg(u, 0.2, 0.35))
    return img

def s6(img, d, u, t):
    k1 = seg(u, 0.0, 0.2); k2 = seg(u, 0.4, 0.6)
    d.rounded_rectangle((140, 560, W - 140, 740), 26, fill=(60, 24, 28, int(230 * k1)))
    text_c(d, 610, "NÃO É GRITO NEM DOR", F_LBL, RED, alpha=k1)
    d.rounded_rectangle((140, 800, W - 140, 980), 26, fill=(20, 52, 36, int(230 * k2)))
    text_c(d, 850, "SÃO CLIQUES", F_LBL, GREEN, alpha=k2)
    return img

def s7(img, d, u, t):
    k = seg(u, 0, 0.2)
    text_c(d, 560, "?", F_BIG, ACC, alpha=k)
    label(d, 760, "HIPÓTESE", ACC, seg(u, 0.15, 0.3))
    text_c(d, 850, "outros seres usam esses sons?", F_MID, WHITE, alpha=seg(u, 0.3, 0.45))
    text_c(d, 920, "ainda precisa ser testado", F_MID, GRAY, alpha=seg(u, 0.45, 0.6))
    return img

def s8(img, d, u, t):
    text_c(d, 640, "@parecefakeereal", F_LOGO, ACC, alpha=seg(u, 0, 0.3))
    text_c(d, 740, "Parece fake. É real.", F_MID, WHITE, alpha=seg(u, 0.15, 0.45))
    return img

CHUNKS = [
 ("Esse tomateiro está fazendo barulho. E você não consegue ouvir.", "Esse tomateiro está fazendo barulho. E você não consegue ouvir.", s0),
 ("Pesquisadores de Tel Aviv puseram tomateiros e tabaco perto de microfones de ultrassom.", "Pesquisadores da Universidade de Tel Aviv colocaram tomateiros e plantas de tabaco perto de microfones de ultrassom.", s1),
 ("Algumas ficaram dias sem água. Outras tiveram o caule cortado.", "Algumas ficaram dias sem água. Outras tiveram o caule cortado.", s2),
 ("As plantas estressadas emitiram dezenas de cliques por hora. As saudáveis, menos de um.", "As plantas estressadas emitiram dezenas de cliques por hora. As saudáveis, menos de um.", s3),
 ("Entre 40 e 80 kHz: agudo demais para nós, mas audível para morcegos e alguns insetos.", "Os sons ficam entre quarenta e oitenta quilohertz: agudos demais para nós, mas na faixa que morcegos e alguns insetos escutam.", s4),
 ("E as plantas sem água começaram a estalar antes de parecerem murchas.", "E as plantas sem água começaram a estalar antes de parecerem murchas.", s5),
 ("Mas atenção: isso não é grito, nem dor. São cliques.", "Mas atenção: isso não é grito, nem dor. São cliques.", s6),
 ("Se outros seres usam essa informação, ainda é uma hipótese a ser testada.", "Se outros seres usam essa informação, ainda é uma hipótese a ser testada.", s7),
 ("Manda pra quem conversa com as plantas.", "Manda pra quem conversa com as plantas.", s8),
]

if __name__ == "__main__":
    import os; wd = os.path.join(os.environ.get("WORK_DIR", "/tmp/reelwork"), "reel2")
    note = "Ilustração autoral; não são as gravações do estudo"
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        render(CHUNKS, wd, None, note, voice="M3", previews=[0.03, 0.13, 0.27, 0.38, 0.5, 0.62, 0.74, 0.86, 0.95, 0.99])
    else:
        render(CHUNKS, wd, sys.argv[1], note, voice="M3")
