import streamlit as st
from googlesearch import search
from bs4 import BeautifulSoup
import requests

st.set_page_config(page_title="Analisi Software Capital Market", layout="wide")
st.title("🔍 Analisi Software per Capital Market & Wealth Management")

software = st.text_input("Inserisci il nome del software", "")

if st.button("Cerca informazioni"):
    if not software.strip():
        st.warning("Inserisci un nome valido.")
    else:
        st.write(f"📡 Ricerca online per: **{software}**...")
        query = f"{software} capital market wealth management software"
        results = list(search(query, num_results=10))
        
        st.subheader("🔗 Risultati trovati")
        for url in results:
            try:
                res = requests.get(url, timeout=5)
                soup = BeautifulSoup(res.text, "html.parser")
                title = soup.title.string if soup.title else url
            except:
                title = url
            st.markdown(f"- [{title}]({url})")