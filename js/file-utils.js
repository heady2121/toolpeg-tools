// Shared helpers used across tool pages. No data ever leaves the browser —
// every function here operates on local Blobs/Files/Canvases only.

function humanFileSize(bytes) {
  if (bytes < 1024) return bytes + ' B';
  const units = ['KB', 'MB', 'GB'];
  let u = -1;
  do { bytes /= 1024; u++; } while (Math.abs(bytes) >= 1024 && u < units.length - 1);
  return bytes.toFixed(1) + ' ' + units[u];
}

function stripExt(name) {
  const i = name.lastIndexOf('.');
  return i > 0 ? name.slice(0, i) : name;
}

function setupDropzone(dz, input, onFiles) {
  dz.addEventListener('click', () => input.click());
  dz.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); input.click(); } });
  dz.addEventListener('dragover', (e) => { e.preventDefault(); dz.classList.add('dragover'); });
  dz.addEventListener('dragleave', () => dz.classList.remove('dragover'));
  dz.addEventListener('drop', (e) => {
    e.preventDefault();
    dz.classList.remove('dragover');
    if (e.dataTransfer.files && e.dataTransfer.files.length) onFiles(e.dataTransfer.files);
  });
  input.addEventListener('change', () => { if (input.files.length) onFiles(input.files); });
}

function loadImage(file) {
  return new Promise((resolve, reject) => {
    const url = URL.createObjectURL(file);
    const img = new Image();
    img.onload = () => resolve({ img, url });
    img.onerror = () => reject(new Error('Could not read that image file.'));
    img.src = url;
  });
}

function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 4000);
}

function showError(box, msg) {
  if (!box) return;
  box.textContent = msg;
  box.classList.add('show');
}

function hideError(box) {
  if (!box) return;
  box.classList.remove('show');
  box.textContent = '';
}

function canvasToBlob(canvas, type, quality) {
  return new Promise((resolve, reject) => {
    canvas.toBlob((blob) => {
      if (blob) resolve(blob); else reject(new Error('Conversion failed in this browser.'));
    }, type, quality);
  });
}
