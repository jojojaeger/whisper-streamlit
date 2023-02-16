from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch
import sys
import librosa
import soundfile as sf
import PySimpleGUI as sg
import docx
from datetime import datetime


# UI
files = sg.popup_get_file('Select files (.wav, .mp3)', multiple_files=True)

# pretrained multilingual model wav2vec 2.0 (XLSR) pretrained in 53 languages
# 18.5 in german
tokenizer = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-xlsr-53-german")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-xlsr-53-german")

def asr_transcript(tokenizer, model, input_file):
    transcript = ""
     # define doc
    doc = docx.Document()

    # stream over 20 seconds chunks 
    stream = librosa.stream(
        input_file,
        block_length=25,
        frame_length=16000,
        hop_length=16000
    )

    for speech in stream:
        if len(speech.shape) > 1:
            speech = speech[:, 0] + speech[:, 1]

        input_values = tokenizer(speech, return_tensors="pt").input_values
        logits = model(input_values).logits

        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = tokenizer.decode(predicted_ids[0])
        transcript += transcription
        
    doc.add_paragraph(transcript)
    file_name = str(input_file).split("/")[-1]
    doc.save("C:/Wav2Vec/" + file_name + datetime.today().strftime('%d-%m-%y') + ".docx")

    return transcript
    
   
if files:
    files = files.split(";")
    print(files)
    for idx, file in enumerate(files):
       print(files[idx])
       file = asr_transcript(tokenizer, model, files[idx]) 

