import os
from moviepy.editor import (
    AudioFileClip,
    ImageClip,
    concatenate_videoclips,
    CompositeVideoClip,
)
from PIL import Image

def create_video(voice_path, product_images, products):
    print("🎞️ Creating video...")

    image_clips = []
    duration_per_clip = 3  # seconds

    for i, image_path in enumerate(product_images):
        try:
            # Ensure image exists
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image not found: {image_path}")

            # Attempt to open with PIL to verify integrity
            with Image.open(image_path) as img:
                img.verify()

            # Create ImageClip with fade in/out
            image_clip = (
                ImageClip(image_path)
                .set_duration(duration_per_clip)
                .resize(height=1080)  # Resize to portrait format height
                .fadein(1)
                .fadeout(1)
            )
            image_clips.append(image_clip)
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")

    if not image_clips:
        raise RuntimeError(
            "❌ No valid images were processed. Ensure your placeholder images exist and Pillow is compatible (try Pillow==9.5.0)."
        )

    video = concatenate_videoclips(image_clips, method="compose")

    audio = AudioFileClip(voice_path)
    video = video.set_audio(audio)
    video = video.set_duration(audio.duration)

    output_path = "outputs/final_video.mp4"
    os.makedirs("outputs", exist_ok=True)
    video.write_videofile(output_path, fps=24)

    print(f"
