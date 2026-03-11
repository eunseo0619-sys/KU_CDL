# CDL 근로장학생 도우미 챗봇

고려대학교 CDL 근로장학생을 위한 챗봇입니다.
도서관 규정 및 인수인계 문서를 기반으로 질문에 답변합니다.

---

## 📁 워드 파일 추가하기

`docs/` 폴더 안에 아래 두 파일을 넣어주세요:

```
docs/
├── CDL 1F, 2F 인수인계_2026.02.06 (1).docx
└── 고려대 도서관 규정 정리 - cdl 관련.docx
```

> ⚠️ 파일 이름을 정확히 맞춰야 합니다.

---

## 🚀 배포 방법 (Streamlit Cloud - 무료)

### 1단계: 깃허브에 올리기
1. [github.com](https://github.com) 접속 → 로그인
2. 이 레포지토리를 **Private**으로 설정 (내부 문서 보호)
3. `docs/` 폴더에 워드 파일 추가 후 커밋

### 2단계: Streamlit Cloud에서 배포
1. [share.streamlit.io](https://share.streamlit.io) 접속
2. GitHub 계정으로 로그인
3. **New app** → 이 레포지토리 선택
4. Main file: `app.py` 선택
5. **Deploy** 클릭

배포 완료 후 링크를 공유하면 누구나 접속 가능합니다!

---

## 💻 로컬에서 실행하기 (내 PC에서만)

```bash
pip install -r requirements.txt
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 열기
