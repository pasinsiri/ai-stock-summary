from jinja2 import Environment, FileSystemLoader
from discord_webhook import DiscordWebhook
import os
from config.settings import DISCORD_WEBHOOK_URL

def render_dashboard(results, total_articles):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('dashboard.html')
    html = template.render(results=results, total_articles=total_articles, now=__import__('datetime').datetime.now())
    
    os.makedirs("output", exist_ok=True)
    with open("output/dashboard.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Dashboard → output/dashboard.html")

def send_discord(results, total_articles):
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL, rate_limit_retry=True)
    embed = {
        "title": "CNBC Stock Sentiment Report",
        "description": f"Analyzed {total_articles} articles",
        "color": 0x00ff88,
        "fields": []
    }
    for r in results[:10]:
        emoji = "Positive" if r['score'] >= 4 else "Warning" if r['score'] >= 3 else "Negative"
        embed["fields"].append({
            "name": f"{emoji} {r['ticker']} • {r['score']}/5 ({r['count']} articles)",
            "value": r['insight'][:250] + "..." if len(r['insight']) > 250 else r['insight']
        })
    webhook.add_embed(embed)
    webhook.execute()