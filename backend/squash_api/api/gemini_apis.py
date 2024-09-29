from datetime import datetime
import squash_api
import flask
from flask import request, jsonify
import math
import os
import pymongo
import sys
from dotenv import load_dotenv
from enum import Enum
from datetime import datetime
import google.generativeai as genai
import requests
import json

import numpy as np
import whisper
import base64
import io
from scipy.io import wavfile
from pydub import AudioSegment

load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")
ocr_key = os.getenv("OCR_API_KEY")
google_maps_key=os.getenv("GOOGLE_MAPS_API_KEY")


# Fetch environment variables
db_password = os.getenv("DB_PASSWORD")

try:
    client = pymongo.MongoClient(f"mongodb+srv://mahesha:{db_password}@cluster0.4xv3s.mongodb.net/?retryWrites=true&w=majority&tls=true&tlsInsecure=true&appName=Cluster0")

except pymongo.errors.ConfigurationError:
    print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
    sys.exit(1)

db = client.inventory




''' 
********************************************************************************
SCANNING AND GEMINI GENERATOR
********************************************************************************
'''


def scan_receipts(img_data):
    url = "https://api.ocr.space/parse/image"

    payload = {
        'language': 'eng',
        'isOverlayRequired': 'false',
        'iscreatesearchablepdf': 'false',
        'issearchablepdfhidetextlayer': 'false',
        'isTable': 'true',
        'base64Image': img_data
    }

    headers = {
        'apikey': ocr_key
    }

    response = requests.post(url, headers=headers, data=payload)
    result = response.json()

    if result.get('IsErroredOnProcessing'):
        error_message = result.get('ErrorMessage', ['Unknown error'])[0]
        print(f"OCR Error: {error_message}")
        return ''

    # Extract the parsed text
    parsed_results = result.get('ParsedResults')
    if parsed_results and len(parsed_results) > 0:
        parsed_text = parsed_results[0].get('ParsedText', '')
    else:
        parsed_text = ''

    # Process the parsed text as needed
    res = parsed_text.split('\t\r\n')
    return ','.join(res)


def gemini_generator(prompt):
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    result = model.generate_content(prompt)
    generated_json = result.text

    clean_json = generated_json.replace("```json", "").replace("```", "").strip()
    ingredients = json.loads(clean_json)
    return ingredients


@squash_api.app.route('/get_recipes', methods=['POST'])
def get_recipes():
    data = request.get_json()
    print("DATA", data)
    meal = data.get("food_type")
    inventory = get_inventory1() # dictionary {'fridge':[], 'pantry': []}
    res=""    
    for type in inventory:
        for item in inventory[type]:
            res+= f"{item['name']}, {item['quantity']}, {item['unit']}"


    prompt = (
        f"{res}: using these ingredients along with their quantities and units, "
        f"give me 3 {meal} recipes for a dish in the following format e.g.\n"
        f"""[
    {{
        "name": "Spaghetti Carbonara",
        "ingredients": [
        {{ "ingredient_name": "Spaghetti", "quantity": "200g" }},
        {{ "ingredient_name": "Eggs", "quantity": "3" }},
        {{ "ingredient_name": "Parmesan cheese", "quantity": "100g" }},
        {{ "ingredient_name": "Bacon", "quantity": "100g" }},
        {{ "ingredient_name": "Black pepper", "quantity": "to taste" }}
        ],
        "instructions": [
        "Cook the spaghetti in salted boiling water until al dente.",
        "In a bowl, whisk together eggs and grated Parmesan cheese.",
        "Fry the bacon until crispy, then mix with drained spaghetti.",
        "Remove from heat and quickly stir in the egg mixture.",
        "Serve immediately, topped with black pepper."
        ],
        "time": "20 minutes"
    }}
    ]\n"""
        f"Make sure the final output is PROPER JSON format and matches this structure exactly."
    )


    return flask.jsonify(gemini_generator(prompt)), 201



def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


@squash_api.app.route('/upload_receipt/', methods=["POST"])
def upload_receipt():
    # print(request.files)
    print('Akhil')
    output = json.loads(request.get_data())
    image_file = output["data"]

    text = scan_receipts(image_file)

    date_str = f"Today's date is {datetime.now().date()}. Message = "
    prompt = date_str+ "This is the current date " + text + """: convert this into JSON format. Generalize the food items i.e. make lowercase and ensure spelling is correct and plural. Divide weight by average weight of item to obtain count. If an expiry date is not given, add the average expiry time onto the current date. Only output the JSON. 

    Use this JSON schema:

    Food = {"name": str, "count": int, "expiry": date}
    Return: {"pantry": list[Food], "fridge": list[Food]}
    Make sure the final output is in PROPER JSON format
    """

    # Generate the response using gemini_generator
    response = gemini_generator(prompt)
    for type in response:
        for food in response[type]:
            insert_food(type, food['name'], food['count'], None, food['expiry'])
    # print(response_data)

    return jsonify(response), 201


@squash_api.app.route('/upload_speech',methods=['POST'])
def upload_speech():
    data = request.get_json()
    base64_audio = data.get('transcript')

    if not base64_audio:
        return jsonify({'error': 'No audio data provided'}), 400

    # Decode the Base64 string to binary
    audio_data = base64.b64decode(base64_audio)

    # Save the decoded audio data to a file
    audio_file_path = "recording.wav"
    with open(audio_file_path, 'wb') as audio_file:
        audio_file.write(audio_data)

    # Convert to WAV using Pydub (if needed)
    sound = AudioSegment.from_file(audio_file_path)
    sound.export(audio_file_path, format="wav")

    model = whisper.load_model("base")
    # Transcribe the audio using Whisper
    result = model.transcribe(audio_file_path)

    text = result['text']
   
    print("Transcribed Text:", text)

    date_str = f"Today's date is {datetime.now().date()}. Message = "
    prompt = date_str + text + """: convert this into JSON format. Only output the JSON.

        Use this JSON schema:

        Food = {"name": str, count": int, "expiry": date}
        Return: {"pantry": list[Food], "fridge": list[Food]
        Make sure the final output is in PROPER JSON format
        """
    response = gemini_generator(prompt)
    
    for type in response:
        for food in response[type]:
          
            insert_food(type,food['name'], food['count'], None, food['expiry'])
    return jsonify(response), 200

def get_location():
    try:
        # Make a request to the ipinfo API
        response = requests.get('https://ipinfo.io/')

        # If the request was successful
        if response.status_code == 200:
            # Parse the JSON data
            data = response.json()
            # Extract location information
            location = {
                'Location': data.get('loc')  # Latitude and Longitude
            }
            return location
        else:
            return None
    except Exception as e:
        return str(e)


def get_nearby_food_banks(latitude, longitude):
    # Google Places API Text Search URL
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    # Define parameters
    params = {
        'query': 'food bank',
        'location': f'{latitude},{longitude}',
        'radius': 2000,
        'key': google_maps_key
    }

    # Make the request to Google Places API
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        return response.json().get('results', [])
    else:
        print("Error:", response.status_code, response.text)
        return None

# Function to get additional details of a place (such as phone number and opening hours)
def get_place_details(place_id):
    # Google Places API Details URL
    url = "https://maps.googleapis.com/maps/api/place/details/json"

    # Define parameters
    params = {
        'place_id': place_id,
        'fields': 'name,vicinity,formatted_phone_number,opening_hours',
        'key': google_maps_key
    }

    # Make the request to Google Places API
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        return response.json().get('result', {})
    else:
        print("Error:", response.status_code, response.text)
        return None


def calculate_distance(lat1, lon1, lat2, lon2):
    # Radius of Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Difference in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula to calculate the distance
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in kilometers
    distance = R * c
    return distance


@squash_api.app.route('/find_food_banks', methods=['GET'])
def find_food_banks():
    # Google Places API Nearby Search URL
    # url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    latitude,longitude = get_location()['Location'].strip().split(',')
    # Define parameters
    nearby_places = get_nearby_food_banks(latitude, longitude)

    food_banks_list = []

    if nearby_places:
        # Iterate over each place to get more details
        for place in nearby_places:
            place_id = place.get('place_id')
            bank_lat = place.get('geometry', {}).get('location', {}).get('lat')
            bank_lng = place.get('geometry', {}).get('location', {}).get('lng')

            # Fetch detailed information for each place
            details = get_place_details(place_id)

            if details:
                name = details.get('name')
                address = details.get('vicinity')
                phone_number = details.get('formatted_phone_number', 'N/A')  # Phone number might not always be available
                opening_hours = details.get('opening_hours', {}).get('weekday_text', 'N/A')  # Opening hours might not always be available

                # Calculate the distance from the current location
                distance = calculate_distance(float(latitude), float(longitude), bank_lat, bank_lng)
                if distance <= 5:
                # Add the food bank details to the list as a dictionary, including the distance
                    food_banks_list.append({
                        'name': name,
                        'address': address,
                        'phone_number': phone_number,
                        'opening_hours': opening_hours,
                        'distance_km': distance
                    })

        # Sort the food banks by distance from the provided location
        food_banks_list.sort(key=lambda x: x['distance_km'])
        # Return the sorted food banks as JSON
        return jsonify(food_banks_list), 200

    else:
        return jsonify({"error": "No nearby food banks found."}), 404


'''
THESE ARE WHEN AARYA IS PUSHING BUTTONS OR TRYING TO SEE ALL
'''
# @squash_api.app.route('/add_food', methods=['POST'])
# def add_food():
#     location, food_name, quantity, expiry_date = flask.request.args.get('location'), flask.request.args.get('food_name'), flask.request.args.get('quantity'), flask.request.args.get('date')
#     insert_food(location, food_name, quantity, expiry_date)


# @squash_api.app.route('/delete_food', methods=['POST'])
# def delete_food():
#     pass

# @squash_api.app.route('/get_inventory', methods=['GET'])
# def get_inventory():
#     # a list of tuples
#     get_inventory1()


# @squash_api.app.route("/add_food/<collection: str>/<item_name: str>/<quantity: int>/<unit: str>/<expiryDate: str>",methods=['POST'])
def insert_food(collection, item_name, quantity, unit, expiryDate):
    db_collection = db[collection]
    db_collection.insert_one({"name": item_name, "quantity": quantity, "unit": unit, "expiryDate": expiryDate})


# @squash_api.app.route("/count/<collection: str>/<name: str>",methods=['GET'])
def get_count(collection, item_name):
    results = db[collection].find({"name": item_name})
    amount = 0
    for result in results:
        amount += result["quantity"]
    # print(amount)
    return amount

# @squash_api.app.route("/delete/<collection: str>/<item_name: str>/<amount: int>",methods=['POST'])
def delete_food(collection, item_name, amount): #amount = 4
    foods = db[collection].find({"name": item_name}).sort({"expiryDate": 1}).to_list()
    total = 0 # 8
    for food in foods:
        total += food["quantity"]
    removed = 0
    i = 0
    while removed < amount and i < len(foods):
        food = foods[i]
        if food["quantity"] <= amount - removed:
            db[collection].delete_one({"_id": food["_id"]})
            removed += food["quantity"]
            i += 1
        else:
            db[collection].update_one({"_id": food["_id"]}, {"$set": {"quantity": food["quantity"] - (amount - removed)}})
            removed = amount

@squash_api.app.route("/inventory",methods=['GET'])
def get_inventory1():
    collections = db.list_collection_names()
    all_documents = {'fridge':[], 'pantry':[]}
    visited = set()
    for collection_name in collections:
        collection = db[collection_name]
        documents = collection.find()
        for document in documents:
            if document["name"] not in visited:
                item_info = {"name": document["name"], "quantity": get_count(collection_name, document["name"]), "unit": document["unit"]}
                all_documents[collection_name].append(item_info)
                visited.add(document["name"])
    return all_documents







