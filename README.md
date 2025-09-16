# Apartment Scraper & Telegram Notifier

This Python script automates the process of finding an apartment by scraping a specified website for listings, checking for keywords you care about, and instantly notifying you on Telegram. To ensure you see the notification as soon as possible, it first attempts to call you on Telegram and then sends a message as a fallback.

## Description

Searching for the perfect apartment can be a tedious process of constantly checking websites for new listings. This script streamlines that process by:

1.  **Scraping**: Regularly fetching the latest apartment listings from a target website.
2.  **Keyword Matching**: Filtering the listings based on a user-defined list of keywords (e.g., "city name", "dorm_name", "balcony," "gym," "pet-friendly").
3.  **Instant Notification**:
    *   **Telegram Call**: Attempts to place a VoIP call to your Telegram account for high-priority notifications.
    *   **Telegram Message**: If the call fails or is not answered, it sends a detailed message with the apartment listing information.

This ensures you are among the first to see listings that match your criteria, giving you a competitive edge in your apartment hunt.

## Features

*   **Targeted Scraping**: Easily configurable to scrape the apartment listing website of your choice.
*   **Customizable Keywords**: Define a list of keywords to match against apartment descriptions.
*   **Dual Notification System**: Prioritizes a Telegram call for immediate attention, with a reliable message fallback.
*   **Prevents Duplicate Notifications**: Keeps track of already-notified listings to avoid spamming you with the same apartment.

## Requirements

*   Python 3.7+
*   A Telegram account

You will also need to authenticate the Telegram bot for sending calls and sending messages.
**Whitelist your Telegram account by following the link: https://api2.callmebot.com/txt/auth.php**

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/AbdeljalilOuafi/Get_dat_Apartment.git
    cd Get_dat_Apartment/
    ```

2.  **Install the required Python libraries:**
    ```bash
    pip install -r requirements.txt
    ```
## Usage

1.  **Configure the script:**
    Open the `config.ini` file and fill in your details:
    *   Telegram `username`
    *   The URL of the apartment website you want to scrape.
    *   Your desired keywords.

2.  **Run the script:**
    ```bash
    python main.py
    ```

The script will now run in the background, checking for new apartments and notifying you when a match is found.

## Disclaimer

This script is for personal use. Please be responsible and respect the terms of service of the website you are scraping. Making too many requests in a short period can lead to your IP address being blocked.