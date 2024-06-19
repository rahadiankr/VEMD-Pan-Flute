import os
from streamlit_theme import st_theme

import streamlit as st
from assets.default_notes import ready_note, stop_note
import assets.languages_data as language

from helper_function import fixing_duration, adjusting_notes
from send_data import sending_data

from basic_pitch import ICASSP_2022_MODEL_PATH
from basic_pitch.inference import Model, predict

model = Model(ICASSP_2022_MODEL_PATH)
theme = st_theme()


if 'stop' and 'play' not in st.session_state:
    st.session_state['stop'] = False
    st.session_state['play'] = False

if 'lang_state' not in st.session_state:
    st.session_state['lang_state'] = 0

def select_language():
    lang_list = ['English', 'Indonesia']
    lang_option = st.selectbox(language.languages[st.session_state.lang_state]['select_lang'], lang_list, index=st.session_state.lang_state)
    if st.session_state['lang_state'] != lang_list.index(lang_option):
        st.session_state['lang_state'] = lang_list.index(lang_option)
        st.rerun()

def load_music(audio):
    audio_path = "test/" + audio
    st.title(audio)
    st.audio(audio_path)
    return audio_path


# Function to simulate data loading
def load_list():
    # Simulate data loading delay
    st.write(language.languages[st.session_state.lang_state]['list_song'])
    with st.container(height=250):
        list_file = os.listdir("test/")
        selected_item = st.radio(language.languages[st.session_state.lang_state]['select_song'], list_file)
    if selected_item:
        audio = load_music(selected_item)
    return audio

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
        st.page_link("pages/page_3.py", label=language.languages[st.session_state.lang_state]['page_3'], disabled=True)
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

data_to_send = None
audio_path = load_list()
# st.write(st.session_state)
st.session_state['stop'] = False
st.session_state['play'] = False
if audio_path:
    option_nada_dasar = st.selectbox(language.languages[st.session_state.lang_state]['select_chord'], ("C", "D", "E", "F", "G", "A", "B"))
    st.write(language.languages[st.session_state.lang_state]['result_chord'], option_nada_dasar)
    if st.button(language.languages[st.session_state.lang_state]['button_play'], use_container_width=True):
        st.session_state['play'] = True

        dict_nada_dasar = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
        nada_dasar = dict_nada_dasar[option_nada_dasar]

        print("predict")
        model_output, midi_data, note_events = predict(f'{audio_path}', model)
        print("predict done")
        note_events = [(round(item[0], 4), round(item[1], 4), item[2], round(item[3] * 32767)) for item in note_events]
        confidence = [item for item in note_events if (item[1] - item[0] > 0.3)]
        confidence = sorted(confidence, key=lambda x: x[0])
        transposed = adjusting_notes.transpose_notes(confidence)
        base_note = [item for item in transposed if ((item[2] - nada_dasar <= 24 and item[2] - nada_dasar >= 0))]
        base_note = [(item[0], item[1], item[2] - nada_dasar, item[3]) for item in base_note]
        base_note = sorted(base_note, key=lambda x: x[0])
        # print("fixing duration")
        fix_duration = fixing_duration.non_negative(base_note)
        fix_duration = [(item[0], item[1], 1 if item[1] - item[0] <= 0 else item[2], item[3]) for item in fix_duration]

        print("send data")
        data_to_send = adjusting_notes.adjust_notes(fix_duration)
        st.table(data_to_send)
        # print(data_to_send)

        sending_data.send_data_to_plc(data_to_send)


print(st.session_state)
