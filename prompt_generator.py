import subprocess

def get_music_prompt(scene_description: str) -> str:
    llm_prompt = (
        f"Create a cinematic orchestral music prompt for a 60-second track. "
        f"It should start softly, build slowly, reach a climax at 40 seconds, "
        f"and resolve gently with a piano outro. "
        f"Describe the mood, instruments, and emotion arc. "
        f"Inspiration: {scene_description}"
    )
    try:
        result = subprocess.run(
            ['ollama', 'run', 'llama3', llm_prompt],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("❌ Error running Ollama:", e)
        return ""