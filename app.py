import streamlit as st
import anthropic
import pymupdf
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

st.title("📄 Document Chatbot")

# File uploader
uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf"])

document_text = ""
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        pdf = pymupdf.open(stream=uploaded_file.read(), filetype="pdf")
        for page in pdf:
            document_text += page.get_text()
    else:
        document_text = uploaded_file.read().decode("utf-8")
    st.success("Document loaded! Ask me anything about it.")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if prompt := st.chat_input("Ask a question about your document..."):
    if not document_text:
        st.warning("Please upload a document first.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
system="You are a friendly and knowledgeable assistant. Use the document below as your primary source of information. When answering, explain things clearly in simple language, give context and background where helpful, suggest next steps or related things the user should know, if something is complex break it down step by step, be conversational and engaging not robotic, and if the document does not cover something use your general knowledge to help.\n\nDOCUMENT:\n" + document_text,            
messages=st.session_state.messages
        )

        answer = response.content[0].text
        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.write(answer)