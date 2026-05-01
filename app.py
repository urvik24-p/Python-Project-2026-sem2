from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

MAX_SCORE = 15


def calculate_bmi(weight_kg, height_cm):
    if height_cm <= 0:
        return 0.0
    return round(weight_kg / ((height_cm / 100) ** 2), 1)


def calculate_risk(data):
    age          = min(max(int(float(data.get('age', 25))), 1), 110)
    gender       = data.get('gender', 'male')
    weight       = min(max(float(data.get('weight', 70)), 20), 250)
    height       = min(max(float(data.get('height', 170)), 50), 220)
    sleep        = min(max(float(data.get('sleep', 7)), 0), 12)
    exercise     = data.get('exercise', '3-5')
    screen       = min(max(float(data.get('screen', 4)), 0), 14)
    diet         = data.get('diet', 'healthy')
    water        = min(max(float(data.get('water', 2)), 0), 5)
    smoking      = data.get('smoking', 'never')
    alcohol      = data.get('alcohol', 'none')
    family_hist  = data.get('family_history', [])
    stress_lvl   = min(max(int(data.get('stress_level', 3)), 1), 10)

    bmi = calculate_bmi(weight, height)

    ob = di = he = hy = st = 0

    # --- BMI ---
    if bmi >= 35:   ob += 5; di += 3; he += 2; hy += 2
    elif bmi >= 30: ob += 4; di += 2; he += 2; hy += 2
    elif bmi >= 25: ob += 2; di += 1; he += 1; hy += 1
    elif bmi < 18.5: st += 1

    # --- Sleep ---
    if sleep < 5:   st += 3; he += 2; hy += 1
    elif sleep < 6: st += 2; he += 1; hy += 1
    elif sleep < 7: st += 1
    elif sleep > 9: st += 1; ob += 1

    # --- Exercise ---
    if exercise == 'none':   ob += 3; di += 2; he += 2; st += 1
    elif exercise == '1-2':  ob += 2; di += 1; he += 1
    elif exercise == 'daily': he = max(0, he - 1)

    # --- Screen time ---
    if screen > 10:  st += 3; ob += 1
    elif screen > 8: st += 2; ob += 1
    elif screen > 6: st += 2
    elif screen > 4: st += 1

    # --- Diet ---
    if diet == 'junk':      ob += 3; di += 2; he += 2; hy += 1
    elif diet == 'moderate': ob += 1; di += 1; he += 1

    # --- Water ---
    if water < 1:   st += 2; hy += 2; ob += 1
    elif water < 1.5: st += 1; hy += 1
    elif water < 2: hy += 1

    # --- Age ---
    if age > 65:    he += 4; hy += 3; di += 2
    elif age > 55:  he += 3; hy += 2; di += 2
    elif age > 45:  he += 2; hy += 2; di += 1
    elif age > 35:  he += 1; hy += 1

    # --- Gender ---
    if gender == 'male' and age > 35:     he += 1
    elif gender == 'female' and age > 50: he += 1; hy += 1

    # --- Smoking ---
    if smoking == 'current': he += 3; hy += 2; di += 1; st += 1
    elif smoking == 'former': he += 1; hy += 1

    # --- Alcohol ---
    if alcohol == 'heavy':    he += 2; hy += 3; ob += 2
    elif alcohol == 'moderate': hy += 1

    # --- Family history ---
    if 'diabetes' in family_hist:     di += 2
    if 'heart' in family_hist:        he += 2
    if 'hypertension' in family_hist: hy += 2
    if 'obesity' in family_hist:      ob += 1

    # --- Self-reported stress ---
    if stress_lvl >= 9:   st += 4; he += 2; hy += 1
    elif stress_lvl >= 7: st += 3; he += 1; hy += 1
    elif stress_lvl >= 5: st += 2; he += 1
    elif stress_lvl >= 3: st += 1

    cap = lambda v: max(0, min(v, MAX_SCORE))
    return {
        'obesity': cap(ob), 'diabetes': cap(di), 'heart': cap(he),
        'hypertension': cap(hy), 'stress': cap(st),
        'bmi': bmi, 'max_score': MAX_SCORE
    }


def get_risk_meta(score, max_score=MAX_SCORE):
    pct = round(score / max_score * 100)
    if pct <= 25:   return {'level': 'low',      'label': 'Low Risk',      'pct': pct}
    elif pct <= 60: return {'level': 'moderate',  'label': 'Moderate Risk', 'pct': pct}
    else:           return {'level': 'high',      'label': 'High Risk',     'pct': pct}


def get_suggestions(data, scores):
    tips = []
    bmi        = scores.get('bmi', 22)
    sleep      = float(data.get('sleep', 7))
    exercise   = data.get('exercise', '3-5')
    diet       = data.get('diet', 'healthy')
    screen     = float(data.get('screen', 4))
    water      = float(data.get('water', 2))
    smoking    = data.get('smoking', 'never')
    alcohol    = data.get('alcohol', 'none')
    stress_lvl = int(data.get('stress_level', 3))
    age        = int(float(data.get('age', 25)))

    def tip(icon, cat, sev, msg, advice):
        tips.append({'icon': icon, 'category': cat, 'severity': sev,
                     'message': msg, 'tip': advice})

    if bmi >= 30:
        tip('⚖️','Weight Management','high',
            f'BMI {bmi} (Obese). Structured weight loss is strongly advised.',
            'Target 0.5–1 kg/week via calorie deficit and regular exercise.')
    elif bmi >= 25:
        tip('⚖️','Weight Management','moderate',
            f'BMI {bmi} (Overweight). Small changes will yield big benefits.',
            '30-min daily walks and reducing processed food can help significantly.')

    if sleep < 6:
        tip('😴','Sleep Health','high',
            'Under 6 h of sleep sharply raises stress, heart, and hypertension risks.',
            'Aim for 7–9 h. No screens 1 h before bed. Keep a consistent schedule.')
    elif sleep < 7:
        tip('😴','Sleep Health','moderate',
            'Slightly under the recommended sleep threshold.',
            'Try going to bed 30 min earlier. Avoid caffeine after 2 pm.')

    if exercise == 'none':
        tip('🏃','Physical Activity','high',
            'No exercise is a major risk factor for obesity, diabetes & heart disease.',
            'Start with 15 min of walking daily, building to 150 min/week.')
    elif exercise == '1-2':
        tip('🏃','Physical Activity','moderate',
            'Only 1–2 days/week is below the recommended level.',
            'Aim for 3–5 days/week mixing cardio and strength training.')

    if diet == 'junk':
        tip('🥗','Diet & Nutrition','high',
            'Frequent junk food is the top driver of obesity and diabetes risk.',
            'Swap one junk meal/day with whole foods. More fibre, less added sugar.')
    elif diet == 'moderate':
        tip('🥗','Diet & Nutrition','low',
            'Diet is moderate. Small upgrades can noticeably improve risk scores.',
            'Add vegetables, legumes, and whole grains. Reduce refined carbs.')

    if screen > 8:
        tip('📱','Screen Time','high',
            f'{screen} h/day screen time significantly impacts stress and sleep.',
            'Use app timers. Apply the 20-20-20 rule: 20s break every 20 min.')
    elif screen > 6:
        tip('📱','Screen Time','moderate',
            'High screen time is elevating your stress risk.',
            'Create tech-free zones: bedroom, dining table.')

    if water < 2:
        tip('💧','Hydration','moderate',
            'Low water intake affects blood pressure and metabolism.',
            'Carry a 1 L bottle. Drink a glass of water before every meal.')

    if smoking == 'current':
        tip('🚭','Smoking','high',
            'Smoking is the single biggest modifiable risk factor for heart disease.',
            'Seek cessation support: nicotine patches, counselling, or your GP.')

    if alcohol == 'heavy':
        tip('🍷','Alcohol','high',
            'Heavy drinking raises BP, contributes to obesity, and damages the heart.',
            'Limit to ≤14 units/week with several alcohol-free days.')

    if stress_lvl >= 7:
        tip('🧘','Stress & Mental Health','high',
            f'Reported stress {stress_lvl}/10. Chronic stress harms heart & BP.',
            'Daily 10-min breathing exercises, mindfulness, or professional support.')
    elif stress_lvl >= 5:
        tip('🧘','Stress & Mental Health','moderate',
            'Moderate stress is affecting your overall risk profile.',
            'Regular breaks, short walks, and hobby time reduce stress effectively.')

    if age > 40 and scores.get('heart', 0) > 5:
        tip('🏥','Medical Check-up','high',
            'Your age and heart risk score make regular cardiac screening important.',
            'Annual check-up: blood pressure, cholesterol panel, ECG.')

    if not tips:
        tip('🎉','Excellent Profile','low',
            'Your lifestyle looks great! Keep up the healthy habits.',
            'Schedule annual preventive health check-ups to stay on track.')
    return tips


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    raw = calculate_risk(data)
    ms  = raw['max_score']

    disease_meta = {
        'obesity':      {'name': 'Obesity',        'icon': '⚖️'},
        'diabetes':     {'name': 'Diabetes',        'icon': '🩸'},
        'heart':        {'name': 'Heart Disease',   'icon': '❤️'},
        'hypertension': {'name': 'Hypertension',    'icon': '🫀'},
        'stress':       {'name': 'Stress Disorder', 'icon': '🧠'},
    }

    results = {}
    for key, meta in disease_meta.items():
        score = raw[key]
        rm = get_risk_meta(score, ms)
        results[key] = {**meta, 'score': score, 'max_score': ms,
                        'level': rm['level'], 'label': rm['label'],
                        'percentage': rm['pct']}

    avg_pct = sum(r['percentage'] for r in results.values()) / len(results)
    if avg_pct <= 25:   overall = {'level': 'low',      'label': 'Low Overall Risk',      'percentage': round(avg_pct)}
    elif avg_pct <= 55: overall = {'level': 'moderate',  'label': 'Moderate Overall Risk', 'percentage': round(avg_pct)}
    else:               overall = {'level': 'high',      'label': 'High Overall Risk',     'percentage': round(avg_pct)}

    bmi = raw['bmi']
    if bmi < 18.5:  bmi_cat = 'Underweight'
    elif bmi < 25:  bmi_cat = 'Normal'
    elif bmi < 30:  bmi_cat = 'Overweight'
    else:           bmi_cat = 'Obese'

    return jsonify({
        'results': results,
        'overall': overall,
        'suggestions': get_suggestions(data, raw),
        'bmi': bmi,
        'bmi_category': bmi_cat,
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)