from scripts.generate_voice import generate_voice

def main():
    # Example list of voice tasks
    tasks = [
        {"text": "Welcome to the channel!", "voice_id": "your_voice_id", "filename": "intro.mp3"},
        {"text": "Here’s your product summary.", "voice_id": "your_voice_id", "filename": "summary.mp3"},
        {"text": "Thanks for watching!", "voice_id": "your_voice_id", "filename": "outro.mp3"}
    ]

    for task in tasks:
        generate_voice(
            text=task["text"],
            voice_id=task["voice_id"],
            filename=task["filename"]
        )

if __name__ == "__main__":
    main()
