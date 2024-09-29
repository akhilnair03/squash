import pyaudio
import numpy as np
import whisper

import google.generativeai as genai
import os
from datetime import datetime
import json
import requests
from dotenv import load_dotenv
from enum import Enum

load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")
ocr_key = os.getenv("OCR_API_KEY")


class Forms(Enum):
    STT = 1
    RECOMMEND = 2
    RECEIPT = 3

def record_audio(duration=5, sample_rate=16000, chunk_size=1024, channels=1):
    audio_format = pyaudio.paInt16  # 16-bit resolution

    p = pyaudio.PyAudio()

    # Open stream
    stream = p.open(format=audio_format,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk_size)


    frames = []

    # Record data in chunks for the specified duration
    for _ in range(0, int(sample_rate / chunk_size * duration)):
        data = stream.read(chunk_size)
        frames.append(np.frombuffer(data, dtype=np.int16))

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Convert frames to a NumPy array
    audio_data = np.hstack(frames)

    return audio_data

def transcribe_audio(audio_data, sample_rate=16000):
    # Load the Whisper model
    model = whisper.load_model("base")  # Options: 'tiny', 'base', 'small', 'medium', 'large'

    # Convert the NumPy array to float32 and normalize
    audio_data = audio_data.astype(np.float32) / 32768.0  # Normalize 16-bit int to float32

    result = model.transcribe(audio_data, fp16=False)
    text = result["text"]

    return text
