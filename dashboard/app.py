
import streamlit as st
import sys
import os
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sqlite3

from database import admin
from auth import create_user, login_user,get_all_users
# from database import db_operations
import sys
import os

ROOT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(ROOT_DIR)
from database import db_operations
from database.db_operations import save_patient_history
# -----------------------------
# Fix Import Path
# -----------------------------
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from digital_twin.twin import DigitalTwin

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Healthcare Digital Twin",
    page_icon="H",
    layout="wide"
)

# =====================================
# AUTHENTICATION SYSTEM
# =====================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.markdown("""
        <div style="
            background:linear-gradient(135deg,#081225,#0F172A);
            border:1px solid #2E86DE;
            border-radius:20px;
            padding:30px;
            margin-bottom:20px;
        ">

        <h1 style="
            text-align:center;
            color:white;
            margin-bottom:5px;
        ">
        Healthcare Digital Twin
        </h1>

        <h3 style="
            text-align:center;
            color:#94A3B8;
            margin-bottom:25px;
        ">
        AI-Powered Health Analytics Platform
        </h3>
        </div>
        """, unsafe_allow_html=True)

    menu = st.radio(
        "",
        ["Login", "Register"],
        horizontal=True
    )
    
    # ==========================
    # REGISTER
    # ==========================
    if menu == "Register":

        st.markdown("## Create Account")

        username = st.text_input(
            "Username",
            key="reg_username"
        )

        email = st.text_input(
            "Email",
            key="reg_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="reg_password"
        )

        role = st.selectbox(
            "Role",
            [
                "Patient",
                "Doctor"
            ],
            key="reg_role"
        )

        if st.button(
            "Register",
            use_container_width=True
        ):

            # Validation
            if not username.strip():

                st.error(
                    "Username is required."
                )

            elif not email.strip():

                st.error(
                    "Email is required."
                )

            elif not password.strip():

                st.error(
                    "Password is required."
                )

            elif len(password) < 6:

                st.error(
                    "Password must be at least 6 characters."
                )

            elif "@" not in email:

                st.error(
                    "Enter a valid email address."
                )

            else:

                success = create_user(
                    username,
                    email,
                    password,
                    role
                )

                if success:

                    st.success(
                        "Account Created Successfully!"
                    )

                else:

                    st.error(
                        "Username or Email Already Exists."
                    )
    # ==========================
    # LOGIN
    # ==========================
    else:

        st.markdown("## Login")

        username = st.text_input(
            "Username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            user = login_user(
                username,
                password
            )

            if user:

                st.session_state.logged_in = True

                st.session_state.user_id = user[0]
                st.session_state.username = user[1]
                st.session_state.email = user[2]
                st.session_state.role = user[3]

                st.success(
                    f"Welcome {user[1]}"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid Username or Password"
                )

    st.stop()


# =====================================
# USER PROFILE CARD
# =====================================

with st.sidebar.container():
    
    st.markdown("""
    <div style="
        background:#0B1727;
        padding:15px;
        border-radius:12px;
        border:1px solid #1E3A5F;
        margin-bottom:10px;
    ">
        <h4 style="color:#00E676;margin:0;text-align:center;">
            Logged in as
        </h4>
        <p style="
            color:white;
            font-size:18px;
            font-weight:bold;
            margin-top:8px;
            margin-bottom:0;
            text-align:center;
        ">
            {username}
        </p>
    </div>
    """.format(
        username=st.session_state.username
    ),
    unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background:#10243F;
        padding:15px;
        border-radius:12px;
        border:1px solid #2E86DE;
        margin-bottom:15px;
    ">
        <h4 style="
                text-align:center;
                color:#2E86DE;margin:0;">
            Account Role
        </h4>
        <p style="
            color:white;
            font-size:18px;
            font-weight:bold;
            margin-top:8px;
            margin-bottom:0;
            text-align:center;
        ">
            {role}
        </p>
    </div>
    """.format(
        role=st.session_state.role
    ),
    unsafe_allow_html=True)

# =====================================
# LOGOUT BUTTON
# =====================================

if st.sidebar.button(
    "Logout",
    use_container_width=True,
    type="secondary"
):

    keys_to_remove = [
        "logged_in",
        "user_id",
        "username",
        "email",
        "role",
        "patient",
        "report"
    ]

    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]

    st.rerun()

# ==========================================
# HERO SECTION
# ==========================================

st.markdown("""
<div style="
    background:linear-gradient(135deg,#081225,#0F172A);
    border:1px solid #2E86DE;
    border-radius:20px;
    padding:30px;
    margin-bottom:20px;
    text-align:center;
">

<h1 style="
    text-align:center;
    color:white;
    margin-bottom:5px;
">
Healthcare Digital Twin
</h1>

<h3 style="
    text-align:center;
    color:#94A3B8;
    margin-bottom:25px;
">
AI-Powered Health Analytics Platform
</h3>

<p style="
    text-align:center;
    color:#CBD5E1;
    margin-bottom:18px;
">
Predict disease risk, monitor patient health,
generate treatment plans and forecast future outcomes
using Digital Twin Technology and Artificial Intelligence.
</p>

</div>
""", unsafe_allow_html=True)
# -----------------------------
# Sidebar
# -----------------------------
if st.session_state.role == "Patient":
    st.sidebar.markdown("""
    <div style="
    background:#081225;
    border:1px solid #2E86DE;
    border-radius:15px;
    padding:15px;
    margin-bottom:15px;
    ">

    <h2 style="color:white;">
    Healthcare Digital Twin
    </h2>

    <p style="color:#CBD5E1;">
    Generate AI-powered health insights, risk prediction,
    treatment recommendations and future health forecasts.
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("""
    <div style="
    background:#081225;
    border:1px solid #2E86DE;
    border-radius:12px;
    padding:10px;
    margin-bottom:10px;
    text-align:center;
    ">
    <h4 style="
    color:white;
    margin:0;
    ">
    Personal Information
    </h4>
    </div>
    """, unsafe_allow_html=True)

    age = st.sidebar.number_input(
        "Age",
        min_value=20,
        max_value=100,
        value=52
    )

    sex_label = st.sidebar.selectbox(
        "Gender",
        ["Female", "Male"]
    )

    sex = 0 if sex_label == "Female" else 1

    # ==========================================
    # HEART HEALTH METRICS
    # ==========================================

    st.sidebar.markdown("""
    <div style="
    background:#081225;
    border:1px solid #00E676;
    border-radius:12px;
    padding:10px;
    margin-top:15px;
    margin-bottom:10px;
    text-align:center;
    ">
    <h4 style="
    color:white;
    margin:0;
    ">
    Heart Health Metrics
    </h4>
    </div>
    """, unsafe_allow_html=True)

    cp_options = {
        "Typical Angina": 0,
        "Atypical Angina": 1,
        "Non-Anginal Pain": 2,
        "Asymptomatic": 3
    }

    cp_label = st.sidebar.selectbox(
        "Chest Pain Type",
        list(cp_options.keys())
    )

    cp = cp_options[cp_label]

    trestbps = st.sidebar.number_input(
        "Resting Blood Pressure (mmHg)",
        min_value=80,
        max_value=250,
        value=145,
        help="Normal range: 90-120 mmHg"
    )

    chol = st.sidebar.number_input(
        "Cholesterol (mg/dL)",
        min_value=100,
        max_value=600,
        value=280,
        help="Ideal value below 200 mg/dL"
    )

    thalach = st.sidebar.number_input(
        "Maximum Heart Rate",
        min_value=60,
        max_value=250,
        value=115,
        help="Higher values indicate better cardiac capacity"
    )

    # ==========================================
    # MEDICAL TEST RESULTS
    # ==========================================

    st.sidebar.markdown("""
    <div style="
    background:#081225;
    border:1px solid #F59E0B;
    border-radius:12px;
    padding:10px;
    margin-top:15px;
    margin-bottom:10px;
    text-align:center;
    ">
    <h4 style="
    color:white;
    margin:0;
    ">
    Medical Test Results
    </h4>
    </div>
    """, unsafe_allow_html=True)

    fbs_options = {
        "Normal": 0,
        "High (>120 mg/dL)": 1
    }

    fbs_label = st.sidebar.selectbox(
        "Fasting Blood Sugar",
        list(fbs_options.keys())
    )

    fbs = fbs_options[fbs_label]

    restecg_options = {
        "Normal": 0,
        "ST-T Abnormality": 1,
        "Left Ventricular Hypertrophy": 2
    }

    restecg_label = st.sidebar.selectbox(
        "Rest ECG Result",
        list(restecg_options.keys())
    )

    restecg = restecg_options[restecg_label]

    exang_options = {
        "No": 0,
        "Yes": 1
    }

    exang_label = st.sidebar.selectbox(
        "Exercise Induced Chest Pain",
        list(exang_options.keys())
    )

    exang = exang_options[exang_label]

    oldpeak = st.sidebar.slider(
        "ST Depression (Oldpeak)",
        min_value=0.0,
        max_value=10.0,
        value=2.5,
        step=0.1
    )

    slope_options = {
        "Upsloping": 0,
        "Flat": 1,
        "Downsloping": 2
    }

    slope_label = st.sidebar.selectbox(
        "ST Segment Slope",
        list(slope_options.keys())
    )

    slope = slope_options[slope_label]

    ca = st.sidebar.selectbox(
        "Blocked Major Vessels",
        [0, 1, 2, 3, 4]
    )

    st.sidebar.caption(
        "Higher values indicate more blocked vessels."
    )

    thal_options = {
        "Normal": 0,
        "Fixed Defect": 1,
        "Reversible Defect": 2,
        "Unknown": 3
    }

    thal_label = st.sidebar.selectbox(
        "Thalassemia Test",
        list(thal_options.keys())
    )

    thal = thal_options[thal_label]

    # ==========================================
    # PATIENT SNAPSHOT
    # ==========================================

    st.sidebar.markdown("""
    <div style="
    background:#081225;
    border:1px solid #8B5CF6;
    border-radius:12px;
    padding:10px;
    margin-top:15px;
    margin-bottom:10px;
    text-align:center;
    ">
    <h4 style="
    color:white;
    margin:0;
    ">
    Patient Snapshot
    </h4>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown(
        f"""
        <div style="
        background:#081225;
        border:1px solid #8B5CF6;
        border-radius:12px;
        padding:15px;
        color:white;
        line-height:1.8;
        ">

        <b>Age:</b> {age}<br>

        <b>Gender:</b> {sex_label}<br>

        <b>Blood Pressure:</b> {trestbps} mmHg<br>

        <b>Cholesterol:</b> {chol} mg/dL<br>

        <b>Heart Rate:</b> {thalach} BPM

        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.markdown("<br>", unsafe_allow_html=True)

    generate = st.sidebar.button(
        "Generate Digital Twin",
        use_container_width=True,
        type="primary"
    )
if st.session_state.role == "Admin":

    st.markdown("""
    <div style="
        background:#081225;
        border:1px solid #FF9800;
        border-radius:15px;
        padding:20px;
        margin-bottom:20px;
        text-align:center;
    ">
        <h1 style="color:#FF9800;">
            Admin Dashboard
        </h1>
        <p style="color:white;">
            User Management & System Administration
        </p>
    </div>
    """, unsafe_allow_html=True)

    users = get_all_users()

    df = pd.DataFrame(
        users,
        columns=[
            "ID",
            "Username",
            "Email",
            "Role"
        ]
    )

    st.subheader("Registered Users")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Users",
            len(df)
        )

    with col2:
        st.metric(
            "Doctors",
            len(
                df[df["Role"] == "Doctor"]
            )
        )

    with col3:
        st.metric(
            "Patients",
            len(
                df[df["Role"] == "Patient"]
            )
        )

    st.stop() 
elif st.session_state.role == "Doctor":
    st.success("Doctor Dashboard")

    try:
        import sqlite3

        conn = sqlite3.connect("database/healthcare.db")

        history = pd.read_sql_query(
            """
            SELECT *
            FROM patient_history
            """,
            conn
        )

        conn.close()

        st.subheader("Patient Records")

        search_name = st.text_input(
            "Search Patient by Username"
        )

        if search_name:

            filtered_history = history[
                history["username"]
                .str.contains(
                    search_name,
                    case=False,
                    na=False
                )
            ]

            st.dataframe(
                filtered_history,
                use_container_width=True
            )

        else:

            st.dataframe(
                history,
                use_container_width=True
            )

    except Exception as e:
        st.error(str(e))

    st.stop()


# -----------------------------
# Generate Digital Twin
# -----------------------------
if generate:

    with st.spinner("Generating Digital Twin Analysis..."):

        patient = DigitalTwin(
            age=age,
            sex=sex,
            cp=cp,
            trestbps=trestbps,
            chol=chol,
            fbs=fbs,
            restecg=restecg,
            thalach=thalach,
            exang=exang,
            oldpeak=oldpeak,
            slope=slope,
            ca=ca,
            thal=thal
        )

        report = patient.generate_report()

        st.session_state.patient = patient
        st.session_state.report = report

        save_patient_history(
            st.session_state.username,
            age,
            chol,
            trestbps,
            thalach,
            report["Health Score"],
            report["Risk Level"],
            report["Disease Probability (%)"]
        )
    

    st.toast(
        "Digital Twin Generated Successfully!",
        icon="✅"
    )



# =====================================
# OUTSIDE BUTTON
# =====================================

if ("patient" in st.session_state and "report" in st.session_state):

    patient = st.session_state.patient
    report = st.session_state.report
    risk_level = report["Risk Level"]

    if risk_level == "High":
        title = "Critical Risk Detected"
        color = "#FF4D4F"

    elif risk_level in ["Medium", "Moderate"]:
        title = "Moderate Risk Detected"
        color = "#F59E0B"

    else:
        title = "Low Risk Profile"
        color = "#00E676"
        
    with st.container(border=True):

        st.markdown(
            f"""
            <h1 style="
                text-align:center;
                color:{color};
            ">
                {title}
            </h1>
            """,
            unsafe_allow_html=True
        )
    
    tab1, tab2, tab3, tab4, tab5,tab6= st.tabs([
        "Overview",
        "Forecast",
        "Treatment",
        "History",
        "AI Assistant",
        "Download Report"
    ])
    
    
    # =====================================
    # Navigation Pages
    # =====================================
    with tab1:
        
        # ==========================================
        # HEALTH OVERVIEW DASHBOARD
        # ==========================================

        st.subheader("Health Overview")

        # -----------------------------
        # Health Score Gauge
        # -----------------------------

        score = report["Health Score"]

        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=score,
                title={"text": "Health Score"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#2E86DE"},
                    "steps": [
                        {"range": [0, 50], "color": "#FF4D4F"},
                        {"range": [50, 80], "color": "#F59E0B"},
                        {"range": [80, 100], "color": "#00E676"}
                    ]
                }
            )
        )

        gauge.update_layout(
            paper_bgcolor="#081225",
            plot_bgcolor="#081225",
            font=dict(color="white"),
            height=400
        )

        st.plotly_chart(
            gauge,
            use_container_width=True
        )

        # -----------------------------
        # Key Metrics
        # -----------------------------

        col1, col2, col3 = st.columns(3)

        with col1:
            with st.container(border=True):
                st.markdown("### Health Score")
                st.markdown(
                    f"<h1 style='text-align:center;color:#00E676;'>{report['Health Score']}</h1>",
                    unsafe_allow_html=True
                )

        with col2:
            with st.container(border=True):
                st.markdown("### Risk Level")

                risk_color = (
                    "#FF4D4F"
                    if report["Risk Level"] == "High"
                    else "#F59E0B"
                    if report["Risk Level"] == "Moderate"
                    else "#00E676"
                )

                st.markdown(
                    f"<h1 style='text-align:center;color:{risk_color};'>{report['Risk Level']}</h1>",
                    unsafe_allow_html=True
                )

        with col3:
            with st.container(border=True):
                st.markdown("### Disease Probability")

                st.markdown(
                    f"<h1 style='text-align:center;color:#2E86DE;'>{report['Disease Probability (%)']}%</h1>",
                    unsafe_allow_html=True
                )

        # -----------------------------
        # Live Health Status
        # -----------------------------

        st.subheader("Live Health Status")

        if report["Health Score"] >= 80:
            status = "Healthy Condition"
            status_color = "#00E676"

        elif report["Health Score"] >= 50:
            status = "Moderate Risk"
            status_color = "#F59E0B"

        else:
            status = "High Risk"
            status_color = "#FF4D4F"

        with st.container(border=True):

            st.markdown(
                f"""
                <h2 style="
                    text-align:center;
                    color:{status_color};
                ">
                    {status}
                </h2>
                """,
                unsafe_allow_html=True
            )

        # -----------------------------
        # Health Indicators
        # -----------------------------

        st.subheader("Health Indicators")

        col1, col2 = st.columns(2)

        with col1:
            st.write("Health Score")
            st.progress(report["Health Score"] / 100)

        with col2:
            st.write("Disease Probability")
            st.progress(report["Disease Probability (%)"] / 100)

        # -----------------------------
        # Vital Signs
        # -----------------------------

        st.subheader("Vital Signs")

        col1, col2, col3 = st.columns(3)

        with col1:
            with st.container(border=True):
                st.markdown("### Cholesterol")
                st.markdown(
                    f"<h1 style='text-align:center;color:#00E676;'>{chol}</h1>",
                    unsafe_allow_html=True
                )
                st.caption("mg/dL")

        with col2:
            with st.container(border=True):
                st.markdown("### Blood Pressure")
                st.markdown(
                    f"<h1 style='text-align:center;color:#2E86DE;'>{trestbps}</h1>",
                    unsafe_allow_html=True
                )
                st.caption("mmHg")

        with col3:
            with st.container(border=True):
                st.markdown("### Heart Rate")
                st.markdown(
                    f"<h1 style='text-align:center;color:#F59E0B;'>{thalach}</h1>",
                    unsafe_allow_html=True
                )
                st.caption("BPM")

        # -----------------------------
        # Overall Health Rating
        # -----------------------------

        st.subheader("Overall Health Rating")

        rating = patient.health_rating()

        rating_color = {
            "Excellent": "#00E676",
            "Good": "#2E86DE",
            "Average": "#F59E0B",
            "Poor": "#FF4D4F"
        }.get(rating, "#FFFFFF")

        with st.container(border=True):

            st.markdown(
                f"""
                <h1 style="
                    text-align:center;
                    color:{rating_color};
                ">
                    {rating}
                </h1>
                """,
                unsafe_allow_html=True
            )

        # -----------------------------
        # Risk Analysis
        # -----------------------------

        st.subheader("Risk Analysis")

        risk = report["Disease Probability (%)"]

        if risk >= 80:
            title = "High Risk Detected"
            message = "Immediate medical consultation recommended."
            color = "#FF4D4F"

        elif risk >= 50:
            title = "Moderate Risk"
            message = "Lifestyle changes and regular monitoring recommended."
            color = "#F59E0B"

        else:
            title = "Low Risk"
            message = "Current health indicators are relatively stable."
            color = "#00E676"

        with st.container(border=True):

            st.markdown(
                f"""
                <h2 style="color:{color};">
                    {title} ({risk}%)
                </h2>

                <p style="
                    color:white;
                    font-size:16px;
                ">
                    {message}
                </p>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")
        
        st.markdown("---")
        # -----------------------------
        # Patient Summary
        # -----------------------------

        st.subheader("Patient Summary")

        col1, col2 = st.columns(2)

        with col1:

            with st.container(border=True):

                st.markdown("### Age")

                st.markdown(
                    f"""
                    <h1 style="
                        text-align:center;
                        color:#2E86DE;
                    ">
                        {age}
                    </h1>
                    """,
                    unsafe_allow_html=True
                )

                st.caption("Patient Age")

            with st.container(border=True):

                risk_color = (
                    "#FF4D4F"
                    if report["Risk Level"] == "High"
                    else "#00E676"
                )

                st.markdown("### Risk Level")

                st.markdown(
                    f"""
                    <h1 style="
                        text-align:center;
                        color:{risk_color};
                    ">
                        {report['Risk Level']}
                    </h1>
                    """,
                    unsafe_allow_html=True
                )

                st.caption("Current Risk Status")

        with col2:

            with st.container(border=True):

                st.markdown("### Health Score")

                st.markdown(
                    f"""
                    <h1 style="
                        text-align:center;
                        color:#00E676;
                    ">
                        {report['Health Score']}
                    </h1>
                    """,
                    unsafe_allow_html=True
                )

                st.caption("Overall Health Rating")

            with st.container(border=True):

                st.markdown("### Disease Probability")

                st.markdown(
                    f"""
                    <h1 style="
                        text-align:center;
                        color:#F59E0B;
                    ">
                        {report['Disease Probability (%)']}%
                    </h1>
                    """,
                    unsafe_allow_html=True
                )

                st.caption("Predicted Risk Percentage")

        # -----------------------------
        # Risk Gauge Chart
        # -----------------------------

        st.markdown("### Disease Risk Analysis")

        risk_fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=report["Disease Probability (%)"],
                title={"text": "Disease Risk %"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#2E86DE"},
                    "steps": [
                        {
                            "range": [0, 30],
                            "color": "#00E676"
                        },
                        {
                            "range": [30, 70],
                            "color": "#F59E0B"
                        },
                        {
                            "range": [70, 100],
                            "color": "#FF4D4F"
                        }
                    ]
                }
            )
        )

        risk_fig.update_layout(
            paper_bgcolor="#081225",
            plot_bgcolor="#081225",
            font=dict(
                color="white",
                size=16
            ),
            height=400
        )

        st.plotly_chart(
            risk_fig,
            use_container_width=True
        )

        # -----------------------------
        # Overall Health Rating
        # -----------------------------

        with st.container(border=True):

            st.markdown("### Overall Health Rating")

            rating = patient.health_rating()

            rating_color = (
                "#00E676"
                if "Excellent" in rating
                else "#F59E0B"
                if "Good" in rating
                else "#FF4D4F"
            )

            st.markdown(
                f"""
                <h2 style="
                    text-align:center;
                    color:{rating_color};
                ">
                    {rating}
                </h2>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")
        # Health Score Gauge
        # Metrics
        # Patient Summary
        # Risk Analysis

    with tab2:

        
        # ==========================
        # 6-Month Health Forecast
        # ==========================
        st.subheader("6-Month Health Forecast")

        forecast = patient.health_forecast()

        # Table
        st.dataframe(
            forecast,
            use_container_width=True,
            hide_index=True
        )

        # Chart
        forecast_fig = px.line(
            forecast,
            x="Month",
            y=["Cholesterol", "Blood Pressure"],
            markers=True,
            title="Future Health Improvement Forecast"
        )

        forecast_fig.update_layout(
            paper_bgcolor="#081225",
            plot_bgcolor="#081225",
            font=dict(color="white"),
            title_font=dict(size=22),
            xaxis=dict(
                title="Month",
                showgrid=False
            ),
            yaxis=dict(
                title="Health Metrics",
                gridcolor="#1E293B"
            ),
            legend=dict(
                orientation="h",
                y=1.1
            ),
            height=500
        )

        forecast_fig.update_traces(
            line=dict(width=4),
            marker=dict(size=10)
        )

        st.plotly_chart(
            forecast_fig,
            use_container_width=True
        )

        st.markdown("---")
        # Smart Health Alerts
        st.markdown("---")
        st.subheader("Smart Health Alerts")

        alerts = patient.emergency_alerts()

        for alert in alerts:

            if alert == "No Critical Alerts.":

                with st.container(border=True):
                    st.markdown(
                        "<h3 style='color:#00E676;'>Health Status</h3>",
                        unsafe_allow_html=True
                    )
                    st.write(alert)

            else:

                with st.container(border=True):
                    st.markdown(
                        "<h3 style='color:#FF4D4F;'>Critical Alert</h3>",
                        unsafe_allow_html=True
                    )
                    st.write(alert)
        st.markdown("---")
        st.subheader("Personalized Health Goals")

        col1, col2, col3 = st.columns(3)

        with col1:
            with st.container(border=True):
                st.markdown("### Target Cholesterol")
                st.markdown(
                    "<h1 style='text-align:center;color:#00E676;'>200</h1>",
                    unsafe_allow_html=True
                )
                st.caption("mg/dL")

        with col2:
            with st.container(border=True):
                st.markdown("### Target Blood Pressure")
                st.markdown(
                    "<h1 style='text-align:center;color:#2E86DE;'>120</h1>",
                    unsafe_allow_html=True
                )
                st.caption("mmHg")

        with col3:
            with st.container(border=True):
                st.markdown("### Target Heart Rate")
                st.markdown(
                    "<h1 style='text-align:center;color:#F59E0B;'>140</h1>",
                    unsafe_allow_html=True
                )
                st.caption("BPM")
        # Goal Completion
        st.markdown("### Goal Completion")

        chol_percent = round((200 / chol) * 100, 1)
        bp_percent = round((120 / trestbps) * 100, 1)
        hr_percent = round((thalach / 140) * 100, 1)

        col1, col2, col3 = st.columns(3)

        with col1:
            with st.container(border=True):
                st.markdown("### Cholesterol Progress")
                st.markdown(
                    f"<h1 style='text-align:center;color:#00E676;'>{chol_percent}%</h1>",
                    unsafe_allow_html=True
                )
                st.caption("Goal Completion")

        with col2:
            with st.container(border=True):
                st.markdown("### BP Progress")
                st.markdown(
                    f"<h1 style='text-align:center;color:#2E86DE;'>{bp_percent}%</h1>",
                    unsafe_allow_html=True
                )
                st.caption("Goal Completion")

        with col3:
            with st.container(border=True):
                st.markdown("### Heart Rate Progress")
                st.markdown(
                    f"<h1 style='text-align:center;color:#F59E0B;'>{hr_percent}%</h1>",
                    unsafe_allow_html=True
                )
                st.caption("Goal Completion")
        

        st.markdown("---")
        st.subheader("Achievement Tracker")

        achievements = patient.achievement_tracker()

        for achievement in achievements:

            st.markdown(
                f"""
                <div style="
                    background:#081225;
                    border:1px solid #00E676;
                    border-radius:12px;
                    padding:18px;
                    margin-bottsom:12px;
                ">
                    <div style="
                        color:white;
                        font-size:18px;
                        font-weight:500;
                    ">
                        {achievement}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")
        
        # Goal Progress
        st.subheader("Goal Progress")

        chol_progress = min(1.0, 200 / max(patient.chol, 1))
        bp_progress = min(1.0, 120 / max(patient.trestbps, 1))
        hr_progress = min(1.0, patient.thalach / 140)

        goals = {
            "Cholesterol Goal": chol_progress,
            "Blood Pressure Goal": bp_progress,
            "Heart Rate Goal": hr_progress
        }

        for goal, value in goals.items():

            percentage = int(value * 100)

            with st.container(border=True):

                st.markdown(f"**{goal}**")

                st.progress(value)

                st.caption(f"{percentage}% Complete")

        st.markdown("---")
        
        # -----------------------------
        # Disease Prediction
        # -----------------------------
        # st.subheader("Disease Prediction")
        prediction = report["Disease Prediction"]

        risk_text = "High Risk" if prediction == 1 else "Low Risk"
        status_text = "Attention Needed" if prediction == 1 else "Healthy"

        risk_color = "#FF4D4F" if prediction == 1 else "#00E676"
        status_color = "#FF9800" if prediction == 1 else "#2E86DE"

        st.subheader("Health Status")

        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                st.markdown("### Disease Prediction")
                st.markdown(
                    f"<h1 style='text-align:center;color:{risk_color};'>{risk_text}</h1>",
                    unsafe_allow_html=True
                )
                st.caption("Model Prediction")

        with col2:
            with st.container(border=True):
                st.markdown("### Health Status")
                st.markdown(
                    f"<h1 style='text-align:center;color:{status_color};'>{status_text}</h1>",
                    unsafe_allow_html=True
                )
                st.caption("Current Condition")
        # forecast dataframe
        # forecast graph
        # future simulation

    with tab3:

        # -----------------------------
        # Recommendations
        # -----------------------------
        st.subheader("Recommendations")

        for rec in report["Recommendations"]:
            st.markdown(
                f"""
                <div style="
                    background:#081225;
                    border:1px solid #2E86DE;
                    border-radius:12px;
                    padding:20px;
                    margin-bottom:12px;
                ">
                    <div style="
                        color:white;
                        font-size:18px;
                        font-weight:500;
                    ">
                        {rec}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.subheader("AI Treatment Recommendations")

        for rec in report["AI Recommendations"]:
            st.markdown(
                f"""
                <div style="
                    background:#081225;
                    border:1px solid #2E86DE;
                    border-radius:12px;
                    padding:20px;
                    margin-bottom:12px;
                ">
                    <div style="
                        color:white;
                        font-size:18px;
                        font-weight:500;
                    ">
                        {rec}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Diet Plan
        st.subheader("Diet Plan")

        diet = patient.diet_plan()

        for meal, food in diet.items():
            st.markdown(
                f"""
                <div style="
                    padding:12px;
                    border-radius:10px;
                    border:1px solid #2e86de;
                    margin-bottom:10px;">
                    <b>{meal}</b><br>
                    {food}
                </div>
                """,
                unsafe_allow_html=True
            )

        # Exercise Plan
        st.subheader("Exercise Plan")

        exercise = patient.exercise_plan()

        for ex, plan in exercise.items():
            st.markdown(
                f"""
                <div style="
                    padding:12px;
                    border-radius:10px;
                    border:1px solid #2e86de;
                    margin-bottom:10px;">
                    <b>{plan}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")
        # -----------------------------
        # AI Treatment Plan
        # -----------------------------
        st.subheader("AI Treatment Plan")

        for item in report["Treatment Plan"]:

            st.markdown(
                f"""
                <div style="
                    padding:12px;
                    border-radius:10px;
                    border:1px solid #2e86de;
                    margin-bottom:10px;">
                    <b>{item}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")
        # -----------------------------
        # Exercise Simulation
        # -----------------------------
        st.subheader("Future Health Simulation")

        sim = patient.simulate_exercise()

        fig = px.bar(
            x=[
                "Current Cholesterol",
                "Future Cholesterol",
                "Current BP",
                "Future BP"
            ],
            y=[
                sim["Current Cholesterol"],
                sim["Future Cholesterol"],
                sim["Current BP"],
                sim["Future BP"]
            ],
            title="Exercise Impact Analysis"
        )

        fig.update_traces(
            marker_color=[
                "#4DA3FF",  # Current Cholesterol
                "#00E676",  # Future Cholesterol
                "#FF9800",  # Current BP
                "#00E676"   # Future BP
            ],
            marker_line_color="white",
            marker_line_width=1
        )

        fig.update_layout(
            paper_bgcolor="#081225",
            plot_bgcolor="#081225",

            font=dict(
                color="white",
                size=14
            ),

            title=dict(
                text="Exercise Impact Analysis",
                font=dict(
                    size=22,
                    color="white"
                )
            ),

            xaxis=dict(
                title="",
                showgrid=False,
                tickfont=dict(size=13)
            ),

            yaxis=dict(
                title="Value",
                showgrid=True,
                gridcolor="rgba(255,255,255,0.08)",
                tickfont=dict(size=13)
            ),

            hoverlabel=dict(
                bgcolor="#0F172A",
                font_color="white"
            ),

            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown("---")

        # -----------------------------
        # Scenario Comparison
        # -----------------------------
        st.subheader("Scenario Comparison")

        scenario = patient.compare_scenarios()

        col1, col2 = st.columns(2)

        # Exercise Plan Scenario
        with col1:
            st.markdown("""
            <div style="
                height:100px;
                padding:15px;
                border:1px solid #2E86DE;
                border-radius:10px;
                margin-bottom:10px;">
                <h4>Exercise Plan</h4>
            """, unsafe_allow_html=True)

            for k, v in scenario["Exercise Plan"].items():
                st.write(f"**{k}:** {v}")

            st.markdown("</div>", unsafe_allow_html=True)

        # No Lifestyle Change Scenario
        with col2:
            st.markdown("""
            <div style="
                height:100px;
                padding:15px;
                border:1px solid #E74C3C;
                border-radius:10px;
                margin-bottom:10px;">
                <h4>No Lifestyle Change</h4>
            """, unsafe_allow_html=True)

            for k, v in scenario["No Lifestyle Change"].items():
                st.write(f"**{k}:** {v}")

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        # -----------------------------
        # Full Report
        # -----------------------------
        st.subheader("Full Digital Twin Report")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div style="
                padding:20px;
                border:1px solid #2E86DE;
                border-radius:10px;
                margin-bottom:15px;">
                <h3>Health Score</h3>
                <h2>{report['Health Score']}</h2>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="
                padding:20px;
                border:1px solid #E74C3C;
                border-radius:10px;
                margin-bottom:15px;">
                <h3>Risk Level</h3>
                <h2>{report['Risk Level']}</h2>
            </div>
            """, unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div style="
                padding:20px;
                border:1px solid #27AE60;
                border-radius:10px;
                margin-bottom:15px;">
                <h3>Disease Prediction</h3>
                <h2>{report['Disease Prediction']}</h2>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="
                padding:20px;
                border:1px solid #F39C12;
                border-radius:10px;
                margin-bottom:15px;">
                <h3>Disease Probability</h3>
                <h2>{report['Disease Probability (%)']}%</h2>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("### Recommendations")

        for rec in report["Recommendations"]:
            st.markdown(f"""
            <div style="
                padding:15px;
                border:1px solid #2E86DE;
                border-radius:10px;
                margin-bottom:10px;">
                {rec}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### AI Recommendations")

        for rec in report["AI Recommendations"]:
            st.markdown(f"""
            <div style="
                padding:15px;
                border:1px solid #27AE60;
                border-radius:10px;
                margin-bottom:10px;">
                {rec}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### Treatment Plan")
        for rec in report["AI Recommendations"]:
            st.markdown(f"""
            <div style="
                padding:15px;
                border:1px solid #27AE60;
                border-radius:10px;
                margin-bottom:10px;">
                {rec}
            </div>
            """, unsafe_allow_html=True)
        st.markdown("---")
        
        # recommendations
        # diet plan
        # treatment plan

    with tab4:
        
        st.markdown("""
        <style>

        /* Table */
        [data-testid="stDataFrame"] {
            border: 1px solid #2E86DE;
            border-radius: 12px;
            overflow: hidden;
        }

        /* Header */
        thead tr th {
            background-color: #0F172A !important;
            color: #2E86DE !important;
            font-size: 16px !important;
            font-weight: 600 !important;
        }

        /* Rows */
        tbody tr {
            background-color: #081225 !important;
        }

        tbody tr:hover {
            background-color: #0F172A !important;
        }

        /* Cells */
        tbody td {
            color: white !important;
            font-size: 15px !important;
        }

        </style>
        """, unsafe_allow_html=True)
        col1, col2 = st.columns([4, 1])
        conn = sqlite3.connect(
            "database/healthcare.db"
        )

        history = pd.read_sql_query(
            """
            SELECT *
            FROM patient_history
            WHERE username = ?
            ORDER BY id DESC
            """,
            conn,
            params=[
                st.session_state.username
            ]
        )

        conn.close()
        if history.empty:

            st.warning(
                "No patient history available."
            )

            st.stop()
        latest = history.iloc[0]

        age = latest["age"]

        health_score = latest["health_score"]

        risk_level = latest["risk_level"]

        disease_probability = latest["disease_probability"]
        with col1:
            st.subheader("Patient History")

        with col2:
            csv = history.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="Download",
                data=csv,
                file_name="patient_history.csv",
                mime="text/csv",
                use_container_width=True
            )
        if history.empty:
            st.warning("No patient history found.")
            st.stop()
        st.dataframe(
            history.tail(10),
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")
        st.subheader("Health Trends Analysis")

        def style_chart(fig):
            fig.update_layout(
                paper_bgcolor="#081225",
                plot_bgcolor="#081225",
                font=dict(
                    color="white",
                    size=14
                ),
                title_font=dict(
                    size=22,
                    color="white"
                ),
                xaxis=dict(
                    showgrid=True,
                    gridcolor="rgba(255,255,255,0.08)"
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="rgba(255,255,255,0.08)"
                ),
                hoverlabel=dict(
                    bgcolor="#0F172A",
                    font_color="white"
                )
            )
            return fig


        # Health Score Trend
        health_fig = px.line(
            history,
            y="health_score",
            title="Health Score Trend",
            markers=True
        )

        health_fig.update_traces(
            line=dict(color="#4DA3FF", width=4),
            marker=dict(size=8, color="#4DA3FF")
        )

        health_fig = style_chart(health_fig)

        st.plotly_chart(
            health_fig,
            use_container_width=True
        )


        # Cholesterol Trend
        chol_fig = px.line(
            history,
            y="chol",
            title="Cholesterol Trend",
            markers=True
        )

        chol_fig.update_traces(
            line=dict(color="#00E676", width=4),
            marker=dict(size=8, color="#00E676")
        )

        chol_fig = style_chart(chol_fig)

        st.plotly_chart(
            chol_fig,
            use_container_width=True
        )


        # Blood Pressure Trend
        bp_fig = px.line(
            history,
            y="trestbps",
            title="Blood Pressure Trend",
            markers=True
        )

        bp_fig.update_traces(
            line=dict(color="#FF9800", width=4),
            marker=dict(size=8, color="#FF9800")
        )

        bp_fig = style_chart(bp_fig)

        st.plotly_chart(
            bp_fig,
            use_container_width=True
        )


        # Disease Probability Trend
        prob_fig = px.line(
            history,
            y="disease_probability",
            title="Disease Probability Trend",
            markers=True
        )

        prob_fig.update_traces(
            line=dict(color="#FF5252", width=4),
            marker=dict(size=8, color="#FF5252")
        )

        prob_fig = style_chart(prob_fig)

        st.plotly_chart(
            prob_fig,
            use_container_width=True
        )


        # Risk Distribution
        risk_fig = px.histogram(
            history,
            x="risk_level",
            title="Risk Level Distribution",
            color="risk_level"
        )

        risk_fig.update_layout(
            paper_bgcolor="#081225",
            plot_bgcolor="#081225",
            font=dict(color="white")
        )

        st.plotly_chart(
            risk_fig,
            use_container_width=True
        )


        # Correlation Heatmap
        numeric_history = history.select_dtypes(include="number")

        corr = numeric_history.corr()

        heatmap = px.imshow(
            corr,
            text_auto=True,
            title="Feature Correlation Heatmap",
            color_continuous_scale="Blues"
        )

        heatmap.update_layout(
            paper_bgcolor="#081225",
            plot_bgcolor="#081225",
            font=dict(color="white")
        )

        st.plotly_chart(
            heatmap,
            use_container_width=True
        )
        st.markdown("---")

        st.markdown("""
        <style>

        .summary-card{
            background:#0F172A;
            border:1px solid #2E86DE;
            border-radius:15px;
            padding:20px;
            text-align:center;
            margin-bottom:15px;
        }

        .summary-label{
            color:#CBD5E1;
            font-size:16px;
            font-weight:500;
        }

        .summary-value{
            color:white;
            font-size:30px;
            font-weight:700;
            margin-top:10px;
        }

        </style>
        """, unsafe_allow_html=True)
        st.markdown("---")
        latest = history.iloc[0]

        age = latest["age"]

        health_score = latest["health_score"]

        risk_level = latest["risk_level"]

        disease_probability = latest["disease_probability"]
        st.subheader("Patient Health Summary")

        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class="summary-card">
                <div class="summary-label">Age</div>
                <div class="summary-value">{age}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="summary-card">
                <div class="summary-label">Health Score</div>
                <div class="summary-value">{health_score}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="summary-card">
                <div class="summary-label">Risk Level</div>
                <div class="summary-value">{risk_level}</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="summary-card">
                <div class="summary-label">Disease Probability</div>
                <div class="summary-value">{disease_probability}%</div>
            </div>
            """, unsafe_allow_html=True)
        # history table
        # achievements
        # alerts

    with tab5:

        
        
        # -----------------------------
        # AI Health Assistant
        # -----------------------------
        st.markdown("""
        <style>

        .ai-card{
            border:1px solid #2E86DE;
            border-radius:15px;
            padding:25px;
            background:#081225;
            margin-top:10px;
        }

        .ai-label{
            color:#CBD5E1;
            font-size:18px;
            margin-bottom:10px;
        }

        </style>
        """, unsafe_allow_html=True)

        st.subheader("AI Health Assistant")

        with st.container(border=True):

            st.markdown(
                '<div class="ai-label">Ask your Digital Twin</div>',
                unsafe_allow_html=True
            )

            user_question = st.text_input(
                "",
                placeholder="e.g. How can I reduce my cholesterol?"
            )

            if user_question:
                st.info(
                    "AI Assistant Response: This is where your Digital Twin response will appear."
                )

    with tab6:
        # -----------------------------
        # Save in Session State
        # -----------------------------
        st.session_state.patient = patient
        st.session_state.report = report

        # -----------------------------
        # Download PDF Report
        # -----------------------------
        st.subheader("Download Report")

        pdf_path = patient.generate_pdf_report()
        with open(pdf_path, "rb") as file:
            pdf_bytes = file.read()
        st.markdown("""
        <style>
        .report-card{
            background:#081225;
            border:1px solid #2E86DE;
            border-radius:18px;
            padding:25px;
            margin-top:10px;
        }

        .report-title{
            font-size:32px;
            font-weight:700;
            color:white;
            margin-bottom:15px;
        }

        .report-text{
            color:#CBD5E1;
            font-size:18px;
            margin-bottom:15px;
        }

        .report-item{
            padding:15px;
            border:1px solid #27AE60;
            border-radius:10px;
            margin-bottom:10px;
        }
        </style>
        """, unsafe_allow_html=True)
        with st.container(border=True):

            st.markdown(
                '<div class="report-title">Patient Health Report</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="report-text">Complete Digital Twin analysis including:</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="report-item">Risk Analysis</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="report-item">Health Forecast</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="report-item">Treatment Plan</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="report-item">AI Recommendations</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="report-item">Future Projections</div>',
                unsafe_allow_html=True
            )

            st.download_button(
                'Download Complete PDF Report',
                data=pdf_bytes,
                file_name="patient_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        # pdf download

    
    


    
    
