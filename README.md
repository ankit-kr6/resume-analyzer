# Resume Analyzer + Skill Gap Detector

A Python-based web application that analyzes a user's resume (PDF) 
against a target job role and identifies skill gaps with a match score.

## Student Details
- **Name:** Ankit Kumar Mandal
- **Registration No:** [Your Registration Number]
- **Branch:** CSE (AI & ML) | First Year B.Tech
- **University:** VIT Bhopal University
- **Course:** CSA2001 - Bring Your Own Project (BYOP)

## Project Overview
This tool helps students and job seekers identify the gap between 
their current skillset and the requirements of their target job role. 
The user uploads their resume as a PDF, selects a target job role, 
and the application extracts skills, compares them against a 
pre-defined skills database, and displays matched skills, missing 
skills, and an overall match score.

## Features
- Upload PDF resume (any format)
- Select from 6 target job roles
- View matched skills in green
- View missing skills in red
- Get a percentage match score with progress bar
- Color-coded feedback based on score

## Supported Job Roles
- Data Scientist
- Web Developer
- DevOps Engineer
- Software Engineer
- Data Analyst
- ML Engineer

## Tech Stack
- **Language:** Python 3.10+
- **Framework:** Streamlit
- **PDF Parsing:** pdfplumber
- **Data Storage:** JSON

## Project Structure
```
resume-analyzer/
├── app.py              # Main Streamlit application
├── analyzer.py         # PDF parsing and skill extraction logic
├── skills_db.json      # Job role to skills mapping database
├── requirements.txt    # Python dependencies
├── sample_resume.pdf   # Sample resume for testing
└── README.md           # Project documentation
```

## Setup Instructions

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

### Step 4: Use the Application
- Browser opens automatically at http://localhost:8501
- Upload any PDF resume using the file uploader
- Select your target job role from the dropdown
- View your skill gap report instantly

## Sample Test
A sample resume (sample_resume.pdf) is included in the repository 
for testing purposes. Upload it and select "Data Scientist" to see 
the application in action.

## How It Works
1. User uploads PDF resume
2. pdfplumber extracts all text from the PDF
3. analyzer.py matches extracted text against skills database
4. Matched and missing skills are identified
5. Match score is calculated as percentage of required skills found
6. Results displayed with color-coded visual feedback

## Requirements
```
streamlit
pdfplumber
```
