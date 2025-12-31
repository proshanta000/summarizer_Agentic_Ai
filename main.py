import streamlit as st
from src.summarizer_Agentic_AI.ui.streamlitui.loadui import LoadStreamlitUI
from src.summarizer_Agentic_AI.graphs.graph import GraphBuilder

class SummarizerApp:
    def __init__(self):
        self.ui = LoadStreamlitUI()

    def run(self):
        user_controls = self.ui.load_streamlit_ui()
        
        if st.button("Start AI Analysis"):
            # Prepare state
            initial_state = {
                "input_type": user_controls['input_type'],
                "file_data": user_controls.get('uploaded_file'),
                "web_url": user_controls.get('web_url'),
                "selected_llm": user_controls['selected_llm'],
                "api_key": st.session_state.get(f"{user_controls['selected_llm'].upper()}_API_KEY"),
                "model_name": user_controls.get(f'selected_{user_controls["selected_llm"].lower()}_model'),
                "documents": [],
                "title": "",
                "summary": "",
                "messages": [],
                "error": None
            }

            # Build and Execute
            builder = GraphBuilder(model=None) # Nodes resolve LLM internally in this version
            graph = builder.setup_graph()
            
            with st.spinner("Agent is processing..."):
                result = graph.invoke(initial_state)

            if result.get("error"):
                st.error(result["error"])
            else:
                st.subheader(f"📌 {result['title']}")
                st.markdown(result['summary'])

def run_app():
    app = SummarizerApp()
    app.run()

if __name__ == "__main__":
    run_app()