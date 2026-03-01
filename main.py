import matplotlib.pyplot as plt
def calculate_risk(age, sleep, exercise, screen, diet, water):

    obesity = 0
    diabetes = 0
    heart = 0
    hypertension = 0
    stress = 0

    # Sleep
    if sleep < 6:
        stress += 2
        heart += 1
        hypertension += 1

    # Exercise
    if exercise == "none":
        obesity += 2
        diabetes += 2
        heart += 2
        stress += 1
    elif exercise == "1-2 days":
        obesity += 1
        diabetes += 1

    # Screen Time
    if screen > 7:
        stress += 2
        obesity += 1

    # Diet
    if diet == "junk food often":
        obesity += 3
        diabetes += 2
        heart += 2
        hypertension += 1
    elif diet == "moderate":
        obesity += 1
        diabetes += 1

    # Water Intake
    if water < 2:
        stress += 1
        hypertension += 1

    # Age Factor
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


# ---------------- MAIN PROGRAM ----------------

print("----- Lifestyle Disease Risk Analyzer -----\n")

age = int(input("Enter your age: "))
sleep = float(input("Sleep hours per day: "))
exercise = input("Exercise (None / 1-2 days / 3-5 days / Daily): ").lower()
screen = float(input("Screen time hours per day: "))
diet = input("Diet type (Healthy / Moderate / Junk food often): ").lower()
water = float(input("Water intake (litres per day): "))

obesity, diabetes, heart, hypertension, stress = calculate_risk(
    age, sleep, exercise, screen, diet, water
)

print("\n--------- Health Risk Report ---------")
print("Obesity Risk:", risk_level(obesity))
print("Diabetes Risk:", risk_level(diabetes))
print("Heart Disease Risk:", risk_level(heart))
print("Hypertension Risk:", risk_level(hypertension))
print("Stress Risk:", risk_level(stress))

print("\nSuggestions:")

if sleep < 7:
    print("✔ Improve sleep to 7–8 hours")

if exercise in ["none", "1-2 days"]:
    print("✔ Exercise at least 3 times per week")

if diet == "junk food often":
    print("✔ Reduce junk food consumption")

if screen > 6:
    print("✔ Reduce screen time")

if water < 2:
    print("✔ Drink at least 2–3 litres of water daily")

print("\nStay healthy! 💚")

# ---------------- GRAPH SECTION ----------------

diseases = ["Obesity", "Diabetes", "Heart", "Hypertension", "Stress"]
scores = [obesity, diabetes, heart, hypertension, stress]

plt.bar(diseases, scores)
plt.xlabel("Diseases")
plt.ylabel("Risk Score")
plt.title("Lifestyle Disease Risk Analysis")
plt.show()