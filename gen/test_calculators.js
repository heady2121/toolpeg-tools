const { JSDOM } = require("jsdom");
const fs = require("fs");
const path = require("path");

function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }

async function loadPage(relPath) {
  const html = fs.readFileSync(path.join(__dirname, "..", relPath), "utf8");
  const dom = new JSDOM(html, { runScripts: "dangerously", resources: "usable", url: "http://localhost/" + relPath });
  await sleep(300);
  return dom;
}

function fire(el, type) {
  el.dispatchEvent(new el.ownerDocument.defaultView.Event(type, { bubbles: true }));
}

let failures = 0;
function assert(name, cond, extra) {
  if (cond) {
    console.log("PASS:", name);
  } else {
    console.log("FAIL:", name, extra || "");
    failures++;
  }
}

// -------------------- GPA calculator --------------------
async function testGPA() {
  const dom = await loadPage("student-tools/gpa-calculator.html");
  const doc = dom.window.document;
  const gpaOut = doc.getElementById("gpa-out");
  const expected = ((4.0 + 3.3 + 3.7) * 3) / 9;
  assert("GPA default calc ~3.67", Math.abs(parseFloat(gpaOut.textContent) - expected) < 0.01, gpaOut.textContent);

  const rows = doc.querySelectorAll("#rows .row");
  rows[0].querySelector(".course-credits").value = 4;
  fire(rows[0].querySelector(".course-credits"), "input");
  rows[0].querySelector(".course-grade").value = "F";
  fire(rows[0].querySelector(".course-grade"), "input");
  const totalCredits = 4 + 3 + 3;
  const totalPoints = 4 * 0 + 3 * 3.3 + 3 * 3.7;
  const expected2 = totalPoints / totalCredits;
  assert("GPA recalculates after edit", Math.abs(parseFloat(gpaOut.textContent) - expected2) < 0.01, gpaOut.textContent + " vs " + expected2.toFixed(2));
}

// -------------------- CGPA calculator (new) --------------------
async function testCGPA() {
  const dom = await loadPage("student-tools/cgpa-calculator.html");
  const doc = dom.window.document;
  const out = doc.getElementById("cgpa-out");
  // default rows: (3.6*15 + 3.8*16 + 3.5*15) / (15+16+16... wait credits: 15+16+15=46)
  const expected = (3.6 * 15 + 3.8 * 16 + 3.5 * 15) / (15 + 16 + 15);
  assert("CGPA default weighted calc", Math.abs(parseFloat(out.textContent) - expected) < 0.01, out.textContent + " vs " + expected.toFixed(2));

  // Add a 4th semester and confirm it recalculates
  const addBtn = doc.getElementById("add-row");
  addBtn.dispatchEvent(new dom.window.Event("click", { bubbles: true }));
  const rows = doc.querySelectorAll("#rows .row");
  const last = rows[rows.length - 1];
  last.querySelector(".sem-gpa").value = 4.0;
  last.querySelector(".sem-credits").value = 10;
  fire(last.querySelector(".sem-gpa"), "input");
  fire(last.querySelector(".sem-credits"), "input");
  const expected2 = (3.6 * 15 + 3.8 * 16 + 3.5 * 15 + 4.0 * 10) / (15 + 16 + 15 + 10);
  assert("CGPA recalculates after adding a semester", Math.abs(parseFloat(out.textContent) - expected2) < 0.01, out.textContent + " vs " + expected2.toFixed(2));

  // Sanity: simple average would give a DIFFERENT number than credit-weighted (proves it's not just averaging)
  const simpleAvg = (3.6 + 3.8 + 3.5 + 4.0) / 4;
  assert("CGPA is credit-weighted, not a flat average", Math.abs(parseFloat(out.textContent) - simpleAvg) > 0.001, out.textContent + " vs flat avg " + simpleAvg.toFixed(2));
}

// -------------------- Percentage calculator --------------------
async function testPercentage() {
  const dom = await loadPage("student-tools/percentage-calculator.html");
  const doc = dom.window.document;
  const out = doc.getElementById("result-out");
  assert("Percentage default 85/100 = 85.00%", out.textContent.trim() === "85.00%", out.textContent);

  const mode = doc.getElementById("mode");
  mode.value = "target";
  fire(mode, "change");
  const a = doc.getElementById("a"), b = doc.getElementById("b");
  a.value = 100; b.value = 90;
  fire(a, "input"); fire(b, "input");
  assert("Target score needed = 90.00", out.textContent.trim() === "90.00", out.textContent);

  mode.value = "change";
  fire(mode, "change");
  const a2 = doc.getElementById("a"), b2 = doc.getElementById("b");
  a2.value = 60; b2.value = 75;
  fire(a2, "input"); fire(b2, "input");
  assert("Percent change 60->75 = +25.00%", out.textContent.trim() === "+25.00%", out.textContent);
}

// -------------------- Final Grade calculator (new) --------------------
async function testGrade() {
  const dom = await loadPage("student-tools/grade-calculator.html");
  const doc = dom.window.document;
  const out = doc.getElementById("grade-out");
  // default rows: Homework 20/90, Midterm 30/82, Final 50/88
  const expected = (20 * 90 + 30 * 82 + 50 * 88) / (20 + 30 + 50);
  assert("Final grade default weighted calc", out.textContent.trim() === expected.toFixed(2) + "%", out.textContent + " vs " + expected.toFixed(2) + "%");

  // Edit final exam score to 100 and confirm recalculation
  const rows = doc.querySelectorAll("#rows .row");
  const finalRow = rows[rows.length - 1];
  finalRow.querySelector(".cat-score").value = 100;
  fire(finalRow.querySelector(".cat-score"), "input");
  const expected2 = (20 * 90 + 30 * 82 + 50 * 100) / (20 + 30 + 50);
  assert("Final grade recalculates after edit", out.textContent.trim() === expected2.toFixed(2) + "%", out.textContent + " vs " + expected2.toFixed(2) + "%");
}

// -------------------- Attendance calculator (new) --------------------
async function testAttendance() {
  const dom = await loadPage("student-tools/attendance-calculator.html");
  const doc = dom.window.document;
  const pctOut = doc.getElementById("pct-out");
  // defaults: held=40, attended=34 -> 85.0%
  assert("Attendance default 34/40 = 85.0%", pctOut.textContent.trim() === "85.0%", pctOut.textContent);

  const held = doc.getElementById("held"), attended = doc.getElementById("attended"), required = doc.getElementById("required"), total = doc.getElementById("total");

  // Case: above requirement, with a known total -> can compute max additional absences
  held.value = 40; attended.value = 34; required.value = 75; total.value = 60;
  [held, attended, required, total].forEach(el => fire(el, "input"));
  const remaining = 60 - 40; // 20
  const maxAdditional = Math.max(0, Math.floor(34 + remaining - (75 / 100) * 60));
  const advice = doc.getElementById("advice-out").textContent;
  assert("Attendance shows correct max additional absences", advice.includes("miss up to " + Math.min(maxAdditional, remaining) + " more"), advice);

  // Case: below requirement -> shows recovery classes needed
  held.value = 20; attended.value = 10; required.value = 80; total.value = "";
  [held, attended, required, total].forEach(el => fire(el, "input"));
  const n = Math.ceil(((80 / 100) * 20 - 10) / (1 - 80 / 100));
  const advice2 = doc.getElementById("advice-out").textContent;
  assert("Attendance shows correct recovery class count when below requirement", advice2.includes("next " + n + " class"), advice2 + " (expected n=" + n + ")");
}

// -------------------- Age calculator --------------------
async function testAge() {
  const dom = await loadPage("student-tools/age-calculator.html");
  const doc = dom.window.document;
  const dob = doc.getElementById("dob");
  const asof = doc.getElementById("asof");
  dob.value = "2000-01-15";
  asof.value = "2026-08-16";
  fire(dob, "input");
  fire(asof, "input");
  const out = doc.getElementById("age-out").textContent;
  const sub = doc.getElementById("age-sub").textContent;
  assert("Age years = 26 yr", out.trim() === "26 yr", out);
  assert("Age months/days = 7 months, 1 days", sub.trim() === "7 months, 1 days", sub);
}

// -------------------- Standard deviation calculator --------------------
async function testStdDev() {
  const dom = await loadPage("student-tools/standard-deviation-calculator.html");
  const doc = dom.window.document;
  const data = doc.getElementById("data");
  const kind = doc.getElementById("kind");
  data.value = "2, 4, 4, 4, 5, 5, 7, 9";
  fire(data, "input");
  kind.value = "population";
  fire(kind, "change");
  const out = doc.getElementById("sd-out").textContent;
  assert("Population stddev of classic set = 2.0000", out.trim() === "2.0000", out);

  kind.value = "sample";
  fire(kind, "change");
  const out2 = doc.getElementById("sd-out").textContent;
  assert("Sample stddev differs from population", out2.trim() !== "2.0000", out2);
}

// -------------------- Scientific calculator --------------------
async function testScientific() {
  const dom = await loadPage("student-tools/scientific-calculator.html");
  const doc = dom.window.document;
  const expr = doc.getElementById("expr");
  const eqBtn = doc.querySelector('.calc-key[data-val="="]');

  expr.value = "2^10";
  fire(expr, "input");
  eqBtn.dispatchEvent(new dom.window.Event("click", { bubbles: true }));
  assert("2^10 = 1024", expr.value === "1024", expr.value);

  expr.value = "sqrt(64)";
  fire(expr, "input");
  eqBtn.dispatchEvent(new dom.window.Event("click", { bubbles: true }));
  assert("sqrt(64) = 8", expr.value === "8", expr.value);

  expr.value = "5!";
  fire(expr, "input");
  eqBtn.dispatchEvent(new dom.window.Event("click", { bubbles: true }));
  assert("5! = 120", expr.value === "120", expr.value);

  expr.value = "sin(pi/2)";
  fire(expr, "input");
  eqBtn.dispatchEvent(new dom.window.Event("click", { bubbles: true }));
  assert("sin(pi/2) = 1", expr.value === "1", expr.value);
}

(async function main() {
  await testGPA();
  await testCGPA();
  await testPercentage();
  await testGrade();
  await testAttendance();
  await testAge();
  await testStdDev();
  await testScientific();
  console.log("\n" + (failures === 0 ? "ALL TESTS PASSED" : failures + " TEST(S) FAILED"));
  process.exit(failures === 0 ? 0 : 1);
})();
