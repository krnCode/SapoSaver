import streamlit as st
import pandas as pd
from io import BytesIO

# CONFIGS
# --------------------
st.set_page_config(page_title="Criar Planilha", page_icon="🐸", layout="wide")


# FUNÇÕES
# --------------------
def converter_para_excel(df: pd.DataFrame) -> BytesIO:
    """
    Converte o dataframe para excel.
    Esta função converte para apenas uma planiha.

    Argumentos:
        df (pd.DataFrame): Pandas dataframe já tratado.

    Retorna:
        BytesIO: Objeto em bytes que pode ser posteriormente salvo em formato excel (.xlsx)
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(
            writer,
            index=False,
            sheet_name="Dados",
        )

    output.seek(0)

    return output


# APP
# --------------------
# MARK: INTRODUÇÃO
st.markdown(
    """
    # Criar Planilha

    Nesta página você pode criar uma planilha de controle de seus gastos.
    
    🚧 Página em construção 🚧
    
    ---
    """
)

# MARK: APP
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(
        """
        ## Planilha Modelo        

        Preencha seus gastos abaixo ou faça o download do modelo para preencher em excel.

        Caso você já tenha uma planilha em que controla gastos, poderá baixar a planilha modelo e popular suas colunas com o que já tem em sua planilha. 

    """
    )

    df_modelo = pd.DataFrame(
        {
            "Data": ["01/01/2000", "10/02/2000", "15/03/2000"],
            "Descrição": [
                "Exemplo de registro 1 - Almoço",
                "Exemplo de registro 2 - Cinema com amigos",
                "Exemplo de registro 3 - Parcela da faculdade",
            ],
            "Tipo": ["Alimentação", "Lazer", "Educação"],
            "Valor": [100.00, 70.00, 350.00],
        }
    )

    df = st.data_editor(data=df_modelo, num_rows="dynamic")

    st.download_button(
        label="Download Modelo",
        data=converter_para_excel(df=df),
        file_name="SapoSaverControleGastos.xlsx",
    )

with col2:
    st.markdown(
        """
        ## Como preencher corretamente:

        Quando estiver usando a planilha modelo, você precisa:
        * Manter o nome das colunas conforme o modelo;
        * Manter o padrão de preenchimento:
            * Data: precisa ser no estilo dia/mes/ano (dd/mm/aaaa)
            * Descrição: pode ser preenchido com a descrição que preferir;
            * Tipo: você pode colocar qualquer descrição de tipo neste campo, como sugestão o tipo deve ser breve e fácil de entender com poucos termos;
            * Valor: deve ser preenchido apenas com números.
        
    """
    )

st.markdown("---")
