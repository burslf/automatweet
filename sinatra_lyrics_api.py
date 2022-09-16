from random import random
import requests
from playwright.sync_api import sync_playwright
import json
import random


class SinatraLyrics:
    active_session = None

    def fetch_titles(
        self,
    ):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            page.goto("https://www.azlyrics.com/f/franksinatra.html", wait_until='commit')
            
            all_songs_title_html = page.locator('div.listalbum-item')

            
            response = []
            
            for i in range(all_songs_title_html.count()):
                response.append(all_songs_title_html.nth(i).text_content())
        
            page.wait_for_load_state(state='domcontentloaded')            

            
            browser.close()

            return response

if __name__ == "__main__":
    sina = SinatraLyrics()
    titles = sina.fetch_titles()
    print(titles)