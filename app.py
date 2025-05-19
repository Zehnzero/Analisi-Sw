import streamlit as st
from googlesearch import search
from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
from openai import OpenAI

# Carica chiave API dal file .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Analisi Software Capital Market", layout="wide")
st.title("🔍 Analisi Software per Capital Market & Wealth Management")

software = st.text_input("Inserisci il nome del software", "")

def estrai_testo(url):
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        for s in soup(['script', 'style', 'noscript']):
            s.decompose()
        testo = ' '.join(soup.stripped_strings)
        return testo[:3000]  # massimo 3000 caratteri per non sovraccaricare
    except:
        return ""

def genera_scheda(contenuti, nome_software):
    prompt = f"""
Analizza le seguenti informazioni web sul software "{nome_software}" e crea una scheda riassuntiva con:

📌 Nome software
🧾 Descrizione
📦 Moduli/funzionalità
🎯 Target (clienti)
💼 Clienti noti
🔗 Eventuale sito ufficiale

Testi da analizzare:
{contenuti}
"""
    risposta = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Sei un assistente esperto di tecnologie per il settore finanziario."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=600
    )
    return risposta.choices[0].message.content.strip()

if st.button("Cerca e analizza"):
    if not software.strip():
        st.warning("Inserisci un nome valido.")
    else:
        st.write(f"📡 Ricerca in corso per: **{software}**...")
        query = f"{software} capital market wealth management software"
        risultati = list(search(query, num_results=5))
        contenuti = ""

        st.subheader("🔗 Risultati trovati")
        for url in risultati:
            st.markdown(f"- [{url}]({url})")
            contenuti += estrai_testo(url) + "\n\n"

        with st.spinner("✍️ Generazione della scheda informativa..."):
            scheda = genera_scheda(contenuti, software)
            st.success("✅ Scheda generata con successo!")
            st.markdown("### 🧾 Scheda del Software")
            st.markdown(scheda)
