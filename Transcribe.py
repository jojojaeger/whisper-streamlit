import streamlit as st
from transcriber import Transcription
import docx
from datetime import datetime
import pathlib
import io
import json
import os
import time

# app wide config
st.set_page_config(
    page_title="Whisper",
    layout="wide",
    page_icon="💬"
)

# load stylesheet
with open('style.css') as f:
    st.markdown('<style>{}</style>'.format(f.read()),
                unsafe_allow_html=True)

# app sidebar for uplading audio files
with st.sidebar.form("input_form"):
    input_files = st.file_uploader(
        "Files", type=["mp4", "m4a", "mp3", "wav"], accept_multiple_files=True)

    whisper_model = st.selectbox("Whisper model", options=[
        "tiny", "base", "small", "medium", "large"], index=4)

    speaker_diarization = st.checkbox(
        "Sprechererkennung", value=False)

    pauses = st.checkbox("Pausen transkribieren", value=False)

    transcribe = st.form_submit_button(label="Start")

if transcribe:
    if input_files:
        st.session_state.transcription = Transcription(
            input_files, speaker_diarization)
        st.session_state.transcription.transcribe(
            whisper_model
        )
    else:
        st.error("Bitte wählen Sie eine Datei")

# if there is a transcription, render it. If not, display instructions
if "transcription" in st.session_state:

    for output in st.session_state.transcription.output:
        doc = docx.Document()
        save_dir = str(pathlib.Path(__file__).parent.absolute()
                       ) + "/transcripts/"
        st.markdown(
            f"#### Transcription of {output['name']}")
        st.markdown(
            f"_(whisper model:_`{whisper_model}` -  _language:_ `{output['language']}`)")
        prev_word_end = -1
        text = ""
        docx = ""

        with st.expander("Transkript"):
            if speaker_diarization:
                speakers = {'SPEAKER_00': 'A', 'SPEAKER_01': 'B'}
                for idx, group in enumerate(output['diarization']):
                    try:
                        captions = json.load(
                            open(f"buffer/{idx}.json"))['segments']
                    except Exception as ex:
                        print(ex)
                    if captions:
                        if idx == 0 and speakers.get(group[0].split()[-1], "") == 'B':
                            speakers['SPEAKER_00'], speakers['SPEAKER_01'] = speakers['SPEAKER_01'], speakers['SPEAKER_00']
                        speaker = speakers.get(group[0].split()[-1], "")
                        if idx != 0:
                            text += "<br><br>"
                        text += f"{speaker}: "
                        for c in captions:
                            for w in c['words']:
                                if w['word']:
                                    if pauses and prev_word_end != -1 and w['start'] - prev_word_end >= 3:
                                        pause = w['start'] - prev_word_end
                                        pause_int = int(pause)
                                        text += f'{"."*pause_int}{{{pause_int}sek}}'
                                    prev_word_end = w['end']
                                    text += w['word']
            else:
                for idx, segment in enumerate(output['segments']):
                    for w in output['segments'][idx]['words']:
                        # check for pauses in speech longer than 3s
                        if pauses and prev_word_end != -1 and w['start'] - prev_word_end >= 3:
                            pause = w['start'] - prev_word_end
                            pause_int = int(pause)
                            text += f'{"."*pause_int}{{{pause_int}sek}}'
                        prev_word_end = w['end']
                        text += w['word']
                        # insert line break if there is a punctuation mark
                        if any(c in w['word'] for c in "!?.") and not any(c.isdigit() for c in w['word']):
                            text += "<br><br>"
            st.markdown(text, unsafe_allow_html=True)
            doc.add_paragraph(text)
            # replace <br> with line breaks
            for para in doc.paragraphs:
                if '<br>' in para.text:
                    para.text = para.text.replace('<br>', '\n')

        # save transcript as docx. in local folder
        file_name = output['name'] + "-" + whisper_model + \
            "-" + datetime.today().strftime('%d-%m-%y') + ".docx"
        doc.save(save_dir + file_name)

        bio = io.BytesIO()
        doc.save(bio)
        st.download_button(
            label="Download Transkript",
            data=bio.getvalue(),
            file_name=file_name,
            mime="docx"
        )

        # delete buffer files
        folder_contents = os.listdir('buffer')

        for item in folder_contents:
            item_path = os.path.join('buffer', item)
            try:
                with open(item_path, 'r') as file:
                    pass
                os.remove(item_path)
            except:
                pass
else:
    # show instruction page
    st.markdown("<h1>WHISPER - AUTOMATISCHE TRANSKRIPTION </h1> <p> Dieses Projekt wurde im Rahmen der Masterarbeit von <a href='mailto:johanna.jaeger89@icloud.com'> Johanna Jäger<a/> " +
                "unter der Verwendung von <a href='https://openai.com/blog/whisper'> OpenAI Whisper</a> durchgeführt.</p> <h2 class='highlight'>DATENSCHUTZ: </h2> <p>Das Programm wird lokal ausgeführt. " +
                "Die Transkripte werden in ein lokales Verzeichnis dieses PCs gespeichert. </p><h2 class='highlight'>VERWENDUNG: </h2> <ol><li> Wählen Sie die Dateien aus, die Sie transkribieren lassen möchten (mehrere Dateien möglich)</li>" +
                "<li>  Wählen Sie ein Modell (<i>large</i> für das beste Resultat) und andere Parameter aus und klicken Sie auf 'Start'</li> <li>  Sehen Sie sich die entstandenen Transkripte im <i>transcripts</i>-Ordner dieses Verzeichnisses an </li></ol>",
                unsafe_allow_html=True)
