# Toolpeg

Free, browser-based tools for images, PDFs, QR codes and everyday student calculations — no sign-up, no file uploads, no watermark.

**Live site:** https://toolpegtools.vercel.app/

## What's here

- **Image tools** — JPG↔PNG, JPG/PNG↔WebP, compressor, resizer, cropper
- **PDF tools** — PDF→JPG, JPG→PDF, merge, split, compress
- **Student tools** — GPA, CGPA, percentage, final grade, attendance, age, standard deviation, and a full scientific calculator
- **QR tools** — QR code generator (link / text / Wi-Fi)
- **Guides** — a few short articles supporting the tools above

Every tool runs entirely client-side: file conversion and compression use the browser's own Canvas API and a small set of open-source libraries (`pdf.js`, `pdf-lib`, `jsPDF`, `qrcodejs`) loaded from a CDN. Nothing is uploaded to a server.

## Tech stack

Plain HTML, CSS and JavaScript. No framework, no build step, no bundler. The site is static and can be hosted anywhere (currently on Vercel).

## Project structure

```
toolpeg-website/
├── css/style.css         # design system (light + dark mode via CSS variables)
├── js/
│   ├── main.js            # nav drawer, dark-mode toggle, footer year
│   ├── search.js          # homepage tool search/filter
│   └── file-utils.js       # shared helpers for the image/PDF tools
├── gen/                   # Python scripts that generate every HTML page
│   └── site_lib.py         # shared header/footer/card templates + tool registry
├── image-tools/, pdf-tools/, student-tools/, qr-tools/   # tool pages
├── guides/                # supporting articles
├── index.html, about.html, contact.html, privacy-policy.html, terms.html, 404.html
├── sitemap.xml, robots.txt
└── og-image.png           # social-share preview image
```

## Regenerating the site

The HTML pages aren't hand-written — they're produced by the Python scripts in `gen/`, so header, footer, navigation and per-tool SEO content (About/FAQ/related tools) stay consistent across every page. To rebuild everything after editing `gen/site_lib.py` or any `gen/gen_*.py` file:

```bash
cd gen
python3 gen_pages.py
python3 gen_image_tools.py
python3 gen_pdf_tools.py
python3 gen_student_tools.py
python3 gen_qr_tools.py
python3 gen_guides.py
```

This overwrites the HTML files in place. There's no `npm install` or dev server required to run the site itself — it's static files you can open directly or deploy as-is.

## Status

Actively developed personal/portfolio project. Not affiliated with any company; there's no user account system, no backend, and no data collection beyond standard analytics/ad-network cookies (see the privacy policy).

## License

No license file yet — all rights reserved by default until one is added.
