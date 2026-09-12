# -*- coding: utf-8 -*-
"""Shared page shell for the Toolpeg static site.
Every HTML file is produced from PAGE() / TOOL_PAGE(), and every tool's
metadata (label, description, About/How-it-works/FAQ copy) lives in one
TOOLS registry so nav, footer, homepage cards, category pages, related-tool
links and on-page SEO content can never drift out of sync with each other.
"""

SITE_NAME = "Toolpeg"
SITE_DOMAIN = "https://toolpegtools.vercel.app"

CATEGORY_INFO = {
    "image-tools": {"label": "Image Tools", "nav_key": "image"},
    "pdf-tools": {"label": "PDF Tools", "nav_key": "pdf"},
    "student-tools": {"label": "Student Tools", "nav_key": "student"},
    "qr-tools": {"label": "QR Tools", "nav_key": "qr"},
}

TOOLS = {
    "image-tools": [
        dict(slug="jpg-to-png.html", label="JPG to PNG", tag="Convert",
             card_desc="Turn JPG photos into transparent-ready PNG files. Drag, convert, download.",
             about="PNG uses lossless compression and supports transparency, which makes it the better choice for a logo, a screenshot with clean edges, or an image you plan to edit further without extra quality loss. This tool decodes your JPG and re-encodes it as PNG using your browser's own image engine.",
             steps=["Drop or select a JPG file.", "The image loads instantly in your browser.", "Click convert to download a PNG version."],
             faqs=[("Will converting to PNG make the file bigger?", "Usually yes — PNG is lossless, so it doesn't throw away detail the way JPG does. Expect a larger file, especially for photos with a lot of color variation."),
                   ("Does this add transparency to my JPG?", "No. JPG has no transparency to begin with, so the converted PNG will have a solid background just like the original.")]),
        dict(slug="png-to-jpg.html", label="PNG to JPG", tag="Convert",
             card_desc="Flatten PNG images to lightweight JPG — great for email and web uploads.",
             about="JPG's lossy compression makes files dramatically smaller than PNG, which helps when you're emailing a photo, uploading to a form with a size limit, or don't need pixel-perfect transparency. This tool flattens any transparent areas to white and re-encodes the image locally.",
             steps=["Drop or select a PNG file.", "Preview it right in your browser.", "Convert and download the JPG."],
             faqs=[("What happens to transparent areas?", "They're filled with white before the JPG is created, since JPG doesn't support transparency."),
                   ("Can I control the JPG quality?", "This converter uses a high-quality setting by default. For more control over file size, use the Image Compressor instead.")]),
        dict(slug="jpg-to-webp.html", label="JPG to WebP", tag="Convert",
             card_desc="Convert JPG photos to the smaller, modern WebP format.",
             about="WebP typically produces smaller files than JPG at the same visual quality, which is why most modern websites use it to speed up page loads. This tool re-encodes your JPG as WebP directly in your browser.",
             steps=["Drop or select a JPG file.", "Your browser decodes and re-encodes it as WebP.", "Download the converted file."],
             faqs=[("Will every browser open the WebP file?", "All current versions of Chrome, Firefox, Edge and Safari display WebP images natively. Very old browsers may not."),
                   ("Is WebP always smaller than JPG?", "Usually, often by 25\u201335% at similar quality, though results vary by image content.")]),
        dict(slug="webp-to-jpg.html", label="WebP to JPG", tag="Convert",
             card_desc="Convert WebP images back to widely-supported JPG.",
             about="Some older software, printers and upload forms still expect JPG rather than WebP. This tool converts a WebP image to JPG locally, so you can use it anywhere JPG is required.",
             steps=["Drop or select a WebP file.", "It's decoded right in your browser.", "Convert and download as JPG."],
             faqs=[("Does this work with animated WebP files?", "No — only the first frame of an animated WebP will be converted, since JPG doesn't support animation."),
                   ("Will I lose quality converting WebP to JPG?", "There's a small amount of additional compression loss, which is normal any time you convert between two lossy formats.")]),
        dict(slug="png-to-webp.html", label="PNG to WebP", tag="Convert",
             card_desc="Shrink PNG images by converting them to WebP.",
             about="WebP can compress PNG-style images to a noticeably smaller file size, which is ideal for speeding up a website or reducing storage use without a visible quality drop.",
             steps=["Drop or select a PNG file.", "It's re-encoded as WebP locally.", "Download the smaller WebP file."],
             faqs=[("Does WebP keep PNG's transparency?", "Yes — WebP fully supports transparency, so transparent areas are preserved."),
                   ("How much smaller will the file be?", "Typically 25\u201350% smaller than the original PNG, depending on the image.")]),
        dict(slug="image-compressor.html", label="Image Compressor", tag="Optimize",
             card_desc="Shrink photo file size with a live quality slider before you upload anywhere.",
             about="Large photos slow down websites, bounce off upload limits, and eat inbox space. This tool re-encodes your image at a quality level you choose, showing an estimated file size live so you can find the smallest file that still looks good.",
             steps=["Drop or select a JPG, PNG or WebP file.", "Drag the quality slider and watch the size estimate update.", "Download the compressed image."],
             faqs=[("Will compressing reduce image dimensions?", "No — only file size changes. Use the Image Resizer if you also want smaller pixel dimensions."),
                   ("What quality setting should I use?", "70\u201385% is a good starting point for photos — noticeably smaller with minimal visible loss. Go higher for images with fine detail or text.")]),
        dict(slug="image-resizer.html", label="Image Resizer", tag="Resize",
             card_desc="Resize images to exact pixels or a percentage, without distorting them.",
             about="Whether you need an image to fit an exact upload spec or just want a smaller file for the web, this tool resizes to precise pixel dimensions while keeping the aspect ratio locked by default.",
             steps=["Drop or select an image.", "Enter a width or height — the other updates automatically if locked.", "Resize and download."],
             faqs=[("Can I resize without keeping the aspect ratio?", "Yes — uncheck 'Lock aspect ratio' to set width and height independently, though this can stretch the image."),
                   ("Does resizing reduce file size too?", "Usually yes, since fewer pixels generally means a smaller file, though the exact amount depends on the image.")]),
        dict(slug="image-cropper.html", label="Image Cropper", tag="Edit",
             card_desc="Crop to a free rectangle or a fixed ratio like 1:1, 4:5, or 16:9.",
             about="Sometimes you just need part of an image — a square profile photo, a specific detail, or the right ratio for a platform like Instagram. Drag the crop handles to select exactly the area you want.",
             steps=["Drop or select an image.", "Drag the crop box or pick a fixed ratio like 1:1 or 16:9.", "Crop and download the result."],
             faqs=[("What ratios are available?", "Free-form, plus common presets: 1:1 square, 4:5 portrait, 16:9 widescreen, and 4:3 standard."),
                   ("Is the crop full resolution?", "Yes — the final image is rendered from the original file at full resolution, not from the smaller on-screen preview.")]),
    ],
    "pdf-tools": [
        dict(slug="pdf-to-jpg.html", label="PDF to JPG", tag="Convert",
             card_desc="Turn every page of a PDF into a downloadable JPG image.",
             about="Need to drop a PDF page into a slide deck, a chat, or a document that doesn't accept PDFs? This tool renders every page as a full-resolution JPG you can download individually or all at once.",
             steps=["Drop or select a PDF file.", "Each page renders as a JPG in your browser.", "Download individual pages or all of them at once."],
             faqs=[("Does this work with scanned PDFs?", "Yes — it renders the page exactly as it appears, whether the PDF contains real text or a scanned image."),
                   ("Is there a page limit?", "No hard limit, but very long PDFs will take longer since every page is rendered locally on your device.")]),
        dict(slug="jpg-to-pdf.html", label="JPG to PDF", tag="Convert",
             card_desc="Combine one or more JPG/PNG photos into a single PDF document.",
             about="Combine one or more photos into a single, shareable PDF — useful for submitting scanned documents, assembling a photo packet, or sending images somewhere that only accepts PDF.",
             steps=["Drop or select one or more JPG/PNG images.", "Reorder pages with the up/down arrows.", "Create the PDF and download it."],
             faqs=[("Can I control the page size?", "Yes — choose A4, US Letter, or 'Fit to image' to make each page match its photo's dimensions."),
                   ("Can I mix JPG and PNG files?", "Yes, you can combine both formats in the same PDF.")]),
        dict(slug="merge-pdf.html", label="Merge PDF", tag="Combine",
             card_desc="Stack multiple PDFs into one file, in the order you choose.",
             about="Combine multiple PDFs — chapters, scanned pages, signed forms — into a single document, in whatever order you choose.",
             steps=["Drop two or more PDF files.", "Reorder them with the up/down arrows.", "Merge and download the combined PDF."],
             faqs=[("Is there a limit to how many PDFs I can merge?", "No fixed limit — it depends on your device's memory for very large or numerous files."),
                   ("Does merging preserve the original quality?", "Yes — pages are copied directly rather than re-rendered, so there's no quality loss.")]),
        dict(slug="split-pdf.html", label="Split PDF", tag="Split",
             card_desc="Pull specific pages out of a PDF, or split it into single pages.",
             about="Pull a specific range of pages out of a longer PDF, or break every page into its own file — handy for sharing just one chapter or section without sending the whole document.",
             steps=["Drop a PDF file.", "Choose a page range, or split into single pages.", "Download the result."],
             faqs=[("Does this reduce file size?", "Splitting reduces size roughly in proportion to how many pages you extract, since it's separating pages rather than compressing them."),
                   ("Can I extract multiple separate ranges at once?", "Not in a single pass currently — run the tool again for a second range.")]),
        dict(slug="compress-pdf.html", label="Compress PDF", tag="Optimize",
             card_desc="Shrink a PDF's file size by re-rendering pages at a quality you choose.",
             about="This compressor rebuilds your PDF by rendering each page as an image at a quality and resolution you control, then reassembling them into a new PDF. It works especially well on scanned documents and image-heavy PDFs. Because pages become images, text in the output is no longer selectable or searchable — for text documents where that matters, this isn't the right tool.",
             steps=["Drop a PDF file.", "Choose a quality level.", "Compress and download the smaller PDF."],
             faqs=[("Will the text still be selectable afterward?", "No — each page becomes an image, so text can no longer be selected, searched or copied. That trade-off is what makes the size reduction possible."),
                   ("What kind of PDFs does this work best on?", "Scanned documents, photo-heavy PDFs, and anything where pages are already essentially images. For text-heavy PDFs you need to keep searchable, this isn't the right tool.")]),
    ],
    "student-tools": [
        dict(slug="gpa-calculator.html", label="GPA Calculator", tag="Grades",
             card_desc="Add courses, credits and letter grades to get your semester GPA.",
             about="Add each course you're taking with its credit hours and letter grade to see your GPA for the term update instantly, on a standard 4.0 or 4.3 scale.",
             steps=["Add a row for each course.", "Set its credit hours and letter grade.", "Your GPA updates automatically as you type."],
             faqs=[("Which grading scale should I choose?", "Most US colleges use a 4.0 scale where an A is worth 4.0. Some use a 4.3 scale where an A+ is worth 4.3 — check your institution's catalog if you're unsure."),
                   ("Does this match my school's exact GPA calculation?", "It uses the standard grade-point mapping, but some schools weight certain courses (like honors or AP classes) differently — check with your registrar for anything official.")]),
        dict(slug="cgpa-calculator.html", label="CGPA Calculator", tag="Grades",
             card_desc="Combine multiple semesters' GPA and credits into one cumulative CGPA.",
             about="Your CGPA is the credit-weighted average of every semester's GPA, not a simple average of the GPA numbers themselves. Enter each semester's GPA and total credit hours to get an accurate cumulative figure.",
             steps=["Add a row for each completed semester.", "Enter that semester's GPA and total credit hours.", "Your CGPA updates automatically."],
             faqs=[("Why can't I just average my semester GPAs?", "A simple average treats every semester equally even if credit loads differ. Weighting by credit hours gives an accurate cumulative figure when semesters carry different course loads."),
                   ("Does this handle a 4.3 scale?", "Yes — enter GPA values from whichever scale your institution uses; the calculation works the same either way.")]),
        dict(slug="percentage-calculator.html", label="Percentage Calculator", tag="Grades",
             card_desc="Work out what percent a score is, or what score hits a target percent.",
             about="Three of the most common percentage questions, in one place: what percent a score is, what score you need to hit a target percentage, and how much something changed in percentage terms.",
             steps=["Choose which type of percentage question you're answering.", "Enter your two numbers.", "Read the result instantly."],
             faqs=[("Which mode should I use to find my grade?", "'What percent is X out of Y?' — enter your score and the total possible points."),
                   ("What does percent change mean?", "It's how much a number increased or decreased, expressed as a percentage of the starting value — useful for comparing two test scores or measurements.")]),
        dict(slug="grade-calculator.html", label="Final Grade Calculator", tag="Grades",
             card_desc="Work out your overall grade from weighted categories like exams and homework.",
             about="Most courses weight different types of work differently — exams might count more than homework. Enter each category's weight and your score in it to get your overall weighted grade.",
             steps=["Add a row for each grading category (e.g. Homework, Midterm, Final).", "Enter the weight (%) and your score (%) for each.", "Your weighted final grade updates automatically."],
             faqs=[("What if my weights don't add up to 100%?", "The calculator still works — it normalizes by the total weight you've entered — but for an accurate result your weights should match your syllabus."),
                   ("Can I use this to see what I need on a final exam?", "Yes — set the final exam's category to a target score and see what overall grade results, or try a few scores to see what you'd need.")]),
        dict(slug="attendance-calculator.html", label="Attendance Calculator", tag="Grades",
             card_desc="Check your attendance percentage and how many classes you can still miss.",
             about="Many courses require a minimum attendance percentage to stay eligible for exams or credit. Enter your classes held and attended to see where you stand, and how many more you can miss before dropping below the requirement.",
             steps=["Enter total classes held and how many you attended.", "Enter your course's minimum required attendance percentage.", "See your current percentage and how many more absences you can afford."],
             faqs=[("How is 'classes I can still miss' calculated?", "It works out the most additional absences you could have — assuming you attend every other remaining class in the term — while staying at or above the required percentage. You'll need to know your course's expected total class count for an accurate answer."),
                   ("What if I'm already below the requirement?", "The calculator shows how many classes in a row you'd need to attend, with no further absences, to climb back up to the required percentage.")]),
        dict(slug="age-calculator.html", label="Age Calculator", tag="Dates",
             card_desc="Get an exact age in years, months and days from any birth date.",
             about="Get an exact age — not just years, but months and days too — from any birth date, calculated as of today or any date you choose.",
             steps=["Enter a date of birth.", "Optionally change the 'as of' date from today.", "Read the exact age in years, months and days."],
             faqs=[("Can I calculate age as of a future date?", "Yes — set the 'as of' date to any future date to see how old someone will be."),
                   ("Does it account for leap years?", "Yes — the calculation uses actual calendar dates, so leap years are handled correctly.")]),
        dict(slug="standard-deviation-calculator.html", label="Standard Deviation Calculator", tag="Statistics",
             card_desc="Enter a data set to get mean, variance and standard deviation instantly.",
             about="Enter any list of numbers to get the mean, variance and standard deviation — choose sample or population depending on whether your data is the whole group or just a subset of it.",
             steps=["Paste or type your numbers, separated by commas or spaces.", "Choose sample or population standard deviation.", "Read the mean, variance and standard deviation."],
             faqs=[("Should I use sample or population standard deviation?", "Use population if your data is the entire group you care about. Use sample if your data is a subset used to estimate a larger population — sample standard deviation is slightly larger to account for that uncertainty."),
                   ("Why is sample standard deviation always a bit higher?", "It divides by n\u22121 instead of n, which corrects for the tendency of a sample to underestimate the true spread of the full population.")]),
        dict(slug="scientific-calculator.html", label="Scientific Calculator", tag="Math",
             card_desc="A full scientific calculator with trig, logs, powers and memory keys.",
             about="A full scientific calculator for trigonometry, logarithms, powers, roots and factorials, with memory keys for multi-step calculations — all typed as a normal expression.",
             steps=["Type or tap an expression, using functions like sin(, sqrt( and constants like pi.", "Press = to evaluate.", "Use M+ / M\u2212 / MR to store and recall a running total."],
             faqs=[("Are angles in degrees or radians?", "Radians. To use degrees, convert first — for example, multiply degrees by pi/180 before applying sin, cos or tan."),
                   ("How do I enter a power or factorial?", "Use ^ for a power (e.g. 2^10) and ! for a factorial (e.g. 5!).")]),
    ],
    "qr-tools": [
        dict(slug="qr-code-generator.html", label="QR Code Generator", tag="Generate",
             card_desc="Turn a link, text or Wi-Fi login into a downloadable QR code.",
             about="Generate a QR code for a website link, a block of plain text, or a Wi-Fi network login that guests can scan to connect — then download it as a PNG to print or share.",
             steps=["Choose what you're encoding: a link, text, or Wi-Fi details.", "Adjust the size and error-correction level if needed.", "Download the QR code as a PNG."],
             faqs=[("What does 'error correction' do?", "Higher error correction lets the QR code still scan correctly even if part of it is damaged or obscured — useful if you're adding a logo on top, at the cost of a slightly denser code."),
                   ("Will the Wi-Fi QR code share my password with anyone who scans it?", "Yes — anyone who scans a Wi-Fi QR code can join the network without typing the password, so only share or print it somewhere trusted.")]),
    ],
}

TOOL_INDEX = {t["slug"]: (cat, t) for cat, items in TOOLS.items() for t in items}

NAV_ITEMS = [("home", "Home", "index.html")] + [
    (info["nav_key"], info["label"], f"{cat}/index.html") for cat, info in CATEGORY_INFO.items()
]


def _nav_html(depth, active):
    links = []
    for key, label, href in NAV_ITEMS:
        cls = ' class="active"' if key == active else ''
        links.append(f'<a href="{depth}{href}"{cls}>{label}</a>')
    return "\n      ".join(links)


def HEADER(depth, active):
    return f"""  <header class="site-header">
    <div class="wrap">
      <a href="{depth}index.html" class="logo"><span class="peg-dot"></span>{SITE_NAME}</a>
      <nav class="main-nav" aria-label="Primary">
      {_nav_html(depth, active)}
      </nav>
      <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </header>
  <div class="status-strip">
    <div class="wrap"><span class="led" aria-hidden="true"></span>Runs entirely in your browser &middot; files are never uploaded &middot; free, no sign-up</div>
  </div>
"""


def _footer_col(title, depth, items):
    rows = "\n        ".join(f'<a href="{depth}{href}">{label}</a>' for href, label in items)
    return f"""      <div>
        <h4>{title}</h4>
        {rows}
      </div>"""


def FOOTER(depth):
    company = [
        ("about.html", "About"),
        ("guides/index.html", "Guides"),
        ("contact.html", "Contact"),
        ("privacy-policy.html", "Privacy Policy"),
        ("terms.html", "Terms of Use"),
    ]
    image_col = _footer_col("Image Tools", depth, [(f"image-tools/{t['slug']}", t['label']) for t in TOOLS["image-tools"]])
    pdf_col = _footer_col("PDF Tools", depth, [(f"pdf-tools/{t['slug']}", t['label']) for t in TOOLS["pdf-tools"]])
    student_qr = [(f"student-tools/{t['slug']}", t['label']) for t in TOOLS["student-tools"]] + [(f"qr-tools/{t['slug']}", t['label']) for t in TOOLS["qr-tools"]]
    student_col = _footer_col("Student &amp; QR", depth, student_qr)
    company_col = _footer_col("Company", depth, company)
    return f"""  <footer class="site-footer">
    <div class="wrap">
      <div class="footer-grid">
        <div class="footer-about">
          <a href="{depth}index.html" class="logo"><span class="peg-dot"></span>{SITE_NAME}</a>
          <p>Free browser-based tools for images, PDFs, and everyday student calculations. No installs, no accounts, no file uploads to a server.</p>
        </div>
{image_col}
{pdf_col}
{student_col}
{company_col}
      </div>
      <div class="footer-bottom">
        <span>&copy; <span data-year></span> {SITE_NAME}. All tools run client-side in your browser.</span>
        <a href="{depth}privacy-policy.html">Privacy</a>
      </div>
    </div>
  </footer>
"""


def PAGE(title, description, canonical_path, depth, active, body, head_extra="", foot_scripts=""):
    canonical = f"{SITE_DOMAIN}/{canonical_path}"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE_DOMAIN}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Toolpeg — free image, PDF and student tools that run in your browser">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE_DOMAIN}/og-image.png">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%2314181A'/%3E%3Ccircle cx='16' cy='16' r='6' fill='%23FFB020'/%3E%3C/svg%3E">
<link rel="stylesheet" href="{depth}css/style.css">
{head_extra}</head>
<body>
{HEADER(depth, active)}
{body}
{FOOTER(depth)}
<script src="{depth}js/main.js"></script>
{foot_scripts}</body>
</html>
"""


def peg_card(href, tool):
    search_key = f"{tool['label']} {tool['tag']} {tool['card_desc']}".lower().replace('"', '&quot;')
    return f"""<a class="peg-card" href="{href}" data-name="{search_key}">
        <span class="tag">{tool['tag']}</span>
        <h3>{tool['label']}</h3>
        <p>{tool['card_desc']}</p>
        <span class="go">Open tool</span>
      </a>"""


def cards_for_category(category, href_prefix=""):
    return "\n".join(peg_card(f"{href_prefix}{t['slug']}", t) for t in TOOLS[category])


def _extra_seo_block(slug):
    category, tool = TOOL_INDEX[slug]
    steps_html = "\n            ".join(f"<li>{s}</li>" for s in tool["steps"])
    faq_html = "\n          ".join(
        f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>' for q, a in tool["faqs"]
    )
    others = [t for t in TOOLS[category] if t["slug"] != slug][:4]
    related_html = "\n".join(peg_card(t["slug"], t) for t in others)
    return f"""
  <section class="section tool-extra-section">
    <div class="wrap">
      <div class="prose" style="max-width:720px">
        <h2 style="margin-top:0">About this tool</h2>
        <p>{tool['about']}</p>
      </div>
      <div class="how-it-works">
        <h2>How it works</h2>
        <ol class="steps-list">
            {steps_html}
        </ol>
      </div>
      <div class="faq-block">
        <h2>Frequently asked questions</h2>
          {faq_html}
      </div>
      <div class="ad-slot" aria-hidden="true">
        <span>Ad space</span>
        <!-- Once you're approved by an ad network, paste its script/ad-unit tag here. -->
      </div>
    </div>
  </section>
  <section class="section" style="border-top:1px solid var(--hairline)">
    <div class="wrap">
      <div class="section-head"><h2>Related tools</h2></div>
      <div class="tool-grid">
{related_html}
      </div>
    </div>
  </section>
"""


def TOOL_PAGE(title, description, canonical_path, depth, active, body, slug, foot_scripts=""):
    """Like PAGE(), but for a tool page: appends the About/How-it-works/FAQ/
    ad-slot/related-tools block automatically, driven by TOOLS[category][slug]."""
    extra = _extra_seo_block(slug)
    return PAGE(title, description, canonical_path, depth, active, body + extra, foot_scripts=foot_scripts)


def write(path, html):
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", path)
