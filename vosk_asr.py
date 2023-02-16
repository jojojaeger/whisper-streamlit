from vosk import Model, KaldiRecognizer
import sys
import wave
import json
import os
import numpy as np
import docx
import subprocess
import PySimpleGUI as sg
from datetime import datetime
# import truecaser
import spacy, re

# UI
files = sg.popup_get_file('Select files (.wav, .mp3, .m4a)', multiple_files=True)


# truecaser: receives text and uses
def truecase(text):
    nlp = spacy.load('de_core_news_sm')
    doc = nlp(text)
    tagged_sent = [(w.text, w.tag_) for w in doc]
    normalized_sent = [w.capitalize() if t in ["NN","NNS"] else w for (w,t) in tagged_sent]
    normalized_sent[0] = normalized_sent[0].capitalize()
    truecased_text = re.sub(" (?=[\.,'!?:;])", "", ' '.join(normalized_sent))
    return truecased_text

# transcripter: receives audio file in wav, mp3 or m4a format and saves transcript in word file
def transcript_audio (audio):
    model_path = "model"

    # define doc
    doc = docx.Document()

    sample_rate = 16000

    # convert to wave file
    process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-i',
                                audio,
                                '-ar', str(sample_rate), '-ac', '1', '-f', 's16le', '-'],
                               stdout=subprocess.PIPE)

    model = Model(model_path)
    rec = KaldiRecognizer(model, sample_rate)

    # read data and adds paragraphs to word document
    while True:
        data = process.stdout.read(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            print(res['text'])
            if res['text'] != "":
                doc.add_paragraph(truecase(res['text']))
    file_name = str(audio).split("/")[-1]
    doc.save("C:/Vosk/" + file_name + datetime.today().strftime('%d-%m-%y') + ".docx")

    return

if files:
    files = files.split(";")
    print(files)
    for idx, file in enumerate(files):
       print(files[idx])
       file = transcript_audio(files[idx])