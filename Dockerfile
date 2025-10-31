FROM pytorch/pytorch:2.6.0-cuda12.1-cudnn9-runtime

WORKDIR /app

# System deps for audio processing and git-based installs
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg git && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7000

ENV PYTHONUNBUFFERED=1 \
    HF_HOME=/app/.cache/huggingface \
    TRANSFORMERS_CACHE=/app/.cache/huggingface

CMD ["uvicorn", "main_api:app", "--host", "0.0.0.0", "--port", "7000"]
