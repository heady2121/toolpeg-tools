# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from site_lib import PAGE, write, TOOLS, CATEGORY_INFO, CATEGORY_ICON, GITHUB_URL, TOOL_INDEX, cards_for_category, peg_card

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))

SEARCH_SVG = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>"""

POPULAR_SLUGS = [
    "scientific-calculator.html", "gpa-calculator.html", "qr-code-generator.html",
    "image-compressor.html", "compress-pdf.html", "percentage-calculator.html",
]
POPULAR_CHIPS = [
    ("student-tools/scientific-calculator.html", "Scientific Calculator"),
    ("pdf-tools/index.html", "PDF Tools"),
    ("qr-tools/qr-code-generator.html", "QR Generator"),
    ("image-tools/image-compressor.html", "Image Compressor"),
    ("student-tools/gpa-calculator.html", "GPA Calculator"),
]

GUIDE_CARDS = [
    ("jpg-vs-png.html", "Guide", "JPG vs PNG: Which Should You Use?",
     "A plain-language guide to picking the right image format, with a quick decision rule you can use every time."),
    ("compress-image-without-losing-quality.html", "Guide", "How to Compress an Image Without Losing (Much) Quality",
     "The real levers that shrink a file size — format, dimensions and quality — and the order to use them in."),
    ("how-to-calculate-gpa.html", "Guide", "How to Calculate GPA (With Formula)",
     "The credit-weighted GPA formula, a worked example, and how GPA differs from CGPA."),
]

CATEGORY_DESC = {
    "student-tools": "Calculate grades, GPA, attendance and more.",
    "image-tools": "Compress, resize, crop and convert images.",
    "pdf-tools": "Merge, split, compress and convert PDFs.",
    "qr-tools": "Generate QR codes quickly.",
}


# ---------------------------------------------------------------- homepage
def gen_home():
    n_image, n_pdf, n_student, n_qr = (len(TOOLS[k]) for k in ["image-tools", "pdf-tools", "student-tools", "qr-tools"])
    total = n_image + n_pdf + n_student + n_qr

    chips_html = "\n        ".join(f'<a href="{href}" class="chip">{label}</a>' for href, label in POPULAR_CHIPS)

    popular_cards = "\n".join(
        peg_card(f"{cat}/{slug}", TOOL_INDEX[slug][1]) for slug in POPULAR_SLUGS for cat in [TOOL_INDEX[slug][0]]
    )

    category_cards = "\n".join(f"""      <a class="category-card" href="{cat}/index.html">
        <span class="icon" aria-hidden="true">{CATEGORY_ICON[cat]}</span>
        <h3>{CATEGORY_INFO[cat]['label']}</h3>
        <p>{CATEGORY_DESC[cat]}</p>
      </a>""" for cat in ["student-tools", "image-tools", "pdf-tools", "qr-tools"])
    category_cards += f"""
      <a class="category-card" href="guides/index.html">
        <span class="icon" aria-hidden="true">\U0001F4DA</span>
        <h3>Guides</h3>
        <p>Learn how to use digital tools effectively.</p>
      </a>"""

    guide_cards_html = "\n".join(f"""      <a class="guide-card" href="guides/{slug}">
        <span class="tag">{tag}</span>
        <h3>{title}</h3>
        <p>{desc}</p>
        <span class="go">Read guide &rarr;</span>
      </a>""" for slug, tag, title, desc in GUIDE_CARDS)

    body = f"""<main>
  <section class="hero">
    <div class="wrap">
      <span class="eyebrow">Free tools for everyday digital tasks</span>
      <h1>Calculators, converters, PDF and image tools &mdash; all in one place.</h1>
      <p class="lede">{total} free utilities for images, PDFs, QR codes and student calculations. Every tool runs locally in your browser: no account, no watermark, no upload wait.</p>
      <label class="tool-search" id="tool-search">
        <span class="sr-only">Search tools</span>
        {SEARCH_SVG}
        <input type="text" id="search-input" placeholder="Search tools&hellip; e.g. compress, GPA, QR" autocomplete="off">
        <p class="no-results">No tools match that search &mdash; try a different word.</p>
      </label>
      <div class="popular-row">
        <span class="label">Popular:</span>
        {chips_html}
      </div>
    </div>
  </section>

  <section class="section" id="categories">
    <div class="wrap">
      <div class="section-head">
        <h2>Explore by category</h2>
      </div>
      <div class="category-grid">
{category_cards}
      </div>
    </div>
  </section>

  <section class="section" id="popular" data-section style="border-top:1px solid var(--border)">
    <div class="wrap">
      <div class="section-head">
        <h2>Popular tools</h2>
        <p>Good starting points if you're new here.</p>
      </div>
      <div class="popular-grid">
{popular_cards}
      </div>
    </div>
  </section>

  <section class="section" style="border-top:1px solid var(--border)">
    <div class="wrap">
      <div class="section-head">
        <h2>Explore our tools</h2>
        <span class="section-tag">{total} tools total</span>
      </div>
    </div>
  </section>

  <section class="section" id="image" data-section style="padding-top:0">
    <div class="wrap">
      <div class="section-head">
        <h2>Image tools</h2>
        <span class="section-tag">{n_image:02d} tools</span>
      </div>
      <div class="tool-grid">
{cards_for_category('image-tools', 'image-tools/')}
      </div>
    </div>
  </section>

  <section class="section" id="pdf" data-section style="border-top:1px solid var(--border)">
    <div class="wrap">
      <div class="section-head">
        <h2>PDF tools</h2>
        <span class="section-tag">{n_pdf:02d} tools</span>
      </div>
      <div class="tool-grid">
{cards_for_category('pdf-tools', 'pdf-tools/')}
      </div>
    </div>
  </section>

  <section class="section" id="student" data-section style="border-top:1px solid var(--border)">
    <div class="wrap">
      <div class="section-head">
        <h2>Student tools</h2>
        <span class="section-tag">{n_student:02d} tools</span>
      </div>
      <div class="tool-grid">
{cards_for_category('student-tools', 'student-tools/')}
      </div>
    </div>
  </section>

  <section class="section" id="qr" data-section style="border-top:1px solid var(--border)">
    <div class="wrap">
      <div class="section-head">
        <h2>QR tools</h2>
        <span class="section-tag">{n_qr:02d} tool</span>
      </div>
      <div class="tool-grid">
{cards_for_category('qr-tools', 'qr-tools/')}
      </div>
    </div>
  </section>

  <section class="section" style="border-top:1px solid var(--border)">
    <div class="wrap">
      <div class="section-head">
        <h2>Helpful guides</h2>
        <p>Short, practical explainers behind the tools.</p>
      </div>
      <div class="guide-grid">
{guide_cards_html}
      </div>
    </div>
  </section>

  <section class="section" style="border-top:1px solid var(--border)">
    <div class="wrap">
      <div class="section-head">
        <h2>Why Toolpeg</h2>
      </div>
      <div class="trust-grid">
        <div class="trust-item">
          <span class="icon" aria-hidden="true">\u26A1</span>
          <h3>Fast</h3>
          <p>Tools are designed to be simple and quick &mdash; open one and use it, no setup.</p>
        </div>
        <div class="trust-item">
          <span class="icon" aria-hidden="true">\U0001F512</span>
          <h3>Privacy-focused</h3>
          <p>Where possible, files are processed locally in your browser instead of being uploaded to a server.</p>
        </div>
        <div class="trust-item">
          <span class="icon" aria-hidden="true">\U0001F4F1</span>
          <h3>Works everywhere</h3>
          <p>A responsive experience across desktop, tablet and mobile.</p>
        </div>
        <div class="trust-item">
          <span class="icon" aria-hidden="true">\U0001F193</span>
          <h3>Free to use</h3>
          <p>Every tool listed here is free, with no sign-up required.</p>
        </div>
      </div>
    </div>
  </section>
</main>
"""
    script = """<script src="js/search.js?v=202611031215"></script>\n"""
    html = PAGE(
        title="Toolpeg — Free Image, PDF & Student Tools (No Sign-up)",
        description="Free browser-based tools: JPG/PNG/WebP converters, image compressor and resizer, merge/split/compress PDF, GPA and CGPA calculators, QR code generator, and more.",
        canonical_path="",
        depth="",
        active="home",
        body=body,
        foot_scripts=script,
    )
    write(os.path.join(ROOT, "index.html"), html)


# ---------------------------------------------------------- category index
def gen_category(folder, active, title, eyebrow, h1, lede):
    n = len(TOOLS[folder])
    body = f"""<main class="tool-shell">
  <div class="wrap">
    <p class="breadcrumb"><a href="../index.html">Home</a> / {title}</p>
    <span class="eyebrow">{eyebrow.format(n=n)}</span>
    <h1 style="margin-bottom:10px">{h1}</h1>
    <p class="lede" style="margin-bottom:32px">{lede}</p>
    <div class="tool-grid">
{cards_for_category(folder)}
    </div>
  </div>
</main>
"""
    html = PAGE(
        title=f"{title} — Free Online {title} | Toolpeg",
        description=f"{lede}",
        canonical_path=f"{folder}/",
        depth="../",
        active=active,
        body=body,
    )
    write(os.path.join(ROOT, folder, "index.html"), html)


def gen_categories():
    gen_category(
        "image-tools", "image", "Image Tools",
        "{n:02d} free tools", "Image tools",
        "Convert between JPG, PNG and WebP, compress large photos, resize to exact dimensions, or crop to a ratio &mdash; all processed locally in your browser.",
    )
    gen_category(
        "pdf-tools", "pdf", "PDF Tools",
        "{n:02d} free tools", "PDF tools",
        "Turn PDFs into images, images into PDFs, merge or split documents, and compress oversized files without installing anything.",
    )
    gen_category(
        "student-tools", "student", "Student Tools",
        "{n:02d} free calculators", "Student tools",
        "GPA, CGPA, percentage, final grade and attendance calculators, plus age, standard deviation and a full scientific calculator &mdash; built for coursework.",
    )
    gen_category(
        "qr-tools", "qr", "QR Tools",
        "{n:02d} free tool", "QR tools",
        "Generate a downloadable QR code for a link, message or Wi-Fi network in seconds.",
    )


# --------------------------------------------------------------- info pages
def gen_about():
    total = sum(len(v) for v in TOOLS.values())
    body = f"""<main class="tool-shell">
  <div class="wrap">
    <p class="breadcrumb"><a href="index.html">Home</a> / About</p>
    <span class="eyebrow">About Toolpeg</span>
    <h1>Small tools, built to be used, not signed up for.</h1>
    <div class="prose">
      <h2 style="margin-top:0">What Toolpeg is</h2>
      <p>Toolpeg is a collection of {total} single-purpose utilities for the things people look up constantly: converting an image format, shrinking a PDF, working out a GPA. Each tool is built to do exactly one job well, load fast, and get out of the way.</p>
      <h2>Why it was created</h2>
      <p>Toolpeg started as a personal project &mdash; a way to build something genuinely useful end-to-end, from picking a tool people actually search for, to shipping a working version of it. It's also a portfolio project: every tool here reflects real, working code, not a mockup.</p>
      <h2>What you can do here</h2>
      <p>Convert and compress images, merge or split PDFs, generate a QR code, or run the calculators students use every semester (GPA, CGPA, attendance, grades) &mdash; all without creating an account or installing anything.</p>
      <h2>How the tools work</h2>
      <p>Every image, PDF and calculator tool on this site runs entirely in your browser using standard web technology (the Canvas API for images, and open-source libraries for PDF handling). Your files are never uploaded to a server &mdash; they're processed on your own device and the output is generated locally, then offered to you as a download.</p>
      <h2>Core principles</h2>
      <ul>
        <li>One tool, one job &mdash; no bloated all-in-one dashboards.</li>
        <li>No account required to use anything.</li>
        <li>Process files locally wherever that's technically possible.</li>
        <li>No fake statistics, no fake reviews, no invented team.</li>
      </ul>
      <h2>About the developer</h2>
      <p>Toolpeg is built and maintained by <strong>Abdul Hadi</strong>, a computer science student and web developer. It's an actively developed personal project &mdash; the <a href="{GITHUB_URL}" target="_blank" rel="noopener">source is on GitHub</a> if you're curious how it's built.</p>
      <h2>Get started</h2>
      <p>Head back to the <a href="index.html">homepage</a> to browse every tool, or jump straight to <a href="image-tools/index.html">Image Tools</a>, <a href="pdf-tools/index.html">PDF Tools</a>, or <a href="student-tools/index.html">Student Tools</a>.</p>
    </div>
  </div>
</main>
"""
    write(os.path.join(ROOT, "about.html"), PAGE(
        title="About Toolpeg — Free Browser-Based Tools",
        description="Toolpeg builds free, single-purpose image, PDF and student tools that run entirely in your browser.",
        canonical_path="about.html", depth="", active="about", body=body))


def gen_contact(email="youraddress@gmail.com"):
    body = f"""<main class="tool-shell">
  <div class="wrap">
    <p class="breadcrumb"><a href="index.html">Home</a> / Contact</p>
    <span class="eyebrow">Get in touch</span>
    <h1>Contact</h1>
    <div class="prose">
      <p>Spotted a bug, have a tool request, or want to talk about advertising? Reach out any time.</p>
      <p><strong>Email:</strong> <a href="mailto:{email}">{email}</a></p>
    </div>
  </div>
</main>
"""
    write(os.path.join(ROOT, "contact.html"), PAGE(
        title="Contact — Toolpeg",
        description="Get in touch with the Toolpeg team about bugs, feature requests or advertising.",
        canonical_path="contact.html", depth="", active=None, body=body))


def gen_privacy():
    from datetime import date
    updated = date.today().strftime("%B %-d, %Y")
    body = f"""<main class="tool-shell">
  <div class="wrap">
    <p class="breadcrumb"><a href="index.html">Home</a> / Privacy Policy</p>
    <span class="eyebrow">Legal</span>
    <h1>Privacy Policy</h1>
    <div class="prose">
      <p><em>Last updated: {updated}.</em></p>
      <h2>Files you process</h2>
      <p>The image, PDF and calculator tools on this site run entirely in your browser. Files you open in a tool are read and processed on your own device using JavaScript, and are never transmitted to our servers or stored by us.</p>
      <h2>Information we collect</h2>
      <p>Like most websites, we may use cookies and similar technology, third-party analytics, and advertising partners to understand aggregate traffic and to display ads. These services may collect information such as your IP address, browser type, and pages visited.</p>
      <h2>Advertising</h2>
      <p>This site may show ads served by third-party advertising networks, including header-bidding networks that run a real-time auction among multiple ad buyers for each ad slot. Those networks and buyers may use cookies, device identifiers, or similar technology to personalize the ads you see, and may collect information such as approximate location or interest data for that purpose. You can control cookie preferences through your browser settings.</p>
      <h2>Third-party links</h2>
      <p>This site may link to third-party sites. We aren't responsible for the content or privacy practices of those sites.</p>
      <h2>Your choices</h2>
      <p>You can clear cookies and site data at any time through your browser settings, and most browsers let you block third-party cookies entirely.</p>
      <h2>Contact</h2>
      <p>Questions about this policy can be sent to the address on the <a href="contact.html">contact page</a>.</p>
    </div>
  </div>
</main>
"""
    write(os.path.join(ROOT, "privacy-policy.html"), PAGE(
        title="Privacy Policy — Toolpeg",
        description="How Toolpeg handles your files and data. Files are processed locally in your browser and are never uploaded.",
        canonical_path="privacy-policy.html", depth="", active=None, body=body))


def gen_terms():
    from datetime import date
    updated = date.today().strftime("%B %-d, %Y")
    body = f"""<main class="tool-shell">
  <div class="wrap">
    <p class="breadcrumb"><a href="index.html">Home</a> / Terms of Use</p>
    <span class="eyebrow">Legal</span>
    <h1>Terms of Use</h1>
    <div class="prose">
      <p><em>Last updated: {updated}.</em></p>
      <h2>Using the tools</h2>
      <p>These tools are provided free of charge, as-is, for personal and professional use. You're responsible for the files you process and the accuracy of any calculator result you rely on.</p>
      <h2>No warranty</h2>
      <p>The tools are offered without warranty of any kind. We aim for accuracy, but conversions, compressions and calculations should be checked before you rely on them for anything important, such as academic or financial decisions.</p>
      <h2>Acceptable use</h2>
      <p>Don't use these tools to process content you don't have the right to use, or in a way that violates applicable law.</p>
      <h2>Changes</h2>
      <p>Tools and pages may be added, changed or removed at any time without notice.</p>
      <h2>Contact</h2>
      <p>Questions can be sent to the address on the <a href="contact.html">contact page</a>.</p>
    </div>
  </div>
</main>
"""
    write(os.path.join(ROOT, "terms.html"), PAGE(
        title="Terms of Use — Toolpeg",
        description="Terms of use for Toolpeg's free image, PDF and student calculator tools.",
        canonical_path="terms.html", depth="", active=None, body=body))


def gen_404():
    body = """<main class="tool-shell">
  <div class="wrap">
    <div class="error-page">
      <span class="code">404</span>
      <h1>Oops! This tool could not be found.</h1>
      <p class="lede" style="margin:0 auto">The page you're looking for may have moved or no longer exists.</p>
      <div class="actions">
        <a href="/index.html" class="btn btn-primary">Back to Home</a>
        <a href="/index.html#categories" class="btn btn-outline">Explore Tools</a>
      </div>
    </div>
  </div>
</main>
"""
    write(os.path.join(ROOT, "404.html"), PAGE(
        title="Page not found — Toolpeg",
        description="This page couldn't be found. Browse Toolpeg's free image, PDF and student tools instead.",
        canonical_path="404.html", depth="", active=None, body=body))


if __name__ == "__main__":
    gen_home()
    gen_categories()
    gen_about()
    gen_contact(email="hadiabdul7291@gmail.com")
    gen_privacy()
    gen_terms()
    gen_404()
