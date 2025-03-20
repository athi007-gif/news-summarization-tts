import requests

API_URL = "https://athihari-news-summarization-tts.hf.space/run"  # Change this based on actual API

def fetch_news_summary(company):
    try:
        response = requests.post(API_URL, json={"news_url": f"https://news.com/{company}"})
        
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)  # Debugging print
        
        if response.status_code == 200:
            try:
                data = response.json()
                return data
            except requests.exceptions.JSONDecodeError:
                print("Error: API did not return valid JSON.")
                return {"error": "Invalid JSON response from API"}
        else:
            return {"error": f"API returned status code {response.status_code}"}

    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}

if __name__ == "__main__":
    company = "Reliance"
    result = fetch_news_summary(company)
    print("Final Result:", result)
