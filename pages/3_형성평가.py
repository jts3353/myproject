import pandas as pd
import streamlit as st
from db_helper import get_user_history, save_quiz_result

st.set_page_config(
    page_title="엔진의 작동원리 형성평가", page_icon="📝", layout="wide"
)

st.title("📝 엔진의 작동원리 형성평가")
st.caption(
    "학습한 엔진 작동원리 개념을 점검하는 형성평가입니다. (총 10문항, 문항당 10점 / 만점 100점)"
)

# 로그인 검증
if (
    "logged_in" not in st.session_state
    or not st.session_state["logged_in"]
):
    st.warning("⚠️ 형성평가에 응시하려면 로그인이 필요합니다. 메인 페이지 사이드바에서 로그인해 주세요.")
    st.stop()

userid = st.session_state["userid"]
st.info(f"👤 현재 응시자: **{userid}** 님")

# 엔진 작동원리 10문항 데이터 정의 (5지선다형, 힌트, 정답, 해설)
questions = [
    {
        "id": 1,
        "question": "1. 4행정(4사이클) 엔진에서 1회의 동력(폭발)을 얻기 위한 피스톤의 왕복 횟수와 크랭크축의 회전수로 올바른 것은?",
        "options": [
            "① 피스톤 2회 왕복, 크랭크축 1회전",
            "② 피스톤 4회 왕복, 크랭크축 2회전",
            "③ 피스톤 4회 왕복, 크랭크축 4회전",
            "④ 피스톤 2회 왕복, 크랭크축 4회전",
            "⑤ 피스톤 1회 왕복, 크랭크축 2회전",
        ],
        "answer": 2,
        "hint": "피스톤이 흡입-압축-폭발-배기의 4가지 행정을 수행하는 동안 회전축은 몇 바퀴를 돌까요?",
        "explanation": "4행정 엔진은 피스톤이 실린더 내부를 4번 왕복(4행정)하는 동안 크랭크축이 2회전(720°)하며 1회의 폭발 행정을 완료합니다.",
    },
    {
        "id": 2,
        "question": "2. 피스톤의 직선 왕복 운동을 회전 운동으로 변환해 주는 엔진의 핵심 부품은 무엇인가요?",
        "options": [
            "① 점화플러그(Spark Plug)",
            "② 실린더 헤드(Cylinder Head)",
            "③ 크랭크축(Crankshaft)",
            "④ 흡기 밸브(Intake Valve)",
            "⑤ 피스톤 링(Piston Ring)",
        ],
        "answer": 3,
        "hint": "자전거 페달의 기랭크 구조처럼 왕복 운동을 바퀴를 돌리는 회전력으로 바꿉니다.",
        "explanation": "크랭크축(Crankshaft)은 커넥팅 로드를 통해 전파된 피스톤의 직선 왕복 운동을 회전 운동으로 변환합니다.",
    },
    {
        "id": 3,
        "question": "3. 4행정 엔진의 '흡입 행정'에 대한 설명으로 옳은 것은?",
        "options": [
            "① 흡입 밸브가 닫히고 피스톤이 상승한다.",
            "② 모든 밸브가 열리고 피스톤이 하강한다.",
            "③ 흡입 밸브가 열리고 피스톤이 하강하면서 혼합기를 흡입한다.",
            "④ 배기 밸브가 열리고 피스톤이 상승한다.",
            "⑤ 점화플러그에서 불꽃이 튀어 혼합기를 연소시킨다.",
        ],
        "answer": 3,
        "hint": "주사기 바늘 쪽 입구를 열고 피스톤을 뒤로 끌어당길 때 기체가 들어오는 원리입니다.",
        "explanation": "흡입 행정에서는 흡입 밸브가 열리고 피스톤이 하강(TDC→BDC)하면서 발생한 負壓(음압)으로 혼합기(공기+연료)를 빨아들입니다.",
    },
    {
        "id": 4,
        "question": "4. 압축 행정 시 실린더 내부의 밸브 상태와 피스톤의 이동 방향으로 올바른 것은?",
        "options": [
            "① 흡입/배기 밸브 모두 열림 / 피스톤 하강",
            "② 흡입/배기 밸브 모두 닫힘 / 피스톤 상승",
            "③ 흡입 밸브만 열림 / 피스톤 상승",
            "④ 배기 밸브만 열림 / 피스톤 하강",
            "⑤ 흡입/배기 밸브 모두 닫힘 / 피스톤 하강",
        ],
        "answer": 2,
        "hint": "기체를 밀폐된 공간에서 고온·고압으로 모으려면 밸브가 어떻게 되어야 할까요?",
        "explanation": "압축 행정에서는 실린더 내부를 밀폐하기 위해 모든 밸브가 닫힌 상태에서 피스톤이 상승(BDC→TDC)합니다.",
    },
    {
        "id": 5,
        "question": "5. 피스톤이 실린더 내부에서 움직일 수 있는 최상단 위치를 뜻하는 용어는?",
        "options": [
            "① BDC (Bottom Dead Center)",
            "② TDC (Top Dead Center)",
            "③ RPM (Revolutions Per Minute)",
            "④ BMEP (Brake Mean Effective Pressure)",
            "⑤ 행정 임계점(Stroke Threshold)",
        ],
        "answer": 2,
        "hint": "'Top(상단)' 위치에 해당하는 사점(Dead Center)의 약자입니다.",
        "explanation": "피스톤이 실린더 내에서 가장 위로 올라갈 수 있는 위치를 상사점(TDC: Top Dead Center)이라고 합니다.",
    },
    {
        "id": 6,
        "question": "6. 가솔린 엔진에서 압축된 혼합기에 불꽃을 일으켜 폭발을 유도하는 장치는?",
        "options": [
            "① 인젝터(Injector)",
            "② 점화플러그(Spark Plug)",
            "③ 피스톤 핀(Piston Pin)",
            "④ 서모스탯(Thermostat)",
            "⑤ 가스켓(Gasket)",
        ],
        "answer": 2,
        "hint": "전기적 불꽃(Spark)을 발생시켜 가솔린 혼합기를 연소시킵니다.",
        "explanation": "가솔린 엔진은 압축 행정 말기에 점화플러그(Spark Plug)에서 전기 불꽃을 튀겨 연소를 개시합니다.",
    },
    {
        "id": 7,
        "question": "7. 폭발(팽창) 행정 동안 엔진 내부에서 일어나는 현상으로 가장 적절한 것은?",
        "options": [
            "① 연소 가스의 폭발력으로 피스톤이 강하게 하강하여 동력을 발생시킨다.",
            "② 배기 밸브가 열려 연소 가스가 외부로 방출된다.",
            "③ 피스톤이 상승하며 공기를 외부로 밀어낸다.",
            "④ 흡입 밸브가 열려 연료가 대량 유입된다.",
            "⑤ 크랭크축의 회전이 멈추고 에너지 소모만 일어난다.",
        ],
        "answer": 1,
        "hint": "4개 행정 중 유일하게 외부로 유용한 일(Work)을 만드는 행정입니다.",
        "explanation": "폭발 행정에서는 혼합기가 연소하며 발생하는 고온·고압 가스의 팽창력으로 피스톤을 하강시켜 동력을 얻습니다.",
    },
    {
        "id": 8,
        "question": "8. 배기 행정 시 피스톤과 밸브의 동작으로 올바른 것은?",
        "options": [
            "① 흡입 밸브 열림, 피스톤 하강",
            "② 배기 밸브 열림, 피스톤 상승",
            "③ 모든 밸브 닫힘, 피스톤 하강",
            "④ 모든 밸브 열림, 피스톤 정지",
            "⑤ 배기 밸브 닫힘, 피스톤 상승",
        ],
        "answer": 2,
        "hint": "타버린 연소 가스를 밖으로 밀어내려면 피스톤이 어느 방향으로 움직여야 할까요?",
        "explanation": "배기 행정에서는 배기 밸브가 열리고 피스톤이 상승(BDC→TDC)하면서 실린더 내의 연소가스를 배출합니다.",
    },
    {
        "id": 9,
        "question": "9. 폭발 행정에서 얻은 동력을 저장해 두었다가, 나머지 3개 관성 행정(흡입, 압축, 배기)을 유연하게 이어주는 부품은?",
        "options": [
            "① 플라이휠(Flywheel)",
            "② 피스톤 링(Piston Ring)",
            "③ 캠축(Camshaft)",
            "④ 커넥팅 로드(Connecting Rod)",
            "⑤ 오일 펌프(Oil Pump)",
        ],
        "answer": 1,
        "hint": "무거운 회전체로서 관성 모멘트를 이용해 엔진의 회전을 원활하게 유지합니다.",
        "explanation": "플라이휠(Flywheel)은 폭발 행정 시 에너지를 저장했다가 관성력으로 흡입, 압축, 배기 행정을 무리 없이 지속하도록 돕습니다.",
    },
    {
        "id": 10,
        "question": "10. 가솔린 엔진과 디젤 엔진의 동작 방식 상 가장 큰 차이점은 무엇인가요?",
        "options": [
            "① 디젤 엔진은 크랭크축이 존재하지 않는다.",
            "② 가솔린 엔진은 점화플러그를 사용하고, 디젤 엔진은 자기점화(압축착화) 방식을 사용한다.",
            "③ 가솔린 엔진은 4행정만 사용하고, 디젤 엔진은 2행정만 사용한다.",
            "④ 디젤 엔진은 배기 행정이 존재하지 않는다.",
            "⑤ 가솔린 엔진은 공기만 흡입할 수 없다.",
        ],
        "answer": 2,
        "hint": "디젤 엔진에는 불꽃을 튀겨주는 '점화플러그'가 별도로 없습니다.",
        "explanation": "가솔린 엔진은 점화플러그의 불꽃으로 점화하지만, 디젤 엔진은 공기를 고비율로 압축하여 생긴 고온의 열로 연료를 자발화(압축착화)시킵니다.",
    },
]

# -----------------------------------------------------------------------------
# 탭 구성: 형성평가 응시 & 나의 이력
# -----------------------------------------------------------------------------
tab_quiz, tab_history = st.tabs(["✍️ 형성평가 응시", "📜 나의 응시 이력 (DB)"])

with tab_quiz:
    with st.form("quiz_form"):
        user_answers = []

        for q in questions:
            st.markdown(f"#### {q['question']}")

            # 힌트 보기 (Expander)
            with st.expander("💡 힌트 보기"):
                st.info(q["hint"])

            # 5지선다 라디오 버튼
            choice = st.radio(
                "답안을 선택하세요:",
                options=q["options"],
                index=None,
                key=f"q_{q['id']}",
            )

            if choice:
                # 선택 항목 문항 번호 추출 ('①' -> 1)
                num = int(
                    choice[0]
                    .replace("①", "1")
                    .replace("②", "2")
                    .replace("③", "3")
                    .replace("④", "4")
                    .replace("⑤", "5")
                )
                user_answers.append(num)
            else:
                user_answers.append(0)

            st.markdown("---")

        submit_btn = st.form_submit_button("🏁 형성평가 제출하기")

    # 제출 버튼 처리
    if submit_btn:
        if 0 in user_answers:
            st.warning("⚠️ 미응시 문항이 있습니다. 10개 문항을 모두 선택한 후 제출해 주세요.")
        else:
            correct_count = 0
            st.subheader("📊 채점 결과 및 해설")

            for i, q in enumerate(questions):
                user_ans = user_answers[i]
                is_correct = user_ans == q["answer"]

                if is_correct:
                    correct_count += 1
                    st.success(
                        f"**{q['id']}번 문제: 정답입니다!** (내가 입력한 답: {user_ans}번)"
                    )
                else:
                    st.error(
                        f"**{q['id']}번 문제: 오답입니다.** (내가 입력한 답: {user_ans}번)"
                    )

                # 정답 및 해설 (원할 때 확인 가능하도록 Expander 처리)
                with st.expander(f"🔍 {q['id']}번 문제 정답 및 해설 확인"):
                    st.write(f"**정답:** {q['answer']}번")
                    st.write(f"**해설:** {q['explanation']}")

            # 점수 계산 (각 문항 10점)
            total_score = correct_count * 10
            st.markdown("---")
            st.metric(label="🏆 최종 점수", value=f"{total_score} / 100 점")

            # DB 저장 (learning_history 테이블)
            save_quiz_result(userid, user_answers, total_score)
            st.balloons()
            st.success(
                f"✅ 응시 결과가 `myproject.db` 데이터베이스의 `learning_history` 테이블에 기록되었습니다."
            )

with tab_history:
    st.subheader(f"📜 [{userid}] 님의 형성평가 응시 기록")
    rows = get_user_history(userid)

    if rows:
        cols = [
            "응시 ID",
            "m1",
            "m2",
            "m3",
            "m4",
            "m5",
            "m6",
            "m7",
            "m8",
            "m9",
            "m10",
            "최종 점수",
            "응시 일시",
        ]
        df_history = pd.DataFrame(rows, columns=cols)
        st.dataframe(df_history, use_container_width=True)
    else:
        st.info("제출된 형성평가 응시 기록이 없습니다. '형성평가 응시' 탭에서 문제를 풀어보세요!")