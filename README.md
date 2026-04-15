# 🤖 AI-Powered Resume Analyzer + Skill Gap Detector

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red?style=for-the-badge&logo=streamlit)
![NLP](https://img.shields.io/badge/NLP-TF--IDF-green?style=for-the-badge)
![ML](https://img.shields.io/badge/ML-Cosine_Similarity-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**An AI/ML-powered web application that analyzes resumes using TF-IDF Vectorization and Cosine Similarity to detect skill gaps for target job roles.**

[Features](#features) • [AI Algorithms](#ai-ml-algorithms-used) • [Setup](#setup-instructions) • [Usage](#usage) • [Job Roles](#supported-job-roles)

</div>

---

## 👨‍💻 Student Details

| Field | Details |
|-------|---------|
| **Name** | Ankit Kumar Mandal |
| **Registration No.** | 25BAI10217 |
| **Branch** | CSE (AI & ML) |
| **Year** | First Year B.Tech |
| **University** | VIT Bhopal University |
| **Course** | CSA2001 — Bring Your Own Project (BYOP) |

---

## 🎯 Project Overview

The **AI-Powered Resume Analyzer + Skill Gap Detector** solves a real-world problem: students and job seekers don't know which skills they're missing for their target roles.

**How it works:**
1. User uploads their resume as a PDF
2. `pdfplumber` extracts all text from the PDF
3. **TF-IDF Vectorization** converts text into numerical vectors
4. **Cosine Similarity** computes semantic match between resume and job role
5. **Hybrid scoring** combines keyword matching (60%) + AI similarity (40%)
6. Results displayed with matched skills, missing skills, and match score

---

## 🧠 AI/ML Algorithms Used

### 1. TF-IDF Vectorization (Term Frequency — Inverse Document Frequency)
```
TF(t, d)  = (Number of times term t appears in document d) / (Total terms in d)
IDF(t, D) = log((N + 1) / (df(t) + 1)) + 1
TF-IDF    = TF × IDF
```
Converts raw resume text into meaningful numerical vectors that capture the importance of each term relative to all documents.

### 2. Cosine Similarity
```
similarity(A, B) = (A · B) / (||A|| × ||B||)
```
Measures the cosine of the angle between the resume vector and the job role skills vector. Returns 0 (no match) to 1 (perfect match).

### 3. Hybrid Scoring Model
```
Final Score = (Keyword Match Score × 0.6) + (AI Similarity Score × 0.4)
```
Combines keyword-based exact matching with semantic TF-IDF similarity for more accurate results than either method alone.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| PDF Upload | Upload any PDF resume via browser |
| TF-IDF Analysis | Real NLP vectorization of resume text |
| Cosine Similarity | ML-based semantic matching algorithm |
| Hybrid AI Score | Weighted combination of keyword + AI scores |
| 8 Job Roles | Data Scientist, Web Dev, DevOps, SWE, Data Analyst, ML Engineer, AI Engineer, Cloud Engineer |
| Skill Breakdown | Color-coded matched vs missing skills |
| Learning Path | Recommended resources for missing skills |
| AI Explainer | Transparent breakdown of how score was computed |

---

## 🛠️ Tech Stack

```
Language    : Python 3.10+
Framework   : Streamlit (Web Application)
PDF Parser  : pdfplumber
NLP Engine  : Custom TF-IDF + Cosine Similarity (implemented from scratch)
Database    : JSON (skills_db.json)
Version     : Git & GitHub
```

---

## 📁 Project Structure

```
resume-analyzer/
├── app.py              # Main Streamlit application
├── analyzer.py         # AI/ML engine: TF-IDF + Cosine Similarity
├── skills_db.json      # Job roles → required skills database
├── requirements.txt    # Python dependencies
├── sample_resume.pdf   # Sample resume for testing
└── README.md           # Documentation
```

---

## 💼 Supported Job Roles

| Job Role | Key Skills |
|----------|-----------|
| Data Scientist | Python, ML, SQL, Statistics, TensorFlow, Pandas, NumPy |
| Web Developer | HTML, CSS, JavaScript, React, Node.js, REST API |
| DevOps Engineer | Docker, Kubernetes, CI/CD, Linux, AWS, Jenkins |
| Software Engineer | Data Structures, Algorithms, OOP, Git, SQL |
| Data Analyst | Excel, SQL, Python, Tableau, Power BI, Statistics |
| ML Engineer | Python, TensorFlow, PyTorch, ML, Docker, REST API |
| AI Engineer | Python, Deep Learning, NLP, TensorFlow, Computer Vision |
| Cloud Engineer | AWS, Azure, Docker, Kubernetes, Linux, Terraform |

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/ankit-kr6/resume-analyzer
cd resume-analyzer
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
streamlit run app.py
```

> ✅ Fully CLI-executable — single command launches the entire application.

### Step 4: Use the Application
- Browser opens at `http://localhost:8501`
- Upload PDF resume
- Select target job role
- View AI-powered skill gap analysis

---

## 🧪 Quick Test

```bash
git clone https://github.com/ankit-kr6/resume-analyzer
cd resume-analyzer
pip install -r requirements.txt
streamlit run app.py
# Upload sample_resume.pdf → Select "Data Scientist" → View results
```

---

## 📊 Algorithm Flow

```
PDF Resume
    ↓
pdfplumber (text extraction)
    ↓
tokenize() → clean & split text
    ↓
compute_tf() → Term Frequency
    ↓
compute_idf() → Inverse Document Frequency
    ↓
compute_tfidf_vector() → TF-IDF Vector
    ↓
cosine_similarity() → Semantic Match Score
    ↓
compute_weighted_match_score() → Hybrid Final Score
    ↓
Streamlit UI → Visual Results
```

---

## 📈 Syllabus Concepts Applied (AI & ML)

| Concept | Implementation |
|---------|---------------|
| NLP — Text Processing | Tokenization, TF-IDF vectorization |
| ML — Similarity Metrics | Cosine Similarity algorithm |
| Mathematics | Vector dot products, magnitudes, logarithms |
| Data Structures | Dictionaries for TF-IDF vectors, Lists for skills |
| File Handling | PDF text extraction using pdfplumber |
| Web Development | Streamlit interactive web application |
| JSON | Skills database storage and retrieval |
| Algorithm Design | Hybrid scoring model (weighted combination) |

---

## 📝 Requirements

```
streamlit
pdfplumber
```

Install: `pip install -r requirements.txt`

---

## 🔮 Future Scope

- Integration of pre-trained BERT/Word2Vec models for deeper semantic matching
- LinkedIn API integration for real-time job market skill requirements
- Support for DOCX and TXT resume formats
- Resume improvement suggestions with course recommendations
- ATS (Applicant Tracking System) score simulation
- Named Entity Recognition (NER) for better skill extraction

---

<div align="center">

**Made with ❤️ by Ankit Kumar Mandal | VIT Bhopal University**

[GitHub](https://github.com/ankit-kr6) • [LinkedIn](https://linkedin.com/in/ankit-kumar-mandal-78b66436b) • [Kaggle](https://kaggle.com/ankitkr6)

</div>
