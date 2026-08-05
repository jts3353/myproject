import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="엔진 작동원리 - 영상으로 배우기", page_icon="🎬", layout="wide"
)

# 로그인 검증
if (
    "logged_in" not in st.session_state
    or not st.session_state["logged_in"]
):
    st.warning(
        "⚠️ 이 페이지를 이용하려면 로그인이 필요합니다. 메인 페이지 사이드바에서 먼저 로그인해 주세요."
    )
    st.stop()

# 헤더 영역
st.title("🎬 2차시: 엔진 작동원리 영상 학습")
st.caption("동영상을 시청한 후 아래의 간단한 확인 퀴즈 2문제를 풀어보세요.")
st.info(f"👤 현재 학습자: **{st.session_state['userid']}** 님")

st.markdown("---")

# -----------------------------------------------------------------------------
# 1. 동영상 시청 영역
# -----------------------------------------------------------------------------
st.subheader("📺 1. 엔진 작동원리 동영상 시청")

col1, col2 = st.columns([3, 1])

with col1:
    # 엔진 작동원리 유튜브 영상 (URL)
    video_url = "https://www.youtube.com/watch?v=06bQPPjnw1g"
    st.video(video_url)

with col2:
    st.markdown("### 💡 시청 포인트")
    st.markdown(
        """
    - **4행정 순서**: 흡입 ➔ 압축 ➔ 폭발 ➔ 배기
    - **피스톤의 운동**: 직선 왕복 운동
    - **크랭크축의 역할**: 회전 운동으로의 변환
    - **점화 방식**: 가솔린(불꽃점화) vs 디젤(압축착화)
    """
    )

st.markdown("---")

# -----------------------------------------------------------------------------
# 2. 개념 확인 퀴즈 (2문제)
# -----------------------------------------------------------------------------
st.subheader("✏️ 2. 개념 확인 퀴즈 (2문제)")
st.write("영상을 잘 시청했는지 확인하는 간단한 퀴즈입니다.")

with st.form("quick_quiz_form"):
    # Q1
    st.markdown("#### **Q1. 4행정 기관의 4가지 단계(행정) 순서로 올바른 것은?**")
    q1_choice = st.radio(
        "Q1 답안 선택:",
        options=[
            "① 흡입 ➔ 폭발 ➔ 압축 ➔ 배기",
            "② 흡입 ➔ 압축 ➔ 폭발 ➔ 배기",
            "③ 압축 ➔ 흡입 ➔ 폭발 ➔ 배기",
            "④ 폭발 ➔ 흡입 ➔ 압축 ➔ 배기",
        ],
        index=None,
        key="qq1",
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Q2
    st.markdown(
        "#### **Q2. 피스톤의 '직선 왕복 운동'을 자동차 바퀴를 돌릴 수 있는 '회전 운동'으로 바꾸어 주는 부품은?**"
    )
    q2_choice = st.radio(
        "Q2 답안 선택:",
        options=[
            "① 점화플러그",
            "② 흡기 밸브",
            "③ 크랭크축",
            "④ 실린더 헤드",
        ],
        index=None,
        key="qq2",
    )

    st.markdown("<br>", unsafe_allow_html=True)
    quiz_submit = st.form_submit_button("Submit 퀴즈 제출하기")

# 퀴즈 제출 결과 처리
if quiz_submit:
    if not q1_choice or not q2_choice:
        st.warning("⚠️ 두 문제의 답을 모두 선택한 후 제출해 주세요.")
    else:
        score = 0

        # Q1 정답 체크 (정답: ②)
        q1_correct = "②" in q1_choice
        if q1_correct:
            score += 50

        # Q2 정답 체크 (정답: ③)
        q2_correct = "③" in q2_choice
        if q2_correct:
            score += 50

        st.markdown("---")
        st.subheader("📊 퀴즈 결과")

        # Q1 결과 표시
        if q1_correct:
            st.success("✅ **Q1 정답입니다!** (4행정 순서: 흡입 ➔ 압축 ➔ 폭발 ➔ 배기)")
        else:
            st.error(
                "❌ **Q1 오답입니다.** (정답: ② 흡입 ➔ 압축 ➔ 폭발 ➔ 배기)"
            )

        # Q2 결과 표시
        if q2_correct:
            st.success(
                "✅ **Q2 정답입니다!** (크랭크축이 왕복 운동을 회전 운동으로 변환합니다.)"
            )
        else:
            st.error("❌ **Q2 오답입니다.** (정답: ③ 크랭크축)")

        if score == 100:
            st.balloons()
            st.success("🎉 완벽합니다! 100점입니다. 다음 차시나 형성평가로 이동해 보세요.")
        else:
            st.info(f"💡 점수: **{score}점** / 100점 (영상을 다시 한번 복습해 보세요!)")