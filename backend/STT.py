import pyaudio
import numpy as np
import whisper

import google.generativeai as genai
import os
from datetime import datetime
import json
import requests
from dotenv import load_dotenv

load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")
ocr_key = os.getenv("OCR_API_KEY")


def record_audio(duration=5, sample_rate=16000, chunk_size=1024, channels=1):
    audio_format = pyaudio.paInt16  # 16-bit resolution

    p = pyaudio.PyAudio()

    # Open stream
    stream = p.open(format=audio_format,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk_size)

    # print("Recording...")

    frames = []

    # Record data in chunks for the specified duration
    for _ in range(0, int(sample_rate / chunk_size * duration)):
        data = stream.read(chunk_size)
        frames.append(np.frombuffer(data, dtype=np.int16))

    # print("Finished recording.")

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

    # Run the transcription
    # print("Transcribing audio...")
    result = model.transcribe(audio_data, fp16=False)
    text = result["text"]
    # print("Transcribed Text:")
    # print(text)
    return text


def scan_receipts(img=None):

    url = "https://api.ocr.space/parse/image"
    api_key = ocr_key
    image_path = "receipt2.png"

    with open(image_path, 'rb') as image_file:
        files = {
            'file': image_file
        }
        
        payload = {
            'language': 'eng',
            'isOverlayRequired': 'false',
            'iscreatesearchablepdf': 'false',
            'issearchablepdfhidetextlayer': 'false',
            'isTable': 'true'
        }

        headers = {
            'apikey': api_key
        }
        # Send the image to OCR.space
        response = requests.post(url, headers=headers, data=payload, files=files)
        result = response.json()

        # Print the result
        # print(result['ParsedResults'][0]['ParsedText'])
        res = result['ParsedResults'][0]['ParsedText'].split('\t\r\n')
        return ','.join(res)



def format_STT(text):
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel("gemini-1.5-pro-latest")

    date_str = f"Today's date is {datetime.now().date()}. Message = "
    audio_input=text
    # audio_input = "2 apples in a few days, 3 bananas in around 5 days, 8 eggs in 3 days"
    prompt = date_str + audio_input + """: convert this into JSON format. Only output the JSON.

    Use this JSON schema:

    Food = {"name": str, count": int, "expiry": date}
    Return: {"pantry": list[Food], "fridge": list[Food]"""
    result = model.generate_content(prompt)
    generated_json = result.text
    clean_json = generated_json.replace("```json", "").replace("```", "").strip()
    ingredients = json.loads(clean_json)
    # print(ingredients)
    return json.loads(ingredients)




def main():
    # Step 1: Record audio without saving to a file
    # audio_data = record_audio(duration=10)  # Record for 5 seconds

    # Step 2: Transcribe audio data to text
    # text = transcribe_audio(audio_data)
    print(scan_receipts())
    # Step 3: Process transcribed text with OctoAI
    # format_STT(text)
    # If needed, you can return or further process 'output'
    # return output

if __name__ == "__main__":
    main()