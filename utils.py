# import base64
# import os
# from google import genai
# from google.genai import types


# def generate(user_food_question):
#     client = genai.Client(
#         api_key="AIzaSyAdTTU2UGP0Q9qo7Kq6aqubovcz4FdOZ8Q",
#     )

#     files = [
#         # Make the file available in local system working directory
#         client.files.upload(file="restaurant_menu_final_expanded.csv"),
#     ]
#     model = "gemini-2.0-flash"
#     contents = [
#         types.Content(
#             role="user",
#             parts=[
#                 types.Part.from_uri(
#                     file_uri=files[0].uri,
#                     mime_type=files[0].mime_type,
#                 ),
#                 types.Part.from_text(text=user_food_question),
#             ],
#         ),
#     ]
#     generate_content_config = types.GenerateContentConfig(
#         temperature=1,
#         top_p=0.95,
#         top_k=40,
#         max_output_tokens=8192,
#         response_mime_type="text/plain",
#         system_instruction=[
#             types.Part.from_text(text="""You are a restaurant assistant who has to use the resturant menu to answer the customer's questions. You can also suggest suitable meal combos to customers according to their needs. Please only use the restaurant menu to recommend dishes."""),
#         ],
#     )
#     full_string=""
#     for chunk in client.models.generate_content_stream(
#         model=model,
#         contents=contents,
#         config=generate_content_config,
#     ):
#         full_string=full_string+chunk.text
        
#     return full_string





# def clinic_booking(user_appointment_query):
#     client = genai.Client(
#         api_key="AIzaSyAdTTU2UGP0Q9qo7Kq6aqubovcz4FdOZ8Q",
#     )

#     files = [
#         # Make the file available in local system working directory
#         client.files.upload(file="updated_clinic_appointments.csv"),
#     ]
#     model = "gemini-2.0-flash"
#     contents = [
#         types.Content(
#             role="user",
#             parts=[
#                 types.Part.from_uri(
#                     file_uri=files[0].uri,
#                     mime_type=files[0].mime_type,
#                 ),
#                 types.Part.from_text(text=user_appointment_query),
#             ],
#         ),
#     ]
#     generate_content_config = types.GenerateContentConfig(
#         temperature=1,
#         top_p=0.95,
#         top_k=40,
#         max_output_tokens=8192,
#         response_mime_type="text/plain",
#         system_instruction=[
#             types.Part.from_text(text="""You are a clinic booking assistant who has to assist customers with booking an appointment based on the data provided to you."""),
#         ],
#     )
#     full_string=""
#     for chunk in client.models.generate_content_stream(
#         model=model,
#         contents=contents,
#         config=generate_content_config,
#     ):
#         full_string=full_string+chunk.text
        
#     return full_string


from google import genai
from google.genai import types
import os

# Initialize clients and upload files once
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Upload files and store references
menu_file = client.files.upload(file="restaurant_menu_final_expanded.csv")
clinic_file = client.files.upload(file="updated_clinic_appointments.csv")

# Common configuration
model = "gemini-2.0-flash"

def generate_conversation(history, new_input, chat_type):
    # Create configuration based on chat type
    if chat_type == "food":
        system_instruction = "You are a restaurant assistant helping with menu questions and meal recommendations."
        file_part = types.Part.from_uri(menu_file.uri, menu_file.mime_type)
    else:
        system_instruction = "You are a clinic booking assistant helping with appointment scheduling."
        file_part = types.Part.from_uri(clinic_file.uri, clinic_file.mime_type)

    # Add initial file context if first message
    if not history:
        history = [
            types.Content(
                role="user",
                parts=[file_part, types.Part.from_text("Hello")]
        )

    # Append new user message
    history.append(types.Content(
        role="user",
        parts=[types.Part.from_text(new_input)]
    ))

    # Generate response
    config = types.GenerateContentConfig(
        temperature=0.9,
        top_p=0.95,
        max_output_tokens=8192,
        system_instruction=system_instruction
    )

    full_response = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=history,
        config=config,
    ):
        full_response += chunk.text

    # Append assistant response to history
    history.append(types.Content(
        role="model",
        parts=[types.Part.from_text(full_response)]
    ))

    return full_response, history
