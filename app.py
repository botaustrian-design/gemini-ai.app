import json
import urllib.error
import urllib.request
import streamlit as st

st.set_page_config(page_title="E-Bot Yapay Zeka", page_icon="🤖")

# CSS: Mobilde zoom engelleme ve profil ikonlarını tamamen gizleme
st.markdown(
    """
    <style>
    /* 1. Mobilde inputa tıklayınca zoom yapmasını engeller */
    input, textarea, [data-baseweb="base-input"] {
        font-size: 16px !important;
    }
    
    /* 2. Kırmızı ve turuncu dahil tüm profil (avatar) ikonlarını tamamen gizler */
    [data-testid="stChatMessageAvatar"], 
    [data-testid="stChatMessageAvatarUser"], 
    [data-testid="stChatMessageAvatarAssistant"] {
        display: none !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🤖 E-Bot Asistan")

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

  # API anahtarı kodda yer almıyor, doğrudan Streamlit secrets'tan okunuyor
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
      
