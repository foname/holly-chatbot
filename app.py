import json

from flask import Flask, request, abort, make_response

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
app = Flask(__name__)
app.config.from_pyfile('config/config_file.cfg')


cred = credentials.Certificate(app.config['FIREBASE_PRIVATE_KEY_PATH'])
firebase_admin.initialize_app(cred)
db = firestore.client()

line_bot_api = LineBotApi(app.config['LINE_ACCESS_TOKEN'])
handler = WebhookHandler(app.config['WEBHOOK_ID'])

@app.route("/callback", methods=['POST'])
def callback():
    req = request.get_json(silent=True, force=True)
    res = process_request(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def process_request(req):
    if req['queryResult']['queryText'] == 'ไม่สมัคร':
        return None
    uid = req['originalDetectIntentRequest']['payload']['data']['source']['userId']
    msg = req['originalDetectIntentRequest']['payload']['data']['message']['text']
    user_profile = line_bot_api.get_profile(uid)
    db.collection(u'user').document(uid).set(user_profile.as_json_dict())
    res = build_response("สมัครเรียบร้อยแล้วค่ะ")
    return res


def build_response(speech):
    return {
        "fulfillmentText": speech
    }


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    app.run()
