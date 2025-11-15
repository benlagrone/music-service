from fastapi import FastAPI, Query
from pydantic import BaseModel
import uuid
import os

try:
    from torch.utils import _pytree as torch_pytree  # type: ignore
    if not hasattr(torch_pytree, "register_pytree_node"):
        torch_pytree.register_pytree_node = torch_pytree._register_pytree_node  # type: ignore[attr-defined]
except Exception:
    pass

from audiocraft.models import MusicGen


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
