# verify_video.py
from moviepy.editor import VideoFileClip

def verify_video(video_path: str) -> bool:
    """
    Verifies the video is playable and contains a non-empty audio track.
    Returns True if OK, otherwise False.
    """
    try:
        clip = VideoFileClip(video_path)
        duration_ok = clip.duration is not None and clip.duration > 0
        has_audio = clip.audio is not None and (clip.audio.duration or 0) > 0
        print(f"[VERIFY] Video duration: {clip.duration:.2f}s")
        print(f"[VERIFY] Audio present: {'Yes' if has_audio else 'No'}")
        clip.close()
        return bool(duration_ok and has_audio)
    except Exception as e:
        print(f"[ERROR] Video verification failed: {e}")
        return False
