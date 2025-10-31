from audiocraft.models import MusicGen
import torchaudio
from datetime import datetime
import uuid
import re

# Load pre-trained model (options: 'small', 'medium', 'melody', 'large')
model = MusicGen.get_pretrained('medium')

# Define prompt with soft time-control cues
prompt = (
    "Cinematic orchestral music that evolves over time: "
    "It begins softly at 0 seconds with ambient textures and subtle strings, evoking the birth of creation. "
    "At 20 seconds, layers of brass and rising harmonies begin to swell, signifying the divine formation of heaven and earth. "
    "At 40 seconds, the music reaches a powerful climax with full orchestration — soaring strings, triumphant horns, and deep percussion. "
    "After 50 seconds, it gently releases into a soft piano outro with warm echoes, expressing the serenity of divine order. "
    "Inspired by Genesis 1:1 — 'In the beginning God created the heaven and the earth' — imagined through the lens of Neoclassical art: "
    "clean lines, moral clarity, radiant light, celestial expanse, and earth's verdant promise, rendered with harmonic depth and balance."
)

# Set total duration in seconds
duration = 60

# Generate music
model.set_generation_params(duration=duration)
wav = model.generate([prompt])

# Create filename using timestamp, UUID, and a shortened keyword from the prompt
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
unique_id = str(uuid.uuid4())[:8]
slug = re.sub(r'\W+', '-', prompt[:60].lower()).strip('-')
filename = f"{timestamp}-{slug}-{unique_id}.wav"

# Save to file
torchaudio.save(filename, wav[0].cpu(), sample_rate=32000)
print(f"✅ Music saved to {filename}")