import streamlit as st
import pandas as pd

# CONFIGS
# --------------------
st.set_page_config(page_title="Inicio", page_icon="🐸")

# CAMINHOS
# --------------------
# Logo
logo = r"res/img/SapoSaver_nobg.png"


# APP
# --------------------
# MARK: LOGO
st.image(
    image=logo,
    width=200,
)


# MARK: INTRODUÇÃO
st.markdown(
    """
    # Sapo Saver
    Bem vindo ao Sapo Saver!

    Caso seja sua primeira vez utilizando o app, crie uma planilha de controle selecionando a página "Criar Planilha" ao lado.

    Caso já tenha sua planilha de investimento no modelo aceito pelo Sapo Saver, acesse a página "Análise dos Gastos" e faça o upload para iniciar as análises.
    
    O Sapo Saver te ajuda a criar uma planilha de controle que sempre fica com você, e quando precisar atualizar ou analisar os gastos, você faz o upload desta
    planilha no app pois não guardamos suas informações.

    ---
    """
)
