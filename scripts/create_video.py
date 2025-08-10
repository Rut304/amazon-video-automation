# create_video.py
import os
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from moviepy.audio.fx import all as afx

def create_video(products, voice_path):
    clips = []
    duration = 5  # seconds per image

    for product in products:
        img_path = product["image_path"]
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Missing image: {img_path}")
        clip = ImageClip(img_path).set_duration(duration).resize(width=1920)
        clips.append(clip)

    video = concatenate_videoclips(clips, method="compose").set_fps(30)

    if os.path.exists(voice_path):
        print(f"🔊 Attaching audio from: {voice_path}")
        audio = AudioFileClip(voice_path)
        audio = audio.fx(afx.audio_normalize).set_fps(44100)
        try:
            audio = audio.set_channels(2)
        except:
            pass
        print(f"[DEBUG] Video duration: {video.duration:.2f}s")
        print(f"[DEBUG] Audio duration: {audio.duration:.2f}s")
        video = video.set_audio(audio)
    else:
        print("⚠️ No audio file found; continuing without sound.")

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
        verbose=True
    )

    video.close()
    return output_path
