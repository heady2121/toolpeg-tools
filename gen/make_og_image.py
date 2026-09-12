from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630

PAPER = (243, 244, 241)
INK = (20, 24, 26)
STEEL = (91, 102, 112)
HAIRLINE = (219, 223, 217)
SIGNAL = (255, 176, 32)
CIRCUIT = (14, 138, 130)

img = Image.new("RGB", (W, H), PAPER)
draw = ImageDraw.Draw(img)

# Subtle pegboard dot-grid background (matches .pegboard CSS pattern)
step = 34
r = 2
for x in range(step, W, step):
    for y in range(step, H, step):
        draw.ellipse([x - r, y - r, x + r, y + r], fill=HAIRLINE)

# Thin top accent bar (matches the site's status-strip teal)
draw.rectangle([0, 0, W, 8], fill=CIRCUIT)

sans_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
sans = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
mono_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

f_logo = ImageFont.truetype(sans_bold, 46)
f_h1 = ImageFont.truetype(sans_bold, 68)
f_body = ImageFont.truetype(sans, 30)
f_mono = ImageFont.truetype(mono_bold, 20)

margin = 90

# Logo: peg-dot + "Toolpeg"
dot_r = 12
dot_cx, dot_cy = margin + dot_r, 120
draw.ellipse([dot_cx - dot_r, dot_cy - dot_r, dot_cx + dot_r, dot_cy + dot_r], fill=SIGNAL)
draw.ellipse([dot_cx - dot_r - 5, dot_cy - dot_r - 5, dot_cx + dot_r + 5, dot_cy + dot_r + 5], outline=(255, 210, 130), width=3)
draw.text((dot_cx + dot_r + 16, dot_cy), "Toolpeg", font=f_logo, fill=INK, anchor="lm")

# Eyebrow (mono, teal) — mirrors .eyebrow style
eyebrow = "FREE  ·  NO SIGN-UP  ·  RUNS IN YOUR BROWSER"
draw.text((margin, 210), eyebrow, font=f_mono, fill=CIRCUIT)

# H1
draw.text((margin, 250), "Tools that just work,", font=f_h1, fill=INK)
draw.text((margin, 328), "right in your browser.", font=f_h1, fill=INK)

# Body line
body = "Free image, PDF & student tools — 22 and counting."
draw.text((margin, 440), body, font=f_body, fill=STEEL)

# Bottom-right small tag row (mirrors tool-grid tag style)
tags = ["IMAGE", "PDF", "STUDENT", "QR"]
tx = margin
ty = H - 90
for t in tags:
    bbox = draw.textbbox((0, 0), t, font=f_mono)
    tw = bbox[2] - bbox[0]
    pad = 14
    box_w = tw + pad * 2
    draw.rectangle([tx, ty, tx + box_w, ty + 40], outline=HAIRLINE, width=2)
    draw.text((tx + pad, ty + 20), t, font=f_mono, fill=STEEL, anchor="lm")
    tx += box_w + 14

img.save("/home/claude/site/og-image.png", "PNG", optimize=True)
print("saved", img.size)
