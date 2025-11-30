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
    print("Fetching recent articles from sitemap...")
    try:
        urls = get_recent_articles(max_articles=args.num_articles * 3)  # fetch extra in case of skips
        urls = urls[:args.num_articles]
    except Exception as e:
        print(f"Failed to fetch sitemap: {e}")
        sys.exit(1)

    if not urls:
        print("No articles found!")
        sys.exit(0)

    print(f"Processing {len(urls)} articles...")

    ticker_data = defaultdict(list)

    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] {url}")
        try:
            title, content, tickers = scrape_article(url)
            if not tickers:
                print("   → No tickers found, skipping")
                continue

            if args.dry_run:
                # Fake neutral result for fastest testing
                score = 3
                summary = "Dry-run mode – no AI call"
                ai_tickers = tickers[:3]
            else:
                result = analyze_article(title, content)
                score = result.get("sentiment_score", 3)
                summary = result.get("summary", "")
                # ai_tickers = result.get("mentioned_tickers", [])

            # Combine heuristic + AI tickers
            # for t in set(tickers + ai_tickers):
            for t in set(tickers):
                ticker_data[t].append({"score": score, "summary": summary})

            time.sleep(0.8)  # Be respectful
        except Exception as e:
            print(f"   → Error: {e}")

    if not ticker_data:
        print("No ticker data collected.")
        return

    # 2. Generate insights
    print("Generating AI-powered insights per ticker...")
    insights = generate_insights(ticker_data)

    # 3. Output
    render_dashboard(insights, len(urls))
    print("Dashboard saved → output/dashboard.html")

    if not args.no_discord and not args.dry_run:
        try:
            send_discord(insights, len(urls))
            print("Report sent to Discord!")
        except Exception as e:
            print(f"Discord failed: {e}")
    else:
        print("Discord notification skipped (use --no-discord or --dry-run to suppress)")

    print("All done!")


if __name__ == "__main__":
    main()