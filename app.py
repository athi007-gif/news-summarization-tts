import streamlit as st
from utils import scrape_news, analyze_sentiment, compare_sentiments, text_to_speech_hindi
import uvicorn

st.title("📢 News Sentiment & Hindi Speech Generator")

company = st.text_input("Enter a company name:", "Reliance")

if st.button("Fetch News"):
    with st.spinner("Fetching news..."):
        articles = scrape_news(company)
        for news in articles:
            news["sentiment"] = analyze_sentiment(news["summary"])
        sentiment_summary = compare_sentiments(articles)

        st.subheader("📰 News Articles & Sentiments")
        for news in articles:
            st.markdown(f"### [{news['title']}]({news['url']})")
            st.write(f"**Summary:** {news['summary']}")
            st.write(f"**Sentiment:** {news['sentiment']}")
            st.write("---")

        st.subheader("📊 Sentiment Analysis Summary")
        st.write(sentiment_summary)

        if articles:
            text_to_convert = " ".join([news["summary"] for news in articles[:3]])
            audio_file = text_to_speech_hindi(text_to_convert, filename="static/output.mp3")

            if audio_file == "static/output.mp3":
                st.audio("static/output.mp3")
            else:
                st.error("TTS generation failed.")
        else:
            st.error("Failed to fetch news. Try again later.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)