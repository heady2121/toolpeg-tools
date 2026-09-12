# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from site_lib import PAGE, TOOL_PAGE, write

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
FOLDER = "image-tools"
DEPTH = "../"

DZ_SVG = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12"/><path d="M7 8l5-5 5 5"/><path d="M4 17v2a2 2 0 002 2h12a2 2 0 002-2v-2"/></svg>"""


def breadcrumb(tool_label):
    return f'<p class="breadcrumb"><a href="../index.html">Home</a> / <a href="index.html">Image Tools</a> / {tool_label}</p>'


def tool_head(tag, title, desc):
    return f"""<span class="tag">{tag}</span>
    <h1>{title}</h1>
    <p>{desc}</p>"""


# ------------------------------------------------------------ format convert
def gen_format_convert(slug, from_fmt, to_fmt, to_mime, title, desc, accept, quality_note=""):
    quality_field = ""
    if to_mime in ("image/jpeg", "image/webp"):
        default_q = 92 if to_mime == "image/jpeg" else 85
        quality_field = f"""
          <div class="field">
            <label for="quality">Output quality &mdash; <span id="qval">{default_q}</span>%</label>
            <input type="range" id="quality" min="40" max="100" value="{default_q}">
          </div>"""
    webp_warning = ""
    if to_mime == "image/webp":
        webp_warning = '<div id="webp-warning" class="error-box" style="display:none">Your browser can\'t export WebP images. Try a current version of Chrome, Firefox, Edge or Safari.</div>'
    body = f"""<main class="tool-shell">
  <div class="wrap">
    {breadcrumb(title)}
    <div class="tool-head">
      {tool_head('Convert', title, desc)}
    </div>
    {webp_warning}
    <div class="grid-2">
      <div>
        <div class="dropzone" id="dz" tabindex="0" role="button" aria-label="Upload image">
          {DZ_SVG}
          <h3>Drop a {from_fmt} here, or click to browse</h3>
          <p>{accept.replace(',', ' / ').upper()} &middot; processed on your device</p>
        </div>
        <input type="file" id="file-input" accept="{accept}" hidden>
        <div id="error" class="error-box"></div>
        <div id="preview-wrap" style="display:none;margin-top:18px">
          <img id="preview" alt="Preview" style="border:1px solid var(--hairline);border-radius:6px;max-height:320px;width:auto;margin:0 auto">
        </div>
      </div>
      <div>
        <div class="panel">
          <div class="field">
            <label>Selected file</label>
            <div id="file-info" style="font-family:var(--font-mono);font-size:13px;color:var(--steel)">No file yet</div>
          </div>{quality_field}
          <button class="btn btn-signal btn-block" id="convert-btn" disabled>Convert to {to_fmt}</button>
          <p class="note">{quality_note}Your image is decoded and re-encoded locally using the browser's canvas &mdash; it's never uploaded anywhere.</p>
        </div>
      </div>
    </div>
  </div>
</main>
"""
    script = f"""<script src="../js/file-utils.js"></script>
<script>
(function(){{
  const dz = document.getElementById('dz');
  const input = document.getElementById('file-input');
  const info = document.getElementById('file-info');
  const btn = document.getElementById('convert-btn');
  const err = document.getElementById('error');
  const previewWrap = document.getElementById('preview-wrap');
  const preview = document.getElementById('preview');
  const qualityEl = document.getElementById('quality');
  const qval = document.getElementById('qval');
  const webpWarning = document.getElementById('webp-warning');
  if (qualityEl) qualityEl.addEventListener('input', () => qval.textContent = qualityEl.value);

  if ('{to_mime}' === 'image/webp' && webpWarning) {{
    const testCanvas = document.createElement('canvas');
    testCanvas.width = 1; testCanvas.height = 1;
    testCanvas.toBlob((blob) => {{
      if (!blob) webpWarning.style.display = 'block';
    }}, 'image/webp');
  }}

  let currentFile = null;

  setupDropzone(dz, input, async (files) => {{
    hideError(err);
    const file = files[0];
    if (!file.type.startsWith('image/')) {{ showError(err, 'Please choose an image file.'); return; }}
    currentFile = file;
    info.textContent = file.name + '  \u00b7  ' + humanFileSize(file.size);
    try {{
      const {{ img, url }} = await loadImage(file);
      preview.src = url;
      previewWrap.style.display = 'block';
      btn.disabled = false;
    }} catch (e) {{
      showError(err, e.message);
    }}
  }});

  btn.addEventListener('click', async () => {{
    if (!currentFile) return;
    hideError(err);
    btn.disabled = true;
    btn.textContent = 'Converting\u2026';
    try {{
      const {{ img }} = await loadImage(currentFile);
      const canvas = document.createElement('canvas');
      canvas.width = img.naturalWidth;
      canvas.height = img.naturalHeight;
      const ctx = canvas.getContext('2d');
      if ('{to_mime}' === 'image/jpeg') {{
        ctx.fillStyle = '#fff';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
      }}
      ctx.drawImage(img, 0, 0);
      const q = qualityEl ? Number(qualityEl.value) / 100 : undefined;
      const blob = await canvasToBlob(canvas, '{to_mime}', q);
      downloadBlob(blob, stripExt(currentFile.name) + '.{to_fmt.lower()}');
    }} catch (e) {{
      showError(err, 'Conversion failed: ' + e.message);
    }} finally {{
      btn.disabled = false;
      btn.textContent = 'Convert to {to_fmt}';
    }}
  }});
}})();
</script>
"""
    html = TOOL_PAGE(
        title=f"{title} &mdash; Free Online Converter | Toolpeg",
        description=desc,
        canonical_path=f"{FOLDER}/{slug}",
        depth=DEPTH,
        active="image",
        body=body,
        slug=slug,
        foot_scripts=script,
    )
    write(os.path.join(ROOT, FOLDER, slug), html)


# ------------------------------------------------------------- compressor
def gen_compressor():
    slug = "image-compressor.html"
    body = f"""<main class="tool-shell">
  <div class="wrap">
    {breadcrumb('Image Compressor')}
    <div class="tool-head">
      {tool_head('Optimize', 'Image Compressor', 'Drag the quality slider and watch the output size update live, before you download.')}
    </div>
    <div class="grid-2">
      <div>
        <div class="dropzone" id="dz" tabindex="0" role="button" aria-label="Upload image">
          {DZ_SVG}
          <h3>Drop a JPG or PNG here, or click to browse</h3>
          <p>JPG / PNG / WEBP &middot; processed on your device</p>
        </div>
        <input type="file" id="file-input" accept="image/jpeg,image/png,image/webp" hidden>
        <div id="error" class="error-box"></div>
        <div id="preview-wrap" style="display:none;margin-top:18px">
          <img id="preview" alt="Preview" style="border:1px solid var(--hairline);border-radius:6px;max-height:320px;width:auto;margin:0 auto">
        </div>
      </div>
      <div>
        <div class="panel">
          <div class="field">
            <label>Selected file</label>
            <div id="file-info" style="font-family:var(--font-mono);font-size:13px;color:var(--steel)">No file yet</div>
          </div>
          <div class="field">
            <label for="quality">Quality &mdash; <span id="qval">75</span>%</label>
            <input type="range" id="quality" min="10" max="100" value="75">
          </div>
          <div class="result-box" style="margin-bottom:18px">
            <span class="label">Estimated output size</span>
            <div class="big" id="est-size">&mdash;</div>
            <div class="sub" id="est-sub"></div>
          </div>
          <button class="btn btn-signal btn-block" id="convert-btn" disabled>Compress &amp; download</button>
          <p class="note">Compression happens locally by re-encoding the image on a canvas &mdash; nothing is uploaded.</p>
        </div>
      </div>
    </div>
  </div>
</main>
"""
    script = """<script src="../js/file-utils.js"></script>
<script>
(function(){
  const dz = document.getElementById('dz');
  const input = document.getElementById('file-input');
  const info = document.getElementById('file-info');
  const btn = document.getElementById('convert-btn');
  const err = document.getElementById('error');
  const previewWrap = document.getElementById('preview-wrap');
  const preview = document.getElementById('preview');
  const quality = document.getElementById('quality');
  const qval = document.getElementById('qval');
  const estSize = document.getElementById('est-size');
  const estSub = document.getElementById('est-sub');

  let currentFile = null, currentImg = null, originalSize = 0, debounceT = null;

  function outMime(file) {
    return file.type === 'image/png' ? 'image/png' : 'image/jpeg';
  }

  async function updateEstimate() {
    if (!currentImg) return;
    const canvas = document.createElement('canvas');
    canvas.width = currentImg.naturalWidth;
    canvas.height = currentImg.naturalHeight;
    const ctx = canvas.getContext('2d');
    const mime = outMime(currentFile);
    if (mime === 'image/jpeg') { ctx.fillStyle = '#fff'; ctx.fillRect(0,0,canvas.width,canvas.height); }
    ctx.drawImage(currentImg, 0, 0);
    const blob = await canvasToBlob(canvas, mime, Number(quality.value) / 100);
    const pct = originalSize ? Math.round((1 - blob.size / originalSize) * 100) : 0;
    estSize.textContent = humanFileSize(blob.size);
    estSub.textContent = pct > 0 ? ('about ' + pct + '% smaller than the original ' + humanFileSize(originalSize)) : ('original was ' + humanFileSize(originalSize));
  }

  quality.addEventListener('input', () => {
    qval.textContent = quality.value;
    clearTimeout(debounceT);
    debounceT = setTimeout(updateEstimate, 150);
  });

  setupDropzone(dz, input, async (files) => {
    hideError(err);
    const file = files[0];
    if (!file.type.startsWith('image/')) { showError(err, 'Please choose an image file.'); return; }
    currentFile = file;
    originalSize = file.size;
    info.textContent = file.name + '  \u00b7  ' + humanFileSize(file.size);
    try {
      const { img, url } = await loadImage(file);
      currentImg = img;
      preview.src = url;
      previewWrap.style.display = 'block';
      btn.disabled = false;
      updateEstimate();
    } catch (e) { showError(err, e.message); }
  });

  btn.addEventListener('click', async () => {
    if (!currentFile || !currentImg) return;
    hideError(err);
    btn.disabled = true;
    btn.textContent = 'Compressing\u2026';
    try {
      const canvas = document.createElement('canvas');
      canvas.width = currentImg.naturalWidth;
      canvas.height = currentImg.naturalHeight;
      const ctx = canvas.getContext('2d');
      const mime = outMime(currentFile);
      if (mime === 'image/jpeg') { ctx.fillStyle = '#fff'; ctx.fillRect(0,0,canvas.width,canvas.height); }
      ctx.drawImage(currentImg, 0, 0);
      const blob = await canvasToBlob(canvas, mime, Number(quality.value) / 100);
      downloadBlob(blob, stripExt(currentFile.name) + '-compressed.' + (mime === 'image/png' ? 'png' : 'jpg'));
    } catch (e) {
      showError(err, 'Compression failed: ' + e.message);
    } finally {
      btn.disabled = false;
      btn.textContent = 'Compress & download';
    }
  });
})();
</script>
"""
    html = TOOL_PAGE(
        title="Image Compressor &mdash; Shrink JPG/PNG File Size Free | Toolpeg",
        description="Compress JPG or PNG images with a live quality slider and size estimate. Free, no upload, works in your browser.",
        canonical_path=f"{FOLDER}/{slug}", depth=DEPTH, active="image", body=body, slug=slug, foot_scripts=script,
    )
    write(os.path.join(ROOT, FOLDER, slug), html)


# ------------------------------------------------------------------ resizer
def gen_resizer():
    slug = "image-resizer.html"
    body = f"""<main class="tool-shell">
  <div class="wrap">
    {breadcrumb('Image Resizer')}
    <div class="tool-head">
      {tool_head('Resize', 'Image Resizer', 'Resize any image to an exact pixel size or a percentage, with the option to lock the aspect ratio.')}
    </div>
    <div class="grid-2">
      <div>
        <div class="dropzone" id="dz" tabindex="0" role="button" aria-label="Upload image">
          {DZ_SVG}
          <h3>Drop an image here, or click to browse</h3>
          <p>JPG / PNG / WEBP &middot; processed on your device</p>
        </div>
        <input type="file" id="file-input" accept="image/jpeg,image/png,image/webp" hidden>
        <div id="error" class="error-box"></div>
        <div id="preview-wrap" style="display:none;margin-top:18px">
          <img id="preview" alt="Preview" style="border:1px solid var(--hairline);border-radius:6px;max-height:320px;width:auto;margin:0 auto">
        </div>
      </div>
      <div>
        <div class="panel">
          <div class="field">
            <label>Selected file</label>
            <div id="file-info" style="font-family:var(--font-mono);font-size:13px;color:var(--steel)">No file yet</div>
          </div>
          <div class="row">
            <div class="field">
              <label for="w">Width (px)</label>
              <input type="number" id="w" min="1">
            </div>
            <div class="field">
              <label for="h">Height (px)</label>
              <input type="number" id="h" min="1">
            </div>
          </div>
          <div class="field">
            <label><input type="checkbox" id="lock" checked style="width:auto;margin-right:8px">Lock aspect ratio</label>
          </div>
          <button class="btn btn-signal btn-block" id="convert-btn" disabled>Resize &amp; download</button>
          <p class="note">Resizing redraws the image on a canvas at the new size locally &mdash; nothing is uploaded.</p>
        </div>
      </div>
    </div>
  </div>
</main>
"""
    script = """<script src="../js/file-utils.js"></script>
<script>
(function(){
  const dz = document.getElementById('dz');
  const input = document.getElementById('file-input');
  const info = document.getElementById('file-info');
  const btn = document.getElementById('convert-btn');
  const err = document.getElementById('error');
  const previewWrap = document.getElementById('preview-wrap');
  const preview = document.getElementById('preview');
  const wEl = document.getElementById('w'), hEl = document.getElementById('h'), lockEl = document.getElementById('lock');

  let currentFile = null, currentImg = null, ratio = 1;

  wEl.addEventListener('input', () => {
    if (lockEl.checked && ratio) hEl.value = Math.round(Number(wEl.value) / ratio);
  });
  hEl.addEventListener('input', () => {
    if (lockEl.checked && ratio) wEl.value = Math.round(Number(hEl.value) * ratio);
  });

  setupDropzone(dz, input, async (files) => {
    hideError(err);
    const file = files[0];
    if (!file.type.startsWith('image/')) { showError(err, 'Please choose an image file.'); return; }
    currentFile = file;
    info.textContent = file.name + '  \u00b7  ' + humanFileSize(file.size);
    try {
      const { img, url } = await loadImage(file);
      currentImg = img;
      ratio = img.naturalWidth / img.naturalHeight;
      wEl.value = img.naturalWidth;
      hEl.value = img.naturalHeight;
      preview.src = url;
      previewWrap.style.display = 'block';
      btn.disabled = false;
    } catch (e) { showError(err, e.message); }
  });

  btn.addEventListener('click', async () => {
    if (!currentFile || !currentImg) return;
    const w = Math.max(1, Math.round(Number(wEl.value) || currentImg.naturalWidth));
    const h = Math.max(1, Math.round(Number(hEl.value) || currentImg.naturalHeight));
    hideError(err);
    btn.disabled = true;
    btn.textContent = 'Resizing\u2026';
    try {
      const canvas = document.createElement('canvas');
      canvas.width = w; canvas.height = h;
      const ctx = canvas.getContext('2d');
      const mime = currentFile.type === 'image/png' ? 'image/png' : 'image/jpeg';
      if (mime === 'image/jpeg') { ctx.fillStyle = '#fff'; ctx.fillRect(0,0,w,h); }
      ctx.imageSmoothingQuality = 'high';
      ctx.drawImage(currentImg, 0, 0, w, h);
      const blob = await canvasToBlob(canvas, mime, 0.92);
      downloadBlob(blob, stripExt(currentFile.name) + '-' + w + 'x' + h + '.' + (mime === 'image/png' ? 'png' : 'jpg'));
    } catch (e) {
      showError(err, 'Resize failed: ' + e.message);
    } finally {
      btn.disabled = false;
      btn.textContent = 'Resize & download';
    }
  });
})();
</script>
"""
    html = TOOL_PAGE(
        title="Image Resizer &mdash; Resize Photos to Exact Pixels Free | Toolpeg",
        description="Resize JPG, PNG or WebP images to an exact width and height or lock the aspect ratio. Free, no upload required.",
        canonical_path=f"{FOLDER}/{slug}", depth=DEPTH, active="image", body=body, slug=slug, foot_scripts=script,
    )
    write(os.path.join(ROOT, FOLDER, slug), html)


# ------------------------------------------------------------------ cropper
def gen_cropper():
    slug = "image-cropper.html"
    body = f"""<main class="tool-shell">
  <div class="wrap">
    {breadcrumb('Image Cropper')}
    <div class="tool-head">
      {tool_head('Edit', 'Image Cropper', 'Drag the corners to crop freely, or lock a ratio like 1:1 or 16:9.')}
    </div>
    <div id="uploader">
      <div class="dropzone" id="dz" tabindex="0" role="button" aria-label="Upload image">
        {DZ_SVG}
        <h3>Drop an image here, or click to browse</h3>
        <p>JPG / PNG / WEBP &middot; processed on your device</p>
      </div>
      <input type="file" id="file-input" accept="image/jpeg,image/png,image/webp" hidden>
      <div id="error" class="error-box"></div>
    </div>
    <div id="editor" style="display:none">
      <div class="grid-2">
        <div>
          <div class="crop-stage" id="stage">
            <canvas id="canvas"></canvas>
            <div class="crop-box" id="cropbox">
              <div class="handle" data-h="nw" style="left:0;top:0;cursor:nwse-resize"></div>
              <div class="handle" data-h="ne" style="right:0;top:0;left:auto;cursor:nesw-resize"></div>
              <div class="handle" data-h="sw" style="left:0;bottom:0;top:auto;cursor:nesw-resize"></div>
              <div class="handle" data-h="se" style="right:0;bottom:0;top:auto;left:auto;cursor:nwse-resize"></div>
            </div>
          </div>
        </div>
        <div>
          <div class="panel">
            <div class="field">
              <label for="ratio">Aspect ratio</label>
              <select id="ratio">
                <option value="free">Free</option>
                <option value="1">Square 1:1</option>
                <option value="0.8">Portrait 4:5</option>
                <option value="1.7778">Widescreen 16:9</option>
                <option value="1.3333">Standard 4:3</option>
              </select>
            </div>
            <div class="field">
              <label>Crop size</label>
              <div id="cropdims" style="font-family:var(--font-mono);font-size:13px;color:var(--steel)">&mdash;</div>
            </div>
            <button class="btn btn-signal btn-block" id="convert-btn">Crop &amp; download</button>
            <button class="btn btn-outline btn-block" id="reset-btn" style="margin-top:10px">Choose a different image</button>
            <p class="note">The crop is rendered on a canvas at full resolution before download &mdash; nothing is uploaded.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</main>
"""
    script = """<script src="../js/file-utils.js"></script>
<script>
(function(){
  const dz = document.getElementById('dz');
  const input = document.getElementById('file-input');
  const err = document.getElementById('error');
  const uploader = document.getElementById('uploader');
  const editor = document.getElementById('editor');
  const stage = document.getElementById('stage');
  const canvas = document.getElementById('canvas');
  const cropbox = document.getElementById('cropbox');
  const ratioSel = document.getElementById('ratio');
  const dims = document.getElementById('cropdims');
  const btn = document.getElementById('convert-btn');
  const resetBtn = document.getElementById('reset-btn');
  const ctx = canvas.getContext('2d');

  let currentFile = null, currentImg = null, scale = 1;
  let box = { x: 40, y: 40, w: 200, h: 200 };

  function clamp(v, min, max) { return Math.max(min, Math.min(max, v)); }

  function layoutCanvas() {
    const maxW = Math.min(stage.clientWidth || 560, 560);
    const maxH = 480;
    scale = Math.min(maxW / currentImg.naturalWidth, maxH / currentImg.naturalHeight, 1);
    canvas.width = currentImg.naturalWidth * scale;
    canvas.height = currentImg.naturalHeight * scale;
    ctx.drawImage(currentImg, 0, 0, canvas.width, canvas.height);
    box = { x: canvas.width * 0.15, y: canvas.height * 0.15, w: canvas.width * 0.7, h: canvas.height * 0.7 };
    drawBox();
  }

  function drawBox() {
    cropbox.style.left = box.x + 'px';
    cropbox.style.top = box.y + 'px';
    cropbox.style.width = box.w + 'px';
    cropbox.style.height = box.h + 'px';
    const rw = Math.round(box.w / scale), rh = Math.round(box.h / scale);
    dims.textContent = rw + ' \u00d7 ' + rh + ' px';
  }

  ratioSel.addEventListener('change', () => {
    const v = ratioSel.value;
    if (v !== 'free') {
      const r = Number(v);
      let w = box.w, h = w / r;
      if (h > canvas.height) { h = canvas.height; w = h * r; }
      box.w = w; box.h = h;
      box.x = clamp(box.x, 0, canvas.width - box.w);
      box.y = clamp(box.y, 0, canvas.height - box.h);
      drawBox();
    }
  });

  let drag = null;
  cropbox.addEventListener('pointerdown', (e) => {
    const handle = e.target.dataset.h;
    drag = { handle, startX: e.clientX, startY: e.clientY, box: { ...box } };
    cropbox.setPointerCapture(e.pointerId);
  });
  cropbox.addEventListener('pointermove', (e) => {
    if (!drag) return;
    const dx = e.clientX - drag.startX, dy = e.clientY - drag.startY;
    let b = { ...drag.box };
    const ratioVal = ratioSel.value === 'free' ? null : Number(ratioSel.value);
    if (!drag.handle) {
      b.x = clamp(drag.box.x + dx, 0, canvas.width - b.w);
      b.y = clamp(drag.box.y + dy, 0, canvas.height - b.h);
    } else {
      if (drag.handle.includes('e')) b.w = clamp(drag.box.w + dx, 20, canvas.width - b.x);
      if (drag.handle.includes('s')) b.h = clamp(drag.box.h + dy, 20, canvas.height - b.y);
      if (drag.handle.includes('w')) { const nw = clamp(drag.box.w - dx, 20, drag.box.x + drag.box.w); b.x = drag.box.x + drag.box.w - nw; b.w = nw; }
      if (drag.handle.includes('n')) { const nh = clamp(drag.box.h - dy, 20, drag.box.y + drag.box.h); b.y = drag.box.y + drag.box.h - nh; b.h = nh; }
      if (ratioVal) { b.h = b.w / ratioVal; b.h = clamp(b.h, 20, canvas.height - b.y); }
    }
    box = b;
    drawBox();
  });
  cropbox.addEventListener('pointerup', () => { drag = null; });
  cropbox.addEventListener('pointerdown', (e) => { if (!e.target.dataset.h) { drag = { handle: null, startX: e.clientX, startY: e.clientY, box: { ...box } }; } });

  setupDropzone(dz, input, async (files) => {
    hideError(err);
    const file = files[0];
    if (!file.type.startsWith('image/')) { showError(err, 'Please choose an image file.'); return; }
    currentFile = file;
    try {
      const { img } = await loadImage(file);
      currentImg = img;
      uploader.style.display = 'none';
      editor.style.display = 'block';
      layoutCanvas();
    } catch (e) { showError(err, e.message); }
  });

  resetBtn.addEventListener('click', () => {
    editor.style.display = 'none';
    uploader.style.display = 'block';
    input.value = '';
  });

  btn.addEventListener('click', async () => {
    if (!currentImg) return;
    btn.disabled = true;
    btn.textContent = 'Cropping\u2026';
    try {
      const sx = box.x / scale, sy = box.y / scale, sw = box.w / scale, sh = box.h / scale;
      const out = document.createElement('canvas');
      out.width = Math.round(sw); out.height = Math.round(sh);
      const octx = out.getContext('2d');
      octx.drawImage(currentImg, sx, sy, sw, sh, 0, 0, out.width, out.height);
      const mime = currentFile.type === 'image/png' ? 'image/png' : 'image/jpeg';
      const blob = await canvasToBlob(out, mime, 0.92);
      downloadBlob(blob, stripExt(currentFile.name) + '-cropped.' + (mime === 'image/png' ? 'png' : 'jpg'));
    } finally {
      btn.disabled = false;
      btn.textContent = 'Crop & download';
    }
  });

  window.addEventListener('resize', () => { if (currentImg) layoutCanvas(); });
})();
</script>
"""
    html = TOOL_PAGE(
        title="Image Cropper &mdash; Crop Photos Online Free | Toolpeg",
        description="Crop an image freely or to a fixed ratio like 1:1, 4:5 or 16:9, directly in your browser.",
        canonical_path=f"{FOLDER}/{slug}", depth=DEPTH, active="image", body=body, slug=slug, foot_scripts=script,
    )
    write(os.path.join(ROOT, FOLDER, slug), html)


if __name__ == "__main__":
    gen_format_convert(
        "jpg-to-png.html", "JPG", "PNG", "image/png",
        "JPG to PNG Converter",
        "Convert a JPG photo to PNG format for free, right in your browser.",
        "image/jpeg",
    )
    gen_format_convert(
        "png-to-jpg.html", "PNG", "JPG", "image/jpeg",
        "PNG to JPG Converter",
        "Convert a PNG image to JPG format for free, right in your browser. Transparent areas become white.",
        "image/png",
        quality_note="Transparent areas are filled white during conversion. ",
    )
    gen_format_convert(
        "jpg-to-webp.html", "JPG", "WebP", "image/webp",
        "JPG to WebP Converter",
        "Convert a JPG photo to the smaller, modern WebP format for free, right in your browser.",
        "image/jpeg",
    )
    gen_format_convert(
        "webp-to-jpg.html", "WebP", "JPG", "image/jpeg",
        "WebP to JPG Converter",
        "Convert a WebP image to widely-supported JPG format for free, right in your browser.",
        "image/webp",
    )
    gen_format_convert(
        "png-to-webp.html", "PNG", "WebP", "image/webp",
        "PNG to WebP Converter",
        "Convert a PNG image to the smaller, modern WebP format for free, right in your browser. Transparency is preserved.",
        "image/png",
    )
    gen_compressor()
    gen_resizer()
    gen_cropper()
