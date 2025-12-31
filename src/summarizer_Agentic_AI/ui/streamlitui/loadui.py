import os
import streamlit as st
from src.summarizer_Agentic_AI.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        """
        Initialize the UI loader by reading the configuration file
        and preparing the dictionary to store user inputs.
        """
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
        # 1. Page Configuration and Title Setup
        try:
            # Dynamically set the browser tab title from the config file
            st.set_page_config(page_title="📄 " + self.config.get_page_title(), layout="wide")
        except st.errors.StreamlitAPIException:
            # Prevents errors if set_page_config is called multiple times during rerun
            pass

        # Main Page Header
        st.header("📄 " + self.config.get_page_title())

        # 2. Sidebar Section: Model and API Key Configuration
        with st.sidebar:
            st.markdown("## ⚙️ Configuration Settings")
            llm_options = self.config.get_llm_options()

            # LLM Provider Selection (e.g., Groq, Gemini)
            st.markdown("### 🤖 LLM Selection")
            self.user_controls['selected_llm'] = st.selectbox("Select LLM", llm_options)

            # --- Dynamic Model & API Key Handling ---
            # Logic for Groq Selection
            if self.user_controls['selected_llm'] == "Groq":
                model_options = self.config.get_groq_model_options()
                self.user_controls['selected_groq_model'] = st.selectbox("Select Model", model_options)

                # Use session_state to persist the API key across page refreshes
                save_groq_key = st.session_state.get("GROQ_API_KEY", "")
                groq_key = st.text_input("Groq API Key", type="password", value=save_groq_key)

                self.user_controls["GROQ_API_KEY"] = groq_key
                st.session_state["GROQ_API_KEY"] = groq_key

                if not groq_key:
                    st.warning("⚠️ Enter GROQ API Key. If You don't have one: [Get it here](https://console.groq.com/keys)")
            
            # Logic for Gemini Selection
            elif self.user_controls["selected_llm"] == "Gemini":
                model_options = self.config.get_gemini_model_options()
                self.user_controls["selected_gemini_model"] = st.selectbox("Select Model", model_options)
                
                saved_gemini_key = st.session_state.get("GEMINI_API_KEY", "")
                gemini_key = st.text_input("Gemini API Key", type="password", value=saved_gemini_key)
                
                self.user_controls["GEMINI_API_KEY"] = gemini_key
                st.session_state["GEMINI_API_KEY"] = gemini_key

                if not gemini_key:
                    st.warning("⚠️ Enter Gemini API Key. If You don't have one: [Get it here](https://aistudio.google.com/api-keys)")

            st.divider()
            
            # 3. Action Buttons
            # Allows user to reset the conversation state
            if st.button("🗑️ Clear Chat History"):
                if "chat_history" in st.session_state:
                    st.session_state.chat_history = []
                st.rerun()

        # 4. Validation Gate: Verify if an API Key is present before allowing data input
        # This prevents the user from uploading docs if the agent cannot process them yet
        current_llm = self.user_controls.get('selected_llm')
        has_key = False
        
        if current_llm == "Groq":
            has_key = bool(st.session_state.get("GROQ_API_KEY"))
        elif current_llm == "Gemini":
            has_key = bool(st.session_state.get("GEMINI_API_KEY"))

        # 5. Data Source Section (Locked until API Key is provided)
        st.divider()
        
        # Radio button to toggle between local files and web links
        input_type = st.radio(
            "Select Data Source", 
            ["Direct PDF Upload", "Website Link"], 
            horizontal=True,
            disabled=not has_key  # Gray out if no key is entered
        )
        self.user_controls['input_type'] = input_type

        # Visual indicator explaining why the section might be disabled
        if not has_key:
            st.info("ℹ️ Please provide an API Key in the sidebar to enable file upload or website input.")

        # --- Conditional Input Rendering ---
        if input_type == "Direct PDF Upload":
            # File uploader restricted to .pdf only
            self.user_controls['uploaded_file'] = st.file_uploader(
                "Upload your PDF document", 
                type=["pdf"], 
                disabled=not has_key
            )
        else:
            # Text input for web scraping links (blogs, news, etc.)
            self.user_controls['web_url'] = st.text_input(
                "Enter Website URL", 
                placeholder="https://example.com/article-to-summarize",
                disabled=not has_key,
                help="Paste a link to a blog post, news article, or any public webpage."
            )

        # Return all collected UI data to the main execution script
        return self.user_controls