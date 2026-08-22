import json
import urllib.error
import urllib.request
import streamlit as st

st.set_page_config(page_title="E-Bot Asistan", page_icon="⚡")

# Güvenli CSS: Simgeleri ve üst menüyü gizler, beyaz sayfa hatası yaratmaz
st.markdown(
    """
    <style>
    /* Streamlit üst menü ve footer gizleme */
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    #MainMenu { visibility: hidden !important; }
    .viewerBadge_container { display: none !important; }
    
    /* Mobilde inputa tıklayınca zoom engelleme (16px) */
    input, textarea, [data-baseweb="base-input"] {
        font-size: 16px !important;
    }
    
    /* Sohbet içi profil ikonlarını tamamen gizleme */
    [data-testid="stChatMessageAvatar"], 
    [data-testid="stChatMessageAvatarUser"], 
    [data-testid="stChatMessageAvatarAssistant"] {
        display: none !important;
    }
    
    /* Şık Logo ve Başlık Tasarımı */
    .custom-header {
        display: flex;
        align-items: center;
        gap: 14px;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    .custom-logo {
        width: 42px;
        height: 42px;
        background: linear-gradient(135deg, #6366f1, #a855f7);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        color: white;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    .custom-title {
        font-size: 24px;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.5px;
    }
    </style>
    
    <div class="custom-header">
        <div class="custom-logo">⚡</div>
        <h2 class="custom-title">E-Bot Asistan</h2>
    </div>
""",
    unsafe_allow_html=True,
)

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
      
