#!/usr/bin/env python3
"""main module"""


import requests
from bs4 import BeautifulSoup
import time
import pprint

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
    while attempts < max_attempts:
        try:
            print(f"Attempt {attempts + 1} of {max_attempts}: Fetching {target_url}...")
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
            print("Search complete.")
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

# --- Example Usage ---
if __name__ == "__main__":

    while True:
        URL = "https://trouverunlogement.lescrous.fr/tools/41/search?bounds=3.8070597_43.6533542_3.9413208_43.5667088"

        STRINGS = ["CITE COLOMBIERE",
                "RESIDENCE MINERVE",
                "RESIDENCE DU POUS DE LAS SERS",
                "CITE VOIE DOMITIENNE",
                "CITE VERT BOIS",
                "RESIDENCE LA LYRE",
                "CITE TRIOLET"]
        
        found_strings = check_website_for_strings(URL, STRINGS)

        if found_strings:
            print("\n--- Search Results ---")
            for string, found in found_strings.items():
                print(f"'{string}': {'Found' if found else 'Not Found'}")
            print("--------------------")
        else:
            print("Script failed to retrieve and parse the website.")