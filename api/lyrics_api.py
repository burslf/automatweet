import random
import azapi
from playwright.sync_api import sync_playwright
from helpers.s3 import add_json_file_to_s3, get_s3_json_file

from helpers.utils import get_random_lyrics_index, remove_empty_lines

class LyricsAPI:

    def fetch_titles(
        self,
        artist
    ):  

        first_letter = self.artist_first_letter(
            artist=artist
        )

        formatted_artist_name = self.format_artist_name(
            artist_name=artist
        )

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()

            artist_page_url = f"https://www.azlyrics.com/{first_letter}/{formatted_artist_name}.html"

            page.goto(artist_page_url, wait_until='commit')
            
            page.wait_for_selector('div.listalbum-item')
            all_songs_title_html = page.locator('div.listalbum-item')

            
            response = []
            
            for i in range(all_songs_title_html.count()):
                response.append(all_songs_title_html.nth(i).text_content())
        
            page.wait_for_load_state(state='domcontentloaded')            

            
            browser.close()
            
            return response


    def get_random_song(
        self,
        artist
    ):
        formatted_artist = self.format_artist_name(artist)
                
        titles = get_s3_json_file(bucket_name='songs-lyrics', file_name=f'{formatted_artist}.json')
        
        if not titles:
            titles = self.fetch_titles(
                artist=artist
            )   
            add_json_file_to_s3(bucket_name='songs-lyrics', file_name=formatted_artist, json_data=titles)

        random_title = random.choice(titles)

        API = azapi.AZlyrics('google', accuracy=0.5)

        API.artist = artist
        API.title = random_title

        lyrics = API.getLyrics()
        lyrics_list = lyrics.split('\n')

        filtered_lyrics = remove_empty_lines(lyrics_list)

        return {
            'title': random_title,
            'lyrics': filtered_lyrics
        }

    def artist_first_letter(
        self,
        artist
    ):
        return artist[0].lower()

    def format_artist_name(
        self,
        artist_name
    ):
        return "".join(artist_name.split(" ")).lower()

def get_two_random_lyrics(
    artist
):
    lyricsapi = LyricsAPI()
    
    song = lyricsapi.get_random_song(artist=artist)
    
    index = get_random_lyrics_index(song['lyrics'])

    two_lines_lyrics = song['lyrics'][index:index+2]
    
    return {
        'title': song['title'],
        'lyrics': two_lines_lyrics
    }
