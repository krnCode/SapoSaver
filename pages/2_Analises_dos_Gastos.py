import streamlit as st
import pandas as pd
from io import BytesIO

# CONFIGS
# --------------------
st.set_page_config(page_title="Analise dos Gastos", page_icon="🐸", layout="wide")


# FUNCÕES
# --------------------
def converter_para_excel_varias_planilhas(dfs: list, nome_planilhas: list) -> BytesIO:
    """
    Converte o dataframe para excel.
    Esta função converte vários dataframes para planilhas diferentes dentro do mesmo arquivo excel (.xlsx).

    Argumentos:
        dfs (list): Lista com todos os pandas dataframe já tratados.
        nome_planilhas (list): Lista com os nomes das planilhas que devem ser utilizados.

    Retorna:
        BytesIO: Objeto em bytes que pode ser posteriormente salvo em formato excel (.xlsx)
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for df, nome_planilha in zip(dfs, nome_planilhas):
            df.to_excel(writer, sheet_name=nome_planilha, index=False)

    output.seek(0)

    return output


# APP
# --------------------
# MARK: INTRODUÇÃO
st.markdown(
    """
    # Análise dos Gastos

    Nesta página você confere as análises de seus gastos, e pode também baixar uma planilha em excel com as análises.
    
    🚧 Página em construção 🚧

    ---
    """
)


# MARK: SIDEBAR
with st.sidebar:
    base_de_dados = st.file_uploader(
        label="Envie a sua planilha de gastos conforme planilha modelo:"
    )
