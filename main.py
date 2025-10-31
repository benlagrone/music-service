from fastapi import FastAPI, Query
from pydantic import BaseModel
from audiocraft.models import MusicGen
import uuid
import os


app = FastAPI()
model = MusicGen.get_pretrained('medium')
model.set_generation_params(duration=30)

class MusicPrompt(BaseModel):
    prompt: str
    duration: int = 30  # seconds

@app.post("/generate-music/")
def generate_music(request: MusicPrompt):
    prompt = request.prompt
    duration = request.duration

    model.set_generation_params(duration=duration)
    output = model.generate([prompt])

    output_filename = f"{uuid.uuid4()}.wav"
    model.save(output[0], output_filename)

    return {"status": "success", "file": output_filename}