import gradio as gr
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from gtts import gTTS

# Load pre-trained models
summarizer = pipeline("summarization")
sentiment_analyzer = pipeline("sentiment-analysis")

# Function to fetch news content
def fetch_news(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)
        soup = BeautifulSoup(response.text, "html.parser")
        
        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text() for p in paragraphs])

        return text[:2000] if text else "No content found."
    except requests.exceptions.RequestException as e:
        return f"Error fetching news: {e}"

# Function to summarize news
def summarize_news(url):
    article_text = fetch_news(url)
    if "Error" in article_text or "No content" in article_text:
        return article_text  # Return error message
    
    summary = summarizer(article_text, max_length=150, min_length=50, do_sample=False)[0]['summary_text']
    return summary

# Function to analyze sentiment
def analyze_sentiment(text):
    sentiment = sentiment_analyzer(text)[0]
    return sentiment['label'], round(sentiment['score'], 2)

# Function to generate Hindi speech
def text_to_speech(text):
    tts = gTTS(text=text, lang="hi")
    audio_path = "output.mp3"
    tts.save(audio_path)
    return audio_path

# API Function
def process_news(url):
    summary = summarize_news(url)
    if "Error" in summary or "No content" in summary:
        return summary, "N/A", "N/A", None  # Return error without crashing
    
    sentiment_label, sentiment_score = analyze_sentiment(summary)
    audio_path = text_to_speech(summary)
    
    return summary, sentiment_label, sentiment_score, audio_path

# Gradio Interface
iface = gr.Interface(
    fn=process_news,
    inputs=gr.Textbox(label="Enter News URL"),
    outputs=[
        gr.Textbox(label="Summarized News"),
        gr.Textbox(label="Sentiment Label"),
        gr.Textbox(label="Sentiment Score"),
        gr.Audio(label="Hindi Speech Output")
    ]
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)
