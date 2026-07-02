import os

# API Configuration (use environment variables in production)
# Default provider: DeepSeek (free tier available, excellent for coding, accessible from China)
API_KEY = os.environ.get("API_KEY", "")
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.deepseek.com/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "deepseek-chat")

# Application settings
APP_NAME = os.environ.get("APP_NAME", "C语言学习小教练")
APP_DESCRIPTION = os.environ.get("APP_DESCRIPTION", "基于AI大模型的C语言智能学习助手")

# Production / Debug
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"
SECRET_KEY = os.environ.get("SECRET_KEY", "c_code_coach_2026")

# Model parameters
TEMPERATURE = float(os.environ.get("TEMPERATURE", "0.7"))
MAX_TOKENS = int(os.environ.get("MAX_TOKENS", "4096"))
MAX_HISTORY = int(os.environ.get("MAX_HISTORY", "30"))

# Suggest follow-up questions after each answer
ENABLE_SUGGESTIONS = os.environ.get("ENABLE_SUGGESTIONS", "True").lower() == "true"

# Preset: switch to OpenAI with env API_OPENAI_KEY
# For other providers, change API_BASE_URL:
# - DeepSeek:   https://api.deepseek.com/v1
# - OpenAI:     https://api.openai.com/v1
# - Moonshot:   https://api.moonshot.cn/v1
# - Yi (01.AI): https://api.01.ai/v1
# - Qwen:       https://dashscope.aliyuncs.com/compatible-mode/v1