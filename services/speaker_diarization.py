from pyannote.audio import Pipeline, Audio
from pyannote.core import Segment

class SpeakerDiarizer:
    def __init__(self) -> None:
        hugging_face_token = "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"
        self.pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=hugging_face_token)
    
    def diarize(self, path):
        diarization = self.pipeline(path)
        result = []
        for turn, _, _ in diarization.itertracks(yield_label=True):
            result.append({'start': turn.start, 'end': turn.end})
        return result
    
speaker_diarizer = SpeakerDiarizer()