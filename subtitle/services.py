import subprocess
from services.srt_compose import srt_compose
from services.translation import translation
from config import UPLOAD_DIR
import os

def convert_to_wav(path, filename):
    subprocess.run([
        'ffmpeg', 
        '-i', path,
        '-acodec', 'pcm_s16le',
        '-ac', '1',
        '-ar', '16000',
        os.path.join(UPLOAD_DIR, f'{filename}.wav')
    ])
    subprocess.run(['rm', '-f', path])
    return f'{filename}.wav'

def generate_srt(segments, path):
    for segment in segments:
        segment['text'] = translation.translate(segment['text'])[0]
    srt_compose.append_bulk(segments)
    srt_compose.save(path)