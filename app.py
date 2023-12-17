from flask import Flask, request, abort

import datetime
#import schedule
#import time

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# Channel Access Token
CHANNEL_ACCESS_TOKEN = 'dHXecqvpOvx8In5RQHci6bbWTlu0FA3kICv0DqMe/Pj0rLQZuux23kX/royu7Pw/IZ0qPTVmW1myNJT9fo2fjOivhaUCHcQeU0mTba+Yl6+FEfLDyoyLDbhGJW9uYi6d27G+uk2Qum/z2KRxgIlBygdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

# Channel Secret
CHANNEL_SECRET = 'ee0b2607b4cd2206e11c6f0dafa88144'
handler = WebhookHandler(CHANNEL_SECRET)

line_bot_api.push_message('U5f5c99cca72d8bb1d3111c3a00e03cea', TextSendMessage(text='您的身體狀況跟平時比起來如何呢？1.好 2.不好'))

# 要發送的訊息
#messages = [TextSendMessage(text='我是朱虹聿，這linebot被我劫持了。')]

# 發送廣播消息
#response = line_bot_api.broadcast(messages=messages)

keyword_responses = {
    '1': '謝謝你的回覆！祝你有美好的一天',
    '2': '您是哪個部位不舒服呢？a.頭 b.脖子 c.手 d.腳 e.背 f.腰 g.心臟',
    'a': '其部位跟平時比起來的疼痛度為何？甲.一直都這樣 乙.突然開始痛',
    'b': '其部位跟平時比起來的疼痛度為何？甲.一直都這樣 乙.突然開始痛',
    'c': '其部位跟平時比起來的疼痛度為何？甲.一直都這樣 乙.突然開始痛',
    'd': '其部位跟平時比起來的疼痛度為何？甲.一直都這樣 乙.突然開始痛',
    'e': '其部位跟平時比起來的疼痛度為何？甲.一直都這樣 乙.突然開始痛',
    'f': '其部位跟平時比起來的疼痛度為何？甲.一直都這樣 乙.突然開始痛',
    'g': '其部位跟平時比起來的疼痛度為何？甲.一直都這樣 乙.突然開始痛',
    '甲':'今天的食慾跟平時比起來如何？h.很好 i.一般 j.不好',
    '乙':'今天的食慾跟平時比起來如何？h.很好 i.一般 j.不好',
    'h':'謝謝你的回覆！祝你有美好的一天',
    'i':'謝謝你的回覆！祝你有美好的一天',
    'j':'謝謝你的回覆！祝你有美好的一天'
    }

# 紀錄次數
# 儲存用戶回答的 dictionary
user_responses = {}

# 儲存用戶資料用的模組
import pandas as pd
import pygsheets

gc = pygsheets.authorize(service_file='linebot-408306-c24b0b63b2cf.json')
sht = gc.open_by_url('https://docs.google.com/spreadsheets/d/1TLRVLW0s9wKxAnvw8yQjBM3r19hWrtVjsPOMeOW73Ts/')

def judge_question(keyword):
    if keyword in '12':
        q = '身體狀況'
    elif keyword in 'abcdefg':
        q = '疼痛部位'
    elif keyword in '甲乙':
        q = '疼痛程度'
    elif keyword in 'hij':
        q = '食慾'
    return q

# 要求內容修改處
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    user_name = profile.display_name
    user_message = event.message.text
    
    if user_name in [ws.title for ws in sht.worksheets()]:
        wks = sht.worksheet_by_title(user_name)
    else:
        wks = sht.add_worksheet(user_name)
        # 列名
        columns = ['date', '身體狀況', '疼痛部位', '疼痛程度', '食慾']
        wks.set_dataframe(pd.DataFrame(columns=columns), start='B1', copy_index=False, nan='')
    
    # 檢查關鍵字
    for keyword, response in keyword_responses.items():
        if keyword in user_message:
            # 如果訊息包含關鍵字，回覆相應內容
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response))
            question = judge_question(keyword)
            
            # 記錄用戶回答的問題和內容，以及用戶ID和日期
            current_date = datetime.date.today().strftime('%Y-%m-%d')
            user_responses = {
                question: [user_message],
                'date': [current_date]
            }

            # 取得用戶以前的資料，並轉為dataframe
            user_data_df = wks.get_as_df(start='B1', empty_value='', include_tailing_empty=False)
            
            # 檢查是否有相同日期的資料
            if current_date in user_data_df['date'].values:
                # 更新現有資料
                user_data_df.at[user_data_df.index.values[-1], question] = user_responses[question]
                combined_user_data = user_data_df
            else:
                # 新增一行資料
                user_responses_df = pd.DataFrame(user_responses)
                combined_user_data = pd.concat([user_data_df, user_responses_df], ignore_index=True)

            # 將結合後的dataframe匯入用戶的工作表中
            wks.set_dataframe(combined_user_data, 'A1', copy_index=True, nan='')
            
            return

#message = TextSendMessage(text='您的身體狀況跟平時比起來如何呢？1.好 2.不好')

'''
import os
#os.environ['TZ'] = 'Asia/Taipei'
'''

# 定義推送任務
'''
def push_message():
    line_bot_api.push_message('U5f5c99cca72d8bb1d3111c3a00e03cea', messages=message)
'''
# 每天的8:00 AM執行推送任務
#schedule.every().day.at('8:00').do(push_message)


# 推送訊息的主程式
'''
def push_job():
    while True:
        schedule.run_pending()
        time.sleep(1)
'''
# 推送訊息的主程式啟動




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


#主程式
import os
if __name__ == "__main__":
    # 使用多執行緒避免 blocking
    '''
    import threading
    thread = threading.Thread(target=push_job)
    thread.start()
    '''
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
