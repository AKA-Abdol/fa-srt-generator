import whisper

class STT:
    def __init__(self) -> None:
        self.model_name = 'medium.en'
        self.model = whisper.load_model(self.model_name)
    
    def transcribe(self, audio_path):
        return self.model.transcribe(audio_path)['segments']

stt = STT()