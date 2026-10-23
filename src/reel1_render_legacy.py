import math, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, DUR = 1080, 1920, 30, 45.0
import json as _j, os as _o
WARP = _j.load(open(_o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "warp.json")))
DUR = WARP["total"]
def warp(tr):
    B, R = WARP["B"], WARP["R"]
    for i in range(len(R) - 1):
        if tr < R[i + 1]:
            return B[i] + (B[i + 1] - B[i]) * (tr - R[i]) / (R[i + 1] - R[i])
    return B[-1] - 0.001
OUT = sys.argv[1] if len(sys.argv) > 1 else "reel1.mp4"
FD = "/usr/share/fonts/opentype/inter/"
def F(w, s): return ImageFont.truetype(FD + f"Inter-{w}.otf", s)
F_HOOK = F("Black", 84); F_LBL = F("ExtraBold", 60); F_SUB = F("SemiBold", 50)
F_SMALL = F("Medium", 30); F_LOGO = F("Black", 64); F_MID = F("Bold", 44)

BG = (11, 13, 19); METAL = (168, 176, 190); METAL_D = (110, 118, 132)
OXIDE = (214, 120, 52); ACC = (255, 196, 64); WHITE = (245, 246, 248)
RED = (235, 77, 75); GREEN = (80, 205, 140); BLUE = (90, 160, 255)

def clamp(x, a=0, b=1): return max(a, min(b, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def seg(t, a, b): return ease((t - a) / (b - a))
def lerp(a, b, k): return a + (b - a) * k
def mix(c1, c2, k): return tuple(int(lerp(a, b, k)) for a, b in zip(c1, c2))

SUBS = [
 (0, 3, "Por que dois metais podem grudar no espaço só de encostar?"),
 (3, 7, "Na Terra, quase todo metal ganha uma película de óxido no contato com o ar."),
 (7, 11, "Ela funciona como uma barreira entre os átomos."),
 (11, 16, "No vácuo, se essa camada se desgasta por atrito, vibração ou impacto…"),
 (16, 21, "…e as superfícies se tocam com força, os átomos podem se ligar. É a soldagem a frio."),
 (21, 23.5, "Para engenheiros, isso é um problema real."),
 (23.5, 27, "A Agência Espacial Europeia estuda essa aderência como modo de falha de mecanismos."),
 (27, 30, "E testa quais pares de materiais são arriscados no vácuo."),
 (30, 36, "Mas não é tão simples: metal com óxido ou revestimento normalmente não gruda só de encostar."),
 (36, 42, "Agora, o projeto ASTROBEAT estuda usar esse efeito para remendar cascos de naves."),
 (42, 45, "Siga para entender a ciência por trás do que parece impossível."),
]

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def text_c(d, y, text, font, fill, maxw=920, gap=12, alpha=1.0):
    lines = wrap(d, text, font, maxw)
    asc = font.getbbox("Ág")[3]
    if alpha <= 0.01: return y + len(lines) * (asc + gap)
    for i, ln in enumerate(lines):
        x = (W - d.textlength(ln, font=font)) / 2
        d.text((x, y + i * (asc + gap)), ln, font=font, fill=fill + (int(255 * alpha),) if len(fill) == 3 else fill)
    return y + len(lines) * (asc + gap)

def subtitle(d, t):
    for a, b, s in SUBS:
        if a <= t < b:
            k = min(seg(t, a, a + 0.25), 1 - seg(t, b - 0.2, b))
            lines = wrap(d, s, F_SUB, 900)
            asc = F_SUB.getbbox("Ág")[3]; lh = asc + 14
            h = len(lines) * lh + 40; y0 = 1240
            d.rounded_rectangle((60, y0 - 20, W - 60, y0 - 20 + h), 28, fill=(0, 0, 0, int(170 * k)))
            for i, ln in enumerate(lines):
                x = (W - d.textlength(ln, font=F_SUB)) / 2
                d.text((x, y0 + i * lh), ln, font=F_SUB, fill=(255, 255, 255, int(255 * k)))

def stars(d, t):
    import random
    r = random.Random(7)
    for i in range(110):
        x, y = r.random() * W, r.random() * H
        tw = 0.5 + 0.5 * math.sin(t * 2 + i)
        c = int(60 + 90 * tw)
        d.ellipse((x, y, x + 3, y + 3), fill=(c, c, c + 20, 255))

def bar(d, x, y, w, h, oxide=0, oxide_frac=1.0, side="right"):
    d.rounded_rectangle((x, y, x + w, y + h), 14, fill=METAL, outline=METAL_D, width=4)
    for i in range(6):
        yy = y + 18 + i * (h - 36) / 5
        d.line((x + 16, yy, x + w - 16, yy), fill=(190, 198, 210), width=2)
    if oxide > 0:
        th = int(oxide)
        if side == "right":
            d.rectangle((x + w - th, y + h * (1 - oxide_frac) / 2, x + w, y + h - h * (1 - oxide_frac) / 2), fill=OXIDE)
        else:
            d.rectangle((x, y + h * (1 - oxide_frac) / 2, x + th, y + h - h * (1 - oxide_frac) / 2), fill=OXIDE)

def glow(img, cx, cy, r, strength):
    if strength <= 0: return img
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.ellipse((cx - r, cy - r, cx + r, cy + r), fill=ACC + (int(220 * strength),))
    g = g.filter(ImageFilter.GaussianBlur(r / 2.2))
    return Image.alpha_composite(img, g)

def label(d, y, text, color=ACC, k=1.0):
    text_c(d, y, text, F_LBL, color, alpha=k)

def scene1(img, d, t):  # 0–3 hook
    k = seg(t, 0, 1.6)
    gap = lerp(320, 0, k)
    bw, bh, cy = 340, 250, 820
    bar(d, W / 2 - gap / 2 - bw, cy - bh / 2, bw, bh)
    bar(d, W / 2 + gap / 2, cy - bh / 2, bw, bh)
    img = glow(img, W / 2, cy, 120, seg(t, 1.5, 1.9) * (1 - seg(t, 2.4, 3.0) * 0.5))
    d = ImageDraw.Draw(img)
    text_c(d, 300, "POR QUE METAIS", F_HOOK, WHITE)
    text_c(d, 400, "GRUDAM NO ESPAÇO?", F_HOOK, ACC)
    return img

def scene2(img, d, t):  # 3–11 oxide layer
    k = seg(t, 3, 4)
    bw, bh, cy = 380, 300, 820
    x = W / 2 - bw / 2
    bar(d, x, cy - bh / 2, bw, bh)
    # oxide shell grows
    th = 22 * seg(t, 4, 6)
    if th > 0:
        d.rounded_rectangle((x - th, cy - bh / 2 - th, x + bw + th, cy + bh / 2 + th), 18, outline=OXIDE, width=int(max(1, th)))
    # air molecules drifting in
    for i in range(14):
        a = i * 2 * math.pi / 14 + t * 0.4
        r = lerp(520, 300, seg(t, 3.5, 6)) + 20 * math.sin(t * 3 + i)
        px, py = W / 2 + r * math.cos(a), cy + r * math.sin(a) * 0.9
        d.ellipse((px - 11, py - 11, px + 11, py + 11), fill=BLUE + (int(200 * (1 - seg(t, 6, 7))),))
        d.text((px - 9, py - 16), "O", font=F_SMALL, fill=WHITE + (int(220 * (1 - seg(t, 6, 7))),))
    label(d, 300, "CAMADA DE ÓXIDO", OXIDE, seg(t, 4.5, 5.2))
    text_c(d, 390, "= um escudo entre os átomos", F_MID, WHITE, alpha=seg(t, 7, 7.6))
    return img

def lattice(d, x0, y0, cols, rows, sp, color, jitter=0, t=0):
    for i in range(cols):
        for j in range(rows):
            jx = jitter * math.sin(t * 7 + i * 1.7 + j)
            cx, cy = x0 + i * sp + jx, y0 + j * sp
            d.ellipse((cx - 20, cy - 20, cx + 20, cy + 20), fill=color)

def scene3(img, d, t):  # 11–21 cold weld
    sp, rows, cols = 64, 7, 5
    cy0 = 820 - (rows - 1) * sp / 2
    approach = seg(t, 15.5, 18.5)
    lx = lerp(150, W / 2 - cols * sp + sp / 2 - sp / 2, approach)
    rx = lerp(W - 150 - (cols - 1) * sp, W / 2 + sp / 2, approach)
    lattice(d, lx, cy0, cols, rows, sp, METAL, 3 if t < 16 else 0, t)
    lattice(d, rx, cy0, cols, rows, sp, METAL, 3 if t < 16 else 0, t)
    # oxide layer on facing surfaces, scraped away 12.5–15
    ox = 1 - seg(t, 12.5, 15)
    if ox > 0:
        xl = lx + (cols - 1) * sp + 26
        xr = rx - 26 - 18
        h = (rows - 1) * sp + 40
        d.rectangle((xl, cy0 - 20 + h * (1 - ox), xl + 18, cy0 - 20 + h), fill=OXIDE)
        d.rectangle((xr, cy0 - 20, xr + 18, cy0 - 20 + h * ox), fill=OXIDE)
        # sparks of scraping
        for i in range(8):
            if 12.5 < t < 15:
                sy = cy0 - 20 + h * (1 - ox) + 10 * math.sin(t * 30 + i)
                d.line((xl + 9, sy, xl + 9 + 40 * math.cos(i), sy - 30 * abs(math.sin(i + t * 9))), fill=ACC, width=4)
    # bonds once together
    b = seg(t, 18.3, 19.2)
    if b > 0:
        xa = lx + (cols - 1) * sp; xb = rx
        for j in range(rows):
            yy = cy0 + j * sp
            d.line((xa + 20, yy, lerp(xa + 20, xb - 20, b), yy), fill=ACC, width=8)
        img = glow(img, W / 2, 820, 160, b * (1 - seg(t, 20, 21) * 0.6))
        d = ImageDraw.Draw(img)
    text_c(d, 300, "NO VÁCUO", F_MID, WHITE, alpha=seg(t, 11, 11.6))
    text_c(d, 360, "atrito · vibração · impacto", F_MID, OXIDE, alpha=seg(t, 12, 12.6) * (1 - seg(t, 18, 18.5)))
    label(d, 360, "SOLDAGEM A FRIO", ACC, seg(t, 18.6, 19.2))
    return img

def scene4(img, d, t):  # 21–30 mechanism failure
    cx, cy = W / 2 - 110, 900
    d.rounded_rectangle((cx - 140, cy - 140, cx + 140, cy + 140), 18, fill=(70, 80, 100), outline=METAL, width=6)
    d.ellipse((cx - 50, cy - 50, cx + 50, cy + 50), outline=ACC, width=7)
    d.text((cx - 70, cy + 70), "satélite", font=F_SMALL, fill=(200, 205, 215))
    hx, hy = cx + 140, cy - 100
    attempt = seg(t, 22, 23.6)
    if t < 23.6:
        ang = lerp(-90, -35, attempt)
    else:
        ang = -35 + 5 * math.sin((t - 23.6) * 20) * math.exp(-(t - 23.6) * 1.5)
    a = math.radians(ang); L = 280
    ex, ey = hx + L * math.cos(a), hy + L * math.sin(a)
    d.line((hx, hy, ex, ey), fill=BLUE, width=46)
    ghost = math.radians(0)
    if t > 23.6:
        gx, gy = hx + L * math.cos(ghost), hy + L * math.sin(ghost)
        d.line((hx, hy, gx, gy), fill=(90, 160, 255, 70), width=46)
    d.ellipse((hx - 26, hy - 26, hx + 26, hy + 26), fill=METAL, outline=OXIDE, width=6)
    k = seg(t, 23.8, 24.3)
    if k > 0:
        d.line((hx - 46, hy - 46, hx + 46, hy + 46), fill=RED + (int(255 * k),), width=13)
        d.line((hx - 46, hy + 46, hx + 46, hy - 46), fill=RED + (int(255 * k),), width=13)
    label(d, 300, "DOBRADIÇA TRAVADA", RED, seg(t, 24, 24.6))
    text_c(d, 1130, "Aderência no vácuo: modo de falha estudado pela ESA", F_SMALL, WHITE, alpha=seg(t, 24.8, 25.4))
    k = seg(t, 26, 26.8)
    if k > 0:
        d.rounded_rectangle((120, 420, W - 120, 600), 22, fill=(25, 30, 42, int(235 * k)))
        rows = [("metal × metal nu", "alto risco", RED), ("com revestimento", "menor risco", GREEN)]
        for i, (a1, b1, c) in enumerate(rows):
            y = 448 + i * 74
            d.text((160, y), a1, font=F_MID, fill=WHITE + (int(255 * k),))
            d.text((W - 160 - d.textlength(b1, font=F_MID), y), b1, font=F_MID, fill=c + (int(255 * k),))
    return img

def scene5(img, d, t):  # 30–36 oxide prevents
    cy, bw, bh = 820, 300, 220
    p = (t - 30)
    cyc = (math.sin(p * 1.6 - math.pi / 2) + 1) / 2  # 0..1..0
    gap = lerp(260, 4, cyc)
    bar(d, W / 2 - gap / 2 - bw, cy - bh / 2, bw, bh, oxide=20, side="right")
    bar(d, W / 2 + gap / 2, cy - bh / 2, bw, bh, oxide=20, side="left")
    k = seg(t, 30.5, 31.2)
    label(d, 300, "COM ÓXIDO:", OXIDE, k)
    label(d, 380, "NÃO GRUDA", WHITE, k)
    return img

def scene6(img, d, t):  # 36–42 ASTROBEAT patch
    cx, cy = W / 2, 820
    d.rounded_rectangle((cx - 380, cy - 230, cx + 380, cy + 230), 26, fill=(64, 72, 90), outline=METAL, width=6)
    for i in range(1, 6):
        d.line((cx - 380 + i * 127, cy - 230, cx - 380 + i * 127, cy + 230), fill=(80, 90, 110), width=3)
    # hole (impact)
    d.ellipse((cx - 50, cy - 50, cx + 50, cy + 50), fill=BG)
    # patch slides in
    k = seg(t, 37, 39.2)
    px = lerp(cx + 700, cx, k)
    d.rounded_rectangle((px - 110, cy - 110, px + 110, cy + 110), 18, fill=(150, 158, 172), outline=(200, 205, 215), width=5)
    if t > 39.2:
        img = glow(img, cx, cy, 150, seg(t, 39.2, 39.8) * (1 - seg(t, 40.5, 42) * 0.7))
        d = ImageDraw.Draw(img)
    label(d, 290, "DE PROBLEMA", WHITE, seg(t, 36, 36.6))
    label(d, 370, "A FERRAMENTA", ACC, seg(t, 36.4, 37))
    text_c(d, 1090, "Projeto ASTROBEAT · ISS National Lab", F_SMALL, WHITE, alpha=seg(t, 37.5, 38))
    return img

def scene7(img, d, t):  # 42–45 outro
    k = seg(t, 42, 42.8)
    text_c(d, 640, "@parecefakeereal", F_LOGO, ACC, alpha=k)
    text_c(d, 740, "Parece fake. É real.", F_MID, WHITE, alpha=seg(t, 42.4, 43))
    return img

SCENES = [(0, 3, scene1), (3, 11, scene2), (11, 21, scene3), (21, 30, scene4),
          (30, 36, scene5), (36, 42, scene6), (42, 45.01, scene7)]

def frame(t):
    t = min(warp(t), 44.99)
    img = Image.new("RGBA", (W, H), BG + (255,))
    d = ImageDraw.Draw(img)
    stars(d, t)
    for a, b, fn in SCENES:
        if a <= t < b:
            layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ld = ImageDraw.Draw(layer)
            layer = fn(layer, ld, t)
            fade = min(seg(t, a, a + 0.3) if a > 0 else 1, 1 - seg(t, b - 0.3, b))
            if fade < 1:
                al = layer.getchannel("A").point(lambda v: int(v * fade))
                layer.putalpha(al)
            img = Image.alpha_composite(img, layer)
            break
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    subtitle(od, t)
    note = "Animação esquemática autoral, sem escala"
    od.text(((W - od.textlength(note, font=F_SMALL)) / 2, 1515), note, font=F_SMALL, fill=(170, 175, 185, 200))
    img = Image.alpha_composite(img, ov)
    return img.convert("RGB")

if __name__ == "__main__":
    if len(sys.argv) > 2:  # preview frames
        for ts in sys.argv[2:]:
            frame(float(ts)).save(f"prev_{ts}.png")
        sys.exit()
    n = int(DUR * FPS)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", "narr.wav", "-shortest",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    print("done", OUT)
