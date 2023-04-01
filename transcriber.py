import whisper
from tempfile import NamedTemporaryFile
from pyannote.audio import Pipeline
from typing import List
import re
import librosa
import soundfile as sf
from pydub import AudioSegment
import json


class Transcription:
    def __init__(self, source: list, diarization: bool):
        self.source = source
        self.audios = []
        self.diarization: bool = diarization

        for file in self.source:
            with NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                tmp_file.write(file.getvalue())
                self.audios.append(tmp_file.name)

    @staticmethod
    def millisec(timeStr) -> int:
        h, m, s = map(float, timeStr.split(':'))
        return int((h * 3600 + m * 60 + s) * 1000)

    @staticmethod
    def get_groups(dzs: List[str], audio_file: str) -> List[List[str]]:
        groups = []
        g = []
        last_end = 0

        for d in dzs:
            speaker = d.split()[-1]
            if g and g[0].split()[-1] != speaker:
                groups.append(g)
                g = []
            g.append(d)

            start, end = map(Transcription.millisec,
                             re.findall(r'\d+:\d+:\d+\.\d+', d))
            if last_end > start:
                groups.append(g)
                g = []
            else:
                last_end = end

        if g:
            groups.append(g)

        audio = AudioSegment.from_wav(audio_file)
        for idx, g in enumerate(groups):
            start, end = map(Transcription.millisec, [re.findall(r'\d+:\d+:\d+\.\d+', g[0])[0],
                                                      re.findall(r'\d+:\d+:\d+\.\d+', g[-1])[1]])
            audio[start:end].export(f'buffer/{idx}.wav', format='wav')
            print(f"group {idx}: {start}--{end}")
        return groups

    @staticmethod
    def pyannote(audio_file: str) -> List[List[str]]:
        data, sample_rate = librosa.load(audio_file)
        resampled_file = librosa.resample(
            data, orig_sr=sample_rate, target_sr=16000)
        sf.write('buffer/audio.wav', resampled_file, sample_rate)

        # pyannote misses the first 0.5 s - add spacer
        spacermilli = 2000
        spacer = AudioSegment.silent(duration=spacermilli)
        audio = AudioSegment.from_wav("buffer/audio.wav")
        audio = spacer.append(audio, crossfade=0)
        audio.export('buffer/audio.wav', format='wav')

        pipeline = Pipeline.from_pretrained(
            'pyannote/speaker-diarization', use_auth_token='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')
        dz = pipeline('buffer/audio.wav')
        with open("diarization.txt", "w") as text_file:
            text_file.write(str(dz))
        dzs = open('diarization.txt').read().splitlines()
        print(dzs)

        groups = Transcription.get_groups(dzs, 'buffer/audio.wav')
        return groups

    def transcribe(
        self,
        whisper_model: str,
    ):

        # get whisper model
        transcriber = whisper.load_model(whisper_model)

        self.output = []

        for idx, _ in enumerate(self.audios):

            # identify language
            audio = whisper.load_audio(self.audios[idx])
            audio = whisper.pad_or_trim(audio)
            mel = whisper.log_mel_spectrogram(audio).to(transcriber.device)
            _, probs = transcriber.detect_language(mel)
            language = max(probs, key=probs.get)

            if self.diarization:
                self.raw_output = {}
                speaker_groups = Transcription.pyannote(self.audios[idx])
                for i in range(len(speaker_groups)):
                    audio = 'buffer/' + str(i) + '.wav'
                    try:
                        result = transcriber.transcribe(
                            audio=audio, language=language, verbose=True, word_timestamps=True)
                    except Exception as ex:
                        print(ex)
                    with open('buffer/' + str(i)+'.json', "w") as outfile:
                        json.dump(result, outfile, indent=4)

                self.raw_output["diarization"] = speaker_groups
            else:
                self.raw_output = transcriber.transcribe(
                    self.audios[idx],
                    language=language,
                    verbose=True,
                    word_timestamps=True
                )
                self.segments = self.raw_output["segments"]
                for segment in self.raw_output["segments"]:
                    del segment["tokens"]

            self.raw_output.update(
                name=self.source[idx].name, language=language)
            self.output.append(self.raw_output)
