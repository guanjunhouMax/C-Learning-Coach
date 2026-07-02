import os

# OpenAI & API config (use env vars in production via Render Dashboard)
API_KEY = os.environ.get("API_KEY", "")
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-3.5-turbo")
APP_NAME = os.environ.get("APP_NAME", "C语言学习小教练")
APP_DESCRIPTION = os.environ.get("APP_DESCRIPTION", "基于大语言模型的C语言编程学习助手")

DEBUG = os.environ.get("DEBUG", "False").lower() == "true"
SECRET_KEY = os.environ.get("SECRET_KEY", "c_code_coach_2026")
USE_LOCAL_MODE = os.environ.get("USE_LOCAL_MODE", "True").lower() == "true"
MAX_HISTORY = int(os.environ.get("MAX_HISTORY", "20"))