import sys
import os

# Ensure the 'src' directory is discoverable by Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import run_app

if __name__ == "__main__":
    # Launch the application 
    run_app()
