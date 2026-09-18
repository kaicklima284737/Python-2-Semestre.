import streamlit as st
import pandas as pd
import plotly.express as px
from pymongo import MongoClient
from bson.decimal128 import Decimal128

# 1. Configuração Visual da Página
st.set_page_config(
    page_title="Executive Dashboard | Gestão de Usuários",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS para ajustar espaçamentos
st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    </style>
""", unsafe_allow_html=True)


# 2. Conexão Segura com o MongoDB
@st.cache_resource
def get_db_client():
    try:
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        return client
    except Exception as e:
        st.error(f"⚠️ Erro ao conectar ao MongoDB: {e}")
        return None


client = get_db_client()


# 3. Carregamento e Tratamento Avançado de Dados
@st.cache_data(ttl=60)
def load_data():
    if not client:
        return pd.DataFrame()

    db = client["meu_banco"]
    collection = db["usuarios"]
    dados = list(collection.find({}, {"_id": 0}))

    if not dados:
        return pd.DataFrame()

    df = pd.DataFrame(dados)

    # Tratamento da coluna 'saldo R$'
    if "saldo R$" in df.columns:
        def parse_saldo(val):
            if isinstance(val, Decimal128):
                return float(val.to_decimal())
            try:
                clean_str = str(val).replace("R$", "").replace(" ", "").replace(",", ".").strip()
                return float(clean_str)
            except (ValueError, TypeError):
                return 0.0

        df["saldo"] = df["saldo R$"].apply(parse_saldo)
    else:
        df["saldo"] = 0.0

    # Garantia de colunas obrigatórias
    if "status" not in df.columns:
        df["status"] = "Não Definido"
    if "idade" not in df.columns:
        df["idade"] = 0
    if "nome" not in df.columns:
        df["nome"] = "Usuário Sem Nome"

    # Classificação Financeira
    df["situacao_financeira"] = df["saldo"].apply(
        lambda x: "Credor (Positivo)" if x >= 0 else "Devedor (Negativo)"
    )

    return df


df_raw = load_data()

if df_raw.empty:
    st.info(
        "ℹ️ Nenhum dado encontrado no MongoDB. Certifique-se de que a coleção 'usuarios' no banco 'meu_banco' possui documentos.")
    st.stop()

# 4. Barra Lateral - Filtros Dinâmicos
with st.sidebar:
    st.title("⚙️ Painel de Controle")
    st.markdown("---")

    # Filtro de Busca por Nome
    busca_nome = st.text_input("🔍 Buscar por Nome:", value="")

    # Filtro de Status
    status_lista = sorted(df_raw["status"].unique().tolist())
    status_sel = st.multiselect("🏷️ Status do Usuário:", options=status_lista, default=status_lista)

    # Filtro de Faixa Etária
    min_i, max_i = int(df_raw["idade"].min()), int(df_raw["idade"].max())
    idade_sel = st.slider("🎂 Faixa Etária:", min_value=min_i, max_value=max_i, value=(min_i, max_i))

    # Filtro de Situação Financeira
    situacao_sel = st.multiselect(
        "💳 Situação Financeira:",
        options=["Credor (Positivo)", "Devedor (Negativo)"],
        default=["Credor (Positivo)", "Devedor (Negativo)"]
    )

    st.markdown("---")
    st.caption("🟢 Conectado ao MongoDB | `meu_banco.usuarios`")

# Aplicação dos Filtros
df = df_raw.copy()

if busca_nome:
    df = df[df["nome"].str.contains(busca_nome, case=False, na=False)]

df = df[
    (df["status"].isin(status_sel)) &
    (df["idade"].between(idade_sel[0], idade_sel[1])) &
    (df["situacao_financeira"].isin(situacao_sel))
    ]

# Cabecalho do Dashboard
st.title("📈 Dashboard Executivo de Gestão de Usuários")
st.markdown("Análise consolidada de métricas demográficas, patrimoniais e comportamentais da base.")

if df.empty:
    st.warning("⚠️ Nenhum registro encontrado para os filtros selecionados.")
    st.stop()

# 5. Cartões de KPIs Estratégicos
st.subheader("📌 Indicadores-Chave (KPIs)")
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

total_usuarios = len(df)
saldo_total = df["saldo"].sum()
saldo_medio = df["saldo"].mean()
devedores = len(df[df["saldo"] < 0])
pct_devedores = (devedores / total_usuarios * 100) if total_usuarios > 0 else 0

with kpi1:
    st.metric("Total de Usuários", f"{total_usuarios:,}")

with kpi2:
    st.metric("Patrimônio Total", f"R$ {saldo_total:,.2f}")

with kpi3:
    st.metric("Saldo Médio", f"R$ {saldo_medio:,.2f}")

with kpi4:
    st.metric("Contas Devedoras", f"{devedores}", delta=f"{pct_devedores:.1f}% da base", delta_color="inverse")

with kpi5:
    st.metric("Média de Idade", f"{df['idade'].mean():.1f} anos")

st.markdown("---")

# 6. Estrutura em Abas
tab1, tab2, tab3 = st.tabs(["📊 Visão Financeira", "👥 Análise Demográfica", "📁 Gestão de Dados"])

# ABA 1: VISÃO FINANCEIRA
with tab1:
    col_a, col_b = st.columns(2)

    with col_a:
        with st.container(border=True):
            st.markdown("#### Distribuição de Saldo por Status (Boxplot)")
            fig_box = px.box(
                df,
                x="status",
                y="saldo",
                color="status",
                points="outliers",
                template="plotly_white",
                labels={"saldo": "Saldo (R$)", "status": "Status"},
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            fig_box.update_layout(showlegend=False, height=380)
            st.plotly_chart(fig_box, use_container_width=True)

    with col_b:
        with st.container(border=True):
            st.markdown("#### Top 10 Maiores Saldos")
            top10 = df.nlargest(10, "saldo")
            fig_top = px.bar(
                top10,
                x="saldo",
                y="nome",
                orientation="h",
                text_auto=".2s",
                template="plotly_white",
                color="saldo",
                color_continuous_scale="Viridis",
                labels={"saldo": "Saldo (R$)", "nome": "Usuário"}
            )
            fig_top.update_layout(yaxis={'categoryorder': 'total ascending'}, height=380, coloraxis_showscale=False)
            st.plotly_chart(fig_top, use_container_width=True)

# ABA 2: ANÁLISE DEMOGRÁFICA
with tab2:
    col_c, col_d = st.columns(2)

    with col_c:
        with st.container(border=True):
            st.markdown("#### Proporção da Base por Status")
            df_status_count = df["status"].value_counts().reset_index()
            df_status_count.columns = ["status", "quantidade"]

            fig_pie = px.pie(
                df_status_count,
                names="status",
                values="quantidade",
                hole=0.45,
                template="plotly_white",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(height=380)
            st.plotly_chart(fig_pie, use_container_width=True)

    with col_d:
        with st.container(border=True):
            st.markdown("#### Dispersão: Idade vs. Saldo")
            fig_scatter = px.scatter(
                df,
                x="idade",
                y="saldo",
                color="status",
                size=df["saldo"].abs() + 1000,  # Ajusta tamanho dos pontos
                hover_name="nome",
                template="plotly_white",
                labels={"idade": "Idade (Anos)", "saldo": "Saldo (R$)"}
            )
            fig_scatter.update_layout(height=380)
            st.plotly_chart(fig_scatter, use_container_width=True)

# ABA 3: GESTÃO DE DADOS
with tab3:
    st.markdown("#### 📋 Base de Dados Filtrada")

    df_display = df.drop(columns=["situacao_financeira"], errors="ignore")
    st.dataframe(df_display, use_container_width=True, height=350)

    # Exportação em CSV
    csv_data = df_display.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Exportar Relatório (CSV)",
        data=csv_data,
        file_name="relatorio_usuarios_mongodb.csv",
        mime="text/csv"
    )