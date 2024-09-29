import google.generativeai as genai
import os
from datetime import datetime
import json

# genai.configure(api_key=os.environ["API_KEY"])
genai.configure(api_key="AIzaSyAgIxIIgq7FXBexx6G_Xm-5Y1SUpGpO-PA")
model = genai.GenerativeModel("gemini-1.5-pro-latest")

date_str = f"Today's date is {datetime.now().date()}. Message = "
# audio_input = "2 apples in a few days, 3 bananas in around 5 days, 8 eggs in 3 days"
# audio_input = "pub diced tomatoes, publix tom/paste, pf w/g wheat bread"
audio_input = "DRAGON FRUIT,BANNAS,2.28 1b @,WHOLE CHICKEN,Order Total,Sales Tax,Food Tax,Grand Total,CREDIT,Change,PRESTO,Public's Store,Store Plaza,1425 Store Drive,Jacksonville, FL, 23231,TEL : +1 888 888 8888,19.71,0.00,0.39,20.10,20.10,0.00,0.55/1b,Payment,3.gg F,1.25 F,14.47 F,Trace,Reference #:,Acct,Purchase #:,Amount,Auth,CREDIT CARD,607539868888,Entry Method:,Mode:,124868,696905034,xxxxxxxxxxxxgggg,VISA,20.10,186707,PURCHASE,VISA,Chip Read,Issuer,Your cashier was Eminem Martin,11/02/2020 17:06 S2353 R2991 03134 C1208,Together, we'll get through this COVID-19,Situation.,Super Market"
prompt = date_str + audio_input + """: convert this into JSON format. Generalize the food items i.e. make lowercase and ensure spelling is correct and plural. Divide weight by average weight of item to obtain count. Only output the JSON. 

Use this JSON schema:

Food = {"name": str, count": int, "expiry": date}
Return: {"pantry": list[Food], "fridge": list[Food]"""
result = model.generate_content(prompt)
generated_json = result.text
clean_json = generated_json.replace("```json", "").replace("```", "").strip()
ingredients = json.loads(clean_json)
print(ingredients)


