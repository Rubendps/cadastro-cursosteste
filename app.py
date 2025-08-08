import streamlit as st
import pandas as pd
import os

# Constantes
CURSOS = [f"Curso {i}" for i in range(1, 9)]
LIMITE_VAGAS = 25
PASTA_PLANILHAS = "planilhas"

# Cria pasta se não existir
if not os.path.exists(PASTA_PLANILHAS):
    os.makedirs(PASTA_PLANILHAS)

# CPF válido
def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    def calc_digito(cpf, peso):
        soma = sum(int(cpf[i]) * peso[i] for i in range(len(peso)))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)

    dig1 = calc_digito(cpf[:9], list(range(10, 1, -1)))
    dig2 = calc_digito(cpf[:9] + dig1, list(range(11, 1, -1)))

    return cpf[-2:] == dig1 + dig2

# Contar quantos inscritos existem por curso
def contar_inscritos(curso):
    arquivo = os.path.join(PASTA_PLANILHAS, f"{curso}.xlsx")
    if os.path.exists(arquivo):
        df = pd.read_excel(arquivo)
        return len(df)
    return 0

# Verifica se CPF já está inscrito em algum curso
def cpf_ja_cadastrado(cpf):
    for curso in CURSOS:
        arquivo = os.path.join(PASTA_PLANILHAS, f"{curso}.xlsx")
        if os.path.exists(arquivo):
            df = pd.read_excel(arquivo)
            if cpf in df['CPF'].astype(str).values:
                return True
    return False

# Salvar inscrição
def salvar_inscricao(curso, nome, cpf, telefone, turma):
    arquivo = os.path.join(PASTA_PLANILHAS, f"{curso}.xlsx")
    nova_inscricao = pd.DataFrame([{
        "Nome": nome,
        "CPF": cpf,
        "Telefone": telefone,
        "Turma": turma
    }])

    if os.path.exists(arquivo):
        df = pd.read_excel(arquivo)
        df = pd.concat([df, nova_inscricao], ignore_index=True)
    else:
        df = nova_inscricao

    df.to_excel(arquivo, index=False)

# Título
st.title("📚 Inscrição em Cursos")

# Escolha do curso com contador
curso_escolhido = st.selectbox("Selecione o curso:", [
    f"{curso} ({contar_inscritos(curso)}/{LIMITE_VAGAS})" for curso in CURSOS
])

curso_nome = curso_escolhido.split(" (")[0]
inscritos = contar_inscritos(curso_nome)

if inscritos >= LIMITE_VAGAS:
    st.warning("❌ Este curso está lotado. Escolha outro.")
else:
    st.subheader(f"Formulário de inscrição - {curso_nome}")

    nome = st.text_input("Nome completo")
    cpf = st.text_input("CPF (somente números)")
    telefone = st.text_input("Telefone (somente números)")
    turma = st.text_input("Turma")

    if st.button("Confirmar inscrição"):
        cpf = ''.join(filter(str.isdigit, cpf))
        telefone = ''.join(filter(str.isdigit, telefone))

        if not nome or not cpf or not telefone or not turma:
            st.error("Preencha todos os campos.")
        elif not validar_cpf(cpf):
            st.error("CPF inválido.")
        elif cpf_ja_cadastrado(cpf):
            st.error("Este CPF já está inscrito em um curso.")
        elif not telefone.isdigit():
            st.error("Telefone deve conter apenas números.")
        elif inscritos >= LIMITE_VAGAS:
            st.error("Este curso já atingiu o limite de inscrições.")
        else:
            salvar_inscricao(curso_nome, nome, cpf, telefone, turma)
            st.success(f"Inscrição realizada com sucesso no {curso_nome}!")

