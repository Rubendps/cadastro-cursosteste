import streamlit as st
from supabase import create_client, Client
import re

# === CONFIGURAÇÕES DO SUPABASE ===
url = "https://obzcymaydfjvsqdnmtty.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9iemN5bWF5ZGZqdnNxZG5tdHR5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ2NjQ2MTIsImV4cCI6MjA3MDI0MDYxMn0.gPUFx0r_SP-g2bl9sOzlxlmkzGPl9_eMk1ORDjMNMXg"
supabase: Client = create_client(url, key)

# === FUNÇÕES DE VALIDAÇÃO ===
def validar_cpf(cpf):
    cpf = re.sub(r'[^0-9]', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    for i in range(9, 11):
        soma = sum(int(cpf[j]) * ((i + 1) - j) for j in range(i))
        digito = (soma * 10) % 11
        if digito == 10:
            digito = 0
        if digito != int(cpf[i]):
            return False
    return True

def validar_telefone(telefone):
    return re.fullmatch(r'\d{10,11}', telefone) is not None

# === INTERFACE STREAMLIT ===
st.title("📋 Cadastro de Cursos")
st.write("Preencha os dados abaixo para se inscrever em **um único curso**.")

curso = st.selectbox("Selecione o curso:", [
    "Curso 1", "Curso 2", "Curso 3", "Curso 4",
    "Curso 5", "Curso 6", "Curso 7", "Curso 8"
])

cpf = st.text_input("CPF (apenas números):")
nome = st.text_input("Nome completo:")
telefone = st.text_input("Telefone (apenas números):")
turma = st.text_input("Turma:")
turno = st.selectbox("Turno:", ["Manhã", "Tarde", "Noite"])

if st.button("📥 Enviar inscrição"):
    cpf_valido = validar_cpf(cpf)
    telefone_valido = validar_telefone(telefone)

    if not cpf_valido:
        st.error("❌ CPF inválido.")
    elif not telefone_valido:
        st.error("❌ Telefone inválido. Use apenas números.")
    else:
        # Verifica se CPF já está inscrito
        existe = supabase.table("inscricoes").select("cpf").eq("cpf", cpf).execute()
        if len(existe.data) > 0:
            st.warning("⚠️ Este CPF já está inscrito em um curso.")
        else:
            # Verifica limite de vagas do curso
            total_inscritos = supabase.table("inscricoes").select("curso").eq("curso", curso).execute()
            if len(total_inscritos.data) >= 25:
                st.warning(f"⚠️ O curso '{curso}' já atingiu o limite de 25 inscritos.")
            else:
                try:
                    supabase.table("inscricoes").insert({
                        "curso": curso,
                        "cpf": cpf,
                        "nome": nome,
                        "telefone": telefone,
                        "turma": turma,
                        "turno": turno
                    }).execute()
                    st.success("✅ Inscrição realizada com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao salvar inscrição: {e}")
