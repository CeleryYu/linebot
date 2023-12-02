from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import datetime
import os

app = Flask(__name__)

line_bot_api = LineBotApi('ofZ8Zu8xLMIp7k/CqUN8amL45Sahn7t4w7ZhndSBk+e7HISzHG7V1sZe52IR65c3euwW/utIMmSaGxUMgJnp1U6MFq/fNh3ERB3+dlx31pxfZNqf9oi2s+1+UwlRu2Hy8HllGCAPbScdIr/ZAPpPCQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('Y84c10630243d396fea192496c7268d16')

line_bot_api.push_message('U29fccb6e017276d8f643b99962307fb5', TextSendMessage(text='你可以開始了'))

# 問題列表
questions = {
    '1': {'question': '請問您昨晚的睡眠如何？ 1.很好 2.一般 3.不好'},
    '2': {'question': '您的心情跟平時比起來如何呢？1.很好 2.一般 3.不好'},
    '3': {'question': '您的身體狀況跟平時比起來如何呢？1.好 2.不好'},
    '4': {'question': '您是哪個部位不舒服呢？1.頭 2.脖子 3.手 4.腳 5.背 6.腰 7.心臟'},
    '5': {'question': '其部位跟平時比起來的疼痛度為何？1.一直都這樣 2.突然開始痛'},
    '6': {'question': '今天的食慾跟平時比起來如何？1.很好 2.一般 3.不好'}
}

# 目前處於第幾個問題
current_question_index = 1

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global current_question_index

    user_response = event.message.text

    # 儲存使用者回答

    # 發送下一個問題
    if current_question_index <= len(questions):
        next_question = questions[str(current_question_index)]['question']
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=next_question))
        current_question_index += 1
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='謝謝您的回答，問卷已完成。'))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
