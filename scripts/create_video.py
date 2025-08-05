from moviepy.editor import *
from PIL import Image
import os

def create_video(voice_path, output_path="outputs/final_video.mp4"):
    audio = AudioFileClip(voice_path)
    duration = audio.duration

    image_path = "assets/placeholder.jpg"
    if not os.path.exists(image_path):
        raise FileNotFoundError("Missing placeholder.jpg in /assets")

    # 🛠 Convert grayscale to RGB if needed
    img = Image.open(image_path)
    if img.mode != "RGB":
        img = img.convert("RGB")
        img.save("assets/converted_placeholder.jpg")
        image_path = "assets/converted_placeholder.jpg"

    image_clip = (
        ImageClip(image_path)
        .set_duration(duration)
        .resize(height=1080)
        .set_position("center")
        .set_fps(30)
        .fadein(1)
        .fadeout(1)
    )

    final_clip = image_clip.set_audio(audio)

    os.makedirs("outputs", exist_ok=True)
    final_clip.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac")
    return output_path
