import os
import feedparser
import urllib.request
import re
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TDRC
from datetime import datetime

# Parse the RSS feed
feed_url = "https://feeds.simplecast.com/qm_9xx0g"
feed = feedparser.parse(feed_url)

# Function to remove invalid characters from a filename
def clean_filename(filename):
    # Define the pattern for invalid characters
    invalid_chars = r'[<>:"/\\|?*\x00-\x1F\x7F]'
    
    # Remove or replace invalid characters
    cleaned_filename = re.sub(invalid_chars, '', filename)
    return cleaned_filename

# Reverse the order of feed entries
feed_entries = reversed(feed.entries)

# Initialize counter
counter = 1

# Iterate over the items in the feed in reverse order
for item in feed_entries:
    # Get the title, publication date, and enclosure URL
    title = item.title
    pub_date = item.published_parsed
    enclosure_url = item.enclosures[0].href

    # Generate the file name
    cleaned_title = clean_filename(title)
    file_name = f"{counter:03d} - {cleaned_title}.mp3"  # Prefix with counter and format with leading zeros

    # Skip download if file already exists
    if os.path.exists(file_name):
        print(f"Skipped {file_name} (already exists)")
    else:
        # Download the audio file
        urllib.request.urlretrieve(enclosure_url, file_name)
        print(f"Downloaded {file_name}")

        # Set the publication date in the file's metadata
        audio = MP3(file_name, ID3=ID3)
        audio.tags.add(TDRC(encoding=3, text=datetime(*pub_date[:6]).strftime('%Y-%m-%d')))
        audio.save()

    # Increment counter
    counter += 1