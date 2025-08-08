import streamlit as st
import pandas as pd
import os
import re

# Criar pasta planilhas se não existir
if not os.path.exists("planilhas"):
    os.makedirs("planilhas")

# Função para validar CPF
def cpf_valido(cpf):
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    for i in range(9, 11):
        soma = sum(int(cpf[j]) * ((i + 1) - j) for j in range(i))
        digito = ((soma * 10) % 11) % 10
        if digito != int(cpf[i]):
            return False
    return True

# Função para salvar inscrição
def salvar_inscricao(curso, nome, cpf, telefone, turma, turno):
    arquivo = f"planilhas/{curso}.xlsx"

    nova_inscricao = pd.DataFrame([{
        "Nome": nome,
        "CPF": cpf,
        "Telefone": telefone,
        "Turma": turma,
        "Turno": turno
    }])

    try:
        if os.path.exists(arquivo):
            df_existente = pd.read_excel(arquivo)
        else:
            df_existente = pd.DataFrame()

        if cpf in df_existente['CPF'].astype(str).values:
            return "⚠️ Este CPF já está inscrito neste curso."

        if len(df_existente) >= 25:
            return "❌ Limite de 25 inscritos atingido para este curso."

        df_novo = pd.concat([df_existente, nova_inscricao], ignore_index=True)
        df_novo.to_excel(arquivo, index=False)
        return "✅ Inscrição realizada com sucesso!"

    except Exception as e:
        return f"Erro ao salvar inscrição: {e}"

# Lista de cursos
cursos = [
    "Curso 1", "Curso 2", "Curso 3", "Curso 4",
    "Curso 5", "Curso 6", "Curso 7", "Curso 8"
]

# Interface
st.title("📚 Cadastro para Cursos")
st.write("Preencha o formulário abaixo para se inscrever em um curso. Cada pessoa pode se inscrever apenas em **um** curso.")

curso_escolhido = st.selectbox("📝 Escolha o curso", cursos)
cpf = st.text_input("📇 CPF (somente números)")
nome = st.text_input("👤 Nome completo")
telefone = st.text_input("📞 Telefone (somente números)")
turma = st.text_input("🏷️ Turma")
turno = st.selectbox("🕐 Turno", ["Manhã", "Tarde", "Noite"])

if st.button("Enviar inscrição"):
    if not cpf_valido(cpf):
        st.error("❌ CPF inválido. Verifique e tente novamente.")
    elif not telefone.isdigit():
        st.error("❌ Telefone deve conter apenas números.")
    else:
        mensagem = salvar_inscricao(curso_escolhido, nome, cpf, telefone, turma, turno)
        if mensagem.startswith("✅"):
            st.success(mensagem)
        elif mensagem.startswith("⚠️"):
            st.warning(mensagem)
        else:
            st.error(mensagem)
