import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import re
import random
from gtts import gTTS
from googletrans import Translator

# Random User-Agents to Avoid Blocking
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
]

# ✅ News Scraping Function
def scrape_news(company_name):
    search_url = f"https://www.bing.com/news/search?q={company_name}&FORM=HDRSC6"
    headers = {"User-Agent": random.choice(USER_AGENTS)}

    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Error: Bing returned status code {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("a", {"class": "title"}, limit=10)  # Check if this tag is still valid!

    news_data = []
    for article in articles:
        title = article.text
        link = article["href"]
        summary = fetch_article_summary(link)
        news_data.append({"title": title, "summary": summary, "url": link})

    return news_data

# ✅ Fetch Article Summary
def fetch_article_summary(url):
    try:
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        content = " ".join([p.text for p in paragraphs[:5]])
        return re.sub(r"\s+", " ", content.strip())
    except requests.exceptions.RequestException as e:
        print("❌ Error fetching article:", e)
        return "Summary unavailable."

# ✅ Sentiment Analysis
def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# ✅ Comparative Sentiment Analysis
def compare_sentiments(news_list):
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for news in news_list:
        sentiment_counts[news["sentiment"]] += 1
    return sentiment_counts

#
