import os
import streamlit as st
from db_helper import init_db, login_user, register_user

# 페이지 기본 설정
st.set_page_config(
    page_title="Mechanical Engineering AIDT 메인", page_icon="📖", layout="wide"
)

# DB 초기화 (최초 실행 시 테이블 자동 생성)
init_db()

# 세션 상태 초기화 (로그인 정보)
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "userid" not in st.session_state:
    st.session_state["userid"] = None

# -----------------------------------------------------------------------------
# 사이드바 로그인 / 회원가입 시스템
# -----------------------------------------------------------------------------
st.sidebar.title("🔐 사용자 인증")

if not st.session_state["logged_in"]:
    auth_mode = st.sidebar.radio("메뉴 선택", ["로그인", "회원가입"])

    if auth_mode == "로그인":
        st.sidebar.subheader("로그인")
        input_id = st.sidebar.text_input("아이디(userid)", key="login_id")
        input_pw = st.sidebar.text_input(
            "비밀번호", type="password", key="login_pw"
        )

        if st.sidebar.button("로그인"):
            if input_id and input_pw:
                user = login_user(input_id, input_pw)
                if user:
                    st.session_state["logged_in"] = True
                    st.session_state["userid"] = input_id
                    st.sidebar.success(f"{input_id}님 환영합니다!")
                    st.rerun()
                else:
                    st.sidebar.error("아이디 또는 비밀번호가 올바르지 않습니다.")
            else:
                st.sidebar.warning("아이디와 비밀번호를 모두 입력해주세요.")

    else:
        st.sidebar.subheader("회원가입")
        new_id = st.sidebar.text_input("아이디(userid) 생성", key="reg_id")
        new_pw = st.sidebar.text_input(
            "비밀번호 생성", type="password", key="reg_pw"
        )
        new_pw_confirm = st.sidebar.text_input(
            "비밀번호 확인", type="password", key="reg_pw_confirm"
        )

        if st.sidebar.button("회원가입 신청"):
            if new_id and new_pw:
                if new_pw != new_pw_confirm:
                    st.sidebar.error("비밀번호 확인이 일치하지 않습니다.")
                else:
                    success, msg = register_user(new_id, new_pw)
                    if success:
                        st.sidebar.success(msg)
                    else:
                        st.sidebar.error(msg)
            else:
                st.sidebar.warning("모든 필드를 입력해 주세요.")
else:
    st.sidebar.success(f"🟢 **{st.session_state['userid']}** 님 로그인 중")
    if st.sidebar.button("로그아웃"):
        st.session_state["logged_in"] = False
        st.session_state["userid"] = None
        st.rerun()

st.sidebar.markdown("---")

# -----------------------------------------------------------------------------
# 메인 컨텐츠 영역 (기존 app.py)
# -----------------------------------------------------------------------------
st.title("This is my first webapp!!")
st.subheader("Mechanical Engineering AIDT")

col1, col2 = st.columns((4, 1))
with col1:
    with st.expander("1차시_ 동영상", expanded=True):
        st.title("동영상 시청......")
        url = "https://www.youtube.com/watch?v=06bQPPjnw1g"
        st.video(url)
with col2:
    with st.expander("Tips..."):
        st.subheader("Tips...")
        imgpath = "https://tago.kr/images/sub/engine_img02.jpg"
        st.image(imgpath)
        st.write("This is a term....")

coll1, coll2 = st.columns((4, 1))
with coll1:
    with st.expander("2차시_ 이미지"):
        st.title("엔진의 작동원리 이미지")
        # 이미지 경로 변경 (engine)
        imgpath1 = "./img/engine.jpeg"
        if os.path.exists(imgpath1):
            st.image(imgpath1)
        else:
            st.info(
                "이미지 파일 경로를 확인해 주세요. (./img/engine.jpeg)"
            )
with coll2:
    with st.expander("Tips..."):
        st.subheader("Tips...")
        imgpath = "https://tago.kr/images/sub/engine_img02.jpg"
        st.image(imgpath)
        st.write("This is a term....")

colll1, colll2 = st.columns((4, 1))

with colll1:
    with st.expander("3차시_이론설명"):
        st.title("엔진의 작동원리")

        st.markdown(
            """
### ⚙️ 4행정(4사이클) 엔진이란?

4행정 가솔린/디젤 엔진은 **피스톤이 실린더 내부를 4번 왕복(크랭크축 2회전)하는 동안 1회의 동력을 발생**시키는 기관입니다.

#### 4사이클 기본 행정
- 📌 **흡입(Intake)** : 흡입 밸브가 열리고 피스톤이 하강하면서 혼합기(공기+연료)를 실린더 내부로 흡입합니다.
- 📌 **압축(Compression)** : 모든 밸브가 닫힌 상태에서 피스톤이 상승하며 혼합기를 고온·고압으로 압축합니다.
- 📌 **폭발/팽창(Combustion/Power)** : 점화플러그에서 불꽃을 튀겨 연소 반응을 일으키며, 폭발 가스의 힘으로 피스톤이 하강하여 동력을 발생시킵니다.
- 📌 **배기(Exhaust)** : 배기 밸브가 열리고 피스톤이 상승하면서 연소된 가스를 실린더 외부로 배출합니다.

#### 주요 동작 특징
1. 크랭크축이 2회전(720°)하는 동안 폭발 행정은 1회 발생합니다.
2. 각 행정마다 흡입·배기 밸브의 개폐 타이밍이 정밀하게 일치해야 합니다.
3. 폭발 행정에서 얻은 관성력(플라이휠)으로 나머지 3개 행정을 유연하게 수행합니다.
        """
        )

        # 이미지 경로 (engine)
        imgpath1 = "./img/engine.jpeg"
        if os.path.exists(imgpath1):
            st.image(imgpath1)

with colll2:
    with st.expander("Tips..."):
        st.subheader("Tips...")

        imgpath = "https://tago.kr/images/sub/engine_img02.jpg"
        st.image(imgpath)

        st.write("### 🔩 엔진 핵심 구성요소")

        st.markdown(
            """
- **피스톤(Piston)** : 연소 가스의 압력을 받아 왕복 운동
- **실린더(Cylinder)** : 피스톤이 왕복하는 밀폐 공간
- **크랭크축(Crankshaft)** : 피스톤의 직선 운동을 회전 운동으로 변환
- **점화플러그(Spark Plug)** : 압축된 혼합기에 불꽃을 일으킴
- **흡/배기 밸브(Valve)** : 혼합기 유입 및 연소가스 배출 제어
- **연소실(Combustion Chamber)** : 폭발 연소가 일어나는 공간
- **커넥팅 로드(Connecting Rod)** : 피스톤과 크랭크축을 연결
- **상사점(TDC) / 하사점(BDC)** : 피스톤 움직임의 최상단 / 최하단 위치
        """
        )