import os
from pathlib import Path
import logging



logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

project_name = "pdf_summarizer_Agentic_AI"

list_of_files =[
    ".git/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/llm/__init__.py",
    f"src/{project_name}/llm/geminillm.py",
    f"src/{project_name}/llm/groqllm.py",
    f"src/{project_name}/graphs/__init__.py",
    f"src/{project_name}/graphs/graph.py",
    f"src/{project_name}/nodes/__init__.py",
    f"src/{project_name}/nodes/node.py",
    f"src/{project_name}/states/state.py",
    f"src/{project_name}/ui/__init__.py",
    f"src/{project_name}/ui/uiconfigfile.ini",
    f"src/{project_name}/ui/uiconfigfile.py",
    f"src/{project_name}/ui/streamlitui/loadui.py",
    f"src/{project_name}/ui/streamlitui/display_result.py",
    "main.py",
    "setup.py",
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    # Create directory if it doesn't exist
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file: {filename}")

    # FIXED: Use 'filepath' instead of 'filename' to check existence correctly
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass  # Create an empty file
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")