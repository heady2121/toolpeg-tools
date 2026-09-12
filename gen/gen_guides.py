# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from site_lib import PAGE, write

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
FOLDER = "guides"
DEPTH = "../"

GUIDES = [
    ("jpg-vs-png.html", "Guide", "JPG vs PNG: Which Should You Use?",
     "A plain-language guide to picking the right image format, with a quick decision rule you can use every time."),
    ("compress-image-without-losing-quality.html", "Guide", "How to Compress an Image Without Losing (Much) Quality",
     "The real levers that shrink a file size — format, dimensions and quality — and the order to use them in."),
    ("how-to-calculate-gpa.html", "Guide", "How to Calculate GPA (With Formula)",
     "The credit-weighted GPA formula, a worked example, and how GPA differs from CGPA."),
]


def breadcrumb(title):
    return f'<p class="breadcrumb"><a href="../index.html">Home</a> / <a href="index.html">Guides</a> / {title}</p>'


def gen_index():
    cards = "\n".join(f"""      <a class="guide-card" href="{slug}">
        <span class="tag">{tag}</span>
        <h3>{title}</h3>
        <p>{desc}</p>
      </a>""" for slug, tag, title, desc in GUIDES)
    body = f"""<main class="tool-shell">
  <div class="wrap">
    <p class="breadcrumb"><a href="../index.html">Home</a> / Guides</p>
    <span class="eyebrow">Guides</span>
    <h1 style="margin-bottom:10px">Short, practical guides</h1>
    <p class="lede" style="margin-bottom:32px">A few plain-language explainers behind the tools &mdash; no fluff, just what actually helps you decide.</p>
    <div class="guide-grid">
{cards}
    </div>
  </div>
</main>
"""
    write(os.path.join(ROOT, FOLDER, "index.html"), PAGE(
        title="Guides — Toolpeg",
        description="Short, practical guides on image formats, compression and GPA calculation, written to support Toolpeg's free tools.",
        canonical_path=f"{FOLDER}/", depth=DEPTH, active=None, body=body))


def gen_jpg_vs_png():
    slug, tag, title, desc = GUIDES[0]
    body = f"""<main class="tool-shell">
  <div class="wrap">
    {breadcrumb(title)}
    <article class="prose">
      <span class="eyebrow">{tag}</span>
      <h1>{title}</h1>
      <p class="byline">6 min read</p>

      <p>JPG and PNG are the two formats you'll run into constantly, and picking the wrong one either bloats your file size or wrecks the quality of what you're trying to share. The good news: the decision usually comes down to one question.</p>

      <h2>The one question that decides it</h2>
      <p><strong>Does the image need transparency, or is it mostly flat colors and sharp edges (like a logo, screenshot, or diagram)?</strong> If yes, use PNG. If it's a photo, use JPG.</p>

      <h2>How JPG works</h2>
      <p>JPG uses lossy compression — it throws away some image data to make the file dramatically smaller, in a way that's hard to notice on photos with lots of natural color variation. That's exactly what photos are, which is why JPG is the standard format for photography. The trade-off is that JPG has no transparency and can show visible artifacts around sharp edges or text at high compression.</p>

      <h2>How PNG works</h2>
      <p>PNG uses lossless compression — nothing is thrown away, so the image looks identical to the original no matter how many times you re-save it. PNG also supports transparency, which JPG simply can't do. The cost is file size: PNG files are usually much larger than JPG for the same photo, especially anything with a lot of texture or color variation.</p>

      <h2>Quick decision guide</h2>
      <p>Use <strong>JPG</strong> for: photos, anything you're emailing or uploading where file size matters, and images that don't need a transparent background.</p>
      <p>Use <strong>PNG</strong> for: logos, icons, screenshots, diagrams, text-heavy graphics, and anything that needs a transparent background.</p>

      <h2>What about WebP?</h2>
      <p>WebP is a newer format that can do both — lossy compression like JPG, or lossless with transparency like PNG — usually at a smaller file size than either. Nearly every modern browser supports it. If you're publishing to the web and don't need maximum compatibility with very old software, WebP is often the better default.</p>

      <h2>Try it</h2>
      <p>Convert between formats directly in your browser: <a href="../image-tools/jpg-to-png.html">JPG to PNG</a>, <a href="../image-tools/png-to-jpg.html">PNG to JPG</a>, or <a href="../image-tools/jpg-to-webp.html">JPG to WebP</a>.</p>
    </article>
  </div>
</main>
"""
    write(os.path.join(ROOT, FOLDER, slug), PAGE(
        title=f"{title} | Toolpeg Guides",
        description=desc,
        canonical_path=f"{FOLDER}/{slug}", depth=DEPTH, active=None, body=body))


def gen_compress_guide():
    slug, tag, title, desc = GUIDES[1]
    body = f"""<main class="tool-shell">
  <div class="wrap">
    {breadcrumb(title)}
    <article class="prose">
      <span class="eyebrow">{tag}</span>
      <h1>{title}</h1>
      <p class="byline">7 min read</p>

      <p>"Compress the image" usually means one thing to most people — drag a quality slider down — but there are actually three separate levers, and using them in the right order makes a much bigger difference than the slider alone.</p>

      <h2>1. Pick the right format first</h2>
      <p>Before touching quality at all, format is usually the biggest lever. A photo saved as PNG can be 5&ndash;10&times; larger than the same photo saved as JPG or WebP, for no visible quality benefit — PNG's lossless compression is wasted on photographic detail it can't meaningfully compress. If your image is a photo and it's currently a PNG, converting it to JPG or WebP first will usually shrink it more than any quality slider will.</p>

      <h2>2. Resize before you compress</h2>
      <p>This is the step people skip. A photo straight off a modern phone camera is often 3000&ndash;4000 pixels wide — far larger than it'll ever be displayed on a screen or in a document. Cutting the pixel dimensions in half roughly cuts the file size to a quarter, with no visible quality loss if you're not displaying it at full size. Resize to roughly the dimensions you'll actually use, then compress.</p>

      <h2>3. Then adjust quality</h2>
      <p>Once the format and dimensions are right, the quality slider is for fine-tuning. For photos, 70&ndash;85% quality is usually the sweet spot — noticeably smaller than 100%, with a quality loss that's hard to spot unless you're pixel-peeping. Below about 50%, compression artifacts (blocky patches, especially around sharp edges) start to become visible.</p>

      <h2>A simple workflow</h2>
      <p>For a typical photo you want to shrink: convert to JPG or WebP if it isn't already &rarr; resize to the dimensions you'll actually display it at &rarr; compress at 70&ndash;85% quality. Doing all three, in that order, usually gets a far smaller file than adjusting quality alone.</p>

      <h2>Try it</h2>
      <p>Toolpeg's <a href="../image-tools/image-resizer.html">Image Resizer</a> and <a href="../image-tools/image-compressor.html">Image Compressor</a> handle steps 2 and 3, with a live file-size estimate so you can see the trade-off as you go.</p>
    </article>
  </div>
</main>
"""
    write(os.path.join(ROOT, FOLDER, slug), PAGE(
        title=f"{title} | Toolpeg Guides",
        description=desc,
        canonical_path=f"{FOLDER}/{slug}", depth=DEPTH, active=None, body=body))


def gen_gpa_guide():
    slug, tag, title, desc = GUIDES[2]
    body = f"""<main class="tool-shell">
  <div class="wrap">
    {breadcrumb(title)}
    <article class="prose">
      <span class="eyebrow">{tag}</span>
      <h1>{title}</h1>
      <p class="byline">5 min read</p>

      <p>GPA looks like it should be a simple average of your grades, but it isn't quite — it's weighted by how many credit hours each course was worth. Here's the actual formula, and why it matters.</p>

      <h2>The formula</h2>
      <p>For each course, multiply the grade points (A = 4.0, B = 3.0, and so on) by the course's credit hours to get that course's <em>quality points</em>. Add up the quality points for every course, then divide by the total credit hours:</p>
      <p><strong>GPA = (sum of grade points &times; credit hours) &divide; (sum of credit hours)</strong></p>

      <h2>A worked example</h2>
      <p>Say you took three courses in a semester: a 4-credit course with an A (4.0), a 3-credit course with a B+ (3.3), and a 3-credit course with a B (3.0).</p>
      <p>Quality points: (4.0 &times; 4) + (3.3 &times; 3) + (3.0 &times; 3) = 16.0 + 9.9 + 9.0 = 34.9</p>
      <p>Total credits: 4 + 3 + 3 = 10</p>
      <p>GPA = 34.9 &divide; 10 = <strong>3.49</strong></p>
      <p>Notice the 4-credit A pulls more weight than either 3-credit course — that's the point of weighting by credit hours instead of just averaging the three grade points (which would give a slightly different 3.43).</p>

      <h2>4.0 scale vs 4.3 scale</h2>
      <p>Most US institutions use a 4.0 scale, where a straight A is the maximum at 4.0. Some use a 4.3 scale, where an A+ is worth 4.3 and a regular A is worth 4.0. Check your school's academic catalog if you're not sure which one applies to you — it changes the math for any course graded A+.</p>

      <h2>GPA vs CGPA</h2>
      <p>GPA typically refers to a single term or semester. CGPA (cumulative GPA) combines every semester you've completed — but importantly, it's <em>also</em> weighted by credit hours, not a flat average of your semester GPAs. A semester where you took more credit hours counts for more in your CGPA than a semester where you took fewer, even if the GPA numbers themselves look similar.</p>

      <h2>Try it</h2>
      <p>Enter your courses and Toolpeg's <a href="../student-tools/gpa-calculator.html">GPA Calculator</a> does this math for you automatically — or use the <a href="../student-tools/cgpa-calculator.html">CGPA Calculator</a> to combine multiple semesters.</p>
    </article>
  </div>
</main>
"""
    write(os.path.join(ROOT, FOLDER, slug), PAGE(
        title=f"{title} | Toolpeg Guides",
        description=desc,
        canonical_path=f"{FOLDER}/{slug}", depth=DEPTH, active=None, body=body))


if __name__ == "__main__":
    gen_index()
    gen_jpg_vs_png()
    gen_compress_guide()
    gen_gpa_guide()
