# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Azure OpenAI Configuration
AZURE_ENDPOINT = os.environ.get("ENDPOINT_URL")
API_KEY = os.environ.get("AZURE_OPENAI_KEY")
API_VERSION = "2023-07-01-preview"

# OpenAI Model Deployment
DEPLOYMENT = os.environ.get('DEPLOYMENT_NAME')