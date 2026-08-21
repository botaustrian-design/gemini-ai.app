import streamlit as st
import urllib.request
import json

# Sayfa Yapılandırması
st.set_page_config(page_title="Yapay Zeka Asistanım", page_icon="🤖", layout="centered")

st.title("🤖 Benim Yapay Zeka Asistanım")
st.write("Bu uygulama, herkesin internet üzerinden erişip sohbet edebileceği yapay zeka merkezidir.")

# API Şifreni koda ekledik
API_KEY = "AQ.Ab8RN6LwOiChGgOcYznWupYYzxQyJkI0wqxp3ABwdObsHABF1A"

URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

# Sohbet Hafızası
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı girişi
if prompt := st.chat_input("Yapay zekaya bir şeyler yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # API'ye gönder
    contents = []
    for m in st.session_state.messages:
        role = "user" if m["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": m["content"]}]})

    data = {"contents": contents}
    req = urllib.request.Request(
        URL,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode("utf-8"))
            bot_reply = res['candidates'][0]['content']['parts'][0]['text']
            
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            with st.chat_message("assistant"):
                st.markdown(bot_reply)
    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
        
