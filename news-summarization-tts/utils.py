import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import re
from gtts import gTTS
from translate import Translator  # Import the translate library

def scrape_news(company_name):
    search_url = f"https://www.bing.com/news/search?q={company_name}&FORM=HDRSC6"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("a", {"class": "title"}, limit=10)
    news_data = []
    for article in articles:
        title = article.text
        link = article["href"]
        summary = fetch_article_summary(link)
        news_data.append({"title": title, "summary": summary, "url": link})
    return news_data

def fetch_article_summary(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        content = " ".join([p.text for p in paragraphs[:5]])
        return re.sub(r"\s+", " ", content.strip())
    except:
        return "Summary unavailable."

def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

def compare_sentiments(news_list):
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for news in news_list:
        sentiment_counts[news["sentiment"]] += 1
    return sentiment_counts

def text_to_speech_hindi(text, filename="output.mp3"):
    try:
        translator = Translator(to_lang="hi")  # Initialize the translator
        translated_text = translator.translate(text)  # Translate the text

        if translated_text == text:
            translated_text = "अनुवाद विफल रहा। कृपया पुनः प्रयास करें।"

        tts = gTTS(translated_text, lang="hi")
        tts.save(filename)
        return filename
    except Exception as e:
        print("❌ Translation Error:", e)
        return "Translation failed."