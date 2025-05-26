import time
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image, ImageDraw
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from gclick_scraper import scrape_responsibles
from datetime import datetime
import base64
from io import BytesIO
import streamlit.components.v1 as components
from datetime import datetime, timedelta
import os


cache_file = "dados_cache.parquet"
cache_time_file = "dados_cache_time.txt"
horarios_recoleta = ["10:00", "12:00", "15:00", "01:00"]  

def precisa_recoletar():
    agora = datetime.now()
    if not os.path.exists(cache_time_file):
        return True

    try:
        with open(cache_time_file, "r") as f:
            ultima_execucao = datetime.fromisoformat(f.read().strip())
    except Exception:
        return True  # arquivo corrompido

    for h in horarios_recoleta:
        alvo = datetime.strptime(h, "%H:%M").replace(
            year=agora.year, month=agora.month, day=agora.day
        )
        if alvo <= agora <= alvo + timedelta(minutes=2):  # margem de 2 minutos
            if ultima_execucao < alvo:
                return True
    return False



cache_file = "dados_cache.parquet"


def formatar_data(data_str):
    if not data_str:
        return "Última atualização: ainda não realizada"
    try:
        dt = datetime.fromisoformat(data_str)
        return dt.strftime("Última atualização: %d/%m/%Y às %H:%M")
    except Exception:
        return "Última atualização: inválida"

if os.path.exists(cache_time_file):
    with open(cache_time_file, "r") as f:
        ultima_atualizacao_str = f.read().strip()
else:
    ultima_atualizacao_str = None

msg = formatar_data(ultima_atualizacao_str)

st.markdown(
    f"""
    <div style='
        position:fixed;
        bottom: 10px;
        right: 50px;
        font-size: 14px;
        color: white;
        padding: 6px 12px
        z-index: 9999;
    '>
        {msg}
    </div>
    """,
    unsafe_allow_html=True
)

#recoletar = st.sidebar.button("🔄 Recoletar dados")

#if recoletar:
 #   if os.path.exists(cache_file):
  #     os.remove(cache_file)
  #  st.session_state.clear()
  #  st.rerun()



def status_categoria(row):
    hoje = datetime.now().date()
    try:
        meta_data = pd.to_datetime(row['Meta'], dayfirst=True, errors='coerce').date() if pd.notnull(row['Meta']) else None
    except Exception:
        meta_data = None
    status = row['Status']
    if status in [
        "Concluída após a meta", "Concluída após o prazo", "Concluída na programação", "Concluídas", "Dispensada"
    ]:
        return "Concluído"
    elif meta_data and hoje > meta_data:
        return "Vencida"
    elif meta_data and hoje <= meta_data:
        return "A vencer"
    else:
        return "A vencer"


def circular_image(img_path, size=(300, 300)):
    img = Image.open(img_path).convert("RGBA").resize(size)
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    img.putalpha(mask)
    bg = Image.new("RGBA", size, (0, 0, 0, 0))
    bg.paste(img, (0, 0), img)
    return bg



def image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


if 'df' not in st.session_state or precisa_recoletar():
    if not precisa_recoletar() and os.path.exists(cache_file):
        st.success("✅ Dados carregados do cache.")
        df = pd.read_parquet(cache_file)
        df['Categoria'] = df.apply(status_categoria, axis=1)
        st.session_state.df = df
        st.session_state.responsaveis = df['Responsável'].unique().tolist() if not df.empty else []
        st.session_state.carousel_index = 0
    else:
        with st.spinner("🔄 Recoletando dados automaticamente..."):
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            driver = webdriver.Chrome(options=chrome_options)

            try:
                dados = scrape_responsibles(driver)
                if dados:
                    df = pd.DataFrame(dados, columns=["Meta", "Responsável", "Status"])
                    df['Categoria'] = df.apply(status_categoria, axis=1)
                    df.to_parquet(cache_file, index=False)

                    with open(cache_time_file, "w") as f:
                        f.write(datetime.now().isoformat())

                    st.session_state.df = df
                    st.session_state.responsaveis = df['Responsável'].unique().tolist() if not df.empty else []
                    st.session_state.carousel_index = 0
                else:
                    st.session_state.responsaveis = []
                    st.warning("Nenhum dado foi coletado.")
            except Exception as e:
                st.session_state.responsaveis = []
                st.error(f"Ocorreu um erro: {e}")
            finally:
                driver.quit()



if 'df' in st.session_state:
    df = st.session_state.df
    responsaveis = st.session_state.responsaveis if 'responsaveis' in st.session_state else []
    if not responsaveis:
        st.warning("Nenhum responsável encontrado.")
        st.stop()
    fotos_dir = os.path.join(os.path.dirname(__file__), 'fotos')

    start_idx = st.session_state.carousel_index
    end_idx = start_idx + 3
    if end_idx > len(responsaveis):
        end_idx = len(responsaveis)
        start_idx = max(0, end_idx - 3)

    exibidos = responsaveis[start_idx:end_idx]

    cols = st.columns(3)
    for idx, responsavel in enumerate(exibidos):
        sub = df[df['Responsável'] == responsavel]
        counts = sub['Categoria'].value_counts().reindex(['A vencer', 'Concluído', 'Vencida'], fill_value=0)
        # ... resto do seu código ...
        values = counts.values
        labels = counts.index.tolist()
        colors = ['#FFD700', '#4CAF50', '#F44336']

        # Verifica e carrega a imagem circular do responsável
        foto_path = os.path.join(fotos_dir, f"{responsavel}.jpg")
        if not os.path.exists(foto_path):
            foto_path = os.path.join(fotos_dir, f"{responsavel}.png")

        st_img_base64 = None
        if os.path.exists(foto_path):
            st_img = circular_image(foto_path)
            st_img_base64 = image_to_base64(st_img)

        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.6,
            marker_colors=colors,
            textinfo='none'
        )])
        fig.update_layout(
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
            width=300,
            height=300
        )

        if st_img_base64:
            fig.update_layout(images=[dict(
                source="data:image/png;base64," + st_img_base64,
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                sizex=0.6, sizey=0.6,
                xanchor="center", yanchor="middle",
                layer="above"
            )])

        with cols[idx % 3]:
            with st.container():
                st.markdown(f"""
                    <div style="  
                        border-radius: 16px;
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                        height: 180px;
                        padding: 20px;
                        margin-bottom: 5px;
                        text-align: center;
                    ">
                        <h3 style="margin-bottom: 20px; font-size: 35px; color: white;">{responsavel}</h3>
                """, unsafe_allow_html=True)

                st.plotly_chart(fig, use_container_width=True)

                st.markdown(f"""
                        <div style="margin-top: 20px;margin-bottom: 40; text-align: center;font-size: 30px;">
                            <p style="margin:5px 0; color:#FFD700;"><b>Vincendas:</b> {counts['A vencer']}</p>
                            <p style="margin:5px 0; color:#4CAF50;"><b>Finalizadas:</b> {counts['Concluído']}</p>
                            <p style="margin:5px 0; color:#F44336;"><b>Atrasadas:</b> {counts['Vencida']}</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)





st.markdown("<br>", unsafe_allow_html=True)  # espaço antes dos botões
# Botões de navegação manual


# Inicializa flag na primeira execução
if 'user_navigated' not in st.session_state:
    st.session_state.user_navigated = False

# ⏱️ Lógica do carrossel automático
if not st.session_state.user_navigated:
    time.sleep(30)  # espera 30 segundos
    st.session_state.carousel_index = (st.session_state.carousel_index + 3) % len(responsaveis)
    st.rerun()
else:
    # Após uma navegação manual, reseta a flag para que auto-carrossel continue depois
    st.session_state.user_navigated = False




