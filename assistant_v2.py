import pyaudio
import wave
import speech_recognition as sr
import time




# Record audio
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10
OUTPUT_FILE = "output.wav"

ASSISTANT_OFF = "assistant off"

def listen_speech():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print(f"Listening...{RECORD_SECONDS} seconds")
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
        return text
    except sr.UnknownValueError:
        print("Could not understand audio or silence or no speech ??")
        return None
    except sr.RequestError as e:
        print(f"Error with request: {e}")
        return None



if __name__ == "__main__":
    # execute only if run as a script
    # main(sys.argv)
    keep_listening_assitant = True
    while keep_listening_assitant :
        text = listen_speech() ;
        if text is None:
            println ("text: None: no speach ") 
        if ASSISTANT_OFF  in text:
            keep_listening_assitant = False
        
        
        # waiting for next 
        time.sleep(10) # 10 seconds 

        
    
    print("Bye Bye")

