import re

from bs4 import BeautifulSoup


def clean_tweets(tweet):
    tweet = BeautifulSoup(tweet, "lxml").get_text()
    tweet = re.sub(r"@[A-Za-z0-9]+", " ", tweet)
    tweet = re.sub(r"https?://[A-Za-z0-9./]+", " ", tweet)
    tweet = re.sub(r"[^a-zA-Z.!?]", " ", tweet)
    tweet = re.sub(r" +", " ", tweet)
    return tweet


def clean_tweets2(tweet, nlp):
    tweet = tweet.lower()
    # document = nlp(tweet)
    # words = []
    # for token in document:
    #     words.append(token.text)

    # words = [word for word in words]
    # words = ' '.join([str(element) for element in words])

    return tweet
    # return words
