import os
import re
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

DOCS_DIR = os.path.join(os.path.dirname(__file__), "docs")

DOC_FILES = {
    "인수인계": "CDL 1F, 2F 인수인계_2026.02.06 (1).docx",
    "도서관 규정": "고려대 도서관 규정 정리 - cdl 관련.docx",
}


def extract_paragraphs(path: str) -> list[dict]:
    """워드 파일에서 문단 목록을 추출합니다."""
    doc = Document(path)
    paragraphs = []
    current_heading = ""

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        # 제목 스타일이면 현재 섹션 제목으로 저장
        if para.style.name.startswith("Heading"):
            current_heading = text
        else:
            paragraphs.append({
                "text": text,
                "heading": current_heading,
            })

    # 표(table) 내용도 추출
    for table in doc.tables:
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
            if cells:
                paragraphs.append({
                    "text": " | ".join(cells),
                    "heading": current_heading,
                })

    return paragraphs


def load_documents() -> dict:
    """두 워드 파일을 읽어 검색 가능한 형태로 반환합니다."""
    all_chunks = []   # {"source", "heading", "text"}
    missing = []

    for label, filename in DOC_FILES.items():
        filepath = os.path.join(DOCS_DIR, filename)
        if not os.path.exists(filepath):
            missing.append(filename)
            continue
        paras = extract_paragraphs(filepath)
        for p in paras:
            all_chunks.append({
                "source": label,
                "heading": p["heading"],
                "text": p["text"],
            })

    if not all_chunks:
        return {"chunks": [], "vectorizer": None, "matrix": None, "missing": missing}

    texts = [c["text"] for c in all_chunks]
    vectorizer = TfidfVectorizer(
        analyzer="char_wb",   # 한국어에 유리한 문자 n-gram
        ngram_range=(2, 4),
        max_features=20000,
    )
    matrix = vectorizer.fit_transform(texts)

    return {
        "chunks": all_chunks,
        "vectorizer": vectorizer,
        "matrix": matrix,
        "missing": missing,
    }


def search_documents(docs: dict, query: str, top_k: int = 5) -> list[dict]:
    """질문과 가장 관련 있는 문단을 반환합니다."""
    if not docs["chunks"]:
        return []

    q_vec = docs["vectorizer"].transform([query])
    scores = cosine_similarity(q_vec, docs["matrix"]).flatten()
    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []
    for idx in top_indices:
        if scores[idx] < 0.05:   # 유사도가 너무 낮으면 제외
            continue
        chunk = docs["chunks"][idx]
        results.append({
            "source": chunk["source"],
            "heading": chunk["heading"],
            "text": chunk["text"],
            "score": float(scores[idx]),
        })

    return results
