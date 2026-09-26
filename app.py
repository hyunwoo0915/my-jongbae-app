import requests
import pandas as pd
import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="종가베팅 포착기", layout="wide")

st.title("🎯 오늘 오후 종가베팅 추천 종목")
st.caption("오후 3시~3시 20분 진입 전용 스코어링 대시보드")

# 보안을 위해 설정값에서 API 키 불러오기
APP_KEY = st.secrets.get("KIS_APPKEY", "")
APP_SECRET = st.secrets.get("KIS_APPSECRET", "")
URL_BASE = "https://openapi.koreainvestment.com:9443"

@st.cache_data(ttl=3600)
def get_access_token():
    headers = {"content-type": "application/json"}
    body = {"grant_type": "client_credentials", "appkey": APP_KEY, "appsecret": APP_SECRET}
    res = requests.post(f"{URL_BASE}/oauth2/tokenP", headers=headers, json=body)
    return res.json().get("access_token")

def fetch_top_trading_volume(token):
    path = "/uapi/domestic-stock/v1/ranking/trade-value"
    headers = {
        "content-type": "application/json",
        "authorization": f"Bearer {token}",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET,
        "tr_id": "FHPST01710000"
    }
    params = {
        "FID_COND_MRKT_DIV_CODE": "J", "FID_COND_SCR_DIV_CODE": "20171",
        "FID_INPUT_ISCD": "0000", "FID_DIV_CLS_CODE": "0",
        "FID_BLNG_CLS_CODE": "0", "FID_TRGT_CLS_CODE": "0",
        "FID_TRGT_EXLS_CLS_CODE": "0", "FID_INPUT_PRICE_1": "",
        "FID_INPUT_PRICE_2": "", "FID_VOL_CONT": ""
    }
    res = requests.get(f"{URL_BASE}/{path}", headers=headers, params=params)
    return pd.DataFrame(res.json().get('output', []))

def calculate_score(row):
    score = 0
    reasons = []
    
    # 1. 거래대금 계산 (1000억 이상)
    price = float(row.get('stck_prpr', 0))
    vol = float(row.get('acml_vol', 0))
    trade_val = (price * vol) / 100000000
    
    if trade_val >= 2000:
        score += 30
        reasons.append("거래대금 2000억 이상")
    elif trade_val >= 1000:
        score += 20
        reasons.append("거래대금 1000억 이상")
        
    # 2. 등락률 계산 (7% ~ 22% 권역)
    rate = float(row.get('prdy_ctrt', 0))
    if 7.0 <= rate <= 22.0:
        score += 30
        reasons.append(f"적정 상승률({rate}%)")
        
    # 3. 윗꼬리 체크 (고가 대비 종가 관리)
    high = float(row.get('stck_hgpr', 1))
    close = float(row.get('stck_prpr', 1))
    open_p = float(row.get('stck_oprc', 1))
    
    if high > open_p:
        tail_ratio = ((high - close) / (high - open_p)) * 100
        if tail_ratio < 20:
            score += 40
            reasons.append("종가 고가 관리 잘됨")
            
    return score, ", ".join(reasons)

# 메인 실행 화면
if st.button("🔥 실시간 종가베팅 후보 분석 실행"):
    if not APP_KEY or not APP_SECRET:
        st.error("API 키 설정이 필요합니다.")
    else:
        token = get_access_token()
        df = fetch_top_trading_volume(token)
        
        results = []
        for idx, row in df.iterrows():
            score, reason = calculate_score(row)
            if score >= 50:  # 50점 이상 종목만
                results.append({
                    "종목명": row.get('hts_kor_isnm'),
                    "현재가": f"{int(row.get('stck_prpr', 0)):,}원",
                    "등락률": f"{float(row.get('prdy_ctrt', 0))}%",
                    "종베점수": score,
                    "포착이유": reason
                })
        
        res_df = pd.DataFrame(results).sort_values(by="종베점수", ascending=False)
        st.dataframe(res_df, use_container_width=True)
