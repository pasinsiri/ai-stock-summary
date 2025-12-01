import openai
from config.settings import MODEL
import time

def generate_insights(ticker_data):
    results = []
    for ticker, items in ticker_data.items():
        if not items:
            continue
        print(f"Parsing {ticker} to AI")
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
                # temperature=1, # for gpt-5-nano, temperature is forced to 1
                temperature=0.5,
                # max_completion_tokens=500 # for gpt-5-nano, use max_completion_tokens
                max_tokens=300 # for gpt-4o-mini, use max_tokens
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