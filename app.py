import streamlit as st
import numpy as np
import pandas as pd
import json

st.set_page_config(page_title='Notas', layout='wide')

def run():

    materia = st.sidebar.selectbox(
        'Escolha a matéria',
        json.loads(open("preset_5ECO.json").read()).keys())

    ask(materia)

def clean_input(text):
    if text == "":
        text = 0
    else:
        text = float(text.replace(",", "."))
        if text > 10 or text < 0:
            text = np.nan
    return text

def ask(materia = "Financas"):
    data = json.loads(open("preset_5ECO.json").read())[materia]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("# Quizes")
        for text in range(data["Quiz"]["Campos"]):
            key = f"Quiz{text+1}_{materia}"
            if key in st.session_state:
                data["Quiz"]["Notas"].append(clean_input(st.text_input(f"Quiz {text+1}", st.session_state[key], key = key)))
            else:
                data["Quiz"]["Notas"].append(clean_input(st.text_input(f"Quiz {text+1}", key = key)))
        st.write(eval(data["Quiz"]["Conta"])(data["Quiz"]["Notas"]))
        
    with col2:
        st.markdown("# APS")
        for text in range(data["APS"]["Campos"]):
            data["APS"]["Notas"].append(clean_input(st.text_input(f"APS {text+1}", key = f"APS{text+1}_{materia}")))
        st.write(eval(data["APS"]["Conta"])(data["APS"]["Notas"]))

    with col3:
        st.markdown("# Provas")
        data["PI"]["Notas"].append(clean_input(st.text_input(f"Prova Intermediária", key = f"PI_{materia}")))
        data["PF"]["Notas"].append(clean_input(st.text_input(f"Prova Final", key = f"PF_{materia}")))
    
    data["Media"] = (
        eval(data["Quiz"]["Conta"])(data["Quiz"]["Notas"]) * data["Quiz"]["Peso"] +
        eval(data["APS"]["Conta"])(data["APS"]["Notas"]) * data["APS"]["Peso"] +
        eval(data["PI"]["Conta"])(data["PI"]["Notas"]) * data["PI"]["Peso"] +
        eval(data["PF"]["Conta"])(data["PF"]["Notas"]) * data["PF"]["Peso"]
    )
    
    st.write(data)

run()