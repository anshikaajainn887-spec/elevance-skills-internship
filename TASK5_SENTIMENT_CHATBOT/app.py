from flask import Flask, render_template, request, jsonify
from chatbot import analyze_sentiment

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    result = analyze_sentiment(user_message)

    return jsonify({
        "user_message": user_message,
        "sentiment": result["sentiment"],
        "confidence": result["confidence"],
        "bot_response": result["response"]
    })

if __name__ == "__main__":
    app.run(debug=True)