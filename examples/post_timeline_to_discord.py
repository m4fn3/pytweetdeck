import pytweetdeck
import json
import requests

# config
webhook_url = "YOUR_WEBHOOK_URL_HERE"
client = pytweetdeck.Client(name_or_email="USERNAME", password="PASSWORD")

# get timeline tweets
for tweets in client.stream_timeline():
    for tweet in tweets:
        content = tweet["text"]
        # replace media url
        if "media" in tweet["entities"]:
            for media in tweet["extended_entities"]["media"]:
                content = content.replace(media["url"], media["media_url"])
        body = {
            "username": tweet["user"]["screen_name"],
            "avatar_url": tweet["user"]["profile_image_url"],
            "content": content
        }
        # send webhook
        requests.post(
            webhook_url, json.dumps(body),
            headers={"Content-Type": "application/json"}
        )
