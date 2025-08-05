# scripts/create_video.py

from moviepy.editor import (
    ImageClip, AudioFileClip, CompositeVideoClip, TextClip, concatenate_videoclips
)
import os

def create_video(voice_path, product_images, products, music_path="assets/music.mp3"):
    duration_per_image = 4  # seconds
    clips = []

    # Generate one clip per product
    for i, (image_path, product) in enumerate(zip(product_images, products)):
        product_text = f"{product['title']}\n{product['price']} | ⭐ {product['rating']}"
        
        image_clip = (
            ImageClip(image_path)
            .set_duration(duration_per_image)
            .resize(height=1920)  # portrait
            .set_position("center")
        )

        text_clip = (
            TextClip(product_text, fontsize=60, color="white", bg_color="black", method="caption", size=(1000, None))
            .set_position(("center", 1600))
            .set_duration(duration_per_image)
        )

        composite = CompositeVideoClip([image_clip, text_clip], size=(1080, 1920))
        clips.append(composite)

    final_clip = concatenate_videoclips(clips, method="compose")

    voiceover = AudioFileClip(voice_path)
    final_clip = final_clip.set_audio(voiceover)

    # Add background music if exists
    if os.path.exists(music_path):
        music = AudioFileClip(music_path).volumex(0.1)
        final_clip = final_clip.set_audio(voiceover.audio_fadein(0.5).audio_fadeout(0.5).fx(lambda a: a.set_duration(final_clip.duration)))
    
    output_path = "outputs/final_video.mp4"
    final_clip.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
    return output_path
