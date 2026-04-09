import streamlit as st
from groq import Groq
import os

st.set_page_config(page_title="Ahmad Assistant", page_icon="🤖")

client = Groq(api_key=os.environ.get("GROQ_API_KEY", "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"))

# ═══ الشريط الجانبي ═══
with st.sidebar:
    st.title("⚙️ الإعدادات")
    
    personality = st.selectbox(
        "شخصية المساعد:",
        ["مساعد عام", "خبير برمجة", "معلم صبور"]
    )
    
    if st.button("🗑️ مسح المحادثة"):
        st.session_state.conversation = []
        st.rerun()
    
    if "conversation" in st.session_state:
        msg_count = len([m for m in st.session_state.conversation if m["role"] == "user"])
        st.metric("عدد رسائلك", msg_count)

# ═══ الشخصيات ═══
personalities = {
    "مساعد عام": "أنت مساعد ذكي اسمك Ahmad Assistant. تتحدث بالعربية دائماً بأسلوب ودي.",
    "خبير برمجة": "أنت خبير برمجة متخصص. تشرح الكود بالتفصيل وتعطي أمثلة عملية دائماً. تتحدث بالعربية.",
    "معلم صبور": "أنت معلم صبور ومحفز. تشرح الأفكار بطريقة بسيطة جداً. تشجع المتعلم دائماً. تتحدث بالعربية."
}

# ═══ تهيئة المحادثة ═══
if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "current_personality" not in st.session_state:
    st.session_state.current_personality = personality

if personality != st.session_state.current_personality:
    st.session_state.conversation = []
    st.session_state.current_personality = personality

# ═══ الواجهة الرئيسية ═══
st.title("🤖 Ahmad Assistant")
st.caption(f"الوضع الحالي: {personality}")

# عرض المحادثة
for msg in st.session_state.conversation:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# المدخل
user_input = st.chat_input("اكتب سؤالك هنا...")

if user_input:
    st.session_state.conversation.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)
    
    messages = [{"role": "system", "content": personalities[personality]}] + st.session_state.conversation
    
    with st.spinner("يفكر..."):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )
    
    reply = response.choices[0].message.content
    st.session_state.conversation.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
