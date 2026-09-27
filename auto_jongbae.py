import requests
import os
from datetime import datetime

# 깃허브 비밀금고에서 내 텔레그램 정보를 몰래 가져옵니다
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, json=payload)

def main():
    now = datetime.now()
    print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] 종가베팅 분석 시작!")
    
    # 🌟 나중에 여기에 진짜 주식 데이터 분석 코드를 넣으시면 됩니다 🌟
    result_message = "🔥 [오늘의 종가베팅 추천 종목]\n\n1. 삼성전자 (80,000원)\n2. 한미반도체 (130,000원)"
    
    send_telegram_message(result_message)
    print("알림 전송 완료!")

# 이 파일을 실행하면 main() 함수가 딱 한 번만 실행되고 끝납니다.
if __name__ == "__main__":
    main()
