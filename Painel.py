import streamlit as st
import pandas as pd
import time
import requests

# Configuração da página web
st.set_page_config(page_title="Spider Spread - Painel de Sinais", layout="wide")

# Definição da senha de acesso VIP do painel
SENHA_CORRETA = "SpiderVIP.5354"

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if "pagina_atual" not in st.session_state:
    st.session_state.pagina_atual = "alertas"

# ==========================================
# TELA DE LOGIN (BLOQUEIO DE ACESSO)
# ==========================================
if not st.session_state.autenticado:
    st.markdown(
        """
        <div style="text-align: center; margin-top: 50px;" translate="no">
            <div style="font-size: 100px; line-height: 1.1; margin-bottom: 20px;">🕷️</div>
            <h1 style="color: #ff000d; font-family: 'Arial Black', Gadget, sans-serif; letter-spacing: 2px;">Spider Spread VIP</h1>
            <p style="color: #666666;">Este é um painel privado. Digite a credencial para liberar os sinais.</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    with st.form("formulario_login", clear_on_submit=True):
        senha_digitada = st.text_input("🔑 Senha de Acesso:", type="password", placeholder="Digite a chave privada aqui...")
        botao_entrar = st.form_submit_button("Liberar Painel Operational", use_container_width=True)
        
        if botao_entrar:
            if senha_digitada == SENHA_CORRETA:
                st.session_state.autenticado = True
                st.success("Acesso autorizado com sucesso! Carregando...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Senha incorreta! Caso tenha esquecido, entre em contato com o administrador.")
    st.stop()

# ==========================================
# CUSTOMIZAÇÃO ESTÉTICA VISUAL COMPLETA (CSS)
# ==========================================
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            background-image: linear-gradient(180deg, #4da6ff 0%, #003366 100%) !important;
            background-color: #4da6ff !important;
        }
        .historico-carlos { color: #ffffff !important; font-size: 15px !important; font-weight: bold !important; text-align: center; margin-top: 20px; }
        .stApp { background-color: #fff2f2 !important; }
        div.stButton > button {
            background-color: #ff000d !important; color: #ffffff !important; border-radius: 8px !important;
            border: 1px solid #ff4d55 !important; font-weight: bold !important; font-size: 16px !important;
            padding: 10px 20px !important; box-shadow: 0px 4px 10px rgba(0,0,0,0.3) !important; transition: 0.3s !important;
        }
        div.stButton > button:hover { background-color: #b30009 !important; color: #ffffff !important; border-color: #b30009 !important; }
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
    
    st.markdown('<div translate="no">', unsafe_allow_html=True)
    if st.button("📢 Alertas", key="btn_alertas_curto", use_container_width=True):
        st.session_state.pagina_atual = "alertas"
        st.rerun()
    if st.button("📊 Relatórios", key="btn_relatorios_curto", use_container_width=True):
        st.session_state.pagina_atual = "relatorios"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
    st.markdown("<div class='historico-carlos' translate='no'>📋 Histórico de Carlos Caldeira</div>", unsafe_allow_html=True)

# ==========================================
# FUNÇÕES DE BUSCA E DIAGNÓSTICO INDEPENDENTES
# ==========================================
def carregar_sinais():
    try:
        url = "https://supabase.co"
        nova_chave = "sb_publishable_gBU-BMvqUKIoTlXppK1_NA_SCQDl_OL"
        
        headers = {
            "apikey": nova_chave,
            "Authorization": f"Bearer {nova_chave}",
            "Cache-Control": "no-cache"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        # Exibe o status da requisição e os dados puros recebidos na tela do painel
        st.write(f"🔍 Status da API Supabase: {response.status_code}")
        st.write(f"📦 Resposta Bruta: {response.text}")
        
        if response.status_code == 200:
            dados = response.json()
            if dados and len(dados) > 0:
                return pd.DataFrame(dados)
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao diagnosticar sinais: {e}")
        return pd.DataFrame()

def carregar_relatorios():
    try:
        url = "https://supabase.co"
        nova_chave = "sb_publishable_gBU-BMvqUKIoTlXppK1_NA_SCQDl_OL"
        
        headers = {
            "apikey": nova_chave,
            "Authorization": f"Bearer {nova_chave}",
            "Cache-Control": "no-cache"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            if dados and len(dados) > 0:
                return pd.DataFrame(dados)
        return pd.DataFrame()
    except Exception:
        return pd.DataFrame()

# ==========================================
# RENDERIZAÇÃO DA TELA SELECIONADA
# ==========================================
if st.session_state.pagina_atual == "alertas":
    st.markdown("<h1 style='color: #111111;' translate='no'>Alertas Milionários</h1>", unsafe_allow_html=True)
    st.caption("Acompanhamento de rompimentos de pivot e pullbacks por zona sincronizados com o robô Python na Nuvem")
    st.markdown("<br>", unsafe_allow_html=True)

    df_sinais = carregar_sinais()
    if df_sinais is not None and not df_sinais.empty:
        st.dataframe(df_sinais, use_container_width=True, hide_index=True)
    else:
        st.info("Aguardando os novos sinais do robô na nuvem...")

elif st.session_state.pagina_atual == "relatorios":
    st.markdown("<h1 style='color: #111111;'>Histórico de Relatórios Diários (21h)</h1>", unsafe_allow_html=True)
    st.caption("Central de fechamento operacional gravado de forma automática todas as noites na nuvem")
    st.markdown("<br>", unsafe_allow_html=True)

    df_repor = carregar_relatorios()
    if df_repor is not None and not df_repor.empty:
        datas_disponiveis = df_repor['data_relatorio'].tolist()
        data_selecionada = st.selectbox("📅 Selecione a data do relatório que deseja revisar:", datas_disponiveis)
        
        linha_selecionada = df_repor[df_repor['data_relatorio'] == data_selecionada]
        
        if not linha_selecionada.empty:
            l_longs = linha_selecionada['longs'].values
            l_shorts = linha_selecionada['shorts'].values
            l_total = linha_selecionada['total'].values
            l_detalhes = linha_selecionada['detalhes'].values
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🟩 Sinais LONG", str(l_longs))
            with col2:
                st.metric("🟥 Sinais SHORT", str(l_shorts))
            with col3:
                st.metric("🔢 Total do Dia", str(l_total))
            
            st.markdown("---")
            st.markdown(f"### 📋 Ativos Operados em {data_selecionada}:")
            st.text(str(l_detalhes))
    else:
        st.info("Ainda não há relatórios gravados às 21h na nuvem.")

# Auto-refresh de 10 segundos
time.sleep(10)
st.rerun()
