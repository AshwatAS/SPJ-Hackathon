import base64
import os
from google import genai
from google.genai import types

def generate(user_food_question):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    files = [client.files.upload(file="restaurant_menu_final_expanded.csv")]
    model = "gemini-2.0-flash"
    
    while True:
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_uri(file_uri=files[0].uri, mime_type=files[0].mime_type),
                    types.Part.from_text(text=user_food_question),
                ],
            ),
        ]
        generate_content_config = types.GenerateContentConfig(
            temperature=1,
            top_p=0.95,
            top_k=40,
            max_output_tokens=8192,
            response_mime_type="text/plain",
            system_instruction=[
                types.Part.from_text(text="""You are a restaurant assistant who has to use the restaurant menu to answer the customer's questions. You can also suggest suitable meal combos to customers according to their needs. Please only use the restaurant menu to recommend dishes."""),
            ],
        )
        
        full_string = ""
        for chunk in client.models.generate_content_stream(
            model=model, contents=contents, config=generate_content_config
        ):
            full_string += chunk.text
        
        print("🤖 Assistant:", full_string)
        user_food_question = input("🧑 You: ")
        if user_food_question.lower() == "stop":
            break
    
    return "Session ended."

def clinic_booking(user_appointment_query):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    files = [client.files.upload(file="updated_clinic_appointments.csv")]
    model = "gemini-2.0-flash"
    
    while True:
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_uri(file_uri=files[0].uri, mime_type=files[0].mime_type),
                    types.Part.from_text(text=user_appointment_query),
                ],
            ),
        ]
        generate_content_config = types.GenerateContentConfig(
            temperature=1,
            top_p=0.95,
            top_k=40,
            max_output_tokens=8192,
            response_mime_type="text/plain",
            system_instruction=[
                types.Part.from_text(text="""You are a clinic booking assistant who has to assist customers with booking an appointment based on the data provided to you."""),
            ],
        )
        
        full_string = ""
        for chunk in client.models.generate_content_stream(
            model=model, contents=contents, config=generate_content_config
        ):
            full_string += chunk.text
        
        print("🤖 Assistant:", full_string)
        user_appointment_query = input("🧑 You: ")
        if user_appointment_query.lower() == "stop":
            break
    
    return "Session ended."
