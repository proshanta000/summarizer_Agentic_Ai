from langchain_groq import ChatGroq

class GroqModel:
    def __init__(self, api_key: str, model_name: str):
        self.api_key = api_key
        self.model_name = model_name

    def get_model(self):
        """Returns the initialized LLM instance."""
        return ChatGroq(
            groq_api_key=self.api_key, 
            model_name=self.model_name
        )