import requests
from playwright.sync_api import sync_playwright
import json


class Twitter:
    active_session = None

    def login_and_tweet(
        self,
        content
    ):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            page.goto("https://twitter.com/i/flow/login")
            login_input_path = 'input[autocomplete="username"]'
            page.wait_for_selector(login_input_path)
            login_input = page.locator(login_input_path)
            login_input.type(
                text="0xgrindin",
            )
            page.wait_for_selector('div[role="button"]')

            next_button = page.locator(
                'div.css-18t94o4.css-1dbjc4n.r-sdzlij.r-1phboty.r-rs99b7.r-ywje51.r-usiww2.r-2yi16.r-1qi8awa.r-1ny4l3l.r-ymttw5.r-o7ynqc.r-6416eg.r-lrvibr.r-13qz1uu').first
            next_button.click()

            print(page.title())

            page.wait_for_load_state(state='domcontentloaded')

            page.wait_for_timeout(timeout=1000)

            verification_input_path = 'input[data-testid="ocfEnterTextTextInput"]'

            if (page.locator(verification_input_path)).count():
                verification_input = page.locator(verification_input_path)

                verification_input.type(
                    text="b_urslf_",
                )

                verif_next_button = page.locator(
                    'div[data-testid="ocfEnterTextNextButton"]').first
                verif_next_button.click()

            page.wait_for_selector('input[autocomplete="current-password"]')
            password_input = page.locator(
                'input[autocomplete="current-password"]')
            password_input.type(
                text="",
            )

            page.locator(
                'div[data-testid="LoginForm_Login_Button"]').first.click()
            page.wait_for_load_state(state='domcontentloaded')
            
            self.scrape_tweet(
                page=page,
                content=content
            )

            browser.close()


    def get_session_from_request(
        self,
        request
    ):
        if "client_event.json" in request.url:
            self.twitter_api_url = request
        if "CreateTweet" in request.url:
            cookies_raw = request.frame.page.context.cookies()
            cookies = {
                element['name']: element['value']
                for element in cookies_raw
            }
            headers_raw = request.all_headers()
            headers = {
                header.replace(':', ''): headers_raw[header]
                for header in headers_raw.keys()
            }

            self.active_session = {
                'cookies': cookies,
                'headers': headers
            }

    def scrape_tweet(
        self, 
        page,
        content,
    ):
        page.on(
            event='request',
            f=self.get_session_from_request,
        )

        tweet_input_path = 'div[contenteditable="true"].notranslate.public-DraftEditor-content'
        page.wait_for_selector(tweet_input_path)

        tweet_input = page.locator(
            selector=tweet_input_path
        )

        tweet_input.type(
            text=content
        )

        page.click(selector='div[data-testid="tweetButtonInline"]')

        page.wait_for_timeout(timeout=2000)


    def tweet_from_session(
        self,
        content,
    ):
        if (self.active_session):
            url = "https://twitter.com/i/api/graphql/kV0jgNRI3ofhHK_G5yhlZg/CreateTweet"
            json_body = {
                "variables": {
                    "media": {
                        "media_entities": [

                        ],
                        "possibly_sensitive": False
                    },
                    "withDownvotePerspective": False,
                    "withReactionsMetadata": False,
                    "withReactionsPerspective": False,
                    "withSuperFollowsTweetFields": True,
                    "withSuperFollowsUserFields": True,
                    "semantic_annotation_ids": [

                    ],
                    "dark_request": False
                },
                "features": {
                    "dont_mention_me_view_api_enabled": True,
                    "responsive_web_uc_gql_enabled": True,
                    "vibe_api_enabled": True,
                    "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": False,
                    "interactive_text_enabled": True,
                    "responsive_web_text_conversations_enabled": False,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": False,
                    "responsive_web_graphql_timeline_navigation_enabled": False,
                    "responsive_web_enhance_cards_enabled": True
                },
                "queryId": "kV0jgNRI3ofhHK_G5yhlZg"
            }
            json_body["variables"]["tweet_text"] = content

            response = requests.post(
                url=url,
                headers=self.active_session['headers'],
                cookies=self.active_session['cookies'],
                json=json_body
            )

            return response.json()
        
        self.scrape_tweet()

    def tweet(
        self,
        content
    ):
        if (self.active_session):
            self.tweet_from_session(content=content)
        else:
            self.login_and_tweet(content=content)


if __name__ == "__main__":
    twitter = Twitter()
    twitter.tweet('hello world')
    # active_session = twitter.active_session
    # if active_session:
    #     print(active_session)
