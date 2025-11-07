FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Etc/UTC

# System deps for audio processing, PyAV, and git-based installs
RUN apt-get update && \
    apt-get install -y --no-install-recommends tzdata ffmpeg git pkg-config \
        libavdevice-dev libavfilter-dev libavformat-dev libavcodec-dev libavutil-dev && \
    ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime && \
    echo ${TZ} > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata && \
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
