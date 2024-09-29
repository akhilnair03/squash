from datetime import datetime
import squash
import flask
from ...utils.mongo import *


@squash.app.route('/get_recipes', methods=['POST'])
def get_recipes():
    meal = flask.request.args.get('food_type')
    inventory = get_inventory1() # dictionary {'fridge':[], 'pantry': []}
    res=""    
    for type in inventory:
        for item in type:
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
    # prompt = (
    #     f"{res}: using these ingredients along with their quantities and units, "
    #     f"give me 3 {meal} recipes for a dish in the following format e.g. "
    #     f'[{{"name": "pasta", "ingredients": [{"ingredient_name": "pasta sauce", "quantity": "5oz"}, {"ingredient_name": "frozen veggies", "quantity": "0.2lbs"}] '
    #     f'"ravioli: 0.1 lbs"], "instructions": ["Boil the pasta", "Add spices", "..."], '
    #     f'"time": "20 mins"}}]\n'
    #     f"Use this JSON schema:\n\n"
    #     f'Food = {{"name": str, "count": int, "expiry": date}}\n'
    #     f'Return: {{"pantry": list[Food], "fridge": list[Food]}}'
    #     f"Make sure the final output is PROPER JSON format"
    # )

    return flask.jsonify(**gemini_generator(prompt)), 201

@squash.app.route('/upload_receipt', methods=['POST'])
def upload_reciept():
    date_str = f"Today's date is {datetime.now().date()}. Message = "
    img = flask.request.args.get('data')

    #text will be equal to results of scan reciept
    text = scan_receipts(img)

    prompt = date_str + text + """: convert this into JSON format. Generalize the food items i.e. make lowercase and ensure spelling is correct and plural. Divide weight by average weight of item to obtain count. Only output the JSON. 

        Use this JSON schema:

        Food = {"name": str, count": int, "expiry": date}
        Return: {"pantry": list[Food], "fridge": list[Food]
        Make sure the final output is in PROPER JSON format
        """

    return flask.jsonify(**gemini_generator(prompt)), 201


@squash.app.route('/upload_speech',methods=['POST'])
def upload_speech():
    transcript = flask.request.args.get('transcript')
    date_str = f"Today's date is {datetime.now().date()}. Message = "
    prompt = date_str + transcript + """: convert this into JSON format. Only output the JSON.

        Use this JSON schema:

        Food = {"name": str, count": int, "expiry": date}
        Return: {"pantry": list[Food], "fridge": list[Food]
        Make sure the final output is in PROPER JSON format
        """
    
    return flask.jsonify(**gemini_generator(prompt)), 201




'''
THESE ARE WHEN AARYA IS PUSHING BUTTONS OR TRYING TO SEE ALL
'''
@squash.app.route('/add_food', methods=['POST'])
def add_food():
    location, food_name, quantity, expiry_date = flask.request.args.get('location'), flask.request.args.get('food_name'), flask.request.args.get('quantity'), flask.request.args.get('date')
    insert_food(location, food_name, quantity, expiry_date)
    

@squash.app.route('/delete_food', methods=['POST'])
def delete_food():
    pass

@squash.app.route('/get_inventory', methods=['GET'])
def get_inventory():

    # a list of tuples
    get_inventory1()

    pass








