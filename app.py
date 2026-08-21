import streamlit as st
import urllib.request
import json
import urllib.error

st.set_page_config(page_title="Yapay Zeka Asistanım", page_icon="🤖")
st.title("🤖 Benim Yapay Zeka Asistanım")

API_KEY = "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"
URL = "https://openrouter.ai/api/v1/chat/completions"

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
        "HTTP-Referer": "https://streamlit.app",
        "X-Title": "Benim Yapay Zeka Asistanim",
        "User-Agent": "Mozilla/5.0"
    }
    
    # OpenRouter üzerinden çalışan stabil ve ücretsiz model
    data = {
        "model": "google/gemma-2-9b-it:free",
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
    except urllib.error.HTTPError as e:
        error_detail = e.read().decode("utf-8")
        st.error(f"HTTP Hatası {e.code}: {error_detail}")
    except Exception as e:
        st.error(f"Hata oluştu: {e}")
        
