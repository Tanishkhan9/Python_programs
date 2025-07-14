import os
import google.auth.transport.requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def authenticate_youtube():
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", SCOPES
    )
    credentials = flow.run_local_server(port=8080)
    youtube = build("youtube", "v3", credentials=credentials)
    return youtube

def upload_video(file_path, title, description, tags=None, privacy="public"):
    youtube = authenticate_youtube()

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or [],
            "categoryId": "22"  # People & Blogs
        },
        "status": {
            "privacyStatus": privacy
        }
    }

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True, mimetype="video/*")

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = request.execute()
    print(f"✅ Video uploaded: https://youtu.be/{response['id']}")
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# === CONFIGURATION ===
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
VIDEO_DIR = "videos"  # Folder where your videos are stored
PRIVACY = "unlisted"  # public | unlisted | private


def authenticate_youtube():
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    credentials = flow.run_local_server(port=8080)
    youtube = build("youtube", "v3", credentials=credentials)
    return youtube


def get_latest_video(folder_path):
    video_files = [f for f in os.listdir(folder_path)
                   if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))]
    if not video_files:
        raise FileNotFoundError("No video files found in the folder.")
    # Sort by creation time, select the latest
    video_files.sort(key=lambda f: os.path.getctime(os.path.join(folder_path, f)))
    latest = video_files[-1]
    return os.path.join(folder_path, latest)


def format_title_and_description(filename):
    title = os.path.splitext(os.path.basename(filename))[0].replace('_', ' ').title()
    description = f"This video titled \"{title}\" was uploaded automatically using Python."
    return title, description


def upload_video_to_youtube(youtube, file_path, title, description, tags=None):
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or [],
            "categoryId": "22"  # People & Blogs
        },
        "status": {
            "privacyStatus": PRIVACY
        }
    }

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True, mimetype="video/*")

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = request.execute()
    print(f"✅ Video uploaded: https://youtu.be/{response['id']}")


def main():
    print("🚀 Starting YouTube AutoUploader...")
    video_path = get_latest_video(VIDEO_DIR)
    title, description = format_title_and_description(video_path)
    print(f"📄 Uploading: {title}")

    youtube = authenticate_youtube()
    upload_video_to_youtube(youtube, video_path, title, description, tags=["python", "automation", "upload"])


if __name__ == "__main__":
    main()
    
    
