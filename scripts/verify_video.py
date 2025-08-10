# verify_video.py
from moviepy.editor import VideoFileClip

def verify_video(video_path: str) -> bool:
    try:
        clip = VideoFileClip(video_path)
        has_audio = clip.audio is not None and clip.audio.duration > 0
        print(f"[VERIFY] Video duration: {clip.duration:.2f}s")
        print(f"[VERIFY] Audio present: {'✅ Yes' if has_audio else '❌ No'}")
        clip.close()

        if not has_audio:
            raise Exception("🛑 Audio track missing — aborting upload.")
        return True
    except Exception as e:
        print(f"[ERROR] Video verification failed: {e}")
        return False
