import streamlit as st
import pandas as pd
import re
import io

st.set_page_config(page_title="Inscrição de Cursos", page_icon="📋")

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

# Inicializa o estado
if "inscricoes" not in st.session_state:
    st.session_state.inscricoes = {curso: [] for curso in cursos_disponiveis}

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

# Interface principal
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

    inscritos = st.session_state.inscricoes[curso_nome]
    cpfs = [i["CPF"] for i in inscritos]

    if not validar_cpf(cpf):
        st.error("❌ CPF inválido.")
    elif not validar_telefone(telefone):
        st.error("❌ Telefone inválido. Use apenas números.")
    elif not nome or not turma or not turno:
        st.warning("⚠️ Por favor, preencha todos os campos.")
    elif cpf in cpfs:
        st.warning("⚠️ Este CPF já está inscrito neste curso.")
    elif len(inscritos) >= 25:
        st.error("❌ Este curso já atingiu o limite de 25 inscritos.")
    else:
        st.session_state.inscricoes[curso_nome].append({
            "Nome": nome,
            "CPF": cpf,
            "Telefone": telefone,
            "Turma": turma,
            "Turno": turno
        })
        st.success("✅ Inscrição realizada com sucesso!")

# 🔒 Área secreta para ADM (você)
st.divider()
senha = st.text_input("Área restrita - digite a senha para acessar as inscrições:", type="password")

if senha == "admin123":  # Você pode trocar essa senha
    st.subheader("📥 Download das inscrições por curso")

    for curso, inscritos in st.session_state.inscricoes.items():
        if inscritos:
            df = pd.DataFrame(inscritos)
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name=curso[:31])  # Excel limita nome da aba a 31 chars
            buffer.seek(0)
            st.download_button(
                label=f"📥 Baixar {curso} ({len(inscritos)} inscritos)",
                data=buffer,
                file_name=f"{curso}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.text(f"{curso}: nenhum inscrito.")
