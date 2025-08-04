# create_video.py
from moviepy.editor import *
import os

def create_video(voice_path, output_path="outputs/final_video.mp4"):
    # Load voiceover audio
    audio = AudioFileClip(voice_path)
    
    # Duration for each slide
    duration = audio.duration

    # Use placeholder image
    image_path = "assets/placeholder.jpg"
    if not os.path.exists(image_path):
        raise FileNotFoundError("Missing placeholder.jpg in /assets")

    # Create image clip
    image_clip = ImageClip(image_path).set_duration(duration).resize(height=1080).set_position("center")

    # Optional: add fade in/out
    image_clip = image_clip.fadein(1).fadeout(1)

    # Add background music (optional)
    # music = AudioFileClip("assets/background_music.mp3").volumex(0.1)
    # final_audio = CompositeAudioClip([audio, music])

    final_clip = image_clip.set_audio(audio)

    # Export video
    os.makedirs("outputs", exist_ok=True)
    final_clip.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac")

    return output_path

