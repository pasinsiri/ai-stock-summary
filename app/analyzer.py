import openai
import json
from config.settings import OPENAI_API_KEY, MODEL

openai.api_key = OPENAI_API_KEY

def analyze_article(title, content):
    prompt = f'''
Title: {title}
Content: {content}

Return valid JSON with:
- "summary": 2-3 sentence summary
- "sentiment_score": int 1-5 (1=very negative, 5=very positive)
- "mentioned_tickers": list of tickers mentioned

Only JSON, no markdown.
'''

    try:
        resp = openai.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500
        )
        raw = resp.choices[0].message.content.strip()
        if "```" in raw:
            raw = raw.split("```")[1].replace("json", "").strip()
        return json.loads(raw)
    except Exception as e:
        print(f"AI Error: {e}")
        return {"summary": content[:200], "sentiment_score": 3, "mentioned_tickers": []}