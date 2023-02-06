import streamlit as st
import numpy as np
import pandas as pd
import json
import os

st.set_page_config(page_title='Notas', layout='wide')

def run():

    if os.path.isfile("data.json")  == False:
        reset_default()

    materia = st.sidebar.selectbox(
        'Escolha a matéria',
        json.loads(open("data.json").read()).keys())

    st.sidebar.button("Reset file", on_click= reset_default)
    ask(materia)

def reset_default(create = True):

    os.remove("data.json")

    if create:
        data = json.loads(open("preset_4ECO.json").read())

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

def create_input(data, materia, avaliacao):
    for campo in range(data[materia][avaliacao]["Campos"]):
            data[materia][avaliacao]["Notas"][campo] = (
                clean_input(
                    st.text_input(f"{avaliacao} {campo+1}", 
                        data[materia][avaliacao]["Notas"][campo], 
                        key = f"{avaliacao}{campo+1}_{materia}")))
    data[materia][avaliacao]["Media"] = (eval(data[materia][avaliacao]["Conta"])(data[materia][avaliacao]["Notas"]))

def ask(materia):
    data = json.loads(open("data.json").read())

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("# Quizes")
        create_input(data, materia, "Quiz")
        st.write(data[materia]["Quiz"]["Media"])
        
    with col2:
        st.markdown("# APS")
        create_input(data, materia, "APS")
        st.write(data[materia]["APS"]["Media"])

    with col3:
        st.markdown("# Provas")
        create_input(data, materia, "PI")
        create_input(data, materia, "PF")
    
    data[materia]["Media"] = (
        eval(data[materia]["Quiz"]["Conta"])(data[materia]["Quiz"]["Notas"]) * data[materia]["Quiz"]["Peso"] +
        eval(data[materia]["APS"]["Conta"])(data[materia]["APS"]["Notas"]) * data[materia]["APS"]["Peso"] +
        eval(data[materia]["PI"]["Conta"])(data[materia]["PI"]["Notas"]) * data[materia]["PI"]["Peso"] +
        eval(data[materia]["PF"]["Conta"])(data[materia]["PF"]["Notas"]) * data[materia]["PF"]["Peso"]
    )
    
    json.dump(data, open('data.json', 'w'))

    st.write(data)

run()