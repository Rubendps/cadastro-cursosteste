import streamlit as st
import pandas as pd
import os
import re

st.set_page_config(page_title="Inscrição de Cursos", page_icon="📋")

# Lista de cursos disponíveis
cursos_disponiveis = [
    "Informática Básica",
    "Programação Python",
    "Excel Avançado",
    "Design Gráfico",
    "Administração",
    "Marketing Digital",
    "Inglês Básico",
    "Robótica Educacional"
]

# Função para validar CPF
def validar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    for i in range(9, 11):
        soma = sum(int(cpf[j]) * ((i + 1) - j) for j in range(i))
        digito = ((soma * 10) % 11) % 10
        if digito != int(cpf[i]):
            return False
    return True

# Função para validar telefone
def validar_telefone(telefone):
    return telefone.isdigit() and 8 <= len(telefone) <= 11

# Função para salvar inscrição
def salvar_inscricao(curso, nome, cpf, telefone, turma_turno):
    try:
        pasta = "planilhas"
        if not os.path.exists(pasta):
            os.makedirs(pasta)

        arquivo = os.path.join(pasta, f"{curso}.xlsx")
        nova_inscricao = pd.DataFrame([{
            "Nome": nome,
            "CPF": cpf,
            "Telefone": telefone,
            "Turma": turma_turno
        }])

        if os.path.exists(arquivo):
            df_existente = pd.read_excel(arquivo)
        else:
            df_existente = pd.DataFrame(columns=["Nome", "CPF", "Telefone", "Turma"])

        if not df_existente.empty and cpf in df_existente["CPF"].values:
            return "cpf_ja_inscrito"

        if len(df_existente) >= 25:
            return "limite"

        df_novo = pd.concat([df_existente, nova_inscricao], ignore_index=True)
        df_novo.to_excel(arquivo, index=False, engine="openpyxl")
        return "ok"
    except Exception as e:
        print("Erro ao salvar:", e)
        return "erro"

# Interface Streamlit
st.title("📋 Formulário de Inscrição em Cursos")

curso_nome = st.selectbox("Escolha o curso desejado:", cursos_disponiveis)
cpf = st.text_input("CPF (somente números):")
nome = st.text_input("Nome completo:")
telefone = st.text_input("Telefone (somente números):")
turma = st.text_input("Turma:")
turno = st.selectbox("Turno:", ["Manhã", "Tarde", "Noite"])

if st.button("Enviar Inscrição"):
    cpf = re.sub(r'\D', '', cpf)
    telefone = re.sub(r'\D', '', telefone)

    if not validar_cpf(cpf):
        st.error("❌ CPF inválido.")
    elif not validar_telefone(telefone):
        st.error("❌ Telefone inválido. Use apenas números.")
    elif not nome or not turma or not turno:
        st.warning("⚠️ Por favor, preencha todos os campos.")
    else:
        resultado = salvar_inscricao(curso_nome, nome, cpf, telefone, f"{turma} - {turno}")
        if resultado == "ok":
            st.success("✅ Inscrição realizada com sucesso!")
        elif resultado == "cpf_ja_inscrito":
            st.warning("⚠️ Este CPF já está inscrito neste curso.")
        elif resultado == "limite":
            st.error("❌ Este curso já atingiu o limite de 25 inscritos.")
        else:
            st.error("❌ Ocorreu um erro ao salvar a inscrição.")
