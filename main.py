from app.sitemap import get_recent_articles
from app.scraper import scrape_article
from app.analyzer import analyze_article
from app.aggregator import generate_insights
from app.reporter import render_dashboard, send_discord
from collections import defaultdict
import time

def main():
    print("Fetching latest CNBC articles...")
    urls = get_recent_articles(max_articles=50)

    ticker_data = defaultdict(list)

    for i, url in enumerate(urls):
        print(f"[{i+1}/{len(urls)}] {url}")
        try:
            title, content, tickers = scrape_article(url)
            if not tickers:
                continue
            result = analyze_article(title, content)
            score = result.get("sentiment_score", 3)
            summary = result.get("summary", "")
            ai_tickers = result.get("mentioned_tickers", [])

            for t in set(tickers + ai_tickers):
                ticker_data[t].append({"score": score, "summary": summary})
        except Exception as e:
            print(f"Failed: {e}")
        time.sleep(1)

    print("Generating insights...")
    insights = generate_insights(ticker_data)

    render_dashboard(insights, len(urls))
    send_discord(insights, len(urls))
    print("Done!")

if __name__ == "__main__":
    main()