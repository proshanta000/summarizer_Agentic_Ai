import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader, UnstructuredURLLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

class AgentNodes:
    def __init__(self):
        """Initializes constant configurations like headers."""
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }

    def _get_llm_instance(self, state):
        """Internal helper to resolve the model based on user selection."""
        if state['selected_llm'] == "Groq":
            from src.summarizer_Agentic_AI.llm.groqllm import GroqModel
            return GroqModel(state['api_key'], state['model_name']).get_model()
        else:
            from src.summarizer_Agentic_AI.llm.geminillm import GeminiModel
            return GeminiModel(state['api_key'], state['model_name']).get_model()

    def data_loader_node(self, state: dict):
        """Loads PDFs or URLs and extracts a topic title."""
        try:
            docs = []
            if state['input_type'] == "Direct PDF Upload":
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(state['file_data'].getvalue())
                    tmp_path = tmp.name
                loader = PyPDFLoader(tmp_path)
                docs = loader.load()
                os.remove(tmp_path)
            else:
                loader = UnstructuredURLLoader(urls=[state['web_url']], headers=self.headers)
                docs = loader.load()

            # Generate a Topic Title using the LLM
            
            llm = self._get_llm_instance(state)
            sample = docs[0].page_content[:1000] if docs else ""

            title_prompt = PromptTemplate.from_template(
                """You are a professional editor. I am going to provide a snippet of text from a document. 
                Your task is to identify the singular main subject of the text.
                
                Rules:
                - Provide a short title (maximum 5 words).
                - Ignore any lists of languages or translations.
                - Provide the title ONLY in English.
                - Do not explain yourself.
                
                Text snippet: {text}
                
                Title:"""
            )

            title = (title_prompt | llm | StrOutputParser()).invoke({"text": sample})

            return {"documents": docs, "title": title.strip()}
        except Exception as e:
            return {"error": str(e)}

    def summarizer_node(self, state: dict):
        """Generates the 300-word summary."""
        if state.get("error"): return state
        
        llm = self._get_llm_instance(state)
        text = "\n".join([d.page_content for d in state['documents']])
        prompt = PromptTemplate.from_template("Summarize in 300 words or less: {text}")
        
        summary = (prompt | llm | StrOutputParser()).invoke({"text": text})
        return {"summary": summary}