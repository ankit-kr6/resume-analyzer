import pdfplumber
import json

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def load_skills_db():
    with open("skills_db.json", "r") as f:
        return json.load(f)

def extract_skills_from_resume(resume_text, all_skills):
    resume_text_lower = resume_text.lower()
    found = [skill for skill in all_skills if skill.lower() in resume_text_lower]
    return found

def get_skill_gap(resume_skills, required_skills):
    matched = [s for s in required_skills if s in resume_skills]
    missing = [s for s in required_skills if s not in resume_skills]
    return matched, missing