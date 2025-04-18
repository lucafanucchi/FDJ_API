# app.py

import streamlit as st
import os
import tempfile
import shutil
import time
import requests

st.set_page_config(page_title="Playlist Downloader", layout="centered")
st.text("✅ Streamlit carregado")


from spotify_utils import get_spotify_tracks
from deezer_utils import get_deezer_tracks
from youtube_utils import search_and_download
from zip_utils import zip_directory

st.title("Playlist Downloader")

# Inicialização segura de variáveis de estado
if 'tracks' not in st.session_state:
    st.session_state.tracks = []
if 'selected_tracks' not in st.session_state:
    st.session_state.selected_tracks = {}

# Seletor de plataforma e input de URL
platform = st.selectbox("Plataforma da playlist", ["Spotify", "Deezer"])
playlist_url = st.text_input("Link da playlist")

# Botão para carregar músicas
if st.button("Carregar músicas") and playlist_url:
    if platform == "Spotify":
        st.session_state.tracks = get_spotify_tracks(playlist_url)
    else:
        st.session_state.tracks = get_deezer_tracks(playlist_url)

    st.session_state.selected_tracks = {
        f"{t['artist']} - {t['title']}": True for t in st.session_state.tracks
    }

# Exibição das músicas com checkboxes
if st.session_state.tracks:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Selecionar todas"):
            for key in st.session_state.selected_tracks:
                st.session_state.selected_tracks[key] = True
    with col2:
        if st.button("Desmarcar todas"):
            for key in st.session_state.selected_tracks:
                st.session_state.selected_tracks[key] = False

    for track in st.session_state.tracks:
        name = f"{track['artist']} - {track['title']}"
        checked = st.checkbox(
            label=name,
            value=st.session_state.selected_tracks.get(name, False),
            key=f"chk_{name}"
        )
        st.session_state.selected_tracks[name] = checked

# Baixar músicas — somente dentro do botão
if st.session_state.tracks and st.button("Baixar músicas"):
    selected_names = [name for name, selected in st.session_state.selected_tracks.items() if selected]

    if not selected_names:
        st.warning("Nenhuma música selecionada.")
    else:
        temp_dir = tempfile.mkdtemp()
        status_text = st.empty()
        st.markdown("Iniciando download...")

        for track in st.session_state.tracks:
            name = f"{track['artist']} - {track['title']}"
            if name in selected_names:
                status_text.markdown(f"Baixando: **{name}**")
                search_and_download(name, temp_dir)
                time.sleep(0.3)

        status_text.markdown("Download finalizado!")
        zip_file_path = zip_directory(temp_dir, "musicas_baixadas")
        with open(zip_file_path, "rb") as f:
            st.download_button(
                label="Baixar ZIP",
                data=f,
                file_name=os.path.basename(zip_file_path),
                mime="application/zip"
            )
        shutil.rmtree(temp_dir)
