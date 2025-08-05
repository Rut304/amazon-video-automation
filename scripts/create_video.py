import os
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips,
)
from PIL import Image
import numpy as np

def create_video(voice_path, image_paths, products):
    clips = []

    for idx, image_path in enumerate(image_paths):
        try:
            # Convert image to RGB and save temp version
            img = Image.open(image_path).convert("RGB")
            img = img.resize((1080, 1080))  # Ensures consistent size

            # Convert to numpy array for MoviePy
            img_array = np.array(img)
            clip = ImageClip(img_array).set_duration(5)
            clips.append(clip)

        except Exception as e:
            print(f"❌ Error processing image {image_path}: {e}")

    if not clips:
        raise RuntimeError(
            "❌ No valid images were processed. Make sure placeholder images exist "
            "and Pillow is pinned to a compatible version like 9.5.0."
        )

    video = concatenate_videoclips(clips, method="compose")

    audio = AudioFileClip(voice_path)
    video = video.set_audio(audio)

    os.makedirs("outputs", exist_ok=True)
    output_path = "outputs/final_video.mp4"
    video.write_videofile(output_path, fps=24)

    print(f"✅ Video saved to {output_path}")
    return output_path
