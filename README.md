# AI Stock Summary

An automated stock sentiment analysis tool that scrapes recent CNBC articles, analyzes their sentiment using OpenAI's GPT models, and generates ticker-specific insights with visual dashboards.

## Features

- **Automated Article Fetching**: Retrieves recent articles from CNBC's sitemap with official stock ticker associations
- **AI-Powered Sentiment Analysis**: Uses OpenAI GPT models to analyze article sentiment on a 1-5 scale
- **Ticker-Specific Insights**: Aggregates multiple article sentiments per ticker and generates comprehensive insights
- **Visual Dashboard**: Generates HTML dashboard with sentiment scores and key themes
- **Discord Integration**: Optionally sends summary reports to Discord webhooks
- **Flexible CLI**: Command-line arguments for testing and customization

## Prerequisites

- Python 3.11 or higher
- OpenAI API key
- Discord webhook URL (optional, for notifications)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/pasinsiri/ai-stock-summary.git
cd ai-stock-summary
```

2. Install dependencies using uv (recommended) or pip:
```bash
# Using uv
uv sync

# Or using pip
pip install -r requirements.txt
```

3. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

4. Add your API keys to `.env`:
```env
OPENAI_API_KEY=your_openai_api_key_here
DISCORD_WEBHOOK_URL=your_discord_webhook_url_here  # optional
```

## Usage

### Basic Usage

Run the analyzer with default settings (50 articles):
```bash
python main.py
```

### Command-Line Arguments

- `-n, --num-articles`: Number of articles to process (default: 50)
- `--no-discord`: Skip Discord notification
- `--dry-run`: Fetch and scrape only, skip OpenAI API calls (fastest test)

### Examples

Process 10 articles for quick testing:
```bash
python main.py -n 10
```

Process 30 articles without Discord notification:
```bash
python main.py -n 30 --no-discord
```

Dry run to test scraping without API costs:
```bash
python main.py -n 5 --dry-run
```

## How It Works

1. **Article Fetching** ([sitemap.py](app/sitemap.py)): Retrieves recent articles from CNBC's sitemap XML with official stock tickers
2. **Content Scraping** ([scraper.py](app/scraper.py)): Extracts article content from CNBC pages
3. **Sentiment Analysis** ([analyzer.py](app/analyzer.py)): Sends article content to OpenAI GPT for sentiment scoring (1-5) and summarization
4. **Aggregation** ([aggregator.py](app/aggregator.py)): Groups articles by ticker and generates AI-powered insights for each stock
5. **Reporting** ([reporter.py](app/reporter.py)): Creates HTML dashboard and sends Discord notifications

## Output

- **HTML Dashboard**: Saved to `output/dashboard.html` with sentiment scores and insights per ticker
- **Discord Notification**: Optional summary sent to configured webhook
- **Console Logs**: Detailed progress logs during execution

## Project Structure

```
ai-stock-summary/
├── app/
│   ├── aggregator.py    # Ticker-level insight generation
│   ├── analyzer.py      # Article sentiment analysis
│   ├── reporter.py      # Dashboard and Discord reporting
│   ├── scraper.py       # Article content extraction
│   ├── sitemap.py       # CNBC sitemap parsing
│   └── utils.py         # Utility functions
├── config/
│   └── settings.py      # Configuration and environment variables
├── templates/
│   └── dashboard.html   # HTML template for dashboard
├── output/              # Generated dashboards
├── logs/                # Application logs
├── main.py              # Main entry point
├── requirements.txt     # Python dependencies
└── pyproject.toml       # Project metadata
```

## Configuration

Edit [config/settings.py](config/settings.py) to customize:

- `MODEL`: OpenAI model to use (default: "gpt-4o-mini")
- `MAX_ARTICLES`: Default maximum articles to process
- `USER_AGENT`: User agent string for web requests

## Development

### Running Tests

For quick testing, use dry-run mode:
```bash
python main.py -n 3 --dry-run
```

### Adding Features

The project is modular:
- Add new data sources in `app/sitemap.py`
- Modify sentiment analysis in `app/analyzer.py`
- Customize reporting in `app/reporter.py`

## GitHub Actions

This project can be configured to run automatically via GitHub Actions. Create a workflow file in `.github/workflows/` to schedule daily runs.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Author

Pasin Sirirat

## Disclaimer

This tool is for informational purposes only. Stock sentiment analysis should not be the sole basis for investment decisions. Always do your own research and consult with financial advisors.
