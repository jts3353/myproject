import os
import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(
    page_title="머신러닝 문제 해결 사례", page_icon="💡", layout="wide"
)

st.title("💡 머신러닝 문제 해결 사례")
st.caption(
    "htmls 폴더 내의 aa.html 파일을 읽어와 1024x768 규격으로 렌더링합니다."
)

st.markdown("---")

# -----------------------------------------------------------------------------
# 1. htmls 폴더 내부의 aa.html 파일 경로 지정
# -----------------------------------------------------------------------------
HTML_FILE_PATH = os.path.join("htmls", "aa.html")

# -----------------------------------------------------------------------------
# 2. HTML 파일 존재 여부 확인 및 렌더링
# -----------------------------------------------------------------------------
if os.path.exists(HTML_FILE_PATH):
    # HTML 파일 읽기 (UTF-8)
    with open(HTML_FILE_PATH, "r", encoding="utf-8") as f:
        html_content = f.read()

    # 1024x768 크기 고정 및 상하/좌우 스크롤바(overflow: auto) 설정
    wrapped_html = f"""
    <div style="
        width: 1024px; 
        height: 768px; 
        overflow: auto; 
        border: 1px solid #cbd5e1; 
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        background-color: #ffffff;
    ">
        {html_content}
    </div>
    """

    # Streamlit Component를 통한 HTML 렌더링
    components.html(wrapped_html, height=780, scrolling=True)

else:
    # 파일이 없을 경우 예외 처리 안내
    st.error(f"⚠️ '{HTML_FILE_PATH}' 파일을 찾을 수 없습니다.")
    st.info(
        """
        **폴더 구조를 확인해 주세요:**
        - `mywork/htmls/aa.html` 위치에 파일이 존재하는지 확인해 주세요.
        """
    )