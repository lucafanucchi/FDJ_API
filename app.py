import streamlit as st

st.set_page_config(page_title="Diagnóstico", layout="centered")

st.title("Teste de Inicialização")

if st.button("Rodar teste"):
    st.success("Inicialização concluída com sucesso.")
