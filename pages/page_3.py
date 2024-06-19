import streamlit as st
import streamlit.components.v1 as components
from streamlit_theme import st_theme
from send_data import sending_data
import assets.languages_data as language
from assets.default_notes import ready_note, stop_note

theme = st_theme()

if 'lang_state' not in st.session_state:
    st.session_state['lang_state'] = 0

if 'lang_state' not in st.session_state:
    st.session_state['lang_state'] = 0

def select_language():
    lang_list = ['English', 'Indonesia']
    lang_option = st.selectbox(language.languages[st.session_state.lang_state]['select_lang'], lang_list, index=st.session_state.lang_state)
    if st.session_state['lang_state'] != lang_list.index(lang_option):
        st.session_state['lang_state'] = lang_list.index(lang_option)
        st.rerun()

with st.sidebar:
    if theme:
        if theme['base'] == 'dark':
            st.image("assets/images/logo.png")
        else:
            st.image("assets/images/logo-dark.png")
    st.title("NAYANIKA")
    with st.container(height=200, border=False):
        st.page_link("main.py", label=language.languages[st.session_state.lang_state]['page_main'])
        st.page_link("pages/page_1.py", label=language.languages[st.session_state.lang_state]['page_1'])
        st.page_link("pages/page_2.py", label=language.languages[st.session_state.lang_state]['page_2'])
        st.page_link("pages/page_3.py", label=language.languages[st.session_state.lang_state]['page_3'])
    col1, col2 = st.columns(2)
    with col1:
        with st.container():
            if st.button(language.languages[st.session_state.lang_state]['button_reset'], use_container_width=True):
                data_to_send = []
                closed = True
                if closed:
                    sending_data.send_data_to_plc(ready_note)
                    st.toast(language.languages[st.session_state.lang_state]['toast_reset'])
    with col2:
        with st.container():
            if st.button(language.languages[st.session_state.lang_state]['button_stop'], use_container_width=True):
                st.session_state["stop"] = True
                print(st.session_state)
                sending_data.send_data_to_plc(stop_note)
                st.toast(language.languages[st.session_state.lang_state]['toast_stop'])
    with st.container():
        if st.button(language.languages[st.session_state.lang_state]['button_force'], use_container_width=True):
            st.warning(language.languages[st.session_state.lang_state]['toast_force'])
            st.stop()

    select_language()

# Define JavaScript for audio recording
audio_recorder_html = """
<script>
  let mediaRecorder;
  let audioChunks = [];

  function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(stream => {
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();

        mediaRecorder.addEventListener("dataavailable", event => {
          audioChunks.push(event.data);
        });

        mediaRecorder.addEventListener("stop", () => {
          const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
          const audioUrl = URL.createObjectURL(audioBlob);
          const audio = new Audio(audioUrl);
          const playButton = document.createElement("button");
          playButton.innerText = "Play Recording";
          playButton.onclick = () => audio.play();
          document.body.appendChild(playButton);

          const downloadLink = document.createElement("a");
          downloadLink.href = audioUrl;
          downloadLink.download = "recording.wav";
          downloadLink.innerText = "Download Recording";
          document.body.appendChild(downloadLink);

          // Create a form and submit the audioBlob as a file
          const formData = new FormData();
          formData.append('audio', audioBlob, 'recording.wav');
          fetch('/upload', {
            method: 'POST',
            body: formData
          });
        });

        audioChunks = [];
      });
  }

  function stopRecording() {
    mediaRecorder.stop();
  }

  function triggerRecording(action) {
    if (action === 'start') {
      startRecording();
    } else if (action === 'stop') {
      stopRecording();
    }
  }
</script>
<button onclick="startRecording()">Start Recording</button>
<button onclick="stopRecording()">Stop Recording</button>
"""

# Embed the JavaScript into Streamlit
components.html(audio_recorder_html)

# Create buttons in Streamlit
if st.button(language.languages[st.session_state.lang_state]['button_start_rec']):
    components.html("<script>triggerRecording('start');</script>")

if st.button(language.languages[st.session_state.lang_state]['button_stop_rec']):
    components.html("<script>triggerRecording('stop');</script>")
