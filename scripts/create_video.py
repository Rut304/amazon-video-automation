from moviepy.editor import *
import os

def create_video(voice_path, image_paths, products):
    clips = []

    for i, image_path in enumerate(image_paths):
        img_clip = ImageClip(image_path).set_duration(4).resize(height=1280).set_position("center").set_fps(24)
        title = f"{products[i]['title']} - ${products[i]['price']} - {products[i]['rating']}⭐"
        txt_clip = TextClip(title, fontsize=48, color='white', size=(1080, None), method='caption').set_duration(4).set_position('bottom')
        composite = CompositeVideoClip([img_clip, txt_clip], size=(1080, 1920))
        clips.append(composite)

    video = concatenate_videoclips(clips, method="compose")
    audio = AudioFileClip(voice_path)
    video = video.set_audio(audio)
    video_path = "outputs/final_video.mp4"
    video.write_videofile(video_path, fps=24)
    return video_path
