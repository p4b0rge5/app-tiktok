import streamlit as st
import pandas as pd
import numpy as np

# A configuração da página DEVE ser o primeiro comando
st.set_page_config(page_title="TikTok Shop Analytics", layout="wide")

# --- SISTEMA DE LOGIN (PAYWALL) ---
def verificar_senha():
    """Retorna True se o usuário estiver logado com sucesso"""
    def checar_credenciais():
        # Verifica se o email existe no nosso "cofre" e se a senha bate
        email = st.session_state["email"]
        senha = st.session_state["senha"]
        
        if email in st.secrets["clientes"] and senha == st.secrets["clientes"][email]:
            st.session_state["logado"] = True
            del st.session_state["senha"] # Apaga a senha da memória por segurança
        else:
            st.session_state["logado"] = False

    if "logado" not in st.session_state:
        st.title("🔒 Acesso Restrito")
        st.markdown("Faça login para analisar suas vendas do TikTok Shop.")
        st.text_input("Email", key="email")
        st.text_input("Senha", type="password", key="senha")
        st.button("Entrar", on_click=checar_credenciais)
        return False
    
    elif not st.session_state["logado"]:
        st.title("🔒 Acesso Restrito")
        st.text_input("Email", key="email")
        st.text_input("Senha", type="password", key="senha")
        st.button("Entrar", on_click=checar_credenciais)
        st.error("Email ou senha incorretos. Verifique sua assinatura.")
        return False
    
    return True

# Se o usuário não passou no login, o aplicativo para aqui.
if not verificar_senha():
    st.stop()

# --- APLICATIVO PRINCIPAL ---
st.sidebar.success(f"👤 Logado como: {st.session_state['email']}")
st.sidebar.markdown("---")

st.title("📊 Painel de Conversão: TikTok Shop")
st.markdown("Transforme visualizações em inteligência de vendas.")

# Função para simular o CSV padrão do TikTok (Para demonstração)
def gerar_dados_simulados():
    np.random.seed(42)
    datas = pd.date_range(end=pd.Timestamp.today(), periods=15)
    dados = {
        "Data da Publicação": datas,
        "Título do Vídeo": [f"Vídeo {i} - Demonstração" if i%3==0 else f"Vídeo {i} - Trend" for i in range(1, 16)],
        "Visualizações": np.random.randint(5000, 250000, 15),
        "Retenção 3s (%)": np.random.uniform(15.0, 65.0, 15),
        "Cliques no Link": np.random.randint(50, 5000, 15),
        "Vendas": np.random.randint(5, 150, 15),
        "Faturamento Bruto (R$)": np.random.uniform(500, 15000, 15)
    }
    df = pd.DataFrame(dados)
    return df

st.sidebar.header("Carregar Relatório")
arquivo_csv = st.sidebar.file_uploader("Suba o CSV do TikTok", type=["csv"])

if arquivo_csv is not None:
    df = pd.read_csv(arquivo_csv)
    st.sidebar.success("Arquivo carregado!")
else:
    df = gerar_dados_simulados()
    st.sidebar.info("Exibindo dados de demonstração.")

st.subheader("Visão Geral da Loja")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Visualizações", f"{df['Visualizações'].sum():,.0f}".replace(',', '.'))
col2.metric("Faturamento", f"R$ {df['Faturamento Bruto (R$)'].sum():,.2f}".replace(',', '.').replace('.', ',', 1))
col3.metric("Retenção (3s)", f"{df['Retenção 3s (%)'].mean():.1f}%")
col4.metric("Vendas", f"{df['Vendas'].sum()}")

st.divider()

st.subheader("O que faz você vender mais?")
st.scatter_chart(data=df, x="Retenção 3s (%)", y="Faturamento Bruto (R$)", size="Visualizações", color="#00f2fe")
