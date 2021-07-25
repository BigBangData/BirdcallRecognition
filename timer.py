import os
import time 
import random 

import wave
import pyaudio
import pandas as pd
import concurrent.futures as cf

from datetime import datetime
from tkinter import Label, Tk

    
def get_time():
    """Get the date and time."""
    dt_object = datetime.fromtimestamp(time.time())
    d, t = str(dt_object).split('.')[0].split(' ')
    return d, t
    

def get_info(rand):
    """Returns info for a specific recording.
    
    Params
    ------
    rand -- a random integer for the wave files
    
    Info
    -----
    XCode -- specific code, append to https://xeno-canto.org 
             to get specific recording 
    Ebird Code -- the abbreviated bird species code
                  also the name of the sub directories
    Bird Species -- the full bird species name 
    Recorded On -- date of recording 
    Recorded In -- country of recording
    """
    rwave = waves[rand]
    rcode = codes[rand]
    rdf = df[df['xc_id'] == int(rcode)]

    ebird_code = rdf['ebird_code'][rdf.index[0]]
    bird_species = rdf['species'][rdf.index[0]]
    rec_date = rdf['date'][rdf.index[0]]
    country = rdf['country'][rdf.index[0]]

    info = f'\nXCode: {rcode}\nEbird Code: {ebird_code}\nBird Species: {bird_species}\
\nRecorded On: {rec_date}\nRecorded In: {country}\n'
    
    return info, rwave


def display_popup(msg, info):
    """Display a self-destructing popup msg."
    
    Args:
    -----
    msg -- time, stand or sit message
    info -- basic info about the recording
    
    TODO: add a picture of bird  
    """
    # instantiate Tkinter
    root = Tk()
    
    # prepare prompt
    prompt = '\n'.join([msg, info])
    label = Label(root, text=prompt, width=len(prompt))
    label.pack()

    def popup_box():
        root.destroy()
        
    # 6 secs
    root.after(6000, popup_box)
    root.mainloop()
    
    
def play_audio(info, rwave):
    """Play a bird call for 10 seconds.
    
    Args:
    -----
    info -- basic info about the recording
    rwave -- random wave file path for audio playback    
    """

    print(info)

    chunk = 1024
    
    wf = wave.open(rwave, 'rb')

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
    # rather: for 10 secs
    while time.time() - T1 < 10:
        stream.write(data)
        data = wf.readframes(chunk)
    
    # stop stream
    stream.stop_stream()
    stream.close()

    # close PyAudio
    p.terminate()


def run_processes(msg):
    """Run both popup and audio processes simultaneously.
    
    TODO: make it work, not simultaneous so far... 
    """
    rand = random.randint(1, len(waves)-1)
    info, rwave = get_info(rand)
    
    with cf.ThreadPoolExecutor(max_workers=2) as executor:
        p1 = executor.submit(play_audio(info, rwave), None, None)
        p2 = executor.submit(display_popup(msg, info), None, None)
        
        
def move_user(direction):
    """Message user to stand up or sit down:
    1. Playing a birdsong to get user's attention.
    2. Printing instructions to the console.
    3. Make a popup dialog box appear with info.
    """
    if direction == "up":
        # get time 
        day, now = get_time()
        msg = f'{now} - If you\'d be so kind as to stand now. Much appreciated!'
        print(msg)
        # play audio, popup box, wait 
        run_processes(msg)
        time.sleep(stand_sec)       
    else:    
        # get time        
        day, now = get_time()
        msg = f'{now} - That was FANTASTIC work! You may sit now.'
        print(msg)
        # play audio, popup box, wait        
        run_processes(msg)
        time.sleep(sit_sec)
        

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
    raw_username = input("What do I call you? ")
    raw_sit_min = input("Set sitting minutes: ")
    raw_stand_min = input("Set standing minutes: ")
    raw_times = input("How many times? ")
    
    # TODO: sanitize input for SQL injections and the like
    #
    #
    #
    #
    
    # validate user data
    username = str(raw_username)
    
    if username:
        pass
    else:
        print("Error: must provide a valid 'username'.")
        exit(1)

    try:
        sit_min = float(raw_sit_min)
    except ValueError as e:
        print("Error: 'sit_min' must be an integer or float.")
        exit(1)
      
    try:
        stand_min = float(raw_stand_min)
    except ValueError as e:
        print("Error: 'stand_min' must be an integer or float.")
        exit(1)
    
    try:
        times = int(raw_times)
    except ValueError as e:
        print("Error: 'times' must be an integer.")
        exit(1)
        
    # calculate secs
    sit_sec = float(sit_min)*60
    stand_sec = float(stand_min)*60

    # start work session
    print(f'\nThank you {username}, your wish is my command.')
    print("Please have a seat.\n")
    
    day, start_time = get_time()
    print(f'Day: {day}')
    print(f'Start time: {start_time}\n')
    time.sleep(sit_sec)
    
    # repeat 'times' times...
    for i in range(times):
        if i+1 == times:
            move_user('up')
        else:
            move_user('up')
            move_user('down')
            
    # end work session
    day, end_time = get_time()
    msg = f'{end_time} - Excellent work all around {username}, how about that break?'
    print(msg)  
    # play audio, popup box	
    run_processes(msg)