# Dental Clinic Receptionist AI Assistant

This project implements an AI-powered dental clinic receptionist that interacts with users via voice. It listens to user speech, transcribes it using Google's Speech-to-Text API, generates a response using Hugging Face's `distilgpt2` model, converts the response to audio using `gTTS`, and plays it back using `pygame`. The application uses free, open-source tools and is compatible with Docker for easy deployment.

## Features
- **Speech-to-Text**: Transcribes user speech using `speech_recognition` with Google's Speech-to-Text API.
- **Text Generation**: Generates responses with `distilgpt2`, a lightweight transformer model.
- **Text-to-Speech**: Converts responses to audio using `gTTS` (Google Text-to-Speech).
- **Audio Playback**: Plays audio responses using `pygame`, ensuring Docker compatibility.
- **Free and Open-Source**: No paid services or API keys required.

## Prerequisites
- **Python**: Version 3.10 or 3.11 (Python 3.13.3 may have compatibility issues with PyTorch).
- **Docker**: Required for containerized deployment (optional).
- **Microphone and Speakers**: For speech input and audio output.
- **Internet Connection**: Required for Google Speech-to-Text API.

## Setup Instructions

### 1. Install Python
- Download and install Python 3.11 from [python.org](https://www.python.org/downloads/).
- Ensure `python` and `pip` are added to your PATH.
- Verify installation:
  ```powershell
  python --version
  pip --version
  ```

### 2. Clone or Create the Project
- Create a project directory (e.g., `dental-ai-assistant`).
- Place the `app.py` file (provided) in the directory.
- Create the following additional files as described below.

### 3. Create `requirements.txt`
Create a file named `requirements.txt` with the following content:
```plaintext
speechrecognition>=3.10.0
pyaudio>=0.2.14
transformers>=4.35.0
gTTS>=2.3.2
pygame>=2.5.2
python-dotenv>=1.0.0
torch>=2.4.1
```

### 4. Create `.env` File (Optional)
No API keys are required, but the application checks for a `.env` file. Create an empty `.env` file or skip this step:
```plaintext
# .env
# No API keys required
```

### 5. Create `Dockerfile` (For Docker Deployment)
Create a file named `Dockerfile` with the following content:
```dockerfile
# Use aassyAI Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies for audio (pygame, pyaudio)
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    libportaudio2 \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app.py .

# Command to run the application
CMD ["python", "app.py"]
```

## Running the Application

### Option 1: Run Locally
1. **Set Up Virtual Environment**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```
   - If `torch` installation fails (e.g., with Python 3.13.3), try:
     ```powershell
     pip install torch==2.4.1
     ```
   - If issues persist, switch to Python 3.11:
     ```powershell
     # Install Python 3.11 via python.org
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     pip install -r requirements.txt
     ```

3. **Run the Application**:
   ```powershell
   python app.py
   ```
   - The assistant will play a greeting: "Thank you for calling Vancouver dental clinic. My name is Sandy, how may I assist you?"
   - Speak into your microphone (e.g., "I need to book an appointment"). The assistant will transcribe, respond, and play the response.
   - Press `Ctrl+C` to stop.

### Option 2: Run in Docker
1. **Build the Docker Image**:
   ```powershell
   docker build -t dental-ai-assistant .
   ```

2. **Run the Docker Container**:
   ```powershell
   docker run --rm -it --device=/dev/snd --network=host dental-ai-assistant
   ```
   - The `--device=/dev/snd` flag enables audio access.
   - The `--network=host` flag ensures internet access for Google Speech-to-Text.
   - On Windows, you may need to run in WSL2:
     ```powershell
     wsl docker run --rm -it --device=/dev/snd --network=host dental-ai-assistant
     ```

3. **Stop the Container**:
   - Press `Ctrl+C` to stop the container.

## Project Structure
```plaintext
dental-ai-assistant/
├── app.py           # Main application script
├── requirements.txt # Python dependencies
├── Dockerfile       # Docker configuration
├── .env            # Environment variables (optional, empty)
```

## Troubleshooting

### Installation Issues
- **PyTorch Installation Fails**:
  - Switch to Python 3.11 if using Python 3.13.3:
    ```powershell
    # Install Python 3.11 via python.org
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```
  - Try a specific PyTorch version:
    ```powershell
    pip install torch==2.4.1
    ```
  - Refer to [PyTorch's installation guide](https://pytorch.org/get-started/locally/).

- **PyAudio Installation Fails**:
  - Install `pyaudio` manually:
    ```powershell
    pip install pyaudio
    ```
  - If it fails, download the wheel from [PyPI](https://pypi.org/project/PyAudio/#files) and install:
    ```powershell
    pip install PyAudio-0.2.14-cp311-cp311-win_amd64.whl
    ```

### Runtime Issues
- **No Transcription**:
  - Test your microphone with a tool like Audacity.
  - Ensure `pyaudio` is installed:
    ```powershell
    pip install pyaudio
    ```
  - Verify internet connectivity for Google Speech-to-Text.
  - If Google API fails, it may be due to usage limits. Try again later.

- **No Audio Playback**:
  - Ensure `pygame` is installed and speakers are working:
    ```powershell
    pip install pygame
    ```
  - In Docker, verify `--device=/dev/snd` is passed:
    ```powershell
    docker run --rm -it --device=/dev/snd --network=host dental-ai-assistant
    ```

- **Poor AI Responses**:
  - `distilgpt2` is lightweight. For better responses, try `gpt2-medium` (requires more memory):
    - Edit `app.py`:
      ```python
      self.text_generator = pipeline("text-generation", model="gpt2-medium")
      ```
    - Reinstall dependencies:
      ```powershell
      pip install -r requirements.txt
      ```

- **Docker Issues**:
  - If audio or microphone access fails, try additional permissions:
    ```powershell
    docker run --rm -it --device=/dev/snd --device=/dev/dsp --network=host dental-ai-assistant
    ```
  - Ensure `libportaudio2` and `portaudio19-dev` are installed in the container.

## Limitations
- **Google Speech-to-Text**: Requires internet and has usage limits. Transcription may fail if limits are exceeded.
- **distilgpt2**: Limited conversational ability compared to advanced models. Suitable for simple tasks.
- **Real-Time Performance**: Slight delays may occur due to Google API or model inference.
- **Windows Docker**: Audio and microphone support may require WSL2.

## Example Usage
1. Run locally:
   ```powershell
   python app.py
   ```
2. Hear the greeting and speak a query (e.g., "I need a cleaning").
3. The assistant responds (e.g., "I can schedule a cleaning. What date works for you?") and plays the response.
4. Press `Ctrl+C` to stop.

## Contributing
- To improve transcription, consider integrating a local model like Vosk.
- For better responses, fine-tune `distilgpt2` or use a larger model.
- Submit issues or pull requests to enhance functionality.

## License
This project is licensed under the MIT License.