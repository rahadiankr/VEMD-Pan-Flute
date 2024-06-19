import streamlit as st
import assets.languages_data as language
from assets.default_notes import ready_note, stop_note
from send_data import sending_data

from streamlit_theme import st_theme
theme = st_theme()

if 'stop' and 'ready' not in st.session_state:
    st.session_state['stop'] = False
    st.session_state['ready'] = False

if 'lang_state' not in st.session_state:
    st.session_state['lang_state'] = 0

def select_language():
    lang_list = ['English', 'Indonesia']
    lang_option = st.selectbox(language.languages[st.session_state.lang_state]['select_lang'], lang_list, index=st.session_state.lang_state)
    if st.session_state['lang_state'] != lang_list.index(lang_option):
        st.session_state['lang_state'] = lang_list.index(lang_option)
        st.rerun()

with st.container():
    with st.columns(3)[1]:
        if theme:
            if theme['base'] == 'dark':
                st.image("assets/images/logo.png", width=300)
            else:
                st.image("assets/images/logo-dark.png", width=300)
    col1, col2 = st.columns(2)
    with col1:
        with st.container():
            if st.button(language.languages[st.session_state.lang_state]['button_ready'], use_container_width=True):
                st.session_state['ready'] = True
                sending_data.send_data_to_plc(ready_note)
    with col2:
        with st.container():
            if st.button(language.languages[st.session_state.lang_state]['button_stop'], use_container_width=True):
                st.session_state["stop"] = True
                sending_data.send_data_to_plc(stop_note)

with (st.sidebar):
    if theme:
        if theme['base'] == 'dark':
            st.image("assets/images/logo.png")
        else:
            st.image("assets/images/logo-dark.png")
    st.title("NAYANIKA")
    with st.container(height=200, border=False):
        st.page_link("main.py", label=language.languages[st.session_state.lang_state]['page_main'])
        st.page_link("pages/page_1.py", label=language.languages[st.session_state.lang_state]['page_1'], disabled=not st.session_state.ready)
        st.page_link("pages/page_2.py", label=language.languages[st.session_state.lang_state]['page_2'], disabled=not st.session_state.ready)
        st.page_link("pages/page_3.py", label=language.languages[st.session_state.lang_state]['page_3'], disabled=not st.session_state.ready)

    select_language()
