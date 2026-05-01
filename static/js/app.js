/* ── VitalPredict Frontend Logic ─────────────────────────────────── */

let currentStep = 1;
let stressLevel = 3;
let radarChartInst = null;
let barChartInst   = null;

/* ── Real-time Warning Helpers ───────────────────────────────────── */
function showWarn(id, grpId, msg) {
  const el  = document.getElementById(id);
  const grp = grpId ? document.getElementById(grpId) : null;
  if (msg) {
    el.textContent = ' ' + msg;
    el.classList.add('show');
    if (grp) grp.classList.add('warning');
  } else {
    el.textContent = '';
    el.classList.remove('show');
    if (grp) grp.classList.remove('warning');
  }
}

function warnAge(v) {
  v = parseFloat(v);
  if (!v) return showWarn('warn-age','grp-age','');
  if (v > 110)      showWarn('warn-age','grp-age','Age over 110 is extremely rare. Please double-check.');
  else if (v > 90)  showWarn('warn-age','grp-age','Age 90+ — risk scores will reflect advanced-age factors.');
  else if (v < 5)   showWarn('warn-age','grp-age','Very young age. Results are optimised for adults.');
  else              showWarn('warn-age','grp-age','');
}

function warnWeight(v) {
  v = parseFloat(v);
  if (!v) return showWarn('warn-weight','grp-weight','');
  if (v > 200)     showWarn('warn-weight','grp-weight','Weight above 200 kg — please consult a specialist.');
  else if (v > 150) showWarn('warn-weight','grp-weight','High weight — obesity risk factors heavily applied.');
  else if (v < 35)  showWarn('warn-weight','grp-weight','Very low weight — underweight indicators active.');
  else              showWarn('warn-weight','grp-weight','');
}

function warnHeight(v) {
  v = parseFloat(v);
  if (!v) return showWarn('warn-height','grp-height','');
  if (v > 210)     showWarn('warn-height','grp-height','Height over 210 cm is very unusual. Please verify.');
  else if (v < 100) showWarn('warn-height','grp-height','Height under 100 cm — BMI will reflect this.');
  else              showWarn('warn-height','grp-height','');
}

function warnSleep(v) {
  v = parseFloat(v);
  if (v <= 0)       showWarn('warn-sleep', null, 'Zero sleep entered — this will trigger maximum stress and heart risk.');
  else if (v < 4)   showWarn('warn-sleep', null, 'Less than 4 h is severely insufficient. High risk of cardiac and stress disorders.');
  else if (v < 6)   showWarn('warn-sleep', null, 'Under 6 h/day is below healthy range. Stress and heart risks elevated.');
  else if (v > 10)  showWarn('warn-sleep', null, 'Sleeping over 10 h can indicate underlying health issues.');
  else if (v > 9)   showWarn('warn-sleep', null, 'Over 9 h is above average adult need — slight obesity risk applied.');
  else              showWarn('warn-sleep', null, '');
}

function warnScreen(v) {
  v = parseFloat(v);
  if (v > 12)      showWarn('warn-screen', null, 'Over 12 h screen time — extreme stress and sedentary risk. Strongly reconsider.');
  else if (v > 8)  showWarn('warn-screen', null, 'Over 8 h is very high. Significant stress & obesity risk factors applied.');
  else if (v > 6)  showWarn('warn-screen', null, 'High screen time — stress risk elevated.');
  else             showWarn('warn-screen', null, '');
}

function warnWater(v) {
  v = parseFloat(v);
  if (v > 4.5)     showWarn('warn-water', null, 'Over 4.5 L/day — excessive intake can cause hyponatremia. Consult a doctor.');
  else if (v > 4)  showWarn('warn-water', null, 'High intake. 2–3 L/day is optimal for most adults.');
  else if (v < 0.5 && v > 0) showWarn('warn-water', null, 'Critically low hydration — serious health risk.');
  else if (v <= 0) showWarn('warn-water', null, 'Zero water intake — hypertension and stress risks maximised.');
  else             showWarn('warn-water', null, '');
}

/* ── Stress meter ────────────────────────────────────────────────── */
function buildStressMeter() {
  const wrap = document.getElementById('stressMeter');
  wrap.innerHTML = '';
  for (let i = 1; i <= 10; i++) {
    const btn = document.createElement('button');
    btn.className = 'stress-btn' + (i === stressLevel ? ' active' : '');
    btn.textContent = i;
    btn.type = 'button';
    btn.onclick = () => setStress(i);
    wrap.appendChild(btn);
  }
}

function setStress(val) {
  stressLevel = val;
  document.getElementById('stressLabel').textContent = val + '/10';
  document.querySelectorAll('.stress-btn').forEach((b, i) => {
    b.classList.toggle('active', i + 1 === val);
  });
}

/* ── Range label sync ────────────────────────────────────────────── */
function updateLabel(id, val, suffix) {
  document.getElementById(id).textContent = parseFloat(val) + suffix;
}

/* ── BMI live calc ───────────────────────────────────────────────── */
function calcBmi() {
  const w = parseFloat(document.getElementById('inp-weight').value);
  const h = parseFloat(document.getElementById('inp-height').value);
  const disp = document.getElementById('bmiDisplay');
  if (!w || !h || h <= 0) { disp.style.display = 'none'; return; }
  const bmi = +(w / ((h / 100) ** 2)).toFixed(1);
  let cat = 'Normal';
  if (bmi < 18.5)     cat = 'Underweight';
  else if (bmi < 25)  cat = 'Normal';
  else if (bmi < 30)  cat = 'Overweight';
  else                cat = 'Obese';
  document.getElementById('bmiValue').textContent = bmi;
  document.getElementById('bmiCat').textContent   = cat;
  disp.style.display = 'flex';
}

document.getElementById('inp-weight').addEventListener('input', calcBmi);
document.getElementById('inp-height').addEventListener('input', calcBmi);

/* ── Validation ──────────────────────────────────────────────────── */
function validate(fields) {
  let ok = true;
  fields.forEach(({ id, grp, test }) => {
    const el  = document.getElementById(id);
    const grpEl = document.getElementById(grp);
    const pass = test(el.value);
    grpEl.classList.toggle('error', !pass);
    if (!pass) ok = false;
  });
  return ok;
}

const step1Fields = [
  { id: 'inp-age',    grp: 'grp-age',    test: v => v && +v >= 1   && +v <= 110 },
  { id: 'inp-gender', grp: 'grp-gender', test: v => v !== '' },
  { id: 'inp-weight', grp: 'grp-weight', test: v => v && +v >= 20  && +v <= 250 },
  { id: 'inp-height', grp: 'grp-height', test: v => v && +v >= 50  && +v <= 220 },
];
const step2Fields = [
  { id: 'inp-exercise', grp: 'grp-exercise', test: v => v !== '' },
  { id: 'inp-diet',     grp: 'grp-diet',     test: v => v !== '' },
];
const step3Fields = [
  { id: 'inp-smoking', grp: 'grp-smoking', test: v => v !== '' },
  { id: 'inp-alcohol', grp: 'grp-alcohol', test: v => v !== '' },
];

/* ── Wizard navigation ───────────────────────────────────────────── */
function goNext(step) {
  let ok = false;
  if (step === 1) ok = validate(step1Fields);
  if (step === 2) ok = validate(step2Fields);
  if (!ok) return;
  showStep(step + 1);
}

function goBack(step) { showStep(step - 1); }

function showStep(n) {
  [1, 2, 3].forEach(i => {
    document.getElementById('panel' + i).classList.toggle('active', i === n);
    document.getElementById('dot' + i).classList.remove('active', 'done');
    document.getElementById('lbl' + i).classList.remove('active');
    if (i < n)  { document.getElementById('dot' + i).classList.add('done'); if(i<3) document.getElementById('line'+i).classList.add('done'); }
    if (i === n){ document.getElementById('dot' + i).classList.add('active'); document.getElementById('lbl'+i).classList.add('active'); }
    if (i > n)  { if(i<=3) try{document.getElementById('line'+(i-1)).classList.remove('done');}catch(e){} }
  });
  currentStep = n;
}

/* ── Analysis ────────────────────────────────────────────────────── */
async function runAnalysis() {
  if (!validate(step3Fields)) return;

  const familyHistory = ['fh-diabetes','fh-heart','fh-hypertension','fh-obesity']
    .filter(id => document.getElementById(id).checked)
    .map(id => document.getElementById(id).value);

  const payload = {
    age:            document.getElementById('inp-age').value,
    gender:         document.getElementById('inp-gender').value,
    weight:         document.getElementById('inp-weight').value,
    height:         document.getElementById('inp-height').value,
    sleep:          document.getElementById('inp-sleep').value,
    exercise:       document.getElementById('inp-exercise').value,
    screen:         document.getElementById('inp-screen').value,
    diet:           document.getElementById('inp-diet').value,
    water:          document.getElementById('inp-water').value,
    smoking:        document.getElementById('inp-smoking').value,
    alcohol:        document.getElementById('inp-alcohol').value,
    family_history: familyHistory,
    stress_level:   stressLevel,
  };

  document.getElementById('loadingOverlay').classList.add('show');

  try {
    const res  = await fetch('/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    renderResults(data);
  } catch (e) {
    alert('Something went wrong. Please try again.');
  } finally {
    document.getElementById('loadingOverlay').classList.remove('show');
  }
}

/* ── Render Results ──────────────────────────────────────────────── */
function renderResults(data) {
  const { results, overall, suggestions, bmi, bmi_category } = data;

  /* Banner */
  const banner = document.getElementById('overallBanner');
  banner.className = 'overall-banner ' + overall.level;
  const icons = { low: '💚', moderate: '⚠️', high: '🚨' };
  document.getElementById('overallIcon').textContent  = icons[overall.level];
  document.getElementById('overallPct').textContent   = overall.percentage + '%';
  document.getElementById('overallLabel').textContent = overall.label;
  const descs = {
    low:      'Your overall lifestyle risk is low. Keep maintaining these healthy habits!',
    moderate: 'Some risk factors need attention. Follow the recommendations below.',
    high:     'Your risk profile is elevated. Please consult a healthcare professional.',
  };
  document.getElementById('overallDesc').textContent = descs[overall.level];
  document.getElementById('resBmi').textContent    = bmi;
  document.getElementById('resBmiCat').textContent = bmi_category;

  /* Risk Cards */
  const cardsWrap = document.getElementById('riskCards');
  cardsWrap.innerHTML = '';
  Object.values(results).forEach(r => {
    const card = document.createElement('div');
    card.className = 'risk-card ' + r.level;
    card.innerHTML = `
      <div class="rc-icon">${r.icon}</div>
      <div class="rc-name">${r.name}</div>
      <div class="rc-score" data-target="${r.score}">0</div>
      <div class="rc-label">${r.label}</div>
      <div class="rc-bar"><div class="rc-bar-fill" data-pct="${r.percentage}"></div></div>`;
    cardsWrap.appendChild(card);
  });

  /* Animate scores */
  setTimeout(() => {
    document.querySelectorAll('.rc-score').forEach(el => countUp(el, +el.dataset.target));
    document.querySelectorAll('.rc-bar-fill').forEach(el => { el.style.width = el.dataset.pct + '%'; });
  }, 200);

  /* Charts */
  renderCharts(results);

  /* Suggestions */
  const sugWrap = document.getElementById('suggestionsGrid');
  sugWrap.innerHTML = '';
  suggestions.forEach(s => {
    const card = document.createElement('div');
    card.className = 'sug-card ' + s.severity;
    card.innerHTML = `
      <div class="sug-header">
        <span class="sug-icon">${s.icon}</span>
        <span class="sug-cat">${s.category}</span>
      </div>
      <p class="sug-msg">${s.message}</p>
      <p class="sug-tip">${s.tip}</p>`;
    sugWrap.appendChild(card);
  });

  /* Show results */
  const sec = document.getElementById('resultsSection');
  sec.classList.add('visible');
  setTimeout(() => sec.scrollIntoView({ behavior: 'smooth', block: 'start' }), 100);
}

/* ── Charts ──────────────────────────────────────────────────────── */
function renderCharts(results) {
  const labels = Object.values(results).map(r => r.name);
  const scores = Object.values(results).map(r => r.score);
  const maxSc  = Object.values(results)[0].max_score;
  const colors = Object.values(results).map(r =>
    r.level === 'low' ? '#10b981' : r.level === 'moderate' ? '#f59e0b' : '#ef4444');

  const darkGrid = 'rgba(255,255,255,0.07)';
  const textCol  = '#94a3b8';
  const defFont  = { family: 'Inter, sans-serif', size: 12 };

  /* Radar */
  if (radarChartInst) radarChartInst.destroy();
  radarChartInst = new Chart(document.getElementById('radarChart'), {
    type: 'radar',
    data: {
      labels,
      datasets: [{
        label: 'Risk Score',
        data: scores,
        backgroundColor: 'rgba(0,212,170,0.15)',
        borderColor: '#00d4aa',
        pointBackgroundColor: colors,
        pointBorderColor: '#fff',
        pointRadius: 5,
        borderWidth: 2,
      }],
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      scales: {
        r: {
          min: 0, max: maxSc,
          ticks: { color: textCol, backdropColor: 'transparent', font: defFont, stepSize: 3 },
          grid:  { color: darkGrid },
          angleLines: { color: darkGrid },
          pointLabels: { color: textCol, font: { family: 'Inter,sans-serif', size: 11 } },
        },
      },
      plugins: { legend: { display: false } },
    },
  });

  /* Bar */
  if (barChartInst) barChartInst.destroy();
  barChartInst = new Chart(document.getElementById('barChart'), {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Risk Score',
        data: scores,
        backgroundColor: colors.map(c => c + 'cc'),
        borderColor: colors,
        borderWidth: 2,
        borderRadius: 8,
        borderSkipped: false,
      }],
    },
    options: {
      indexAxis: 'y',
      responsive: true, maintainAspectRatio: false,
      scales: {
        x: { min: 0, max: maxSc, grid: { color: darkGrid }, ticks: { color: textCol, font: defFont } },
        y: { grid: { display: false }, ticks: { color: textCol, font: defFont } },
      },
      plugins: { legend: { display: false } },
    },
  });
}

/* ── Count-up animation ──────────────────────────────────────────── */
function countUp(el, target) {
  let start = 0;
  const dur = 800;
  const step = 16;
  const inc  = target / (dur / step);
  const timer = setInterval(() => {
    start += inc;
    if (start >= target) { el.textContent = target; clearInterval(timer); }
    else el.textContent = Math.floor(start);
  }, step);
}

/* ── Re-analyze ──────────────────────────────────────────────────── */
function reanalyze() {
  document.getElementById('resultsSection').classList.remove('visible');
  showStep(1);
  document.getElementById('analyzer').scrollIntoView({ behavior: 'smooth' });
}

/* ── Navbar scroll ───────────────────────────────────────────────── */
window.addEventListener('scroll', () => {
  document.getElementById('navbar').style.boxShadow =
    window.scrollY > 40 ? '0 4px 30px rgba(0,0,0,0.5)' : 'none';
});

/* ── Intersection observer for fade-in ──────────────────────────── */
const observer = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.style.animationDelay = '0s'; e.target.classList.add('fade-in'); }});
}, { threshold: 0.1 });
document.querySelectorAll('.step-card, .tip-card').forEach(el => observer.observe(el));

/* ── Init ────────────────────────────────────────────────────────── */
buildStressMeter();
