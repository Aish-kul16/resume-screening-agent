import streamlit as st
from screening import screen_resumes

# ---------- Custom CSS ----------
CUSTOM_CSS = """
<style>
/* Page background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: #e5e7eb;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* Main title */
.big-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #e5e7eb;
    margin-bottom: 0.2rem;
}

/* Subtitle */
.subtitle {
    font-size: 0.95rem;
    color: #9ca3af;
    margin-bottom: 1.5rem;
}

/* Card container */
.card {
    background: #020617;
    border-radius: 16px;
    padding: 1.2rem 1.4rem;
    border: 1px solid rgba(148, 163, 184, 0.3);
    box-shadow: 0 18px 35px rgba(15, 23, 42, 0.7);
}

/* Expander styling */
.streamlit-expanderHeader {
    font-weight: 600;
    color: #e5e7eb !important;
}

.streamlit-expanderContent {
    background-color: #020617 !important;
}

/* Labels */
label, .stTextArea label, .stFileUploader label {
    font-weight: 600 !important;
    color: #e5e7eb !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #020617;
    border-right: 1px solid rgba(148, 163, 184, 0.3);
}

/* Button */
div.stButton > button:first-child {
    background: linear-gradient(135deg, #22c55e, #16a34a);
    color: white;
    border-radius: 999px;
    padding: 0.6rem 1.4rem;
    border: none;
    font-weight: 600;
    box-shadow: 0 12px 25px rgba(34, 197, 94, 0.3);
}

div.stButton > button:first-child:hover {
    background: linear-gradient(135deg, #16a34a, #22c55e);
    box-shadow: 0 14px 28px rgba(34, 197, 94, 0.5);
}

/* Dataframe tweaks */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}
</style>
"""

st.set_page_config(
    page_title="AI Resume Screening Agent",
    page_icon="🧠",
    layout="wide",
)

# Inject CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------- Layout ----------

# Top section
with st.container():
    st.markdown('<div class="big-title">🧠 AI Resume Screening Agent</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Ranks resumes against a job description using TF-IDF & cosine similarity.</div>',
        unsafe_allow_html=True,
    )

# Sidebar
st.sidebar.header("📌 How to use")
st.sidebar.markdown("1. Paste the **Job Description** in the text area.")
st.sidebar.markdown("2. Upload one or more **PDF resumes**.")
st.sidebar.markdown("3. Click **Run Screening** to see ranked candidates.")
st.sidebar.markdown("---")


# Main layout with two columns
left_col, right_col = st.columns([2, 1])

with left_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    job_description = st.text_area(
        "Job Description",
        placeholder="Paste the full job description here...",
        height=220,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Upload candidate resumes (PDF only)",
        type=["pdf"],
        accept_multiple_files=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")  # small vertical space

# Run button in center
button_col = st.container()
with button_col:
    run_button = st.button("🚀 Run Screening")

# ---------- Logic ----------
if run_button:
    if not job_description.strip():
        st.error("Please paste a job description.")
    elif not uploaded_files:
        st.error("Please upload at least one PDF resume.")
    else:
        with st.spinner("Analyzing resumes..."):
            results = screen_resumes(job_description, uploaded_files)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Ranked Results")

        if not results:
            st.warning("No results generated. Check the PDFs or try with different resumes.")
        else:
            for i, r in enumerate(results):
                with st.expander(f"{i+1}. {r['file_name']} — Score: {r['score']:.1f}"):
                    st.markdown(f"**Summary:** {r['summary']}")
                    st.markdown("**Strengths (keywords matched):**")
                    if r["strengths"]:
                        for s in r["strengths"]:
                            st.markdown(f"- `{s}`")
                    else:
                        st.write("None detected.")

                    st.markdown("**Gaps (keywords missing):**")
                    if r["gaps"]:
                        for g in r["gaps"]:
                            st.markdown(f"- `{g}`")
                    else:
                        st.write("None detected.")
        st.markdown("</div>", unsafe_allow_html=True)
