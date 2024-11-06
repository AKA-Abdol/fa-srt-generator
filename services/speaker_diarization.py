from pyannote.audio import Pipeline
from config import settings

class SpeakerDiarizer:
    def __init__(self) -> None:
        hugging_face_token = settings.HUGGINGFACE_TOKEN
        self.pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=hugging_face_token)
    
    def diarize(self, path):
        diarization = self.pipeline(path)
        result = []
        for turn, _, _ in diarization.itertracks(yield_label=True):
            result.append({'start': turn.start, 'end': turn.end})
        return result
    
speaker_diarizer = SpeakerDiarizer()