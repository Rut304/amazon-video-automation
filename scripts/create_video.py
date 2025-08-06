# -*- coding: utf-8 -*-
import os
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

def create_video(products, voice_path):
    clips = []
    duration = 5  # seconds per product

    for product in products:
        if not os.path.exists(product["image_path"]):
            raise FileNotFoundError(f"Missing image: {product['image_path']}")

        clip = ImageClip(product["image_path"]).set_duration(duration)
        clips.append(clip)

    final_clip = concatenate_videoclips(clips, method="compose")

    if os.path.exists(voice_path):
        audio = AudioFileClip(voice_path)
        final_clip = final_clip.set_audio(audio)

    os.makedirs("videos", exist_ok=True)
    output_path = "videos/final_video.mp4"
    final_clip.write_videofile(output_path, fps=24)

    return output_path
