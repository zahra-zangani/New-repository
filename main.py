import requests
from flask import Flask, request

app = Flask(__name__)

# توکن روبیکا رو اینجا بذار
TOKEN = "BCDFA0DNWUDLMHDXPXFBUEQFANMLFDGBBOZTVYEKVKBLNULVAPUGBEFMYDRAPSOH"

# آدرس API روبیکا (تغییر نده)
API_URL = f"https://messengerg2c4.iranlms.ir/"

# حافظه کوتاه برای چت
memory = {}

def send_message(chat_id, text):
    payload = {
        "method": "sendMessage",
        "chat_id": chat_id,
        "text": text,
    }
    requests.post(API_URL, json=payload)

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        msg = data["message"]
        chat_id = msg["chat_id"]
        text = msg.get("text", "")

        user_id = str(chat_id)
        if user_id not in memory:
            memory[user_id] = []

        memory[user_id].append(text)
        if len(memory[user_id]) > 5:
            memory[user_id] = memory[user_id][-5:]  # محدودیت حافظه

        # پاسخ هوش مصنوعی ساده
        response = ai_response(text)

        send_message(chat_id, response)

    return "ok"

def ai_response(text):
    if "سلام" in text:
        return "سلام! خوش اومدی 🌟"
    elif "چطوری" in text:
        return "من خوبم! تو چطوری؟ 😊"
    elif "خداحافظ" in text:
        return "فعلاً! هر وقت خواستی برگرد 🌈"
    else:
        return f"تو گفتی: {text}؟ جالبه! 🤔"

if __name__ == "__main__":
    app.run()
