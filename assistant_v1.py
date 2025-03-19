import pyaudio
import wave
import speech_recognition as sr

# Record audio
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
OUTPUT_FILE = "output.wav"

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
print("Recording...")
frames = []
for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print("Done recording.")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(OUTPUT_FILE, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

# Transcribe
recognizer = sr.Recognizer()
with sr.AudioFile(OUTPUT_FILE) as source:
    audio = recognizer.record(source)
try:
    text = recognizer.recognize_google(audio)
    print("Transcript:", text)
except sr.UnknownValueError:
    print("Could not understand audio")
except sr.RequestError as e:
    print(f"Error with request: {e}")
    