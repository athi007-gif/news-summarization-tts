from flask import Flask, jsonify
from utils import fetch_news_summary, analyze_sentiment, generate_hindi_speech

app = Flask(__name__)

@app.route("/news/<company>", methods=["GET"])
def get_news(company):
    try:
        summary = fetch_news_summary(company)
        sentiment = analyze_sentiment(summary)

        return jsonify({
            "company": company,
            "summary": summary,
            "sentiment": sentiment
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/tts/<company>", methods=["GET"])
def get_tts(company):
    try:
        audio_path = generate_hindi_speech(company)
        with open(audio_path, "rb") as f:
            return f.read(), 200, {'Content-Type': 'audio/wav'}
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
