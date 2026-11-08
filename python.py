"""
grade_app.py - Student Grade Manager (Streamlit)

Run:
    pip install streamlit
    streamlit run grade_app.py        # not "python grade_app.py"
"""

import streamlit as st


# --------------------------------------------------------------------------
# Day 2 grading logic - paste your own get_grade() here if your scale differs.
# --------------------------------------------------------------------------
def get_grade(mark: float) -> str:
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "F"


# --------------------------------------------------------------------------
# Page setup
# --------------------------------------------------------------------------
st.set_page_config(page_title="Student Grade Manager", page_icon="🎓")
st.title("🎓 Student Grade Manager")

# Streamlit re-runs this whole file on every click.
# A plain `students = []` would be reset to empty each time,
# so the list lives in st.session_state, which survives reruns.
if "students" not in st.session_state:
    st.session_state.students = []


# --------------------------------------------------------------------------
# Form to add a student
# --------------------------------------------------------------------------
with st.form("add", clear_on_submit=True):
    col1, col2 = st.columns([2, 1])
    name = col1.text_input("Name")
    # min/max stop marks outside 0-100 right in the interface
    mark = col2.number_input("Mark", min_value=0, max_value=100, step=1)
    submitted = st.form_submit_button("Add")

    if submitted:
        name = name.strip()
        if not name:
            st.error("Please enter a name.")
        elif not 0 <= mark <= 100:          # extra safety check
            st.error("Mark must be between 0 and 100.")
        else:
            st.session_state.students.append(
                {"Name": name, "Mark": int(mark), "Grade": get_grade(mark)}
            )
            st.success(f"Added {name} - {int(mark)} ({get_grade(mark)})")


# --------------------------------------------------------------------------
# Results table and class figures
# --------------------------------------------------------------------------
students = st.session_state.students

if students:
    marks = [s["Mark"] for s in students]

    st.subheader("Class figures")
    c1, c2, c3 = st.columns(3)
    c1.metric("Average", f"{sum(marks) / len(marks):.1f}")
    c2.metric("Highest", max(marks))
    c3.metric("Lowest", min(marks))

    st.subheader(f"Students ({len(students)})")
    st.table(students)

    if st.button("Clear all students"):
        st.session_state.students = []
        st.rerun()
else:
    st.info("No students yet - add one using the form above.")