from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("xai-4nQHNO8S9hxzF9K8hL8fZ7HJ84nXyUe6sm7r0P54Cr5ftzYnD449WIIqCCQuxDWnr6B7swlzKXNJ5fwA")

app = Flask(__name__)
history = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")
    history.append({"role": "user", "content": user_msg})

    resp = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=history
    )
    bot_msg = resp.choices[0].message.content
    history.append({"role": "assistant", "content": bot_msg})

    return jsonify({"reply": bot_msg})

if __name__ == "__main__":
    app.run(debug=True)