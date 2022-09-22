import os
import tweepy

class TweetAPI:
    api = None
    client = None

    def __init__(
        self,
        creds
    ):
        creds_keys = ['access_key', 'access_secret', 'api_key', 'api_secret', 'bearer']

        for key in creds_keys:
            if key not in creds or creds.get(key) is None:
                raise Exception("Missing conditional key/s")

        auth = tweepy.OAuth2BearerHandler(bearer_token=creds['bearer'])

        self.client = tweepy.Client(
            consumer_key=creds['api_key'], 
            consumer_secret=creds['api_secret'], 
            access_token=creds['access_key'], 
            access_token_secret=creds['access_secret'], 
            bearer_token=creds['bearer']
        )
        
        self.api = tweepy.API(auth=auth)


    def get_user(
        self,
        username,
    ):
        user = self.client.get_user(username=username)
        return user.data

    def get_mentions(
        self,
        username, 
        expantions=None,
    ):
        user = self.get_user(username=username)
        user_id = user['id']
        mentions = self.client.get_users_mentions(id=user_id, expansions=expantions)
        return mentions 

    def create_tweet(
        self,
        text,
    ):
        tweet = self.client.create_tweet(text=text)
        return tweet



if __name__ == "__main__":

    api_key = os.environ['api_key']
    api_secret = os.environ['api_secret']
    access_key = os.environ['access_key']
    access_secret = os.environ['access_secret']
    bearer = os.environ['bearer']
    
    creds = {
        'api_key': None,
        'api_secret': api_secret,
        'access_key': access_key,
        'access_secret': access_secret,
        'bearer': bearer
    }

    tweeapi = TweetAPI(
        creds=creds
    )

    # res = tweeapi.get_mentions(username="0xgrind")
    
    # res = tweeapi.send_dm('b_urslf_')
    # print(res)

    # res = tweeapi.get_random_song()
    # random_lyrics = random.choice(res)
    # tweeapi.create_tweet(content=random_lyrics)

    # res = tweeapi.create_tweet(content="my boo is the best boo")
    # print(random_lyrics)
