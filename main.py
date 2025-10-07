# This file serves as a simple entry point for deployment platforms like Render.
# It imports the actual FastAPI application from app.main.

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app
