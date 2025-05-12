# import os
# from dotenv import load_dotenv
# import speech_recognition as sr
# import google.generativeai as genai
# import pyttsx3
# import time
# import re

# # Load environment variables from .env
# load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# def clean_markdown(text):
#     """Remove markdown formatting characters (e.g., *, **, _) from text."""
#     # Remove * and ** used for bold/italic
#     text = re.sub(r'\*{1,2}(.*?)\*{1,2}', r'\1', text)
#     # Remove _ used for italic
#     text = re.sub(r'_(.*?)_', r'\1', text)
#     # Remove other common markdown (e.g., ``` for code blocks, # for headers)
#     text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
#     text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
#     # Remove extra whitespace
#     text = ' '.join(text.split())
#     return text.strip()

# class AI_Assistant:
#     def __init__(self):
#         # Initialize speech recognizer
#         self.recognizer = sr.Recognizer()
#         self.microphone = sr.Microphone()

#         # Initialize Gemini model for chat
#         self.model = genai.GenerativeModel("gemini-1.5-flash")  # Updated to a valid model
#         self.chat = self.model.start_chat(history=[
#             {"role": "user", "parts": ["You are a receptionist at a dental clinic. Be resourceful, efficient, and friendly."]},
#             {"role": "model", "parts": ["Got it! I'm ready to assist as a friendly dental clinic receptionist. How can I help you today?"]}
#         ])

#         # Initialize pyttsx3 for text-to-speech
#         self.tts_engine = pyttsx3.init()
#         self.tts_engine.setProperty('rate', 150)  # Speed up speech
#         self.tts_engine.setProperty('volume', 0.9)  # Set volume (0.0 to 1.0)

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
#             # Clean the response for speech
#             clean_response = clean_markdown(ai_response)
#             self.generate_audio(clean_response, ai_response)
#         except Exception as e:
#             print(f"Error generating AI response: {e}")

#     ###### Step 4: Generate and play audio with pyttsx3 ######
#     def generate_audio(self, clean_text, raw_text):
#         print(f"\nAI Receptionist: {raw_text}")
#         try:
#             # Use pyttsx3 to speak the cleaned text
#             self.tts_engine.say(clean_text)
#             self.tts_engine.runAndWait()
#         except Exception as e:
#             print(f"Error generating or playing audio: {e}")

#     def __del__(self):
#         # Clean up pyttsx3 engine
#         self.tts_engine.stop()

# if __name__ == "__main__":
#     greeting = "Thank you for calling Vancouver dental clinic. My name is Sandy, how may I assist you?"
#     try:
#         ai_assistant = AI_Assistant()
#         ai_assistant.generate_audio(greeting, greeting)  # Pass greeting as both clean and raw
#         ai_assistant.start_transcription()
#     except KeyboardInterrupt:
#         print("\nShutting down...")










# database



# import os
# from dotenv import load_dotenv
# import speech_recognition as sr
# import google.generativeai as genai
# import pyttsx3
# import time
# import re
# import mysql.connector
# from mysql.connector import Error

# # Load environment variables from .env
# load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# # MySQL configuration
# MYSQL_CONFIG = {
#     'host': 'localhost',
#     'database': 'dental_clinic',
#     'user': os.getenv("MYSQL_USER"),
#     'password': os.getenv("MYSQL_PASSWORD")
# }

# def clean_markdown(text):
#     """Remove markdown formatting characters (e.g., *, **, _) from text."""
#     text = re.sub(r'\*{1,2}(.*?)\*{1,2}', r'\1', text)
#     text = re.sub(r'_(.*?)_', r'\1', text)
#     text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
#     text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
#     text = ' '.join(text.split())
#     return text.strip()

# def connect_to_db():
#     """Connect to MySQL database."""
#     try:
#         connection = mysql.connector.connect(**MYSQL_CONFIG)
#         if connection.is_connected():
#             return connection
#     except Error as e:
#         print(f"Error connecting to MySQL: {e}")
#         return None
#     return None

# def create_appointments_table():
#     """Create appointments table if it doesn't exist."""
#     connection = connect_to_db()
#     if connection:
#         try:
#             cursor = connection.cursor()
#             create_table_query = """
#                 CREATE TABLE IF NOT EXISTS appointments (
#                     id INT AUTO_INCREMENT PRIMARY KEY,
#                     patient_name VARCHAR(255) NOT NULL,
#                     appointment_date DATE NOT NULL,
#                     appointment_time TIME NOT NULL,
#                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#                 )
#             """
#             cursor.execute(create_table_query)
#             connection.commit()
#             print("Appointments table ensured.")
#         except Error as e:
#             print(f"Error creating appointments table: {e}")
#         finally:
#             cursor.close()
#             connection.close()

# def save_interaction(patient_name, query, response):
#     """Save patient interaction to MySQL database."""
#     connection = connect_to_db()
#     if connection:
#         try:
#             cursor = connection.cursor()
#             query_sql = """
#                 INSERT INTO patient_interactions (patient_name, patient_query, ai_response)
#                 VALUES (%s, %s, %s)
#             """
#             cursor.execute(query_sql, (patient_name, query, response))
#             connection.commit()
#             print(f"Saved interaction for {patient_name} to database.")
#         except Error as e:
#             print(f"Error saving to database: {e}")
#         finally:
#             cursor.close()
#             connection.close()

# def save_appointment(patient_name, response):
#     """Parse AI response and save appointment details to database."""
#     # Simple regex to detect appointment details (e.g., "Appointment scheduled for 2025-05-15 at 14:30")
#     appointment_pattern = r"Appointment scheduled for (\d{4}-\d{2}-\d{2}) at (\d{2}:\d{2})"
#     match = re.search(appointment_pattern, response)
    
#     if match:
#         appointment_date = match.group(1)
#         appointment_time = match.group(2)
        
#         connection = connect_to_db()
#         if connection:
#             try:
#                 cursor = connection.cursor()
#                 query_sql = """
#                     INSERT INTO appointments (patient_name, appointment_date, appointment_time)
#                     VALUES (%s, %s, %s)
#                 """
#                 cursor.execute(query_sql, (patient_name, appointment_date, appointment_time))
#                 connection.commit()
#                 print(f"Saved appointment for {patient_name} on {appointment_date} at {appointment_time}.")
#             except Error as e:
#                 print(f"Error saving appointment: {e}")
#             finally:
#                 cursor.close()
#                 connection.close()
#     else:
#         print("No appointment details detected in response.")

# class AI_Assistant:
#     def __init__(self):
#         # Initialize speech recognizer
#         self.recognizer = sr.Recognizer()
#         self.microphone = sr.Microphone()

#         # Initialize Gemini model for chat
#         self.model = genai.GenerativeModel("gemini-1.5-flash")
#         self.chat = self.model.start_chat(history=[
#             {"role": "user", "parts": ["You are a receptionist at a dental clinic. Be resourceful, efficient, and friendly. When scheduling an appointment, include the date and time in the format: 'Appointment scheduled for YYYY-MM-DD at HH:MM'."]},
#             {"role": "model", "parts": ["Got it! I'm ready to assist as a friendly dental clinic receptionist. How can I help you today?"]}
#         ])

#         # Initialize pyttsx3 for text-to-speech
#         self.tts_engine = pyttsx3.init()
#         self.tts_engine.setProperty('rate', 150)
#         self.tts_engine.setProperty('volume', 0.9)

#         # Patient name
#         self.patient_name = "Unknown"

#         # Ensure appointments table exists
#         create_appointments_table()

#     def get_patient_name(self):
#         """Prompt for and capture patient name via speech with retry."""
#         max_attempts = 3
#         for attempt in range(max_attempts):
#             print(f"Attempt {attempt + 1}/{max_attempts}: Please say your name.")
#             self.generate_audio("Please say your name.", "Please say your name.")
#             with self.microphone as source:
#                 self.recognizer.adjust_for_ambient_noise(source, duration=1)
#                 try:
#                     audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=15)
#                     name = self.recognizer.recognize_google(audio).strip()
#                     if name:
#                         self.patient_name = name
#                         print(f"Patient name: {name}")
#                         self.generate_audio(f"Thank you, {name}. How may I assist you?",
#                                            f"Thank you, {name}. How may I assist you?")
#                         return
#                     else:
#                         print("No name detected.")
#                 except sr.WaitTimeoutError:
#                     print("Timeout: No speech detected within 10 seconds.")
#                 except sr.UnknownValueError:
#                     print("Could not understand audio.")
#                 except sr.RequestError as e:
#                     print(f"Google API error: {e}")
#                 except Exception as e:
#                     print(f"Error capturing name: {e}")

#             if attempt < max_attempts - 1:
#                 self.generate_audio("Sorry, I didn't catch your name. Please try again.",
#                                    "Sorry, I didn't catch your name. Please try again.")
#                 time.sleep(1)

#         print("No name detected after retries, using 'Unknown'.")
#         self.generate_audio("Sorry, I didn't catch your name. I'll proceed as Unknown. How may I assist you?",
#                            "Sorry, I didn't catch your name. I'll proceed as Unknown. How may I assist you?")

#     def start_transcription(self):
#         print("Listening... Speak now.")
#         with self.microphone as source:
#             self.recognizer.adjust_for_ambient_noise(source)
#             while True:
#                 try:
#                     audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=15)
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
#                     time.sleep(1)

#     def generate_ai_response(self, transcript):
#         try:
#             response = self.chat.send_message(transcript)
#             ai_response = response.text.strip()
#             clean_response = clean_markdown(ai_response)
#             self.generate_audio(clean_response, ai_response)
#             save_interaction(self.patient_name, transcript, ai_response)
#             save_appointment(self.patient_name, ai_response)
#         except Exception as e:
#             print(f"Error generating AI response: {e}")

#     def generate_audio(self, clean_text, raw_text):
#         print(f"\nAI Receptionist: {raw_text}")
#         try:
#             self.tts_engine.say(clean_text)
#             self.tts_engine.runAndWait()
#         except Exception as e:
#             print(f"Error generating or playing audio: {e}")

#     def __del__(self):
#         self.tts_engine.stop()

# if __name__ == "__main__":
#     greeting = "Thank you for calling Vancouver dental clinic. My name is Sandy, how may I assist you?"
#     try:
#         ai_assistant = AI_Assistant()
#         ai_assistant.generate_audio(greeting, greeting)
#         ai_assistant.get_patient_name()
#         ai_assistant.start_transcription()
#     except KeyboardInterrupt:
#         print("\nShutting down...")

import os
from dotenv import load_dotenv
import speech_recognition as sr
import google.generativeai as genai
import pyttsx3
import time
import re
import mysql.connector
from mysql.connector import Error
from twilio.rest import Client

# Load environment variables from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# MySQL configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'database': 'dental_clinic',
    'user': os.getenv("MYSQL_USER"),
    'password': os.getenv("MYSQL_PASSWORD")
}

# Twilio configuration
TWILIO_CONFIG = {
    'account_sid': os.getenv("TWILIO_ACCOUNT_SID"),
    'auth_token': os.getenv("TWILIO_AUTH_TOKEN"),
    'phone_number': os.getenv("TWILIO_PHONE_NUMBER")
}

def clean_markdown(text):
    """Remove markdown formatting characters (e.g., *, **, _) from text."""
    text = re.sub(r'\*{1,2}(.*?)\*{1,2}', r'\1', text)
    text = re.sub(r'_(.*?)_', r'\1', text)
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    text = ' '.join(text.split())
    return text.strip()

def clean_name(name):
    """Clean patient name by removing prefixes like 'my name is'."""
    prefixes = r'^(my name is|this is|i am)\s+'
    name = re.sub(prefixes, '', name, flags=re.IGNORECASE).strip()
    return name

def connect_to_db():
    """Connect to MySQL database."""
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
    return None

def update_tables():
    """Update database schema to ensure required columns exist and remove email."""
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            # Ensure phone_number column exists
            cursor.execute("SHOW COLUMNS FROM patients LIKE 'phone_number'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE patients ADD COLUMN phone_number VARCHAR(20)")
                print("Added phone_number column to patients table.")
            
            # Ensure sms_consent column exists
            cursor.execute("SHOW COLUMNS FROM patients LIKE 'sms_consent'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE patients ADD COLUMN sms_consent BOOLEAN DEFAULT TRUE")
                print("Added sms_consent column to patients table.")
            
            # Remove email column if it exists
            cursor.execute("SHOW COLUMNS FROM patients LIKE 'email'")
            if cursor.fetchone():
                cursor.execute("ALTER TABLE patients DROP COLUMN email")
                print("Removed email column from patients table.")
            
            connection.commit()
        except Error as e:
            print(f"Error updating tables: {e}")
        finally:
            cursor.close()
            connection.close()

def create_tables():
    """Create necessary tables if they don't exist and update schema."""
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            # Create patients table (no email column)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    patient_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    phone_number VARCHAR(20),
                    sms_consent BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            # Create appointments table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS appointments (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    patient_id INT NOT NULL,
                    appointment_date DATE NOT NULL,
                    appointment_time TIME NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
                )
            """)
            # Create patient_interactions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS patient_interactions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    patient_id INT NOT NULL,
                    patient_query TEXT NOT NULL,
                    ai_response TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
                )
            """)
            connection.commit()
            print("Tables ensured.")
            # Update schema to add missing columns and remove email
            update_tables()
        except Error as e:
            print(f"Error creating tables: {e}")
        finally:
            cursor.close()
            connection.close()

def save_interaction(patient_id, query, response):
    """Save patient interaction to MySQL database."""
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            query_sql = """
                INSERT INTO patient_interactions (patient_id, patient_query, ai_response)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query_sql, (patient_id, query, response))
            connection.commit()
            print(f"Saved interaction for patient ID {patient_id} to database.")
        except Error as e:
            print(f"Error saving to database: {e}")
        finally:
            cursor.close()
            connection.close()

def get_or_create_patient(name, phone_number=None, sms_consent=True):
    """Retrieve or create patient record in the database."""
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            # Check if patient exists
            cursor.execute("SELECT patient_id, phone_number, sms_consent FROM patients WHERE name = %s", (name,))
            result = cursor.fetchone()
            if result:
                patient_id, stored_phone, stored_consent = result
                update_needed = False
                if phone_number and stored_phone != phone_number:
                    update_needed = True
                if sms_consent != stored_consent:
                    update_needed = True
                if update_needed:
                    cursor.execute("UPDATE patients SET phone_number = %s, sms_consent = %s WHERE patient_id = %s",
                                   (phone_number or stored_phone, sms_consent, patient_id))
                    connection.commit()
                return patient_id, stored_phone or phone_number, stored_consent
            else:
                # Create new patient
                cursor.execute("INSERT INTO patients (name, phone_number, sms_consent) VALUES (%s, %s, %s)",
                               (name, phone_number, sms_consent))
                connection.commit()
                cursor.execute("SELECT LAST_INSERT_ID()")
                patient_id = cursor.fetchone()[0]
                return patient_id, phone_number, sms_consent
        except Error as e:
            print(f"Error managing patient: {e}")
        finally:
            cursor.close()
            connection.close()
    return None, None, True

def send_appointment_message(patient_name, patient_phone, sms_consent, appointment_date, appointment_time):
    """Send appointment confirmation via SMS."""
    if patient_phone and sms_consent:
        # Initialize Twilio client
        twilio_client = Client(TWILIO_CONFIG['account_sid'], TWILIO_CONFIG['auth_token'])
        from_number = TWILIO_CONFIG['phone_number']
        to_number = f"+91{patient_phone}" if not patient_phone.startswith('+') else patient_phone
        
        # SMS message body (under 160 characters)
        body = f"Hi {patient_name}, your appt at Vancouver Dental Clinic is on {appointment_date} at {appointment_time}. Call (555) 123-4567 to reschedule. Reply STOP to opt out. -Sandy"
        
        try:
            message = twilio_client.messages.create(
                body=body,
                from_=from_number,
                to=to_number
            )
            print(f"Appointment confirmation SMS sent to {patient_phone} (SID: {message.sid}).")
        except Exception as e:
            print(f"Error sending SMS: {e}")
    else:
        print("No valid phone number provided or SMS consent not given. Skipping message.")

def save_appointment(patient_id, patient_name, patient_phone, sms_consent, response):
    """Parse AI response and save appointment details to database."""
    appointment_pattern = r"Appointment scheduled for (\d{4}-\d{2}-\d{2}) at (\d{2}:\d{2})"
    match = re.search(appointment_pattern, response)
    
    if match:
        appointment_date = match.group(1)
        appointment_time = match.group(2)
        
        connection = connect_to_db()
        if connection:
            try:
                cursor = connection.cursor()
                query_sql = """
                    INSERT INTO appointments (patient_id, appointment_date, appointment_time)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(query_sql, (patient_id, appointment_date, appointment_time))
                connection.commit()
                print(f"Saved appointment for patient ID {patient_id} on {appointment_date} at {appointment_time}.")
                # Send SMS confirmation
                send_appointment_message(patient_name, patient_phone, sms_consent, appointment_date, appointment_time)
            except Error as e:
                print(f"Error saving appointment: {e}")
            finally:
                cursor.close()
                connection.close()
    else:
        print("No appointment details detected in response.")

class AI_Assistant:
    def __init__(self):
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Initialize Gemini model for chat
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.chat = self.model.start_chat(history=[
            {"role": "user", "parts": ["You are a receptionist at a dental clinic. Be resourceful, efficient, and friendly. When scheduling an appointment, include the date and time in the format: 'Appointment scheduled for YYYY-MM-DD at HH:MM'."]},
            {"role": "model", "parts": ["Got it! I'm ready to assist as a friendly dental clinic receptionist. How can I help you today?"]}
        ])

        # Initialize pyttsx3 for text-to-speech
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)
        self.tts_engine.setProperty('volume', 0.9)

        # Patient details
        self.patient_name = "Unknown"
        self.patient_id = None
        self.patient_phone = None
        self.sms_consent = True  # Default to True

        # Ensure tables exist and are updated
        create_tables()

    def cleanup(self):
        """Explicitly stop the TTS engine."""
        try:
            self.tts_engine.stop()
        except Exception as e:
            print(f"Error stopping TTS engine: {e}")

    def get_patient_details(self):
        """Prompt for and capture patient name and phone number via speech with retry."""
        max_attempts = 3

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=3)  # 3 seconds for noise adjustment

            # Get patient name
            for attempt in range(max_attempts):
                print(f"Attempt {attempt + 1}/{max_attempts}: Please say your name.")
                self.generate_audio("Please say your name.", "Please say your name.")
                try:
                    audio = self.recognizer.listen(source, timeout=15, phrase_time_limit=15)
                    name = self.recognizer.recognize_google(audio).strip()
                    print(f"Raw name input: {name}")
                    if name:
                        self.patient_name = clean_name(name)
                        print(f"Patient name: {self.patient_name}")
                        break
                    else:
                        print("No name detected.")
                except sr.WaitTimeoutError:
                    print("Timeout: No speech detected within 15 seconds.")
                except sr.UnknownValueError:
                    print("Could not understand audio.")
                except sr.RequestError as e:
                    print(f"Google API error: {e}")
                except Exception as e:
                    print(f"Error capturing name: {e}")

                if attempt < max_attempts - 1:
                    self.generate_audio("Sorry, I didn't catch your name. Please try again.",
                                       "Sorry, I didn't catch your name. Please try again.")
                    time.sleep(1)
            
            if self.patient_name == "Unknown":
                print("No name detected after retries, using 'Unknown'.")
                self.generate_audio("Sorry, I didn't catch your name. I'll proceed as Unknown.",
                                   "Sorry, I didn't catch your name. I'll proceed as Unknown.")

            # Check if patient exists or create new record
            self.patient_id, self.patient_phone, self.sms_consent = get_or_create_patient(self.patient_name)

            # Get patient phone number
            if not self.patient_phone:
                for attempt in range(max_attempts):
                    print(f"Attempt {attempt + 1}/{max_attempts}: Please say your phone number.")
                    self.generate_audio("Please say your phone number.", "Please say your phone number.")
                    try:
                        audio = self.recognizer.listen(source, timeout=15, phrase_time_limit=15)
                        phone = self.recognizer.recognize_google(audio).strip()
                        print(f"Raw phone input: {phone}")
                        phone = re.sub(r'\D', '', phone)  # Remove non-digits
                        if len(phone) >= 10:
                            self.patient_phone = phone[:10]  # Take first 10 digits
                            print(f"Patient phone: {self.patient_phone}")
                            self.patient_id, _, self.sms_consent = get_or_create_patient(
                                self.patient_name, self.patient_phone, self.sms_consent)
                            break
                        else:
                            print("Invalid phone number format detected.")
                    except sr.WaitTimeoutError:
                        print("Timeout: No speech detected within 15 seconds.")
                    except sr.UnknownValueError:
                        print("Could not understand audio.")
                    except sr.RequestError as e:
                        print(f"Google API error: {e}")
                    except Exception as e:
                        print(f"Error capturing phone number: {e}")

                    if attempt < max_attempts - 1:
                        self.generate_audio("Sorry, I didn't catch your phone number. Please try again.",
                                           "Sorry, I didn't catch your phone number. Please try again.")
                        time.sleep(1)

        self.generate_audio(f"Thank you, {self.patient_name}. How may I assist you?",
                           f"Thank you, {self.patient_name}. How may I assist you?")

    def start_transcription(self):
        """Listen for patient speech and generate AI responses."""
        print("Listening... Speak now.")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=3)
            while True:
                try:
                    audio = self.recognizer.listen(source, timeout=15, phrase_time_limit=15)
                    try:
                        transcript = self.recognizer.recognize_google(audio)
                        print(f"Raw transcript: {transcript}")
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
                    time.sleep(1)

    def generate_ai_response(self, transcript):
        """Generate AI response and save interaction/appointment."""
        try:
            response = self.chat.send_message(transcript)
            ai_response = response.text.strip()
            clean_response = clean_markdown(ai_response)
            self.generate_audio(clean_response, ai_response)
            save_interaction(self.patient_id, transcript, ai_response)
            save_appointment(self.patient_id, self.patient_name, self.patient_phone, self.sms_consent, ai_response)
        except Exception as e:
            print(f"Error generating AI response: {e}")

    def generate_audio(self, clean_text, raw_text):
        """Generate and play audio for AI response."""
        print(f"\nAI Receptionist: {raw_text}")
        try:
            self.tts_engine.say(clean_text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"Error generating or playing audio: {e}")

if __name__ == "__main__":
    greeting = "Thank you for calling Vancouver Dental Clinic. My name is Sandy, how may I assist you?"
    try:
        ai_assistant = AI_Assistant()
        try:
            ai_assistant.generate_audio(greeting, greeting)
            ai_assistant.get_patient_details()
            ai_assistant.start_transcription()
        finally:
            ai_assistant.cleanup()
    except KeyboardInterrupt:
        print("\nShutting down...")
        ai_assistant.cleanup()