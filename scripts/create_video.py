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
    video = video.set_audio(audio)

    os.makedirs(VIDEOS_DIR, exist_ok=True)
    output_path = os.path.join(VIDEOS_DIR, "final_video.mp4")
    video.write_videofile(output_path, codec="libx264", audio_codec="aac")

    return output_path
