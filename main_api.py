from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torchaudio
from datetime import datetime
import uuid
import os

try:
    from torch.utils import _pytree as torch_pytree  # type: ignore
    if not hasattr(torch_pytree, "register_pytree_node"):
        _orig_register = torch_pytree._register_pytree_node

        def _register_pytree_node(tree_type, flatten_fn, unflatten_fn, *, serialized_type_name=None):
            # Older torch only exposes _register_pytree_node without the newer kwargs.
            return _orig_register(tree_type, flatten_fn, unflatten_fn)

        torch_pytree.register_pytree_node = _register_pytree_node  # type: ignore[attr-defined]
except Exception:
    pass

from audiocraft.models import MusicGen

from prompt_generator import get_music_prompt  # ← from earlier step

app = FastAPI()
model = MusicGen.get_pretrained('medium')
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

class MusicRequest(BaseModel):
    scene: str
    duration: int = 60  # seconds

@app.post("/generate-music/")
def generate_music(request: MusicRequest):
    prompt = get_music_prompt(request.scene)
    if not prompt:
        raise HTTPException(status_code=500, detail="Failed to generate prompt from Ollama.")
    
    model.set_generation_params(duration=request.duration)
    wav = model.generate([prompt])

    filename = f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:8]}.wav"
    filepath = os.path.join(output_dir, filename)
    torchaudio.save(filepath, wav[0].cpu(), sample_rate=32000)

    return {
        "scene": request.scene,
        "prompt": prompt,
        "file": filepath
    }
#   uvicorn main_api:app --host 0.0.0.0 --port 7000
