import os
import json
import random
from requests_oauthlib import OAuth1Session
from TwitterAPI import TwitterAPI

import azapi

from load_env import load_environment_variables


class TweetAPI:
    api_key = api_secret = access_key = access_secret = None
    api = None
    # base_api_url = "https://api.twitter.com/2"

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

        self.api =  TwitterAPI(
            access_token_key=os.environ['access_key'],
            access_token_secret=os.environ['access_secret'],
            consumer_key=os.environ['api_key'],
            consumer_secret=os.environ['api_secret'],
        )


    def create_tweet(
        self,
        content,
    ):
        if self.auth is None:
            raise Exception("Auth not initiated")

        create_tweet_api_url = f"{self.base_api_url}/tweets"

        payload = {"text": content}

        response = self.auth.post(
            url=create_tweet_api_url,
            json=payload,
        )

        if response.status_code != 201:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text)
            )

        return response.json()

    def get_mentions(
        self,
        username
    ):
        user_id = self.get_user_id(
            username=username
        )

        metions_api_url = f"{self.base_api_url}/users/{user_id}/mentions"

        params = {"expansions": 'author_id'}

        mentions_response = self.auth.get(
            url=metions_api_url,
            params=params
        )

        if not mentions_response.ok:
            raise Exception("ERUR")

        return mentions_response.json()

    def get_user_id(
        self,
        username,
    ):
        if self.auth is None:
            raise Exception("Auth not initiated")

        user_info_url = f"{self.base_api_url}/users/by/username/{username}"

        infos_response = self.auth.get(
            url=user_info_url,
        )

        if not infos_response.ok:
            raise Exception("ERUR")

        user_info = infos_response.json()

        user_id = user_info["data"]["id"]

        return user_id


    def send_dm(
        self,
        username,
    ):
        user_id = self.get_user_id(
            username=username
        )
        payload = {
            'event': {
                'type': 'message_create',
                'message_create': {
                    'target': {
                        'recipient_id': f'{user_id}'
                    },
                    'message_data': {
                        'text': 'Hello World!'
                    }
                }
            }
        }

        response = self.auth.post(
            url=f'https://api.twitter.com/1.1/direct_messages/events/new.json',
            json=payload,
        )

        print(response)
        # if response.status_code != 201:
        #     raise Exception(
        #         "Request returned an error: {} {}".format(
        #             response.status_code, response.text)
        #     )

        # return response.json()

        


if __name__ == "__main__":
    load_environment_variables()

    api_secret = os.environ['api_secret']
    api_key = os.environ['api_key']
    access_key = os.environ['access_key']
    access_secret = os.environ['access_secret']

    tweeapi = TweetAPI()

    tweeapi.init_auth(
        api_secret=api_secret,
        api_key=api_key,
        access_key=access_key,
        access_secret=access_secret
    )

    # res = tweeapi.get_mentions(username="0xgrind")
    res = tweeapi.send_dm('b_urslf_')
    print(res)

    # res = tweeapi.create_tweet(content="my boo is the best boo")
    # res = tweeapi.get_random_song()
    # random_lyrics = random.choice(res)
    # tweeapi.create_tweet(content=random_lyrics)

    # print(random_lyrics)
