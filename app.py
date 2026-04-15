import streamlit as st
from BLABLABLA import app, init_db, save_message, CLINIC_CONFIG

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title=f"PawPal — {CLINIC_CONFIG['name']}",
    page_icon="🐾",
    layout="centered"
)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Quicksand:wght@500;600;700&display=swap');

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

.stApp {
    background: linear-gradient(160deg, #f0faf4 0%, #e8f4fd 50%, #fef6ee 100%);
    min-height: 100vh;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Header card ── */
.pawpal-header {
    background: linear-gradient(135deg, #2d9e6b 0%, #1a7a8a 60%, #2563a8 100%);
    border-radius: 20px;
    padding: 24px 28px;
    margin-bottom: 8px;
    box-shadow: 0 8px 32px rgba(45,158,107,0.25);
    display: flex;
    align-items: center;
    gap: 16px;
}

.pawpal-logo {
    font-size: 3rem;
    line-height: 1;
}

.pawpal-title {
    color: white;
    font-family: 'Quicksand', sans-serif;
    font-size: 1.75rem;
    font-weight: 700;
    margin: 0;
    line-height: 1.2;
}

.pawpal-subtitle {
    color: rgba(255,255,255,0.85);
    font-size: 0.85rem;
    font-weight: 500;
    margin: 2px 0 0 0;
}

/* ── Status badges ── */
.badge-row {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 16px;
}

.badge {
    background: white;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.75rem;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.badge-green { color: #2d9e6b; border: 1.5px solid #b7e8d1; }
.badge-blue  { color: #2563a8; border: 1.5px solid #bdd5f5; }
.badge-orange{ color: #d97706; border: 1.5px solid #fcd9a0; }

/* ── Chat container ── */
.chat-wrapper {
    background: white;
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.07);
    margin-bottom: 8px;
    min-height: 420px;
}

/* ── Message bubbles ── */
[data-testid="stChatMessage"] {
    border-radius: 16px !important;
    margin-bottom: 4px !important;
}

/* User bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg, #e8f5ff, #dbeeff) !important;
    border: 1px solid #c3deff !important;
}

/* Assistant bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: linear-gradient(135deg, #f0faf6, #e6f7f0) !important;
    border: 1px solid #b7e8d1 !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    border-radius: 16px !important;
    border: 2px solid #b7e8d1 !important;
    background: white !important;
    font-family: 'Nunito', sans-serif !important;
    box-shadow: 0 4px 16px rgba(45,158,107,0.12) !important;
}

[data-testid="stChatInput"]:focus-within {
    border-color: #2d9e6b !important;
    box-shadow: 0 4px 20px rgba(45,158,107,0.22) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a3a2e 0%, #1a2e3a 100%) !important;
}

[data-testid="stSidebar"] * {
    color: #e8f5f0 !important;
}

[data-testid="stSidebar"] .stTextInput input {
    background: rgba(255,255,255,0.1) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    color: white !important;
    border-radius: 10px !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #7fe8b8 !important;
    font-family: 'Quicksand', sans-serif !important;
}

/* ── Clinic info card in sidebar ── */
.clinic-card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 12px;
    padding: 14px;
    margin-top: 8px;
    font-size: 0.82rem;
    line-height: 1.7;
}

.clinic-card a {
    color: #7fe8b8 !important;
    text-decoration: none;
}

/* ── Emergency banner ── */
.emergency-banner {
    background: linear-gradient(135deg, #fff1f1, #ffe4e4);
    border: 2px solid #fca5a5;
    border-radius: 14px;
    padding: 12px 16px;
    margin-bottom: 12px;
    font-size: 0.82rem;
    color: #c0392b;
    font-weight: 700;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: #2d9e6b !important;
}

/* ── Welcome message ── */
.welcome-box {
    text-align: center;
    padding: 40px 20px;
    color: #5a7a6a;
}

.welcome-box .paw-big {
    font-size: 3.5rem;
    margin-bottom: 12px;
}

.welcome-box h3 {
    font-family: 'Quicksand', sans-serif;
    font-weight: 700;
    color: #2d9e6b;
    margin-bottom: 6px;
}

.welcome-box p {
    font-size: 0.9rem;
    color: #6b8f7a;
    max-width: 320px;
    margin: 0 auto;
}
</style>
""", unsafe_allow_html=True)

# ── Init ─────────────────────────────────────────────────────
init_db()

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🐾 PawPal")
    st.markdown(f"### {CLINIC_CONFIG['name']}")
    st.divider()

    st.markdown("**Session**")
    thread_id = st.text_input(
        "Session ID",
        value="default",
        label_visibility="collapsed",
        placeholder="Enter session name..."
    )
    st.caption("Same name = PawPal remembers you. New name = fresh start.")

    st.divider()
    st.markdown("**📍 Clinic Info**")
    st.markdown(f"""
<div class="clinic-card">
📍 {CLINIC_CONFIG['city_state']}<br>
📞 {CLINIC_CONFIG['phone']}<br>
✉️ {CLINIC_CONFIG['email']}<br>
🕐 {CLINIC_CONFIG['hours']}<br><br>
<a href="{CLINIC_CONFIG['booking_link']}" target="_blank">📅 Book Appointment →</a>
</div>
""", unsafe_allow_html=True)

    st.divider()
    st.markdown("**We See:**")
    st.markdown("🐕 Dogs &nbsp; 🐈 Cats &nbsp; 🐇 Rabbits")
    st.markdown("🦎 Reptiles &nbsp; 🐦 Birds &nbsp; 🐹 Exotics")

    st.divider()
    st.caption("Powered by LangGraph + Groq LLaMA 3.3")

# ── Session state ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_thread" not in st.session_state:
    st.session_state.last_thread = thread_id

if thread_id != st.session_state.last_thread:
    st.session_state.messages = []
    st.session_state.last_thread = thread_id
# ── Trial limit ──
if "message_count" not in st.session_state:
    st.session_state.message_count = 0

TRIAL_LIMIT = 20
# ── Header ────────────────────────────────────────────────────
st.markdown(f"""
<div class="pawpal-header">
    <div class="pawpal-logo">🐾</div>
    <div>
        <p class="pawpal-title">PawPal</p>
        <p class="pawpal-subtitle">{CLINIC_CONFIG['name']} · Virtual Assistant</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Badges ───────────────────────────────────────────────────
st.markdown("""
<div class="badge-row">
    <span class="badge badge-green">🟢 Online 24/7</span>
    <span class="badge badge-blue">🔍 Web Search Enabled</span>
    <span class="badge badge-orange">🦎 Exotic Pet Specialist</span>
    <span class="badge badge-green">🧠 Memory Enabled</span>
</div>
""", unsafe_allow_html=True)

# ── Emergency banner ─────────────────────────────────────────
st.markdown(f"""
<div class="emergency-banner">
    🚨 <strong>Emergency?</strong> Call immediately: {CLINIC_CONFIG['phone']} 
    &nbsp;|&nbsp; For after-hours emergencies, go to your nearest 24-hour animal hospital.
</div>
""", unsafe_allow_html=True)
if st.session_state.message_count < TRIAL_LIMIT:
    remaining = TRIAL_LIMIT - st.session_state.message_count
    st.markdown(f"""
    <div style="text-align:right; margin-bottom: 8px;">
        <span style="
            background: white;
            border: 1.5px solid #b7e8d1;
            border-radius: 20px;
            padding: 4px 14px;
            font-size: 0.78rem;
            font-weight: 700;
            color: #2d9e6b;
        ">
            💬 {remaining} free messages remaining
        </span>
    </div>
    """, unsafe_allow_html=True)

# ── Chat messages ─────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
<div class="welcome-box">
    <div class="paw-big">🐾</div>
    <h3>Hi! I'm PawPal 💛</h3>
    <p>I'm here to help with any questions about your pet — 
    from dogs and cats to exotic companions. Ask me anything!</p>
</div>
""", unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="🐾" if msg["role"] == "assistant" else "👤"):
            st.markdown(msg["content"])

# ── Chat input ────────────────────────────────────────────────
# ── Trial wall ──
if st.session_state.message_count >= TRIAL_LIMIT:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1a3a2e, #1a2e3a);
        border-radius: 20px;
        padding: 32px;
        text-align: center;
        color: white;
        margin-top: 20px;
    ">
        <div style="font-size: 2.5rem;">🐾</div>
        <h2 style="color: #7fe8b8; font-family: Quicksand;">
            You've used your free preview!
        </h2>
        <p style="color: rgba(255,255,255,0.8); font-size: 0.95rem;">
            PawPal has answered your 20 free questions.<br>
            Start your 14-day free trial to unlock unlimited access.
        </p>
        <div style="
            background: #2d9e6b;
            color: white;
            padding: 14px 32px;
            border-radius: 50px;
            font-weight: 700;
            font-size: 1rem;
            display: inline-block;
            margin-top: 16px;
            cursor: pointer;
        ">
            🚀 Start Free 14-Day Trial — $199/month after
        </div>
        <p style="
            color: rgba(255,255,255,0.5);
            font-size: 0.75rem;
            margin-top: 12px;
        ">
            Cancel anytime. No contracts. Setup included.
        </p>
        <p style="
            color: rgba(255,255,255,0.6);
            font-size: 0.8rem;
            margin-top: 8px;
        ">
            Questions? Email us: yourname@gmail.com
        </p>
    </div>
    """, unsafe_allow_html=True)

else:
    # ── Normal chat input ──
    user_input = st.chat_input(
        f"Ask about your pet... ({TRIAL_LIMIT - st.session_state.message_count} free messages remaining)"
    )

    if user_input:
        st.session_state.message_count += 1
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)

        save_message(thread_id, "user", user_input)

        config = {"configurable": {"thread_id": thread_id}}

with st.chat_message("assistant", avatar="🐾"):
        with st.spinner("PawPal is thinking..."):
            try:
                result = app.invoke(
                    {"messages": [("human", user_input)]},
                    config=config
                )
                response = result["messages"][-1].content
            except Exception as e:
                response = "Sorry, I'm having trouble right now. Please try again!"
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    save_message(thread_id, "agent", response)
        
        save_message(thread_id, "agent", response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    save_message(thread_id, "agent", response)
