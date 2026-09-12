# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from site_lib import PAGE, TOOL_PAGE, write

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
FOLDER = "qr-tools"
DEPTH = "../"
QRLIB = '<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>'


def gen_qr():
    slug = "qr-code-generator.html"
    body = f"""<main class="tool-shell">
  <div class="wrap">
    <p class="breadcrumb"><a href="../index.html">Home</a> / <a href="index.html">QR Tools</a> / QR Code Generator</p>
    <div class="tool-head">
      <span class="tag">Generate</span>
      <h1>QR Code Generator</h1>
      <p>Turn a link, plain text, or a Wi-Fi login into a QR code you can download as a PNG.</p>
    </div>
    <div class="grid-2">
      <div class="panel">
        <div class="field">
          <label for="qtype">Content type</label>
          <select id="qtype">
            <option value="url">Website link</option>
            <option value="text">Plain text</option>
            <option value="wifi">Wi-Fi network</option>
          </select>
        </div>
        <div id="fields-url" class="qr-fields">
          <div class="field"><label for="url-input">URL</label><input type="text" id="url-input" placeholder="https://example.com" value="https://example.com"></div>
        </div>
        <div id="fields-text" class="qr-fields" style="display:none">
          <div class="field"><label for="text-input">Text</label><textarea id="text-input" placeholder="Anything you want encoded"></textarea></div>
        </div>
        <div id="fields-wifi" class="qr-fields" style="display:none">
          <div class="field"><label for="wifi-ssid">Network name (SSID)</label><input type="text" id="wifi-ssid" placeholder="My Wi-Fi"></div>
          <div class="field"><label for="wifi-pass">Password</label><input type="text" id="wifi-pass" placeholder="Password"></div>
          <div class="field">
            <label for="wifi-enc">Security</label>
            <select id="wifi-enc"><option value="WPA">WPA/WPA2</option><option value="WEP">WEP</option><option value="nopass">None</option></select>
          </div>
        </div>
        <div class="row">
          <div class="field"><label for="size">Size (px)</label><input type="number" id="size" value="320" min="128" max="1024" step="32"></div>
          <div class="field"><label for="ecl">Error correction</label>
            <select id="ecl"><option value="L">Low</option><option value="M" selected>Medium</option><option value="Q">Quartile</option><option value="H">High</option></select>
          </div>
        </div>
      </div>
      <div class="panel" style="text-align:center">
        <div id="qr-canvas-wrap" style="display:inline-block;padding:16px;background:#fff;border:1px solid var(--hairline);border-radius:6px"></div>
        <div id="error" class="error-box" style="text-align:left"></div>
        <button class="btn btn-signal btn-block" id="download-btn" style="margin-top:18px">Download PNG</button>
        <p class="note">The QR code is generated locally in your browser and never sent anywhere.</p>
      </div>
    </div>
  </div>
</main>
"""
    script = f"""{QRLIB}
<script src="../js/file-utils.js"></script>
<script>
(function(){{
  const qtype = document.getElementById('qtype');
  const wrap = document.getElementById('qr-canvas-wrap');
  const err = document.getElementById('error');
  const sizeEl = document.getElementById('size');
  const eclEl = document.getElementById('ecl');
  const downloadBtn = document.getElementById('download-btn');
  let qr = null, debounceT = null;

  document.querySelectorAll('.qr-fields').forEach(el => el.style.display = 'none');
  document.getElementById('fields-' + qtype.value).style.display = 'block';
  qtype.addEventListener('change', () => {{
    document.querySelectorAll('.qr-fields').forEach(el => el.style.display = 'none');
    document.getElementById('fields-' + qtype.value).style.display = 'block';
    render();
  }});

  function escapeWifi(s) {{ return (s || '').replace(/([\\\\;,:"])/g, '\\\\$1'); }}

  function buildContent() {{
    if (qtype.value === 'url') {{
      let v = document.getElementById('url-input').value.trim();
      if (v && !/^[a-zA-Z][a-zA-Z0-9+.-]*:\\/\\//.test(v)) v = 'https://' + v;
      return v;
    }}
    if (qtype.value === 'text') return document.getElementById('text-input').value;
    if (qtype.value === 'wifi') {{
      const ssid = escapeWifi(document.getElementById('wifi-ssid').value);
      const pass = escapeWifi(document.getElementById('wifi-pass').value);
      const enc = document.getElementById('wifi-enc').value;
      return 'WIFI:T:' + enc + ';S:' + ssid + ';P:' + (enc === 'nopass' ? '' : pass) + ';;';
    }}
    return '';
  }}

  function render() {{
    hideError(err);
    const content = buildContent();
    wrap.innerHTML = '';
    if (!content) {{ return; }}
    if (!window.QRCode) {{ showError(err, "Couldn't load the QR engine. Check your connection and try again."); return; }}
    const size = Math.max(128, Math.min(1024, Number(sizeEl.value) || 320));
    try {{
      qr = new QRCode(wrap, {{
        text: content,
        width: size,
        height: size,
        correctLevel: QRCode.CorrectLevel[eclEl.value] || QRCode.CorrectLevel.M,
      }});
    }} catch (e) {{
      showError(err, 'Could not generate a QR code for that input.');
    }}
  }}

  ['input', 'change'].forEach(evt => {{
    document.getElementById('fields-url').addEventListener(evt, debounced);
    document.getElementById('fields-text').addEventListener(evt, debounced);
    document.getElementById('fields-wifi').addEventListener(evt, debounced);
    sizeEl.addEventListener(evt, debounced);
    eclEl.addEventListener(evt, debounced);
  }});
  function debounced() {{ clearTimeout(debounceT); debounceT = setTimeout(render, 200); }}

  downloadBtn.addEventListener('click', () => {{
    const canvas = wrap.querySelector('canvas');
    const img = wrap.querySelector('img');
    if (canvas) {{
      canvas.toBlob((blob) => downloadBlob(blob, 'qr-code.png'));
    }} else if (img) {{
      downloadBlob(dataURLtoBlob(img.src), 'qr-code.png');
    }} else {{
      showError(err, 'Generate a QR code first.');
    }}
  }});

  function dataURLtoBlob(dataUrl) {{
    const [meta, b64] = dataUrl.split(',');
    const mime = meta.match(/:(.*?);/)[1];
    const bin = atob(b64);
    const arr = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
    return new Blob([arr], {{ type: mime }});
  }}

  render();
}})();
</script>
"""
    write(os.path.join(ROOT, FOLDER, slug), TOOL_PAGE(
        title="QR Code Generator &mdash; Free, No Sign-up | Toolpeg",
        description="Generate a QR code for a link, plain text, or a Wi-Fi login and download it as a PNG, free and in your browser.",
        canonical_path=f"{FOLDER}/{slug}", depth=DEPTH, active="qr", body=body, slug=slug, foot_scripts=script))


if __name__ == "__main__":
    gen_qr()
