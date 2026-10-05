import os
from dotenv import load_dotenv

def load_config():
    # Load .env file
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    load_dotenv(env_path)

    # Provider and model config with defaults
    return {
        "AI_PROVIDER": os.environ.get("AI_PROVIDER", "openai"),
        "AI_MODEL": os.environ.get("AI_MODEL", "gpt-5.6-sol"),
        "AI_BATCH_SIZE": int(os.environ.get("AI_BATCH_SIZE", "10")),
        "GEMINI_API_KEY": os.environ.get("GEMINI_API_KEY", ""),
        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
        "GROQ_API_KEY": os.environ.get("GROQ_API_KEY", "")
    }

CONFIG = load_config()
