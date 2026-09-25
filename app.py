import streamlit as st
import pandas as pd
import numpy as np

# Configuração inicial da página
st.set_page_config(page_title="TikTok Shop Analytics", layout="wide")

st.title("📊 Painel de Conversão: TikTok Shop")
st.markdown("Transforme visualizações em inteligência de vendas.")

# Função para simular o CSV padrão do TikTok
def gerar_dados_simulados():
    np.random.seed(42) # Mantém os dados iguais a cada atualização
    datas = pd.date_range(end=pd.Timestamp.today(), periods=15)
    
    dados = {
        "Data da Publicação": datas,
        "Título do Vídeo": [f"Vídeo {i} - Demonstração Produto" if i%3==0 else f"Vídeo {i} - Trend" for i in range(1, 16)],
        "Visualizações": np.random.randint(5000, 250000, 15),
        "Retenção 3s (%)": np.random.uniform(15.0, 65.0, 15),
        "Cliques no Link": np.random.randint(50, 5000, 15),
        "Vendas": np.random.randint(5, 150, 15),
        "Faturamento Bruto (R$)": np.random.uniform(500, 15000, 15)
    }
    df = pd.DataFrame(dados)
    # Calculando a taxa de conversão (Vendas / Cliques)
    df["Conversão de Clique (%)"] = (df["Vendas"] / df["Cliques no Link"]) * 100
    return df

# Barra lateral para upload
st.sidebar.header("Carregar Relatório")
arquivo_csv = st.sidebar.file_uploader("Suba o CSV do TikTok", type=["csv"])

# Lógica de carregamento de dados
if arquivo_csv is not None:
    # Quando você tiver o CSV real, ele vai ler aqui
    df = pd.read_csv(arquivo_csv)
    st.sidebar.success("Arquivo carregado com sucesso!")
else:
    # Se não tem arquivo, usa os dados simulados
    df = gerar_dados_simulados()
    st.sidebar.info("Exibindo dados de demonstração.")

# --- INÍCIO DO PAINEL VISUAL ---

st.subheader("Visão Geral da Loja")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total de Visualizações", f"{df['Visualizações'].sum():,.0f}".replace(',', '.'))
col2.metric("Faturamento Total", f"R$ {df['Faturamento Bruto (R$)'].sum():,.2f}".replace(',', '.').replace('.', ',', 1))
col3.metric("Média de Retenção (3s)", f"{df['Retenção 3s (%)'].mean():.1f}%")
col4.metric("Total de Vendas", f"{df['Vendas'].sum()}")

st.divider()

# Gráfico 1: Relação entre Retenção e Faturamento
st.subheader("O que faz você vender mais?")
st.markdown("Veja a relação entre a retenção nos primeiros 3 segundos e o faturamento do vídeo.")
st.scatter_chart(
    data=df,
    x="Retenção 3s (%)",
    y="Faturamento Bruto (R$)",
    size="Visualizações",
    color="#00f2fe" # Cor azul ciano estilo TikTok
)

st.divider()

# Tabela dos Top Vídeos
st.subheader("Top 5 Vídeos em Vendas")
top_videos = df.sort_values(by="Faturamento Bruto (R$)", ascending=False).head(5)
st.dataframe(
    top_videos[["Data da Publicação", "Título do Vídeo", "Visualizações", "Retenção 3s (%)", "Vendas", "Faturamento Bruto (R$)"]],
    use_container_width=True,
    hide_index=True
)