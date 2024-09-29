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


# def scan_receipts(img=None):

#     url = "https://api.ocr.space/parse/image"
#     api_key = ocr_key
#     image_path = "receipt2.png"

#     with open(image_path, 'rb') as image_file:
#         files = {
#             'file': image_file
#         }
        
#         payload = {
#             'language': 'eng',
#             'isOverlayRequired': 'false',
#             'iscreatesearchablepdf': 'false',
#             'issearchablepdfhidetextlayer': 'false',
#             'isTable': 'true'
#         }

#         headers = {
#             'apikey': api_key
#         }
#         # Send the image to OCR.space
#         response = requests.post(url, headers=headers, data=payload, files=files)
#         result = response.json()

#         # Print the result
#         # print(result['ParsedResults'][0]['ParsedText'])
#         res = result['ParsedResults'][0]['ParsedText'].split('\t\r\n')
#         return ','.join(res)



# def gemini_generator(text,input_form: Forms=Forms.STT, meal=None):
#     genai.configure(api_key=gemini_key)
#     model = genai.GenerativeModel("gemini-1.5-pro-latest")

#     date_str = f"Today's date is {datetime.now().date()}. Message = "

#     if input_form == Forms.STT:
#         prompt = date_str + text + """: convert this into JSON format. Only output the JSON.

#         Use this JSON schema:

#         Food = {"name": str, count": int, "expiry": date}
#         Return: {"pantry": list[Food], "fridge": list[Food]"""
#     elif input_form == Forms.RECEIPT:
#         prompt = date_str + text + """: convert this into JSON format. Generalize the food items i.e. make lowercase and ensure spelling is correct and plural. Divide weight by average weight of item to obtain count. Only output the JSON. 

#         Use this JSON schema:

#         Food = {"name": str, count": int, "expiry": date}
#         Return: {"pantry": list[Food], "fridge": list[Food]"""
#     else:
#         # TODO : UPDATE THE JSON SCHEMA
#         # ADD BREAKFAST DINNER LUNCH

#         prompt = date_str + text + """: using these ingredients along with their quantities and units, give me 3 recipes for a dish in the following format e.g. [{“name”: “pasta”, “ingredients”: [“pasta sauce: 5 oz”, “frozen veggies: .2 lbs”, “raviolli: .1 lbs”], “instructions”: [“Boil the pasta”, “Add spices”, ...], “time (mins)“: 20}
#         and for the 
#         Use this JSON schema:

#         Food = {"name": str, count": int, "expiry": date}
#         Return: {"pantry": list[Food], "fridge": list[Food]"""



#     result = model.generate_content(prompt)
#     generated_json = result.text
#     clean_json = generated_json.replace("```json", "").replace("```", "").strip()
#     ingredients = json.loads(clean_json)

#     return json.loads(ingredients)




def main():
    pass
    # Step 1: Record audio without saving to a file
    # audio_data = record_audio(duration=10)  # Record for 5 seconds

    # Step 2: Transcribe audio data to text
    # text = transcribe_audio(audio_data)
    
    # RECEIPT SCANNING
    # scan_receipts()
    # Step 3: Process transcribed text with OctoAI
    # format_STT(text)
    # If needed, you can return or further process 'output'
    # return output

if __name__ == "__main__":
    main()