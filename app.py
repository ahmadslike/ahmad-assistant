import streamlit as st
import anthropic
import os

st.set_page_config(page_title="Ahmad Assistant", page_icon="🤖")

client = anthropic.Anthropic(api_key="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")
if not api_key:
    st.error("لم يتم العثور على API Key")
    st.stop()
client = anthropic.Anthropic(api_key=api_key.strip())

# ═══ الشخصيات ═══
personalities = {
    "مساعد عام": "أنت مساعد ذكي اسمك Ahmad Assistant. تتحدث بالعربية دائماً بأسلوب ودي ومحفز.",
    "خبير برمجة": "أنت خبير برمجة متخصص. تشرح الكود بالتفصيل وتعطي أمثلة عملية دائماً. تتحدث بالعربية.",
    "معلم صبور": "أنت معلم صبور ومحفز. تشرح الأفكار بطريقة بسيطة جداً. تشجع المتعلم دائماً. تتحدث بالعربية."
}

length_instruction = {
    "قصير": "أجب بإيجاز شديد — جملة أو جملتان فقط.",
    "متوسط": "أجب بشكل معقول — لا طويل جداً ولا قصير جداً.",
    "مفصّل": "أجب بالتفصيل الكامل مع أمثلة."
}

# ═══ الشريط الجانبي ═══
with st.sidebar:
    st.title("⚙️ الإعدادات")

    personality = st.selectbox(
        "شخصية المساعد:",
        ["مساعد عام", "خبير برمجة", "معلم صبور"]
    )

    max_length = st.select_slider(
        "طول الرد:",
        options=["قصير", "متوسط", "مفصّل"],
        value="متوسط"
    )

    st.divider()

    if st.button("🗑️ مسح المحادثة"):
        st.session_state.conversation = []
        st.session_state.current_personality = personality
        st.rerun()

    if "conversation" in st.session_state:
        msg_count = len([m for m in st.session_state.conversation if m["role"] == "user"])
        st.metric("عدد رسائلك", msg_count)
        
    if st.session_state.conversation:
        chat_text = ""
        for msg in st.session_state.conversation:
            role = "أنت" if msg["role"] == "user" else "المساعد"
            chat_text += f"{role}: {msg['content']}\n\n"
        
        st.download_button(
            label="💾 تحميل المحادثة",
            data=chat_text,
            file_name="محادثة.txt",
            mime="text/plain"
        )

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
st.caption(f"الوضع الحالي: {personality} — رد {max_length}")

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

    system_content = personalities[personality] + " " + length_instruction[max_length]
    messages = [{"role": "system", "content": system_content}] + st.session_state.conversation

    with st.spinner("يفكر..."):
        response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    messages=[m for m in messages if m["role"] != "system"],
    system=next((m["content"] for m in messages if m["role"] == "system"), "")
)
reply = response.content[0].text
    st.session_state.conversation.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
