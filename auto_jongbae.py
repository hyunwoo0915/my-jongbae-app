import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

# 깃허브 비밀금고에서 정보 가져오기
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, json=payload)

# 🌟 새롭게 추가된 뉴스 분석 함수 🌟
def get_news_score(stock_name):
    # 네이버 뉴스에 종목 이름 검색
    url = f"https://search.naver.com/search.naver?where=news&query={stock_name}"
    # 컴퓨터가 아닌 진짜 사람인 척하는 코드 (네이버 차단 방지)
    headers = {"User-Agent": "Mozilla/5.0"} 
    
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    # 뉴스 제목들만 쏙쏙 뽑아오기
    titles = soup.find_all('a', class_='news_tit')
    
    # 종가베팅에 유리한 '호재 키워드' 사전
    good_keywords = ['수주', '돌파', '흑자', '공급', '계약', '퀄테스트', '최대 실적', '수혜']
    
    bonus_score = 0
    found_keywords = []
    
    for title in titles:
        text = title.get_text() # 뉴스 제목 텍스트
        for kw in good_keywords:
            if kw in text:
                bonus_score += 10  # 호재 하나당 10점 추가!
                found_keywords.append(kw)
                
    # 중복된 키워드 정리
    found_keywords = list(set(found_keywords))
    
    return bonus_score, found_keywords

def main():
    now = datetime.now()
    
    # 임시 관심 종목 리스트 (추후 조건검색기 연동)
    candidates = ["삼성전자", "한미반도체"]
    
    result_message = f"🔥 [{now.strftime('%m/%d')} 뉴스 기반 종베 분석]\n\n"
    
    for stock in candidates:
        base_score = 50 # 기본 점수 50점 세팅
        
        # 뉴스 점수와 발견된 호재 단어들 가져오기
        news_score, keywords = get_news_score(stock)
        total_score = base_score + news_score
        
        result_message += f"▶ {stock}\n"
        result_message += f" - 총점: {total_score}점\n"
        
        if keywords:
            result_message += f" - 💡 발견된 호재: {', '.join(keywords)}\n"
        else:
            result_message += f" - 💤 특별한 호재 뉴스 없음\n"
        result_message += "\n"
        
    send_telegram_message(result_message)
    print("뉴스 분석 및 알림 전송 완료!")

if __name__ == "__main__":
    main()
