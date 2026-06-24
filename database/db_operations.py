import os
import sqlite3

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DB_PATH = os.path.join(
    BASE_DIR,
    "database",
    "healthcare.db"
)

def save_patient_history(
    username,
    age,
    chol,
    trestbps,
    thalach,
    health_score,
    risk_level,
    disease_probability
):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO patient_history
        (
            username,
            age,
            chol,
            trestbps,
            thalach,
            health_score,
            risk_level,
            disease_probability
        )
        VALUES (?,?,?,?,?,?,?,?)
        """,
        (
            username,
            age,
            chol,
            trestbps,
            thalach,
            health_score,
            risk_level,
            disease_probability
        )
    )

    conn.commit()
    conn.close()