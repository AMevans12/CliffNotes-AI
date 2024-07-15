# CliffNotes AI: Text Summarization App

## Overview

CliffNotes AI is a Streamlit application designed for text summarization using transformer models. The app allows users to summarize text from direct inputs or uploaded files, providing an interactive and user-friendly interface. It also features session management and clipboard copying functionality for convenience.

## Features

- **Text Summarization:** Summarizes user input or uploaded text files (txt, docx, pdf) using the "Azma-AI/bart-large-text-summarizer" model.
- **Session Management:** Create, rename, switch, and clear sessions to organize different text summarization tasks.
- **Clipboard Copying:** Copy the latest summary to the clipboard with a single click.
- **Custom Styling:** Enhanced user interface with custom CSS styling.

## Files

- `gen.py`: Main Streamlit application file.
- `style.css`: Custom CSS for enhancing the app's user interface.

## Installation

To use the CliffNotes AI app, follow these steps:

1. **Clone the repository:**

    
    git clone https://github.com/AMevans12/Cliffnotes-AI.git
    cd Cliffnotes-AI
    

2. **Install the required dependencies:**

    
    pip install -r requirements.txt
    

## Usage

To run the application, use the following command:


streamlit run app.py


### Application Interface

- **Title and Header:**
   
    st.title('CliffNotes AI')

    html_temp = """ 
        <div style ="background-color:yellow;padding:13px"> 
        <h1 style ="color:black;text-align:center;">Text Summarization GEN-AI Application </h1> 
        </div> 
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    

- **Sidebar and Sessions:**
  
    with st.sidebar:
        with open("style.css") as css:
            css = css.read()
        st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
        st.markdown('<h1 class="custom-header">CliffNotes AI</h1>', unsafe_allow_html=True)
        st.header('' , divider='rainbow')
        st.header("Sessions")
        ...
    

### Summarizing Text

- **Direct Input:**
    
    if prompt := st.chat_input("What's Crackin'"):
        ...
        summary = summarizer(prompt, max_length=250, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary_text = summary[0]['summary_text']
        ...
  

- **File Upload:**
    def file_upload():
        uploaded_file = st.file_uploader('Upload a text file', type=['txt', 'docx', 'pdf'])
        ...
        summary = summarizer(text_content, max_length=250, min_length=60, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary_text = summary[0]['summary_text']
        ...
    

### Copying to Clipboard

- **Copy Button:**
    if st.button("Copy"):
        if st.session_state.latest_summary:
            pp.copy(st.session_state.latest_summary)
            st.success('Text Copied to Clipboard')
        else:
            st.error('No summary available to copy')
    


## Contact

For any questions or feedback, please reach out to me via [GitHub](https://github.com/AMevans12).

---

**Effortlessly summarize your text with CliffNotes AI!**
