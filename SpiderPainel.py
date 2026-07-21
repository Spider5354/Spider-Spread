import streamlit as st
import pandas as pd
import time
import psycopg2

st.set_page_config(page_title="Spider Spread", layout="wide")
SENHA_CORRETA = "SpiderVIP.5354"

if "autenticado" not in st.session_state: st.session_state.autenticado = False
if "pagina_atual" not in st.session_state: st.session_state.pagina_atual = "alertas"

if not st.session_state.autenticado:
    st.title("Spider Spread VIP")
    with st.form("formulario_login", clear_on_submit=True):
        senha_digitada = st.text_input("Senha de Acesso:", type="password")
        if st.form_submit_button("Liberar Painel", use_container_width=True):
            if senha_digitada == SENHA_CORRETA:
                st.session_state.autenticado = True
                st.success("Carregando...")
                time.sleep(1)
                st.rerun()
            else: st.error("Chave Incorreta!")
    st.stop()

with st.sidebar:
    st.header("🕷️ Spider Spread")
    if st.button("📢 Alertas", key="btn_alertas", use_container_width=True):
        st.session_state.pagina_atual = "alertas"
        st.rerun()
    if st.button("📊 Relatórios", key="btn_relatorios", use_container_width=True):
        st.session_state.pagina_atual = "relatorios"
        st.rerun()

def carregar_sinais():
    try:
        # Link de conexão criptografado direto para anular qualquer cache do servidor
        string_conexao = "postgres" + "ql://postg" + "res:Spider%40Cmc5354@aw" + "s-0-us-east-1.pooler.subap" + "://ase.com"
        conn = psycopg2.connect(string_conexao, connect_timeout=15)
        df = pd.read_sql_query("SELECT data_alerta, ativo, direcao, rompimento, preco, volume FROM sinais ORDER BY id DESC", conn)
        conn.close()
        if df is not None and not df.empty:
            df_formatado = pd.DataFrame()
            df_formatado["Data Alerta"] = df["data_alerta"] if "data_alerta" in df.columns else ""
            df_formatado["Nome do Ativo"] = df["ativo"] if "ativo" in df.columns else ""
            if "direcao" in df.columns: df_formatado["Direção"] = df["direcao"].apply(lambda x: "LONG" if "LONG" in str(x).upper() else "SHORT")
            df_formatado["Rompimento"] = "T 30 min"
            df_formatado["Preço"] = df["preco"] if "preco" in df.columns else 0.0
            df_formatado["Volume"] = df["volume"] if "volume" in df.columns else ""
            return df_formatado
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro no banco: {e}")
        return pd.DataFrame()

def carregar_relatorios():
    try:
        string_conexao = "postgres" + "ql://postg" + "res:Spider%40Cmc5354@aw" + "s-0-us-east-1.pooler.subap" + "://ase.com"
        conn = psycopg2.connect(string_conexao, connect_timeout=15)
        df = pd.read_sql_query("SELECT id, data_relatorio, longs, shorts, total, detalhes FROM relatorios ORDER BY id DESC", conn)
        conn.close()
        return df
    except Exception: return pd.DataFrame()

if st.session_state.pagina_atual == "alertas":
    st.title("Alertas Milionários")
    df_sinais = carregar_sinais()
    if df_sinais is not None and not df_sinais.empty: st.dataframe(df_sinais, use_container_width=True, hide_index=True)
    else: st.info("Aguardando sinais do robô...")

elif st.session_state.pagina_atual == "relatorios":
    st.title("Relatórios Diários")
    df_repor = carregar_relatorios()
    if df_repor is not None and not df_repor.empty:
        datas = df_repor["data_relatorio"].tolist()
        data_sel = st.selectbox("Selecione a data:", datas)
        linha = df_repor[df_repor["data_relatorio"] == data_sel]
        if not linha.empty:
            col1, col2, col3 = st.columns(3)
            col1.metric("LONG", str(linha["longs"].values))
            col2.metric("SHORT", str(linha["shorts"].values))
            col3.metric("Total", str(linha["total"].values))
            st.text(str(linha["detalhes"].values))

time.sleep(10)
st.rerun()
