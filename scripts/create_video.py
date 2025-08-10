# create_video.py
import os
from typing import List, Dict
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
VIDEOS_DIR = os.path.join(PROJECT_ROOT, "videos")


def _abs_path(path: str) -> str:
    return path if os.path.isabs(path) else os.path.join(PROJECT_ROOT, path)


def create_video(products: List[Dict], voice_path: str, seconds_per_image: int = 5) -> str:
    """
    Creates a slideshow video from product images and attaches the provided voice audio.
    Returns the final video path: videos/final_video.mp4
    """
    if not products:
        raise ValueError("Products list is empty. Provide at least one image_path.")

    clips = []
    for product in products:
        img_path = _abs_path(product["image_path"])
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Missing image: {img_path}")
        clip = ImageClip(img_path).set_duration(seconds_per_image).resize(width=1920)
        clips.append(clip)

    video = concatenate_videoclips(clips, method="compose").set_fps(30)

    vpath = _abs_path(voice_path)
    if not os.path.exists(vpath):
        raise FileNotFoundError(f"Missing audio file: {vpath}")

    audio = AudioFileClip(vpath)
    # Fit audio to video duration if needed
    if audio.duration > video.duration:
        audio = audio.subclip(0, video.duration)
    try:
        audio = audio.set_fps(44100).set_channels(2)
    except Exception:
        pass

    video = video.set_audio(audio)

    os.makedirs(VIDEOS_DIR, exist_ok=True)
    output_path = os.path.join(VIDEOS_DIR, "final_video.mp4")

    video.write_videofile(
        output_path,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        audio_bitrate="192k",
        temp_audiofile=os.path.join(VIDEOS_DIR, "temp-audio.m4a"),
        remove_temp=True,
        threads=4,
        preset="medium",
        verbose=False
    )

    video.close()
    audio.close()
    for c in clips:
        c.close()

    return output_path
