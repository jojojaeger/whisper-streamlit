import streamlit as st
from transcriber import Transcription
import docx
from datetime import datetime
import pathlib
import io
import os


# App wide config
st.set_page_config(
    page_title="Whisper",
    layout="wide",
    page_icon="💬"
)

print("hello", os.getcwd())

# load stylesheet
with open('style.css') as f:
    st.markdown('<style>{}</style>'.format(f.read()),
                unsafe_allow_html=True)

# App sidebar for uplading audio files
with st.sidebar.form("input_form"):
    input_files = st.file_uploader(
        "Files", type=["mp4", "m4a", "mp3", "wav"], accept_multiple_files=True)

    whisper_model = st.selectbox("Whisper model", options=[
        "tiny", "base", "small", "medium", "large"], index=4)

    pauses = st.checkbox("Pausen transkribieren", value=False)

    speaker_diarization = st.checkbox(
        "Sprechererkennung", value=False)

    transcribe = st.form_submit_button(label="Start")

if transcribe:
    if input_files:
        st.session_state.transcription = Transcription(
            input_files)
        st.session_state.transcription.transcribe(
            whisper_model
        )
    else:
        st.error("Bitte wählen Sie eine Datei")

# If there is a transcription, render it. If not, display instructions
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
        speaker = ""
        # initial speaker:
        if speaker_diarization:
            speaker = 'A'
            text += speaker + ": "
        with st.expander("Transkript"):
            for idx, segment in enumerate(output['segments']):

                for word in output['segments'][idx]['words']:
                    # Check for speaker change
                    if speaker_diarization:
                        for row in output['diarization']:
                            print(row[0], word['start'], row[1])
                            if (row[0] <= word['start'] <= row[1]) and speaker != row[2]:
                                speaker = row[2]
                                doc.add_paragraph(text)
                                st.markdown(text)
                                text = ""
                                text += speaker + ": "
                                break

                    # Check for pauses in speech longer than 3s
                    if pauses and prev_word_end != -1 and int(word['start'] - prev_word_end) >= 3:
                        pause = int(word['start'] - prev_word_end)
                        pause_str = "{" + str(pause) + "sek" + "}"
                        text += str(f"""{" "}{"."*pause}{pause_str}""")
                    prev_word_end = word['end']
                    text += (word['word'])
                    # Insert line break when there is a punctuation mark
                    if "!" in word['word'] or "?" in word['word'] or '.' in word['word']:
                        if not any(i.isdigit() for i in word['word']):
                            any(i.isdigit() for i in word)
                            doc.add_paragraph(text)
                            st.markdown(text)
                            text = ""
            doc.add_paragraph(text)
            st.markdown(text)
        # Save transcript as docx. in local folder
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


else:
    # show instruction page
    st.markdown("<h1>WHISPER - AUTOMATISCHE TRANSKRIPTION </h1> <p> Dieses Projekt wurde im Rahmen der Masterarbeit von <a href='mailto:johanna.jaeger89@icloud.com'> Johanna Jäger<a/> " +
                "unter der Verwendung von <a href='https://openai.com/blog/whisper'> OpenAI Whisper </a> durchgeführt.</p> <h2 class='highlight'>DATENSCHUTZ: </h2> <p>Das Programm wird lokal und offline (d.h. ohne einer vorausgesetzten Internetverbindung) ausgeführt. " +
                "Die Transkripte werden in ein lokales Verzeichnis dieses PCs gespeichert. </p><h2 class='highlight'>VERWENDUNG: </h2> <ol><li> Wählen Sie die Dateien aus, die Sie transkribieren lassen möchten (mehrere Dateien möglich)</li>" +
                "<li>  Wählen Sie ein Modell (<i>large</i> als exakteste Option) und andere Parameter aus und klicken Sie auf 'Start'</li> <li>  Sehen Sie sich die entstandenen Transkripte im <i>transcripts</i>-Ordner dieses Verzeichnisses an </li></ol>",
                unsafe_allow_html=True)
