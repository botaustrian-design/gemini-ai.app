import streamlit as st
import urllib.request
import json

st.set_page_config(page_title="Yapay Zeka Asistanım", page_icon="🤖")
st.title("🤖 Benim Yapay Zeka Asistanım")

# Videodaki token'ını buraya ekledik
TOKEN = "AQ.Ab8RN6LwOiChGgOcYznWupYYzxQyJkI0wqxp3ABwdObsHABF1A"

# AQ token'ları için URL'de ?key= KULLANILMAZ
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
    
    # AQ token'ları için en önemli kısım: Authorization Bearer header'ı
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}"
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
        
