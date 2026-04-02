import streamlit as st
from groq import Groq

client = Groq(api_key="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")

st.set_page_config(page_title="Ahmad Assistant", page_icon="🤖")

st.title("🤖 Ahmad Assistant")
st.write("مساعدك الذكي للبرمجة والذكاء الاصطناعي")

if "conversation" not in st.session_state:
    st.session_state.conversation = [
        {
            "role": "system",
            "content": """أنت مساعد ذكي اسمك Ahmad Assistant.
تتحدث بالعربية دائماً بأسلوب ودي ومحفز.
تساعد في البرمجة والذكاء الاصطناعي.
تؤمن أن أي شخص يمكنه تعلم البرمجة."""
        }
    ]

for msg in st.session_state.conversation[1:]:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

user_input = st.chat_input("اكتب سؤالك هنا...")

if user_input:
    st.session_state.conversation.append({
        "role": "user",
        "content": user_input
    })
    st.chat_message("user").write(user_input)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=st.session_state.conversation
    )

    reply = response.choices[0].message.content
    st.session_state.conversation.append({
        "role": "assistant",
        "content": reply
    })
    st.chat_message("assistant").write(reply)
```
