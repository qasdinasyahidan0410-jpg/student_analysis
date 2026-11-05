import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title("Student Test Score Analysis System")
st.subheader("English Course")

if "students" not in st.session_state:
    st.session_state.students = []

with st.form("student_form"):

    student_name = st.text_input("Student Name")

    gender = st.radio("Gender", ["Male", "Female"])

    score = st.number_input(
        "Score",
        min_value=0,
        max_value=100,
        step=1
    )

    submit = st.form_submit_button(
        "Submit",
        disabled=len(st.session_state.students) >= 3
    )

    if submit:
        try:
            if student_name.strip() == "":
                raise ValueError("Student name cannot be empty")

            if len(st.session_state.students) >= 3:
                raise ValueError("Only three students are allowed")

            student = {
                "Student Name": student_name,
                "Gender": gender,
                "Score": score
            }

            st.session_state.students.append(student)

            st.success("Student information submitted successfully")

        except ValueError as e:
            st.error(str(e))

if len(st.session_state.students) == 3:

    st.header("Student Score Analysis")

    names = []
    genders = []
    student_scores = []

    for student in st.session_state.students:
        names.append(student["Student Name"])
        genders.append(student["Gender"])
        student_scores.append(student["Score"])

    scores = np.array(student_scores)

    mean_score = np.mean(scores)
    max_score = np.max(scores)

    st.write("Mean Score:", format(mean_score, ".2f"))
    st.write("Maximum Score:", max_score)

    results = []

    for mark in scores:
        if mark >= 50:
            results.append("Pass")
        else:
            results.append("Fail")

    data = {
        "Student Name": names,
        "Gender": genders,
        "Score": scores,
        "Result": results
    }

    df = pd.DataFrame(data)

    df = df.sort_values(by="Score", ascending=True)

    st.subheader("Student Results")

    st.dataframe(df)

    st.subheader("Student Score Graph")

    fig, ax = plt.subplots()

    ax.bar(df["Student Name"], df["Score"])

    ax.set_xlabel("Student Name")
    ax.set_ylabel("Score")
    ax.set_title("English Test Scores")

    st.pyplot(fig)

else:
    st.info(
        "Please submit information for "
        + str(3 - len(st.session_state.students))
        + " more student(s)."
    )
