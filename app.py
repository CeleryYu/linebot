#助教調過的程式碼
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
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('dHXecqvpOvx8In5RQHci6bbWTlu0FA3kICv0DqMe/Pj0rLQZuux23kX/royu7Pw/IZ0qPTVmW1myNJT9fo2fjOivhaUCHcQeU0mTba+Yl6+FEfLDyoyLDbhGJW9uYi6d27G+uk2Qum/z2KRxgIlBygdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('ee0b2607b4cd2206e11c6f0dafa88144')

line_bot_api.push_message('U5f5c99cca72d8bb1d3111c3a00e03cea', TextSendMessage(text='你可以開始了'))
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
#messages = [TextSendMessage(text='我是朱虹聿，這linebot被我劫持了。')]

# 發送廣播消息
#response = line_bot_api.broadcast(messages=messages)

#try2
# 定義關鍵字和回覆內容
from linebot.models import TextSendMessage

questions = {
    '1': {'question': '請問您昨晚的睡眠如何？ 1.很好 2.一般 3.不好'},
    '2': {'question': '您的心情跟平時比起來如何呢？1.很好 2.一般 3.不好'},
    '3': {'question': '您的身體狀況跟平時比起來如何呢？1.好 2.不好'},
    '4': {'question': '您是哪個部位不舒服呢？1.頭 2.脖子 3.手 4.腳 5.背 6.腰 7.心臟'},
    '5': {'question': '其部位跟平時比起來的疼痛度為何？1.一直都這樣 2.突然開始痛'},
    '6': {'question': '今天的食慾跟平時比起來如何？1.很好 2.一般 3.不好'}
}

current_question_number = 1  # 初始問題編號

# 處理使用者回答的函數
def handle_user_response(user_response):
    global current_question_number

    # 根據問題編號取得當前問題
    current_question = questions.get(str(current_question_number))

    if current_question:
        # 更新問題編號
        current_question_number += 1

        # 根據使用者回答處理下一個問題
        next_question = handle_next_question(current_question_number, user_response)

        return TextSendMessage(text=next_question)
    else:
        return TextSendMessage(text='謝謝您的回答！')

# 根據問題編號處理下一個問題的函數
def handle_next_question(question_number, user_response):
    # 在這裡實現你的邏輯，根據問題編號和使用者回答來返回下一個問題的內容
    # 這只是一個簡單的例子，你可以根據實際需求進行修改
    if question_number == 2:
        if user_response == '1':
            return '好的，心情很好！下一個問題...'
        elif user_response == '2':
            return '一般般，繼續下一個問題...'
        elif user_response == '3':
            return '不太好，請告訴我原因...'
    elif question_number == 3:
        # 添加第三個問題的邏輯...

# 在使用者回答時呼叫處理函數
user_response = '1'  # 使用者回答的內容
response_message = handle_user_response(user_response)

# 將回應訊息發送給使用者
print(response_message.text)


    # 如果訊息中沒有任何關鍵字，可以回覆預設訊息或不回覆
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


#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
