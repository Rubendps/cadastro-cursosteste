import streamlit as st
import os

st.set_page_config(page_title="Administração - Cursos", layout="centered")

st.title("🔒 Área Administrativa - Cursos")

senha = st.text_input("Digite a senha:", type="password")

SENHA_CORRETA = "brasil"

if senha == SENHA_CORRETA:
    st.success("✅ Acesso liberado!")

    cursos = ["Curso 1", "Curso 2", "Curso 3", "Curso 4", "Curso 5", "Curso 6", "Curso 7", "Curso 8"]

    for curso in cursos:
        nome_arquivo = f"planilhas/{curso}.xlsx"
        if os.path.exists(nome_arquivo):
            with open(nome_arquivo, "rb") as f:
                st.download_button(
                    label=f"⬇️ Baixar inscrições do {curso}",
                    data=f,
                    file_name=f"{curso}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.write(f"📄 Nenhuma inscrição no {curso}")
elif senha != "":
    st.error("❌ Senha incorreta!")
