# Auotmatic Speech Recognition 
this project is based on the offline speech recognition API VOSK: https://github.com/alphacep/vosk-api in order to transcibe interviews 

## VOSK INSTALLATION

1) Update python 
2) Use mambaforge
3) download german vosk model: https://alphacephei.com/vosk/models

## DEPENDENCIES
 1) Doc: `pip install python-docx`
 2) ffmpeg: https://de.wikihow.com/FFmpeg-unter-Windows-installieren 
 3) UI: `pip install PySimpleGUI`
 4) Truecase: `pip install nlp` | download german corpus: `python -m spacy download de_core_news_sm` (https://spacy.io/models/de)

## RUN 
* switch to path of your vosk model
* run: `python speechtotext.py audio.wav`

