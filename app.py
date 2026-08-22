import json
import urllib.error
import urllib.request
import streamlit as st

st.set_page_config(page_title="E-Bot Asistan", page_icon="⚡")

# --- 1. SESSION STATE (Oturum Hafızası) ---
if "page" not in st.session_state:
  st.session_state.page = "chat"
if "theme" not in st.session_state:
  st.session_state.theme = "Koyu Mod"
if "language" not in st.session_state:
  st.session_state.language = "Türkçe 🇹🇷"
if "messages" not in st.session_state:
  st.session_state.messages = []

# --- 2. ÇOKLU DİL SÖZLÜĞÜ (Tüm Arayüz Çevirileri) ---
translations = {
    "Türkçe 🇹🇷": {
        "settings": "⚙️ Ayarlar",
        "back_to_chat": "⬅️ Sohbet'e Dön",
        "back_to_settings": "⬅️ Ayarlara Dön",
        "theme_menu": "🎨 Renk Modları",
        "lang_menu": "🌍 Diller",
        "chat_placeholder": "E-Bot'a bir şeyler yaz...",
        "settings_title": "⚙️ Ayarlar",
        "settings_desc": (
            "Uygulama görünümünü ve dil tercihlerini buradan yönetebilirsin."
        ),
        "themes_title": "🎨 Renk Modları",
        "themes_desc": "Uygulamanın tema rengini seç:",
        "lang_title": "🌍 Dil Seçimi",
        "lang_desc": "E-Bot'un ve uygulamanın dilini seç:",
    },
    "İngilizce 🇬🇧": {
        "settings": "⚙️ Settings",
        "back_to_chat": "⬅️ Back to Chat",
        "back_to_settings": "⬅️ Back to Settings",
        "theme_menu": "🎨 Color Themes",
        "lang_menu": "🌍 Languages",
        "chat_placeholder": "Type something to E-Bot...",
        "settings_title": "⚙️ Settings",
        "settings_desc": (
            "Manage app appearance and language preferences here."
        ),
        "themes_title": "🎨 Color Themes",
        "themes_desc": "Choose the app theme color:",
        "lang_title": "🌍 Language Selection",
        "lang_desc": "Choose the language for E-Bot and the app:",
    },
    "Almanca 🇩🇪": {
        "settings": "⚙️ Einstellungen",
        "back_to_chat": "⬅️ Zurück zum Chat",
        "back_to_settings": "⬅️ Zurück zu den Einstellungen",
        "theme_menu": "🎨 Farbthemes",
        "lang_menu": "🌍 Sprachen",
        "chat_placeholder": "Schreibe etwas an E-Bot...",
        "settings_title": "⚙️ Einstellungen",
        "settings_desc": (
            "Verwalten Sie hier das App-Aussehen und die Spracheneinstellungen."
        ),
        "themes_title": "🎨 Farbthemes",
        "themes_desc": "Wählen Sie die Theme-Farbe:",
        "lang_title": "🌍 Sprachauswahl",
        "lang_desc": "Wählen Sie die Sprache für E-Bot und die App:",
    },
    "Fransızca 🇫🇷": {
        "settings": "⚙️ Paramètres",
        "back_to_chat": "⬅️ Retour au chat",
        "back_to_settings": "⬅️ Retour aux paramètres",
        "theme_menu": "🎨 Thèmes de couleurs",
        "lang_menu": "🌍 Langues",
        "chat_placeholder": "Écrivez quelque chose à E-Bot...",
        "settings_title": "⚙️ Paramètres",
        "settings_desc": (
            "Gérez l'apparence de l'application et les préférences de langue"
            " ici."
        ),
        "themes_title": "🎨 Thèmes de couleurs",
        "themes_desc": "Choisissez la couleur du thème :",
        "lang_title": "🌍 Sélection de la langue",
        "lang_desc": "Choisissez la langue pour E-Bot et l'application :",
    },
    "İtalyanca 🇮🇹": {
        "settings": "⚙️ Impostazioni",
        "back_to_chat": "⬅️ Torna alla chat",
        "back_to_settings": "⬅️ Torna alle impostazioni",
        "theme_menu": "🎨 Temi di colore",
        "lang_menu": "🌍 Lingue",
        "chat_placeholder": "Scrivi qualcosa a E-Bot...",
        "settings_title": "⚙️ Impostazioni",
        "settings_desc": (
            "Gestisci l'aspetto dell'app e le preferenze della lingua qui."
        ),
        "themes_title": "🎨 Temi di colore",
        "themes_desc": "Scegli il colore del tema:",
        "lang_title": "🌍 Selezione della lingua",
        "lang_desc": "Scegli la lingua per E-Bot e l'app:",
    },
    "İspanyolca 🇪🇸": {
        "settings": "⚙️ Ajustes",
        "back_to_chat": "⬅️ Volver al chat",
        "back_to_settings": "⬅️ Volver a ajustes",
        "theme_menu": "🎨 Temas de color",
        "lang_menu": "🌍 Idiomas",
        "chat_placeholder": "Escribe algo a E-Bot...",
        "settings_title": "⚙️ Ajustes",
        "settings_desc": (
            "Gestiona la apariencia de la aplicación y las preferencias de"
            " idioma aquí."
        ),
        "themes_title": "🎨 Temas de color",
        "themes_desc": "Elige el color del tema:",
        "lang_title": "🌍 Selección de idioma",
        "lang_desc": "Elige el idioma para E-Bot y la aplicación:",
    },
    "Rusça 🇷🇺": {
        "settings": "⚙️ Настройки",
        "back_to_chat": "⬅️ Назад к чату",
        "back_to_settings": "⬅️ Назад к настройкам",
        "theme_menu": "🎨 Цветовые темы",
        "lang_menu": "🌍 Языки",
        "chat_placeholder": "Напишите что-нибудь E-Bot...",
        "settings_title": "⚙️ Настройки",
        "settings_desc": (
            "Здесь вы можете управлять внешним видом приложения и языком."
        ),
        "themes_title": "🎨 Цветовые темы",
        "themes_desc": "Выберите цвет темы приложения:",
        "lang_title": "🌍 Выбор языка",
        "lang_desc": "Выберите язык для E-Bot и приложения:",
    },
    "Arapça 🇸🇦": {
        "settings": "⚙️ الإعدادات",
        "back_to_chat": "⬅️ العودة إلى الدردشة",
        "back_to_settings": "⬅️ العودة إلى الإعدادات",
        "theme_menu": "🎨 سمات الألوان",
        "lang_menu": "🌍 اللغات",
        "chat_placeholder": "اكتب شيئًا لـ E-Bot...",
        "settings_title": "⚙️ الإعدادات",
        "settings_desc": "إدارة مظهر التطبيق وتفضيلات اللغة من هنا.",
        "themes_title": "🎨 سمات الألوان",
        "themes_desc": "اختر لون سمة التطبيق:",
        "lang_title": "🌍 اختيار اللغة",
        "lang_desc": "اختر لغة E-Bot والتطبيق:",
    },
    "Çince 🇨🇳": {
        "settings": "⚙️ 设置",
        "back_to_chat": "⬅️ 返回聊天",
        "back_to_settings": "⬅️ 返回设置",
        "theme_menu": "🎨 颜色主题",
        "lang_menu": "🌍 语言",
        "chat_placeholder": "给 E-Bot 发送消息...",
        "settings_title": "⚙️ 设置",
        "settings_desc": "在此管理应用外观和语言首选项。",
        "themes_title": "🎨 颜色主题",
        "themes_desc": "选择应用主题颜色：",
        "lang_title": "🌍 语言选择",
        "lang_desc": "选择 E-Bot 和应用语言：",
    },
}

t = translations.get(st.session_state.language, translations["Türkçe 🇹🇷"])

# --- 3. RENK PALETLERİ VE TEMA STİLLERİ ---
theme_styles = {
    "Koyu Mod": {
        "bg": "#0e1117",
        "text": "#ffffff",
        "card": "#1e2129",
        "btn_bg": "#262730",
        "btn_txt": "#ffffff",
        "accent": "linear-gradient(135deg, #6366f1, #a855f7)",
    },
    "Açık Mod": {
        "bg": "#ffffff",
        "text": "#111111",
        "card": "#f0f2f6",
        "btn_bg": "#e2e8f0",
        "btn_txt": "#111111",
        "accent": "linear-gradient(135deg, #3b82f6, #1d4ed8)",
    },
    "Neon Mor": {
        "bg": "#090514",
        "text": "#f3e8ff",
        "card": "#170f2b",
        "btn_bg": "#241542",
        "btn_txt": "#f3e8ff",
        "accent": "linear-gradient(135deg, #a855f7, #ec4899)",
    },
    "Okyanus Mavisi": {
        "bg": "#030712",
        "text": "#e0f2fe",
        "card": "#0c192c",
        "btn_bg": "#132744",
        "btn_txt": "#e0f2fe",
        "accent": "linear-gradient(135deg, #0ea5e9, #2563eb)",
    },
    "Gün Batımı": {
        "bg": "#180808",
        "text": "#ffedea",
        "card": "#2d1212",
        "btn_bg": "#421a1a",
        "btn_txt": "#ffedea",
        "accent": "linear-gradient(135deg, #f97316, #db2777)",
    },
    "Zümrüt Yeşili": {
        "bg": "#02150a",
        "text": "#ecfdf5",
        "card": "#062814",
        "btn_bg": "#0d3b1f",
        "btn_txt": "#ecfdf5",
        "accent": "linear-gradient(135deg, #10b981, #059669)",
    },
}

current_theme = theme_styles.get(
    st.session_state.theme, theme_styles["Koyu Mod"]
)

# --- 4. GELİŞMİŞ CSS ENJEKSİYONU ---
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {current_theme['bg']} !important;
        color: {current_theme['text']} !important;
    }}
    
    h1, h2, h3, h4, h5, h6, p, span, label, div {{
        color: {current_theme['text']} !important;
    }}
    
    /* Butonların okunaklı ve tema uyumlu olması */
    .stButton>button {{
        background-color: {current_theme['btn_bg']} !important;
        color: {current_theme['btn_txt']} !important;
        border: 1px solid rgba(128, 128, 128, 0.3) !important;
        border-radius: 8px !important;
        width: 100% !important;
    }}
    .stButton>button:hover {{
        border-color: #6366f1 !important;
        color: {current_theme['btn_txt']} !important;
    }}
    
    header {{ visibility: hidden !important; }}
    footer {{ visibility: hidden !important; }}
    #MainMenu {{ visibility: hidden !important; }}
    
    input, textarea, [data-baseweb="base-input"] {{
        font-size: 16px !important;
        background-color: {current_theme['card']} !important;
        color: {current_theme['text']} !important;
    }}
    
    [data-testid="stChatMessageAvatar"], 
    [data-testid="stChatMessageAvatarUser"], 
    [data-testid="stChatMessageAvatarAssistant"] {{
        display: none !important;
    }}
    
    .custom-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(128, 128, 128, 0.2);
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

# --- 5. SAYFA 1: ANA SOHBET EKRANI ---
if st.session_state.page == "chat":
  col1, col2 = st.columns([5, 2])
  with col1:
    st.markdown(
        f"""
        <div class="custom-header" style="border:none; margin-bottom:0px; padding-bottom:0px;">
            <div class="header-left">
                <div class="custom-logo">⚡</div>
                <h2 class="custom-title" style="font-size:20px;">E-Bot Asistan</h2>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
  with col2:
    if st.button(t["settings"], use_container_width=True):
      st.session_state.page = "settings"
      st.rerun()

  st.markdown(
      "<hr style='margin-top:5px; margin-bottom:20px;"
      " border-color:rgba(128,128,128,0.2);'>",
      unsafe_allow_html=True,
  )

  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  if prompt := st.chat_input(t["chat_placeholder"]):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
      st.markdown(prompt)

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

# --- 6. SAYFA 2: AYARLAR MENÜSÜ ---
elif st.session_state.page == "settings":
  st.title(t["settings_title"])
  st.write(t["settings_desc"])
  st.write("")

  if st.button(t["theme_menu"], use_container_width=True):
    st.session_state.page = "themes"
    st.rerun()

  if st.button(t["lang_menu"], use_container_width=True):
    st.session_state.page = "languages"
    st.rerun()

  st.write("")
  if st.button(t["back_to_chat"], use_container_width=True):
    st.session_state.page = "chat"
    st.rerun()

# --- 7. SAYFA 3: RENK MODLARI SAYFASI ---
elif st.session_state.page == "themes":
  st.title(t["themes_title"])
  st.write(t["themes_desc"])
  st.write("")

  themes_list = [
      "Koyu Mod",
      "Açık Mod",
      "Neon Mor",
      "Okyanus Mavisi",
      "Gün Batımı",
      "Zümrüt Yeşili",
  ]
  for thm in themes_list:
    if st.button(
        f"{'✅ ' if st.session_state.theme == thm else ''}{thm}",
        use_container_width=True,
    ):
      st.session_state.theme = thm
      st.rerun()

  st.write("")
  if st.button(t["back_to_settings"], use_container_width=True):
    st.session_state.page = "settings"
    st.rerun()

# --- 8. SAYFA 4: DİLLER SAYFASI ---
elif st.session_state.page == "languages":
  st.title(t["lang_title"])
  st.write(t["lang_desc"])
  st.write("")

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
  if st.button(t["back_to_settings"], use_container_width=True):
    st.session_state.page = "settings"
    st.rerun()
