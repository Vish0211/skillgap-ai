import streamlit as st
import pdfplumber
import math

st.set_page_config(page_title="SkillGap AI", page_icon="🚀", layout="centered")

# --- Custom Styling ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.main-header {
    background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #A855F7 100%) !important;
    padding: 35px 20px;
    border-radius: 16px;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0 8px 20px rgba(139, 92, 246, 0.35);
}
.main-header h1 {
    color: white !important;
    font-size: 2.3rem;
    margin: 0;
    text-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
.main-header p {
    color: #F3E8FF !important;
    margin-top: 10px;
    font-size: 1.05rem;
}

[data-testid="stMarkdownContainer"] .section-card,
.section-card {
    background-color: #F9FAFB !important;
    border-radius: 14px !important;
    padding: 20px 24px !important;
    margin-bottom: 18px !important;
    border: 1px solid #E5E7EB !important;
}
.section-card h3 {
    color: #4F46E5 !important;
}

/* Sidebar styling - forced regardless of light/dark toggle */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
section[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg, #4F46E5 0%, #7C3AED 100%) !important;
}
[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}
.sidebar-card {
    background-color: rgba(255,255,255,0.12) !important;
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 12px;
}
.sidebar-card h3 {
    color: #FFFFFF !important;
}
.sidebar-card p {
    color: #F3E8FF !important;
}

.stButton>button {
    background: linear-gradient(90deg, #6366F1, #8B5CF6) !important;
    color: white !important;
    border-radius: 10px;
    border: none;
    padding: 8px 20px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="main-header">
    <h1>🚀 SkillGap AI</h1>
    <p>Upload your resume, pick your dream role, and find your skill gaps!</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div class="sidebar-card">
        <h3>ℹ️ How it works</h3>
        <p>1. Upload your resume (PDF)</p>
        <p>2. Pick your dream job role</p>
        <p>3. See your skill gaps</p>
        <p>4. Get a 30-day roadmap, project ideas, and interview questions</p>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Built by Vishwapriya • Python, Streamlit, pdfplumber")

# --- Skill database for each role ---
ROLE_SKILLS = {
    "Python Developer": ["python", "django", "flask", "sql", "git", "rest api", "oop", "debugging"],
    "Data Analyst": ["python", "sql", "excel", "power bi", "tableau", "pandas", "numpy", "statistics"],
    "AI Engineer": ["python", "machine learning", "deep learning", "pytorch", "tensorflow",
                     "sql", "fastapi", "docker", "nlp", "computer vision"],
    "Web Developer": ["html", "css", "javascript", "react", "node.js", "git", "rest api", "sql"],
}

PROJECT_SUGGESTIONS = {
    "Python Developer": ["Blog CMS with Django", "REST API for a To-Do App", "Automated File Organizer Script"],
    "Data Analyst": ["Sales Dashboard in Power BI", "COVID Data Trend Analysis", "Customer Churn EDA with Pandas"],
    "AI Engineer": ["Resume Analyzer (like this one!)", "Chat with PDF using LLMs", "Image Classifier with PyTorch"],
    "Web Developer": ["Portfolio Website with React", "E-commerce Cart with Node.js", "Real-time Chat App"],
}

INTERVIEW_QUESTIONS = {
    "Python Developer": ["What is the difference between a list and a tuple?",
                          "Explain Python's GIL.",
                          "How does Django's ORM work?"],
    "Data Analyst": ["What is the difference between WHERE and HAVING in SQL?",
                      "How do you handle missing data in a dataset?",
                      "Explain the difference between correlation and causation."],
    "AI Engineer": ["What is the difference between supervised and unsupervised learning?",
                     "Explain backpropagation in simple terms.",
                     "What is overfitting and how do you prevent it?"],
    "Web Developer": ["What is the virtual DOM in React?",
                       "Explain the difference between GET and POST requests.",
                       "What is CORS and why does it matter?"],
}

uploaded_file = st.file_uploader("Upload your resume (PDF only)", type="pdf")
target_role = st.selectbox("Select your dream job role", list(ROLE_SKILLS.keys()))

if uploaded_file is not None:
    with st.spinner("Analyzing your resume..."):
        with pdfplumber.open(uploaded_file) as pdf:
            resume_text = ""
            for page in pdf.pages:
                resume_text += page.extract_text() or ""

        resume_text_lower = resume_text.lower()

        if len(resume_text.strip()) < 30:
            st.warning("⚠️ We couldn't read much text from this PDF. It might be a scanned/image-based resume. Try uploading a text-based PDF instead.")

        required_skills = ROLE_SKILLS[target_role]
        have_skills = [s for s in required_skills if s in resume_text_lower]
        missing_skills = [s for s in required_skills if s not in resume_text_lower]

    st.markdown(f'<div class="section-card"><h3 style="color:#4F46E5; margin:0;">Skill Analysis for {target_role}</h3></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.success("✅ Skills You Have")
        for s in have_skills:
            st.write(f"- {s.title()}")

    with col2:
        st.error("❌ Missing Skills")
        for s in missing_skills:
            st.write(f"- {s.title()}")

    st.divider()

    if missing_skills:
        st.subheader("📅 Your 30-Day Roadmap")
        chunk_size = math.ceil(len(missing_skills) / 4)
        weeks = [missing_skills[i:i + chunk_size] for i in range(0, len(missing_skills), chunk_size)]
        week_labels = ["Week 1", "Week 2", "Week 3", "Week 4"]
        for i, week_skills in enumerate(weeks):
            if week_skills:
                skills_str = ", ".join(s.title() for s in week_skills)
                st.markdown(f"**{week_labels[i]}:** Learn {skills_str}")
    else:
        st.success("🎉 You already have all the key skills for this role!")

    st.divider()

    st.subheader("💡 Suggested Projects")
    for proj in PROJECT_SUGGESTIONS[target_role]:
        st.write(f"- {proj}")

    st.divider()

    st.subheader("🎯 Sample Interview Questions")
    for q in INTERVIEW_QUESTIONS[target_role]:
        st.write(f"- {q}")
