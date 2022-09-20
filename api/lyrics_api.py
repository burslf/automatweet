import json
import random
import azapi
from playwright.sync_api import sync_playwright

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
            browser = p.chromium.launch(headless=False)
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

    def artist_first_letter(
        self,
        artist
    ):
        return artist[0]

    def format_artist_name(
        self,
        artist_name
    ):
        return "".join(artist_name.split(" ")).lower()

if __name__ == "__main__":
    lyricsapi = LyricsAPI()

    songs = lyricsapi.fetch_titles("lil baby")
    print(songs)