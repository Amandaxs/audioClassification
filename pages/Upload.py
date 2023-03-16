import streamlit as st
import os.path
import pathlib
from pydub import AudioSegment

st.write("""
# File Picker
""")

import pydub
from pathlib import Path

def upload_and_save_wavfiles(save_dir: str) :
    """ limited 200MB, you could increase by `streamlit run foo.py --server.maxUploadSize=1024` """
    uploaded_files = st.file_uploader("upload", type=['wav','mp3'] ,accept_multiple_files=True)
    save_paths = []
    for uploaded_file in uploaded_files:
        if uploaded_file is not None:
            if uploaded_file.name.endswith('wav'):
                audio = pydub.AudioSegment.from_wav(uploaded_file)
                file_type = 'wav'
            elif uploaded_file.name.endswith('mp3'):
                audio = pydub.AudioSegment.from_mp3(uploaded_file)
                file_type = 'mp3'

            save_path = Path(save_dir) / uploaded_file.name
            save_paths.append(save_path)
            audio.export(save_path, format=file_type)
    return save_paths

def display_wavfile(wavpath):
    audio_bytes = open(wavpath, 'rb').read()
    file_type = Path(wavpath).suffix
    st.audio(audio_bytes, format=f'audios/{file_type}', start_time=0)


files = upload_and_save_wavfiles('audios')

for wavpath in files:
    display_wavfile(wavpath)


