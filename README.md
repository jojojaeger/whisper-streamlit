# Whisper with Streamlit UI
This project is a tool that was developed as part of a Master's thesis in cooperation with the University Clinic of Psychoanalysis and Psychotherapy of Vienna. It is based on the Whisper automatic speech recogniton system and is embedded into a Streamlit Web App. 

## Features

- Streamlit UI: The tool includes a user-friendly interface that allows you to upload multiple audio files and get a nicely formated transcript.
- Pause detection: The tool can detect pauses in the audio.
- Confidence scores: The tool can color the words according to its probability and display the average score.
- Translation to english 
- Speaker detection: The tool can also detect different speakers in the audio and label them accordingly. (still experimental, available in whisper-streamlit-speaker folder)

## Data Privacy

- Whisper is used locally as well as offline (no internet connection needed)
- Nothing is being uploaded to the cloud
- Therefore safe clinical use 

## User Interface

Start Screen            |  Results
:-------------------------:|:-------------------------:
![](https://user-images.githubusercontent.com/65357373/226929650-97a978c7-5ea9-41dd-8c25-660d4d2eea43.png)  |  ![](https://user-images.githubusercontent.com/65357373/226930996-26aaafb3-138c-4cea-964d-c9459c3e92f5.png)

## Getting Started

To use this tool, you will need to install the required dependencies and run the Streamlit app. You can do this by following these steps:

1. Clone the repository: git clone https://github.com/jojojaeger/whisper-streamlit
2. Install prerequisites: Python, Pip, Git, PyTorch (pip install torch torchvision torchaudio)
3. Install dependencies: pip install -r requirements.txt
4. Run the Streamlit app: streamlit run Transcribe.py (you can also launch it from a desktop shortcut following these instructions: https://discuss.streamlit.io/t/launching-streamlit-webapp-from-desktop-shortcut/26297)

## How to Use

1. Upload one or multiple audio files 
2. Select a model (large for the best result) and set additional parameters 
3. Download the resulting transcript (also saved to local transcripts-folder)

## Fixes to common errors

* Error: Request failed with status code 403 -> run the app with "--server.enableWebsocketCompression=false"

## Contact

If you have any questions or feedback about this project, please feel free to contact us by email at johanna.jaeger89@icloud.com.

## Sources

This project includes code from multiple different sources, each licensed under the MIT License:

* [Source A] (https://github.com/openai/whisper)
* [Source A] (https://github.com/pyannote/pyannote-audio)
* [Source C] (https://github.com/hayabhay/whisper-ui)

See the LICENSE file for the full text of the licenses.
