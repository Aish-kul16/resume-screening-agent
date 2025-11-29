# 🧠 AI Resume Screening Agent 

This project is an AI-powered Resume Screening Agent that ranks candidate resumes based on how well they match a given Job Description (JD).

Unlike many AI agents, this one is:

- ✅ Completely offline (no external APIs)
- ✅ **100% free to run** (no OpenAI / Claude / Gemini keys)
- ✅ **Fast and lightweight**
- ✅ Built with **Streamlit** + **scikit-learn**

---

## 🚀 What It Does

1. You paste a **Job Description**.
2. You upload one or more **PDF resumes**.
3. The agent:
   - Extracts text from each resume.
   - Uses **TF-IDF + Cosine Similarity** to measure how close each resume is to the JD.
   - Calculates a **score (0–100)** for each resume.
   - Identifies basic **strengths** (matching keywords) and **gaps** (missing keywords).
4. It then shows a ranked list of candidates from **best match → lowest match**.

This is ideal as a **first-pass resume filter** in an HR process.

---

## 🧱 Tech Stack

- **Language:** Python
- **UI:** [Streamlit](https://streamlit.io/)
- **ML / Scoring:**
  - `scikit-learn` (TF-IDF, cosine similarity)
- **PDF Text Extraction:**
  - `PyPDF2`
- **APIs Used:** None (fully offline ML, no external services)


---

## 🏗 Project Structure

```bash
resume-screening-agent/
├── app.py           # Streamlit UI
├── screening.py     # Core logic: PDF reading + TF-IDF scoring
├── requirements.txt # Python dependencies
└── venv/            # Local virtual environment (not needed on GitHub ideally)
