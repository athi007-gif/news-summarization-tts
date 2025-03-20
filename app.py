import requests

# Update this with your Hugging Face Space URL
API_URL = "https://athihari-news-summarization-tts.hf.space"

def fetch_news_summary(company):
    try:
        response = requests.get(f"{API_URL}/news/{company}")
        
        # Print response details for debugging
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)  # Check if it's valid JSON

        if response.status_code == 200:
            try:
                data = response.json()  # Ensure it's valid JSON
                return data
            except requests.exceptions.JSONDecodeError:
                print("Error: API did not return valid JSON.")
                return {"error": "Invalid JSON response from API"}
        else:
            return {"error": f"API returned status code {response.status_code}"}

    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}

# Example call
if __name__ == "__main__":
    company = "Reliance"
    result = fetch_news_summary(company)
    print("Result:", result)
