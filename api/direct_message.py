import tweepy
import os

from load_env import load_environment_variables
load_environment_variables()

consumer_secret = os.environ['api_secret']
consumer_key = os.environ['api_key']
access_secret = os.environ['access_secret']
access_token = os.environ['access_key']
bearer = os.environ['bearer']

auth = tweepy.OAuth2BearerHandler(bearer_token=bearer)

api = tweepy.API(auth=auth)
# api.send_direct_message(recipient_id="")

client = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_secret, bearer_token=bearer)

user = client.get_user(username="b_urslf_")

# res = api.get_direct_messages()
res = client.get_users_mentions(id=user.data['id'], expansions="author_id")
print(res)
# client.create_tweet(text="HEY")
