from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
MODEL = "gpt-4o-mini"  # or "gpt-4o" for best quality
MAX_ARTICLES = 50
USER_AGENT = "Mozilla/5.0 (SentimentBot/1.0)"