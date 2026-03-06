import streamlit as st
import matplotlib.pyplot as plt

# Page title
st.title("🏥 LifeStyle Disease Risk Analyzer")
 
#   input section

age = st.number_input("Enter your age", min_value=1, max_value=100)
sleep = st.number_input("Sleep hours per day", min_value=0.0, max_value=24.0)
exercise = st.selectbox("Exercise Frequency",
                        ["None", "1-2 days", "3-5 days", "Daily"])
screen = st.number_input("Screen time hours per day", min_value=0.0, max_value=24.0)
diet = st.selectbox("Diet Type",
                    ["Healthy", "Moderate", "Junk food often"])
water = st.number_input("Water intake (litres per day)", min_value=0.0, max_value=10.0)

# logic function

def calculate_risk(age, sleep, exercise, screen, diet, water):

    obesity = diabetes = heart = hypertension = stress = 0

    if sleep < 6:
        stress += 2
        heart += 1
        hypertension += 1

    if exercise == "None":
        obesity += 2
        diabetes += 2
        heart += 2
        stress += 1
    elif exercise == "1-2 days":
        obesity += 1
        diabetes += 1

    if screen > 7:
        stress += 2
        obesity += 1

    if diet == "Junk food often":
        obesity += 3
        diabetes += 2
        heart += 2
        hypertension += 1
    elif diet == "Moderate":
        obesity += 1
        diabetes += 1

    if water < 2:
        stress += 1
        hypertension += 1

    if age > 40:
        heart += 2
        hypertension += 2
        diabetes += 1

    return obesity, diabetes, heart, hypertension, stress


def risk_level(score):
    if score <= 2:
        return "Low ✅"
    elif score <= 5:
        return "Moderate ⚠️"
    else:
        return "High 🔴"


# ---------------- BUTTON ----------------

if st.button("Analyze My Health Risk"):

    obesity, diabetes, heart, hypertension, stress = calculate_risk(
        age, sleep, exercise, screen, diet, water
    )

    st.subheader("📊 Health Risk Report")

    st.write("**Obesity Risk:**", risk_level(obesity))
    st.write("**Diabetes Risk:**", risk_level(diabetes))
    st.write("**Heart Disease Risk:**", risk_level(heart))
    st.write("**Hypertension Risk:**", risk_level(hypertension))
    st.write("**Stress Risk:**", risk_level(stress))

    st.subheader("💡 Suggestions")

    if sleep < 7:
        st.write("✔ Improve sleep to 7–8 hours")
    if exercise in ["None", "1-2 days"]:
        st.write("✔ Exercise at least 3 times per week")
    if diet == "Junk food often":
        st.write("✔ Reduce junk food consumption")
    if screen > 6:
        st.write("✔ Reduce screen time")
    if water < 2:
        st.write("✔ Drink at least 2–3 litres of water daily")

    # -------- Graph --------
    diseases = ["Obesity", "Diabetes", "Heart", "Hypertension", "Stress"]
    scores = [obesity, diabetes, heart, hypertension, stress]

    fig, ax = plt.subplots()
    ax.bar(diseases, scores)
    ax.set_label("Risk Score")
    ax.set_title("Lifestyle Disease Risk Analysis")

    st.pyplot(fig)