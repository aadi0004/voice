# import os
# from dotenv import load_dotenv
# import assemblyai as aai
# from elevenlabs.client import ElevenLabs
# from openai import OpenAI
# import pygame
# import tempfile
# import io

# # Load environment variables from .env
# load_dotenv()

# class AI_Assistant:
#     def __init__(self):
#         # Load API keys
#         aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
#         self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#         self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

#         self.transcriber = None

#         # Initialize pygame mixer for audio playback
#         pygame.mixer.init()

#         # Initial prompt for OpenAI
#         self.full_transcript = [
#             {"role": "system", "content": "You are a receptionist at a dental clinic. Be resourceful and efficient."},
#         ]

#     ###### Step 2: Real-Time Transcription with AssemblyAI ######
#     def start_transcription(self):
#         self.transcriber = aai.RealtimeTranscriber(
#             sample_rate=16000,
#             on_data=self.on_data,
#             on_error=self.on_error,
#             on_open=self.on_open,
#             on_close=self.on_close,
#             end_utterance_silence_threshold=1000
#         )

#         self.transcriber.connect()
#         microphone_stream = aai.extras.MicrophoneStream(sample_rate=16000)
#         self.transcriber.stream(microphone_stream)

#     def stop_transcription(self):
#         if self.transcriber:
#             self.transcriber.close()
#             self.transcriber = None

#     def on_open(self, session_opened: aai.RealtimeSessionOpened):
#         print("Session ID:", session_opened.session_id)

#     def on_data(self, transcript: aai.RealtimeTranscript):
#         if not transcript.text:
#             return

#         if isinstance(transcript, aai.RealtimeFinalTranscript):
#             self.generate_ai_response(transcript)
#         else:
#             print(transcript.text, end="\r")

#     def on_error(self, error: aai.RealtimeError):
#         print("An error occurred:", error)

#     def on_close(self):
#         print("Transcription session closed.")

#     ###### Step 3: Pass transcript to OpenAI ######
#     def generate_ai_response(self, transcript):
#         self.stop_transcription()

#         self.full_transcript.append({"role": "user", "content": transcript.text})
#         print(f"\nPatient: {transcript.text}\n")

#         try:
#             response = self.openai_client.chat.completions.create(
#                 model="gpt-3.5-turbo",
#                 messages=self.full_transcript
#             )
#             ai_response = response.choices[0].message.content
#             self.generate_audio(ai_response)
#         except Exception as e:
#             print(f"Error generating AI response: {e}")

#         self.start_transcription()
#         print("\nReal-time transcription resumed.\n")

#     ###### Step 4: Generate and play audio with ElevenLabs and pygame ######
#     def generate_audio(self, text):
#         self.full_transcript.append({"role": "assistant", "content": text})
#         print(f"\nAI Receptionist: {text}")

#         try:
#             client = ElevenLabs(api_key=self.elevenlabs_api_key)

#             # Generate audio stream
#             audio_stream = client.generate(
#                 text=text,
#                 voice="Rachel",
#                 stream=True
#             )

#             # Save audio to a temporary file
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
#                 for chunk in audio_stream:
#                     temp_audio_file.write(chunk)
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
#     ai_assistant = AI_Assistant()
#     ai_assistant.generate_audio(greeting)
#     ai_assistant.start_transcription()


import os
from dotenv import load_dotenv
import speech_recognition as sr
from transformers import pipeline
from gtts import gTTS
import pygame
import tempfile
import time

# Load environment variables from .env (optional, as no API keys are needed)
load_dotenv()

class AI_Assistant:
    def __init__(self):
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Initialize Hugging Face text generation pipeline
        self.text_generator = pipeline("text-generation", model="distilgpt2")

        # Initialize pygame mixer for audio playback
        pygame.mixer.init()

        # Initial prompt for text generation
        self.full_transcript = [
            {"role": "system", "content": "You are a receptionist at a dental clinic. Be resourceful and efficient."},
        ]

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

    ###### Step 3: Generate AI response with Hugging Face ######
    def generate_ai_response(self, transcript):
        self.full_transcript.append({"role": "user", "content": transcript})
        
        # Prepare prompt for distilgpt2
        prompt = f"System: You are a receptionist at a dental clinic. Be resourceful and efficient.\nPatient: {transcript}\nReceptionist:"
        
        try:
            # Generate response
            response = self.text_generator(prompt, max_length=100, num_return_sequences=1, truncation=True)[0]["generated_text"]
            # Extract the receptionist part
            ai_response = response.split("Receptionist:")[-1].strip()
            self.full_transcript.append({"role": "assistant", "content": ai_response})
            self.generate_audio(ai_response)
        except Exception as e:
            print(f"Error generating AI response: {e}")

    ###### Step 4: Generate and play audio with gTTS and pygame ######
    def generate_audio(self, text):
        print(f"\nAI Receptionist: {text}")
        try:
            # Generate audio with gTTS
            tts = gTTS(text=text, lang="en")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
                tts.save(temp_audio_file.name)
                temp_audio_file_path = temp_audio_file.name

            # Play audio using pygame
            pygame.mixer.music.load(temp_audio_file_path)
            pygame.mixer.music.play()

            # Wait until playback is finished
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            # Clean up temporary file
            pygame.mixer.music.unload()
            os.remove(temp_audio_file_path)

        except Exception as e:
            print(f"Error generating or playing audio: {e}")

    def __del__(self):
        # Clean up pygame mixer
        pygame.mixer.quit()

if __name__ == "__main__":
    greeting = "Thank you for calling Vancouver dental clinic. My name is Sandy, how may I assist you?"
    try:
        ai_assistant = AI_Assistant()
        ai_assistant.generate_audio(greeting)
        ai_assistant.start_transcription()
    except KeyboardInterrupt:
        print("\nShutting down...")