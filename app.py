from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()
XAI_API_KEY = os.getenv("XAI_API_KEY")
API_URL = "https://api.x.ai/v1/chat/completions"

app = Flask(__name__)
history = [{"role": "system", "content": "You are a helpful assistant."}]  # 시스템 프롬프트 고정

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")
    if not user_msg:
        return jsonify({"reply": "메시지를 입력해주세요."}), 400

    # 사용자 메시지 추가
    history.append({"role": "user", "content": user_msg})

    headers = {
        "Authorization": f"Bearer {XAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "grok-4-latest",  # 최신 모델
        "messages": history,
        "temperature": 0.7,
        "stream": False
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        bot_msg = data["choices"][0]["message"]["content"]
        history.append({"role": "assistant", "content": bot_msg})
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            bot_msg = "API 키 오류 (403): console.x.ai에서 새 키를 생성하고 활성화하세요."
        else:
            bot_msg = f"HTTP 오류: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        bot_msg = f"오류: {str(e)}"

    return jsonify({"reply": bot_msg})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

