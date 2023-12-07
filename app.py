#學姊原本的程式碼
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
#嘗試
# 要發送的訊息
message = TextSendMessage(text='這是一則廣播消息。')

# 發送廣播消息
response = line_bot_api.broadcast(messages=message)

# 檢查是否成功
if response.status_code == 200:
    print("廣播消息發送成功！")
else:
    print(f"廣播消息發送失敗，錯誤碼：{response.status_code}")
    print(response.json())
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
