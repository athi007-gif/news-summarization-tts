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
                    data = response.json()
                    
                    if "error" in data:
                        st.error("No news articles found.")
                    else:
                        articles = data.get("articles", [])
                        sentiment_summary = data.get("sentiment_summary", "No sentiment summary available.")
                        
                        st.subheader("📰 News Articles & Sentiments")
                        for news in articles:
                            st.markdown(f"### [{news.get('title', 'No Title')}]({news.get('url', '#')})")
                            st.write(f"**Summary:** {news.get('summary', 'No summary available.')}")
                            st.write(f"**Sentiment:** {news.get('sentiment', 'Unknown')}")
                            st.write("---")
                        
                        st.subheader("📊 Sentiment Analysis Summary")
                        st.write(sentiment_summary)
                        
                        if articles:
                            text_to_convert = " ".join([news.get("summary", "") for news in articles[:3]])  
                            tts_response = requests.post(f"{API_URL}/tts/", json={"text": text_to_convert})
                            
                            if tts_response.status_code == 200:
                                st.audio("output.mp3")
                            else:
                                st.error("TTS generation failed.")
                except requests.exceptions.JSONDecodeError:
                    st.error("Error decoding JSON response. The API might not be returning valid JSON.")
                    st.write("Response Content:", response.text)
            else:
                st.error(f"Failed to fetch news. Status Code: {response.status_code}")
                st.write("Response Content:", response.text)
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred while making the request: {e}")
