"""Run the Actor with the Apify client and print a few fields per row."""
import os

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("clearfetch/tiktok-comments-scraper").call(run_input={"urls": ["https://www.tiktok.com/@tiktok/video/7106594312292453675"], "maxCommentsPerVideo": 100})

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item.get("createdAt"), item.get("likes"), item.get("text"))
