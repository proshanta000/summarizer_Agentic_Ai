from langchain_google_genai import ChatGoogleGenerativeAI

class GeminiModel:
    def __init__(self, api_key: str, model_name: str):
        self.llm = ChatGoogleGenerativeAI(google_api_key=api_key, model=model_name)

    def get_model(self):
        return self.llm