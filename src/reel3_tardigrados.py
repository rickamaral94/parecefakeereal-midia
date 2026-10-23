import sys, math
from engine import *

TARDI = (214, 196, 170); TARDI_D = (160, 140, 118)

def tardigrade(d, cx, cy, s=1.0, tun=0.0, col=TARDI, wiggle=0.0, alpha=255):
    """Tardígrado estilizado; tun=1 → forma de barril (desidratado)."""
    c = col + (alpha,); cd = TARDI_D + (alpha,) if col == TARDI else tuple(int(v * 0.7) for v in col) + (alpha,)
    L = lerp(300, 170, tun) * s; Hh = lerp(130, 120, tun) * s
    # pernas (somem no modo barril)
    leg = (1 - tun)
    if leg > 0.05:
        for k in range(4):
            lx = cx - L / 2 + L * (0.18 + 0.22 * k)
            sw = 10 * math.sin(wiggle * 6 + k) * s
            d.rounded_rectangle((lx - 18 * s + sw, cy + Hh * 0.25, lx + 18 * s + sw, cy + Hh * 0.25 + 70 * s * leg), 14 * s, fill=cd)
            for c2 in (-12, 0, 12):
                d.line((lx + sw + c2 * s, cy + Hh * 0.25 + 70 * s * leg, lx + sw + c2 * s * 1.4, cy + Hh * 0.25 + 85 * s * leg), fill=(60, 50, 40, alpha), width=max(2, int(4 * s)))
    d.rounded_rectangle((cx - L / 2, cy - Hh / 2, cx + L / 2, cy + Hh / 2), int(Hh / 2), fill=c)
    # segmentos
    for k in range(1, 5):
        x = cx - L / 2 + L * k / 5
        d.arc((x - 20 * s, cy - Hh / 2, x + 20 * s, cy + Hh / 2), 260, 100, fill=cd, width=max(2, int(4 * s)))
    if tun < 0.5:
        hx = cx + L / 2 - 30 * s
        d.ellipse((hx - 8 * s, cy - 18 * s, hx + 6 * s, cy - 4 * s), fill=(40, 30, 25, alpha))
        d.ellipse((cx + L / 2 - 14 * s, cy - 2 * s, cx + L / 2 + 6 * s, cy + 16 * s), fill=cd)

def earth_arc(d):
    d.ellipse((-600, 1640, W + 600, 3700), fill=(30, 70, 140, 255))
    d.ellipse((-600, 1640, W + 600, 3700), outline=(110, 170, 255, 255), width=6)

def s0(img, d, u, t):
    earth_arc(d)
    y = 820 + 20 * math.sin(t * 1.5)
    d.ellipse((W / 2 - 230, y - 120, W / 2 + 230, y + 130), outline=(255, 255, 255, 40), width=3)
    tardigrade(d, W / 2, y, 1.1, wiggle=t)
    text_c(d, 290, "COMO UM ANIMAL", F_HOOK, WHITE, maxw=1000)
    text_c(d, 390, "SOBREVIVEU AO VÁCUO?", F_HOOK, ACC, maxw=1000)
    return img

def s1(img, d, u, t):
    for k in range(9):
        x = 140 + k * 105; h = 190 + 40 * math.sin(k * 1.3)
        d.polygon([(x - 20, 1120), (x + 4 * math.sin(t + k), 1120 - h), (x + 20, 1120)], fill=LEAF_D + (255,))
    tardigrade(d, W / 2, 790, 0.9, wiggle=t)
    k = seg(u, 0.35, 0.55)
    if k > 0:
        d.line((W / 2 - 150, 660, W / 2 + 150, 660), fill=ACC + (int(255 * k),), width=6)
        for x in (W / 2 - 150, W / 2 + 150): d.line((x, 645, x, 675), fill=ACC + (int(255 * k),), width=6)
        text_c(d, 580, "≈ 1 mm", F_MID, ACC, alpha=k)
    label(d, 300, "URSO-D'ÁGUA", ACC, seg(u, 0, 0.15))
    text_c(d, 380, "tardígrado · vive em musgos e liquens", F_MID, WHITE, alpha=seg(u, 0.15, 0.3))
    return img

def s2(img, d, u, t):
    tun = seg(u, 0.15, 0.55)
    tardigrade(d, W / 2, 800, 1.0, tun=tun, col=tuple(int(lerp(a, b, tun)) for a, b in zip(TARDI, (176, 150, 112))), wiggle=t * (1 - tun))
    # medidor de metabolismo
    k = seg(u, 0.1, 0.2)
    x0, y0 = 240, 1030
    d.rounded_rectangle((x0, y0, W - x0, y0 + 46), 23, outline=WHITE + (int(255 * k),), width=4)
    lvl = lerp(1, 0.03, seg(u, 0.25, 0.7))
    d.rounded_rectangle((x0 + 6, y0 + 6, x0 + 6 + (W - 2 * x0 - 12) * lvl, y0 + 40), 18, fill=(GREEN if lvl > 0.3 else RED) + (int(255 * k),))
    text_c(d, y0 - 60, "metabolismo", F_SMALL, WHITE, alpha=k)
    label(d, 300, "MODO PAUSA", ACC, seg(u, 0.4, 0.55))
    text_c(d, 380, "desidratado, em forma de barril", F_MID, WHITE, alpha=seg(u, 0.5, 0.65))
    return img

def capsule(d, cx, cy, lid):
    d.polygon([(cx - 150, cy + 140), (cx + 150, cy + 140), (cx + 90, cy - 140), (cx - 90, cy - 140)], fill=(120, 126, 140, 255))
    d.rectangle((cx - 160, cy + 130, cx + 160, cy + 170), fill=(80, 86, 100, 255))
    # tampa abre
    a = math.radians(-70 * lid)
    px, py = cx - 90, cy - 140
    ex, ey = px + 180 * math.cos(a), py + 180 * math.sin(a)
    d.line((px, py, ex, ey), fill=(200, 205, 215, 255), width=18)
    for k in range(5):
        tx = cx - 60 + k * 30
        d.ellipse((tx - 10, cy - 130, tx + 10, cy - 110), fill=(176, 150, 112, 255))

def s3(img, d, u, t):
    earth_arc(d)
    cx = lerp(W / 2 - 60, W / 2 + 60, u); cy = 820
    capsule(d, cx, cy, seg(u, 0.55, 0.75))
    if u > 0.75:
        for k in range(12):
            r = 120 + ((t * 120 + k * 40) % 260)
            d.line((cx, cy - 140, cx + r * math.cos(k), cy - 140 - abs(r * math.sin(k)) * 0.6), fill=(150, 170, 255, 70), width=3)
    label(d, 300, "FOTON-M3 · 2007", ACC, seg(u, 0, 0.12))
    text_c(d, 380, "Agência Espacial Europeia", F_MID, WHITE, alpha=seg(u, 0.12, 0.25))
    text_c(d, 1070, "vácuo + radiação do espaço", F_MID, BLUE, alpha=seg(u, 0.75, 0.85))
    return img

def grid_tardis(d, alive_frac, u, y0=600, rows=3, cols=4, s=0.42):
    n = rows * cols; alive = round(n * alive_frac)
    for k in range(n):
        r, c = divmod(k, cols)
        x = 200 + c * 225; y = y0 + r * 150
        ok = k < alive
        col = TARDI if ok else (90, 92, 100)
        tardigrade(d, x, y, s, wiggle=(u * 20 + k) if ok else 0, col=col)

def s4(img, d, u, t):
    grid_tardis(d, 0.83, u)
    label(d, 300, "VÁCUO", BLUE, seg(u, 0, 0.15))
    text_c(d, 380, "a maioria sobreviveu", F_MID, GREEN, alpha=seg(u, 0.25, 0.4))
    return img

def s5(img, d, u, t):
    # Sol e raios UV
    img = glow(img, 900, 330, 160, 0.9, (255, 210, 90)); d = ImageDraw.Draw(img)
    d.ellipse((840, 270, 960, 390), fill=(255, 220, 110, 255))
    for k in range(8):
        a = math.radians(180 + 10 * k + 5 * math.sin(t * 3 + k))
        d.line((900 + 90 * math.cos(a), 330 - 90 * math.sin(a) * -1, 900 + 520 * math.cos(a), 330 + 520 * math.sin(-a) * -1), fill=(190, 120, 255, 120), width=6)
    grid_tardis(d, lerp(1.0, 0.17, seg(u, 0.3, 0.7)), u, y0=650)
    text_c(d, 300, "UV SOLAR", F_LBL, (200, 140, 255), x=380, maxw=600)
    text_c(d, 380, "> 1.000× a da superfície", F_MID, WHITE, alpha=seg(u, 0.1, 0.25), x=380, maxw=640)
    text_c(d, 1080, "alguns resistiram", F_MID, ACC, alpha=seg(u, 0.7, 0.8))
    return img

def s6(img, d, u, t):
    tardigrade(d, W / 2 - 160, 760, 0.8, wiggle=t)
    for k in range(3):
        k2 = seg(u, 0.15 + 0.15 * k, 0.3 + 0.15 * k)
        x = W / 2 + 140 + k * 110; y = 980
        if k2 > 0:
            d.ellipse((x - 40, y - 40, x + 40, y + 40), fill=(230, 220, 190, int(255 * k2)))
            if u > 0.7:
                tardigrade(d, x, y - 120, 0.28, wiggle=t + k, alpha=int(255 * seg(u, 0.7, 0.85)))
    label(d, 300, "E SE REPRODUZIRAM", GREEN, seg(u, 0, 0.15))
    return img

def s7(img, d, u, t):
    k1 = seg(u, 0.0, 0.2); k2 = seg(u, 0.25, 0.45); k3 = seg(u, 0.55, 0.75)
    d.rounded_rectangle((140, 520, W - 140, 680), 26, fill=(20, 52, 36, int(230 * k1)))
    text_c(d, 565, "SECOS ✓   ATIVOS ✗", F_LBL, GREEN, alpha=k1)
    d.rounded_rectangle((140, 740, W - 140, 980), 26, fill=(60, 24, 28, int(230 * k2)))
    text_c(d, 770, "UV TOTAL", F_LBL, RED, alpha=k2)
    text_c(d, 860, "a maioria não resistiu", F_MID, WHITE, alpha=k3)
    label(d, 300, "DETALHE IMPORTANTE", ACC, seg(u, 0, 0.12))
    return img

def s8(img, d, u, t):
    tardigrade(d, W / 2, 470, 0.6, wiggle=t)
    text_c(d, 640, "@parecefakeereal", F_LOGO, ACC, alpha=seg(u, 0, 0.3))
    text_c(d, 740, "Parece fake. É real.", F_MID, WHITE, alpha=seg(u, 0.15, 0.45))
    return img

CHUNKS = [
 ("Como um animal sobreviveu ao vácuo do espaço, sem traje?", "Como um animal sobreviveu ao vácuo do espaço, sem traje?", s0),
 ("Ele é um tardígrado, o urso-d'água. Mede cerca de 1 milímetro e vive em musgos e liquens que secam com frequência.", "Ele é um tardígrado, o urso-d'água. Mede cerca de um milímetro, e vive em musgos e liquens que secam com frequência.", s1),
 ("Quando o ambiente seca, ele desidrata e praticamente para o metabolismo.", "Quando o ambiente seca, ele desidrata, e praticamente para o metabolismo.", s2),
 ("Em 2007, a missão FOTON-M3, da Agência Espacial Europeia, expôs tardígrados secos ao vácuo e à radiação do espaço.", "Em dois mil e sete, a missão Fóton eme três, da Agência Espacial Europeia, expôs tardígrados secos ao vácuo e à radiação do espaço.", s3),
 ("De volta à Terra, a maioria sobreviveu ao vácuo.", "De volta à Terra, a maioria sobreviveu ao vácuo.", s4),
 ("Alguns resistiram até à radiação ultravioleta do Sol, mais de mil vezes mais forte que na superfície da Terra.", "Alguns resistiram até à radiação ultravioleta do Sol, mais de mil vezes mais forte do que na superfície da Terra.", s5),
 ("E os sobreviventes se reproduziram.", "E os sobreviventes se reproduziram.", s6),
 ("Detalhe: eles estavam secos, não ativos. E, com o ultravioleta total, a maioria não resistiu.", "Detalhe: eles estavam secos, não ativos. E, com o ultravioleta total, a maioria não resistiu.", s7),
 ("Siga para mais ciência que parece mentira.", "Siga, para mais ciência que parece mentira.", s8),
]

if __name__ == "__main__":
    import os; wd = os.path.join(os.environ.get("WORK_DIR", "/tmp/reelwork"), "reel3")
    note = "Ilustração autoral; não são imagens do experimento"
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        render(CHUNKS, wd, None, note, voice="M4", speed=1.22, previews=[0.04, 0.15, 0.3, 0.42, 0.55, 0.68, 0.76, 0.86, 0.97])
    else:
        render(CHUNKS, wd, sys.argv[1], note, voice="M4", speed=1.22)
