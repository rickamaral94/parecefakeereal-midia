"""Motor de renderização de Reels do @parecefakeereal.
Cada Reel define CHUNKS = [(legenda, texto_tts, funcao_cena), ...].
A narração é sintetizada por trecho; cada cena recebe u ∈ [0,1] do seu trecho."""
import math, subprocess, json, wave, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
FD = "/usr/share/fonts/opentype/inter/"
def F(w, s): return ImageFont.truetype(FD + f"Inter-{w}.otf", s)
F_HOOK = F("Black", 84); F_LBL = F("ExtraBold", 60); F_SUB = F("SemiBold", 50)
F_SMALL = F("Medium", 30); F_LOGO = F("Black", 64); F_MID = F("Bold", 44); F_BIG = F("Black", 120)

BG = (11, 13, 19); METAL = (168, 176, 190); METAL_D = (110, 118, 132)
OXIDE = (214, 120, 52); ACC = (255, 196, 64); WHITE = (245, 246, 248)
RED = (235, 77, 75); GREEN = (80, 205, 140); BLUE = (90, 160, 255)
LEAF = (88, 178, 98); LEAF_D = (52, 120, 64); SOIL = (110, 76, 52); TOMATO = (226, 72, 52)
GRAY = (130, 136, 148)

TTS_DIR = os.environ.get("TTS_DIR", "/tmp/tts")
VOICE = "vits-piper-pt_BR-faber-medium/pt_BR-faber-medium.onnx"

def clamp(x, a=0, b=1): return max(a, min(b, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def seg(u, a, b): return ease((u - a) / (b - a))
def lerp(a, b, k): return a + (b - a) * k

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def text_c(d, y, text, font, fill, maxw=920, gap=12, alpha=1.0, x=None):
    lines = wrap(d, text, font, maxw)
    asc = font.getbbox("Ág")[3]
    if alpha <= 0.01: return y + len(lines) * (asc + gap)
    for i, ln in enumerate(lines):
        xx = (W - d.textlength(ln, font=font)) / 2 if x is None else x - d.textlength(ln, font=font) / 2
        d.text((xx, y + i * (asc + gap)), ln, font=font, fill=tuple(fill[:3]) + (int(255 * alpha),))
    return y + len(lines) * (asc + gap)

def label(d, y, text, color=ACC, k=1.0): text_c(d, y, text, F_LBL, color, alpha=k)

def glow(img, cx, cy, r, strength, color=ACC):
    if strength <= 0.01: return img
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.ellipse((cx - r, cy - r, cx + r, cy + r), fill=color + (int(220 * strength),))
    g = g.filter(ImageFilter.GaussianBlur(r / 2.2))
    return Image.alpha_composite(img, g)

def stars(d, t, n=110):
    import random
    r = random.Random(7)
    for i in range(n):
        x, y = r.random() * W, r.random() * H
        c = int(60 + 90 * (0.5 + 0.5 * math.sin(t * 2 + i)))
        d.ellipse((x, y, x + 3, y + 3), fill=(c, c, c + 20, 255))

def subtitle(d, text, k):
    if k <= 0.01: return 1460
    lines = wrap(d, text, F_SUB, 900)
    asc = F_SUB.getbbox("Ág")[3]; lh = asc + 14
    h = len(lines) * lh + 40; y0 = 1240
    d.rounded_rectangle((60, y0 - 20, W - 60, y0 - 20 + h), 28, fill=(0, 0, 0, int(170 * k)))
    for i, ln in enumerate(lines):
        x = (W - d.textlength(ln, font=F_SUB)) / 2
        d.text((x, y0 + i * lh), ln, font=F_SUB, fill=(255, 255, 255, int(255 * k)))
    return y0 - 20 + h

def synth(chunks, workdir, length_scale=1.05):
    durs = []
    for i, ch in enumerate(chunks):
        out = os.path.join(workdir, f"c{i}.wav")
        subprocess.run([os.path.join(TTS_DIR, "piper/piper"), "-m", os.path.join(TTS_DIR, VOICE),
                        "--espeak_data", os.path.join(TTS_DIR, "piper/espeak-ng-data"),
                        "--length_scale", str(length_scale), "--sentence_silence", "0.1", "-f", out],
                       input=ch[1].encode(), capture_output=True, check=True)
        w = wave.open(out); durs.append(w.getnframes() / w.getframerate()); w.close()
    return durs

def build_audio(workdir, durs, gap=0.3, start=0.15, tail=0.7):
    R, t, starts = [0.0], start, []
    for d in durs:
        starts.append(t); t += d + gap; R.append(t)
    R[-1] = t + tail; total = R[-1]
    sr = 22050; n = int(total * sr)
    mix = np.zeros(n + sr)
    for i, s in enumerate(starts):
        w = wave.open(os.path.join(workdir, f"c{i}.wav"))
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
        k = int(s * sr); mix[k:k + len(a)] += a
    tt = np.arange(len(mix)) / sr
    pad = sum(np.sin(2 * np.pi * f * tt) for f in (110, 164.8, 220)) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.1 * tt)) * 0.012
    mix += pad * np.clip(tt / 1.5, 0, 1) * np.clip((total - tt) / 1.5, 0, 1)
    mix = (mix / max(1, np.abs(mix).max() * 1.05))[:n]
    w = wave.open(os.path.join(workdir, "narr.wav"), "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((mix * 32767).astype(np.int16).tobytes()); w.close()
    return R, total

def make_frame(chunks, R, t, note, bg_fn=None):
    img = Image.new("RGBA", (W, H), BG + (255,))
    d = ImageDraw.Draw(img)
    (bg_fn or stars)(d, t)
    i = max(0, min(len(chunks) - 1, next((j for j in range(len(R) - 1) if t < R[j + 1]), len(chunks) - 1)))
    a, b = R[i], R[i + 1]
    u = clamp((t - a) / (b - a))
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer = chunks[i][2](layer, ImageDraw.Draw(layer), u, t)
    fade = min(seg(t, a, a + 0.25) if i > 0 else 1, 1 - seg(t, b - 0.2, b) if i < len(chunks) - 1 else 1)
    if fade < 1:
        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * fade)))
    img = Image.alpha_composite(img, layer)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    k = min(seg(t, a, a + 0.2) if i > 0 else 1, 1 - seg(t, b - 0.15, b) if i < len(chunks) - 1 else 1)
    bottom = max(1460, subtitle(od, chunks[i][0], k) or 1460)
    od.text(((W - od.textlength(note, font=F_SMALL)) / 2, bottom + 18), note, font=F_SMALL, fill=(170, 175, 185, 200))
    return Image.alpha_composite(img, ov).convert("RGB")

def render(chunks, workdir, out, note, previews=None, bg_fn=None):
    os.makedirs(workdir, exist_ok=True)
    durs = synth(chunks, workdir)
    R, total = build_audio(workdir, durs)
    json.dump({"R": R, "total": total}, open(os.path.join(workdir, "timeline.json"), "w"))
    if previews is not None:
        ims = []
        for f in previews:
            ims.append(make_frame(chunks, R, f * total, note, bg_fn).resize((270, 480)))
        sheet = Image.new("RGB", (270 * min(6, len(ims)), 480 * ((len(ims) + 5) // 6)))
        for k, im in enumerate(ims): sheet.paste(im, ((k % 6) * 270, (k // 6) * 480))
        sheet.save(os.path.join(workdir, "sheet.png"))
        print("total", round(total, 2)); return
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", os.path.join(workdir, "narr.wav"), "-shortest",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", out],
        stdin=subprocess.PIPE)
    for n in range(int(total * FPS)):
        p.stdin.write(make_frame(chunks, R, n / FPS, note, bg_fn).tobytes())
    p.stdin.close(); p.wait()
    print("done", out, round(total, 2))
