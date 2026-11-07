# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from site_lib import PAGE, TOOL_PAGE, write

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
FOLDER = "pdf-tools"
DEPTH = "../"

DZ_SVG = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12"/><path d="M7 8l5-5 5 5"/><path d="M4 17v2a2 2 0 002 2h12a2 2 0 002-2v-2"/></svg>"""

PDFJS = '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>\n<script>if(window["pdfjsLib"]){pdfjsLib.GlobalWorkerOptions.workerSrc="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";}</script>'
JSPDF = '<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>'
PDFLIB = '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf-lib/1.17.1/pdf-lib.min.js"></script>'


def breadcrumb(tool_label):
    return f'<p class="breadcrumb"><a href="../index.html">Home</a> / <a href="index.html">PDF Tools</a> / {tool_label}</p>'


def tool_head(tag, title, desc):
    return f"""<span class="tag">{tag}</span>
    <h1>{title}</h1>
    <p>{desc}</p>"""


# ------------------------------------------------------------- PDF to JPG
def gen_pdf_to_jpg():
    slug = "pdf-to-jpg.html"
    body = f"""<main class="tool-shell">
  <div class="wrap">
    {breadcrumb('PDF to JPG')}
    <div class="tool-head">
      {tool_head('Convert', 'PDF to JPG', 'Turn every page of a PDF into a downloadable JPG image, rendered locally in your browser.')}
    </div>
    <div class="dropzone" id="dz" tabindex="0" role="button" aria-label="Upload PDF">
      {DZ_SVG}
      <h3>Drop a PDF here, or click to browse</h3>
      <p>PDF &middot; processed on your device</p>
    </div>
    <input type="file" id="file-input" accept="application/pdf" hidden>
    <div id="error" class="error-box"></div>
    <div id="status" style="display:none;margin-top:18px">
      <div class="progress"><i id="bar"></i></div>
      <p class="note" id="status-text"></p>
    </div>
    <div id="results" class="tool-grid" style="margin-top:20px"></div>
    <div id="download-all-wrap" style="display:none;margin-top:16px">
      <button class="btn btn-primary" id="download-all">Download all as JPGs</button>
    </div>
  </div>
</main>
"""
    script = f"""{PDFJS}
<script src="../js/file-utils.js?v=202611031215"></script>
<script>
(function(){{
  const dz = document.getElementById('dz');
  const input = document.getElementById('file-input');
  const err = document.getElementById('error');
  const status = document.getElementById('status');
  const bar = document.getElementById('bar');
  const statusText = document.getElementById('status-text');
  const results = document.getElementById('results');
  const dlAllWrap = document.getElementById('download-all-wrap');
  const dlAll = document.getElementById('download-all');
  let pageBlobs = [];

  setupDropzone(dz, input, async (files) => {{
    hideError(err);
    const file = files[0];
    if (file.type !== 'application/pdf') {{ showError(err, 'Please choose a PDF file.'); return; }}
    if (!window.pdfjsLib) {{ showError(err, "Couldn't load the PDF engine. Check your connection and try again."); return; }}
    results.innerHTML = '';
    pageBlobs = [];
    dlAllWrap.style.display = 'none';
    status.style.display = 'block';
    statusText.textContent = 'Reading PDF\u2026';
    bar.style.width = '5%';
    try {{
      const buf = await file.arrayBuffer();
      const pdf = await pdfjsLib.getDocument({{ data: buf }}).promise;
      const baseName = stripExt(file.name);
      for (let i = 1; i <= pdf.numPages; i++) {{
        statusText.textContent = 'Rendering page ' + i + ' of ' + pdf.numPages + '\u2026';
        bar.style.width = Math.round((i / pdf.numPages) * 100) + '%';
        const page = await pdf.getPage(i);
        const viewport = page.getViewport({{ scale: 2 }});
        const canvas = document.createElement('canvas');
        canvas.width = viewport.width; canvas.height = viewport.height;
        await page.render({{ canvasContext: canvas.getContext('2d'), viewport }}).promise;
        const blob = await canvasToBlob(canvas, 'image/jpeg', 0.92);
        pageBlobs.push({{ blob, name: baseName + '-page-' + i + '.jpg' }});
        const card = document.createElement('div');
        card.className = 'peg-card';
        card.style.cursor = 'default';
        card.innerHTML = '<span class="tag">Page ' + i + '</span><h3 style="font-size:14px">' + baseName + '-page-' + i + '.jpg</h3><span class="go" style="cursor:pointer">Download</span>';
        card.querySelector('.go').addEventListener('click', () => downloadBlob(blob, baseName + '-page-' + i + '.jpg'));
        results.appendChild(card);
      }}
      statusText.textContent = 'Done \u2014 ' + pdf.numPages + ' page(s) converted.';
      bar.style.width = '100%';
      if (pageBlobs.length > 1) dlAllWrap.style.display = 'block';
    }} catch (e) {{
      showError(err, 'Could not convert that PDF: ' + e.message);
      status.style.display = 'none';
    }}
  }});

  dlAll.addEventListener('click', () => {{
    pageBlobs.forEach((p, idx) => setTimeout(() => downloadBlob(p.blob, p.name), idx * 300));
  }});
}})();
</script>
"""
    write(os.path.join(ROOT, FOLDER, slug), TOOL_PAGE(
        title="PDF to JPG Converter &mdash; Free Online Tool | Toolpeg",
        description="Convert every page of a PDF into a JPG image for free, right in your browser.",
        canonical_path=f"{FOLDER}/{slug}", depth=DEPTH, active="pdf", body=body, slug=slug, foot_scripts=script))


# ------------------------------------------------------------- JPG to PDF
def gen_jpg_to_pdf():
    slug = "jpg-to-pdf.html"
    body = f"""<main class="tool-shell">
  <div class="wrap">
    {breadcrumb('JPG to PDF')}
    <div class="tool-head">
      {tool_head('Convert', 'JPG to PDF', 'Combine one or more photos into a single PDF document. Drag to reorder pages before you export.')}
    </div>
    <div class="dropzone" id="dz" tabindex="0" role="button" aria-label="Upload images">
      {DZ_SVG}
      <h3>Drop JPG or PNG images here, or click to browse</h3>
      <p>Multiple files supported &middot; processed on your device</p>
    </div>
    <input type="file" id="file-input" accept="image/jpeg,image/png" multiple hidden>
    <div id="error" class="error-box"></div>
    <div id="list" style="margin-top:18px"></div>
    <div class="grid-2" id="options-wrap" style="display:none;margin-top:18px">
      <div class="panel">
        <div class="field">
          <label for="pagesize">Page size</label>
          <select id="pagesize">
            <option value="a4">A4</option>
            <option value="letter">US Letter</option>
            <option value="fit">Fit to image</option>
          </select>
        </div>
      </div>
      <div class="panel">
        <button class="btn btn-primary btn-block" id="make-btn">Create PDF &amp; download</button>
        <p class="note">Pages are added in the order listed above. Use the &uarr; / &darr; buttons to reorder.</p>
      </div>
    </div>
  </div>
</main>
"""
    script = f"""{JSPDF}
<script src="../js/file-utils.js?v=202611031215"></script>
<script>
(function(){{
  const dz = document.getElementById('dz');
  const input = document.getElementById('file-input');
  const err = document.getElementById('error');
  const list = document.getElementById('list');
  const optionsWrap = document.getElementById('options-wrap');
  const pagesize = document.getElementById('pagesize');
  const makeBtn = document.getElementById('make-btn');
  let items = [];

  function render() {{
    list.innerHTML = '';
    items.forEach((it, i) => {{
      const row = document.createElement('div');
      row.className = 'file-item';
      row.innerHTML = `<img class="thumb" src="${{it.url}}" alt=""><span class="name">${{it.file.name}}</span><span class="size">${{humanFileSize(it.file.size)}}</span>`;
      const up = document.createElement('button'); up.textContent = '\\u2191'; up.title = 'Move up';
      up.addEventListener('click', () => {{ if (i > 0) {{ [items[i-1], items[i]] = [items[i], items[i-1]]; render(); }} }});
      const down = document.createElement('button'); down.textContent = '\\u2193'; down.title = 'Move down';
      down.addEventListener('click', () => {{ if (i < items.length - 1) {{ [items[i+1], items[i]] = [items[i], items[i+1]]; render(); }} }});
      const rm = document.createElement('button'); rm.textContent = '\\u00d7'; rm.title = 'Remove';
      rm.addEventListener('click', () => {{ items.splice(i, 1); render(); }});
      row.appendChild(up); row.appendChild(down); row.appendChild(rm);
      list.appendChild(row);
    }});
    optionsWrap.style.display = items.length ? 'grid' : 'none';
  }}

  setupDropzone(dz, input, async (files) => {{
    hideError(err);
    for (const file of files) {{
      if (!file.type.startsWith('image/')) continue;
      const {{ url }} = await loadImage(file);
      items.push({{ file, url }});
    }}
    render();
  }});

  makeBtn.addEventListener('click', async () => {{
    if (!items.length) return;
    if (!window.jspdf) {{ showError(err, "Couldn't load the PDF engine. Check your connection and try again."); return; }}
    makeBtn.disabled = true;
    makeBtn.textContent = 'Building PDF\\u2026';
    try {{
      const {{ jsPDF }} = window.jspdf;
      let doc = null;
      for (const it of items) {{
        const {{ img }} = await loadImage(it.file);
        const isLandscape = img.naturalWidth > img.naturalHeight;
        let format = 'a4';
        if (pagesize.value === 'letter') format = 'letter';
        if (pagesize.value === 'fit') format = [img.naturalWidth, img.naturalHeight];
        const orientation = pagesize.value === 'fit' ? 'p' : (isLandscape ? 'l' : 'p');
        if (!doc) doc = new jsPDF({{ orientation, unit: 'pt', format }});
        else doc.addPage(format, orientation);
        const pageW = doc.internal.pageSize.getWidth();
        const pageH = doc.internal.pageSize.getHeight();
        let w = pageW, h = (img.naturalHeight / img.naturalWidth) * pageW;
        if (h > pageH) {{ h = pageH; w = (img.naturalWidth / img.naturalHeight) * pageH; }}
        const x = (pageW - w) / 2, y = (pageH - h) / 2;
        const canvas = document.createElement('canvas');
        canvas.width = img.naturalWidth; canvas.height = img.naturalHeight;
        const ctx = canvas.getContext('2d');
        // JPEG has no alpha channel, so fill white first or transparent pixels turn black
        ctx.fillStyle = '#fff';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0);
        const dataUrl = canvas.toDataURL('image/jpeg', 0.92);
        doc.addImage(dataUrl, 'JPEG', x, y, w, h);
      }}
      doc.save('images.pdf');
    }} catch (e) {{
      showError(err, 'Could not build the PDF: ' + e.message);
    }} finally {{
      makeBtn.disabled = false;
      makeBtn.textContent = 'Create PDF & download';
    }}
  }});
}})();
</script>
"""
    write(os.path.join(ROOT, FOLDER, slug), TOOL_PAGE(
        title="JPG to PDF Converter &mdash; Combine Images into a PDF | Toolpeg",
        description="Combine one or more JPG or PNG images into a single PDF document, free and in your browser.",
        canonical_path=f"{FOLDER}/{slug}", depth=DEPTH, active="pdf", body=body, slug=slug, foot_scripts=script))


# ---------------------------------------------------------------- merge
def gen_merge_pdf():
    slug = "merge-pdf.html"
    body = f"""<main class="tool-shell">
  <div class="wrap">
    {breadcrumb('Merge PDF')}
    <div class="tool-head">
      {tool_head('Combine', 'Merge PDF', 'Combine two or more PDFs into one file, in the order you arrange them below.')}
    </div>
    <div class="dropzone" id="dz" tabindex="0" role="button" aria-label="Upload PDFs">
      {DZ_SVG}
      <h3>Drop PDF files here, or click to browse</h3>
      <p>Multiple files supported &middot; processed on your device</p>
    </div>
    <input type="file" id="file-input" accept="application/pdf" multiple hidden>
    <div id="error" class="error-box"></div>
    <div id="list" style="margin-top:18px"></div>
    <button class="btn btn-primary" id="merge-btn" style="display:none;margin-top:16px">Merge &amp; download</button>
  </div>
</main>
"""
    script = f"""{PDFLIB}
<script src="../js/file-utils.js?v=202611031215"></script>
<script>
(function(){{
  const dz = document.getElementById('dz');
  const input = document.getElementById('file-input');
  const err = document.getElementById('error');
  const list = document.getElementById('list');
  const mergeBtn = document.getElementById('merge-btn');
  let items = [];

  function render() {{
    list.innerHTML = '';
    items.forEach((file, i) => {{
      const row = document.createElement('div');
      row.className = 'file-item';
      row.innerHTML = `<span class="name">${{i+1}}. ${{file.name}}</span><span class="size">${{humanFileSize(file.size)}}</span>`;
      const up = document.createElement('button'); up.textContent = '\\u2191';
      up.addEventListener('click', () => {{ if (i > 0) {{ [items[i-1], items[i]] = [items[i], items[i-1]]; render(); }} }});
      const down = document.createElement('button'); down.textContent = '\\u2193';
      down.addEventListener('click', () => {{ if (i < items.length - 1) {{ [items[i+1], items[i]] = [items[i], items[i+1]]; render(); }} }});
      const rm = document.createElement('button'); rm.textContent = '\\u00d7';
      rm.addEventListener('click', () => {{ items.splice(i, 1); render(); }});
      row.appendChild(up); row.appendChild(down); row.appendChild(rm);
      list.appendChild(row);
    }});
    mergeBtn.style.display = items.length >= 2 ? 'inline-flex' : 'none';
  }}

  setupDropzone(dz, input, (files) => {{
    hideError(err);
    for (const f of files) {{ if (f.type === 'application/pdf') items.push(f); }}
    render();
  }});

  mergeBtn.addEventListener('click', async () => {{
    if (!window.PDFLib) {{ showError(err, "Couldn't load the PDF engine. Check your connection and try again."); return; }}
    mergeBtn.disabled = true;
    mergeBtn.textContent = 'Merging\\u2026';
    try {{
      const {{ PDFDocument }} = PDFLib;
      const merged = await PDFDocument.create();
      for (const file of items) {{
        const bytes = await file.arrayBuffer();
        const src = await PDFDocument.load(bytes);
        const pages = await merged.copyPages(src, src.getPageIndices());
        pages.forEach(p => merged.addPage(p));
      }}
      const outBytes = await merged.save();
      downloadBlob(new Blob([outBytes], {{ type: 'application/pdf' }}), 'merged.pdf');
    }} catch (e) {{
      showError(err, 'Could not merge those PDFs: ' + e.message);
    }} finally {{
      mergeBtn.disabled = false;
      mergeBtn.textContent = 'Merge & download';
    }}
  }});
}})();
</script>
"""
    write(os.path.join(ROOT, FOLDER, slug), TOOL_PAGE(
        title="Merge PDF &mdash; Combine PDF Files Free | Toolpeg",
        description="Combine multiple PDF files into one document, in the order you choose, free and in your browser.",
        canonical_path=f"{FOLDER}/{slug}", depth=DEPTH, active="pdf", body=body, slug=slug, foot_scripts=script))


# ---------------------------------------------------------------- split
def gen_split_pdf():
    slug = "split-pdf.html"
    body = f"""<main class="tool-shell">
  <div class="wrap">
    {breadcrumb('Split PDF')}
    <div class="tool-head">
      {tool_head('Split', 'Split PDF', 'Pull specific pages out of a PDF, or split every page into its own file.')}
    </div>
    <div class="dropzone" id="dz" tabindex="0" role="button" aria-label="Upload PDF">
      {DZ_SVG}
      <h3>Drop a PDF here, or click to browse</h3>
      <p>PDF &middot; processed on your device</p>
    </div>
    <input type="file" id="file-input" accept="application/pdf" hidden>
    <div id="error" class="error-box"></div>
    <div id="options-wrap" style="display:none;margin-top:18px" class="grid-2">
      <div class="panel">
        <div class="field">
          <label id="page-count-label">Loaded PDF</label>
          <div id="page-count" style="font-family:var(--font);font-size:13px;color:var(--text-muted)"></div>
        </div>
        <div class="field">
          <label for="mode">Mode</label>
          <select id="mode">
            <option value="range">Extract a page range</option>
            <option value="each">Split into single-page files</option>
          </select>
        </div>
        <div class="row" id="range-fields">
          <div class="field"><label for="from">From page</label><input type="number" id="from" min="1" value="1"></div>
          <div class="field"><label for="to">To page</label><input type="number" id="to" min="1" value="1"></div>
        </div>
      </div>
      <div class="panel">
        <button class="btn btn-primary btn-block" id="split-btn">Split &amp; download</button>
        <p class="note">"Split into single-page files" downloads one PDF per page, one after another.</p>
      </div>
    </div>
  </div>
</main>
"""
    script = f"""{PDFLIB}
<script src="../js/file-utils.js?v=202611031215"></script>
<script>
(function(){{
  const dz = document.getElementById('dz');
  const input = document.getElementById('file-input');
  const err = document.getElementById('error');
  const optionsWrap = document.getElementById('options-wrap');
  const pageCount = document.getElementById('page-count');
  const mode = document.getElementById('mode');
  const rangeFields = document.getElementById('range-fields');
  const fromEl = document.getElementById('from');
  const toEl = document.getElementById('to');
  const splitBtn = document.getElementById('split-btn');
  let currentFile = null, totalPages = 0;

  mode.addEventListener('change', () => {{ rangeFields.style.display = mode.value === 'range' ? 'flex' : 'none'; }});

  setupDropzone(dz, input, async (files) => {{
    hideError(err);
    const file = files[0];
    if (file.type !== 'application/pdf') {{ showError(err, 'Please choose a PDF file.'); return; }}
    if (!window.PDFLib) {{ showError(err, "Couldn't load the PDF engine. Check your connection and try again."); return; }}
    try {{
      currentFile = file;
      const bytes = await file.arrayBuffer();
      const doc = await PDFLib.PDFDocument.load(bytes);
      totalPages = doc.getPageCount();
      pageCount.textContent = file.name + '  \\u00b7  ' + totalPages + ' page(s)';
      fromEl.max = totalPages; toEl.max = totalPages; toEl.value = totalPages;
      optionsWrap.style.display = 'grid';
    }} catch (e) {{
      showError(err, 'Could not read that PDF: ' + e.message);
    }}
  }});

  splitBtn.addEventListener('click', async () => {{
    if (!currentFile) return;
    splitBtn.disabled = true;
    splitBtn.textContent = 'Splitting\\u2026';
    try {{
      const bytes = await currentFile.arrayBuffer();
      const baseName = stripExt(currentFile.name);
      if (mode.value === 'range') {{
        const from = Math.max(1, Math.min(totalPages, Number(fromEl.value) || 1));
        const to = Math.max(from, Math.min(totalPages, Number(toEl.value) || totalPages));
        const src = await PDFLib.PDFDocument.load(bytes);
        const out = await PDFLib.PDFDocument.create();
        const indices = [];
        for (let i = from - 1; i <= to - 1; i++) indices.push(i);
        const pages = await out.copyPages(src, indices);
        pages.forEach(p => out.addPage(p));
        const outBytes = await out.save();
        downloadBlob(new Blob([outBytes], {{ type: 'application/pdf' }}), baseName + '-p' + from + '-' + to + '.pdf');
      }} else {{
        for (let i = 0; i < totalPages; i++) {{
          const src = await PDFLib.PDFDocument.load(bytes);
          const out = await PDFLib.PDFDocument.create();
          const [page] = await out.copyPages(src, [i]);
          out.addPage(page);
          const outBytes = await out.save();
          downloadBlob(new Blob([outBytes], {{ type: 'application/pdf' }}), baseName + '-page-' + (i + 1) + '.pdf');
          await new Promise(r => setTimeout(r, 250));
        }}
      }}
    }} catch (e) {{
      showError(err, 'Could not split that PDF: ' + e.message);
    }} finally {{
      splitBtn.disabled = false;
      splitBtn.textContent = 'Split & download';
    }}
  }});
}})();
</script>
"""
    write(os.path.join(ROOT, FOLDER, slug), TOOL_PAGE(
        title="Split PDF &mdash; Extract or Split PDF Pages Free | Toolpeg",
        description="Extract a page range from a PDF, or split every page into its own file, free and in your browser.",
        canonical_path=f"{FOLDER}/{slug}", depth=DEPTH, active="pdf", body=body, slug=slug, foot_scripts=script))


# ---------------------------------------------------------------- Compress PDF
COMPRESS_JS = r"""(function(){
  const dz = document.getElementById('dz');
  const input = document.getElementById('file-input');
  const err = document.getElementById('error');
  const optionsWrap = document.getElementById('options-wrap');
  const fileInfo = document.getElementById('file-info');
  const mode = document.getElementById('mode');
  const modeNote = document.getElementById('mode-note');
  const level = document.getElementById('level');
  const compressBtn = document.getElementById('compress-btn');
  const status = document.getElementById('status');
  const bar = document.getElementById('bar');
  const statusText = document.getElementById('status-text');
  const resultBox = document.getElementById('result-box');
  const newSize = document.getElementById('new-size');
  const sizeSub = document.getElementById('size-sub');
  let currentFile = null;

  // Rasterize mode: re-render every page as an image.
  const RASTER = {
    high: { scale: 1.0, quality: 0.5 },
    balanced: { scale: 1.5, quality: 0.7 },
    low: { scale: 2.0, quality: 0.85 },
  };
  // Keep-text mode: recompress embedded JPEGs, longest side capped at maxDim pixels.
  const KEEP = {
    high: { maxDim: 1200, quality: 0.5 },
    balanced: { maxDim: 1800, quality: 0.7 },
    low: { maxDim: 2600, quality: 0.85 },
  };
  const MIN_IMAGE_BYTES = 20 * 1024; // skip tiny images, not worth touching

  const NOTES = {
    keep: 'Text, fonts and links are left exactly as they are. Only the JPEG images inside the PDF are recompressed.',
    raster: 'Every page becomes an image. Text will no longer be selectable or searchable.',
  };
  function updateNote() { modeNote.textContent = NOTES[mode.value]; }
  mode.addEventListener('change', updateNote);
  updateNote();

  setupDropzone(dz, input, async (files) => {
    hideError(err);
    const file = files[0];
    if (file.type !== 'application/pdf') { showError(err, 'Please choose a PDF file.'); return; }
    currentFile = file;
    fileInfo.textContent = file.name + '  \u00b7  ' + humanFileSize(file.size);
    optionsWrap.style.display = 'grid';
    resultBox.style.display = 'none';
  });

  // ---- Mode 1: keep text -------------------------------------------------
  async function shrinkJpeg(bytes, maxDim, quality) {
    if (!window.createImageBitmap) return null;
    // 'none' = ignore EXIF rotation, because PDF viewers ignore it too
    const bmp = await createImageBitmap(new Blob([bytes], { type: 'image/jpeg' }), { imageOrientation: 'none' });
    try {
      const ratio = Math.min(1, maxDim / Math.max(bmp.width, bmp.height));
      const w = Math.max(1, Math.round(bmp.width * ratio));
      const h = Math.max(1, Math.round(bmp.height * ratio));
      const canvas = document.createElement('canvas');
      canvas.width = w; canvas.height = h;
      const ctx = canvas.getContext('2d');
      ctx.fillStyle = '#fff';
      ctx.fillRect(0, 0, w, h);
      ctx.imageSmoothingQuality = 'high';
      ctx.drawImage(bmp, 0, 0, w, h);
      const out = await new Promise((resolve) => canvas.toBlob(resolve, 'image/jpeg', quality));
      if (!out) return null;
      const outBytes = new Uint8Array(await out.arrayBuffer());
      if (outBytes.length > bytes.length * 0.9) return null; // not a meaningful saving, keep original
      return { bytes: outBytes, w, h };
    } finally {
      if (bmp.close) bmp.close();
    }
  }

  async function compressKeepText(buf) {
    const { PDFDocument, PDFName, PDFArray, PDFRawStream } = PDFLib;
    const { maxDim, quality } = KEEP[level.value];
    let pdfDoc;
    try {
      pdfDoc = await PDFDocument.load(buf, { updateMetadata: false });
    } catch (e) {
      if (/encrypt/i.test((e && e.message) || '')) {
        throw new Error('this PDF is password-protected. Remove the password first, then try again.');
      }
      throw e;
    }
    const ctx = pdfDoc.context;
    const candidates = [];
    for (const [ref, obj] of ctx.enumerateIndirectObjects()) {
      if (!(obj instanceof PDFRawStream)) continue;
      const d = obj.dict;
      const subtype = d.lookup(PDFName.of('Subtype'));
      if (!subtype || subtype.toString() !== '/Image') continue;
      let filter = d.lookup(PDFName.of('Filter'));
      if (filter instanceof PDFArray) { if (filter.size() !== 1) continue; filter = filter.lookup(0); }
      if (!filter || filter.toString() !== '/DCTDecode') continue;      // JPEG only
      if (d.has(PDFName.of('Mask'))) continue;                          // colour-key mask would break
      const isMask = d.lookup(PDFName.of('ImageMask'));
      if (isMask && isMask.toString() === 'true') continue;
      if (obj.contents.length < MIN_IMAGE_BYTES) continue;
      candidates.push({ ref, obj });
    }

    let replaced = 0;
    for (let i = 0; i < candidates.length; i++) {
      statusText.textContent = 'Optimizing image ' + (i + 1) + ' of ' + candidates.length + '\u2026';
      bar.style.width = Math.round(((i + 1) / candidates.length) * 90) + '%';
      const { ref, obj } = candidates[i];
      try {
        const res = await shrinkJpeg(obj.contents, maxDim, quality);
        if (!res) continue;
        const newDict = ctx.obj({
          Type: 'XObject', Subtype: 'Image', Width: res.w, Height: res.h,
          ColorSpace: 'DeviceRGB', BitsPerComponent: 8, Filter: 'DCTDecode',
        });
        const smask = obj.dict.get(PDFName.of('SMask'));
        if (smask) newDict.set(PDFName.of('SMask'), smask);
        ctx.assign(ref, PDFRawStream.of(newDict, res.bytes));
        replaced++;
      } catch (e) {
        // leave this image untouched
      }
    }
    statusText.textContent = 'Saving\u2026';
    bar.style.width = '95%';
    const bytes = await pdfDoc.save({ useObjectStreams: true });
    return { bytes, replaced, found: candidates.length };
  }

  // ---- Mode 2: rasterize --------------------------------------------------
  async function compressRasterize(buf) {
    const { scale, quality } = RASTER[level.value];
    const pdf = await pdfjsLib.getDocument({ data: buf }).promise;
    const { jsPDF } = window.jspdf;
    let doc = null;
    for (let i = 1; i <= pdf.numPages; i++) {
      statusText.textContent = 'Compressing page ' + i + ' of ' + pdf.numPages + '\u2026';
      bar.style.width = Math.round((i / pdf.numPages) * 100) + '%';
      const page = await pdf.getPage(i);
      const viewport = page.getViewport({ scale });
      const canvas = document.createElement('canvas');
      canvas.width = viewport.width; canvas.height = viewport.height;
      const ctx = canvas.getContext('2d');
      // PDF pages render onto a transparent canvas; fill white so JPEG doesn't turn it black
      ctx.fillStyle = '#fff';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      await page.render({ canvasContext: ctx, viewport }).promise;
      const dataUrl = canvas.toDataURL('image/jpeg', quality);
      const wPt = viewport.width / scale;
      const hPt = viewport.height / scale;
      const orientation = wPt > hPt ? 'l' : 'p';
      if (!doc) doc = new jsPDF({ orientation, unit: 'pt', format: [wPt, hPt] });
      else doc.addPage([wPt, hPt], orientation);
      doc.addImage(dataUrl, 'JPEG', 0, 0, wPt, hPt);
    }
    return { bytes: doc.output('arraybuffer') };
  }

  compressBtn.addEventListener('click', async () => {
    if (!currentFile) return;
    hideError(err);
    const keepText = mode.value === 'keep';
    if (keepText && !window.PDFLib) { showError(err, "Couldn't load the PDF engine. Check your connection and try again."); return; }
    if (!keepText && (!window.pdfjsLib || !window.jspdf)) { showError(err, "Couldn't load the PDF engine. Check your connection and try again."); return; }
    compressBtn.disabled = true;
    status.style.display = 'block';
    resultBox.style.display = 'none';
    statusText.textContent = 'Reading PDF\u2026';
    bar.style.width = '5%';
    try {
      const buf = await currentFile.arrayBuffer();
      const result = keepText ? await compressKeepText(buf) : await compressRasterize(buf);
      const blob = new Blob([result.bytes], { type: 'application/pdf' });
      const pct = Math.round((1 - blob.size / currentFile.size) * 100);
      resultBox.style.display = 'block';
      if (keepText && blob.size >= currentFile.size) {
        newSize.textContent = 'No savings';
        sizeSub.textContent = 'This PDF is already compact in this mode \u2014 its size comes from text, fonts or graphics that Keep text leaves alone. If you don\u2019t need searchable text, try Rasterize.';
        statusText.textContent = 'Done. No smaller version found, so nothing was downloaded.';
        bar.style.width = '100%';
        return;
      }
      newSize.textContent = humanFileSize(blob.size);
      let sub = pct > 0 ? ('about ' + pct + '% smaller than the original ' + humanFileSize(currentFile.size)) : ('original was ' + humanFileSize(currentFile.size));
      if (keepText) sub += ' \u00b7 ' + result.replaced + ' of ' + result.found + ' JPEG image' + (result.found === 1 ? '' : 's') + ' recompressed \u00b7 text still selectable';
      sizeSub.textContent = sub;
      downloadBlob(blob, stripExt(currentFile.name) + '-compressed.pdf');
      statusText.textContent = 'Done.';
      bar.style.width = '100%';
    } catch (e) {
      showError(err, 'Could not compress that PDF: ' + e.message);
    } finally {
      compressBtn.disabled = false;
    }
  });
})();"""


def gen_compress_pdf():
    slug = "compress-pdf.html"
    body = f"""<main class="tool-shell">
  <div class="wrap">
    {breadcrumb('Compress PDF')}
    <div class="tool-head">
      {tool_head('Optimize', 'Compress PDF', 'Shrink a PDF while keeping its text searchable, or re-render pages for the smallest possible file.')}
    </div>
    <div class="error-box show" style="background:#F6FBFA;border-color:var(--primary-tint-border);color:var(--primary-hover)">
      <strong>Two ways to compress:</strong> <em>Keep text</em> recompresses the JPEG images inside your PDF and leaves text, fonts and links alone, so it stays searchable &mdash; but it only helps PDFs that contain JPEG images. <em>Rasterize</em> turns every page into an image, which usually shrinks scans and image-heavy files much more, but the text is no longer selectable or searchable.
    </div>
    <div class="dropzone" id="dz" tabindex="0" role="button" aria-label="Upload PDF" style="margin-top:18px">
      {DZ_SVG}
      <h3>Drop a PDF here, or click to browse</h3>
      <p>PDF &middot; processed on your device</p>
    </div>
    <input type="file" id="file-input" accept="application/pdf" hidden>
    <div id="error" class="error-box"></div>
    <div id="options-wrap" style="display:none;margin-top:18px" class="grid-2">
      <div class="panel">
        <div class="field">
          <label>Loaded PDF</label>
          <div id="file-info" style="font-family:var(--font);font-size:13px;color:var(--text-muted)"></div>
        </div>
        <div class="field">
          <label for="mode">Mode</label>
          <select id="mode">
            <option value="keep" selected>Keep text searchable (lighter)</option>
            <option value="raster">Rasterize pages (smallest file)</option>
          </select>
          <p class="note" id="mode-note"></p>
        </div>
        <div class="field">
          <label for="level">Compression level</label>
          <select id="level">
            <option value="high">Smallest file (lower quality)</option>
            <option value="balanced" selected>Balanced</option>
            <option value="low">Best quality (larger file)</option>
          </select>
        </div>
      </div>
      <div class="panel">
        <button class="btn btn-primary btn-block" id="compress-btn">Compress &amp; download</button>
        <div id="status" style="display:none;margin-top:14px">
          <div class="progress"><i id="bar"></i></div>
          <p class="note" id="status-text"></p>
        </div>
        <div class="result-box" id="result-box" style="display:none;margin-top:14px">
          <span class="label">New size</span>
          <div class="big" id="new-size">&mdash;</div>
          <div class="sub" id="size-sub"></div>
        </div>
      </div>
    </div>
  </div>
</main>
"""
    script = (PDFJS + "\n" + JSPDF + "\n" + PDFLIB +
              '\n<script src="../js/file-utils.js?v=202611031215"></script>\n<script>\n' +
              COMPRESS_JS + "\n</script>\n")
    write(os.path.join(ROOT, FOLDER, slug), TOOL_PAGE(
        title="Compress PDF &mdash; Shrink PDF File Size Free | Toolpeg",
        description="Shrink a PDF's file size free in your browser. Keep text searchable by recompressing embedded images, or rasterize pages for the smallest file.",
        canonical_path=f"{FOLDER}/{slug}", depth=DEPTH, active="pdf", body=body, slug=slug, foot_scripts=script))


if __name__ == "__main__":
    gen_pdf_to_jpg()
    gen_jpg_to_pdf()
    gen_merge_pdf()
    gen_split_pdf()
    gen_compress_pdf()
