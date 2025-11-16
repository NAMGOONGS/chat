from flask import Flask, render_template, request, jsonify
from huggingface_hub import InferenceClient
import os

app = Flask(__name__)
history = [{"role": "system", "content": "You are a helpful assistant."}]  # 시스템 프롬프트 추가

# Hugging Face 클라이언트 초기화
client = InferenceClient(
    model="meta-llama/Meta-Llama-3.1-8B-Instruct",
    token=os.getenv("HF_TOKEN")
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")
    if not user_msg:
        return jsonify({"reply": "메시지를 입력해주세요."}), 400

    # 대화 기록에 사용자 메시지 추가
    history.append({"role": "user", "content": user_msg})

    try:
        # 채팅 완성 생성 (OpenAI 호환 형식)
        completion = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-8B-Instruct",
            messages=history[-10:],  # 최근 10개만
            max_tokens=150,
            temperature=0.7
        )
        bot_msg = completion.choices[0].message.content
        history.append({"role": "assistant", "content": bot_msg})
    except Exception as e:
        bot_msg = f"오류: {str(e)} (모델 로딩 중일 수 있음)"

    return jsonify({"reply": bot_msg})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

