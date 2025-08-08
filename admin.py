import streamlit as st
import os
import pandas as pd

# Senha para acessar o painel
SENHA = "12345"

# Título da página
st.title("🔒 Painel Administrativo")

# Campo de senha
senha_digitada = st.text_input("Digite a senha para acessar:", type="password")

if senha_digitada != SENHA:
    st.warning("Acesso restrito. Informe a senha correta.")
    st.stop()

# Pasta onde os arquivos estão
PASTA = "planilhas"

if not os.path.exists(PASTA):
    st.error("❌ A pasta de planilhas não foi encontrada.")
    st.stop()

# Lista os arquivos .xlsx disponíveis
arquivos = [f for f in os.listdir(PASTA) if f.endswith(".xlsx")]

if not arquivos:
    st.info("Nenhum arquivo de inscrição encontrado ainda.")
else:
    st.success("Arquivos de inscrição encontrados:")

    for arquivo in arquivos:
        caminho = os.path.join(PASTA, arquivo)
        df = pd.read_excel(caminho)
        st.subheader(f"📄 {arquivo} ({len(df)} inscritos)")
        st.dataframe(df)

        # Botão para download
        with open(caminho, "rb") as f:
            st.download_button(
                label=f"📥 Baixar {arquivo}",
                data=f,
                file_name=arquivo,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
