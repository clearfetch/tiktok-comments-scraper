"""Run on a schedule: after the first run, each run returns only comments posted since the previous one."""
import os

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("clearfetch/tiktok-comments-scraper").call(run_input={
    "urls": ["https://www.tiktok.com/@tiktok/video/7106594312292453675"],
    # TikTok orders comments by popularity, not date, so read them all to catch every new one.
    "maxCommentsPerVideo": 0,
    "onlyNew": True,
    # One name per schedule keeps two schedules on the same video apart.
    "stateStoreName": "brand-monitoring",
})

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item["createdAt"], item["likes"], item["text"])
