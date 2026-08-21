import streamlit as st
import urllib.request
import json

st.set_page_config(page_title="Yapay Zeka Asistanım", page_icon="🤖")
st.title("🤖 Benim Yapay Zeka Asistanım")

API_KEY = "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"
URL = "https://api.groq.com/openai/v1/chat/completions"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Yapay zekaya bir şeyler yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
        "User-Agent": "Mozilla/5.0"
    }
    
    # En stabil çalışan ana model
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": messages
    }
    
    req = urllib.request.Request(URL, data=json.dumps(data).encode("utf-8"), headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode("utf-8"))
            bot_reply = res['choices'][0]['message']['content']
            
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            with st.chat_message("assistant"):
                st.markdown(bot_reply)
    except Exception as e:
        st.error(f"Hata oluştu: {e}")
        
