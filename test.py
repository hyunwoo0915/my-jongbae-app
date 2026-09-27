import requests

def send_telegram_message(message):
    token = "8812942768:AAEmNuVuayecKgur-U9WtXV8x8xG0-vaOZc"
    chat_id = "8853037286"
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("텔레그램 알림 발송 성공!")
    else:
        print("발송 실패:", response.text)

# 테스트해보기
send_telegram_message("🔥 테스트 메시지: 종가베팅 알림봇 정상 작동 중!")
