from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)  # Allow frontend requests

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

messages = [{"role": "system", "content": "You are a helpful AI chatbot."}]

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    messages.append({"role": "user", "content": user_message})

    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "https://example.com",
            "X-Title": "DeepSeek Chatbot",
        },
        extra_body={},
        model="deepseek/deepseek-chat-v3-0324:free",
        messages=messages
    )

    bot_reply = completion.choices[0].message.content.strip()
    messages.append({"role": "assistant", "content": bot_reply})

    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
