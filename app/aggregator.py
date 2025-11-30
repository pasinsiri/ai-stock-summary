import openai
from config.settings import MODEL
import time

def generate_insights(ticker_data):
    results = []
    for ticker, items in ticker_data.items():
        if not items:
            continue
        avg_score = sum(x['score'] for x in items) / len(items)
        summaries = "\n".join([f"- {x['summary']}" for x in items])

        prompt = f'''
Ticker: {ticker}
Average Sentiment: {avg_score:.2f}/5
Recent news:
{summaries}

Write a concise 2-4 sentence professional insight about current sentiment and key themes.
'''

        try:
            resp = openai.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=300
            )
            insight = resp.choices[0].message.content.strip()
        except:
            insight = "Insight generation failed."

        results.append({
            "ticker": ticker,
            "score": round(avg_score, 2),
            "count": len(items),
            "insight": insight
        })
        time.sleep(0.5)
    return sorted(results, key=lambda x: x["score"], reverse=True)