import os
import subprocess

mp3_dir = os.path.join("audio", "mp3")
wav_dir = os.path.join("audio", "wav")

for subdir in os.listdir(mp3_dir):

    mp3_subdir = os.path.join(mp3_dir, subdir)
    wav_subdir = os.path.join(wav_dir, subdir)
    
    try:
        os.stat(wav_subdir)
    except FileNotFoundError:
        os.makedirs(wav_subdir)
    
    for mp3 in os.listdir(mp3_subdir):
    
        wav = ''.join([mp3.split('.')[0], '.wav'])
        
        mp3_filepath = os.path.join(mp3_subdir, mp3)
        wav_filepath = os.path.join(wav_subdir, wav)

        subprocess.call([
            'ffmpeg', '-hide_banner', 
            '-loglevel', 'quiet', 
            '-i', mp3_filepath, wav_filepath
        ])