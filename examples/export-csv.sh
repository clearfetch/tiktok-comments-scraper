#!/usr/bin/env bash
# Export a video's comments straight to a CSV file. Use format=xlsx for Excel, and fields=... to pick columns.
curl -X POST "https://api.apify.com/v2/acts/clearfetch~tiktok-comments-scraper/run-sync-get-dataset-items?token=$APIFY_TOKEN&format=csv" \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://www.tiktok.com/@tiktok/video/7106594312292453675"], "maxCommentsPerVideo": 500}' \
  -o comments.csv
