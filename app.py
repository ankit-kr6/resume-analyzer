import streamlit as st
from analyzer import (
    extract_text_from_pdf,
    load_skills_db,
    extract_skills_from_resume,
    get_skill_gap,
    compute_weighted_match_score,
    compute_ai_match_score
)

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Resume Analyzer + Skill Gap Detector",
    page_icon="🤖",
    layout="wide"
)

# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────
st.title("🤖 AI-Powered Resume Analyzer + Skill Gap Detector")
st.markdown("""
> **How it works:** Upload your resume → Select a job role → Get AI-powered skill gap analysis  
> Uses **TF-IDF Vectorization** + **Cosine Similarity** (NLP/ML algorithms) to analyze your resume
""")
st.divider()

# ─────────────────────────────────────────────────────────────
# SIDEBAR — About the AI
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("🧠 AI/ML Algorithms Used")
    st.markdown("""
    **1. TF-IDF Vectorization**
    - TF = Term Frequency
    - IDF = Inverse Document Frequency
    - Converts text into numerical vectors

    **2. Cosine Similarity**
    - Measures angle between two vectors
    - Score: 0 (no match) → 1 (perfect match)
    - Formula: (A·B) / (||A|| × ||B||)

    **3. Hybrid Scoring**
    - Keyword Match: 60% weight
    - AI Similarity: 40% weight
    - Final = weighted combination

    **Tech Stack**
    - Python 3.10+
    - Streamlit
    - pdfplumber
    - Custom NLP Engine
    """)
    st.divider()
    st.markdown("**CSA2001 — BYOP Project**")
    st.markdown("Ankit Kumar Mandal | 25BAI10217")
    st.markdown("CSE (AI & ML) | VIT Bhopal")

# ─────────────────────────────────────────────────────────────
# MAIN — INPUT
# ─────────────────────────────────────────────────────────────
skills_db = load_skills_db()
job_roles = list(skills_db.keys())

col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader(
        "📄 Upload Your Resume (PDF)",
        type=["pdf"],
        help="Upload your resume in PDF format for analysis"
    )
with col2:
    selected_role = st.selectbox(
        "💼 Select Target Job Role",
        job_roles,
        help="Choose the job role you are targeting"
    )

# ─────────────────────────────────────────────────────────────
# ANALYSIS
# ─────────────────────────────────────────────────────────────
if uploaded_file and selected_role:

    # Save uploaded file temporarily
    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.read())

    # Extract text from PDF
    with st.spinner("🔍 Extracting text from PDF..."):
        resume_text = extract_text_from_pdf("temp_resume.pdf")

    if not resume_text.strip():
        st.error("❌ Could not extract text from this PDF. Please try another file.")
        st.stop()

    # Get required skills for selected role
    required_skills = skills_db[selected_role]

    # Get all unique skills across all roles
    all_skills_flat = list(set(s for skills in skills_db.values() for s in skills))

    # Extract skills from resume
    with st.spinner("🧠 Running AI skill extraction..."):
        resume_skills = extract_skills_from_resume(resume_text, all_skills_flat)
        matched, missing = get_skill_gap(resume_skills, required_skills)

    # Compute weighted AI score
    with st.spinner("📊 Computing TF-IDF + Cosine Similarity score..."):
        scores = compute_weighted_match_score(
            matched, required_skills, resume_text, required_skills
        )

    st.divider()

    # ─────────────────────────────────────────────────────────
    # RESULTS — SCORE CARDS
    # ─────────────────────────────────────────────────────────
    st.subheader(f"📊 Analysis Results for: **{selected_role}**")

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(
            label="🎯 Final AI Score",
            value=f"{scores['final_score']}%",
            delta="Hybrid AI Score"
        )
    with m2:
        st.metric(
            label="🔑 Keyword Match",
            value=f"{scores['keyword_score']}%",
            delta=f"{len(matched)}/{len(required_skills)} skills"
        )
    with m3:
        st.metric(
            label="🤖 TF-IDF Similarity",
            value=f"{scores['ai_similarity_score']}%",
            delta="Cosine Similarity"
        )

    st.divider()

    # ─────────────────────────────────────────────────────────
    # PROGRESS BAR + FEEDBACK
    # ─────────────────────────────────────────────────────────
    final = scores['final_score']
    st.subheader("🎯 Overall Match Score")
    st.progress(int(final) / 100)

    if final >= 80:
        st.success(f"🌟 Excellent Match! ({final}%) — You are highly suitable for the {selected_role} role!")
    elif final >= 60:
        st.warning(f"👍 Good Match! ({final}%) — Focus on developing the missing skills.")
    elif final >= 40:
        st.warning(f"📈 Moderate Match ({final}%) — Significant skill development needed.")
    else:
        st.error(f"📚 Low Match ({final}%) — Consider building more skills for this role.")

    st.divider()

    # ─────────────────────────────────────────────────────────
    # SKILLS BREAKDOWN
    # ─────────────────────────────────────────────────────────
    col_match, col_miss = st.columns(2)

    with col_match:
        st.subheader(f"✅ Matched Skills ({len(matched)})")
        if matched:
            for skill in matched:
                st.success(f"✓ {skill}")
        else:
            st.info("No matching skills found in your resume.")

    with col_miss:
        st.subheader(f"❌ Missing Skills ({len(missing)})")
        if missing:
            for skill in missing:
                st.error(f"✗ {skill}")
        else:
            st.balloons()
            st.success("🎉 No skill gaps! Perfect match!")

    st.divider()

    # ─────────────────────────────────────────────────────────
    # AI EXPLAINER
    # ─────────────────────────────────────────────────────────
    with st.expander("🧠 How the AI Score Was Computed"):
        st.markdown(f"""
        ### Algorithm Breakdown

        **Step 1: Text Extraction**
        - Extracted {len(resume_text.split())} words from your resume using pdfplumber

        **Step 2: TF-IDF Vectorization**
        - Tokenized resume text into individual terms
        - Computed Term Frequency (TF) for each word
        - Computed Inverse Document Frequency (IDF) across documents
        - Generated TF-IDF vectors for resume and job role skills

        **Step 3: Cosine Similarity**
        - Formula: similarity = (A·B) / (||A|| × ||B||)
        - Resume vector vs Job Role skills vector
        - Result: **{scores['ai_similarity_score']}%** similarity

        **Step 4: Hybrid Scoring**
        - Keyword Match Score: **{scores['keyword_score']}%** (60% weight)
        - TF-IDF AI Score: **{scores['ai_similarity_score']}%** (40% weight)
        - Final Score = (0.6 × {scores['keyword_score']}) + (0.4 × {scores['ai_similarity_score']}) = **{scores['final_score']}%**

        **Why Hybrid?**
        Keyword matching catches exact skill names while TF-IDF captures
        semantic relevance of the overall resume content to the job role.
        """)

    # ─────────────────────────────────────────────────────────
    # RECOMMENDATIONS
    # ─────────────────────────────────────────────────────────
    if missing:
        st.subheader("📚 Recommended Learning Path")
        st.info(f"To improve your match score for **{selected_role}**, focus on developing these {len(missing)} missing skills:")

        resources = {
            "Python": "python.org/doc | Kaggle Python Course (free)",
            "Machine Learning": "Coursera ML by Andrew Ng | Kaggle ML Course",
            "SQL": "sqlzoo.net | W3Schools SQL Tutorial",
            "TensorFlow": "tensorflow.org/tutorials",
            "Docker": "docs.docker.com/get-started",
            "React": "react.dev/learn",
            "JavaScript": "javascript.info",
            "AWS": "aws.amazon.com/training/free",
            "Git": "learngitbranching.js.org",
            "Pandas": "pandas.pydata.org/docs",
            "Statistics": "Khan Academy Statistics | StatQuest YouTube",
            "Power BI": "Microsoft Learn - Power BI",
            "Tableau": "Tableau Public Free Training",
            "Linux": "linuxjourney.com",
        }

        for skill in missing[:5]:  # Show top 5 recommendations
            resource = resources.get(skill, "Search on Coursera, Udemy, or YouTube")
            st.markdown(f"**{skill}** → {resource}")

else:
    st.info("👆 Please upload your resume PDF and select a target job role to begin analysis.")

    # Show sample info
    st.subheader("📋 Supported Job Roles")
    skills_db = load_skills_db()
    for role, skills in skills_db.items():
        with st.expander(f"💼 {role}"):
            st.write(", ".join(skills))
