import pyaudio
import numpy as np
import whisper

def record_audio(duration=5, sample_rate=16000, chunk_size=1024, channels=1):
    audio_format = pyaudio.paInt16  # 16-bit resolution

    p = pyaudio.PyAudio()

    # Open stream
    stream = p.open(format=audio_format,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk_size)

    print("Recording...")

    frames = []

    # Record data in chunks for the specified duration
    for _ in range(0, int(sample_rate / chunk_size * duration)):
        data = stream.read(chunk_size)
        frames.append(np.frombuffer(data, dtype=np.int16))

    print("Finished recording.")

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
    print("Transcribing audio...")
    result = model.transcribe(audio_data, fp16=False)
    text = result["text"]
    print("Transcribed Text:")
    print(text)
    return text




def main():
    # Step 1: Record audio without saving to a file
    audio_data = record_audio(duration=5)  # Record for 5 seconds

    # Step 2: Transcribe audio data to text
    text = transcribe_audio(audio_data)

    # Step 3: Process transcribed text with OctoAI
    # output = process_with_octoai(text)
    # print(output)
    # If needed, you can return or further process 'output'
    # return output

if __name__ == "__main__":
    main()


# import SpeechRecognition as sr
# import whisper
# import requests
# import json
# import pyaudio
# from octoai import OctoAI, ChatMessage, ChatCompletionResponseFormat

# # Initialize the speech recognizer
# r = sr.Recognizer()

# # Step 1: Capture microphone input
# with sr.Microphone() as source:
#     print("Please say something...")
#     audio = r.listen(source)

#     # Save the audio data to a WAV file
#     with open("input.wav", "wb") as f:
#         f.write(audio.get_wav_data())

# # Step 2: Convert speech to text using Whisper
# print("Transcribing audio...")
# model = whisper.load_model("base")  # Options: 'tiny', 'base', 'small', 'medium', 'large'
# result = model.transcribe("input.wav")
# text = result["text"]
# print(f"Transcribed Text: {text}")

# # Step 3: Send text to Llama 3 via OctoAI
# # Replace 'YOUR_OCTOAPI_KEY' with your actual OctoAI API key
# client = OctoAI(
#     api_key="YOUR_OCTOAPI_KEY"
# )

# # Define the schema for the expected JSON output
# class Output:
#     @staticmethod
#     def model_json_schema():
#         return {
#             "type": "object",
#             "properties": {
#                 "transactions": {
#                     "type": "array",
#                     "items": {
#                         "type": "object",
#                         "properties": {
#                             "sender": {"type": "string"},
#                             "receiver": {"type": "string"},
#                             "currency": {"type": "string"},
#                             "amount": {"type": "number"},
#                             "items": {"type": "string"},
#                         },
#                         "required": ["sender", "receiver", "currency", "amount", "items"],
#                     },
#                 }
#             },
#             "required": ["transactions"],
#         }

# # Prepare the messages for the chat completion
# messages = [
#     ChatMessage(
#         content=(
#             "Extract the receiver, sender, currency, amount, and items from the given text for each transaction. "
#             "If there are N senders in one transaction, make N transactions. Use context clues. "
#             "Return only in a JSON format with no other content at all."
#         ),
#         role="system"
#     ),  # Instructions for the model
#     ChatMessage(
#         content=text,
#         role="user"
#     )  # User input (transcribed text)
# ]

# # Prepare the response format
# response_format = ChatCompletionResponseFormat(
#     type="json_object",
#     schema=Output.model_json_schema(),
# )

# # Create the chat completion
# print("Sending request to Llama 3 via OctoAI...")
# model_output = client.text_gen.create_chat_completion(
#     model="meta-llama-3-8b-instruct",
#     messages=messages,
#     max_tokens=512,
#     presence_penalty=0,
#     temperature=0,
#     top_p=1,
#     response_format=response_format,
# )

# # Step 4: Handle the response
# output_content = model_output.choices[0].message.content
# print("Received output:")
# print(json.dumps(output_content, indent=2))

# If you need to return the output from a function, uncomment the following line
# return output_content








# # Import necessary libraries
# from google.cloud import speech_v1p1beta1 as speech
# import json
# from flask import Flask, request, jsonify
# # from octoai.text_gen import ChatMessage, ChatCompletionResponseFormat
# # from octoai.client import OctoAI
# # from pydantic import BaseModel

# #Initialize Flask API
# app = Flask(__name__)



# def transcribe_speech_to_text(audio_file_path):
#     # Initialize the client
#     client = speech.SpeechClient()

#     # Load audio file
#     with open(audio_file_path, 'rb') as audio_file:
#         content = audio_file.read()

#     # Configure request
#     audio = speech.RecognitionAudio(content=content)
#     config = speech.RecognitionConfig(
#         encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#         sample_rate_hertz=16000,
#         language_code="en-US",
#     )

#     # Transcribe audio
#     response = client.recognize(config=config, audio=audio)

#     # Extract and return transcribed text
#     for result in response.results:
#         print(f"Transcription: {result.alternatives[0].transcript}")
#     return response.results[0].alternatives[0].transcript



# @app.route('/analyze_text', methods=['POST'])
# def analyze_text():
#     data = request.get_json()
#     if 'text' not in data:
#         return jsonify({"error": "No text provided"}), 400
    

#     # result={"transactions": []}
#     # text = data['text']

#     # result["transactions"]= json.loads(octoai_api(text))


#     #TODO: have to rethink this with flask sessions later
#     for transaction in result["transactions"]:
#         if transaction["receiver"].lower() in ['i','my','me','you']:
#             transaction["amount"] *= -1
#     # print(result)
#     return jsonify(result)

# if __name__ == '__main__':
#     app.run(debug=True)