import streamlit as st
import pdfplumber
import docx2txt
from transformers import pipeline
import uuid
import pyperclip as pp

st.title('CliffNotes AI')

html_temp = """ 
    <div style ="background-color:yellow;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Text Summarization GEN-AI Application </h1> 
    </div> 
    """
st.markdown(html_temp, unsafe_allow_html=True)

@st.cache_resource
def load_model():
    model = "Azma-AI/bart-large-text-summarizer"
    summarizer = pipeline("summarization", model=model)
    return summarizer

summarizer = load_model()

if "sessions" not in st.session_state:
    st.session_state.sessions = {}

if "current_session" not in st.session_state:
    st.session_state.current_session = None

if "latest_summary" not in st.session_state:
    st.session_state.latest_summary = ""

def create_new_session(session_name="New Session"):
    session_id = str(uuid.uuid4())
    st.session_state.sessions[session_id] = {
        "name": session_name,
        "messages": [],
        "file_content": ""
    }
    st.session_state.current_session = session_id

def switch_session(session_id):
    st.session_state.current_session = session_id  

def rename_session(session_id, new_name):
    st.session_state.sessions[session_id]["name"] = new_name

def clear_session_state():
    st.session_state.sessions = {}
    st.session_state.current_session = None
    st.session_state.latest_summary = ""
    st.experimental_rerun()

with st.sidebar:
    with open("style.css") as css:
        css = css.read()

    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    st.markdown('<h1 class="custom-header">CliffNotes AI</h1>', unsafe_allow_html=True)

    st.header('' , divider='rainbow')
    st.header("Sessions")
    for session_id, session_data in st.session_state.sessions.items():
        if st.button(session_data["name"], key=session_id):
            switch_session(session_id)
    
    if st.button("New Session"):
        create_new_session()
    
    if st.session_state.current_session:
        current_name = st.session_state.sessions[st.session_state.current_session]["name"]
        new_name = st.text_input("Rename Session", current_name)
        if new_name != current_name:
            rename_session(st.session_state.current_session, new_name)
    
    if st.button("Clear All Sessions"):
        clear_session_state()

if st.session_state.current_session:
    session = st.session_state.sessions[st.session_state.current_session]

    for message in session["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What's Crackin'"):
        with st.chat_message("User"):
            st.markdown(prompt)
        session["messages"].append({'role': 'user', 'content': prompt})
        # Summarize the prompt immediately
        summary = summarizer(prompt, max_length=250, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary_text = summary[0]['summary_text']
        session["messages"].append({'role': 'assistant', 'content': summary_text})
        st.session_state.latest_summary = summary_text
        with st.chat_message("Assistant"):
            st.markdown(summary_text)

    def file_upload():
        uploaded_file = st.file_uploader('Upload a text file', type=['txt', 'docx', 'pdf'])
        if uploaded_file is not None:
            if uploaded_file.type == 'text/plain':
                text_content = uploaded_file.read().decode('utf-8')
            elif uploaded_file.type == 'application/pdf':
                with pdfplumber.open(uploaded_file) as pdf:
                    text_content = ""
                    for page in pdf.pages:
                        text_content += page.extract_text()
            elif uploaded_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                text_content = docx2txt.process(uploaded_file)
            else:
                text_content = "Unsupported file type."
            
            session["file_content"] = text_content
            st.write(text_content)

            summary = summarizer(text_content, max_length=250, min_length=60, length_penalty=2.0, num_beams=4, early_stopping=True)
            summary_text = summary[0]['summary_text']
            session["messages"].append({'role': 'assistant', 'content': summary_text})
            st.session_state.latest_summary = summary_text
            with st.chat_message("Assistant"):
                st.markdown(summary_text)
            
    file_upload()

    if st.button("Copy"):
        if st.session_state.latest_summary:
            pp.copy(st.session_state.latest_summary)
            st.success('Text Copied to Clipboard')
        else:
            st.error('No summary available to copy')
else:
    st.write('No session selected. Create or select a session from the sidebar')
