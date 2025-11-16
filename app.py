from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder='src')  # src 폴더를 정적 파일로 설정
history = []

API_URL = "https://router.huggingface.co/hf-inference/models/meta-llama/Meta-Llama-3.1-8B-Instruct"
HF_TOKEN = os.getenv("HF_TOKEN")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")
    if not user_msg:
        return jsonify({"reply": "메시지를 입력해주세요."}), 400

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

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 503:
            bot_msg = "모델 로딩 중입니다. 10초 후 다시 시도해주세요."
        elif response.status_code != 200:
            bot_msg = f"오류 {response.status_code}: {response.text}"
        else:
            result = response.json()
            bot_msg = result[0]["generated_text"].strip() if isinstance(result, list) else "응답 오류"
            history.append(f"Assistant: {bot_msg}")
    except Exception as e:
        bot_msg = f"연결 오류: {str(e)}"

    return jsonify({"reply": bot_msg})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)