import os
import json
import random
from requests_oauthlib import OAuth1Session

import azapi

from load_env import load_environment_variables

class TweetAPI:
    api_key = api_secret = access_key = access_secret = None
    auth = None

    def init_auth(
        self, 
        api_key, 
        api_secret, 
        access_key, 
        access_secret
    ):
        creds = [access_key, access_secret, api_key, api_key]

        if None in creds:
            raise Exception("Missing conditional key/s")

        self.api_key = api_key
        self.api_secret = api_secret
        self.access_key = access_key
        self.access_secret = access_secret

        self.auth = OAuth1Session(
            client_key=self.api_key,
            client_secret=self.api_secret,
            resource_owner_key=access_key,
            resource_owner_secret=access_secret,
        )

    def create_tweet(
        self,
        content,
    ):
        if self.auth is None:
            raise Exception("Auth not initiated")

        create_tweet_api_url = "https://api.twitter.com/2/tweets"
        payload = {"text": content}

        response = self.auth.post(
            url=create_tweet_api_url,
            json=payload,
        )
        
        if response.status_code != 201:
            raise Exception(
                "Request returned an error: {} {}".format(response.status_code, response.text)
            )

        return response.json()

    def get_random_song(
        self,
    ):
        with open('sinatracks.json') as json_file:
            titles = json.load(json_file)

        random_title = random.choice(titles)

        API = azapi.AZlyrics('google', accuracy=0.5)

        API.artist = 'Frank Sinatra'
        API.title = random_title

        lyrics = API.getLyrics()
        lyrics_list = lyrics.split('\n')\

        filtered_lyrics = list(filter((lambda x: len(x) > 0), lyrics_list))
        return filtered_lyrics



if __name__ == "__main__":
    load_environment_variables()
    
    api_secret = os.environ['api_secret']
    api_key = os.environ['api_key']
    access_key = os.environ['access_key']
    access_secret = os.environ['access_secret']
    
    tweeapi = TweetAPI(
        # api_secret=api_secret,
        # api_key=api_key,
        # access_key=access_key,
        # access_secret=access_secret
    )

    # res = tweeapi.create_tweet(content="my boo is the best boo")
    res = tweeapi.get_random_song()
    random_lyrics = random.choice(res)
    # tweeapi.create_tweet(content=random_lyrics)

    print(random_lyrics)


