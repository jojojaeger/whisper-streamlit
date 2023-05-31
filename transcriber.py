import whisper
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
            print(self.output)
