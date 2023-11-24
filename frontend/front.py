import streamlit as st
import requests
import time
import pandas as pd

st.set_page_config(
    page_title="Next word prediction",page_icon=':person:',initial_sidebar_state="expanded"
)



  
with open('./frontend/style.css') as f:
    st.markdown(f'<style>{f.read()}/<style>', unsafe_allow_html=True)

with st.container():
    st.write("""# Next word prediction project """)
    st.write("""### Accuracy for the test data 86% """)
    st.write('---')

c1 = st.container()
c2 = st.container()


def test(next_word):
    if next_word:
        try:
            with st.spinner('Wait for it...'):
                time.sleep(1)
            r = requests.get(f'http://api:8080/{next_word}')
            data = r.json().get('next_word')
            with c2:
                st.write(""" ### The next word is : """)
                st.write(f"""{data}""")
        except Exception as e:
            st.error(e, icon="🚨")
    else:
        st.error('Please articles text', icon="🚨")

with c1:
    with st.form(key='Predict next word'):
        name = st.text_input(label="Text")
        submit_form = st.form_submit_button(label="Predict next word", help="Click to predict!", on_click=test(name))


