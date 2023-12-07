#broadcast成功的程式碼
# -*- coding: utf-8 -*-

#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('ofZ8Zu8xLMIp7k/CqUN8amL45Sahn7t4w7ZhndSBk+e7HISzHG7V1sZe52IR65c3euwW/utIMmSaGxUMgJnp1U6MFq/fNh3ERB3+dlx31pxfZNqf9oi2s+1+UwlRu2Hy8HllGCAPbScdIr/ZAPpPCQdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('Y84c10630243d396fea192496c7268d16')

line_bot_api.push_message('U29fccb6e017276d8f643b99962307fb5', TextSendMessage(text='你可以開始了'))
# 要發送的訊息
#message = TextSendMessage(text='我是朱虹聿，這linebot被我劫持了。')

# 發送廣播消息
#response = line_bot_api.broadcast(messages=message)

# 檢查是否成功
#if response.status_code == 200:
    #print("廣播消息發送成功！")
#else:
   #print(f"廣播消息發送失敗，錯誤碼：{response.status_code}")
    #print(response.json())
#嘗試
#try1
# 要發送的訊息
messages = [TextSendMessage(text='我是朱虹聿，這linebot被我劫持了。')]

# 發送廣播消息
response = line_bot_api.broadcast(messages=messages)
#try2

image_urls = [
    'https://drive.google.com/file/d/1RHygPRwNg0bdiN51i35X1B7XefC6FNW2/view?usp=sharing',
    'https://drive.google.com/file/d/1lqrH_34kf-J50LMXO9aidJMYmOYHYGkB/view?usp=sharing',
    'https://drive.google.com/file/d/1iM9CqTPbdwA3oIi8ZmcYzvetxLfdr2CP/view?usp=sharing',
    'https://drive.google.com/file/d/1ChEFRM_EBDD9fV7UNAlNEJSaTJS714qw/view?usp=sharing',
    'https://drive.google.com/file/d/1V9g79W8tuMH_TP4Ce54dgmdSs91I0LXp/view?usp=sharing',
    'https://drive.google.com/file/d/1U7VInWvCxUtlCL9Xs6MqLnLbC0OOL2dh/view?usp=sharing',
    'https://drive.google.com/file/d/1LffGzf3uyg66igeiqyCRVwic8EPz5r6h/view?usp=sharing',
    'https://drive.google.com/file/d/1zWz0lplkaHbwIV583XIQ5TshiYzI1bek/view?usp=sharing',
    'https://drive.google.com/file/d/1U4wXJRYFmEYtYJSJfSocQ9ATylJAt8NF/view?usp=sharing',
    'https://drive.google.com/file/d/1htUL52vKgiCyz8LbirhhqIck8jYTkzA_/view?usp=sharing',
    'https://drive.google.com/file/d/1wBmzZW9Vk562fCnZNMo13udNWAkQhgnL/view?usp=sharing',
    'https://drive.google.com/file/d/1x_-aqNYji_Z2JkH9YBeGL9C13b6ahIr8/view?usp=sharing',
    'https://drive.google.com/file/d/16LkzQ_yXmJInigzVkBpsH346ikF_j1q4/view?usp=sharing',
    'https://drive.google.com/file/d/1EKG6fMV15vCCXJHX-I6sCxLP7DFOs09Q/view?usp=sharing',
    'https://drive.google.com/file/d/1GWczzcsioSeKtNbbIc7Qv1v02Cbr81BG/view?usp=sharing',
    'https://drive.google.com/file/d/1uCpyX5Btnh3IF9BGs2ULgAFJY850X6HP/view?usp=sharing',
    'https://drive.google.com/file/d/1S8_jFsJc9Ob_-XclL48n6k3uMgma74R1/view?usp=sharing',
    'https://drive.google.com/file/d/1M78gGbo0aJ9djfX89kHarhy7v7TAuam2/view?usp=sharing',
    'https://drive.google.com/file/d/1F7SlRsvpzxU58VoWIyO8LWRj5DKyjSPg/view?usp=sharing',
    'https://drive.google.com/file/d/1bT9i-inItuGN12StnBaaPRKzectuRPsP/view?usp=sharing'
    # 添加更多連結...
]

def send_scheduled_message():
    # 隨機選擇一個圖片連結
    
    
    selected_image_url = random.choice(image_urls)

    # 發送圖片給用戶
    line_bot_api.broadcast(
        ImageSendMessage(original_content_url=selected_image_url, preview_image_url=selected_image_url)
    )

# 設定每天時間執行一次
schedule.every().day.at("20:45").do(send_scheduled_message)
#try2
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_response = event.message.text

    # 根據使用者回覆做相對應的回應
    if user_response == '你好':
        reply_message = '你好！'
    elif user_response == '再見':
        reply_message = '再見！'
        # 如果收到 '再見' 回覆，你可以結束對話或執行其他操作

    # 回覆使用者
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
#嘗試結束
# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token,message)

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
