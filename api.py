import gradio as gr

def summarize_news(news_url):
    return {"summary": "This is a test summary", "sentiment": "Positive"}

iface = gr.Interface(
    fn=summarize_news,
    inputs=gr.Textbox(label="News URL"),
    outputs=gr.JSON()
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)
