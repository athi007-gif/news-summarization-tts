import streamlit as st
import requests

# ✅ Update API URL
API_URL = "https://athihari-news-summarization-tts.hf.space"

st.title("📢 News Summarization & Hindi TTS")

company = st.text_input("Enter a company name:", "Reliance")

if st.button("Fetch & Summarize"):
    with st.spinner("Fetching news..."):
        try:
            response = requests.get(f"{API_URL}/news/{company}")
            
            if response.status_code == 200:
                try:
                    data = response.json()  # Ensure response is valid JSON
                except requests.exceptions.JSONDecodeError:
                    st.error("Received an invalid response from the server. Please try again later.")
                    st.stop()

                if "error" in data or "articles" not in data:
                    st.error("No news articles found.")
                else:
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
                        
                        tts_response = requests.post(f"{API_URL}/tts/", json={"text": text_to_convert})

                        if tts_response.status_code == 200:
                            try:
                                with open("output.mp3", "wb") as f:
                                    f.write(tts_response.content)
                                st.audio("output.mp3")
                            except Exception as e:
                                st.error(f"Error saving TTS output: {e}")
                        else:
                            st.error("TTS generation failed.")
            else:
                st.error(f"Failed to fetch news. HTTP Status: {response.status_code}")

        except requests.exceptions.RequestException as e:
            st.error(f"Network error: {e}")
