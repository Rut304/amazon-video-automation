# create_video.py
import os
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

def create_video(products: list, voice_path: str, seconds_per_image: int = 5) -> str:
    """
    Creates a slideshow video from product images and attaches the provided voice audio.
    Returns the final video path: videos/final_video.mp4
    """
    if not products:
        raise ValueError("Products list is empty. Provide at least one image_path.")

    clips = []
    for product in products:
        img_path = product["image_path"]
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Missing image: {img_path}")
        # 1920-wide with aspect preserved; duration per image
        clip = ImageClip(img_path).set_duration(seconds_per_image).resize(width=1920)
        clips.append(clip)

    video = concatenate_videoclips(clips, method="compose").set_fps(30)

    if not os.path.exists(voice_path):
        raise FileNotFoundError(f"Missing audio file: {voice_path}")

    audio = AudioFileClip(voice_path)
    # Trim/fit audio to video duration to avoid trailing silence or cutoff
    if audio.duration > video.duration:
        audio = audio.subclip(0, video.duration)
    # Ensure consistent audio parameters
    try:
        audio = audio.set_fps(44100).set_channels(2)
    except Exception:
        pass

    video = video.set_audio(audio)

    os.makedirs("videos", exist_ok=True)
    output_path = "videos/final_video.mp4"

    video.write_videofile(
        output_path,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        audio_bitrate="192k",
        temp_audiofile="temp-audio.m4a",
        remove_temp=True,
        threads=4,
        preset="medium",
        verbose=False,
    )

    video.close()
    audio.close()
    for c in clips:
        c.close()

    return output_path
