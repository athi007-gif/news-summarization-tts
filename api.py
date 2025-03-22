from fastapi import FastAPI
from pydantic import BaseModel
from utils import scrape_news, analyze_sentiment, compare_sentiments, text_to_speech_hindi

app = FastAPI()

# Request Model for TTS
class TTSRequest(BaseModel):
    text: str

# ✅ Fetch News API Endpoint
@app.get("/news/{company}")
def get_news(company: str):
    news_articles = scrape_news(company)
    if not news_articles:
        return {"error": "No news articles found."}
    
    for news in news_articles:
        news["sentiment"] = analyze_sentiment(news["summary"])
    
    sentiment_summary = compare_sentiments(news_articles)
    
    return {"articles": news_articles, "sentiment_summary": sentiment_summary}

# ✅ Text-to-Speech API Endpoint
@app.post("/tts/")
def generate_tts(request: TTSRequest):
    audio_file = text_to_speech_hindi(request.text)
    return {"audio_file": audio_file}
