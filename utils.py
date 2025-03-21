import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import googletrans
from gtts import gTTS

def scrape_news(url):
    """Scrapes news headlines from the given URL."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        headlines = [h.get_text(strip=True) for h in soup.find_all("h2")]
        if not headlines:
            headlines = [h.get_text(strip=True) for h in soup.find_all("h3")]

        return headlines if headlines else None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return None

def analyze_sentiment(text):
    """Performs sentiment analysis."""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

def text_to_speech_hindi(text):
    """Generates Hindi speech from text."""
    translator = googletrans.Translator()
    hindi_text = translator.translate(text, dest="hi").text
    tts = gTTS(hindi_text, lang="hi")
    file_path = "output.mp3"
    tts.save(file_path)
    return file_path
