# scripts/create_video.py

import os
from moviepy.editor import (
    AudioFileClip,
    ImageClip,
    concatenate_videoclips,
    CompositeVideoClip,
)
from PIL import Image

def create_video(voice_path, product_images, products):
    from moviepy.editor import TextClip

    # Set up output paths
    os.makedirs("outputs", exist_ok=True)
    image_clips = []
    duration_per_image = 5  # seconds

    for i, image_path in enumerate(product_images):
        try:
            image_clip = (
                ImageClip(image_path)
                .set_duration(duration_per_image)
                .resize(height=1080)
                .set_position("center")
            )

            # Add text overlay
            product = products[i]
            text = f"{product['title']}\n${product['price']} | ⭐ {product['rating']}"
            text_clip = (
                TextClip(text, fontsize=50, color="white", font="Arial-Bold", method="caption", size=(1080, None))
                .set_duration(duration_per_image)
                .set_position(("center", "bottom"))
            )

            # Combine image and text
            combined = CompositeVideoClip([image_clip, text_clip])
            image_clips.append(combined)

        except Exception as e:
            print(f"Error processing image {image_path}: {e}")

    # Combine all image clips
    video = concatenate_videoclips(image_clips, method="compose")

    # Add voiceover
    audio = AudioFileClip(voice_path)
    video = video.set_audio(audio)

    # Add background music if available
    music_path = "assets/music.mp3"
    if os.path.exists(music_path):
        from moviepy.editor import AudioFileClip, CompositeAudioClip

        music = AudioFileClip(music_path).volumex(0.2).set_duration(video.duration)
        final_audio = CompositeAudioClip([audio, music])
        video = video.set_audio(final_audio)

    # Export final video
    output_path = "outputs/final_video.mp4"
    video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")

    return output_path
