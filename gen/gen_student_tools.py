# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from site_lib import PAGE, TOOL_PAGE, write

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
FOLDER = "student-tools"
DEPTH = "../"


def breadcrumb(tool_label):
    return f'<p class="breadcrumb"><a href="../index.html">Home</a> / <a href="index.html">Student Tools</a> / {tool_label}</p>'


def tool_head(tag, title, desc):
    return f"""<span class="tag">{tag}</span>
    <h1>{title}</h1>
    <p>{desc}</p>"""


# --------------------------------------------------------------- GPA
def gen_gpa():
    slug = "gpa-calculator.html"
    body = f"""<main class="tool-shell">
  <div class="wrap">
    {breadcrumb('GPA Calculator')}
    <div class="tool-head">
      {tool_head('Grades', 'GPA Calculator', 'Add each course with its credit hours and letter grade to get your semester GPA on a standard 4.0 scale.')}
    </div>
    <div class="grid-2">
      <div>
        <div class="panel">
          <div id="rows"></div>
          <button class="btn btn-outline" id="add-row" style="margin-top:6px">+ Add course</button>
        </div>
      </div>
      <div>
        <div class="panel">
          <div class="field">
            <label for="scale">Grading scale</label>
            <select id="scale">
              <option value="4">4.0 scale (A=4.0)</option>
              <option value="4.3">4.3 scale (A+=4.3)</option>
            </select>
          </div>
          <div class="result-box">
            <span class="label">Semester GPA</span>
            <div class="big" id="gpa-out">0.00</div>
            <div class="sub" id="credits-out">0 total credit hours</div>
          </div>
          <p class="note">Grade points: A/A+ = 4.0&ndash;4.3, A- = 3.7, B+ = 3.3, B = 3.0, B- = 2.7, C+ = 2.3, C = 2.0, C- = 1.7, D+ = 1.3, D = 1.0, F = 0.0. Adjust to match your institution's exact scale if it differs.</p>
        </div>
      </div>
    </div>
  </div>
</main>
"""
    script = """<script>
(function(){
  const rowsEl = document.getElementById('rows');
  const addBtn = document.getElementById('add-row');
  const scaleEl = document.getElementById('scale');
  const gpaOut = document.getElementById('gpa-out');
  const creditsOut = document.getElementById('credits-out');

  const GRADES_4 = { 'A':4.0,'A-':3.7,'B+':3.3,'B':3.0,'B-':2.7,'C+':2.3,'C':2.0,'C-':1.7,'D+':1.3,'D':1.0,'D-':0.7,'F':0.0 };
  const GRADES_43 = Object.assign({}, GRADES_4, { 'A+':4.3 });

  function gradeOptions(map) {
    return Object.keys(map).map(g => `<option value="${g}">${g}</option>`).join('');
  }

  function addRow(name, credits, grade) {
    const map = scaleEl.value === '4.3' ? GRADES_43 : GRADES_4;
    const row = document.createElement('div');
    row.className = 'row';
    row.style.marginBottom = '10px';
    row.innerHTML = `
      <div class="field" style="margin-bottom:0;flex:2">
        <input type="text" placeholder="Course name" class="course-name" value="${name || ''}">
      </div>
      <div class="field" style="margin-bottom:0;flex:1;min-width:90px">
        <input type="number" placeholder="Credits" min="0" step="0.5" class="course-credits" value="${credits || 3}">
      </div>
      <div class="field" style="margin-bottom:0;flex:1;min-width:90px">
        <select class="course-grade">${gradeOptions(map)}</select>
      </div>
      <button class="btn btn-outline remove-row" style="flex:0 0 auto;padding:11px 14px">&times;</button>
    `;
    rowsEl.appendChild(row);
    if (grade) row.querySelector('.course-grade').value = grade;
    row.querySelector('.remove-row').addEventListener('click', () => { row.remove(); calc(); });
    row.querySelectorAll('input,select').forEach(el => el.addEventListener('input', calc));
  }

  function calc() {
    const map = scaleEl.value === '4.3' ? GRADES_43 : GRADES_4;
    let totalPoints = 0, totalCredits = 0;
    rowsEl.querySelectorAll('.row').forEach(row => {
      const credits = parseFloat(row.querySelector('.course-credits').value) || 0;
      const grade = row.querySelector('.course-grade').value;
      const points = map[grade] !== undefined ? map[grade] : 0;
      totalPoints += credits * points;
      totalCredits += credits;
    });
    gpaOut.textContent = totalCredits ? (totalPoints / totalCredits).toFixed(2) : '0.00';
    creditsOut.textContent = totalCredits + ' total credit hours';
  }

  scaleEl.addEventListener('change', () => {
    document.querySelectorAll('.course-grade').forEach(sel => {
      const cur = sel.value;
      const map = scaleEl.value === '4.3' ? GRADES_43 : GRADES_4;
      sel.innerHTML = gradeOptions(map);
      if (map[cur] !== undefined) sel.value = cur;
    });
    calc();
  });

  addBtn.addEventListener('click', () => addRow());
  addRow('', 3, 'A');
  addRow('', 3, 'B+');
  addRow('', 3, 'A-');
  calc();
})();
</script>
"""
    write(os.path.join(ROOT, FOLDER, slug), TOOL_PAGE(
        title="GPA Calculator &mdash; Free Semester GPA Calculator | Toolpeg",
        description="Calculate your semester GPA by entering course credits and letter grades. Supports 4.0 and 4.3 scales.",
        canonical_path=f"{FOLDER}/{slug}", depth=DEPTH, active="student", body=body, slug=slug, foot_scripts=script))


# ------------------------------------------------------------ percentage
def gen_percentage():
    slug = "percentage-calculator.html"
    body = f"""<main class="tool-shell">
  <div class="wrap">
    {breadcrumb('Percentage Calculator')}
    <div class="tool-head">
      {tool_head('Grades', 'Percentage Calculator', 'Three common percentage questions in one tool: what percent a score is, what score you need, and percent change.')}
    </div>
    <div class="panel" style="margin-bottom:16px">
      <div class="field">
        <label for="mode">What do you want to work out?</label>
        <select id="mode">
          <option value="score">What percent is X out of Y?</option>
          <option value="target">What score do I need to get a target percent?</option>
          <option value="change">Percent change from X to Y</option>
        </select>
      </div>
    </div>
    <div class="grid-2">
      <div class="panel" id="inputs"></div>
      <div class="panel">
        <div class="result-box">
          <span class="label" id="result-label">Result</span>
          <div class="big" id="result-out">&mdash;</div>
          <div class="sub" id="result-sub"></div>
        </div>
      </div>
    </div>
  </div>
</main>
"""
    script = """<script>
(function(){
  const mode = document.getElementById('mode');
  const inputs = document.getElementById('inputs');
  const label = document.getElementById('result-label');
  const out = document.getElementById('result-out');
  const sub = document.getElementById('result-sub');

  const templates = {
    score: `
      <div class="row">
        <div class="field"><label for="a">Score (X)</label><input type="number" id="a" value="85"></div>
        <div class="field"><label for="b">Out of (Y)</label><input type="number" id="b" value="100"></div>
      </div>`,
    target: `
      <div class="row">
        <div class="field"><label for="a">Out of (Y)</label><input type="number" id="a" value="100"></div>
        <div class="field"><label for="b">Target percent (%)</label><input type="number" id="b" value="90"></div>
      </div>`,
    change: `
      <div class="row">
        <div class="field"><label for="a">From (X)</label><input type="number" id="a" value="60"></div>
        <div class="field"><label for="b">To (Y)</label><input type="number" id="b" value="75"></div>
      </div>`,
  };

  function render() {
    inputs.innerHTML = templates[mode.value];
    inputs.querySelectorAll('input').forEach(el => el.addEventListener('input', calc));
    calc();
  }

  function calc() {
    const a = parseFloat(document.getElementById('a').value);
    const b = parseFloat(document.getElementById('b').value);
    if (isNaN(a) || isNaN(b)) { out.textContent = '\u2014'; sub.textContent = ''; return; }
    if (mode.value === 'score') {
      label.textContent = 'Percentage';
      if (b === 0) { out.textContent = '\u2014'; sub.textContent = "Can't divide by zero"; return; }
      const pct = (a / b) * 100;
      out.textContent = pct.toFixed(2) + '%';
      sub.textContent = a + ' out of ' + b;
    } else if (mode.value === 'target') {
      label.textContent = 'Score needed';
      const needed = (b / 100) * a;
      out.textContent = needed.toFixed(2);
      sub.textContent = 'out of ' + a + ' to reach ' + b + '%';
    } else {
      label.textContent = 'Percent change';
      if (a === 0) { out.textContent = '\u2014'; sub.textContent = "Can't divide by zero"; return; }
      const change = ((b - a) / Math.abs(a)) * 100;
      out.textContent = (change >= 0 ? '+' : '') + change.toFixed(2) + '%';
      sub.textContent = change >= 0 ? 'increase' : 'decrease';
    }
  }

  mode.addEventListener('change', render);
  render();
})();
</script>
"""
    write(os.path.join(ROOT, FOLDER, slug), TOOL_PAGE(
        title="Percentage Calculator &mdash; Free Online Tool | Toolpeg",
        description="Work out what percent a score is, what score hits a target percentage, or percent change between two numbers.",
        canonical_path=f"{FOLDER}/{slug}", depth=DEPTH, active="student", body=body, slug=slug, foot_scripts=script))


# ------------------------------------------------------------------ age
def gen_age():
    slug = "age-calculator.html"
    body = f"""<main class="tool-shell">
  <div class="wrap">
    {breadcrumb('Age Calculator')}
    <div class="tool-head">
      {tool_head('Dates', 'Age Calculator', 'Get an exact age in years, months and days, calculated to any date you choose.')}
    </div>
    <div class="grid-2">
      <div class="panel">
        <div class="field">
          <label for="dob">Date of birth</label>
          <input type="date" id="dob">
        </div>
        <div class="field">
          <label for="asof">Calculate age as of</label>
          <input type="date" id="asof">
        </div>
      </div>
      <div class="panel">
        <div class="result-box">
          <span class="label">Exact age</span>
          <div class="big" id="age-out">&mdash;</div>
          <div class="sub" id="age-sub"></div>
        </div>
        <p class="note" id="days-out" style="margin-top:14px"></p>
      </div>
    </div>
  </div>
</main>
"""
    script = """<script>
(function(){
  const dob = document.getElementById('dob');
  const asof = document.getElementById('asof');
  const out = document.getElementById('age-out');
  const sub = document.getElementById('age-sub');
  const daysOut = document.getElementById('days-out');

  function calc() {
    if (!dob.value) { out.textContent = '\u2014'; sub.textContent = ''; daysOut.textContent = ''; return; }
    const start = new Date(dob.value + 'T00:00:00');
    const end = asof.value ? new Date(asof.value + 'T00:00:00') : new Date();
    if (end < start) { out.textContent = '\u2014'; sub.textContent = 'End date is before birth date'; daysOut.textContent = ''; return; }
    let years = end.getFullYear() - start.getFullYear();
    let months = end.getMonth() - start.getMonth();
    let days = end.getDate() - start.getDate();
    if (days < 0) {
      months -= 1;
      const prevMonth = new Date(end.getFullYear(), end.getMonth(), 0);
      days += prevMonth.getDate();
    }
    if (months < 0) { months += 12; years -= 1; }
    out.textContent = years + ' yr';
    sub.textContent = months + ' months, ' + days + ' days';
    const totalDays = Math.round((end - start) / 86400000);
    daysOut.innerHTML = '<strong>' + totalDays.toLocaleString() + '</strong> total days &middot; ' + Math.round(totalDays / 7).toLocaleString() + ' weeks &middot; ' + (years * 12 + months) + ' full months';
  }

  const today = new Date().toISOString().slice(0, 10);
  asof.value = today;
  dob.addEventListener('input', calc);
  asof.addEventListener('input', calc);
})();
</script>
"""
    write(os.path.join(ROOT, FOLDER, slug), TOOL_PAGE(
        title="Age Calculator &mdash; Exact Age in Years, Months, Days | Toolpeg",
        description="Calculate exact age in years, months and days from a birth date, as of today or any date you choose.",
        canonical_path=f"{FOLDER}/{slug}", depth=DEPTH, active="student", body=body, slug=slug, foot_scripts=script))


# ---------------------------------------------------------- std deviation
def gen_stddev():
    slug = "standard-deviation-calculator.html"
    body = f"""<main class="tool-shell">
  <div class="wrap">
    {breadcrumb('Standard Deviation Calculator')}
    <div class="tool-head">
      {tool_head('Statistics', 'Standard Deviation Calculator', 'Enter a list of numbers to get the mean, variance and standard deviation for a population or a sample.')}
    </div>
    <div class="grid-2">
      <div class="panel">
        <div class="field">
          <label for="data">Data set (comma or space separated)</label>
          <textarea id="data">4, 8, 6, 5, 3, 2, 8, 9, 2, 5</textarea>
        </div>
        <div class="field">
          <label for="kind">Calculation type</label>
          <select id="kind">
            <option value="sample">Sample standard deviation</option>
            <option value="population">Population standard deviation</option>
          </select>
        </div>
      </div>
      <div class="panel">
        <div class="result-box">
          <span class="label">Standard deviation</span>
          <div class="big" id="sd-out">&mdash;</div>
        </div>
        <p class="note" id="stats-out" style="margin-top:14px"></p>
      </div>
    </div>
  </div>
</main>
"""
    script = """<script>
(function(){
  const data = document.getElementById('data');
  const kind = document.getElementById('kind');
  const out = document.getElementById('sd-out');
  const stats = document.getElementById('stats-out');

  function parse() {
    return (data.value.match(/-?\\d+(\\.\\d+)?/g) || []).map(Number);
  }

  function calc() {
    const nums = parse();
    if (nums.length < 2) { out.textContent = '\u2014'; stats.textContent = 'Enter at least two numbers.'; return; }
    const n = nums.length;
    const mean = nums.reduce((a, b) => a + b, 0) / n;
    const sqDiffs = nums.map(x => (x - mean) ** 2);
    const sumSq = sqDiffs.reduce((a, b) => a + b, 0);
    const divisor = kind.value === 'sample' ? (n - 1) : n;
    const variance = sumSq / divisor;
    const sd = Math.sqrt(variance);
    out.textContent = sd.toFixed(4);
    stats.innerHTML = '<strong>n</strong> = ' + n + ' &middot; <strong>mean</strong> = ' + mean.toFixed(4) + ' &middot; <strong>variance</strong> = ' + variance.toFixed(4) + ' &middot; <strong>sum</strong> = ' + nums.reduce((a,b)=>a+b,0).toFixed(2);
  }

  data.addEventListener('input', calc);
  kind.addEventListener('change', calc);
  calc();
})();
</script>
"""
    write(os.path.join(ROOT, FOLDER, slug), TOOL_PAGE(
        title="Standard Deviation Calculator &mdash; Free Online Tool | Toolpeg",
        description="Calculate mean, variance and standard deviation (sample or population) from a list of numbers.",
        canonical_path=f"{FOLDER}/{slug}", depth=DEPTH, active="student", body=body, slug=slug, foot_scripts=script))


# ------------------------------------------------------------- scientific
def gen_scientific():
    slug = "scientific-calculator.html"
    keys = [
        ("7","7"),("8","8"),("9","9"),("/","\u00f7"),("sin(","sin"),
        ("4","4"),("5","5"),("6","6"),("*","\u00d7"),("cos(","cos"),
        ("1","1"),("2","2"),("3","3"),("-","\u2212"),("tan(","tan"),
        ("0","0"),(".","."),("00","00"),("+","+"),("log(","log"),
        ("(","("),(")",")"),("^","^"),("sqrt(","\u221ax"),("ln(","ln"),
        ("pi","\u03c0"),("e","e"),("%","%"),("!","x!"),("=","="),
    ]
    key_html = []
    for val, label in keys:
        extra_class = " key-eq" if val == "=" else ""
        key_html.append(f'<button class="calc-key{extra_class}" data-val="{val}">{label}</button>')
    body = f"""<main class="tool-shell">
  <div class="wrap">
    {breadcrumb('Scientific Calculator')}
    <div class="tool-head">
      {tool_head('Math', 'Scientific Calculator', 'Trig, logs, powers, roots and constants, plus memory keys. Type or click, and your keyboard works too.')}
    </div>
    <div class="grid-2">
      <div>
        <div class="panel">
          <input type="text" id="expr" style="width:100%;font-family:var(--font-mono);font-size:22px;border:none;text-align:right;background:transparent;color:var(--ink);padding:8px 4px 4px" value="" placeholder="0" autocomplete="off">
          <div id="expr-result" style="text-align:right;font-family:var(--font-mono);color:var(--steel-light);font-size:13px;min-height:18px;padding:0 4px 12px">&nbsp;</div>
          <div id="calc-grid" style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px">
            {''.join(key_html)}
          </div>
          <div class="row" style="margin-top:8px">
            <button class="btn btn-outline btn-block" id="clear-btn">Clear</button>
            <button class="btn btn-outline btn-block" id="back-btn">&larr; Backspace</button>
          </div>
        </div>
      </div>
      <div>
        <div class="panel">
          <div class="field">
            <label>Memory</label>
            <div id="mem-out" style="font-family:var(--font-mono);font-size:20px">0</div>
          </div>
          <div class="row">
            <button class="btn btn-outline" id="mc">MC</button>
            <button class="btn btn-outline" id="mplus">M+</button>
            <button class="btn btn-outline" id="mminus">M-</button>
            <button class="btn btn-outline" id="mr">MR</button>
          </div>
          <p class="note">Angles are in radians. Use <code>pi</code> and <code>e</code> as constants, <code>sqrt(</code> for a square root, and <code>^</code> for a power &mdash; e.g. <code>2^10</code> or <code>sin(pi/2)</code>.</p>
        </div>
      </div>
    </div>
  </div>
</main>
"""
    script = r"""<script>
(function(){
  const expr = document.getElementById('expr');
  const resultLine = document.getElementById('expr-result');
  const memOut = document.getElementById('mem-out');
  let memory = 0;

  function factorial(n) {
    if (n < 0 || Math.floor(n) !== n) return NaN;
    let r = 1;
    for (let i = 2; i <= n; i++) r *= i;
    return r;
  }

  function safeEval(input) {
    let s = input
      .replace(/\u00f7/g, '/')
      .replace(/\u00d7/g, '*')
      .replace(/\u2212/g, '-')
      .replace(/\^/g, '**')
      .replace(/pi/g, 'Math.PI')
      .replace(/\be\b/g, 'Math.E')
      .replace(/sqrt\(/g, 'Math.sqrt(')
      .replace(/sin\(/g, 'Math.sin(')
      .replace(/cos\(/g, 'Math.cos(')
      .replace(/tan\(/g, 'Math.tan(')
      .replace(/log\(/g, 'Math.log10(')
      .replace(/ln\(/g, 'Math.log(');
    s = s.replace(/(\d+(\.\d+)?)!/g, 'FACT($1)');
    if (!/^[0-9+\-*/().\s,MathPIElogsqrtincoat\^FACT]*$/i.test(s)) {
      // allow-list check loosely; fall through to Function eval with try/catch as final guard
    }
    // eslint-disable-next-line no-new-func
    const fn = new Function('FACT', 'return (' + s + ')');
    return fn(factorial);
  }

  function updatePreview() {
    if (!expr.value.trim()) { resultLine.innerHTML = '&nbsp;'; return; }
    try {
      const val = safeEval(expr.value);
      resultLine.textContent = (typeof val === 'number' && isFinite(val)) ? ('= ' + round(val)) : '';
    } catch (e) { resultLine.innerHTML = '&nbsp;'; }
  }

  function round(n) { return Math.round(n * 1e10) / 1e10; }

  document.querySelectorAll('.calc-key').forEach(btn => {
    btn.addEventListener('click', () => {
      const val = btn.dataset.val;
      if (val === '=') {
        try {
          const result = round(safeEval(expr.value));
          expr.value = String(result);
        } catch (e) { resultLine.textContent = 'Error'; return; }
      } else {
        expr.value += val;
      }
      updatePreview();
      expr.focus();
    });
  });

  document.getElementById('clear-btn').addEventListener('click', () => { expr.value = ''; updatePreview(); });
  document.getElementById('back-btn').addEventListener('click', () => { expr.value = expr.value.slice(0, -1); updatePreview(); });
  expr.addEventListener('input', updatePreview);
  expr.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      try { expr.value = String(round(safeEval(expr.value))); updatePreview(); } catch (er) { resultLine.textContent = 'Error'; }
    }
  });

  document.getElementById('mc').addEventListener('click', () => { memory = 0; memOut.textContent = memory; });
  document.getElementById('mplus').addEventListener('click', () => { try { memory += safeEval(expr.value || '0'); } catch(e){} memOut.textContent = round(memory); });
  document.getElementById('mminus').addEventListener('click', () => { try { memory -= safeEval(expr.value || '0'); } catch(e){} memOut.textContent = round(memory); });
  document.getElementById('mr').addEventListener('click', () => { expr.value += String(memory); updatePreview(); });
})();
</script>
<style>
  #calc-grid .calc-key{font-family:var(--font-mono);font-size:15px;padding:14px 0;border-radius:var(--radius);border:1px solid var(--hairline);background:#fff;cursor:pointer;transition:background .12s,border-color .12s}
  #calc-grid .calc-key:hover{border-color:var(--ink)}
  #calc-grid .key-eq{background:var(--signal);border-color:var(--signal);color:var(--signal-ink);font-weight:600}
</style>
"""
    write(os.path.join(ROOT, FOLDER, slug), TOOL_PAGE(
        title="Scientific Calculator &mdash; Free Online Tool | Toolpeg",
        description="A free online scientific calculator with trig functions, logarithms, powers, roots and memory keys.",
        canonical_path=f"{FOLDER}/{slug}", depth=DEPTH, active="student", body=body, slug=slug, foot_scripts=script))


# ------------------------------------------------------------- CGPA
def gen_cgpa():
    slug = "cgpa-calculator.html"
    body = f"""<main class="tool-shell">
  <div class="wrap">
    {breadcrumb('CGPA Calculator')}
    <div class="tool-head">
      {tool_head('Grades', 'CGPA Calculator', 'Combine multiple semesters of GPA and credit hours into one credit-weighted cumulative GPA.')}
    </div>
    <div class="grid-2">
      <div>
        <div class="panel">
          <div id="rows"></div>
          <button class="btn btn-outline" id="add-row" style="margin-top:6px">+ Add semester</button>
        </div>
      </div>
      <div>
        <div class="panel">
          <div class="result-box">
            <span class="label">Cumulative GPA (CGPA)</span>
            <div class="big" id="cgpa-out">0.00</div>
            <div class="sub" id="credits-out">0 total credit hours</div>
          </div>
          <p class="note">CGPA is a credit-weighted average: each semester's GPA counts in proportion to how many credit hours it covered, not as a flat average of the GPA numbers.</p>
        </div>
      </div>
    </div>
  </div>
</main>
"""
    script = """<script>
(function(){
  const rowsEl = document.getElementById('rows');
  const addBtn = document.getElementById('add-row');
  const cgpaOut = document.getElementById('cgpa-out');
  const creditsOut = document.getElementById('credits-out');

  function addRow(name, gpa, credits) {
    const row = document.createElement('div');
    row.className = 'row';
    row.style.marginBottom = '10px';
    row.innerHTML = `
      <div class="field" style="margin-bottom:0;flex:2">
        <input type="text" placeholder="Semester name" class="sem-name" value="${name || ''}">
      </div>
      <div class="field" style="margin-bottom:0;flex:1;min-width:90px">
        <input type="number" placeholder="GPA" min="0" max="4.3" step="0.01" class="sem-gpa" value="${gpa !== undefined ? gpa : ''}">
      </div>
      <div class="field" style="margin-bottom:0;flex:1;min-width:90px">
        <input type="number" placeholder="Credits" min="0" step="0.5" class="sem-credits" value="${credits !== undefined ? credits : ''}">
      </div>
      <button class="btn btn-outline remove-row" style="flex:0 0 auto;padding:11px 14px">&times;</button>
    `;
    rowsEl.appendChild(row);
    row.querySelector('.remove-row').addEventListener('click', () => { row.remove(); calc(); });
    row.querySelectorAll('input').forEach(el => el.addEventListener('input', calc));
  }

  function calc() {
    let totalPoints = 0, totalCredits = 0;
    rowsEl.querySelectorAll('.row').forEach(row => {
      const gpa = parseFloat(row.querySelector('.sem-gpa').value) || 0;
      const credits = parseFloat(row.querySelector('.sem-credits').value) || 0;
      totalPoints += gpa * credits;
      totalCredits += credits;
    });
    cgpaOut.textContent = totalCredits ? (totalPoints / totalCredits).toFixed(2) : '0.00';
    creditsOut.textContent = totalCredits + ' total credit hours';
  }

  addBtn.addEventListener('click', () => addRow());
  addRow('Semester 1', 3.6, 15);
  addRow('Semester 2', 3.8, 16);
  addRow('Semester 3', 3.5, 15);
  calc();
})();
</script>
"""
    write(os.path.join(ROOT, FOLDER, slug), TOOL_PAGE(
        title="CGPA Calculator &mdash; Free Cumulative GPA Calculator | Toolpeg",
        description="Calculate your cumulative GPA (CGPA) across multiple semesters, weighted correctly by credit hours.",
        canonical_path=f"{FOLDER}/{slug}", depth=DEPTH, active="student", body=body, slug=slug, foot_scripts=script))


# ------------------------------------------------------- final grade calc
def gen_grade():
    slug = "grade-calculator.html"
    body = f"""<main class="tool-shell">
  <div class="wrap">
    {breadcrumb('Final Grade Calculator')}
    <div class="tool-head">
      {tool_head('Grades', 'Final Grade Calculator', 'Enter each grading category weight and your score to get your overall weighted grade.')}
    </div>
    <div class="grid-2">
      <div>
        <div class="panel">
          <div id="rows"></div>
          <button class="btn btn-outline" id="add-row" style="margin-top:6px">+ Add category</button>
        </div>
      </div>
      <div>
        <div class="panel">
          <div class="result-box">
            <span class="label">Weighted final grade</span>
            <div class="big" id="grade-out">0.00%</div>
            <div class="sub" id="weight-out"></div>
          </div>
          <p class="note">Weight and score are both percentages. If your weights don't add up to 100%, the result is still normalized correctly by the total weight you've entered.</p>
        </div>
      </div>
    </div>
  </div>
</main>
"""
    script = """<script>
(function(){
  const rowsEl = document.getElementById('rows');
  const addBtn = document.getElementById('add-row');
  const gradeOut = document.getElementById('grade-out');
  const weightOut = document.getElementById('weight-out');

  function addRow(name, weight, score) {
    const row = document.createElement('div');
    row.className = 'row';
    row.style.marginBottom = '10px';
    row.innerHTML = `
      <div class="field" style="margin-bottom:0;flex:2">
        <input type="text" placeholder="Category (e.g. Homework)" class="cat-name" value="${name || ''}">
      </div>
      <div class="field" style="margin-bottom:0;flex:1;min-width:90px">
        <input type="number" placeholder="Weight %" min="0" max="100" step="1" class="cat-weight" value="${weight !== undefined ? weight : ''}">
      </div>
      <div class="field" style="margin-bottom:0;flex:1;min-width:90px">
        <input type="number" placeholder="Score %" min="0" max="100" step="1" class="cat-score" value="${score !== undefined ? score : ''}">
      </div>
      <button class="btn btn-outline remove-row" style="flex:0 0 auto;padding:11px 14px">&times;</button>
    `;
    rowsEl.appendChild(row);
    row.querySelector('.remove-row').addEventListener('click', () => { row.remove(); calc(); });
    row.querySelectorAll('input').forEach(el => el.addEventListener('input', calc));
  }

  function calc() {
    let weightedSum = 0, totalWeight = 0;
    rowsEl.querySelectorAll('.row').forEach(row => {
      const weight = parseFloat(row.querySelector('.cat-weight').value) || 0;
      const score = parseFloat(row.querySelector('.cat-score').value) || 0;
      weightedSum += weight * score;
      totalWeight += weight;
    });
    gradeOut.textContent = totalWeight ? (weightedSum / totalWeight).toFixed(2) + '%' : '0.00%';
    weightOut.textContent = 'total weight entered: ' + totalWeight + '%';
  }

  addBtn.addEventListener('click', () => addRow());
  addRow('Homework', 20, 90);
  addRow('Midterm', 30, 82);
  addRow('Final Exam', 50, 88);
  calc();
})();
</script>
"""
    write(os.path.join(ROOT, FOLDER, slug), TOOL_PAGE(
        title="Final Grade Calculator &mdash; Weighted Grade Calculator | Toolpeg",
        description="Calculate your overall course grade from weighted categories like homework, exams and participation.",
        canonical_path=f"{FOLDER}/{slug}", depth=DEPTH, active="student", body=body, slug=slug, foot_scripts=script))


# -------------------------------------------------------- attendance calc
def gen_attendance():
    slug = "attendance-calculator.html"
    body = f"""<main class="tool-shell">
  <div class="wrap">
    {breadcrumb('Attendance Calculator')}
    <div class="tool-head">
      {tool_head('Grades', 'Attendance Calculator', 'Check your attendance percentage and how many more classes you can miss.')}
    </div>
    <div class="grid-2">
      <div class="panel">
        <div class="row">
          <div class="field"><label for="held">Classes held so far</label><input type="number" id="held" min="0" value="40"></div>
          <div class="field"><label for="attended">Classes you attended</label><input type="number" id="attended" min="0" value="34"></div>
        </div>
        <div class="row">
          <div class="field"><label for="required">Required attendance (%)</label><input type="number" id="required" min="0" max="100" value="75"></div>
          <div class="field"><label for="total">Total classes this term (optional)</label><input type="number" id="total" min="0" placeholder="e.g. 60"></div>
        </div>
      </div>
      <div class="panel">
        <div class="result-box">
          <span class="label">Your current attendance</span>
          <div class="big" id="pct-out">&mdash;</div>
        </div>
        <p class="note" id="advice-out" style="margin-top:14px"></p>
      </div>
    </div>
  </div>
</main>
"""
    script = """<script>
(function(){
  const held = document.getElementById('held');
  const attended = document.getElementById('attended');
  const required = document.getElementById('required');
  const total = document.getElementById('total');
  const pctOut = document.getElementById('pct-out');
  const adviceOut = document.getElementById('advice-out');

  function calc() {
    const h = Math.max(0, Number(held.value) || 0);
    const a = Math.max(0, Math.min(h, Number(attended.value) || 0));
    const req = Math.max(0, Math.min(100, Number(required.value) || 0));
    const t = Number(total.value) || 0;

    if (h === 0) { pctOut.textContent = '\u2014'; adviceOut.textContent = 'Enter how many classes have been held so far.'; return; }

    const currentPct = (a / h) * 100;
    pctOut.textContent = currentPct.toFixed(1) + '%';

    let advice = a + ' attended out of ' + h + ' classes held so far.';

    if (currentPct >= req) {
      if (t > h) {
        const remaining = t - h;
        const maxAdditionalAbsences = Math.max(0, Math.floor(a + remaining - (req / 100) * t));
        advice += ' You can miss up to ' + Math.min(maxAdditionalAbsences, remaining) + ' more of the remaining ' + remaining + ' classes and stay at or above ' + req + '%.';
      } else {
        advice += ' You are currently meeting the ' + req + '% requirement.';
      }
    } else {
      if (req < 100) {
        const n = Math.ceil(((req / 100) * h - a) / (1 - req / 100));
        advice += ' You are below the ' + req + '% requirement. Attending the next ' + n + ' class(es) in a row, with no further absences, would bring you back up to ' + req + '%.';
      } else {
        advice += ' You are below the required 100% attendance and cannot mathematically reach it after a missed class.';
      }
    }
    adviceOut.textContent = advice;
  }

  [held, attended, required, total].forEach(el => el.addEventListener('input', calc));
  calc();
})();
</script>
"""
    write(os.path.join(ROOT, FOLDER, slug), TOOL_PAGE(
        title="Attendance Calculator &mdash; Free Online Tool | Toolpeg",
        description="Calculate your attendance percentage and see how many classes you can still miss while meeting a required minimum.",
        canonical_path=f"{FOLDER}/{slug}", depth=DEPTH, active="student", body=body, slug=slug, foot_scripts=script))


if __name__ == "__main__":
    gen_gpa()
    gen_cgpa()
    gen_percentage()
    gen_grade()
    gen_attendance()
    gen_age()
    gen_stddev()
    gen_scientific()
