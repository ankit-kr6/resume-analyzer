import streamlit as st
from analyzer import extract_text_from_pdf, load_skills_db, extract_skills_from_resume, get_skill_gap

st.set_page_config(page_title="Resume Analyzer", page_icon="📄")
st.title("📄 Resume Analyzer + Skill Gap Detector")
st.markdown("Upload your resume and select a target job role to see your skill gap report.")

skills_db = load_skills_db()
job_roles = list(skills_db.keys())

uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
selected_role = st.selectbox("Select Target Job Role", job_roles)

if uploaded_file and selected_role:
    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.read())

    resume_text = extract_text_from_pdf("temp_resume.pdf")
    required_skills = skills_db[selected_role]
    all_skills_flat = list(set(s for skills in skills_db.values() for s in skills))

    resume_skills = extract_skills_from_resume(resume_text, all_skills_flat)
    matched, missing = get_skill_gap(resume_skills, required_skills)

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✅ Skills You Have")
        if matched:
            for skill in matched:
                st.success(skill)
        else:
            st.warning("No matching skills found")

    with col2:
        st.subheader("❌ Skills You're Missing")
        if missing:
            for skill in missing:
                st.error(skill)
        else:
            st.balloons()
            st.success("No gaps! You're a perfect fit! 🎉")

    st.divider()
    score = int((len(matched) / len(required_skills)) * 100) if required_skills else 0
    st.subheader(f"🎯 Match Score: {score}%")
    st.progress(score / 100)

    if score >= 80:
        st.success("Excellent match! You're well suited for this role.")
    elif score >= 50:
        st.warning("Good match! Focus on the missing skills to improve.")
    else:
        st.error("Low match. Consider building more skills for this role.")