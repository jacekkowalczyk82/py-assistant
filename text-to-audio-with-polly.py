
import time
import sys
import logging
import json
import os
from configparser import ConfigParser


DEFAULT_STATION_RMF_FM = "http://31.192.216.5/rmf_fm"
ANTY_RADIO = "http://redir.atmcdn.pl/sc/o2/Eurozet/live/antyradio.livx"
RADIO_WNET = "http://audio.radiownet.pl:8000/stream64"
RADIO_ZET = "http://redir.atmcdn.pl/sc/o2/Eurozet/live/audio.livx"
RADIO_PR24 = "http://stream3.polskieradio.pl:8080/"

CHECK_CONTROL_MESSAGE_INTERVAL_SECONDS = 60

CHECK_CONTROL_MESSAGE_INTERVAL_SECONDS_RABBITMQ = 2

# for testing only
CHECK_CONTROL_MESSAGE_INTERVAL_SECONDS_TESTING_ONLY = 10

# in BASIC MODE start only DEFAULT RMF FM station
BASIC_MODE = False

# DEFAULT_STATION_1001 = "http://streaming.radio.pl/1001.pls"

# Konfiguracja logowania (będzie widoczne w journalctl)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# Konfiguracja logowania (będzie widoczne w journalctl)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("text-to-audio")

def get_aws_session(profile_name, region_name):
    import boto3
    
    if profile_name:
        return boto3.Session(profile_name=profile_name, region_name=region_name)
    else:
        return boto3.Session(region_name=region_name)

def synthesize_announcement(text, voice_id, mp3_file_path, profile_name, region_name):
    logger.info(f"Synthesizing announcement for: '{text}'")
    if not text:
        logger.warning("Text is empty, skipping announcement.")
        return None
        
    try:
        session = get_aws_session(profile_name, region_name)
        logger.debug(f"AWS Session created: region={session.region_name}, profile={session.profile_name}")
        
        polly = session.client("polly")
        logger.debug("Polly client created. calling synthesize_speech...")
        #Ewa, Maja, Jacek, Jan, Ola 

        response = polly.synthesize_speech(
            Text=f"<speak><prosody volume='x-loud'>{text}</prosody></speak>",
            TextType="ssml",
            OutputFormat="mp3",
            VoiceId=voice_id # Polish voice
        )
        logger.debug("Polly response received.")
        
        
        with open(mp3_file_path, "wb") as f:
            f.write(response["AudioStream"].read())
            
        if os.path.exists(mp3_file_path):
            logger.info(f"Announcement saved to {mp3_file_path}, size: {os.path.getsize(mp3_file_path)} bytes")
            return mp3_file_path
        else:
            logger.error("File write appeared to fail - file not found after writing.")
            return None
            
    except Exception as e:
        logger.error(f"Polly error details: {type(e).__name__}: {e}", exc_info=True)
        return None



if __name__ == "__main__":
    # #Ewa, Maja, Jacek, Jan, Ola 
    # mp3_path = synthesize_announcement("Witaj Świecie mój kochany", "Maja", "./witaj-swiecie-moj-kochany-Maja.mp3", "default", "us-east-1") 
    # print(f"MP3 path: {mp3_path}")

    # mp3_path = synthesize_announcement("Witaj Świecie mój kochany", "Ewa", "./witaj-swiecie-moj-kochany-Ewa.mp3", "default", "us-east-1") 
    # print(f"MP3 path: {mp3_path}")

    # mp3_path = synthesize_announcement("Witaj Świecie mój kochany", "Jacek", "./witaj-swiecie-moj-kochany-Jacek.mp3", "default", "us-east-1") 
    # print(f"MP3 path: {mp3_path}")

    # mp3_path = synthesize_announcement("Witaj Świecie mój kochany", "Jan", "./witaj-swiecie-moj-kochany-Jan.mp3", "default", "us-east-1") 
    # print(f"MP3 path: {mp3_path}")

    

    mp3_path = synthesize_announcement("Panie Jacku, za chwilkę ma pan spotkanie ", "Jacek", "./za-chwilke-spotkanie-Jacek.mp3", "default", "us-east-1") 
    print(f"MP3 path: {mp3_path}")


