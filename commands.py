import os
from colors import *
from pyautogui import screenshot
from dotenv import load_dotenv, find_dotenv
from google import genai
from PIL import Image
from io import BytesIO

def load_ai():
    _ = load_dotenv(find_dotenv())
    client = genai.Client()
    chat = client.chats.create(model="gemini-2.5-flash-lite")
    print(BRIGHT_GREEN + "gemini ready!" + RESET)
    return chat

def append_log(source: str, msg: str):
    match source:
        case "q":
            with open(file='responses.log', mode='a', encoding='utf-8') as f:
                f.write("Q: " + msg + "\n")
        case "a":
            with open(file='responses.log', mode='a', encoding='utf-8') as f:
                f.write("A: " + msg + "\n\n")
        case _:
            print(BRIGHT_RED + "invalid input" + RESET)

def text_response(chat: genai.chats.Chat, prompt: str, instructions: str):
    response = chat.send_message(
        prompt,
        config=genai.types.GenerateContentConfig(
            system_instruction=instructions,
        ),
    )

    print(BRIGHT_GREEN + response.text + RESET, end="")
    append_log("q", prompt)
    append_log("a", response.text)
    return response.text

def analyze_screenshot(chat: genai.chats.Chat, prompt: str, instructions: str):
    screenshot("screenshot.png")
    with open('screenshot.png', 'rb') as f:
        image_bytes = f.read()
    response = chat.send_message(
        message=[
            genai.types.Part.from_bytes(
                data=image_bytes,
                mime_type='image/png',
            ),
            prompt
        ],
        config=genai.types.GenerateContentConfig(
            system_instruction=instructions,
        ),
    )

    print(BRIGHT_GREEN + response.text + RESET, end="")
    append_log("q", prompt)
    append_log("a", response.text)
    return response.text

def generate_image(prompt: str):
    full_response = ""
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE'],
        )
    )

    for part in response.candidates[0].content.parts:
        if part.text is not None:
            full_response += part.text
        elif part.inline_data is not None:
            image = Image.open(BytesIO((part.inline_data.data)))
            image.save('gemini-native-image.png')
            os.startfile('gemini-native-image.png')
    
    print(BRIGHT_GREEN + full_response + RESET)
    append_log("q", prompt)
    append_log("a", full_response)
    return full_response