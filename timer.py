import os
import time 
import random 

import wave
import pyaudio
import pandas as pd

from datetime import datetime


def get_time():
    """Get the date and time."""
    dt_object = datetime.fromtimestamp(time.time())
    d, t = str(dt_object).split('.')[0].split(' ')
    return d, t


def play_wav():
    """Play a random birdsong wave file.
    
    Prints to console main identifying characteristics
    for the recording:
    XCode -- specific code, append to https://xeno-canto.org 
             to get specific recording 
    Ebird Code -- the abbreviated bird species code
                  also the name of the sub directories
    Bird Species -- the full bird species name 
    Recorded On -- date of recording 
    Recorded In -- country of recording
    """
    rand = random.randint(1, len(waves)-1)
    rbird = waves[rand]
    rcode = codes[rand]
    rdf = df[df['xc_id'] == int(rcode)]

    ebird_code = rdf['ebird_code'][rdf.index[0]]
    bird_species = rdf['species'][rdf.index[0]]
    rec_date = rdf['date'][rdf.index[0]]
    country = rdf['country'][rdf.index[0]]

    print(f'\nXCode: {rcode}\nEbird Code: {ebird_code}\nBird Species: {bird_species}\
\nRecorded On: {rec_date}\nRecorded In: {country}\n')

    chunk = 1024

    wf = wave.open(rbird, 'rb')

    # instantiate PyAudio
    p = pyaudio.PyAudio()

    # open stream
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # read data
    data = wf.readframes(chunk)

    # play stream
    T1 = time.time()
    # while len(data) > 0:
    while time.time() - T1 < 12:
        stream.write(data)
        data = wf.readframes(chunk)

    # stop stream
    stream.stop_stream()
    stream.close()

    # close PyAudio
    p.terminate()


def move_user(direction):
    """Message user to stand up or sit down in two ways:
    1. Playing a birdsong to get user's attention.
    2. Printing instructions to the console.
    """
    if direction == "up":
        day, now = get_time()
        print(f'{now} - If you\'d be so kind as to stand now. Much appreciated!')
        print('-'*65)
        print(f'(Standing for {stand_min} minutes...)')
        play_wav()
        time.sleep(stand_sec)
    elif direction == "down":
        day, now = get_time()
        print(f'{now} - That was FANTASTIC work! You may sit now.')
        print('-'*52)
        print(f'(Sitting for {sit_min} minutes...)')
        play_wav()
        time.sleep(sit_sec)
    else:
        pass
        
            
if __name__ == '__main__':

    # read metadata
    df = pd.read_csv(os.path.join("metadata.csv"))

    wav_dir = os.path.join("audio", "wav")
    waves, codes = [], []

    for subdir in os.listdir(wav_dir):
        for wav in os.listdir(os.path.join(wav_dir, subdir)):
            waves.append(os.path.join(wav_dir, subdir, wav))
            codes.append(wav.split('.')[0][2:])
                
    # get user input 
    sit_min = input("Set sitting minutes: ")
    stand_min = input("Set standing minutes: ")
    times = input("How many times? ")
    
    # calculate, sanitize
    sit_sec = float(sit_min)*60
    stand_sec = float(stand_min)*60
    times = int(times)

    # start work session
    print("\nThank you Ms. Wehinger, your wish is my command.")
    print("Please have a seat.\n")
    
    day, start_time = get_time()
    print(f'Day: {day}')
    print(f'Start time: {start_time}\n')
    time.sleep(sit_sec)

    for i in range(times):
        if i+1 == times:
            move_user("up")
        else:
            move_user("up")
            move_user("down")
            
    # end work session
    day, end_time = get_time()
    print(f'{end_time} - Excellent work all around, how about that break?')
    print('-'*59)
    play_wav()