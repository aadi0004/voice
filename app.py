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
import asyncio

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

# Response cache for common queries
RESPONSE_CACHE = {
    "routine dental check up": "Thanks, {name}! Great to keep up with your check-ups. Do you prefer morning or afternoon, and any dates to avoid?",
    "reschedule my appointment": "Thanks, {name}! When would you like to reschedule your appointment?",
    "change my appointment": "Thanks, {name}! Please tell me the new date and time for your appointment.",
    "move my appointment": "Thanks, {name}! When would you like to move your appointment to?"
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

async def connect_to_db():
    """Connect to MySQL database with buffered cursor."""
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG, buffered=True)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
    return None

async def update_tables():
    """Update database schema to ensure required columns exist and remove email."""
    connection = await connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            # Log MySQL version for debugging
            cursor.execute("SELECT VERSION()")
            mysql_version = cursor.fetchone()[0]
            print(f"MySQL Server Version: {mysql_version}")

            # Add phone_number column if it doesn't exist
            cursor.execute("SHOW COLUMNS FROM patients LIKE 'phone_number'")
            cursor.fetchall()  # Consume all results
            if not cursor.rowcount:
                cursor.execute("ALTER TABLE patients ADD COLUMN phone_number VARCHAR(20)")
                print("Added phone_number column to patients table.")
            
            # Add sms_consent column if it doesn't exist
            cursor.execute("SHOW COLUMNS FROM patients LIKE 'sms_consent'")
            cursor.fetchall()  # Consume all results
            if not cursor.rowcount:
                cursor.execute("ALTER TABLE patients ADD COLUMN sms_consent BOOLEAN DEFAULT TRUE")
                print("Added sms_consent column to patients table.")
            
            # Remove email column if it exists
            cursor.execute("SHOW COLUMNS FROM patients LIKE 'email'")
            cursor.fetchall()  # Consume all results
            if cursor.rowcount:
                cursor.execute("ALTER TABLE patients DROP COLUMN email")
                print("Removed email column from patients table.")
            
            # Check if appointments table exists
            cursor.execute("SHOW TABLES LIKE 'appointments'")
            cursor.fetchall()  # Consume all results
            if cursor.rowcount:
                # Check if index idx_patient_id_created_at exists
                cursor.execute("SHOW INDEXES FROM appointments WHERE Key_name = 'idx_patient_id_created_at'")
                cursor.fetchall()  # Consume all results
                if not cursor.rowcount:
                    cursor.execute("CREATE INDEX idx_patient_id_created_at ON appointments (patient_id, created_at)")
                    print("Added index on appointments(patient_id, created_at).")
                else:
                    print("Index idx_patient_id_created_at already exists.")
            else:
                print("Appointments table does not exist. Skipping index creation.")
            
            connection.commit()
        except Error as e:
            print(f"Error updating tables: {e}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

async def create_tables():
    """Create necessary tables if they don't exist and update schema."""
    connection = await connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    patient_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    phone_number VARCHAR(20),
                    sms_consent BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
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
            await update_tables()
        except Error as e:
            print(f"Error creating tables: {e}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

async def save_interaction(patient_id, query, response):
    """Save patient interaction to MySQL database."""
    connection = await connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            query_sql = """
                INSERT INTO patient_interactions (patient_id, patient_query, ai_response)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query_sql, (patient_id, query, response))
            connection.commit()
            print(f"Saved interaction for patient ID {patient_id}")
        except Error as e:
            print(f"Error saving interaction: {e}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

async def get_or_create_patient(name, phone_number=None, sms_consent=True):
    """Retrieve or create patient record in the database."""
    connection = await connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
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
                cursor.execute("INSERT INTO patients (name, phone_number, sms_consent) VALUES (%s, %s, %s)",
                               (name, phone_number, sms_consent))
                connection.commit()
                cursor.execute("SELECT LAST_INSERT_ID()")
                patient_id = cursor.fetchone()[0]
                return patient_id, phone_number, sms_consent
        except Error as e:
            print(f"Error managing patient: {e}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
    return None, None, True

async def fetch_appointment(patient_id):
    """Fetch the latest appointment for a patient."""
    connection = await connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT id, appointment_date, appointment_time
                FROM appointments
                WHERE patient_id = %s
                ORDER BY created_at DESC
                LIMIT 1
            """, (patient_id,))
            result = cursor.fetchone()
            if result:
                print(f"Fetched appointment for patient ID {patient_id}: ID={result[0]}, Date={result[1]}, Time={result[2]}")
                return {'id': result[0], 'date': result[1], 'time': result[2]}
            print(f"No appointment found for patient ID {patient_id}")
            return None
        except Error as e:
            print(f"Error fetching appointment: {e}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
    return None

async def send_appointment_message(patient_name, patient_phone, sms_consent, appointment_date, appointment_time, is_reschedule=False):
    """Send appointment confirmation via SMS."""
    if patient_phone and sms_consent and appointment_date and appointment_time:
        twilio_client = Client(TWILIO_CONFIG['account_sid'], TWILIO_CONFIG['auth_token'])
        from_number = TWILIO_CONFIG['phone_number']
        to_number = f"+91{patient_phone}" if not patient_phone.startswith('+') else patient_phone
        
        action = "rescheduled" if is_reschedule else "scheduled"
        body = f"Hi {patient_name}, your appt at Vancouver Dental is {action} for {appointment_date} at {appointment_time}. Call (555) 123-4567 to change. Reply STOP to opt out. -Sandy"
        
        try:
            message = twilio_client.messages.create(
                body=body,
                from_=from_number,
                to=to_number
            )
            print(f"Appointment {'reschedule' if is_reschedule else 'confirmation'} SMS sent to {patient_phone} (SID: {message.sid}).")
        except Exception as e:
            print(f"Error sending SMS: {e}")
    else:
        print("No valid phone number, SMS consent, or appointment details provided. Skipping message.")

async def save_appointment(patient_id, patient_name, patient_phone, sms_consent, response):
    """Parse AI response and save new appointment details to database."""
    print(f"Processing save_appointment with AI response: {response}")
    # Broadened regex to match both scheduled and rescheduled
    appointment_pattern = r"Appointment\s*(?:scheduled|booked|set|rescheduled)\s*(?:for|on|at)?\s*(\d{4}-\d{2}-\d{2})\s*(?:at)?\s*(\d{2}:\d{2})"
    match = re.search(appointment_pattern, response, re.IGNORECASE)
    
    if match:
        appointment_date = match.group(1)
        appointment_time = match.group(2)
        print(f"Regex matched: date={appointment_date}, time={appointment_time}")
        
        connection = await connect_to_db()
        if connection:
            try:
                cursor = connection.cursor()
                query_sql = """
                    INSERT INTO appointments (patient_id, appointment_date, appointment_time)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(query_sql, (patient_id, appointment_date, appointment_time))
                if cursor.rowcount > 0:
                    connection.commit()
                    print(f"Saved new appointment for patient ID {patient_id} on {appointment_date} at {appointment_time}. Rows affected: {cursor.rowcount}")
                    await send_appointment_message(patient_name, patient_phone, sms_consent, appointment_date, appointment_time)
                else:
                    print(f"Failed to save appointment for patient ID {patient_id}: No rows affected.")
                    connection.rollback()
            except Error as e:
                print(f"Error saving appointment: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
    else:
        print(f"No new appointment details detected in response: {response}")

async def reschedule_appointment(patient_id, patient_name, patient_phone, sms_consent, response):
    """Parse AI response and reschedule existing appointment."""
    print(f"Raw AI response for rescheduling: {response}")
    # Broadened regex to capture various rescheduling formats
    appointment_pattern = r"Appointment\s*(?:re)?scheduled\s*(?:for|to|on|at)?\s*(\d{4}-\d{2}-\d{2})\s*(?:at)?\s*(\d{2}:\d{2})"
    match = re.search(appointment_pattern, response, re.IGNORECASE)
    
    if match:
        appointment_date = match.group(1)
        appointment_time = match.group(2)
        print(f"Regex matched for reschedule: date={appointment_date}, time={appointment_time}")
        
        existing_appointment = await fetch_appointment(patient_id)
        if existing_appointment:
            connection = await connect_to_db()
            if connection:
                try:
                    cursor = connection.cursor()
                    query_sql = """
                        UPDATE appointments
                        SET appointment_date = %s, appointment_time = %s, created_at = CURRENT_TIMESTAMP
                        WHERE id = %s AND patient_id = %s
                    """
                    print(f"Executing UPDATE: date={appointment_date}, time={appointment_time}, id={existing_appointment['id']}, patient_id={patient_id}")
                    cursor.execute(query_sql, (appointment_date, appointment_time, existing_appointment['id'], patient_id))
                    if cursor.rowcount > 0:
                        connection.commit()
                        print(f"Successfully rescheduled appointment for patient ID {patient_id} to {appointment_date} at {appointment_time}. Rows affected: {cursor.rowcount}")
                        await send_appointment_message(patient_name, patient_phone, sms_consent, appointment_date, appointment_time, is_reschedule=True)
                    else:
                        print(f"Failed to update appointment for patient ID {patient_id}: No rows affected.")
                        connection.rollback()
                except Error as e:
                    print(f"Error rescheduling appointment: {e}")
                    connection.rollback()
                finally:
                    cursor.close()
                    connection.close()
        else:
            print("No existing appointment found. Saving as new appointment.")
            await save_appointment(patient_id, patient_name, patient_phone, sms_consent, response)
    else:
        print(f"No reschedule details detected in response: {response}")
        # Fallback: Prompt for clarification
        clarification_response = "I couldn't find clear date and time details. Could you please specify the new date and time for your appointment?"
        await send_appointment_message(patient_name, patient_phone, sms_consent, None, None, is_reschedule=True)

class AI_Assistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.recognizer.energy_threshold = 4000  # Adjust for better detection
        self.recognizer.dynamic_energy_threshold = True

        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.chat = self.model.start_chat(history=[
            {"role": "user", "parts": [
                "You are Sandy, a friendly and efficient receptionist at Vancouver Dental Clinic. Be concise, empathetic, and professional. Use patient details (name, phone number) provided to avoid redundant requests. For scheduling or rescheduling, always confirm with 'Appointment scheduled for YYYY-MM-DD at HH:MM' or 'Appointment rescheduled for YYYY-MM-DD at HH:MM'. For routine check-ups, ask about morning/afternoon preferences and date constraints. For rescheduling, confirm the change and update the existing appointment. Acknowledge prior inputs (e.g., 'Thanks, [name], I have your details'). If no appointment exists for rescheduling, suggest booking a new one. If input is unclear, ask for clarification with 'Could you please specify the date and time?'."
            ]},
            {"role": "model", "parts": ["Understood! I'm Sandy, ready to assist at Vancouver Dental Clinic. How can I help you today?"]}]
        )

        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 220)  # Faster speech
        self.tts_engine.setProperty('volume', 0.9)
        voices = self.tts_engine.getProperty('voices')
        for voice in voices:
            if "David" in voice.name:
                self.tts_engine.setProperty('voice', voice.id)
                break

        self.patient_name = "Unknown"
        self.patient_id = None
        self.patient_phone = None
        self.sms_consent = True
        self.last_intent = None  # Track scheduling or rescheduling intent

        self.audio_cache = {}
        self.response_cache = RESPONSE_CACHE
        self.audio_failure_count = 0

    def cleanup(self):
        """Explicitly stop the TTS engine."""
        try:
            self.tts_engine.stop()
        except Exception as e:
            print(f"Error stopping TTS engine: {e}")

    async def get_patient_details(self):
        """Prompt for and capture patient name and phone number via speech with retry."""
        max_attempts = 3

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1.5)  # Reduced for speed

            for attempt in range(max_attempts):
                print(f"Attempt {attempt + 1}/{max_attempts}: Please say your name.")
                await self.generate_audio("Please say your name.", "Please say your name.")
                try:
                    audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=8)
                    name = self.recognizer.recognize_google(audio).strip()
                    print(f"Raw name input: {name}")
                    if name:
                        self.patient_name = clean_name(name)
                        print(f"Patient name: {self.patient_name}")
                        break
                    else:
                        print("No name detected.")
                except sr.WaitTimeoutError:
                    print("Timeout: No speech detected within 8 seconds.")
                except sr.UnknownValueError:
                    print("Could not understand audio.")
                except sr.RequestError as e:
                    print(f"Google API error: {e}")
                except Exception as e:
                    print(f"Error capturing name: {e}")

                if attempt < max_attempts - 1:
                    await self.generate_audio("Sorry, I didn't catch your name. Please try again.",
                                             "Sorry, I didn't catch your name. Please try again.")
                    time.sleep(0.1)

            if self.patient_name == "Unknown":
                print("No name detected after retries, using 'Unknown'.")
                await self.generate_audio("Sorry, I couldn't get your name. I'll use 'Unknown' for now.",
                                         "Sorry, I couldn't get your name. I'll use 'Unknown' for now.")

            self.patient_id, self.patient_phone, self.sms_consent = await get_or_create_patient(self.patient_name)

            if not self.patient_phone:
                for attempt in range(max_attempts):
                    print(f"Attempt {attempt + 1}/{max_attempts}: Please say your phone number.")
                    await self.generate_audio("Please say a 10-digit phone number.", "Please say a 10-digit phone number.")
                    try:
                        audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=8)
                        phone = self.recognizer.recognize_google(audio).strip()
                        print(f"Raw phone input: {phone}")
                        phone = re.sub(r'\D', '', phone)
                        if len(phone) >= 10:
                            self.patient_phone = phone[:10]
                            print(f"Patient phone: {self.patient_phone}")
                            self.patient_id, _, self.sms_consent = await get_or_create_patient(
                                self.patient_name, self.patient_phone, self.sms_consent)
                            break
                        else:
                            print("Invalid phone number format detected.")
                    except sr.WaitTimeoutError:
                        print("Timeout: No speech detected within 8 seconds.")
                    except sr.UnknownValueError:
                        print("Could not understand audio.")
                    except sr.RequestError as e:
                        print(f"Google API error: {e}")
                    except Exception as e:
                        print(f"Error capturing phone number: {e}")

                    if attempt < max_attempts - 1:
                        await self.generate_audio("Sorry, I need a 10-digit phone number. Please try again.",
                                                 "Sorry, I need a 10-digit phone number. Please try again.")
                        time.sleep(0.1)

        await self.generate_audio(f"Thanks, {self.patient_name}! How can I assist you today?",
                                 f"Thanks, {self.patient_name}! How can I assist you today?")

    async def start_transcription(self):
        """Listen for patient speech and generate AI responses."""
        print("Listening... Speak now.")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1.5)
            while True:
                try:
                    audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=8)
                    try:
                        transcript = self.recognizer.recognize_google(audio)
                        print(f"Raw transcript: {transcript}")
                        if transcript.strip():
                            print(f"\nPatient: {transcript}\n")
                            self.audio_failure_count = 0
                            await self.generate_ai_response(transcript)
                        else:
                            print("No speech detected, continuing to listen...")
                    except sr.UnknownValueError:
                        self.audio_failure_count += 1
                        print("Could not understand audio.")
                        if self.audio_failure_count >= 3:
                            await self.generate_audio("I'm having trouble hearing you. Please try again or say 'book new appointment'.",
                                                     "I'm having trouble hearing you. Please try again or say 'book new appointment'.")
                            self.audio_failure_count = 0
                    except sr.RequestError as e:
                        print(f"Google API error: {e}, continuing to listen...")
                    except Exception as e:
                        print(f"Error processing audio: {e}")
                except KeyboardInterrupt:
                    print("\nStopping transcription...")
                    break
                except Exception as e:
                    print(f"Error during transcription: {e}")
                    time.sleep(0.1)

    async def generate_ai_response(self, transcript):
        """Generate AI response and handle scheduling/rescheduling."""
        try:
            # Use existing patient details if available
            if self.patient_id and self.patient_name != "Unknown":
                cache_key = transcript.lower().strip()
                if cache_key in self.response_cache:
                    ai_response = self.response_cache[cache_key].format(name=self.patient_name)
                    clean_response = clean_markdown(ai_response)
                    await self.generate_audio(clean_response, ai_response)
                    await save_interaction(self.patient_id, transcript, ai_response)
                    self.last_intent = "reschedule" if "reschedule" in cache_key or "change" in cache_key or "move" in cache_key else "schedule"
                    print(f"Using cached response. Intent set to: {self.last_intent}")
                    return

                existing_appointment = await fetch_appointment(self.patient_id)
                context = f"The patient's name is {self.patient_name} and their phone number is {self.patient_phone}. "
                if existing_appointment:
                    context += f"They have an appointment on {existing_appointment['date']} at {existing_appointment['time']}. "
                context += "Respond concisely and handle rescheduling if requested. Always confirm scheduling or rescheduling with 'Appointment scheduled for YYYY-MM-DD at HH:MM' or 'Appointment rescheduled for YYYY-MM-DD at HH:MM'."

                response = await asyncio.to_thread(self.chat.send_message, context + transcript)
                ai_response = response.text.strip()
                clean_response = clean_markdown(ai_response)
                await self.generate_audio(clean_response, ai_response)
                await save_interaction(self.patient_id, transcript, ai_response)

                # Determine intent based on transcript and AI response
                is_reschedule = any(phrase in transcript.lower() for phrase in ["reschedule", "change my appointment", "move my appointment"])
                is_confirmation = any(phrase in transcript.lower() for phrase in ["yes", "correct", "confirm", "all details are correct"])
                ai_indicates_reschedule = "rescheduled" in ai_response.lower()

                if is_reschedule:
                    self.last_intent = "reschedule"
                    print(f"Intent: reschedule (based on transcript: {transcript})")
                    await reschedule_appointment(self.patient_id, self.patient_name, self.patient_phone, self.sms_consent, ai_response)
                elif is_confirmation and (self.last_intent == "reschedule" or ai_indicates_reschedule):
                    self.last_intent = "reschedule"
                    print(f"Intent: reschedule (confirmation: {transcript}, last_intent or AI response)")
                    await reschedule_appointment(self.patient_id, self.patient_name, self.patient_phone, self.sms_consent, ai_response)
                else:
                    self.last_intent = "schedule"
                    print(f"Intent: schedule (default, transcript: {transcript})")
                    await save_appointment(self.patient_id, self.patient_name, self.patient_phone, self.sms_consent, ai_response)
            else:
                await self.get_patient_details()
        except Exception as e:
            print(f"Error generating AI response: {e}")
            await self.generate_audio("Sorry, I'm having trouble. Please repeat that.",
                                     "Sorry, I'm having trouble. Please repeat that.")

    async def generate_audio(self, clean_text, raw_text):
        """Generate and play audio for AI response, using cache."""
        print(f"\nAI Receptionist: {raw_text}")
        try:
            if raw_text not in self.audio_cache:
                self.tts_engine.say(clean_text)
                self.audio_cache[raw_text] = True
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"Error generating or playing audio: {e}")

async def main():
    greeting = "Thank you for calling Vancouver Dental Clinic. My name is Sandy, how may I assist you?"
    try:
        # Ensure tables are created before initializing AI_Assistant
        await create_tables()
        ai_assistant = AI_Assistant()
        try:
            await ai_assistant.generate_audio(greeting, greeting)
            await ai_assistant.get_patient_details()
            await ai_assistant.start_transcription()
        finally:
            ai_assistant.cleanup()
    except KeyboardInterrupt:
        print("\nShutting down...")
        ai_assistant.cleanup()

if __name__ == "__main__":
    asyncio.run(main())

    