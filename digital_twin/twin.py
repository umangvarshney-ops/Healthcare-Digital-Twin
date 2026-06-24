import joblib
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

class DigitalTwin:

    def __init__(
        self,
        age,
        sex,
        cp,
        trestbps,
        chol,
        fbs,
        restecg,
        thalach,
        exang,
        oldpeak,
        slope,
        ca,
        thal
    ):

        self.age = age
        self.sex = sex
        self.cp = cp
        self.trestbps = trestbps
        self.chol = chol
        self.fbs = fbs
        self.restecg = restecg
        self.thalach = thalach
        self.exang = exang
        self.oldpeak = oldpeak
        self.slope = slope
        self.ca = ca
        self.thal = thal

        # Load trained model
        self.model = joblib.load("models/disease_model.pkl")

    # ---------------------------
    # Health Score
    # ---------------------------
    def health_score(self):

        score = 100

        if self.trestbps > 140:
            score -= 15

        if self.chol > 240:
            score -= 15

        if self.thalach < 120:
            score -= 15

        if self.oldpeak > 2:
            score -= 15

        return max(score, 0)

    # ---------------------------
    # Risk Level
    # ---------------------------
    def risk_level(self):

        score = self.health_score()

        if score >= 80:
            return "Low"

        elif score >= 50:
            return "Moderate"

        else:
            return "High"

    # ---------------------------
    # Recommendations
    # ---------------------------
    def recommendations(self):

        rec = []

        if self.chol > 240:
            rec.append("Reduce cholesterol intake")

        if self.trestbps > 140:
            rec.append("Reduce salt intake")

        if self.thalach < 120:
            rec.append("Increase physical activity")

        if len(rec) == 0:
            rec.append("Maintain healthy lifestyle")

        return rec

    # ---------------------------
    # Prepare Patient Data
    # ---------------------------
    def get_patient_data(self):

        return pd.DataFrame([{
            "age": self.age,
            "sex": self.sex,
            "cp": self.cp,
            "trestbps": self.trestbps,
            "chol": self.chol,
            "fbs": self.fbs,
            "restecg": self.restecg,
            "thalach": self.thalach,
            "exang": self.exang,
            "oldpeak": self.oldpeak,
            "slope": self.slope,
            "ca": self.ca,
            "thal": self.thal
        }])

    # ---------------------------
    # Disease Prediction
    # ---------------------------
    def predict_disease(self):

        patient_data = self.get_patient_data()

        prediction = self.model.predict(
            patient_data
        )

        return int(prediction[0])

    # ---------------------------
    # Disease Probability
    # ---------------------------
    def disease_probability(self):

        patient_data = self.get_patient_data()

        probability = self.model.predict_proba(
            patient_data
        )

        return float(probability[0][1])

    # ---------------------------
    # Full Report
    # ---------------------------
    def generate_report(self):

        return {
            "Health Score": self.health_score(),
            "Risk Level": self.risk_level(),
            "Disease Prediction": self.predict_disease(),
            "Disease Probability (%)": round(
                self.disease_probability() * 100,
                2
            ),
            "Recommendations": self.recommendations(),

            "AI Recommendations":
                self.ai_recommendations(),

            "Treatment Plan":
                self.treatment_plan()
        }
    # ---------------------------
    # Exercise Simulation
    # ---------------------------
    def simulate_exercise(self, months=6):

        future_chol = max(self.chol - 20, 150)
        future_bp = max(self.trestbps - 10, 100)
        future_thalach = min(self.thalach + 10, 220)

        return {
            "Current Cholesterol": self.chol,
            "Future Cholesterol": future_chol,
            "Current BP": self.trestbps,
            "Future BP": future_bp,
            "Current Thalach": self.thalach,
            "Future Thalach": future_thalach
        }

    # ---------------------------
    # No Change Simulation
    # ---------------------------
    def simulate_no_change(self):

        return {
            "Cholesterol": self.chol,
            "Blood Pressure": self.trestbps,
            "Thalach": self.thalach
        }

    # ---------------------------
    # Compare Scenarios
    # ---------------------------
    def compare_scenarios(self):

        return {
            "Exercise Plan": self.simulate_exercise(),
            "No Lifestyle Change": self.simulate_no_change()
        }
    
    # ---------------------------
    # AI Treatment Plan
    # ---------------------------
    def treatment_plan(self):

        plan = []

        if self.chol > 240:
            plan.append(
                "Follow a low cholesterol diet and avoid fried foods."
            )

        if self.trestbps > 140:
            plan.append(
                "Reduce salt intake and monitor blood pressure daily."
            )

        if self.thalach < 120:
            plan.append(
                "Perform 30 minutes of walking or cardio exercise daily."
            )

        if self.oldpeak > 2:
            plan.append(
                "Consult a cardiologist for stress-related heart risk."
            )

        if len(plan) == 0:
            plan.append(
                "Continue maintaining a healthy lifestyle."
            )

        return plan
    # ---------------------------
    # AI recommendations
    # ---------------------------
    def ai_recommendations(self):
        recommendations = []

        if self.chol > 240:
            recommendations.append(
                "Follow a low-cholesterol diet. Avoid fried foods and increase fruits and vegetables."
            )

        if self.trestbps > 140:
            recommendations.append(
                "Reduce salt intake and monitor blood pressure regularly."
            )

        if self.thalach < 120:
            recommendations.append(
                "Perform at least 30 minutes of cardio exercise daily."
            )

        if self.oldpeak > 2:
            recommendations.append(
                "Consult a cardiologist for stress-related heart risk evaluation."
            )

        if len(recommendations) == 0:
            recommendations.append(
                "Excellent health condition. Continue maintaining a healthy lifestyle."
            )

        return recommendations
    # ---------------------------
    # Diet Plan
    # ---------------------------
    def diet_plan(self):

        return {
            "Breakfast":"Oats, Fruits, Green Tea",

            "Lunch":"Brown Rice, Dal, Salad",

            "Dinner":"Vegetable Soup, Chapati",

            "Snacks":"Nuts and Fruits"
        }
    # ---------------------------
    # Exercise Plan
    # ---------------------------
    def exercise_plan(self):

        return {
            "Walking":
                "30 mins/day",

            "Cycling":
                "20 mins/day",

            "Cardio":
                "3 times/week",

            "Yoga":
                "15 mins/day"
        }
    # ---------------------------
    # generate pdf report
    # ---------------------------
    def generate_pdf_report(self):

        report = self.generate_report()

        pdf_path = "reports/patient_report.pdf"

        doc = SimpleDocTemplate(pdf_path)

        styles = getSampleStyleSheet()

        content = []

        content.append(
            Paragraph(
                "Healthcare Digital Twin Report",
                styles["Title"]
            )
        )

        content.append(Spacer(1, 12))

        content.append(
            Paragraph(
                f"Age: {self.age}",
                styles["BodyText"]
            )
        )

        content.append(
            Paragraph(
                f"Health Score: {report['Health Score']}",
                styles["BodyText"]
            )
        )

        content.append(
            Paragraph(
                f"Risk Level: {report['Risk Level']}",
                styles["BodyText"]
            )
        )

        content.append(
            Paragraph(
                f"Disease Prediction: {report['Disease Prediction']}",
                styles["BodyText"]
            )
        )

        content.append(
            Paragraph(
                f"Disease Probability: {report['Disease Probability (%)']}%",
                styles["BodyText"]
            )
        )

        content.append(Spacer(1, 12))

        content.append(
            Paragraph(
                "AI Recommendations",
                styles["Heading2"]
            )
        )

        for rec in report["AI Recommendations"]:
            content.append(
                Paragraph(
                    f"• {rec}",
                    styles["BodyText"]
                )
            )

        content.append(Spacer(1, 12))

        content.append(
            Paragraph(
                "Treatment Plan",
                styles["Heading2"]
            )
        )

        for item in report["Treatment Plan"]:
            content.append(
                Paragraph(
                    f"• {item}",
                    styles["BodyText"]
                )
            )

        content.append(Spacer(1, 12))

        content.append(
            Paragraph(
                "Diet Plan",
                styles["Heading2"]
            )
        )

        for meal, food in self.diet_plan().items():
            content.append(
                Paragraph(
                    f"{meal}: {food}",
                    styles["BodyText"]
                )
            )

        content.append(Spacer(1, 12))

        content.append(
            Paragraph(
                "Exercise Plan",
                styles["Heading2"]
            )
        )

        for ex, plan in self.exercise_plan().items():
            content.append(
                Paragraph(
                    f"{ex}: {plan}",
                    styles["BodyText"]
                )
            )

        doc.build(content)

        return pdf_path
    # ---------------------------
    # chatbot_response
    # ---------------------------
    def chatbot_response(self, question):
        question = question.lower()

        if "cholesterol" in question:
            return "Reduce fried foods, eat fruits, vegetables, oats, and exercise regularly."

        elif "blood pressure" in question or "bp" in question:
            return "Reduce salt intake, stay hydrated, and perform daily walking."

        elif "exercise" in question:
            return str(self.exercise_plan())

        elif "diet" in question or "food" in question:
            return str(self.diet_plan())

        elif "health score" in question:
            return f"Your current health score is {self.health_score()}."

        else:
            return "Please consult a healthcare professional for detailed advice."
    # ---------------------------
    # Health Rating
    # ---------------------------
    def health_rating(self):

        score = self.health_score()

        if score >= 90:
            return "Excellent"

        elif score >= 75:
            return "Good"

        elif score >= 50:
            return "Average"

        else:
            return "Poor"
    # ---------------------------
    # health forecast
    # ---------------------------  
    def health_forecast(self):

        forecast = []

        chol = self.chol
        bp = self.trestbps

        for month in range(7):

            forecast.append({
                "Month": "Current" if month == 0 else f"{month} Month",
                "Cholesterol": round(chol),
                "Blood Pressure": round(bp)
            })

            # Improvement rate according to risk

            if self.risk_level() == "High":
                chol *= 0.97
                bp *= 0.98

            elif self.risk_level() == "Medium":
                chol *= 0.98
                bp *= 0.99

            else:
                chol *= 0.995
                bp *= 0.995

        return pd.DataFrame(forecast)
        # ---------------------------
    # emergency alerts
    # --------------------------- 
    def emergency_alerts(self):

        alerts = []

        if self.chol > 300:
            alerts.append(
                "Critical Cholesterol Level Detected!"
            )

        if self.trestbps > 180:
            alerts.append(
                "Dangerous Blood Pressure Level!"
            )

        if self.thalach < 100:
            alerts.append(
                "Very Low Heart Rate Capacity!"
            )

        if self.oldpeak > 4:
            alerts.append(
                "Severe Cardiac Stress Risk!"
            )

        if len(alerts) == 0:
            alerts.append(
                "No Critical Alerts."
            )

        return alerts
    # ---------------------------
    # Health Goals
    # ---------------------------
    def health_goals(self):

        goals = {
            "Target Cholesterol": 200,
            "Target Blood Pressure": 120,
            "Target Heart Rate": 140
        }

        return goals
    # ---------------------------
    # Achievement Tracker
    # ---------------------------
    def achievement_tracker(self):

        achievements = []

        if self.chol <= 200:
            achievements.append(
                "Cholesterol Goal Achieved"
            )

        if self.trestbps <= 120:
            achievements.append(
                "Blood Pressure Goal Achieved"
            )

        if self.thalach >= 140:
            achievements.append(
                "Heart Rate Goal Achieved"
            )

        if len(achievements) == 0:
            achievements.append(
                "Keep working toward your health goals"
            )

        return achievements