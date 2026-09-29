#!/usr/bin/env bash
# Run the Actor and print the rows as JSON.
curl -X POST "https://api.apify.com/v2/acts/clearfetch~tiktok-comments-scraper/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://www.tiktok.com/@tiktok/video/7106594312292453675"], "maxCommentsPerVideo": 100}'
