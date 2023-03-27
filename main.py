import pyaudio
import wave
import os
import openai
import io
from pynput.keyboard import Key, Controller

from dotenv import load_dotenv
load_dotenv()

# Set up audio recording
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5
BUFFER_SIZE = int(RATE / CHUNK * RECORD_SECONDS)
WAVE_OUTPUT_FILENAME = "output.wav"
openai.api_key = os.getenv("WHISPER_API_KEY")
p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

keyboard = Controller()


# Continuously record and transcribe audio
while True:
    frames = []

    # Record audio to buffer file
    for i in range(BUFFER_SIZE):
        data = stream.read(CHUNK)
        frames.append(data)

    # Transcribe audio from buffer file
    data_bytes = io.BytesIO(b''.join(frames)).getvalue()

    # Write buffer file to disk
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb')as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    audio_file = open(WAVE_OUTPUT_FILENAME, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    # Print transcript
    print(transcript)

    # type the transcript
    keyboard.type(transcript['text'])

# Stop recording and close stream
stream.stop_stream()
stream.close()
p.terminate()


