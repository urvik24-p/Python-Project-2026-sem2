# 🩺 VitalPredict – Predict Today, Protect Tomorrow

> An advanced, full-stack **Lifestyle Disease Risk Analyzer** built with Python Flask and modern HTML/CSS/JS.

![VitalPredict Banner](static/assets/logo.png)

---

## 🌟 Features

- 🔍 **5 Disease Risk Predictions** — Obesity, Diabetes, Heart Disease, Hypertension, Stress Disorder
- 📊 **Interactive Charts** — Radar profile chart + horizontal bar chart (Chart.js)
- 🧠 **10+ Risk Factors** — Age, BMI, sleep, exercise, diet, screen time, smoking, alcohol, family history, stress level
- ⚖️ **Live BMI Calculator** — Auto-calculates as you type weight & height
- ⚠️ **Smart Validation & Warnings** — Real-time amber warnings for medically extreme inputs
- 💡 **Personalised Recommendations** — Tailored health tips per risk factor
- 🎨 **Premium Dark UI** — Glassmorphism design with teal/purple gradient accents
- 📱 **Fully Responsive** — Works on mobile, tablet, and desktop

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Charts | Chart.js |
| Fonts | Google Fonts (Outfit + Inter) |
| Deployment | Render.com + Gunicorn |

---

## 🚀 Run Locally

### Prerequisites
- Python 3.10+

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/urvik24-p/Python-Project-2026-sem2.git
cd Python-Project-2026-sem2

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py

# 4. Open in browser
# Navigate to http://127.0.0.1:5000
```

---

## 📁 Project Structure

```
├── app.py                  # Flask backend + risk engine API
├── main.py                 # Original CLI version (preserved)
├── requirements.txt        # Python dependencies
├── Procfile                # Render deployment config
├── runtime.txt             # Python version for Render
├── templates/
│   └── index.html          # Full SPA frontend
└── static/
    ├── css/
    │   └── style.css       # Premium dark-mode design system
    ├── js/
    │   └── app.js          # Frontend logic, charts, wizard
    └── assets/
        └── logo.png        # App logo
```

---

## 🧠 Risk Factors Analyzed

| Factor | Diseases Affected |
|---|---|
| BMI (auto-calculated) | Obesity, Diabetes, Heart, Hypertension |
| Age | Heart, Hypertension, Diabetes |
| Sleep hours (0–12 h) | Stress, Heart, Hypertension |
| Exercise frequency | Obesity, Diabetes, Heart |
| Diet quality | Obesity, Diabetes, Heart, Hypertension |
| Screen time (0–14 h) | Stress, Obesity |
| Water intake (0–5 L) | Hypertension, Stress |
| Smoking status | Heart, Hypertension, Diabetes |
| Alcohol consumption | Heart, Hypertension, Obesity |
| Family history | Diabetes, Heart, Hypertension, Obesity |
| Self-reported stress | Stress, Heart, Hypertension |

---

## ⚠️ Disclaimer

VitalPredict is for **educational and informational purposes only**. It does not constitute medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional for medical guidance.

---

## 👨‍💻 Author

**Urvik** — Python Project 2026 Sem 2

---

## 📄 License

MIT License — free to use and modify.
