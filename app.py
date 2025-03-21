import streamlit as st
import requests

# Hugging Face API Endpoint
API_URL = "https://huggingface.co/spaces/athihari/news-summarization-tts/api"

st.title("📰 News Summarization & Hindi TTS")

news_url = st.text_input("🔗 Enter News URL")

if st.button("Fetch & Summarize"):
    if news_url:
        with st.spinner("⏳ Fetching news..."):
            response = requests.get(f"{API_URL}/scrape/", params={"url": news_url})
            if response.status_code == 200:
                data = response.json()
                if "error" in data or not data["headlines"]:
                    st.error("⚠️ No headlines found. Try a different URL.")
                else:
                    st.subheader("📌 Top Headlines")
                    for headline in data["headlines"]:
                        st.write(f"- {headline}")

                    # Sentiment Analysis
                    with st.spinner("🔍 Performing Sentiment Analysis..."):
                        sentiment_res = requests.post(f"{API_URL}/sentiment/", json={"text": data["headlines"]})
                        sentiments = sentiment_res.json()
                        st.write("📊 **Sentiment:**", sentiments)

                    # Generate Hindi TTS
                    with st.spinner("🔊 Generating Hindi Speech..."):
                        tts_res = requests.post(f"{API_URL}/tts/", json={"text": data["headlines"][0]})
                        if tts_res.status_code == 200:
                            st.audio(tts_res.content, format="audio/wav")
                        else:
                            st.error("⚠️ Error generating speech.")
            else:
                st.error("❌ Failed to fetch news.")
    else:
        st.warning("⚠️ Please enter a valid news URL.")
