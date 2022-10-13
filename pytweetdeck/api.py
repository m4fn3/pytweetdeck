import requests
import time
from lxml.html import fromstring
import json


class Client:
    def __init__(self, auth: dict = None, name_or_email: str = None, password: str = None):
        self.session = requests.Session()
        self.session.headers.update({
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs=1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        })
        if auth:
            self.auth = auth
            self.session.headers.update(auth)
        elif name_or_email and password:
            self.login(name_or_email, password)
        else:
            raise RuntimeError("Either auth or name/email+password is required to login.")

    def login(self, name_or_email: str, password: str):
        login_session = requests.Session()
        resp = login_session.get("https://twitter.com/account/begin_password_reset")
        auth_token = fromstring(resp.text).xpath("//input[@name='authenticity_token']/@value")[0]
        headers = {
            'cookie': '_mb_tk=' + auth_token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'
        }
        data = {
            'session[username_or_email]': name_or_email,
            'session[password]': password,
            'remember_me': '0',
            'return_to_ssl': 'true',
            'redirect_after_login': 'https://tweetdeck.twitter.com/?via_twitter_login=true',
            'authenticity_token': auth_token
        }
        login_session.post('https://twitter.com/sessions', headers=headers, data=data)
        cookie = login_session.cookies.get_dict()
        if "auth_token" not in cookie or "ct0" not in cookie:
            raise RuntimeError("Failed to login to the account. username/password may be incorrect.")
        self.auth = {
            'x-csrf-token': cookie["ct0"],
            'cookie': f'auth_token={cookie["auth_token"]}; '
                      f'ct0={cookie["ct0"]}',
        }
        self.session.headers.update(self.auth)

    def dump_auth(self) -> None:
        print(json.dumps(self.auth, indent=2))

    def get_timeline(self, count) -> dict:
        resp = self.session.get(
            "https://api.twitter.com/1.1/statuses/home_timeline.json",
            params={
                "count": count
            }
        )
        return resp.json()

    def stream_timeline(self) -> dict:
        resp = self.session.get("https://api.twitter.com/1.1/statuses/home_timeline.json?count=1")
        last_tweet = resp.json()[0]["id"]
        while True:
            try:
                resp = self.session.get(
                    "https://api.twitter.com/1.1/statuses/home_timeline.json",
                    params={
                        "count": 40,
                        "since_id": last_tweet
                    }
                )
                data = resp.json()
                if data:
                    last_tweet = data[0]["id"]
                yield data
                time.sleep(4)
            except requests.exceptions.ConnectionError:
                print("Connection aborted! Retrying...")

    def follow_user(self, screen_name: str, type_: bool = True) -> bool:
        url = "https://api.twitter.com/1.1/friendships/" + ("create.json" if type_ else "destroy.json")
        resp = self.session.post(
            url,
            data={"screen_name": screen_name}
        )
        return False if "errors" in resp.json() else True

    def favorite_tweet(self, tweet_id: int, type_: bool = True) -> bool:
        url = "https://api.twitter.com/1.1/favorites/" + ("create.json" if type_ else "destroy.json")
        resp = self.session.post(
            url,
            data={"id": tweet_id}
        )
        return False if "errors" in resp.json() else True

    def send_tweet(self, text: str) -> bool:
        resp = self.session.post(
            "https://api.twitter.com/1.1/statuses/update.json",
            data={"status": text}
        )
        return False if "errors" in resp.json() else True

    def delete_tweet(self, tweet_id: int) -> bool:
        resp = self.session.post(
            f"https://api.twitter.com/1.1/statuses/destroy/{tweet_id}.json"
        )
        return False if "errors" in resp.json() else True
