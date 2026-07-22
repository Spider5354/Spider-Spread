import streamlit as st
import pandas as pd
import time
import psycopg2
st.set_page_config(page_title="Spider Spread", layout="wide")
SENHA_CORRETA = "SpiderVIP.5354"
if "autenticado" not in st.session_state:
st.session_state.autenticado = False
if "pagina_atual" not in st.session_state:
st.session_state.pagina_atual = "alertas"
if not st.session_state.autenticado:
st.title("🕷️ Spider Spread VIP")
st.write("Este é um painel privado. Digite a credencial para liberar os sinais.")
with st.form("formulario_login", clear_on_submit=True):
senha_digitada = st.text_input("🔑 Senha de Acesso:", type="password")
botao_entrar = st.form_submit_button("Liberar Painel Operational", use_container_width=True)
if botao_entrar:
if senha_digitada == SENHA_CORRETA:
st.session_state.autenticado = True
st.success("Acesso autorizado com sucesso! Carregando...")
time.sleep(1)
st.rerun()
else:
st.error("❌ Senha incorreta!")
st.stop()
with st.sidebar:
st.title("🕷️ Spider Spread")
st.write("---")
if st.button("📢 Alertas", key="btn_alertas", use_container_width=True):
st.session_state.pagina_atual = "alertas"
st.rerun()
if st.button("📊 Relatórios", key="btn_relatorios", use_container_width=True):
st.session_state.pagina_atual = "relatorios"
st.rerun()
st.write("




", unsafe_allow_html=True)
st.write("---")
st.info("📋 Histórico de Carlos Caldeira")
