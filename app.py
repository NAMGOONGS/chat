from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# xAI API 설정
XAI_API_KEY = os.getenv("XAI_API_KEY")
API_URL = "https://api.x.ai/v1/chat/completions"
MODEL = "grok-beta"  # 또는 grok-2, grok-3 등

app = Flask(__name__)
history = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")
    if not user_msg:
        return jsonify({"reply": "메시지를 입력해주세요."}), 400

    history.append({"role": "user", "content": user_msg})

    headers = {
        "Authorization": f"Bearer {XAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": history,
        "temperature": 0.7
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        bot_msg = data["choices"][0]["message"]["content"]
        history.append({"role": "assistant", "content": bot_msg})
    except Exception as e:
        bot_msg = f"오류: {str(e)}"

    return jsonify({"reply": bot_msg})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)