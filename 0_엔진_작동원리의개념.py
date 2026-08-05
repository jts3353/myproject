# streamlit Webapp의 pages 경로 밑에 서브 페이지로 다음을 생성해주세요.
# 엔진_작동원리의 개념에 대해 학습할 콘텐츠 생성
# 간단하게 엔진_작동원리의 개념을 실습할 수 있는 시뮬레이터 포함(mock data 생성해서(분류 데이터) 직접 실습하도록 함)
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# 페이지 기본 설정
st.set_page_config(
    page_title="엔진 작동원리 및 상태 진단 실습", page_icon="⚙️", layout="wide"
)

st.title("⚙️ 4사이클 엔진 작동원리 & 상태 진단 시뮬레이터")
st.caption("기계공학 AIDT 학습 콘텐츠 | 0차시: 엔진 작동원리와 데이터 기반 상태 진단")

# Tab 구성: 이론 학습 및 시뮬레이터 실습
tab1, tab2 = st.tabs(["📖 1. 엔진 작동원리 학습", "🧪 2. 엔진 진단 시뮬레이터 (ML 실습)"])

# =============================================================================
# TAB 1: 이론 학습 콘텐츠
# =============================================================================
with tab1:
    st.header("💡 4행정(4사이클) 엔진의 핵심 개념")
    st.write(
        "가솔린 및 디젤 엔진은 피스톤이 실린더 내부를 4번 왕복(크랭크축 2회전)하는 동안 1회의 동력을 발생시킵니다."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.subheader("1. 흡입 (Intake)")
        st.info("""
        - **흡입 밸브**: 열림 / **배기 밸브**: 닫힘
        - **피스톤**: 상사점(TDC) ➔ 하사점(BDC) 이동
        - **특징**: 실린더 내부 압력이 낮아지며 공기+연료 혼합기가 유입됩니다.
        """)

    with col2:
        st.subheader("2. 압축 (Compression)")
        st.warning("""
        - **흡입 밸브**: 닫힘 / **배기 밸브**: 닫힘
        - **피스톤**: 하사점(BDC) ➔ 상사점(TDC) 이동
        - **특징**: 혼합기를 고온·고압 상태로 압축하여 폭발 효율을 높입니다.
        """)

    with col3:
        st.subheader("3. 폭발 (Combustion)")
        st.error("""
        - **흡입 밸브**: 닫힘 / **배기 밸브**: 닫힘
        - **피스톤**: 상사점(TDC) ➔ 하사점(BDC) 이동
        - **특징**: 점화플러그의 불꽃으로 급격한 연소가 일어나며 강력한 동력을 얻습니다.
        """)

    with col4:
        st.subheader("4. 배기 (Exhaust)")
        st.success("""
        - **흡입 밸브**: 닫힘 / **배기 밸브**: 열림
        - **피스톤**: 하사점(BDC) ➔ 상사점(TDC) 이동
        - **특징**: 연소 후 남은 배기가스를 실린더 외부로 배출합니다.
        """)

    st.markdown("---")

    st.subheader("🔍 주요 엔진 파라미터와 진단 지표")
    st.markdown("""
    엔진이 정상적으로 작동하는지 판단하기 위해 센서를 통해 다음과 같은 데이터를 수집합니다:
    * **RPM (회전수)**: 엔진 크랭크축의 분당 회전수
    * **압축 압력 (Compression Pressure, bar)**: 압축 행정 시 연소실 내부 최고 압력
    * **연소실 최고 온도 (Peak Temp, °C)**: 폭발 행정 시 연소실 내부 온도
    * **배기 다니폴드 압력 (Exhaust Pressure, bar)**: 배기 행정 시 배기관 내부 압력
    """)

# =============================================================================
# TAB 2: 엔진 진단 시뮬레이터 (Mock Data 기반 분류 실습)
# =============================================================================
with tab2:
    st.header("🧪 엔진 상태 분류 진단 실습 (Machine Learning)")
    st.write(
        "센서 데이터를 활용해 엔진의 상태(**정상, 압축불량, 점화불량, 배기막힘**)를 머신러닝 알고리즘으로 진단해보는 실습입니다."
    )

    # 1. 데이터 생성 매개변수 설정 (사이드바 또는 메인창)
    st.subheader("1️⃣ 모의 센서 데이터(Mock Data) 생성 설정")
    num_samples = st.slider(
        "생성할 센서 데이터 개수 (샘플 수)",
        min_value=100,
        max_value=1000,
        value=400,
        step=100,
    )

    # Mock Data 생성 함수
    @st.cache_data
    def generate_engine_mock_data(n):
        np.random.seed(42)
        samples_per_class = n // 4

        # 1) 정상 (Normal)
        rpm_n = np.random.normal(2500, 200, samples_per_class)
        press_n = np.random.normal(12.5, 0.8, samples_per_class)
        temp_n = np.random.normal(650, 30, samples_per_class)
        exh_n = np.random.normal(1.2, 0.1, samples_per_class)
        label_n = ["정상"] * samples_per_class

        # 2) 압축 불량 (Low Compression)
        rpm_c = np.random.normal(2200, 250, samples_per_class)
        press_c = np.random.normal(7.5, 1.0, samples_per_class)  # 압력 낮음
        temp_c = np.random.normal(500, 40, samples_per_class)
        exh_c = np.random.normal(1.1, 0.1, samples_per_class)
        label_c = ["압축불량"] * samples_per_class

        # 3) 점화 불량 (Misfire)
        rpm_i = np.random.normal(2000, 300, samples_per_class)
        press_i = np.random.normal(11.8, 0.9, samples_per_class)
        temp_i = np.random.normal(300, 50, samples_per_class)  # 폭발 안되어 온도 낮음
        exh_i = np.random.normal(1.0, 0.1, samples_per_class)
        label_i = ["점화불량"] * samples_per_class

        # 4) 배기 막힘 (Exhaust Blocked)
        rpm_e = np.random.normal(2100, 200, samples_per_class)
        press_e = np.random.normal(11.5, 0.8, samples_per_class)
        temp_e = np.random.normal(720, 35, samples_per_class)
        exh_e = np.random.normal(3.5, 0.4, samples_per_class)  # 배기압 매우 높음
        label_e = ["배기막힘"] * samples_per_class

        df = pd.DataFrame(
            {
                "RPM": np.concatenate([rpm_n, rpm_c, rpm_i, rpm_e]),
                "압축압력(bar)": np.concatenate(
                    [press_n, press_c, press_i, press_e]
                ),
                "연소실온도(°C)": np.concatenate(
                    [temp_n, temp_c, temp_i, temp_e]
                ),
                "배기압력(bar)": np.concatenate(
                    [exh_n, exh_c, exh_i, exh_e]
                ),
                "엔진상태": np.concatenate(
                    [label_n, label_c, label_i, label_e]
                ),
            }
        )
        return df

    df_engine = generate_engine_mock_data(num_samples)

    # 데이터 확인
    col_data, col_viz = st.columns([1, 1])
    with col_data:
        st.write("📊 생성된 엔진 센서 데이터셋 (상위 10개)")
        st.dataframe(df_engine.head(10), use_container_width=True)

    with col_viz:
        st.write("📈 데이터 분포 시각화 (압축압력 vs 연소실온도)")
        fig = px.scatter(
            df_engine,
            x="압축압력(bar)",
            y="연소실온도(°C)",
            color="엔진상태",
            symbol="엔진상태",
            hover_data=["RPM", "배기압력(bar)"],
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # 2. 머신러닝 학습 및 테스트
    st.subheader("2️⃣ 엔진의_작동원리 학습 및 평가")

    X = df_engine[
        ["RPM", "압축압력(bar)", "연소실온도(°C)", "배기압력(bar)"]
    ]
    y = df_engine["엔진상태"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    st.success(f"✅ 모델 학습 완료! **테스트 정확도(Accuracy): {acc * 100:.1f}%**")

    st.markdown("---")

    # 3. 사용자 직접 가상 데이터 입력 및 실시간 상태 진단
    st.subheader("3️⃣ 실시간 엔진 상태 예측 실습")
    st.write(
        "아래 슬라이더로 엔진 센서 수치를 직접 조절하여 상태를 진단해보세요."
    )

    sim_col1, sim_col2, sim_col3, sim_col4 = st.columns(4)

    with sim_col1:
        test_rpm = st.slider("RPM", 1000, 4000, 2500)
    with sim_col2:
        test_press = st.slider("압축압력 (bar)", 4.0, 16.0, 12.5, step=0.1)
    with sim_col3:
        test_temp = st.slider("연소실온도 (°C)", 200, 900, 650)
    with sim_col4:
        test_exh = st.slider("배기압력 (bar)", 0.5, 5.0, 1.2, step=0.1)

    input_data = pd.DataFrame(
        [
            {
                "RPM": test_rpm,
                "압축압력(bar)": test_press,
                "연소실온도(°C)": test_temp,
                "배기압력(bar)": test_exh,
            }
        ]
    )

    predicted_status = model.predict(input_data)[0]
    proba = model.predict_proba(input_data)[0]
    classes = model.classes_

    st.markdown("### 🤖 엔진의_작동원리 진단 결과")
    if predicted_status == "정상":
        st.success(f"🟢 진단 결과: **[{predicted_status}]** 상태입니다.")
    elif predicted_status == "압축불량":
        st.warning(
            f"🟡 진단 결과: **[{predicted_status}]** 상태입니다. (실린더/피스톤 링 점검 필요)"
        )
    elif predicted_status == "점화불량":
        st.error(
            f"🔴 진단 결과: **[{predicted_status}]** 상태입니다. (점화플러그/코일 점검 필요)"
        )
    else:
        st.info(
            f"🟠 진단 결과: **[{predicted_status}]** 상태입니다. (배기 매니폴드/촉매 점검 필요)"
        )

    # 확률 분포 시각화
    df_proba = pd.DataFrame({"상태": classes, "확률": proba})
    fig_proba = px.bar(
        df_proba,
        x="상태",
        y="확률",
        text_auto=".1%",
        color="상태",
        title="상태별 예측 확률",
    )
    st.plotly_chart(fig_proba, use_container_width=True)