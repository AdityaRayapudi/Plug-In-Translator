from speechmatics.rt import AsyncClient, TranscriptionConfig
import asyncio
import pyaudio
from dotenv import load_dotenv

import os

load_dotenv()

API_KEY = os.getenv('API_KEY')
LANGUAGE = "en"
CONNECTION_URL = f"wss://eu2.rt.speechmatics.com/v2/{LANGUAGE}"
DEVICE_INDEX = 5
CHUNK_SIZE = 1024

# Set up PyAudio
p = pyaudio.PyAudio()

SAMPLE_RATE = int(p.get_device_info_by_index(DEVICE_INDEX)["defaultSampleRate"])
device_name = p.get_device_info_by_index(DEVICE_INDEX)["name"]

print(f"\nUsing << {device_name} >> which is DEVICE_INDEX {DEVICE_INDEX}")
print("Starting transcription (type Ctrl-C to stop):")

audio_stream = p.open(
    format=pyaudio.paFloat32,
    channels=1,
    rate=SAMPLE_RATE,
    input=True,
    frames_per_buffer=CHUNK_SIZE,
    input_device_index=DEVICE_INDEX,
)

async def main():
    async with AsyncClient(API_KEY) as client:

        conf = TranscriptionConfig(language="en")

        await client.transcribe(audio_stream, transcription_config=conf)

asyncio.run(main())