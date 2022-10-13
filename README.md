# pytweetdeck
Wrapper library of TweetDeck's internal api.

You can handle twitter functions without consumer key/secret since pytweetdeck uses an internal api which is used in TweetDeck.

## Install
```
pip install pytweetdeck
```
or directly from GitHub
```
pip install git+https://github.com/m4fn3/pytweetdeck.git
```
## Quick Example
Check examples directory to find more.
```python
import pytweetdeck
# login
client = pytweetdeck.Client(name_or_email="USERNAME", password="PASSWORD")
# tweet text
client.send_tweet("Hello from pytweetdeck!")
# stream timeline tweet
for tweet in client.stream_timeline():
    print(tweet)
```

