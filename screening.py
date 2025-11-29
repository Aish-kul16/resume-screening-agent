import io
from typing import List, Dict, Any

import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        try:
            text += page.extract_text() + "\n"
        except:
            continue
    return text.strip()


def simple_clean(text: str) -> str:
    return " ".join(
        word.lower()
        for word in text.split()
        if len(word) > 2
    )


def extract_keywords(jd: str, resume: str, top_n: int = 5) -> Dict[str, List[str]]:
    jd_words = set(simple_clean(jd).split())
    cv_words = set(simple_clean(resume).split())

    strengths = list(jd_words & cv_words)[:top_n]
    gaps = list(jd_words - cv_words)[:top_n]

    return {"strengths": strengths, "gaps": gaps}


def call_model(job_description: str, resume_text: str) -> Dict[str, Any]:
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf = vectorizer.fit_transform([job_description, resume_text])
    similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

    score = float(similarity * 100)
    kw = extract_keywords(job_description, resume_text)

    summary = f"Resume matches job description with a score of {score:.1f}."

    return {
        "score": score,
        "summary": summary,
        "strengths": kw["strengths"],
        "gaps": kw["gaps"],
    }


def screen_resumes(job_description: str, uploaded_files) -> List[Dict[str, Any]]:
    results = []

    for file in uploaded_files:
        file_bytes = file.read()
        resume_text = extract_text_from_pdf(file_bytes)

        evaluation = call_model(job_description, resume_text)

        results.append({
            "file_name": file.name,
            "score": evaluation["score"],
            "summary": evaluation["summary"],
            "strengths": evaluation["strengths"],
            "gaps": evaluation["gaps"],
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results
