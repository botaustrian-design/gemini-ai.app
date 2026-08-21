import streamlit as st
import urllib.request
import json

st.set_page_config(page_title="Yapay Zeka Asistanım", page_icon="🤖")
st.title("🤖 Benim Yapay Zeka Asistanım")

# Senin yeni ve güncel anahtarın
API_KEY = "AQ.Ab8RN6KCwUNe4iaTrz6kY_YgBxxhsSOuVFWFLFDsoRRjDMwmxQ"

# URL'den ?key= kısmını tamamen kaldırdık
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Yapay zekaya bir şeyler yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    contents = [{"role": "user" if m["role"] == "user" else "model", "parts": [{"text": m["content"]}]} for m in st.session_state.messages]
    
    # İŞTE SİHİRLİ KISIM: Anahtarı Google'ın özel başlığı ile gönderiyoruz
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    }
    
    data = {"contents": contents}
    req = urllib.request.Request(URL, data=json.dumps(data).encode("utf-8"), headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode("utf-8"))
            bot_reply = res['candidates'][0]['content']['parts'][0]['text']
            
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            with st.chat_message("assistant"):
                st.markdown(bot_reply)
    except Exception as e:
        st.error(f"Hata oluştu: {e}")
        
