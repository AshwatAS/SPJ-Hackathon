from google import genai
from google.genai import types
import os

# Initialize clients and upload files once
client = genai.Client(api_key="AIzaSyAdTTU2UGP0Q9qo7Kq6aqubovcz4FdOZ8Q")

# Upload files and store references
menu_file = client.files.upload(file="restaurant_menu_final_expanded.csv")
clinic_file = client.files.upload(file="updated_clinic_appointments.csv")

# Common configuration
model = "gemini-2.0-flash"

def generate_conversation(history, new_input, chat_type):
    # Create configuration based on chat type
    if chat_type == "food":
        system_instruction = "You are a restaurant assistant helping with menu questions and meal recommendations."
        file_part = types.Part.from_uri(
            file_uri=menu_file.uri,
            mime_type=menu_file.mime_type
        )
    else:
        system_instruction = "You are a clinic booking assistant helping with appointment scheduling."
        file_part = types.Part.from_uri(
            file_uri=clinic_file.uri,
            mime_type=clinic_file.mime_type
        )

    # Add initial file context if first message
    if not history:
        history = [
            types.Content(
                role="user",
                parts=[
                    file_part,
                    types.Part.from_text(text="Hello")  # Fixed here
                ]
            )
        ]

    # Append new user message
    history.append(types.Content(
        role="user",
        parts=[types.Part.from_text(text=new_input)]  # Fixed here
    ))

    # Generate response
    config = types.GenerateContentConfig(
        temperature=0.9,
        top_p=0.95,
        max_output_tokens=8192,
        system_instruction=types.Part.from_text(text=system_instruction)  # Fixed here
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
        parts=[types.Part.from_text(text=full_response)]  # Fixed here
    ))

    return full_response, history
