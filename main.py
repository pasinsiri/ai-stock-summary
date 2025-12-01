#!/usr/bin/env python3
"""
CNBC Stock Sentiment Analyzer
Run daily via GitHub Actions or locally for testing.
"""

import argparse
from collections import defaultdict
import time
import sys

# Local imports
from app.sitemap import get_recent_articles_with_tickers
from app.scraper import scrape_article
from app.analyzer import analyze_article
from app.aggregator import generate_insights
from app.reporter import render_dashboard, send_discord


def main():
    parser = argparse.ArgumentParser(description="CNBC Stock Sentiment Analyzer")
    parser.add_argument(
        "-n", "--num-articles",
        type=int,
        default=50,
        help="Number of recent articles to process (default: 50, use 3-10 for quick testing)"
    )
    parser.add_argument(
        "--no-discord",
        action="store_true",
        help="Skip sending to Discord (useful for local testing)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch and scrape only (skip OpenAI calls) – fastest test"
    )

    args = parser.parse_args()

    if args.num_articles < 1:
        print("Error: --num-articles must be >= 1")
        sys.exit(1)

    print(f"Starting CNBC Sentiment Analysis – processing {args.num_articles} article(s)")

    # 1. Fetch article URLs
    print("Fetching articles with official tickers...")
    articles = get_recent_articles_with_tickers(max_articles=args.num_articles * 2)
    articles = articles[:args.num_articles]  # Limit exactly

    ticker_data = defaultdict(list)

    for i, article in enumerate(articles, 1):
        url = article["url"]
        # official_tickers = article["tickers"]
        official_tickers = sorted([t for t in article["tickers"] if t[0] != '.']) # ? filter only stocks
        title = article["title"]

        print(f"[{i}/{len(articles)}] {title}")
        print(f"   → Official tickers: {', '.join(official_tickers)}")

        try:
            # Scrape content for AI summary
            page_title, content = scrape_article(url)

            if args.dry_run:
                score = 3
                summary = "Dry-run: no AI call"
            else:
                print("Calling analyze_article")
                result = analyze_article(page_title or title, content)
                score = result.get("sentiment_score", 3)
                summary = result.get("summary", "")

            # Use ONLY official tickers from sitemap
            for ticker in official_tickers:
                ticker_data[ticker].append({
                    "score": score,
                    "summary": summary,
                    "url": url,
                    "title": title
                })

            time.sleep(0.8)
        except Exception as e:
            print(f"   → Failed: {e}")

    if not ticker_data:
        print("No ticker data collected.")
        return

    # 2. Generate insights
    print("Generating AI-powered insights per ticker...")
    insights = generate_insights(ticker_data)

    # 3. Output
    render_dashboard(insights, len(articles))
    print("Dashboard saved → output/dashboard.html")

    if not args.no_discord and not args.dry_run:
        try:
            send_discord(insights, len(articles))
            print("Report sent to Discord!")
        except Exception as e:
            print(f"Discord failed: {e}")
    else:
        print("Discord notification skipped (use --no-discord or --dry-run to suppress)")

    print("All done!")


if __name__ == "__main__":
    main()