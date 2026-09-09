import streamlit as st
import re
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="InterviewIQ",
    page_icon="🎯",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.main {
    background-color: #f8f9fc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    padding: 25px;
    border-radius: 18px;
    background: linear-gradient(135deg, #111827, #374151);
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 42px;
    margin-bottom: 5px;
}

.hero p {
    font-size: 18px;
    opacity: 0.85;
}

.score-card {
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #e5e7eb;
    background: white;
    text-align: center;
}

.small-text {
    color: #6b7280;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- ROLE KEYWORDS ----------------

ROLE_KEYWORDS = {
    "Software Developer": [
        "python", "java", "c++", "javascript", "sql",
        "github", "api", "database", "algorithm",
        "data structures", "debugging", "project"
    ],

    "AI / ML Engineer": [
        "python", "machine learning", "deep learning",
        "artificial intelligence", "numpy", "pandas",
        "scikit-learn", "model", "dataset", "training",
        "prediction", "neural network", "project"
    ],

    "Data Scientist": [
        "python", "pandas", "numpy", "statistics",
        "machine learning", "visualization", "dataset",
        "sql", "analysis", "model", "prediction"
    ],

    "Data Analyst": [
        "excel", "sql", "python", "dashboard",
        "visualization", "data", "analysis",
        "statistics", "power bi", "tableau"
    ],

    "Student / Fresher": [
        "project", "learning", "team", "communication",
        "problem", "skills", "python", "college",
        "experience", "goal"
    ]
}


# ---------------- SESSION STATE ----------------

if "history" not in st.session_state:
    st.session_state.history = []


# ---------------- ANALYSIS FUNCTION ----------------

def analyze_answer(answer, role):

    words = re.findall(r"\b[\w'-]+\b", answer.lower())
    word_count = len(words)

    filler_words = [
        "um",
        "uh",
        "like",
        "basically",
        "actually",
        "literally",
        "you know",
        "i think",
        "maybe"
    ]

    filler_count = 0

    for filler in filler_words:
        filler_count += answer.lower().count(filler)

    # Length score
    if 50 <= word_count <= 120:
        length_score = 90
    elif 30 <= word_count < 50:
        length_score = 75
    elif 120 < word_count <= 170:
        length_score = 75
    elif word_count < 30:
        length_score = 55
    else:
        length_score = 60

    # Filler score
    confidence_score = max(
        40,
        min(100, 95 - filler_count * 8)
    )

    # Structure keywords
    structure_words = [
        "first",
        "second",
        "because",
        "experience",
        "example",
        "result",
        "finally",
        "learned",
        "solved",
        "achieved",
        "improved"
    ]

    structure_count = sum(
        1 for word in structure_words
        if word in answer.lower()
    )

    structure_score = min(
        100,
        55 + structure_count * 7
    )

    # Role keyword matching
    role_keywords = ROLE_KEYWORDS[role]

    matched_keywords = [
        keyword
        for keyword in role_keywords
        if keyword in answer.lower()
    ]

    keyword_score = min(
        100,
        40 + len(matched_keywords) * 8
    )

    # Overall
    overall = round(
        (
            length_score
            + confidence_score
            + structure_score
            + keyword_score
        ) / 4
    )

    return {
        "word_count": word_count,
        "filler_count": filler_count,
        "length": length_score,
        "confidence": confidence_score,
        "structure": structure_score,
        "keywords": keyword_score,
        "overall": overall,
        "matched_keywords": matched_keywords
    }


# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">

<h1>🎯 InterviewIQ</h1>

<p>
AI-inspired interview coaching for students and aspiring professionals.
Practice. Analyze. Improve.
</p>

</div>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.header("⚙️ Interview Setup")

    role = st.selectbox(
        "Target Role",
        list(ROLE_KEYWORDS.keys())
    )

    difficulty = st.select_slider(
        "Difficulty",
        options=[
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    st.divider()

    st.markdown("### 📌 How it works")

    st.write("1️⃣ Enter a question")
    st.write("2️⃣ Write your answer")
    st.write("3️⃣ Analyze your response")
    st.write("4️⃣ Review your weaknesses")
    st.write("5️⃣ Improve and retry")

    st.divider()

    st.caption(
        "InterviewIQ • Portfolio Project"
    )


# ---------------- MAIN INPUT ----------------

st.subheader("💬 Practice Interview")

question = st.text_input(
    "Interview Question",
    placeholder="Example: Tell me about yourself."
)

answer = st.text_area(
    "Your Answer",
    height=230,
    placeholder=(
        "Write your answer naturally...\n\n"
        "Tip: Try to include your experience, "
        "skills, examples and results."
    )
)


# ---------------- ANALYZE BUTTON ----------------

if st.button(
    "🚀 Analyze My Answer",
    use_container_width=True
):

    if not question.strip():

        st.warning(
            "Please enter an interview question."
        )

    elif not answer.strip():

        st.warning(
            "Please enter your answer."
        )

    else:

        result = analyze_answer(answer, role)

        # Save history
        st.session_state.history.append({
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Role": role,
            "Score": result["overall"]
        })

        st.divider()

        # ---------------- SCORE ----------------

        st.subheader("📊 Performance Overview")

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric(
            "Overall",
            f"{result['overall']}/100"
        )

        c2.metric(
            "Clarity",
            f"{result['length']}/100"
        )

        c3.metric(
            "Confidence",
            f"{result['confidence']}/100"
        )

        c4.metric(
            "Structure",
            f"{result['structure']}/100"
        )

        c5.metric(
            "Role Match",
            f"{result['keywords']}/100"
        )

        st.divider()

        # ---------------- SCORE CHART ----------------

        st.subheader("📈 Skill Breakdown")

        categories = [
            "Clarity",
            "Confidence",
            "Structure",
            "Role Match"
        ]

        values = [
            result["length"],
            result["confidence"],
            result["structure"],
            result["keywords"]
        ]

        fig = go.Figure(
            go.Bar(
                x=categories,
                y=values,
                text=values,
                textposition="auto"
            )
        )

        fig.update_layout(
            yaxis=dict(
                range=[0, 100],
                title="Score"
            ),
            xaxis_title="Interview Skill",
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ---------------- AI STYLE FEEDBACK ----------------

        st.subheader("🧠 Smart Feedback")

        score = result["overall"]

        if score >= 85:

            st.success(
                "🔥 Excellent response! Your answer is "
                "well-balanced and interview-ready."
            )

        elif score >= 70:

            st.info(
                "👍 Good response! With a few improvements, "
                "you can make it much stronger."
            )

        else:

            st.warning(
                "💡 Your answer has potential. "
                "Focus on structure, examples and clarity."
            )

        # ---------------- STRENGTHS ----------------

        st.subheader("✅ Your Strengths")

        strengths = []

        if result["length"] >= 75:
            strengths.append(
                "Your answer has a reasonable amount of detail."
            )

        if result["confidence"] >= 80:
            strengths.append(
                "You avoided excessive filler words."
            )

        if result["structure"] >= 70:
            strengths.append(
                "Your answer contains useful structural signals."
            )

        if result["keywords"]:
            strengths.append(
                f"You included {len(result['matched_keywords'])} "
                f"role-relevant keywords."
            )

        if not strengths:
            strengths.append(
                "You completed the response — now let's improve it."
            )

        for item in strengths:
            st.write("•", item)

        # ---------------- IMPROVEMENTS ----------------

        st.subheader("🔧 What You Can Improve")

        improvements = []

        if result["word_count"] < 40:
            improvements.append(
                "Add more specific details or examples."
            )

        if result["word_count"] > 150:
            improvements.append(
                "Try making your answer more concise."
            )

        if result["filler_count"] > 2:
            improvements.append(
                "Reduce filler words and use short pauses instead."
            )

        if result["structure"] < 70:
            improvements.append(
                "Organize your answer with a clear beginning, "
                "action and result."
            )

        if result["keywords"] < 65:
            improvements.append(
                f"Include more skills related to {role}."
            )

        if not improvements:
            improvements.append(
                "Keep practicing natural delivery and confidence."
            )

        for item in improvements:
            st.write("•", item)

        # ---------------- ROLE KEYWORDS ----------------

        st.subheader("🎯 Role Relevance")

        if result["matched_keywords"]:

            st.write(
                "Keywords detected in your answer:"
            )

            st.write(
                " • ".join(
                    result["matched_keywords"]
                )
            )

        else:

            st.write(
                "No strong role-specific keywords detected yet."
            )

        # ---------------- STAR METHOD ----------------

        st.subheader("⭐ Recommended Answer Structure")

        st.info(
            """
**S — Situation**  
Explain the situation or context.

**T — Task**  
Explain what your responsibility was.

**A — Action**  
Explain what you personally did.

**R — Result**  
Explain the result or what you learned.
"""
        )

        # ---------------- DOWNLOAD REPORT ----------------

        report = f"""
INTERVIEWIQ — INTERVIEW REPORT
================================

Date:
{datetime.now().strftime("%d-%m-%Y %H:%M")}

Target Role:
{role}

Difficulty:
{difficulty}

QUESTION:
{question}

ANSWER:
{answer}

SCORES
------

Overall: {result['overall']}/100
Clarity: {result['length']}/100
Confidence: {result['confidence']}/100
Structure: {result['structure']}/100
Role Match: {result['keywords']}/100

Word Count:
{result['word_count']}

Filler Words:
{result['filler_count']}

Matched Role Keywords:
{", ".join(result['matched_keywords'])}

RECOMMENDATION
--------------

Practice the same question again after reviewing
the feedback and try to improve your score.
"""

        st.download_button(
            "📄 Download Interview Report",
            report,
            file_name="InterviewIQ_Report.txt",
            mime="text/plain",
            use_container_width=True
        )


# ---------------- HISTORY ----------------

if st.session_state.history:

    st.divider()

    st.subheader("🕘 Practice History")

    history_df = pd.DataFrame(
        st.session_state.history
    )

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )

    if len(history_df) >= 2:

        st.subheader("📈 Progress")

        progress_fig = go.Figure(
            go.Scatter(
                x=list(range(1, len(history_df) + 1)),
                y=history_df["Score"],
                mode="lines+markers"
            )
        )

        progress_fig.update_layout(
            xaxis_title="Attempt",
            yaxis_title="Overall Score",
            yaxis=dict(range=[0, 100]),
            height=350
        )

        st.plotly_chart(
            progress_fig,
            use_container_width=True
        )


# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "Built with Python • Streamlit • Plotly | InterviewIQ"
)