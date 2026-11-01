import sys, math
import numpy as np
from engine import *

# Cores de película fina (ilustração): refletância ~ sen²(2π·n·d/λ), com inversão de fase
# na face externa. Diagrama sem escala; só para visualizar a ideia de interferência.
N_FILM = 1.33
LAMS = {0: (600, 640, 680), 1: (510, 540, 570), 2: (430, 460, 490)}
CYAN = (120, 220, 255); MAG = (240, 110, 220)

R0 = 270
yy, xx = np.mgrid[-R0:R0, -R0:R0].astype(np.float32)
RR = np.sqrt(xx ** 2 + yy ** 2) / R0
MASK = RR <= 1.0
YN = yy / R0  # -1 topo, +1 base

def film_rgb(dnm):
    out = np.zeros(dnm.shape + (3,), np.float32)
    for c, ls in LAMS.items():
        out[..., c] = sum(np.sin(2 * np.pi * N_FILM * dnm / l) ** 2 for l in ls) / len(ls)
    return out

def bubble_img(t, base=520.0, black=0.0, alpha=255):
    """base: espessura média (nm) da faixa de baixo; black: 0..1 afina o topo até ficar escuro."""
    grad = 0.25 + 0.75 * (YN + 1) / 2            # topo mais fino, base mais grossa
    swirl = 60 * np.sin(3.0 * xx / R0 + 2.2 * YN + t * 1.3) + 40 * np.sin(5.0 * YN - 2.0 * xx / R0 - t * 0.9)
    d = base * grad + swirl * grad
    d = d - black * 220 * np.clip(1 - (YN + 1) / 0.9, 0, 1)
    d = np.clip(d, 0, None)
    col = film_rgb(d)
    shade = 0.22 + 0.78 * np.clip(RR ** 1.6, 0, 1)   # borda mais refletiva, centro transparente
    rgb = np.clip(col * 255 * 1.15, 0, 255)
    a = (shade * 235 * MASK * (alpha / 255)).astype(np.uint8)
    arr = np.dstack([rgb.astype(np.uint8), a])
    im = Image.fromarray(arr, "RGBA")
    hd = ImageDraw.Draw(im)
    hd.ellipse((R0 - 190, R0 - 200, R0 - 120, R0 - 150), fill=(255, 255, 255, int(150 * alpha / 255)))
    hd.ellipse((0, 0, 2 * R0 - 1, 2 * R0 - 1), outline=(220, 230, 255, int(120 * alpha / 255)), width=3)
    return im

def put_bubble(img, cx, cy, t, s=1.0, **kw):
    b = bubble_img(t, **kw)
    if s != 1.0:
        b = b.resize((int(2 * R0 * s), int(2 * R0 * s)))
    img.alpha_composite(b, (int(cx - b.width / 2), int(cy - b.height / 2)))

def soft_bg(d, t):
    d.rectangle((0, 0, W, H), fill=(12, 14, 22, 255))
    for i in range(14):
        x = (i * 173 + t * 12) % (W + 200) - 100
        y = 200 + (i * 331) % 1500
        r = 6 + (i % 4) * 3
        d.ellipse((x - r, y - r, x + r, y + r), outline=(40, 46, 66, 255), width=2)

def film_diagram(d, u, t, show_out=True, phase=0.0):
    # película: duas linhas (sabão) com água entre elas, vista em corte
    y1, y2 = 820, 900
    d.rectangle((120, y1, 960, y2), fill=(60, 110, 170, 120))
    d.line((120, y1, 960, y1), fill=WHITE + (255,), width=5)
    d.line((120, y2, 960, y2), fill=WHITE + (255,), width=5)
    text_c(d, 775, "face de fora", F_SMALL, GRAY, x=850)
    text_c(d, 915, "face de dentro", F_SMALL, GRAY, x=850)
    k = seg(u, 0.05, 0.4)
    # raio incidente
    x0, y0 = 300, 520
    xi, yi = lerp(x0, 470, k), lerp(y0, y1, k)
    d.line((x0, y0, xi, yi), fill=ACC + (255,), width=6)
    if show_out and u > 0.35:
        k2 = seg(u, 0.35, 0.7)
        d.line((470, y1, lerp(470, 640, k2), lerp(y1, 520, k2)), fill=CYAN + (255,), width=6)
        d.line((470, y1, 505, y2), fill=ACC + (180,), width=4)
        d.line((505, y2, 540, y1), fill=MAG + (220,), width=4)
        d.line((540, y1, lerp(540, 710, k2), lerp(y1, 520, k2)), fill=MAG + (255,), width=6)

def wave(d, y, amp, ph, col, a=255, x0=160, x1=920):
    pts = [(x, y + amp * math.sin((x - x0) / 55 + ph)) for x in range(x0, x1, 6)]
    d.line(pts, fill=col + (a,), width=6)

def s0(img, d, u, t):
    put_bubble(img, W / 2, 860 + 12 * math.sin(t * 1.5), t)
    d = ImageDraw.Draw(img)
    text_c(d, 170, "POR QUE UMA BOLHA", F_HOOK, WHITE, maxw=1040)
    text_c(d, 270, "TRANSPARENTE FICA", F_HOOK, WHITE, maxw=1040)
    text_c(d, 370, "COLORIDA?", F_HOOK, ACC, maxw=1040, alpha=seg(u, 0.1, 0.25))
    return img

def s1(img, d, u, t):
    put_bubble(img, W / 2, 860, t)
    d = ImageDraw.Draw(img)
    label(d, 240, "NÃO É TINTA", RED, seg(u, 0, 0.12))
    text_c(d, 340, "a cor vem da própria luz", F_MID, WHITE, alpha=seg(u, 0.3, 0.45))
    return img

def s2(img, d, u, t):
    k = seg(u, 0.1, 0.5)
    y1, y2 = lerp(860, 800, k), lerp(860, 920, k)
    d.rectangle((120, y1, 960, y2), fill=(60, 110, 170, int(140 * k)))
    d.line((120, y1, 960, y1), fill=WHITE + (255,), width=6)
    d.line((120, y2, 960, y2), fill=WHITE + (255,), width=6)
    text_c(d, 740 - 60 * k, "sabão", F_SMALL, WHITE, alpha=k)
    text_c(d, 838, "água", F_SMALL, CYAN, alpha=k)
    text_c(d, 940 + 0 * k, "sabão", F_SMALL, WHITE, alpha=k)
    label(d, 240, "PELÍCULA FINÍSSIMA", CYAN, seg(u, 0, 0.12))
    text_c(d, 340, "a parede da bolha, em corte", F_MID, WHITE, alpha=seg(u, 0.2, 0.35))
    text_c(d, 1100, "diagrama sem escala", F_SMALL, GRAY, alpha=k)
    return img

def s3(img, d, u, t):
    film_diagram(d, u, t)
    label(d, 240, "A LUZ REFLETE DUAS VEZES", ACC, seg(u, 0, 0.12))
    return img

def s4(img, d, u, t):
    film_diagram(d, 1.0, t)
    label(d, 240, "CAMINHO MAIS LONGO", MAG, seg(u, 0, 0.12))
    text_c(d, 340, "o raio de dentro sai", F_MID, WHITE, alpha=seg(u, 0.2, 0.35))
    text_c(d, 400, "fora de passo", F_MID, MAG, alpha=seg(u, 0.35, 0.5))
    return img

def s5(img, d, u, t):
    k = seg(u, 0.05, 0.3)
    wave(d, 600, 45, t * 3, CYAN, int(255 * k))
    wave(d, 600, 45, t * 3, MAG, int(255 * k), x0=160, x1=920)
    text_c(d, 690, "em fase: se somam", F_MID, GREEN, alpha=k)
    k2 = seg(u, 0.4, 0.65)
    wave(d, 900, 45, t * 3, CYAN, int(255 * k2))
    wave(d, 900, 45, t * 3 + math.pi, MAG, int(255 * k2))
    text_c(d, 990, "fora de fase: se cancelam", F_MID, RED, alpha=k2)
    label(d, 240, "INTERFERÊNCIA", ACC, seg(u, 0, 0.12))
    return img

def s6(img, d, u, t):
    # tira de espessura crescente
    x0, x1, y0, y1 = 140, 940, 640, 860
    ds = np.linspace(80, 700, x1 - x0, dtype=np.float32)
    strip = np.clip(film_rgb(ds[None, :].repeat(y1 - y0, 0)) * 255 * 1.15, 0, 255).astype(np.uint8)
    k = seg(u, 0.1, 0.5)
    im = Image.fromarray(strip, "RGB").convert("RGBA")
    im.putalpha(int(255 * k))
    img.alpha_composite(im, (x0, y0))
    d = ImageDraw.Draw(img)
    text_c(d, 890, "mais fina  →  mais grossa", F_MID, WHITE, alpha=k)
    label(d, 240, "A ESPESSURA ESCOLHE", ACC, seg(u, 0, 0.12))
    text_c(d, 340, "qual cor sobra", F_MID, WHITE, alpha=seg(u, 0.2, 0.35))
    text_c(d, 1100, "ilustração simplificada", F_SMALL, GRAY, alpha=k)
    return img

def s7(img, d, u, t):
    put_bubble(img, W / 2, 860, t * 3, base=lerp(560, 430, u))
    d = ImageDraw.Draw(img)
    for i in range(3):
        y = 1000 + ((t * 80 + i * 40) % 120)
        d.polygon([(W / 2 - 14 + i * 0, y), (W / 2 + 14, y), (W / 2, y + 22)], fill=CYAN + (200,))
    label(d, 240, "ELA VAI AFINANDO", CYAN, seg(u, 0, 0.12))
    text_c(d, 330, "o líquido escorre e evapora", F_MID, WHITE, alpha=seg(u, 0.2, 0.35))
    text_c(d, 390, "e as cores giram", F_MID, ACC, alpha=seg(u, 0.4, 0.55))
    return img

def s8(img, d, u, t):
    put_bubble(img, W / 2, 860, t * 2, base=420, black=seg(u, 0.15, 0.7))
    d = ImageDraw.Draw(img)
    label(d, 240, "MANCHAS ESCURAS", WHITE, seg(u, 0, 0.12))
    text_c(d, 330, "mais fina que o comprimento", F_MID, WHITE, alpha=seg(u, 0.2, 0.35))
    text_c(d, 390, "de onda da luz: tudo se cancela", F_MID, WHITE, alpha=seg(u, 0.2, 0.35))
    return img

def s9(img, d, u, t):
    if u < 0.55:
        put_bubble(img, W / 2, 860, t * 2, base=420, black=1.0)
    else:
        k = seg(u, 0.55, 0.75)
        d = ImageDraw.Draw(img)
        for i in range(16):
            ang = i * 2 * math.pi / 16
            r = lerp(R0, R0 + 160, k)
            x, y = W / 2 + r * math.cos(ang), 860 + r * math.sin(ang)
            d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=CYAN + (int(255 * (1 - k)),))
    d = ImageDraw.Draw(img)
    label(d, 240, "SINAL DE QUE VAI ESTOURAR", RED, seg(u, 0, 0.12))
    return img

def s10(img, d, u, t):
    put_bubble(img, W / 2, 900, t, s=0.85)
    d = ImageDraw.Draw(img)
    label(d, 240, "RESSALVA", RED, seg(u, 0, 0.12))
    text_c(d, 340, "o ângulo de visão e a luz", F_MID, WHITE, alpha=seg(u, 0.05, 0.2))
    text_c(d, 400, "também mudam a cor", F_MID, WHITE, alpha=seg(u, 0.05, 0.2))
    return img

def s11(img, d, u, t):
    put_bubble(img, W / 2, 1000, t, s=0.7)
    d = ImageDraw.Draw(img)
    text_c(d, 480, "SALVA PRA EXPLICAR", F_LBL, WHITE, alpha=seg(u, 0, 0.2))
    text_c(d, 570, "NA PRÓXIMA BOLHA", F_LBL, ACC, alpha=seg(u, 0.05, 0.25))
    text_c(d, 690, "@parecefakeereal", F_LOGO, ACC, alpha=seg(u, 0.2, 0.4))
    return img

CHUNKS = [
 ("Por que uma bolha de sabão transparente fica colorida?", "Por que uma bolha de sabão transparente fica colorida?", s0),
 ("Não é tinta. A cor vem da própria luz.", "Não é tinta. A cor vem da própria luz.", s1),
 ("A parede da bolha é uma película finíssima: água entre duas camadas de sabão.", "A parede da bolha é uma película finíssima: água entre duas camadas de sabão.", s2),
 ("A luz reflete duas vezes: na face de fora e na de dentro.", "A luz reflete duas vezes: na face de fora e na de dentro.", s3),
 ("O raio de dentro faz um caminho maior e volta fora de passo.", "O raio de dentro faz um caminho maior e volta fora de passo.", s4),
 ("Em algumas cores as ondas se somam; em outras, se cancelam.", "Em algumas cores as ondas se somam; em outras, se cancelam.", s5),
 ("E a cor que sobra depende da espessura da película.", "E a cor que sobra depende da espessura da película.", s6),
 ("O líquido escorre e evapora: a película afina e as cores giram.", "Com o tempo, o líquido escorre e evapora: a película afina, e as cores mudam e giram.", s7),
 ("No topo, ela fica mais fina que a onda da luz: tudo se cancela e surgem manchas escuras.", "No topo, ela fica mais fina que o comprimento de onda da luz: os reflexos se cancelam, e surgem manchas escuras.", s8),
 ("É sinal de que a bolha está perto de estourar.", "É sinal de que a bolha está perto de estourar.", s9),
 ("Ressalva: o ângulo de visão e a iluminação também mudam a cor.", "Ressalva: o ângulo de visão e a iluminação também mudam a cor que você vê.", s10),
 ("Salva pra explicar na próxima bolha.", "Salva pra explicar na próxima bolha.", s11),
]

if __name__ == "__main__":
    wd = os.path.join(os.environ.get("WORK_DIR", "/tmp/reelwork"), "reel9")
    note = "Animação autoral, sem escala · locução sintética"
    kw = dict(voice="M3", speed=float(os.environ.get("SPEED", "1.15")), bg_fn=soft_bg)
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        render(CHUNKS, wd, None, note, previews=[0.02, 0.1, 0.18, 0.26, 0.34, 0.43, 0.52, 0.6, 0.7, 0.78, 0.88, 0.98], **kw)
    else:
        render(CHUNKS, wd, sys.argv[1], note, **kw)
