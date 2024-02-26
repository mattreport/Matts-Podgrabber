import os
import requests
import feedparser
from tqdm import tqdm
import json
import string

LIBRARY_FILE = 'podcast_library.json'
CONFIG_FILE = 'config.json'

def initialize_config():
    if not os.path.exists(CONFIG_FILE):
        config = {'download_folder': 'podcasts'}
        with open(CONFIG_FILE, 'w') as file:
            json.dump(config, file)
    else:
        with open(CONFIG_FILE) as file:
            config = json.load(file)
    return config['download_folder']

def download_file(url, local_filename):
    headers = {'User-Agent': 'MattsPodGrabber/1.0'}
    with requests.get(url, stream=True, headers=headers) as r:
        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))
        with tqdm(total=total_size, unit='B', unit_scale=True, desc=local_filename) as bar:
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    bar.update(len(chunk))
                    f.write(chunk)
    print(f"Downloaded {local_filename}")

def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, 'r') as file:
            library = json.load(file)
    else:
        library = {}
    return library

def save_to_library(feed_url, title):
    library = load_library()
    library[title] = feed_url
    with open(LIBRARY_FILE, 'w') as file:
        json.dump(library, file, indent=4)
    print("Saved to library.")

def is_feed_in_library(feed_url):
    return feed_url in load_library().values()

def get_user_input(prompt, valid_responses=None):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input == 'q':
            print("Exiting Matt's PodGrabber. Goodbye!")
            exit()
        if valid_responses is None or user_input in valid_responses:
            return user_input
        print("Invalid input. Please try again.")

def select_feed():
    library = load_library()
    if library:
        print("Select a podcast from your library or enter a new RSS feed URL:")
        for i, (title, url) in enumerate(library.items(), 1):
            print(f"{i}. {title}")
        choice = get_user_input("Your choice (or enter a new URL): ")
        if choice.isdigit() and int(choice) <= len(library):
            selected_url = list(library.values())[int(choice)-1]
            return selected_url, is_feed_in_library(selected_url)
        return choice, is_feed_in_library(choice)
    return get_user_input("Enter the podcast RSS feed URL: "), False

def display_and_select_episodes(feed_url):
    feed = feedparser.parse(feed_url)
    episodes = feed.entries[:10]  # Get the latest 10 episodes for display
    letter_mapping = dict(zip(string.ascii_uppercase, episodes))

    print("\nAvailable episodes:")
    for letter, episode in letter_mapping.items():
        print(f"{letter}.) {episode.title}")

    print("Enter letters for specific episodes (e.g., A, B), 'all' for all episodes,")
    print("'first' for the first episode, 'last' for the last episode,")
    print("a number for a specific number of recent episodes, or enter a keyword to filter by title.")
    selection = get_user_input("Your choice: ").upper()

    selected_episodes = []
    if selection in letter_mapping:
        selected_episodes.append(letter_mapping[selection])
    elif ',' in selection:
        selected_episodes.extend([letter_mapping[letter] for letter in selection.split(',') if letter in letter_mapping])
    elif selection == 'ALL':
        selected_episodes.extend(feed.entries)
    elif selection == 'FIRST':
        selected_episodes.append(feed.entries[0])
    elif selection == 'LAST':
        selected_episodes.append(feed.entries[-1])
    elif selection.isdigit():
        num = int(selection)
        selected_episodes.extend(feed.entries[:num])
    else:  # Treat as keyword
        keyword = selection.lower()
        selected_episodes.extend([episode for episode in feed.entries if keyword in episode.title.lower()])

    return selected_episodes

def download_podcast_episodes(selected_episodes, download_folder):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    for episode in selected_episodes:
        if 'enclosures' in episode:
            episode_url = episode.enclosures[0]['href']
            filename = os.path.basename(episode_url)
            download_path = os.path.join(download_folder, filename)
            print(f"Downloading episode: {episode.title}...")
            download_file(episode_url, download_path)

def run_podgrabber():
    while True:
        download_folder = initialize_config()
        feed_url, already_in_library = select_feed()
        selected_episodes = display_and_select_episodes(feed_url)
        download_podcast_episodes(selected_episodes, download_folder)
        if not already_in_library:
            if get_user_input("Do you want to save this RSS feed in the Library? (y/n): ", ['y', 'n']).startswith('y'):
                feed = feedparser.parse(feed_url)
                podcast_title = feed.feed.title if 'title' in feed.feed else "Unknown Podcast"
                save_to_library(feed_url, podcast_title)
        action = get_user_input("Would you like to start again or quit Matt's PodGrabber? (start/quit): ", ['start', 'quit'])
        if action == 'quit':
            print("Thank you for using Matt's PodGrabber. Goodbye!")
            break

if __name__ == "__main__":
    run_podgrabber()
    