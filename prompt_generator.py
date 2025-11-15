import json
import os
import shutil
import subprocess
from typing import Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
OLLAMA_API_URL = os.getenv(
    "OLLAMA_API_URL", "http://host.docker.internal:11434/api/generate"
)


def get_music_prompt(scene_description: str) -> str:
    llm_prompt = (
        f"Create a cinematic orchestral music prompt for a 60-second track. "
        f"It should start softly, build slowly, reach a climax at 40 seconds, "
        f"and resolve gently with a piano outro. "
        f"Describe the mood, instruments, and emotion arc. "
        f"Inspiration: {scene_description}"
    )
    response = _run_ollama_cli(llm_prompt) or _run_ollama_http(llm_prompt)
    if response:
        return response
    return (
        "Evolving orchestral suite with strings and woodwinds painting a fading sunset over the sea; "
        f"grows to brass-driven heroism before dissolving into a solo piano reflection inspired by {scene_description}."
    )


def _run_ollama_cli(prompt: str) -> Optional[str]:
    """Call the Ollama CLI if it is available inside the container."""
    if shutil.which("ollama") is None:
        return None
    try:
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL, prompt],
            capture_output=True,
            text=True,
            check=True,
            timeout=120,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        print("❌ Error running Ollama CLI:", exc)
        return None
    return result.stdout.strip()


def _run_ollama_http(prompt: str) -> Optional[str]:
    """Fallback to the Ollama HTTP API if reachable (typically host machine port 11434)."""
    if not OLLAMA_API_URL:
        return None
    payload = json.dumps(
        {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
    ).encode("utf-8")
    request = Request(
        OLLAMA_API_URL, data=payload, headers={"Content-Type": "application/json"}
    )
    try:
        with urlopen(request, timeout=120) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, ConnectionError) as exc:  # type: ignore[arg-type]
        print(f"❌ Error calling Ollama HTTP API at {OLLAMA_API_URL}: {exc}")
        return None
    return (data.get("response") or data.get("output") or "").strip()
