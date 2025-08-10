from scripts.generate_voice import generate_voice

def main():
    # Define tasks: text, voice ID, and output filename
    tasks = [
        {
            "text": "Welcome to Jeff's fully automated affiliate channel!",
            "voice_id": "your_voice_id_here",
            "filename": "intro.mp3"
        },
        {
            "text": "This product is one of our top picks for 2025.",
            "voice_id": "your_voice_id_here",
            "filename": "product_highlight.mp3"
        },
        {
            "text": "Thanks for watching. Don’t forget to like and subscribe!",
            "voice_id": "your_voice_id_here",
            "filename": "outro.mp3"
        }
    ]

    # Run the generate_voice function for each task
    for task in tasks:
        try:
            generate_voice(
                text=task["text"],
                voice_id=task["voice_id"],
                filename=task["filename"]
            )
        except Exception as e:
            print(f"⚠️ Failed to generate
