import json
import urllib.error
import urllib.request
import streamlit as st

st.set_page_config(page_title="E-Bot Asistan", page_icon="⚡")

# --- 1. SESSION STATE (Oturum Hafızası) BAŞLANGICI ---
if "page" not in st.session_state:
  st.session_state.page = "chat"
if "theme" not in st.session_state:
  st.session_state.theme = "Koyu Mod"
if "language" not in st.session_state:
  st.session_state.language = "Türkçe 🇹🇷"
if "messages" not in st.session_state:
  st.session_state.messages = []

# --- 2. TEMA VE RENK MODU CSS AYARLARI ---
theme_styles = {
    "Koyu Mod": {
        "bg": "#0e1117",
        "text": "#ffffff",
        "card": "#1e2129",
        "accent": "linear-gradient(135deg, #6366f1, #a855f7)",
    },
    "Açık Mod": {
        "bg": "#ffffff",
        "text": "#111111",
        "card": "#f0f2f6",
        "accent": "linear-gradient(135deg, #3b82f6, #1d4ed8)",
    },
    "Neon Mor": {
        "bg": "#090514",
        "text": "#f3e8ff",
        "card": "#170f2b",
        "accent": "linear-gradient(135deg, #a855f7, #ec4899)",
    },
    "Okyanus Mavisi": {
        "bg": "#030712",
        "text": "#e0f2fe",
        "card": "#0c192c",
        "accent": "linear-gradient(135deg, #0ea5e9, #2563eb)",
    },
}

current_theme = theme_styles.get(
    st.session_state.theme, theme_styles["Koyu Mod"]
)

st.markdown(
    f"""
    <style>
    /* Genel Stiller ve Streamlit Kalıntılarını Gizleme */
    header {{ visibility: hidden !important; }}
    footer {{ visibility: hidden !important; }}
    #MainMenu {{ visibility: hidden !important; }}
    
    /* Mobil Zoom Engelleme */
    input, textarea, [data-baseweb="base-input"] {{
        font-size: 16px !important;
    }}
    
    /* Profil İkonlarını Gizleme */
    [data-testid="stChatMessageAvatar"], 
    [data-testid="stChatMessageAvatarUser"], 
    [data-testid="stChatMessageAvatarAssistant"] {{
        display: none !important;
    }}
    
    /* Özel Başlık ve Logo Tasarımı */
    .custom-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }}
    .header-left {{
        display: flex;
        align-items: center;
        gap: 14px;
    }}
    .custom-logo {{
        width: 42px;
        height: 42px;
        background: {current_theme['accent']};
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        color: white;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }}
    .custom-title {{
        font-size: 24px;
        font-weight: 700;
        color: {current_theme['text']};
        margin: 0;
        letter-spacing: -0.5px;
    }}
    </style>
""",
    unsafe_allow_html=True,
)

URL = "https://router.huggingface.co/v1/chat/completions"

# --- 3. SAYFA 1: ANA SOHBET EKRANI ---
if st.session_state.page == "chat":
  col1, col2 = st.columns([6, 1])
  with col1:
    st.markdown(
        f"""
        <div class="custom-header" style="border:none; margin-bottom:0px; padding-bottom:0px;">
            <div class="header-left">
                <div class="custom-logo">⚡</div>
                <h2 class="custom-title" style="font-size:22px;">E-Bot Asistan</h2>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
  with col2:
    if st.button("⚙️ Ayarlar", use_container_width=True):
      st.session_state.page = "settings"
      st.rerun()

  st.markdown(
      "<hr style='margin-top:5px; margin-bottom:20px;"
      " border-color:rgba(255,255,255,0.1);'>",
      unsafe_allow_html=True,
  )

  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  if prompt := st.chat_input("E-Bot'a bir şeyler yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
      st.markdown(prompt)

    # Seçilen dile göre sistem komutu
    lang_instructions = {
        "Türkçe 🇹🇷": "Türkçe",
        "Almanca 🇩🇪": "Almanca (German)",
        "İngilizce 🇬🇧": "İngilizce (English)",
        "Fransızca 🇫🇷": "Fransızca (French)",
        "İtalyanca 🇮🇹": "İtalyanca (Italian)",
        "İspanyolca 🇪🇸": "İspanyolca (Spanish)",
        "Rusça 🇷🇺": "Rusça (Russian)",
        "Arapça 🇸🇦": "Arapça (Arabic)",
        "Çince 🇨🇳": "Çince (Chinese)",
    }
    selected_lang = lang_instructions.get(
        st.session_state.language, "Türkçe"
    )

    system_prompt = {
        "role": "system",
        "content": (
            f"Sen E-Bot adında bir yapay zekasın. Kullanıcıya her konuda"
            f" yardımcı ol. Kesinlikle ve sadece şu dilde yanıt ver:"
            f" {selected_lang}."
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
      st.error(f"HTTP Hatası {e.code}")
    except Exception as e:
      st.error(f"Hata oluştu: {e}")

# --- 4. SAYFA 2: AYARLAR MENÜSÜ ---
elif st.session_state.page == "settings":
  st.title("⚙️ Ayarlar")
  st.write("Uygulama görünümünü ve dil tercihlerini buradan yönetebilirsin.")

  if st.button("🎨 Renk Modları", use_container_width=True):
    st.session_state.page = "themes"
    st.rerun()

  if st.button("🌍 Diller", use_container_width=True):
    st.session_state.page = "languages"
    st.rerun()

  st.write("")
  if st.button("⬅️ Sohbet'e Dön", use_container_width=True):
    st.session_state.page = "chat"
    st.rerun()

# --- 5. SAYFA 3: RENK MODLARI SAYFASI ---
elif st.session_state.page == "themes":
  st.title("🎨 Renk Modları")
  st.write("Uygulamanın tema rengini seç:")

  themes_list = ["Koyu Mod", "Açık Mod", "Neon Mor", "Okyanus Mavisi"]
  for t in themes_list:
    if st.button(
        f"{'✅ ' if st.session_state.theme == t else ''}{t}",
        use_container_width=True,
    ):
      st.session_state.theme = t
      st.rerun()

  st.write("")
  if st.button("⬅️ Ayarlara Dön", use_container_width=True):
    st.session_state.page = "settings"
    st.rerun()

# --- 6. SAYFA 4: DİLLER SAYFASI ---
elif st.session_state.page == "languages":
  st.title("🌍 Dil Seçimi")
  st.write("E-Bot'un konuşmasını istediğin dili seç:")

  languages_list = [
      "Türkçe 🇹🇷",
      "Almanca 🇩🇪",
      "İngilizce 🇬🇧",
      "Fransızca 🇫🇷",
      "İtalyanca 🇮🇹",
      "İspanyolca 🇪🇸",
      "Rusça 🇷🇺",
      "Arapça 🇸🇦",
      "Çince 🇨🇳",
  ]

  for lang in languages_list:
    if st.button(
        f"{'✅ ' if st.session_state.language == lang else ''}{lang}",
        use_container_width=True,
    ):
      st.session_state.language = lang
      st.rerun()

  st.write("")
  if st.button("⬅️ Ayarlara Dön", use_container_width=True):
    st.session_state.page = "settings"
    st.rerun()
    
