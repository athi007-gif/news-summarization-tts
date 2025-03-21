from fastapi import FastAPI, HTTPException
from utils import scrape_news, analyze_sentiment, text_to_speech_hindi

app = FastAPI()

@app.get("/scrape/")
def scrape(url: str):
    headlines = scrape_news(url)
    if not headlines:
        return {"error": "No headlines found"}
    return {"headlines": headlines}

@app.post("/sentiment/")
def sentiment(data: dict):
    text = data.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")
    return analyze_sentiment(text)

@app.post("/tts/")
def tts(data: dict):
    text = data.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")
    audio_path = text_to_speech_hindi(text)
    with open(audio_path, "rb") as audio:
        return audio.read()
