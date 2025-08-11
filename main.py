import commands
import os
import playsound3
import soundsystem
from datetime import datetime
from colors import *

voice_mode = False
voice_instructions = "You are a virtual assistant. You have a cold personality and always speak rationally and intelligently. You will always express rational, objective opinions based on truth, facts, and accurate information. Users may make typos, send incomplete messages, or give contradictory voice_instructions. If you notice something odd about a user's voice_instructions, always ask the user to clarify. If you notice a typographical error in a user's voice_instructions, make a precise and detailed assumption. Do not hallucinate. You must distinguish fact from imagination and be honest about what you don't know. Above all else, always keep your responses between 1 and 3 sentences."
text_instructions = ""

if __name__ == '__main__':
    client = commands.load_ai()

    soundsystem.load_stt()
    soundsystem.load_tts()
    soundsystem.start_keyboard()

    print(BRIGHT_BLUE + "JaffeBot 3.0 loaded at " + str(datetime.now()) + RESET)
    with open('responses.log', 'a') as f:
        f.write("\n" + str(datetime.now()) + "\n")
    playsound3.playsound("startup.wav")

    while True:
        answer = ""
        if voice_mode == True:
            if soundsystem.listener.running == False:
                soundsystem.start_keyboard()
            print("\nHold Insert or say 'Hey Google' and begin speaking.")

            # record voice
            query = soundsystem.recorder.text().lower()
            print(query)

            # interpret recording
            if "text mode" in query:
                voice_mode = False
            elif "open" in query and "log" in query:
                os.startfile('responses.log')
            elif "screenshot" in query:
                answer = commands.analyze_screenshot(client, query, voice_instructions)
            elif "generate" in query and "image" in query:
                answer = commands.generate_image(query)
            else:
                answer = commands.text_response(client, query, voice_instructions)

            # playback ai response
            soundsystem.playback_response(answer)
            
        else:
            if soundsystem.listener.running == True:
                soundsystem.stop_keyboard()
            query = input(BRIGHT_BLUE + "\n>>> " + RESET)

            match query:
                case "help" | "commands":
                    print(BRIGHT_YELLOW +
                        "help: bring up this screen\n" + 
                        "details: view model details\n" + 
                        "log: opens the log file\n" + 
                        "instructions: modify the model instructions\n" + 
                        "screenshot: takes a picture of your screen and sends it to gemini\n" + 
                        "anything else: gets sent to gemini for a response" + RESET)
                case "voice mode":
                    voice_mode = True
                case "log":
                    os.startfile('responses.log')
                case "folder":
                    os.startfile(".")
                case "instructions" | "system prompt":
                    text_instructions = input(BRIGHT_BLUE + "\n>>> Enter new instructions: " + RESET)
                case "screenshot":
                    answer = commands.analyze_screenshot(client, query, text_instructions)
                case "generate image":
                    query = input(BRIGHT_BLUE + "\n>>> Prompt for generating image: " + RESET)
                    answer = commands.generate_image(query)
                case _:
                    answer = commands.text_response(client, query, text_instructions)