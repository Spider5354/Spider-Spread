import streamlit as st
import pandas as pd
import sqlite3
import time

# Configuração da página web
st.set_page_config(page_title="Spider Spread - Painel de Sinais", layout="wide")

# Inicialização do controle de navegação de telas
if "pagina_atual" not in st.session_state:
    st.session_state.pagina_atual = "alertas"

# ==========================================
# CUSTOMIZAÇÃO ESTÉTICA VISUAL COMPLETA (CSS)
# ==========================================
st.markdown(
    """
    <style>
        /* 1. Barra lateral com o Degradê de Azul do Spider */
        section[data-testid="stSidebar"] {
            background-image: linear-gradient(180deg, #4da6ff 0%, #003366 100%) !important;
            background-color: #4da6ff !important;
        }
        
        .historico-carlos {
            color: #ffffff !important;
            font-size: 15px !important;
            font-weight: bold !important;
            text-align: center;
            margin-top: 20px;
        }
        
        .stApp {
            background-color: #fff2f2 !important;
        }
        
        /* Estilização dos botões nativos em Vermelho Aranha com texto Branco */
        div.stButton > button {
            background-color: #ff000d !important;
            color: #ffffff !important;
            border-radius: 8px !important;
            border: 1px solid #ff4d55 !important;
            font-weight: bold !important;
            font-size: 16px !important;
            padding: 10px 20px !important;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.3) !important;
            transition: 0.3s !important;
        }
        
        div.stButton > button:hover {
            background-color: #b30009 !important;
            color: #ffffff !important;
            border-color: #b30009 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================
# MENU LATERAL PERSONALIZADO (SIDEBAR)
# ==========================================
with st.sidebar:
    st.markdown(
        """
        <div style="text-align: center;" translate="no">
            <div style="font-size: 80px; line-height: 1.1; margin-bottom: 10px; filter: drop-shadow(0px 4px 8px rgba(0,0,0,0.5));">🕷️</div>
            <h2 style="color: #ffffff; font-family: 'Arial Black', Gadget, sans-serif; letter-spacing: 1.5px; margin-top: 0px; margin-bottom: 0px;">Spider Spread</h2>
        </div>
        """, 
        unsafe_allow_html=True
    )
    st.markdown("<br><hr style='border-color: rgba(255,255,255,0.3);'>", unsafe_allow_html=True)
    
    # Nomes curtos e isolados para blindar o tradutor do Chrome de vez
    st.markdown('<div translate="no">', unsafe_allow_html=True)
    
    if st.button("📢 Alertas", key="btn_alertas_curto", use_container_width=True):
        st.session_state.pagina_atual = "alertas"
        st.rerun()
        
    if st.button("📊 Relatórios", key="btn_relatorios_curto", use_container_width=True):
        st.session_state.pagina_atual = "relatorios"
        st.rerun()
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    <br><br><br><br><br>
    st.markdown("<hr style='border-color: rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
    st.markdown("<div class='historico-carlos' translate='no'>📋 Histórico de Carlos Caldeira</div>", unsafe_allow_html=True)

# ==========================================
# FUNÇÕES DE BUSCA DE DADOS (SQLITE)
# ==========================================
def carregar_sinais():
    try:
        conn = sqlite3.connect("alertas.db")
        df = pd.read_sql_query("SELECT data_alerta, ativo, direcao, rompimento, preco, volume FROM sinais ORDER BY id DESC", conn)
        conn.close()
        return df
    except Exception: return pd.DataFrame()

def carregar_relatorios():
    try:
        conn = sqlite3.connect("alertas.db")
        df = pd.read_sql_query("SELECT id, data_relatorio, longs, shorts, total, detalhes FROM relatorios ORDER BY id DESC", conn)
        conn.close()
        return df
    except Exception: return pd.DataFrame()

# ==========================================
# RENDERIZAÇÃO DA TELA SELECIONADA
# ==========================================
if st.session_state.pagina_atual == "alertas":
    st.markdown("<h1 style='color: #111111;' translate='no'>Alertas Milionários</h1>", unsafe_allow_html=True)
    st.caption("Acompanhamento de rompimentos de pivot e pullbacks por zona sincronizados com o robô Python")
    st.markdown("<br>", unsafe_allow_html=True)

    df_sinais = carregar_sinais()
    if not df_sinais.empty:
        df_sinais['direcao'] = df_sinais['direcao'].apply(lambda x: "🟩 LONG" if 'LONG' in str(x).upper() else "🟥 SHORT")
        df_sinais['rompimento'] = "T 30 min"
        df_sinais.columns = ["Data Alerta", "Nome do Ativo", "Direção", "Rompimento", "Preço", "Volume"]
        st.dataframe(df_sinais, use_container_width=True, hide_index=True)
    else:
        st.info("Aguardando os sinais do robô...")

elif st.session_state.pagina_atual == "relatorios":
    st.markdown("<h1 style='color: #111111;'>Histórico de Relatórios Diários (21h)</h1>", unsafe_allow_html=True)
    st.caption("Central de fechamento operacional gravado de forma automática todas as noites")
    st.markdown("<br>", unsafe_allow_html=True)

    df_repor = carregar_relatorios()
    if not df_repor.empty:
        datas_disponiveis = df_repor['data_relatorio'].tolist()
        data_selecionada = st.selectbox("📅 Selecione a data do relatório que deseja revisar:", datas_disponiveis)
        
        linha_relatorio = df_repor[df_repor['data_relatorio'] == data_selecionada].iloc[0]
        
        col1, col2, col3 = st.columns(3)
        col1.metric("🟩 Sinais LONG", int(linha_relatorio['longs']))
        col2.metric("🔴 Sinais SHORT", int(linha_relatorio['shorts']))
        col3.metric("🔢 Total do Dia", int(linha_relatorio['total']))
        
        st.markdown("---")
        st.markdown(f"### 📋 Ativos Operados em {data_selecionada}:")
        st.text(linha_relatorio['detalhes'])
    else:
        st.info("Ainda não há relatórios gravados às 21h. O primeiro fechamento aparecerá aqui de forma automática!")

# Auto-refresh de 10 segundos
time.sleep(10)
st.rerun()
