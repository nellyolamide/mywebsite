import requests
import json
import re


def get_instagram_video_url(post_url):
    # Send a GET request to the Instagram post URL
    response = requests.get(post_url)

    if response.status_code != 200:
        print("Failed to retrieve post.")
        return None

    # Use regex to find the script tag containing the JSON data
    json_match = re.search(r'window\._sharedData = (.+);</script>', response.text)
    if not json_match:
        print("Could not find JSON data.")
        return None

    # Load the JSON data
    json_data = json.loads(json_match.group(1))

    # Extract video URL
    video_url = None
    try:
        video_url = json_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['video_url']
    except KeyError:
        print("Could not find video URL.")
        return None

    return video_url


def download_video(video_url, file_name):
    response = requests.get(video_url, stream=True)

    if response.status_code == 200:
        with open(file_name, 'wb') as f:
            for chunk in response.iter_content(1024 * 1024):  # Write in chunks
                f.write(chunk)
        print(f"Video downloaded successfully: {file_name}")
    else:
        print("Failed to download video.")


if __name__ == "__main__":
    # Input: Instagram post URL
    post_url = input("Enter the Instagram post URL: ")

    # Get video URL
    video_url = get_instagram_video_url(post_url)

    if video_url:
        # Download the video
        download_video(video_url, 'downloaded_video.mp4')
