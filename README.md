# Matt's PodGrabber v1.0

## Description
Matt's PodGrabber is a Python script designed for downloading podcast episodes. 
It allows users to select specific episodes from the last 10 listed for a chosen podcast feed and proceed with downloading as per their choice.

## Dependencies
- Python 3
- Requests: For making HTTP requests to download episodes.
- Feedparser: For parsing podcast RSS feeds.
- Tqdm: For displaying download progress bars.

## Installation
1. Ensure Python 3 is installed on your system.
2. Install the required Python libraries by running: pip install requests feedparser tqdm

## How to Operate
1. Run the script in a terminal or command prompt:
python matts_podgrabber.py

2. Follow the on-screen prompts to:
   - Enter a podcast RSS feed URL or select one from the saved library.
   - Choose to download all episodes, the first, last, a specific number of episodes, or filter episodes by keyword.
   - Decide whether to save the new podcast feed to the library for future use.
3. The script will download the selected episodes to a specified download folder.

## Features
- Download specific episodes by selection or filter by keyword.
- Download the first, last, or a specified number of the latest episodes.
- Save and select podcast feeds from a library for easy access.
- Customizable download folder through a configuration file.
- User-friendly prompts and progress display for downloads.

## Quitting the Script
Enter 'q' at any prompt to exit the script immediately.

Thank you for using Matt's PodGrabber!
