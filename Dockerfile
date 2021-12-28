FROM python:3.8

WORKDIR /app

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    ffmpeg libsm6 libxext6 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir \
    cryptography~=3.4.0 \
    opencv-python \
    && mkdir output

COPY app/steganography.py .