import streamlit as st
import numpy as np
import joblib
import warnings

warnings.filterwarnings("ignore")

# Load model
model = joblib.load("best_model.pkl")

# Page configuration
st.set_page_config(
    page_title="Student Exam Score Predictor",
    page_icon=None,
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>

.main-title {
    text-align: center;
    color: #2563eb;
    font-size: 36px;
    font-weight: bold;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #666666;
    font-size: 17px;
    margin-bottom: 30px;
}

.prediction {
    background-color: #eff6ff;
    border: 2px solid #2563eb;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    margin-top: 25px;
}

.score {
    color: #2563eb;
    font-size: 42px;
    font-weight: bold;
}

.footer {
    text-align: center;
    color: #777777;
    margin-top: 35px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


# Title
st.markdown(
    '<div class="main-title">Student Exam Score Predictor</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Predict a student\'s exam score using academic and lifestyle factors.'
    '</div>',
    unsafe_allow_html=True
)


# Input section
st.subheader("Student Information")

col1, col2 = st.columns(2)

with col1:

    study_hours = st.slider(
        "Study Hours Per Day",
        0.0,
        8.3,
        3.5,
        0.1
    )

    attendance = st.slider(
        "Attendance Percentage",
        56.0,
        100.0,
        84.0,
        0.1
    )

    mental_health = st.slider(
        "Mental Health Rating",
        1,
        10,
        5
    )

with col2:

    sleep_hours = st.slider(
        "Sleep Hours",
        3.2,
        10.0,
        6.5,
        0.1
    )

    part_time_job = st.selectbox(
        "Part-time Job",
        ["No", "Yes"]
    )

    ptj_encoded = 1 if part_time_job == "Yes" else 0


# Prediction button
if st.button("Predict Exam Score", use_container_width=True):

    input_data = np.array([[
        study_hours,
        attendance,
        mental_health,
        sleep_hours,
        ptj_encoded
    ]])

    prediction = model.predict(input_data)[0]

    # Keep prediction between 0 and 100
    prediction = max(0, min(100, prediction))

    # Score category
    if prediction >= 90:
        result = "Excellent"
    elif prediction >= 75:
        result = "Very Good"
    elif prediction >= 60:
        result = "Good"
    elif prediction >= 50:
        result = "Average"
    else:
        result = "Needs Improvement"

    # Display prediction
    st.markdown(
        f"""
        <div class="prediction">
            <h3>Predicted Exam Score</h3>
            <div class="score">{prediction:.2f}</div>
            <p>out of 100</p>
            <h4>{result}</h4>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Progress bar
    st.write("")
    st.progress(int(prediction))

    # Input summary
    st.write("### Input Summary")

    c1, c2, c3 = st.columns(3)

    c1.metric("Study Hours", f"{study_hours} hrs")
    c2.metric("Attendance", f"{attendance}%")
    c3.metric("Sleep", f"{sleep_hours} hrs")


# Footer
st.markdown(
    """
    <div class="footer">
        Student Exam Score Prediction | Machine Learning Project
    </div>
    """,
    unsafe_allow_html=True
)