import os
from moviepy.editor import (
    AudioFileClip,
    ImageClip,
    concatenate_videoclips,
)
from PIL import Image

def create_video(voice_path, product_images, products):
    print("🎞️ Creating video...")

    image_clips = []
    duration_per_clip = 3  # seconds

    for i, image_path in enumerate(product_images):
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image not found: {image_path}")

            # Verify image is valid
            with Image.open(image_path) as img:
                img.verify()

            image_clip = (
                ImageClip(image_path)
                .set_duration(duration_per_clip)
                .resize(height=1080)
                .fadein(1)
                .fadeout(1)
            )
            image_clips.append(image_clip)

        except Exception as e:
            print(f"❌ Error processing image {image_path}: {e}")

    if not image_clips:
        raise RuntimeError(
            "❌ No valid images were processed. Make sure placeholder images exist and Pillow is pinned to a compatible version like 9.5.0."
        )

    video = concatenate_videoclips(image_clips, method="compose")

    # Add voice-over
    audio = AudioFileClip(voice_path)
    video = video.set_audio(audio)
    video = video.set_duration(audio.duration)

    # Ensure output directory exists
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "final_video.mp4")

    # Export video
    video.write_videofile(output_path, fps=24)

    print(f"✅ Video saved to {output_path}")
    return output_path
