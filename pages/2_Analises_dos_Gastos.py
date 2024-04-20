import streamlit as st
import pandas as pd
from io import BytesIO

# CONFIGS
# --------------------
st.set_page_config(page_title="Analise dos Gastos", page_icon="🐸", layout="wide")

# CONSTANTES
# --------------------
MESES: list = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
]


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
    base_de_dados: pd.DataFrame = st.file_uploader(
        label="Envie a sua planilha de gastos conforme planilha modelo:", type="xlsx"
    )


# MARK: APP
if base_de_dados is not None:
    df: pd.DataFrame = pd.read_excel(io=base_de_dados)

    # MARK: TRATAMENTO DADOS
    df = df.sort_values(by="Data", ascending=True)
    df = df.assign(
        **{
            "Mes": df["Data"].dt.month_name(locale="pt_BR"),
            "Ano": df["Data"].dt.year,
        }
    )
    df["Mes"] = pd.Categorical(df["Mes"], categories=MESES, ordered=True)

    # MARK: DFS AGRUPADAS
    df_por_tipo = df.pivot_table(
        values="Valor",
        index=["Ano", "Mes"],
        columns="Tipo",
        aggfunc="sum",
        fill_value=0,
        observed=True,
    )

    # MARK: ANÁLISES
    # Extrato
    st.markdown("## Extrato")
    col1, col2 = st.columns([2, 1])

    with col1:
        pass

    with col2:
        extrato_despesas = st.dataframe(
            data=df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Data": st.column_config.DatetimeColumn(format="DD/MM/YYYY")
            },
        )
    st.markdown("---")

    # Gastos por tipo

    st.markdown("## Gastos por Tipo")

    col3, col4 = st.columns([2, 1])

    with col3:
        pass

    with col4:
        por_tipo = st.dataframe(
            data=df_por_tipo,
            use_container_width=True,
            column_config={"Mes": st.column_config.TextColumn()},
        )
    st.markdown("---")

else:
    st.markdown(
        """
    ### Faça o upload da sua planilha de gastos na tela lateral 👈
    """
    )
