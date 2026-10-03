# TikTok Comments Scraper - Comments & Replies from Any Video

Paste TikTok video links and get every comment as a clean row: the text, likes, when it was posted, who wrote it,
the language, whether the creator pinned or liked it, and, if you want them, the full reply threads.
**$0.40 per 1,000 comments.** No login, no cookies, no proxy.

## What data you get

Per comment or reply:

- `text`, `likes`, `replyCount`, `createdAt`, and TikTok's detected `language`
- **Reply threads**: every reply is its own row with `parentCommentId`, so a flat CSV still rebuilds the
  conversation
- **Creator signals**: `pinnedByAuthor` and `likedByAuthor`, the comments the creator chose to pin or like
- **Commerce signals**: `taggedProducts` (TikTok Shop products tagged in the comment) and `purchaseIntent`,
  TikTok's own flag for a comment that reads like someone wanting to buy
- `mentions`, `hashtags`, and `imageUrls` for comments posted as pictures
- Author: `authorUsername`, `authorNickname`, `authorId`, `authorProfileUrl`, `authorAvatarUrl`
- The video: `videoId`, `videoUrl`, and the comment count TikTok shows for it

Every row has the same columns, so exports to CSV, Excel or Google Sheets stay tidy.

## How to use

1. Paste video links into **TikTok video links**, one per line. Share links (`vm.tiktok.com/...`,
   `tiktok.com/t/...`), photo posts and bare video ids work too.
2. Choose how many comments per video, and whether to include replies.
3. Run it, then download the rows as JSON, CSV or Excel, or pull them through the API.

## Input

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `urls` | array | — | TikTok video links or ids. Also accepts `postURLs`, `videoUrls`, `url` and `startUrls`. |
| `maxCommentsPerVideo` | integer | `100` | Top-level comments per video. `0` means all of them. |
| `includeReplies` | boolean | `false` | Also collect replies, each as its own row. |
| `maxRepliesPerComment` | integer | `20` | Replies per comment when replies are on. `0` means all. |
| `onlyNew` | boolean | `false` | For scheduled runs: write and charge only comments posted since the newest one an earlier run delivered for the same video. |
| `stateStoreName` | string | `tiktok-comments-scraper-state` | The key-value store that remembers what earlier runs delivered, for `onlyNew`. One name per schedule. |
| `includeRaw` | boolean | `false` | Add TikTok's untouched comment object as `raw`. |
| `maxConcurrency` | integer | `3` | Videos worked on in parallel. |
| `timeoutSecs` | integer | `30` | Per-request timeout. Slow requests are retried. |
| `proxyConfiguration` | object | off | Not needed. Available for very large volumes. |

## Output example

One row from a real run, with the commenter's identity replaced by placeholders:

```json
{
  "ok": true,
  "commentId": "7680437555809010439",
  "videoId": "7680396878776700174",
  "videoUrl": "https://www.tiktok.com/@seansvv/video/7680396878776700174",
  "text": "whatever, they never tell us what rule we're breaking anyways",
  "createdAt": "2026-09-01T05:40:35.000Z",
  "likes": 519,
  "replyCount": 6,
  "isReply": false,
  "parentCommentId": null,
  "replyToCommentId": null,
  "language": "en",
  "pinnedByAuthor": false,
  "likedByAuthor": true,
  "purchaseIntent": false,
  "mentions": [],
  "hashtags": [],
  "taggedProducts": [],
  "imageUrls": [],
  "authorUsername": "example_user",
  "authorNickname": "Example User",
  "authorId": "6820000000000000000",
  "authorSecUid": "MS4wLjABAAAA...",
  "authorProfileUrl": "https://www.tiktok.com/@example_user",
  "authorAvatarUrl": "https://p16-common-sign.tiktokcdn-eu.com/...",
  "videoCommentCount": 1215,
  "inputUrl": "https://www.tiktok.com/@seansvv/video/7680396878776700174",
  "scrapedAt": "2026-09-19T13:52:56.157Z"
}
```

A video that cannot be read comes back as one row with `ok: false` and a plain reason, such as
`video not found or not public` or `the creator has turned comments off for this video`. Those rows are free.

## Pricing

- **$0.0004 per comment or reply**, which is $0.40 per 1,000. The 50 comments in the example input cost two
  cents.
- You pay only for comments written to your dataset. Videos that fail, links that are not TikTok videos, and
  duplicates are never charged (see the FAQ).
- Set a maximum cost on the run and it stops cleanly when it gets there.

Paid Apify plans pay less: 10% off on Bronze, 20% on Silver and 30% on Gold and higher tiers.

Apify also charges a run-start fee of $0.00005 per started GB of allocated memory (minimum one event), including runs that produce no chargeable results.

## Use cases

- **Brand and campaign monitoring**: what people say under your videos, your competitors' and your creators'.
- **Influencer vetting**: whether an audience is real people talking or bots, and whether the creator engages.
- **Product research for TikTok Shop**: comments with tagged products and purchase intent show demand in the
  audience's own words.
- **Sentiment and topic analysis**: clean text with a language code, ready for an LLM or a classifier.
- **Giveaways and contests**: every entry in the comments, with timestamps and profile links.
- **Community management**: find the questions under a viral video that still have no reply.

## Integrations

```bash
curl -X POST "https://api.apify.com/v2/acts/clearfetch~tiktok-comments-scraper/run-sync-get-dataset-items?token=YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://www.tiktok.com/@tiktok/video/7106594312292453675"], "maxCommentsPerVideo": 200}'
```

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_TOKEN")
run = client.actor("clearfetch/tiktok-comments-scraper").call(
    run_input={"urls": ["https://www.tiktok.com/@tiktok/video/7106594312292453675"], "includeReplies": True}
)

for c in client.dataset(run["defaultDatasetId"]).iterate_items():
    if c["ok"]:
        print(c["likes"], c["authorUsername"], c["text"][:80])
```

Works with the Apify integrations for n8n, Make, Zapier, Google Sheets, Slack and webhooks, with scheduled runs,
and with AI agents through the Apify MCP server.

## FAQ

**Why do I get fewer comments than TikTok shows?** The number under a video counts replies too, and it includes
comments TikTok hides from everyone: filtered, deleted, or restricted. On a video showing 1,215, this Actor
collected 673 comments and 310 replies, which is everything TikTok would serve.

**What does "duplicates are never charged" mean?** TikTok's comment pages overlap: its ranking shifts while you
page through, so the same comment can come back again later. On that same video, 109 of the first 782 comments
TikTok returned were repeats. This Actor drops them before they reach your dataset, so you do not pay for them.

**Do I need a proxy?** No. TikTok serves comments to Apify's own servers. The proxy option is there for very large
volumes, if you start seeing rate-limit errors.

**Can I monitor a video and get only the new comments?** Yes. Schedule the Actor with `onlyNew` on: the first run
returns everything, and each later run writes and charges only comments posted after the newest one already
delivered for that video. TikTok orders comments by popularity rather than date, so a new comment can sit anywhere
in the list; set the maximum per video to `0` (all) or a high number on monitoring runs so it is found.

**How large a video can one run handle?** Measured on Apify's default settings: 9,469 comments in 89 seconds,
about 100 a second, so 20,000 comments take about four minutes. If a video is too large for the run's time limit,
the run stops a minute before it and ends as succeeded with everything read so far; raise the run timeout for the
very largest videos.

**Can it find videos by hashtag, keyword or profile?** No. It takes video links. If you already have a list of
videos from another tool or a spreadsheet, paste it in.

**Do image links keep working?** For a few weeks. TikTok signs comment image links with an expiry date, so download
the images you need to keep.

**Is this legal?** It reads public comments that anyone can see without an account, and it does not log in or use
cookies. Comments contain usernames, which are personal data under laws such as the GDPR, so you are responsible
for having a lawful reason to process them and for storing them appropriately.

## More tools from clearfetch

- [TikTok Scraper](https://apify.com/clearfetch/tiktok-scraper): hashtags, profiles, sounds and video stats in one Actor
- [TikTok Profile Scraper](https://apify.com/clearfetch/tiktok-profile-scraper): followers, likes and the latest videos of any account
- [TikTok Video Scraper](https://apify.com/clearfetch/tiktok-video-scraper): full stats for any video link
- [Google Trends Scraper](https://apify.com/clearfetch/google-trends-scraper): interest over time, by region and related queries, plus today's trending searches

## Changelog

- **1.1.0** (2026-10-02) — `onlyNew` for scheduled monitoring; comments are written a page at a time, about eight
  times faster on large videos (9,469 comments in 89 s, where 10,003 took 751 s); a run stops cleanly before its
  time limit instead of timing out.
- **1.0.0** (2026-09) — first release: comments and replies by video link or id, share-link resolution, reply
  threading, creator pin and like flags, tagged products, purchase intent, image comments, duplicate removal,
  plain-language reasons for videos that cannot be read.
