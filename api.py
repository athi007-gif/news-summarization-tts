from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/news/{company}")
def get_news(company: str):
    try:
        # Simulating API call (Replace with real logic)
        news_summary = {"company": company, "summary": "Sample summarized news"}
        
        print("API Response:", news_summary)  # Debugging print
        return news_summary
    except Exception as e:
        print("API Error:", str(e))
        return {"error": "Failed to fetch news"}
