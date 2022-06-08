# Auotmatic Speech Recognition 
this project is based on the offline speech recognition API VOSK: https://github.com/alphacep/vosk-api. The goal is to automatically transcibe interviews. 

## VOSK INSTALLATION

* make sure to have python and mambaforge installed
* download the big german vosk model and place it in same folder as python file: https://alphacephei.com/vosk/models

## DEPENDENCIES
* Doc: `pip install python-docx`
* ffmpeg: https://de.wikihow.com/FFmpeg-unter-Windows-installieren 
* Truecase: `pip install nlp` & download german corpus: `python -m spacy download de_core_news_sm` (https://spacy.io/models/de)
* GUI: `pip install PySimpleGUI` (only neceassary if using speechtotext_GUI.py)

## RUN 
* switch to path of your vosk model
* run: `python speechtotext.py audio.wav` or `python speechtotext_GUI.py` when using the GUI. 

