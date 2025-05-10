# import os
# from dotenv import load_dotenv
# import speech_recognition as sr
# import google.generativeai as genai
# from gtts import gTTS
# import pygame
# import tempfile
# import time

# # Load environment variables from .env
# load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# class AI_Assistant:
#     def __init__(self):
#         # Initialize speech recognizer
#         self.recognizer = sr.Recognizer()
#         self.microphone = sr.Microphone()

#         # Initialize Gemini model for chat
#         self.model = genai.GenerativeModel("gemini-2.0-flash")
#         self.chat = self.model.start_chat(history=[
#             {"role": "user", "parts": ["You are a receptionist at a dental clinic. Be resourceful, efficient, and friendly."]},
#             {"role": "model", "parts": ["Got it! I'm ready to assist as a friendly dental clinic receptionist. How can I help you today?"]}])

#         # Initialize pygame mixer for audio playback
#         pygame.mixer.init()

#     ###### Step 2: Real-Time Transcription with speech_recognition ######
#     def start_transcription(self):
#         print("Listening... Speak now.")
#         with self.microphone as source:
#             self.recognizer.adjust_for_ambient_noise(source)
#             while True:
#                 try:
#                     # Capture audio
#                     audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
#                     # Transcribe using Google Speech-to-Text
#                     try:
#                         transcript = self.recognizer.recognize_google(audio)
#                         if transcript.strip():
#                             print(f"\nPatient: {transcript}\n")
#                             self.generate_ai_response(transcript)
#                         else:
#                             print("No speech detected, continuing to listen...")
#                     except sr.UnknownValueError:
#                         print("Could not understand audio, continuing to listen...")
#                     except sr.RequestError as e:
#                         print(f"Google API error: {e}, continuing to listen...")
#                 except KeyboardInterrupt:
#                     print("\nStopping transcription...")
#                     break
#                 except Exception as e:
#                     print(f"Error during transcription: {e}")
#                     time.sleep(1)  # Prevent rapid looping on errors

#     ###### Step 3: Generate AI response with Gemini ######
#     def generate_ai_response(self, transcript):
#         try:
#             # Send user input to Gemini
#             response = self.chat.send_message(transcript)
#             ai_response = response.text.strip()
#             self.generate_audio(ai_response)
#         except Exception as e:
#             print(f"Error generating AI response: {e}")

#     ###### Step 4: Generate and play audio with gTTS and pygame ######
#     def generate_audio(self, text):
#         print(f"\nAI Receptionist: {text}")
#         try:
#             # Generate audio with gTTS
#             tts = gTTS(text=text, lang="en")
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
#                 tts.save(temp_audio_file.name)
#                 temp_audio_file_path = temp_audio_file.name

#             # Play audio using pygame
#             pygame.mixer.music.load(temp_audio_file_path)
#             pygame.mixer.music.play()

#             # Wait until playback is finished
#             while pygame.mixer.music.get_busy():
#                 pygame.time.Clock().tick(10)

#             # Clean up temporary file
#             pygame.mixer.music.unload()
#             os.remove(temp_audio_file_path)

#         except Exception as e:
#             print(f"Error generating or playing audio: {e}")

#     def __del__(self):
#         # Clean up pygame mixer
#         pygame.mixer.quit()

# if __name__ == "__main__":
#     greeting = "Thank you for calling Vancouver dental clinic. My name is Sandy, how may I assist you?"
#     try:
#         ai_assistant = AI_Assistant()
#         ai_assistant.generate_audio(greeting)
#         ai_assistant.start_transcription()
#     except KeyboardInterrupt:
#         print("\nShutting down...")

import os
from dotenv import load_dotenv
import speech_recognition as sr
import google.generativeai as genai
import pyttsx3
import time

# Load environment variables from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class AI_Assistant:
    def __init__(self):
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Initialize Gemini model for chat
        self.model = genai.GenerativeModel("gemini-2.0-flash")
        self.chat = self.model.start_chat(history=[
            {"role": "user", "parts": ["You are a receptionist at a dental clinic. Be resourceful, efficient, and friendly."]},
            {"role": "model", "parts": ["Got it! I'm ready to assist as a friendly dental clinic receptionist. How can I help you today?"]}])

        # Initialize pyttsx3 for text-to-speech
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)  # Speed up speech
        self.tts_engine.setProperty('volume', 0.9)  # Set volume (0.0 to 1.0)

    ###### Step 2: Real-Time Transcription with speech_recognition ######
    def start_transcription(self):
        print("Listening... Speak now.")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while True:
                try:
                    # Capture audio
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    # Transcribe using Google Speech-to-Text
                    try:
                        transcript = self.recognizer.recognize_google(audio)
                        if transcript.strip():
                            print(f"\nPatient: {transcript}\n")
                            self.generate_ai_response(transcript)
                        else:
                            print("No speech detected, continuing to listen...")
                    except sr.UnknownValueError:
                        print("Could not understand audio, continuing to listen...")
                    except sr.RequestError as e:
                        print(f"Google API error: {e}, continuing to listen...")
                except KeyboardInterrupt:
                    print("\nStopping transcription...")
                    break
                except Exception as e:
                    print(f"Error during transcription: {e}")
                    time.sleep(1)  # Prevent rapid looping on errors

    ###### Step 3: Generate AI response with Gemini ######
    def generate_ai_response(self, transcript):
        try:
            # Send user input to Gemini
            response = self.chat.send_message(transcript)
            ai_response = response.text.strip()
            self.generate_audio(ai_response)
        except Exception as e:
            print(f"Error generating AI response: {e}")

    ###### Step 4: Generate and play audio with pyttsx3 ######
    def generate_audio(self, text):
        print(f"\nAI Receptionist: {text}")
        try:
            # Use pyttsx3 to speak the text directly
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"Error generating or playing audio: {e}")

    def __del__(self):
        # Clean up pyttsx3 engine
        self.tts_engine.stop()

if __name__ == "__main__":
    greeting = "Thank you for calling Vancouver dental clinic. My name is Sandy, how may I assist you?"
    try:
        ai_assistant = AI_Assistant()
        ai_assistant.generate_audio(greeting)
        ai_assistant.start_transcription()
    except KeyboardInterrupt:
        print("\nShutting down...")