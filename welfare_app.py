import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import platform
import matplotlib.font_manager as fm

# ────────────────────────────────────────────
# 페이지 설정
# ────────────────────────────────────────────
st.set_page_config(
    page_title="스마트 복지안전망 v2.0",
    page_icon="🏠",
    layout="centered"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=Noto+Sans+KR:wght@400;500;700;900&display=swap');

    :root {
        --paper:     #FBF4E8;
        --paper-2:   #F4EBDB;
        --ink:       #3A2E26;
        --pine:      #3E5C50;
        --pine-2:    #2E4A3F;
        --sun:       #E8A04C;
        --sun-soft:  #F6D9A8;
        --clay:      #D9764A;
        --clay-soft: #F7E2D7;
        --sage:      #6E8F75;
        --sage-soft: #E4EEE3;
    }

    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
        color: var(--ink);
    }

    .stApp {
        background: var(--paper);
        background-image:
            radial-gradient(circle at 8% 12%, rgba(232,160,76,0.10) 0, transparent 38%),
            radial-gradient(circle at 92% 85%, rgba(110,143,117,0.12) 0, transparent 42%);
    }

    h1, h2, h3 { font-family: 'Gowun Batang', serif; }

    @keyframes heroIn {
        from { opacity: 0; transform: translateY(14px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .hero {
        background: linear-gradient(135deg, var(--pine) 0%, var(--pine-2) 100%);
        border-radius: 22px;
        padding: 2.4rem 2rem 2rem;
        color: var(--paper);
        text-align: center;
        margin-bottom: 1.6rem;
        position: relative;
        overflow: hidden;
        animation: heroIn 0.6s ease-out;
        box-shadow: 0 10px 28px -12px rgba(46,74,63,0.55);
    }
    .hero::before {
        content: "";
        position: absolute;
        right: -40px; top: -60px;
        width: 180px; height: 180px;
        background: radial-gradient(circle, rgba(232,160,76,0.35), transparent 70%);
        border-radius: 50%;
    }
    .hero::after {
        content: "";
        position: absolute;
        left: -50px; bottom: -70px;
        width: 200px; height: 200px;
        background: radial-gradient(circle, rgba(110,143,117,0.45), transparent 70%);
        border-radius: 50%;
    }
    .hero .eyebrow {
        font-size: 0.78rem; letter-spacing: 0.22em; font-weight: 700;
        color: var(--sun-soft); text-transform: uppercase; margin-bottom: 0.5rem;
        position: relative; z-index: 1;
    }
    .hero h1 {
        font-size: 1.9rem; margin: 0; font-weight: 700; position: relative; z-index: 1;
    }
    .hero p {
        font-size: 0.95rem; margin: 0.6rem auto 0; opacity: 0.9; max-width: 480px;
        position: relative; z-index: 1; line-height: 1.6;
    }

    .section-title {
        font-family: 'Gowun Batang', serif;
        font-size: 1.18rem;
        font-weight: 700;
        color: var(--pine-2);
        display: flex; align-items: center; gap: 0.5rem;
        margin: 1.8rem 0 0.9rem;
    }
    .section-title::before {
        content: "";
        display: inline-block;
        width: 8px; height: 8px;
        border-radius: 50%;
        background: var(--sun);
    }
    .section-sub {
        font-size: 0.85rem; color: #7A6E62; margin: -0.5rem 0 1rem;
    }

    @keyframes cardIn {
        from { opacity: 0; transform: translateY(10px) scale(0.98); }
        to   { opacity: 1; transform: translateY(0) scale(1); }
    }

    .result-card {
        border-radius: 18px;
        padding: 1.4rem 1.6rem;
        text-align: center;
        animation: cardIn 0.5s ease-out both;
        border: 1px solid transparent;
    }
    .result-danger {
        background: linear-gradient(135deg, var(--clay-soft) 0%, #FDF1EA 100%);
        border-color: #EFC2AC;
    }
    .result-safe {
        background: linear-gradient(135deg, var(--sage-soft) 0%, #F1F7EF 100%);
        border-color: #C9DEC7;
    }
    .result-title { font-size: 1.25rem; font-weight: 900; margin-bottom: 0.2rem; font-family: 'Gowun Batang', serif; }
    .result-caption { font-size: 0.88rem; margin-top: 0.4rem; opacity: 0.85; }

    .policy-card {
        background: #FFFEFB;
        border: 1px solid #ECE0CC;
        border-left: 5px solid var(--sage);
        border-radius: 14px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 0.9rem;
        transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
        animation: cardIn 0.45s ease-out both;
    }
    .policy-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 22px -14px rgba(58,46,38,0.35);
        border-left-color: var(--sun);
    }
    .policy-card.top { border-left-color: var(--clay); }
    .policy-name  { font-weight: 700; color: var(--pine-2); font-size: 1.02rem; font-family: 'Gowun Batang', serif; }
    .policy-desc  { color: #5C5048; font-size: 0.88rem; margin: 0.35rem 0; line-height: 1.55; }
    .policy-badge {
        display: inline-block;
        background: var(--sage-soft);
        color: var(--pine-2);
        font-size: 0.72rem;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 20px;
        margin-right: 5px;
        margin-bottom: 4px;
    }
    .match-badge {
        display: inline-block;
        background: var(--clay);
        color: #fff;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 20px;
        margin-bottom: 4px;
        margin-right: 5px;
    }
    .match-bar-bg {
        background: #EFE6D6; border-radius: 6px; height: 7px; overflow: hidden; margin-top: 0.55rem;
    }
    .match-bar-fill {
        height: 100%; border-radius: 6px;
        background: linear-gradient(90deg, var(--sun), var(--clay));
        animation: growBar 0.9s ease-out both;
    }
    @keyframes growBar { from { width: 0; } }

    .crisis-card {
        border-radius: 14px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.8rem;
        animation: cardIn 0.45s ease-out both;
        transition: transform 0.18s ease;
        border: 1px solid;
    }
    .crisis-card:hover { transform: translateX(3px); }
    .crisis-high   { background: #FDF1EA; border-color: #EFC2AC; }
    .crisis-medium { background: #FCF6E6; border-color: #F2DBA6; }
    .crisis-low    { background: var(--sage-soft); border-color: #C9DEC7; }
    .crisis-label  { font-weight: 700; font-size: 0.92rem; margin-bottom: 0.3rem; color: var(--ink); }
    .crisis-desc   { font-size: 0.85rem; color: #6B5F54; line-height: 1.5; }

    div[data-testid="stForm"] {
        background: #FFFEFB;
        border: 1px solid #ECE0CC;
        border-radius: 18px;
        padding: 1.6rem 1.6rem 1.2rem;
    }

    .stButton > button, .stFormSubmitButton > button {
        border-radius: 12px !important;
        font-weight: 700 !important;
        transition: transform 0.12s ease, box-shadow 0.12s ease !important;
        border: none !important;
    }
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, var(--sun) 0%, var(--clay) 100%) !important;
        color: #fff !important;
        box-shadow: 0 6px 16px -8px rgba(217,118,74,0.6) !important;
    }
    .stButton > button:hover, .stFormSubmitButton > button:hover {
        transform: translateY(-2px) scale(1.015);
        box-shadow: 0 10px 22px -10px rgba(217,118,74,0.55) !important;
    }
    .stButton > button:active, .stFormSubmitButton > button:active {
        transform: translateY(0px) scale(0.99);
    }
    .stLinkButton > a {
        border-radius: 12px !important;
        transition: transform 0.12s ease !important;
        border-color: #ECE0CC !important;
    }
    .stLinkButton > a:hover { transform: translateY(-2px); }

    .stTabs [data-baseweb="tab"] { font-weight: 700; font-family: 'Gowun Batang', serif; font-size: 1rem; }
    .stTabs [aria-selected="true"] { color: var(--pine-2) !important; }

    .metric-row { display: flex; gap: 0.7rem; flex-wrap: wrap; margin: 1rem 0 0.4rem; }
    .metric-box {
        flex: 1; min-width: 110px;
        background: #FFFEFB; border: 1px solid #ECE0CC; border-radius: 14px;
        padding: 0.8rem 1rem; text-align: center;
        animation: cardIn 0.45s ease-out both;
    }
    .metric-box .v { font-size: 1.35rem; font-weight: 900; color: var(--pine-2); font-family: 'Gowun Batang', serif; }
    .metric-box .l { font-size: 0.76rem; color: #8A7D6E; margin-top: 2px; }

    hr { border-color: #ECE0CC !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="eyebrow">WELFARE SAFETY NET · AI ANALYSIS</div>
  <h1>🏡 스마트 복지안전망 v2.0</h1>
  <p>가구 정보를 입력하면 AI가 기초생활수급 가능성을 분석하고,
  우리 가구 상황에 꼭 맞는 복지 제도와 위기 신호를 안내해드려요.</p>
</div>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────
# 모델 로드
# ────────────────────────────────────────────
@st.cache_resource
def load_model():
    try:
        model = joblib.load("welfare_model_real.pkl")
        return model
    except Exception as e:
        st.error(f"모델 파일을 불러올 수 없습니다: {e}")
        return None

model = load_model()

# ────────────────────────────────────────────
# 파생변수 계산 함수
# ────────────────────────────────────────────
def build_input_df(가구원수, 가구형태, 주거점유형태, 주거면적, 부채규모, 총소득_연간):
    """
    모델 학습 피처(8개)에 맞게 파생변수를 계산해 DataFrame 반환.
    학습 데이터의 총소득은 연간 단위이므로 총소득_연간을 그대로 사용.
    주거면적은 직접 피처가 아니라 파생변수 계산에만 사용됨.
    피처 순서: 가구원수, 가구형태, 주거점유형태, 부채규모, 총소득,
               인당_주거면적, 소득_대비_부채비율, 면적당_소득
    """
    인당_주거면적 = 주거면적 / 가구원수
    소득_대비_부채비율 = 부채규모 / (총소득_연간 + 1)
    면적당_소득 = 총소득_연간 / (주거면적 + 1)

    return pd.DataFrame(
        [[가구원수, 가구형태, 주거점유형태, 부채규모, 총소득_연간,
          인당_주거면적, 소득_대비_부채비율, 면적당_소득]],
        columns=['가구원수', '가구형태', '주거점유형태', '부채규모', '총소득',
                 '인당_주거면적', '소득_대비_부채비율', '면적당_소득']
    )


WELFARE_POLICIES = [
    {
        "name": "생계급여",
        "tags": ["기초생활보장", "현금지원"],
        "household": ["전체"],
        "desc": "기준 중위소득 32% 이하 가구에 매월 생활비를 현금으로 지급합니다. 4인 가구 기준 최대 약 195만 원(2025년 기준)까지 받을 수 있어요.",
        "income_match": True,
        "link": "https://www.bokjiro.go.kr",
        "contact": "주민센터 방문 또는 복지로(bokjiro.go.kr)"
    },
    {
        "name": "의료급여",
        "tags": ["기초생활보장", "의료비"],
        "household": ["전체"],
        "desc": "기준 중위소득 40% 이하 가구 대상으로, 병원비와 약값의 대부분을 지원합니다. 근로 능력에 따라 1종·2종으로 나뉘어요.",
        "income_match": True,
        "link": "https://www.bokjiro.go.kr",
        "contact": "주민센터 방문 또는 복지로"
    },
    {
        "name": "주거급여",
        "tags": ["기초생활보장", "주거비"],
        "household": ["전체"],
        "desc": "기준 중위소득 48% 이하 가구가 대상입니다. 세입자는 매달 월세 일부를, 자가 거주자는 집 수선 비용을 지원받을 수 있어요.",
        "income_match": True,
        "housing_match": True,
        "link": "https://www.myhome.go.kr",
        "contact": "주거급여 콜센터 1600-0777"
    },
    {
        "name": "교육급여",
        "tags": ["기초생활보장", "교육비"],
        "household": ["다인가구", "한부모"],
        "desc": "기준 중위소득 50% 이하 가구의 초·중·고 학생에게 교육활동 지원비를 지급합니다. 고등학생 기준 연 최대 약 65만 원이에요.",
        "income_match": True,
        "link": "https://www.bokjiro.go.kr",
        "contact": "주민센터 방문 또는 복지로"
    },
    {
        "name": "긴급복지지원제도",
        "tags": ["위기지원", "긴급생계비"],
        "household": ["전체"],
        "desc": "갑작스러운 실직, 화재, 질병 등으로 생계가 막막해진 가구에 생계비·의료비·주거비를 빠르게 지원합니다. 기준 중위소득 75% 이하면 신청할 수 있어요.",
        "crisis_match": True,
        "income_match": True,
        "link": "https://www.bokjiro.go.kr",
        "contact": "보건복지상담센터 ☎ 129"
    },
    {
        "name": "에너지 바우처",
        "tags": ["에너지", "현물지원"],
        "household": ["1인가구", "다인가구"],
        "desc": "기초생활수급 가구 중 노인·영유아·장애인·임산부 등이 있는 가구에 전기·도시가스·난방 요금을 연간 최대 약 73만 원까지 지원합니다.",
        "income_match": True,
        "crisis_match": True,
        "link": "https://www.energyv.or.kr",
        "contact": "한국에너지재단 ☎ 1600-3190"
    },
    {
        "name": "차상위계층 지원",
        "tags": ["차상위", "의료·교육비"],
        "household": ["전체"],
        "desc": "기준 중위소득 50% 이하지만 기초생활수급 대상은 아닌 가구를 위한 제도입니다. 의료비·교육비·자활사업 등을 연계해드려요.",
        "income_match": True,
        "link": "https://www.bokjiro.go.kr",
        "contact": "주민센터 방문 또는 복지로"
    },
    {
        "name": "한부모가족 지원",
        "tags": ["한부모", "아동양육비"],
        "household": ["한부모"],
        "desc": "한부모·조손 가족에게 아동양육비(월 21만 원 이상)와 학용품비, 생활보조금을 지원합니다. 기준 중위소득 63% 이하 가구가 대상이에요.",
        "income_match": True,
        "link": "https://www.bokjiro.go.kr",
        "contact": "여성가족부 ☎ 1366 또는 주민센터"
    },
    {
        "name": "주거취약계층 주거지원사업",
        "tags": ["주거지원", "임대주택"],
        "household": ["1인가구", "전체"],
        "desc": "쪽방, 고시원, 비닐하우스 등에 머무는 가구에게 공공임대주택 입주와 이사비, 생활집기를 지원합니다.",
        "housing_match": True,
        "income_match": True,
        "link": "https://www.lh.or.kr",
        "contact": "LH 콜센터 ☎ 1600-1004"
    },
    {
        "name": "노인맞춤돌봄서비스",
        "tags": ["1인가구", "돌봄"],
        "household": ["1인가구"],
        "desc": "혼자 사는 어르신께 안전 확인, 가사·일상생활 지원, 정서 지원 등을 제공합니다. 만 65세 이상 1인 가구라면 꼭 확인해보세요.",
        "income_match": False,
        "link": "https://www.bokjiro.go.kr",
        "contact": "주민센터 방문 또는 복지로"
    },
    {
        "name": "복지멤버십(맞춤형 급여 안내)",
        "tags": ["통합안내", "자동알림"],
        "household": ["전체"],
        "desc": "복지로에 가입해두면 가구 상황이 바뀔 때마다 받을 수 있는 복지급여를 자동으로 알려줍니다. 별도 신청 없이 대상 여부를 미리 확인할 수 있어요.",
        "income_match": False,
        "link": "https://www.bokjiro.go.kr",
        "contact": "복지로(bokjiro.go.kr) 회원가입 후 신청"
    },
]


def detect_crisis_signals(월소득, 주거점유형태, 부채규모, 가구형태, 가구원수):
    signals = []
    if 월소득 == 0:
        signals.append({"level": "high", "icon": "🔴", "title": "소득이 없어요 — 단전·단수 위험",
            "desc": "소득이 없는 가구는 공과금을 못 내서 전기·수도가 끊길 위험이 큽니다. 보건복지상담센터(☎ 129)에 바로 연락해보세요."})
    elif 월소득 < 100:
        signals.append({"level": "high", "icon": "🔴", "title": "소득이 매우 낮아요 — 건강보험료 체납 위험",
            "desc": f"월 소득 {월소득:.0f}만 원은 건강보험료를 밀릴 위험이 있는 수준입니다. 129에 연락하면 체납 유예나 감면을 신청할 수 있어요."})
    elif 월소득 < 200:
        signals.append({"level": "medium", "icon": "🟡", "title": "소득이 다소 낮아요 — 생계급여 검토 필요",
            "desc": "기준 중위소득과 비교했을 때 생계급여 등 기초생활보장 대상에 해당될 가능성이 있습니다. 아래 추천 제도를 확인해보세요."})
    if 주거점유형태 in [4, 5]:
        signals.append({"level": "high", "icon": "🔴", "title": "주거가 불안정해요 — 퇴거 위험",
            "desc": "보증금 없이 월세나 무상으로 거주 중이라면 주거 안정성이 낮습니다. 주거급여나 주거취약계층 지원사업을 신청해보세요."})
    elif 주거점유형태 == 3:
        signals.append({"level": "medium", "icon": "🟡", "title": "월세 거주 — 주거급여 대상 확인 필요",
            "desc": "월세로 거주 중인 가구는 주거급여 대상일 수 있습니다. 소득 조건을 충족하면 매달 월세 일부를 지원받을 수 있어요."})
    if 부채규모 >= 5000:
        signals.append({"level": "high", "icon": "🔴", "title": "부채가 많아요 — 금융 위기 위험",
            "desc": "부채 규모가 큰 경우 신용 문제로 이어질 수 있습니다. 서민금융진흥원(☎ 1397)이나 법률구조공단(☎ 132)에 상담받아보세요."})
    elif 부채규모 >= 1000:
        signals.append({"level": "medium", "icon": "🟡", "title": "부채 수준 모니터링 필요",
            "desc": "소득 대비 부채가 부담될 수 있는 수준이에요. 복지로 모의계산기로 수급 가능 여부를 먼저 확인해보세요."})
    if 가구형태 == 3:
        signals.append({"level": "medium", "icon": "🟡", "title": "한부모 가구 — 추가 지원 가능",
            "desc": "한부모가족 지원사업 대상일 수 있어요. 아동양육비와 교육비 등 추가 지원을 받을 수 있습니다."})
    if 가구원수 == 1:
        signals.append({"level": "low", "icon": "🟢", "title": "1인 가구 — 고립 위험 모니터링 권장",
            "desc": "혼자 사는 가구는 위기 상황이 생겨도 늦게 발견될 수 있어요. 가까운 주민센터에 돌봄 서비스 연계를 문의해보세요."})
    if not signals:
        signals.append({"level": "low", "icon": "🟢", "title": "현재 특별한 위기 신호는 없어요",
            "desc": "지금 입력하신 정보로는 당장의 위기 신호가 보이지 않아요. 그래도 복지멤버십에 가입해두면 상황 변화 시 자동으로 안내받을 수 있습니다."})
    return signals


def household_tag(가구형태, 가구원수):
    if 가구원수 == 1 or 가구형태 == 5:
        return "1인가구"
    if 가구형태 == 3:
        return "한부모"
    return "다인가구"


def score_policy(p, hh_tag, 월소득, 주거점유형태, 부채규모, prob, signals_level_high):
    score = 0
    reasons = []
    if hh_tag in p["household"]:
        score += 40
        reasons.append(f"{hh_tag} 맞춤 제도")
    elif "전체" in p["household"]:
        score += 10
    if p.get("income_match") and (월소득 < 250 or prob >= 0.20):
        score += 30
        reasons.append("소득 기준 해당 가능성")
    if p.get("housing_match") and 주거점유형태 in [3, 4, 5]:
        score += 20
        reasons.append("주거 형태 해당")
    if p.get("crisis_match") and signals_level_high:
        score += 20
        reasons.append("위기 상황 신속 지원")
    if 부채규모 >= 1000 and "주거지원" in p["tags"]:
        score += 5
    return score, reasons


def recommend_policies(월소득, 주거점유형태, 가구형태, 가구원수, 부채규모, prob, signals):
    hh_tag = household_tag(가구형태, 가구원수)
    has_high = any(s["level"] == "high" for s in signals)
    scored = []
    for p in WELFARE_POLICIES:
        s, reasons = score_policy(p, hh_tag, 월소득, 주거점유형태, 부채규모, prob, has_high)
        if s > 0:
            scored.append((s, p, reasons))
    scored.sort(key=lambda x: x[0], reverse=True)
    max_score = scored[0][0] if scored else 1
    return scored, max_score, hh_tag


def make_gauge(prob, threshold):
    color = "#D9764A" if prob >= threshold else "#6E8F75"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob * 100,
        number={"suffix": "%", "font": {"size": 38, "family": "Gowun Batang"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#D8CBB6"},
            "bar": {"color": color, "thickness": 0.32},
            "bgcolor": "#F4EBDB",
            "borderwidth": 0,
            "steps": [
                {"range": [0, threshold * 100], "color": "#EFE6D6"},
                {"range": [threshold * 100, 100], "color": "#F7E2D7"},
            ],
            "threshold": {
                "line": {"color": "#3A2E26", "width": 2},
                "thickness": 0.85,
                "value": threshold * 100
            }
        }
    ))
    fig.update_layout(
        height=200,
        margin=dict(l=20, r=20, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": "Noto Sans KR", "color": "#3A2E26"}
    )
    return fig


MEDIAN_INCOME = {1: 239, 2: 393, 3: 503, 4: 610, 5: 711, 6: 806}
HOUSING_BENEFIT = {1: 33, 2: 37, 3: 44, 4: 51, 5: 52, 6: 58}


def estimate_benefits(가구원수, 월소득, 주거점유형태):
    hh = min(max(가구원수, 1), 6)
    median = MEDIAN_INCOME[hh]
    items = []
    line32 = median * 0.32
    if 월소득 < line32:
        amt = round(line32 - 월소득)
        items.append(("생계급여", amt, f"기준 중위소득 32%({line32:.0f}만 원) 대비 소득이 부족한 만큼 매월 현금으로 지급될 것으로 추정돼요."))
    line48 = median * 0.48
    if 월소득 < line48 and 주거점유형태 in [2, 3, 4]:
        items.append(("주거급여", HOUSING_BENEFIT[hh], "전·월세 가구 기준, 1급지 평균 지원액으로 추정한 금액이에요."))
    line50 = median * 0.50
    if 월소득 < line50:
        items.append(("교육급여(자녀 1인 기준)", 5, "초·중·고 자녀가 있다면 교육활동지원비를 연 단위로 지급받을 수 있어요(월 환산 추정)."))
    return items, median


# ────────────────────────────────────────────
# 탭 구성
# ────────────────────────────────────────────
tab_main, tab_policy, tab_faq = st.tabs(["🏠 가구 분석", "📖 복지 제도 한눈에", "❓ 자주 묻는 질문"])

# ══════════════════════════════════════════
# TAB 1 — 가구 분석
# ══════════════════════════════════════════
with tab_main:

    st.markdown('<div class="section-title">가구 정보 입력</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">아래 정보를 입력하면 AI가 분석해드려요. 입력하신 정보는 저장되지 않아요.</div>', unsafe_allow_html=True)

    with st.form("input_form"):
        col1, col2 = st.columns(2)
        with col1:
            가구원수 = st.number_input("👨‍👩‍👧 가구원수 (명)", min_value=1, max_value=7, value=3, step=1)
            가구형태 = st.selectbox(
                "🏠 가구형태",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: {1: "부부", 2: "부부 + 자녀", 3: "한부모 + 자녀", 4: "기타", 5: "1인 가구"}[x],
                index=1
            )
            주거점유형태 = st.selectbox(
                "🔑 주거 점유 형태",
                options=[1, 2, 3, 4, 5, 6],
                format_func=lambda x: {1: "자가", 2: "전세", 3: "보증금 있는 월세", 4: "보증금 없는 월세", 5: "무상 거주", 6: "기타"}[x],
                index=2
            )
        with col2:
            주거면적 = st.number_input("📐 주거 면적 (㎡)", min_value=1.0, max_value=160.0, value=45.0, step=1.0,
                                    help="파생변수(인당 면적, 면적당 소득) 계산에 사용돼요.")
            부채규모 = st.number_input(
                "💳 부채 규모 (만원, 없으면 0)",
                min_value=0.0, max_value=50000.0, value=0.0, step=100.0
            )
            월소득 = st.number_input("💰 월 총소득 (만 원)", min_value=0.0, max_value=2000.0, value=150.0, step=10.0,
                                  help="근로소득 + 사업소득 + 재산소득을 모두 합한 가구의 월 평균 소득이에요.")

        submitted = st.form_submit_button("🔍 우리 가구 분석하기", use_container_width=True)

    if submitted:
        if model is None:
            st.error("모델 파일을 불러오지 못했습니다. welfare_model_real.pkl 파일이 앱과 같은 폴더에 있는지 확인해주세요.")
        else:
            # ──────────────────────────────────────────
            # 핵심 수정: 연간 소득으로 변환 후 파생변수 계산
            # 모델은 연간 총소득으로 학습됨 (KoWePS 원본 기준)
            # ──────────────────────────────────────────
            총소득_연간 = 월소득 * 12

            input_data = build_input_df(
                가구원수, 가구형태, 주거점유형태,
                주거면적, 부채규모, 총소득_연간
            )

            prob_1 = model.predict_proba(input_data)[0][1]

            custom_threshold = 0.35
            predicted = 1 if prob_1 >= custom_threshold else 0

            st.markdown("---")
            st.markdown('<div class="section-title">AI 분석 결과</div>', unsafe_allow_html=True)

            gcol, rcol = st.columns([1, 1.2])
            with gcol:
                st.plotly_chart(make_gauge(prob_1, custom_threshold), use_container_width=True, config={"displayModeBar": False})
            with rcol:
                if predicted == 1:
                    st.markdown("""
                    <div class="result-card result-danger">
                      <div class="result-title">⚠️ 복지 수급 가능성이 있어요</div>
                      <div class="result-caption">아래 위기 신호와 맞춤 복지 제도를 꼭 확인해보세요</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="result-card result-safe">
                      <div class="result-title">✅ 현재 수급 가능성은 낮아요</div>
                      <div class="result-caption">그래도 아래 맞춤 복지 제도는 한 번 살펴보세요</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.caption("※ 이 결과는 한국복지패널(KoWePS) 데이터를 학습한 AI의 참고용 예측입니다. 실제 수급 여부는 거주지 주민센터에서 공식적으로 확인해주세요.")

            signals = detect_crisis_signals(월소득, 주거점유형태, 부채규모, 가구형태, 가구원수)
            hh_tag_display = household_tag(가구형태, 가구원수)
            high_count = sum(1 for s in signals if s["level"] == "high")

            st.markdown(f"""
            <div class="metric-row">
              <div class="metric-box"><div class="v">{hh_tag_display}</div><div class="l">가구 유형</div></div>
              <div class="metric-box"><div class="v">{월소득:.0f}만 원</div><div class="l">월 총소득</div></div>
              <div class="metric-box"><div class="v">{high_count}건</div><div class="l">고위험 신호</div></div>
              <div class="metric-box"><div class="v">{prob_1*100:.1f}%</div><div class="l">수급 가능성</div></div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="section-title">💸 예상 지원금 (월 기준 추정)</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-sub">기준 중위소득과 입력 정보를 바탕으로 계산한 추정치예요. 실제 지급액은 가구별 심사 결과에 따라 달라질 수 있어요.</div>', unsafe_allow_html=True)

            benefit_items, median_income = estimate_benefits(가구원수, 월소득, 주거점유형태)

            if benefit_items:
                total_b = sum(item[1] for item in benefit_items)
                bcols = st.columns(len(benefit_items) + 1)
                for col, (name, amt, desc) in zip(bcols[:-1], benefit_items):
                    with col:
                        st.markdown(f"""
                        <div class="metric-box">
                          <div class="v">+{amt}만</div>
                          <div class="l">{name}</div>
                        </div>
                        """, unsafe_allow_html=True)
                with bcols[-1]:
                    st.markdown(f"""
                    <div class="metric-box" style="border-color: var(--clay);">
                      <div class="v" style="color: var(--clay);">{total_b}만</div>
                      <div class="l">월 합계 추정</div>
                    </div>
                    """, unsafe_allow_html=True)
                for name, amt, desc in benefit_items:
                    st.markdown(f"""
                    <div class="crisis-card crisis-low">
                      <div class="crisis-label">💰 {name} — 약 {amt}만 원/월</div>
                      <div class="crisis-desc">{desc}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info(f"가구원수 {가구원수}명 기준 중위소득은 약 {median_income}만 원이에요. 현재 소득 수준으로는 기초생활보장 급여 추정 대상에 해당하지 않지만, 차상위계층 지원 등은 확인해볼 수 있어요.")

            st.markdown('<div class="section-title">🚨 위기 신호 자동 탐지</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-sub">입력한 정보를 바탕으로 가능한 위기 상황을 미리 살펴봤어요.</div>', unsafe_allow_html=True)

            for s in signals:
                css_class = {"high": "crisis-high", "medium": "crisis-medium", "low": "crisis-low"}[s["level"]]
                st.markdown(f"""
                <div class="crisis-card {css_class}">
                  <div class="crisis-label">{s["icon"]} {s["title"]}</div>
                  <div class="crisis-desc">{s["desc"]}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('<div class="section-title">📋 우리 가구에 맞는 복지 제도</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="section-sub">"{hh_tag_display}" 유형과 입력하신 소득·주거·부채 상황을 기준으로 적합도가 높은 제도부터 보여드려요.</div>', unsafe_allow_html=True)

            scored, max_score, _ = recommend_policies(월소득, 주거점유형태, 가구형태, 가구원수, 부채규모, prob_1, signals)

            if scored:
                top_scored = scored[:4]
                rest_scored = scored[4:]
                for s, p, reasons in top_scored:
                    match_pct = min(100, round(s / max_score * 100))
                    badge_html = "".join([f'<span class="policy-badge">{t}</span>' for t in p["tags"]])
                    reason_html = "".join([f'<span class="match-badge">✓ {r}</span>' for r in reasons])
                    st.markdown(f"""
                    <div class="policy-card top">
                      <div class="policy-name">📌 {p["name"]}</div>
                      <div style="margin: 0.35rem 0;">{badge_html}</div>
                      <div class="policy-desc">{p["desc"]}</div>
                      <div style="margin: 0.4rem 0 0.2rem;">{reason_html}</div>
                      <div class="match-bar-bg"><div class="match-bar-fill" style="width:{match_pct}%;"></div></div>
                      <div class="policy-desc" style="color:#3E5C50; margin-top:0.5rem; font-weight:600;">
                        📞 신청 안내: {p["contact"]}
                      </div>
                    </div>
                    """, unsafe_allow_html=True)
                if rest_scored:
                    with st.expander(f"📂 그 외 확인해볼 만한 제도 {len(rest_scored)}개 더 보기"):
                        for s, p, reasons in rest_scored:
                            badge_html = "".join([f'<span class="policy-badge">{t}</span>' for t in p["tags"]])
                            st.markdown(f"""
                            <div class="policy-card">
                              <div class="policy-name">📌 {p["name"]}</div>
                              <div style="margin: 0.35rem 0;">{badge_html}</div>
                              <div class="policy-desc">{p["desc"]}</div>
                              <div class="policy-desc" style="color:#3E5C50; margin-top:0.4rem; font-weight:600;">
                                📞 신청 안내: {p["contact"]}
                              </div>
                            </div>
                            """, unsafe_allow_html=True)
            else:
                st.info("현재 조건에서는 우선 추천 제도가 없어요. '복지 제도 한눈에' 탭에서 전체 제도를 확인해보세요.")

            st.markdown("---")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.link_button("🌐 복지로 바로가기", "https://www.bokjiro.go.kr", use_container_width=True)
            with col_b:
                st.link_button("📞 복지 상담 129", "tel:129", use_container_width=True)
            with col_c:
                st.link_button("🏠 주거급여 안내", "https://www.myhome.go.kr", use_container_width=True)
    else:
        st.info("👆 가구 정보를 입력하고 **'우리 가구 분석하기'** 버튼을 눌러보세요.")


# ══════════════════════════════════════════
# TAB 2 — 복지 제도 한눈에
# ══════════════════════════════════════════
with tab_policy:
    st.markdown('<div class="section-title">📖 전체 복지 제도 한눈에 보기</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">보건복지부 공식 기준(2025년)을 바탕으로 정리했어요. 가구 유형을 선택하면 그에 맞는 제도만 모아볼 수 있어요.</div>', unsafe_allow_html=True)

    filter_option = st.selectbox(
        "가구 유형으로 필터링",
        options=["전체 보기", "1인가구", "다인가구", "한부모"],
        key="tab2_filter",
        index=0
    )

    if filter_option == "전체 보기":
        specific = []
        universal = WELFARE_POLICIES
    else:
        specific = [p for p in WELFARE_POLICIES if filter_option in p["household"] and "전체" not in p["household"]]
        universal = [p for p in WELFARE_POLICIES if "전체" in p["household"]]

    if filter_option != "전체 보기" and specific:
        st.markdown(f"#### ✅ {filter_option} 맞춤 제도")
        for p in specific:
            badge_html = "".join([f'<span class="policy-badge">{t}</span>' for t in p["tags"]])
            hh_html = "".join([f'<span class="match-badge">{h}</span>' for h in p["household"]])
            st.markdown(f"""
            <div class="policy-card top">
              <div class="policy-name">📌 {p["name"]}</div>
              <div style="margin: 0.35rem 0;">{badge_html}{hh_html}</div>
              <div class="policy-desc">{p["desc"]}</div>
              <div class="policy-desc" style="color:#3E5C50; margin-top:0.4rem; font-weight:600;">
                📞 신청 안내: {p["contact"]}
              </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("#### 📋 모든 가구 대상 제도")
    elif filter_option != "전체 보기":
        st.info(f"'{filter_option}' 전용 제도는 따로 없어요. 아래 모든 가구 대상 제도를 확인해보세요.")
        st.markdown("#### 📋 모든 가구 대상 제도")

    filtered = universal if filter_option != "전체 보기" else WELFARE_POLICIES
    for p in filtered:
        badge_html = "".join([f'<span class="policy-badge">{t}</span>' for t in p["tags"]])
        hh_html = "".join([f'<span class="match-badge">{h}</span>' for h in p["household"]])
        st.markdown(f"""
        <div class="policy-card">
          <div class="policy-name">📌 {p["name"]}</div>
          <div style="margin: 0.35rem 0;">{badge_html}{hh_html}</div>
          <div class="policy-desc">{p["desc"]}</div>
          <div class="policy-desc" style="color:#3E5C50; margin-top:0.4rem; font-weight:600;">
            📞 신청 안내: {p["contact"]}
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.info("💡 **복지멤버십**(복지로 회원가입)에 가입하면 가구 상황에 맞는 급여를 자동으로 안내받을 수 있어요.")
    st.link_button("🌐 복지로 전체 정책 검색", "https://www.bokjiro.go.kr", use_container_width=True)


# ══════════════════════════════════════════
# TAB 3 — 자주 묻는 질문
# ══════════════════════════════════════════
with tab_faq:
    st.markdown('<div class="section-title">❓ 자주 묻는 질문</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">이 서비스를 이용하기 전에 알아두면 좋은 내용들을 모았어요.</div>', unsafe_allow_html=True)

    # --------------------------------------------------
    # 📊 시각화 — 실제 KoWePS 데이터 기반 수치로 교체
    # --------------------------------------------------
    kor_font = fm.FontProperties(family='NanumGothic')
    plt.rcParams['font.family'] = 'NanumGothic'
    plt.rcParams['axes.unicode_minus'] = False

    COLOR_POS = '#D9764A'
    COLOR_NEG = '#6E8F75'

    fig_vis, axes = plt.subplots(1, 3, figsize=(16, 4.5))
    fig_vis.patch.set_facecolor('#FBF4E8')
    for ax in axes:
        ax.set_facecolor('#FBF4E8')

    # 그래프 [1] 변수 중요도 — welfare_model_real.pkl 기준 8개 피처
    importances = model.feature_importances_
    feature_names = ['가구원수', '가구형태', '주거점유형태', '부채규모', '총소득', '인당_주거면적', '소득대비부채', '면적당소득']
    indices = np.argsort(importances)[::-1]
    axes[0].bar(range(len(feature_names)), importances[indices], color=COLOR_POS, edgecolor='white')
    axes[0].set_xticks(range(len(feature_names)))
    axes[0].set_xticklabels([feature_names[i] for i in indices], rotation=25, fontsize=8, fontproperties=kor_font)
    axes[0].set_title('변수 중요도 (랜덤포레스트)', fontweight='bold', fontsize=10, fontproperties=kor_font)
    axes[0].set_ylabel('중요도', fontproperties=kor_font)

    # 그래프 [2] 수급여부 분포 — 실제 데이터 (비수급 6105 / 수급 953)
    counts_val = [6105, 953]
    total = sum(counts_val)
    axes[1].bar(['비수급자', '수급자'], counts_val, color=[COLOR_NEG, COLOR_POS], edgecolor='white', width=0.5)
    axes[1].set_xticklabels(['비수급자', '수급자'], fontproperties=kor_font)
    for i, val in enumerate(counts_val):
        axes[1].text(i, val + 30, f'{val:,}명\n({val/total*100:.1f}%)', ha='center', fontweight='bold', fontsize=9, fontproperties=kor_font)
    axes[1].set_title('수급여부 분포 (클래스 불균형)', fontweight='bold', fontsize=10, fontproperties=kor_font)
    axes[1].set_ylabel('가구 수', fontproperties=kor_font)
    axes[1].set_ylim(0, max(counts_val) * 1.2)

    # 그래프 [3] 총소득 구간별 수급자 비율 — 실제 KoWePS 계산값
    labels_b = ['0~50', '50~100', '100~200', '200~300', '300~500', '500~1000', '1000+']
    rates = [27.6, 10.9, 9.0, 7.3, 2.0, 1.0, 0.3]   # 실제 데이터 기반
    axes[2].bar(labels_b, rates, color=COLOR_POS, alpha=0.8, edgecolor='white')
    for i, val in enumerate(rates):
        axes[2].text(i, val + 0.3, f'{val:.1f}%', ha='center', fontsize=8, fontweight='bold', fontproperties=kor_font)
    axes[2].set_title('월소득 구간별 수급자 비율', fontweight='bold', fontsize=10, fontproperties=kor_font)
    axes[2].set_xlabel('월 총소득 (만원)', fontsize=9, fontproperties=kor_font)
    axes[2].set_ylabel('수급자 비율 (%)', fontproperties=kor_font)
    axes[2].tick_params(axis='x', labelsize=8)

    plt.tight_layout()

    st.markdown('### 📊 AI 모델 데이터 분석 및 주요 탐색 결과')
    st.pyplot(fig_vis)
    plt.close(fig_vis)
    st.markdown('<hr style="border:1px solid #F4EAD4;">', unsafe_allow_html=True)

    # --------------------------------------------------
    # ❓ FAQ 리스트
    # --------------------------------------------------
    faqs = [
        ("이 결과가 실제 수급 자격을 의미하나요?",
         "아니요. 이 서비스는 한국복지패널(KoWePS) 데이터를 학습한 AI 모델의 <b>참고용 예측</b>이에요. "
         "실제 기초생활보장 수급 여부는 소득·재산·부양의무자 기준 등을 종합한 행정 조사를 통해 "
         "거주지 주민센터에서 최종적으로 결정돼요."),
        ("입력한 정보는 저장되거나 외부로 전송되나요?",
         "아니요. 입력한 정보는 화면에서 예측을 보여주는 데만 사용되고 별도로 저장되지 않아요. "
         "다만 정확한 안내를 위해 실제 신청 시에는 주민센터에 직접 정보를 제출해야 해요."),
        ("'수급 가능성'은 어떻게 계산되나요?",
         "가구원수, 가구형태, 주거 점유 형태, 부채 규모, 총소득 5개 기본 변수에 더해 "
         "<b>인당 주거면적·소득 대비 부채비율·면적당 소득</b> 3개 파생변수까지 총 8개 피처로 "
         "랜덤포레스트 모델이 KoWePS 데이터 패턴을 학습해 수급 여부를 확률로 예측해요. "
         "수급자를 놓치지 않는 것이 더 중요하다고 판단해, 일반적인 50% 기준 대신 <b>35%만 넘어도 '가능성 있음'</b>으로 표시하고 있어요."),
        ("예상 지원금은 정확한 금액인가요?",
         "아니요. 2025년 기준 중위소득을 기준으로 한 <b>단순 추정치</b>예요. 실제 지급액은 가구의 "
         "재산, 부양의무자, 근로능력, 거주 지역(급지) 등에 따라 달라질 수 있어요. 정확한 금액은 "
         "복지로 모의계산 또는 주민센터 상담을 통해 확인해주세요."),
        ("위기 신호 탐지는 어떤 기준으로 판단하나요?",
         "소득 수준, 주거 형태(보증금 없는 월세·무상 거주 등), 부채 규모, 가구 형태(한부모·1인 가구) 등을 "
         "기준으로 단전·단수, 건강보험료 체납, 퇴거, 고립 등의 위험 신호를 규칙 기반으로 판단해요. "
         "실제 위기 상황 여부는 보건복지상담센터(☎ 129) 상담을 통해 확인하는 게 가장 정확해요."),
        ("어떤 가구가 1인가구 / 다인가구 / 한부모로 분류되나요?",
         "가구원수가 1명이거나 가구형태를 '1인 가구'로 선택하면 <b>1인가구</b>, 가구형태가 "
         "'한부모 + 자녀'면 <b>한부모</b>, 그 외에는 <b>다인가구</b>로 분류돼요."),
        ("주거면적은 예측에 직접 사용되나요?",
         "직접 피처로는 사용되지 않지만, 모델 학습에 쓰인 <b>인당 주거면적</b>(주거면적 ÷ 가구원수)과 "
         "<b>면적당 소득</b>(총소득 ÷ 주거면적) 파생변수를 계산하는 데 활용돼요. 따라서 면적 입력이 "
         "정확할수록 예측 정밀도가 높아집니다."),
    ]

    for q, a in faqs:
        with st.expander(f"Q. {q}"):
            st.markdown(f"<div class='policy-desc'>{a}</div>", unsafe_allow_html=True)
