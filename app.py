from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
import logging

app = Flask(__name__, static_folder='static',
            template_folder='templates')
CORS(app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
history = []

API_URL = "https://router.huggingface.co/v1/chat/completions"
HF_TOKEN = os.getenv("HF_TOKEN")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_msg = request.json.get("message")
        if not user_msg:
            return jsonify({"reply": "메시지를 입력해주세요."}), 400

        if not HF_TOKEN:
            logger.error("HF_TOKEN 환경 변수가 설정되지 않음")
            return jsonify({"reply": "⚠️ API 키 설정 오류. 관리자에게 연락하세요."}), 500

        history.append(f"User: {user_msg}")
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        prompt = "\n".join(history[-10:]) + "\nAssistant:"

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 150,
                "temperature": 0.7,
                "return_full_text": False
            }
        }

        logger.info(f"API 호출: {user_msg[:50]}")
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 503:
            bot_msg = "모델 로딩 중입니다. 10초 후 다시 시도해주세요."
        elif response.status_code != 200:
            logger.error(f"API 오류 {response.status_code}: {response.text}")
            bot_msg = f"⚠️ API 오류 ({response.status_code}). 잠시 후 다시 시도해주세요."
        else:
            result = response.json()
            if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
                bot_msg = result[0]["generated_text"].strip()
                history.append(f"Assistant: {bot_msg}")
            else:
                logger.error(f"예상 외 응답: {result}")
                bot_msg = "응답 형식 오류. 잠시 후 다시 시도해주세요."
                
    except requests.exceptions.Timeout:
        logger.error("API 타임아웃")
        bot_msg = "응답 시간 초과. 잠시 후 다시 시도해주세요."
    except Exception as e:
        logger.error(f"예외 발생: {str(e)}", exc_info=True)
        bot_msg = f"오류 발생: {str(e)}"

    return jsonify({"reply": bot_msg})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
