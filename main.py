#!/usr/bin/env python3
"""main module"""

import configparser
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import quote

config = configparser.ConfigParser()
config.read('config.ini')

# Configuration
URL = config.get("scraper", "url")
keywords_str = config.get("scraper", "keywords")

STRINGS = [kw.strip() for kw in keywords_str.split(",")]

USER = config.get("telegram", "username")

TOTAL_REQUESTS = 0


def check_website_for_strings(target_url, strings_to_find, max_attempts=5, cooldown_seconds=10):
    """
    Fetches a website's content and checks for the presence of specific strings.

    Args:
        target_url (str): The URL of the website to check.
        strings_to_find (list): A list of strings to search for in the website's text.
        max_attempts (int): The maximum number of times to try fetching the URL.
        cooldown_seconds (int): The number of seconds to wait between failed attempts.

    Returns:
        dict: A dictionary where keys are the strings and values are booleans indicating if the string was found.
              Returns an empty dictionary on failure after all attempts.
    """
    attempts = 0
    global TOTAL_REQUESTS
    
    while attempts < max_attempts:
        try:
            # Set a user-agent to mimic a real browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(target_url, headers=headers, timeout=15)

            # Raise an exception for bad status codes (4xx or 5xx)
            response.raise_for_status()

            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Get all visible text from the website
            page_text = soup.get_text().lower()

            # Check for the presence of each string
            results = {s: s.lower() in page_text for s in strings_to_find}
            TOTAL_REQUESTS += 1
            print(f"Search complete. ({TOTAL_REQUESTS})")
            return results

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            attempts += 1
            if attempts < max_attempts:
                print(f"Waiting for {cooldown_seconds} seconds before retrying...")
                time.sleep(cooldown_seconds)
            else:
                print("Max attempts reached. Could not fetch the website.")
                return {}
    return {}


def call_user_on_telegram(user={}, keyword=""):
    try:
        parsed_message = f"An apartment was found at {keyword}.".replace(" ", "+")
        
        response = requests.get(f"http://api.callmebot.com/start.php?user={user["username"]}&text={parsed_message}&lang=en-GB-Standard-B&rpt=2")
        response.raise_for_status()
        
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occured while calling user: {e}")
        return False


def send_message_telegram(user={}, keyword=""):
    try:
        message = f"An apartment was found at {keyword}."
        encoded_message = quote(message)
        
        response = requests.get(f"https://api.callmebot.com/text.php?user={user["username"]}&text={encoded_message}")
        response.raise_for_status()
        
        return response.text
    except Exception as e:
        print(f"An error accured while sending a message to the user...\n{e}")
        return "Failed"


if __name__ == "__main__":
    while True:
        found_strings = check_website_for_strings(URL, STRINGS)
        if found_strings:
            for string, found in found_strings.items():
                if found:
                    # Call the user on Telegram
                    page_content = call_user_on_telegram(USER, string)
                    
                    # If calling fails, send a text message instead
                    if isinstance(page_content, bool) or "Script ended before Timeout." in page_content:
                        res = send_message_telegram(USER, string)
                        if "Successful" in res:
                            print("Message sent to the user successfully.")
                            break
                    else:
                        print("User called successfully on Telegram.")
                        break
        else:
            print("Script failed to retrieve and parse the website.")
            
        time.sleep(2)