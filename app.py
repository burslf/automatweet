import os
from time import sleep
from api.lyrics_api import get_two_random_lyrics

from api.twitter_api import TweetAPI
from helpers.custom_log import get_logger

logger = get_logger()

def main(event, context):
    creds = {
        'api_key': os.environ.get('api_key'),
        'api_secret': os.environ.get('api_secret'),
        'access_key': os.environ.get('access_key'),
        'access_secret': os.environ.get('access_secret'),
        'bearer': os.environ.get('bearer')
    }

    tweeapi = TweetAPI(creds=creds)

    random_lyrics = get_two_random_lyrics(artist='Lil Baby')
    
    logger.info("TITLE: ", random_lyrics['title'])
    
    formatted_lyrics = '\n'.join(random_lyrics['lyrics'])
    
    logger.info("LYRICS: ", formatted_lyrics)

    tweeapi.create_tweet(
        text=formatted_lyrics
    )
