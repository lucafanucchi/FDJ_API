import streamlit as st

st.set_page_config(page_title="Debug Test", layout="centered")
st.text("✅ Streamlit iniciou com sucesso")

if st.button("Testar"):
    st.text("🟢 Clique no botão funcionou")
