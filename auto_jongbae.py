import schedule
import time
from datetime import datetime
import requests

# 1. 텔레그램 메시지 보내는 함수
def send_telegram_message(message):
    token = "8812942768:AAEmNuVuayecKgur-U9WtXV8x8xG0-vaOZc"     # 아까 봇파더에게 받은 토큰 (따옴표 유지)
    chat_id = "8853037286"   # 아까 숫자로만 된 Chat ID (따옴표 유지)
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    requests.post(url, json=payload)

# 2. 실제로 실행될 작업 (종가베팅 분석)
def job():
    now = datetime.now()
    print(f"\n[{now.strftime('%Y-%m-%d %H:%M:%S')}] 종가베팅 분석을 시작합니다!")
    
    # ==============================================================
    # 🌟 여기에 원래 작성하셨던 주식 분석 코드를 넣으시면 됩니다! 🌟
    # 지금은 테스트용으로 가짜 결과를 만들겠습니다.
    # ==============================================================
    
    # 분석이 끝났다고 가정하고 메시지 작성
    result_message = "🔥 [오늘의 종가베팅 추천 종목]\n\n"
    result_message += "1. 삼성전자 (현재가: 80,000원) - 점수: 85점\n"
    result_message += "2. 한미반도체 (현재가: 130,000원) - 점수: 90점\n"
    
    # 텔레그램으로 전송!
    send_telegram_message(result_message)
    print("텔레그램 알림 전송 완료!")

# 3. 알람시계 맞추기 (매일 오후 3시 12분)
# 서버나 PC의 시간이 한국 시간으로 맞춰져 있어야 합니다.
schedule.every().day.at("15:12").do(job)

# 테스트용: 프로그램을 켰을 때 잘 작동하는지 10초 뒤에 한번 보내보기 (확인용)
# 확인이 끝나면 아래 한 줄은 지우거나 앞에 #을 붙여서 꺼주세요.
# schedule.every(10).seconds.do(job) 

print("로봇이 켜졌습니다. 매일 오후 3시 12분을 기다리는 중입니다... (창을 끄지 마세요!)")

# 4. 무한 반복 (프로그램이 꺼지지 않게 계속 켜두는 역할)
while True:
    schedule.run_pending() # 할 일이 있는지 시계를 확인
    time.sleep(1)          # 1초 쉬고 다시 확인 (컴퓨터 과부하 방지)
