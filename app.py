import streamlit as st
import requests

# Update with your actual Hugging Face Space API URL
API_URL = "https://huggingface.co/spaces/athihari/news-summarization-tts"  

st.title("📢 News Sentiment & Hindi Speech Generator")
st.write("Enter a company name to fetch the latest news and analyze sentiment.")

company = st.text_input("Enter a company name:", "Reliance")

if st.button("Fetch News"):
    try:
        response = requests.get(f"{API_URL}/news/{company}")
        st.write("Response Status Code:", response.status_code)  # Debugging
        st.write("Response Text:", response.text)  # Debugging

        if response.status_code == 200:
            data = response.json()
            st.write("### News Summary:", data.get("summary", "No summary found"))
            st.write("### Sentiment Analysis:", data.get("sentiment", "No sentiment found"))

            # Fetch Hindi Speech
            speech_response = requests.get(f"{API_URL}/tts/{company}")
            if speech_response.status_code == 200:
                st.audio(speech_response.content, format="audio/wav")
            else:
                st.write("Failed to generate speech.")

        else:
            st.error(f"Failed to fetch news. Status Code: {response.status_code}")

    except requests.exceptions.JSONDecodeError:
        st.error("Error: Response is not in JSON format.")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
