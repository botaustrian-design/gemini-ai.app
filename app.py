import json
import urllib.error
import urllib.request
import streamlit as st

st.set_page_config(page_title="E-Bot Asistan", page_icon="⚡")

# Profesyonel görünüm için tüm Streamlit kalıntılarını ve ikonları gizleyen CSS
st.markdown(
    """
    <style>
    /* 1. Üstteki Streamlit menü, Fork ve GitHub buton çubuğunu tamamen gizle */
    header {visibility: hidden !important;}
    
    /* 2. Alttaki "Hosted with Streamlit" rozetini ve logoları tamamen gizle */
    footer {visibility: hidden !important;}
    .viewerBadge_container__1QSob {display: none !important;}
    
    /* 3. Mobilde inputa tıklayınca ekranın zoom yapmasını engelle */
    input, textarea, [data-baseweb="base-input"] {
        font-size: 16px !important;
    }
    
    /* 4. Sohbet içerisindeki profil ikonlarını tamamen ortadan kaldır */
    [data-testid="stChatMessageAvatar"], 
    [data-testid="stChatMessageAvatarUser"], 
    [data-testid="stChatMessageAvatarAssistant"] {
        display: none !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("E-Bot Asistan")

URL = "https://router.huggingface.co/v1/chat/completions"

if "messages" not in st.session_state:
  st.session_state.messages = []

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

if prompt := st.chat_input("E-Bot'a bir şeyler yaz..."):
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  system_prompt = {
      "role": "system",
      "content": (
          "Sen E-Bot adında, kullanıcıya her konuda yardımcı olan, akıllı,"
          " samimi ve net bir yapay zeka asistanısın."
      ),
  }

  messages = [system_prompt] + [
      {"role": m["role"], "content": m["content"]}
      for m in st.session_state.messages
  ]

  headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {st.secrets['HF_KEY']}",
      "User-Agent": "Mozilla/5.0",
  }

  data = {
      "model": "meta-llama/Llama-3.1-8B-Instruct",
      "messages": messages,
      "max_tokens": 800,
  }

  req = urllib.request.Request(
      URL, data=json.dumps(data).encode("utf-8"), headers=headers
  )

  try:
    with urllib.request.urlopen(req) as response:
      res = json.loads(response.read().decode("utf-8"))
      bot_reply = res["choices"][0]["message"]["content"]

      st.session_state.messages.append(
          {"role": "assistant", "content": bot_reply}
      )
      with st.chat_message("assistant"):
        st.markdown(bot_reply)
  except urllib.error.HTTPError as e:
    error_detail = e.read().decode("utf-8")
    st.error(f"HTTP Hatası {e.code}: {error_detail}")
  except Exception as e:
    st.error(f"Hata oluştu: {e}")
      
