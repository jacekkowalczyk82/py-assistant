import pyaudio
import wave
import speech_recognition as sr
import time




# Record audio
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
OUTPUT_FILE = "output.wav"

ASSISTANT_OFF = "assistant turn off"
ASSISTANT_COMMANDS_PREFIX = "assistant "
SUPPORTED_COMMANDS = ["play radio RMF", "stop radio", "volume up", "volume down", "play youtube favorites", "stop youtube", "help me"]

def assist_print(text):
    print("\n    " + text)
def show_assistent_help():
    assist_print("Supported commands are: " + str(SUPPORTED_COMMANDS))


def listen_speech():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    assist_print(f"Listening...{RECORD_SECONDS} seconds")
    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    assist_print("Done recording.")

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


def is_supported (command_text):
    if ASSISTANT_OFF  in command_text:
        return True

    for command in SUPPORTED_COMMANDS:
        full_command = ASSISTANT_COMMANDS_PREFIX + command
        if full_command.lower() in command_text.lower():
            return True


    assist_print(command_text + " does not contain any supported command ")
    show_assistent_help();
    return False; 

def handle_supported_command(command_text):
    if is_supported(command_text):
        assist_print("Received command: " + command_text.lower())

        lower_command = command_text.lower()
        assist_print("Running command: " + lower_command)


if __name__ == "__main__":
    # execute only if run as a script
    # main(sys.argv)
    keep_listening_assitant = True
    while keep_listening_assitant :
        text = listen_speech() ;
        if text is None:
            assist_print ("text: None: no speach ") 
        else: 
            handle_supported_command (text)

            if ASSISTANT_OFF  in text:
                keep_listening_assitant = False
        
        

        # waiting for next 
        time.sleep(5) #  seconds 

        
    
    print("Bye Bye")

