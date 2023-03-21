import torch
from whisper import load_model
from tempfile import NamedTemporaryFile
from pyannote.audio import Pipeline
import re
import librosa
import soundfile as sf
import numpy as np

from pydub import AudioSegment


class Transcription:
    def __init__(self, source: list):
        self.source = source
        self.audios = []

        print("init Transcription")

        for file in self.source:
            with NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                tmp_file.write(file.getvalue())
                self.audios.append(tmp_file.name)

    @staticmethod
    def sec(timeStr):
        spl = timeStr.split(":")
        s = int(spl[0]) * 60 * 60 + int(spl[1]) * 60 + float(spl[2])
        return np.float64("{:.3f}".format(s))

    def pyannote():
        dz = open('diarization.txt').read().splitlines()
        print(dz)
        dzList = []
        for l in dz:
            start, end = tuple(re.findall(
                '[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=l))
            start = Transcription.sec(start)
            end = Transcription.sec(end)
            print(type(start))
            speaker0 = re.findall('SPEAKER_00', string=l)
            speaker_string = "A" if speaker0 else "B"
            dzList.append([start, end, speaker_string])
        return dzList

    def transcribe(
        self,
        whisper_model: str,
        keep_model_in_memory: bool = True,
    ):

        pipeline = Pipeline.from_pretrained(
            'pyannote/speaker-diarization', use_auth_token='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')

        # Get whisper model
        transcriber = load_model(whisper_model)

        self.output = []

        for idx, _ in enumerate(self.audios):
            # Transcription is being done here
            self.raw_output = transcriber.transcribe(
                self.audios[idx],
                verbose=True,
                word_timestamps=True
            )
            # diarization
            # convert to wav
            data, sample_rate = librosa.load(self.audios[idx])
            resampled_file = librosa.resample(
                data, orig_sr=sample_rate, target_sr=16000)
            sf.write('buffer.wav', resampled_file, sample_rate)
            dz = pipeline('buffer.wav')
            print(str(dz))

            with open("diarization.txt", "w") as text_file:
                text_file.write(str(dz))

            self.raw_output["diarization"] = Transcription.pyannote()
            self.raw_output["name"] = self.source[idx].name
            self.text = self.raw_output["text"]
            self.language = self.raw_output["language"]
            self.segments = self.raw_output["segments"]
            for segment in self.segments:
                del segment["tokens"]
            self.output.append(self.raw_output)
            print(self.raw_output)

        if not keep_model_in_memory:
            del transcriber
            torch.cuda.empty_cache()
