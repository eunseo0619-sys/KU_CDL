import streamlit as st
from document_processor import load_documents, search_documents

# ── 페이지 설정 ──────────────────────────────────────────────
st.set_page_config(
    page_title="CDL 근로장학생 도우미",
    page_icon="📚",
    layout="centered",
)

st.title("📚 CDL 근로장학생 도우미")
st.caption("인수인계 규정과 도서관 규정을 기반으로 답변합니다.")

# ── 문서 로드 (최초 1회만) ───────────────────────────────────
@st.cache_resource(show_spinner="문서를 불러오는 중...")
def get_docs():
    return load_documents()

docs = get_docs()

# 파일 누락 경고
if docs.get("missing"):
    st.warning(
        "⚠️ 아래 파일이 `docs/` 폴더에 없어요. 파일을 추가해 주세요:\n\n"
        + "\n".join(f"- `{f}`" for f in docs["missing"])
    )

# ── 채팅 기록 초기화 ─────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕하세요! CDL 근로장학생 도우미예요 😊\n\n"
                "도서관 규정이나 업무 관련 궁금한 점을 물어보세요.\n\n"
                "예시 질문:\n"
                "- 대출 기간이 얼마나 돼요?\n"
                "- 연체료는 얼마예요?\n"
                "- 개관 시간이 어떻게 돼요?\n"
                "- 분실 처리는 어떻게 해요?"
            ),
        }
    ]

# 이전 메시지 표시
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── 사용자 입력 처리 ─────────────────────────────────────────
if prompt := st.chat_input("질문을 입력하세요..."):
    # 사용자 메시지 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 검색 및 응답 생성
    with st.chat_message("assistant"):
        if not docs["chunks"]:
            answer = "❌ 문서 파일을 찾을 수 없어요. `docs/` 폴더에 워드 파일을 넣어주세요."
        else:
            results = search_documents(docs, prompt, top_k=4)
            if not results:
                answer = (
                    "🤔 관련 내용을 찾지 못했어요.\n\n"
                    "다른 표현으로 다시 질문해 보거나, "
                    "더 구체적으로 물어봐 주세요."
                )
            else:
                lines = [f"**'{prompt}'** 관련 내용이에요:\n"]
                for i, r in enumerate(results, 1):
                    heading_str = f" > {r['heading']}" if r["heading"] else ""
                    lines.append(f"---\n**📄 [{r['source']}{heading_str}]**")
                    lines.append(r["text"])
                answer = "\n\n".join(lines)

        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
