import streamlit as st
import pandas as pd
import altair as alt
from io import BytesIO

# CONFIGS
# --------------------
# Pandas
pd.set_option("styler.format.precision", 2)
pd.set_option("display.precision", 2)


# Streamlit
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
    df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y")
    df = df.sort_values(by="Data", ascending=True)

    # MARK: FILTROS
    with st.sidebar:
        st.markdown("---")
        st.write("Variáveis de Controle dos Gastos")
        renda = st.number_input("Informe sua renda do mes:", min_value=0, value=0)
        meta_gastos = st.number_input(
            "Informe seu limite de gastos:", min_value=0, value=0
        )
        st.markdown("---")

        st.write("Filtros")
        # Filtro de períodos, lado a lado
        col1, col2 = st.columns([1, 1])
        with col1:
            ano = st.multiselect(
                label="Ano",
                options=df["Data"].dt.year.unique(),
                default=None,
                placeholder="Selecione",
            )
        with col2:
            mes = st.multiselect(
                label="Mes",
                options=df["Data"].dt.month.sort_values().unique(),
                default=None,
                placeholder="Selecione",
            )

        # Filtros de tipo e descrição da despesa
        descricao = st.multiselect(
            label="Descrição",
            options=df["Descrição"].unique(),
            default=None,
            placeholder="Selecione",
        )
        tipo = st.multiselect(
            label="Tipo",
            options=df["Tipo"].unique(),
            default=None,
            placeholder="Selecione",
        )

        df = df.assign(
            **{
                "Ano": df["Data"].dt.year,
                "Mes": df["Data"].dt.month,
            }
        )

        query = []
        if ano:
            query.append(f"Ano == {ano}")
        if mes:
            query.append(f"Mes == {mes}")
        if descricao:
            descricao_str = "', '".join(descricao)
            query.append(f"Descrição in ['{descricao_str}']")
        if tipo:
            tipo_str = "', '".join(tipo)
            query.append(f"Tipo in ['{tipo_str}']")
        if query:
            df_filtro = df.query(" and ".join(query))
        else:
            df_filtro = df

    # MARK: MÉTRICAS
    st.markdown("## Resumo do Mes Atual")
    col1, col2, col3 = st.columns([1, 1, 1])

    df_total_mes = (
        df.groupby([pd.Grouper(key="Data", freq="ME")])["Valor"].sum().reset_index()
    )
    df_dif_mes_anterior = df_total_mes.set_index("Data").diff().tail(n=1)

    with col1:
        st.metric(
            label="Gastos do Mês",
            value=df_total_mes["Valor"].tail(n=1),
            delta=round(df_dif_mes_anterior["Valor"].item(), 2),
            delta_color="inverse",
        )

    with col2:
        media_gastos = round(df_total_mes["Valor"].mean(), 2)
        st.metric(label="Valor Médio dos Gastos", value=media_gastos)

    with col3:
        pass

        gasto_menos_meta = df_total_mes["Valor"].tail(n=1).item() - meta_gastos
        if gasto_menos_meta < 0:
            gasto_menos_meta *= -1
        if meta_gastos <= df_total_mes["Valor"].tail(n=1).item():
            st.markdown(
                f"Total acima do previsto: :red[**{round(gasto_menos_meta,2)}**]"
            )
        else:
            st.balloons()
            st.markdown(
                f"Total abaixo do previsto :green[**{round(gasto_menos_meta,2)}**]"
            )

        renda_menos_gastos = df_total_mes["Valor"].tail(n=1).item() - renda
        if renda_menos_gastos < 0:
            renda_menos_gastos *= -1
        if renda <= df_total_mes["Valor"].tail(n=1).item():
            st.markdown(
                f"Após pagar todos os gastos, você terá de perda: :red[**{round(renda_menos_gastos,2)}**]"
            )
        else:
            st.markdown(
                f"Após pagar todos os gastos, você terá de sobra: :green[**{round(renda_menos_gastos,2)}**]"
            )

    st.markdown("---")

    # MARK: GRÁFICOS
    st.markdown("## Visualizações")
    col4, col5 = st.columns([1, 1])

    # TODO: Ajustar datas - tradução para pt_BR
    # TODO: Ajustar gráfico - descrição aparece entre as barras
    with col4:
        df_periodo = (
            df_filtro.groupby([pd.Grouper(key="Data", freq="ME")])["Valor"]
            .sum()
            .reset_index()
        )
        chart_extrato = (
            (
                alt.Chart(data=df_periodo)
                .mark_bar(align="center", cursor="auto")
                .encode(
                    x=alt.X(
                        "Data:T",
                        timeUnit="yearmonth",
                        axis=alt.Axis(
                            title="Periodo",
                            format="%b %y",
                            labelAlign="left",
                        ),
                    ),
                    y=alt.Y("Valor", title="Valor"),
                    color="Valor",
                )
            )
            .properties(
                title={
                    "text": "Gastos por Período",
                    "anchor": "middle",
                    "fontSize": 20,
                    "fontWeight": "bold",
                }
            )
            .interactive()
        )
        chart_renda = (
            alt.Chart(pd.DataFrame({"Renda": [renda]}))
            .mark_rule(
                color="#7CFFCB",
                description="Valor da Renda",
                strokeCap="butt",
                strokeWidth=1,
                strokeDash=[8.8],
            )
            .encode(y="Renda")
        )
        chart_meta_gastos = (
            alt.Chart(pd.DataFrame({"Meta de Gastos": [meta_gastos]}))
            .mark_rule(
                color="#eabe76",
                description="Meta de Gastos",
                strokeCap="butt",
                strokeWidth=1,
                strokeDash=[8.8],
            )
            .encode(y="Meta de Gastos")
        )
        chart_media_gastos = (
            alt.Chart(pd.DataFrame({"Media dos Gastos": [media_gastos]}))
            .mark_rule(
                color="#c1121f",
                description="Média dos Gastos",
                strokeCap="butt",
                strokeWidth=1,
                strokeDash=[8.8],
            )
            .encode(y="Media dos Gastos")
        )
        st.altair_chart(
            altair_chart=chart_extrato
            + chart_renda
            + chart_meta_gastos
            + chart_media_gastos,
            use_container_width=True,
        )

    with col5:
        df_descricao = (
            df_filtro.groupby(["Descrição", "Tipo"])["Valor"].sum().reset_index()
        )
        chart_descricao = (
            alt.Chart(data=df_descricao)
            .mark_bar(align="center", cursor="auto")
            .encode(
                x="Valor",
                y=alt.Y("Descrição").sort("-x"),
                color="Tipo",
            )
            .properties(
                title={
                    "text": "Total de Gastos Conforme Descrição",
                    "anchor": "middle",
                    "fontSize": 20,
                    "fontWeight": "bold",
                }
            )
            .interactive()
        )
        st.altair_chart(altair_chart=chart_descricao, use_container_width=True)
    st.markdown("---")

else:
    st.markdown(
        """
    ### Faça o upload da sua planilha de gastos na tela lateral 👈
    """
    )


with st.sidebar:
    st.markdown(
        """
    ---

    [![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/B0B3V8QAU)
    
    """
    )
