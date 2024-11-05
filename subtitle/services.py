import subprocess
from services.srt_compose import srt_compose
from services.translation import translation
from services.speaker_diarization import speaker_diarizer
from services.stt import stt
from pyannote.audio import Audio
from pyannote.core import Segment
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

def shift_segments(segments, shift_in_sec):
    for seg in segments:
        seg['start'] += shift_in_sec
        seg['end'] += shift_in_sec
    return segments

def generate_segments(audio_path):
    audio_tool = Audio()
    diarization = speaker_diarizer.diarize(audio_path)
    segments = []
    for segment in diarization:
        wave, sr = audio_tool.crop(audio_path, Segment(segment['start'], segment['end']))
        if sr != 16000:
            print('invalid sample rate')
            return []
        nested_segments = stt.transcribe(wave.squeeze())
        nested_segments = shift_segments(nested_segments, segment['start'])
        segments += nested_segments
    return segments