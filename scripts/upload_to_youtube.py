# upload_to_youtube.py
import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from verify_video import verify_video

def upload_to_youtube(video_path: str, title="My Product Promo", description="", tags=[], privacy_status="unlisted"):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Missing video file: {video_path}")

    # 🧪 Verify video/audio
    if not verify_video(video_path):
        print("🚫 Video verification failed — not uploading.")
        return

    # 📡 OAuth2 authentication
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", scopes)
    creds = flow.run_console()
    youtube = build("youtube", "v3", credentials=creds)

    # 📦 Upload metadata
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags
        },
        "status": {
            "privacyStatus": privacy_status
        }
    }

    print("⏫ Uploading to YouTube...")
    media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()
    print(f"✅ Upload successful: https://youtu.be/{response['id']}")

    return response["id"]
