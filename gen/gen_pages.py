# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from site_lib import PAGE, write, TOOLS, CATEGORY_INFO, cards_for_category

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))

SEARCH_SVG = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>"""


# ---------------------------------------------------------------- homepage
def gen_home():
    n_image, n_pdf, n_student, n_qr = (len(TOOLS[k]) for k in ["image-tools", "pdf-tools", "student-tools", "qr-tools"])
    body = f"""<main>
  <section class="hero pegboard">
    <div class="wrap">
      <span class="eyebrow">100% free &middot; no sign-up &middot; nothing leaves your device</span>
      <h1>Tools that just work,<br>right in your browser.</h1>
      <p class="lede">Toolpeg is a set of free online image, PDF and student tools &mdash; convert images, wrangle PDFs, and run the calculators students actually search for. Every tool processes your file locally, with no account, no watermark and no upload wait.</p>
      <div class="hero-actions">
        <a href="#image" class="btn btn-signal">Browse image tools</a>
        <a href="#pdf" class="btn btn-outline">Browse PDF tools</a>
      </div>
    </div>
  </section>

  <section class="section" style="padding-bottom:0">
    <div class="wrap">
      <label class="tool-search" id="tool-search">
        <span class="sr-only">Search tools</span>
        {SEARCH_SVG}
        <input type="text" id="search-input" placeholder="Search tools&hellip; e.g. compress, GPA, QR" autocomplete="off">
        <p class="no-results">No tools match that search &mdash; try a different word.</p>
      </label>
    </div>
  </section>

  <section class="section" id="image" data-section>
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

  <section class="section" id="pdf" data-section style="border-top:1px solid var(--hairline)">
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

  <section class="section" id="student" data-section style="border-top:1px solid var(--hairline)">
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

  <section class="section" id="qr" data-section style="border-top:1px solid var(--hairline)">
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

  <section class="section" style="border-top:1px solid var(--hairline)">
    <div class="wrap">
      <div class="section-head">
        <h2>Why use Toolpeg</h2>
        <span class="section-tag">how it works</span>
      </div>
      <div class="trust-grid">
        <div class="trust-item">
          <span class="num">01</span>
          <h3>Your file stays on your device</h3>
          <p>Every tool uses your browser's own engine to read, edit and export files &mdash; nothing is sent to a server, so there's no upload wait and no privacy trade-off.</p>
        </div>
        <div class="trust-item">
          <span class="num">02</span>
          <h3>No account, no watermark</h3>
          <p>Open a tool and use it. There's no sign-up wall, no daily limit, and no logo stamped on your output.</p>
        </div>
        <div class="trust-item">
          <span class="num">03</span>
          <h3>Works on any device</h3>
          <p>The layout adapts from a phone in one hand to a widescreen monitor, so the same tool works before class or at a desk.</p>
        </div>
      </div>
      <ul style="list-style:none;padding:0;margin:28px 0 0;display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px">
        <li style="font-size:13.5px;color:var(--steel)">&#10003;&nbsp; 100% free, every tool</li>
        <li style="font-size:13.5px;color:var(--steel)">&#10003;&nbsp; No registration required</li>
        <li style="font-size:13.5px;color:var(--steel)">&#10003;&nbsp; No files uploaded to a server</li>
        <li style="font-size:13.5px;color:var(--steel)">&#10003;&nbsp; Works on mobile and desktop</li>
        <li style="font-size:13.5px;color:var(--steel)">&#10003;&nbsp; No watermark on your output</li>
        <li style="font-size:13.5px;color:var(--steel)">&#10003;&nbsp; No daily usage limit</li>
      </ul>
    </div>
  </section>
</main>
"""
    script = """<script src="js/search.js"></script>\n"""
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
      <p>Toolpeg is a collection of {total} single-purpose utilities for the things people look up constantly: converting an image format, shrinking a PDF, working out a GPA. Each tool is built to do exactly one job well, load fast, and get out of the way.</p>
      <h2>How the tools work</h2>
      <p>Every image, PDF and calculator tool on this site runs entirely in your browser using standard web technology (the Canvas API for images, and open-source libraries for PDF handling). Your files are never uploaded to a server &mdash; they're processed on your own device and the output is generated locally, then offered to you as a download.</p>
      <h2>Why it's free</h2>
      <p>The site is supported by advertising rather than subscriptions, so every tool stays free and usable without an account.</p>
      <h2>Feedback</h2>
      <p>If a tool doesn't work the way you expect, or you'd like to see a new one added, the <a href="contact.html">contact page</a> is the fastest way to reach us.</p>
    </div>
  </div>
</main>
"""
    write(os.path.join(ROOT, "about.html"), PAGE(
        title="About Toolpeg — Free Browser-Based Tools",
        description="Toolpeg builds free, single-purpose image, PDF and student tools that run entirely in your browser.",
        canonical_path="about.html", depth="", active=None, body=body))


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
  <div class="wrap" style="text-align:center;padding:60px 0">
    <span class="eyebrow" style="justify-content:center">404</span>
    <h1>That page moved or never existed.</h1>
    <p class="lede" style="margin:0 auto 28px">Try the homepage, or jump straight to a category below.</p>
    <div class="hero-actions" style="justify-content:center">
      <a href="/index.html" class="btn btn-signal">Back to homepage</a>
      <a href="/image-tools/index.html" class="btn btn-outline">Image tools</a>
      <a href="/pdf-tools/index.html" class="btn btn-outline">PDF tools</a>
      <a href="/student-tools/index.html" class="btn btn-outline">Student tools</a>
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
