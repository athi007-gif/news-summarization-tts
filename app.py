import streamlit as st
import requests

API_URL = "https://huggingface.co/spaces/athihari/news-summarization-tts"

st.title("📢 News Summarization & Hindi TTS")

company = st.text_input("Enter a company name:", "Reliance")

if st.button("Fetch & Summarize"):
    with st.spinner("Fetching news..."):
        response = requests.get(f"{API_URL}/news/{company}")
        
        if response.status_code == 200:
            data = response.json()
            articles = data["articles"]
            sentiment_summary = data["sentiment_summary"]

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
                tts_response = requests.get(f"{API_URL}/tts/?text={text_to_convert}")

                if tts_response.status_code == 200:
                    st.audio("output.mp3")
                else:
                    st.error("TTS generation failed.")
        else:
            st.error("Failed to fetch news. Try again later.")
