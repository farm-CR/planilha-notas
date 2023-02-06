import streamlit as st
import numpy as np
import pandas as pd
import json
import os.path

st.set_page_config(page_title='Notas', layout='wide')

def run():

    if os.path.isfile("data.json")  == False:
        reset_default()

    materia = st.sidebar.selectbox(
        'Escolha a matéria',
        json.loads(open("data.json").read()).keys())

    st.sidebar.button("Reset to default", on_click= reset_default)
    ask(materia)

def reset_default():
    data = json.loads(open("preset_5ECO.json").read())

    for materia in data.keys():
        for avaliacao in data[materia].keys():
            data[materia][avaliacao]["Notas"] = list(np.zeros(data[materia][avaliacao]["Campos"]))
    json.dump(data, open('data.json', 'w'))

def clean_input(text):
    if text == "":
        text = 0
    else:
        text = float(text.replace(",", "."))
        if text > 10 or text < 0:
            text = np.nan
    return text

def ask(materia):
    data = json.loads(open("data.json").read())

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("# Quizes")
        for campo in range(data[materia]["Quiz"]["Campos"]):
            data[materia]["Quiz"]["Notas"][campo] = (
                clean_input(
                    st.text_input(f"Quiz {campo+1}", 
                        data[materia]["Quiz"]["Notas"][campo], 
                        key = f"Quiz{campo+1}_{materia}")))
        st.write(eval(data[materia]["Quiz"]["Conta"])(data[materia]["Quiz"]["Notas"]))
        
    with col2:
        st.markdown("# Quizes")
        for campo in range(data[materia]["APS"]["Campos"]):
            data[materia]["APS"]["Notas"][campo] = (
                clean_input(
                    st.text_input(f"APS {campo+1}", 
                        data[materia]["APS"]["Notas"][campo], 
                        key = f"APS{campo+1}_{materia}")))
        st.write(eval(data[materia]["APS"]["Conta"])(data[materia]["APS"]["Notas"]))

    with col3:
        st.markdown("# Provas")
        for campo in range(data[materia]["PI"]["Campos"]):
            data[materia]["PI"]["Notas"][campo] = (
                clean_input(
                    st.text_input(f"PI", 
                        data[materia]["PI"]["Notas"][campo], 
                        key = f"PI{campo+1}_{materia}")))
        for campo in range(data[materia]["PF"]["Campos"]):
            data[materia]["PF"]["Notas"][campo] = (
                clean_input(
                    st.text_input(f"PF", 
                        data[materia]["PF"]["Notas"][campo], 
                        key = f"PF{campo+1}_{materia}")))
    
    data[materia]["Media"] = (
        eval(data[materia]["Quiz"]["Conta"])(data[materia]["Quiz"]["Notas"]) * data[materia]["Quiz"]["Peso"] +
        eval(data[materia]["APS"]["Conta"])(data[materia]["APS"]["Notas"]) * data[materia]["APS"]["Peso"] +
        eval(data[materia]["PI"]["Conta"])(data[materia]["PI"]["Notas"]) * data[materia]["PI"]["Peso"] +
        eval(data[materia]["PF"]["Conta"])(data[materia]["PF"]["Notas"]) * data[materia]["PF"]["Peso"]
    )
    
    json.dump(data, open('data.json', 'w'))

    st.write(data)

run()