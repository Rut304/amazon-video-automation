# verify_video.py
import os
from moviepy.editor import VideoFileClip

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _abs_path(path: str) -> str:
    return path if os.path.isabs(path) else os.path.join(PROJECT_ROOT, path)


def verify_video(video_path: str) -> bool:
    """
    Verifies the video is playable and contains a non-empty audio track.
    Returns True if OK, otherwise False.
    """
    try:
        vpath = _abs_path(video_path)
        clip = VideoFileClip(vpath)
        duration_ok = clip.duration is not None and clip.duration > 0
        has_audio = clip.audio is not None and (clip.audio.duration or 0) > 0
        print(f"[VERIFY] Video duration: {clip.duration:.2f}s")
        print(f"[VERIFY] Audio present: {'Yes' if has_audio else 'No'}")
        clip.close()
        return bool(duration_ok and has_audio)
    except Exception as e:
        print(f"[ERROR] Video verification failed: {e}")
        return False
