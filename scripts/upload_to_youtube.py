# upload_to_youtube.py
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from verify_video import verify_video

def upload_to_youtube(
    video_path: str,
    title: str,
    description: str,
    tags: list,
    privacy_status: str = "unlisted"
) -> str:
    """
    Verifies the video, then uploads to YouTube using OAuth.
    Requires client_secrets.json in the project root.
    Returns the YouTube video ID on success.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Missing video file: {video_path}")

    # Mandatory verification BEFORE upload
    if not verify_video(video_path):
        raise RuntimeError("Video failed verification (no audio or invalid). Upload aborted.")

    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", scopes)

    # Opens a browser window for Google login/consent on your Mac
    creds = flow.run_local_server(port=8080, prompt="consent")
    youtube = build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "22"  # People & Blogs (adjust if you want)
        },
        "status": {
            "privacyStatus": privacy_status
        }
    }

    media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()
    video_id = response["id"]
    print(f"✅ Upload successful: https://youtu.be/{video_id}")
    return video_id
