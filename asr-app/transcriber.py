from typing import Union
import torch
from stable_whisper import load_model
from tempfile import NamedTemporaryFile


class Transcription:
    def __init__(self, source: list):
        self.source = source
        self.audios = []

        for file in self.source:
            with NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                tmp_file.write(file.getvalue())
                self.audios.append(tmp_file.name)

    def transcribe(
        self,
        whisper_model: str,
        keep_model_in_memory: bool = True,
    ):

        # Get whisper model
        transcriber = load_model(whisper_model)

        self.output = []

        for idx, _ in enumerate(self.audios):
            # Transcription is being done here
            self.raw_output = transcriber.transcribe(
                self.audios[idx],
                verbose=True,
            )
            self.raw_output["name"] = self.source[idx].name
            self.text = self.raw_output["text"]
            self.language = self.raw_output["language"]
            self.segments = self.raw_output["segments"]
            for segment in self.segments:
                del segment["tokens"]
            self.output.append(self.raw_output)

        if not keep_model_in_memory:
            del transcriber
            torch.cuda.empty_cache()
