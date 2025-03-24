import pyaudio
import wave
import speech_recognition as sr
import time
import logging

import subprocess
import threading
import os
import sys

import pyttsx3


# sudo apt-get install espeak
# pip3 install pyttsx3
# pip3 install SpeechRecognition
# pip3 install pyaudio

# engine = pyttsx3.init('espeak') # Linux
# engine.setProperty('volume', 1.0)  # Max volume
# engine.setProperty('rate', 150)    # Default rate 200
# engine.say("Hello I am listening")
# engine.runAndWait()
# engine.stop()  # Explicitly stop the engine after speaking

# # Initialize the text-to-speech engine
# # engine = pyttsx3.init('espeak') # Linux
# engine = pyttsx3.init() # Linux
# engine.setProperty('volume', 1.0)  # Max volume
# engine.setProperty('rate', 200)    # Default rate

# # Set speech rate (default is 200)
# # engine.setProperty('rate', 150)  # Slower speech

# # Set volume (0.0 to 1.0)
# # engine.setProperty('volume', 1.0)  # Max volume

# engine.say("Can you hear me now?")
# engine.runAndWait()


## logging 

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler('py-assistant.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)


logger.addHandler(file_handler)
logger.addHandler(stdout_handler)

## commands subprocesses

BASH_COMMAND_SWITCH = "-c"
BASH_EXE = "bash"

##

# Record audio
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
OUTPUT_FILE = "output.wav"

HELLO_ASSISTANT = "hello assistant"
ASSISTANT_OFF = "assistant turn off"
ASSISTANT_COMMANDS_PREFIX = "assistant "
SUPPORTED_COMMANDS = ["play radio RMF", "play radio", "stop radio", "volume up", "volume down", "play youtube favorites", "stop youtube", "help me"]
 
def speak_Polish(text):
    """Convert text to speech and play it through speakers"""
    # engine = pyttsx3.init()
    engine = pyttsx3.init('espeak') # Linux

    engine.setProperty('voice', "Polish")  # Index depends on your system
    engine.setProperty('volume', 5.0)  # Max volume
    
    engine.setProperty('rate', 140)    # Default rate 200
    engine.say(text)
    engine.runAndWait()
    engine.stop()  # Explicitly stop the engine after speaking
    print("speak exit")


def speak(text):
    """Convert text to speech and play it through speakers"""
    # Set speech rate (default is 200)
    # engine.setProperty('rate', 150)  # Slower speech

    # Set volume (0.0 to 1.0)
    # engine.setProperty('volume', 1.0)  # Max volume
    # engine.setProperty('volume', 1.0)  # Max volume
    # engine.setProperty('rate', 200)    # Default rate

    # Ensure PyAudio resources are not conflicting
    # engine = pyttsx3.init()
    engine = pyttsx3.init('espeak') # Linux

    voices = engine.getProperty('voices')
    for voice in voices:
        print(f"Voice: {voice.name}, ID: {voice.id}")

    # Voice: English (America), ID: English (America)
    engine.setProperty('voice', "English (Great Britain)")  # Index depends on your system
    engine.setProperty('volume', 5.0)  # Max volume
    
    engine.setProperty('rate', 140)    # Default rate 200
    engine.say(text)
    engine.runAndWait()
    engine.stop()  # Explicitly stop the engine after speaking
    print("speak exit")


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

def get_command(lower_command):

    for command in SUPPORTED_COMMANDS:
        full_command = ASSISTANT_COMMANDS_PREFIX + command
        if full_command.lower() in lower_command:
            return command
    return None


def command_handler_stop(active_command, sub_commands_pids):
    assist_print("Stopping active_command: " + str(active_command))


def command_handler(command, sub_commands_pids):
    if command is None:
        assist_print("command is None")
        return 
    else:    
        message = "Running command: " + command
        assist_print(message)
        speak(message)

        if "play radio RMF" in command:
            thread_play_radio_rmf(command, sub_commands_pids)
        elif "play radio" in command:
            thread_play_radio_rmf(command, sub_commands_pids)
        elif "stop radio" in command:
            thread_stop_radio(command, sub_commands_pids)
 

    # if radio -> rmf-ubuntu.sh 

def thread_play_radio_rmf(command, sub_commands_pids):
    print("RMF FM ")

    command_thread = threading.Thread(target=thread_command_function, args=(command, sub_commands_pids, "/home/jacek/bin/rmf-ubuntu.sh","dummy")) # extra comma , must be added
    command_thread.daemon = True  # Thread will terminate when main program exits
    command_thread.start()

    logger.debug("thread_play_radio_rmf: " + str(sub_commands_pids))

def thread_stop_radio(command, sub_commands_pids):
    print("Stop Radio")

    if "play radio RMF" in sub_commands_pids:
        radio_pid = sub_commands_pids["play radio RMF"]
        kill_command = "kill -9 -" + str(radio_pid)
        command_thread = threading.Thread(target=thread_command_function, args=(command, sub_commands_pids, kill_command,"dummy")) # extra comma , must be added
        command_thread.daemon = True  # Thread will terminate when main program exits
        command_thread.start()

        logger.debug("thread_stop_radio: " + str(sub_commands_pids))
        # remove stoped command
        del sub_commands_pids["play radio RMF"]

    elif "play radio" in sub_commands_pids:
        radio_pid = sub_commands_pids["play radio"]
        kill_command = "kill -9 -" + str(radio_pid)
        command_thread = threading.Thread(target=thread_command_function, args=(command, sub_commands_pids, kill_command,"dummy")) # extra comma , must be added
        command_thread.daemon = True  # Thread will terminate when main program exits
        command_thread.start()

        logger.debug("thread_stop_radio: " + str(sub_commands_pids))
        # remove stoped command
        del sub_commands_pids["play radio"]



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

def handle_supported_command(command_text, active_command, sub_commands_pids):
    assist_print("Last active command is: " + str(active_command))

    if is_supported(command_text):
        assist_print("Received command: " + command_text.lower())

        if active_command is not None:
            assist_print("Stopping last active command: " + active_command)
            command_handler_stop(active_command, sub_commands_pids)

        command = get_command(command_text.lower())

        command_handler(command, sub_commands_pids)

        return command
    else:
        return None


def thread_command_function(assistant_command, sub_commands_pids, tuple_os_command_to_run, sec_unused_param):
    thread_id = threading.get_ident()
    print("Started thread_command_function thread " + str(thread_id) + " with command: " +  str(tuple_os_command_to_run))
    logger.debug(str(sub_commands_pids))

    with open("/tmp/py-assistant.log", "a") as assistant_log:
        with open("/tmp/py-assistant.err.log", "a") as assistant_err:
            logger.debug("Before starting subprocess : "+ str(tuple_os_command_to_run))
            process3 = subprocess.Popen(
            [BASH_EXE, BASH_COMMAND_SWITCH, tuple_os_command_to_run],
            stdout=assistant_log, 
            stderr=assistant_err,
            preexec_fn=os.setsid  # Creates a new process group
            )

            sub_commands_pids[assistant_command] = process3.pid
            logger.debug("After starting subprocess : "+ str(tuple_os_command_to_run))
            logger.debug("sub_commands_pids: " + str(sub_commands_pids))

            pgid = os.getpgid(process3.pid)
            logger.debug("sub_commands_pids process group PGID: " + str(pgid))


            stdout3, stderr3 = process3.communicate()

            if stdout3 is not None:
                stdout_decoded = stdout3.decode("UTF-8")
                logger.debug("stdout", stdout_decoded)
            if stderr3 is not None:
                stderr_decoded = stderr3.decode("UTF-8")
                logger.debug("stdout", stderr_decoded)
            
            pass



if __name__ == "__main__":
    

    speak("Hello my Master")
    time.sleep(1) #  seconds 
    speak_Polish("Witaj panie")
    # exit(0)




    # execute only if run as a script
    # main(sys.argv)
    keep_listening_assitant = True
    active_command = None
    sub_commands_pids = dict()

    while keep_listening_assitant :

        print(str(sub_commands_pids))

        text = listen_speech() ;
        if text is None:
            assist_print ("text: None: no speach ") 
        else: 
            if HELLO_ASSISTANT in text:
                assist_print("I am listening")
                speak("I am listening")
                time.sleep(1) #  seconds 
                speak_Polish("Słucham")

                text = listen_speech() ;
                if text is None:
                    assist_print ("text: None: no speach ") 
                else: 
                    command_started_possible = handle_supported_command (text, active_command, sub_commands_pids)
                    if (command_started_possible is not None):
                        active_command = command_started_possible
                        

                    if ASSISTANT_OFF  in text:
                        keep_listening_assitant = False
        
        
        print(str(sub_commands_pids))
        # waiting for next 
        time.sleep(2) #  seconds 

        
    
    print("Bye Bye")

