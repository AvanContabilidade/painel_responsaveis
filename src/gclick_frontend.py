import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image, ImageDraw
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from gclick_scraper import scrape_responsibles
from datetime import datetime

st.set_page_config(page_title="GClick Responsáveis Dashboard", layout="wide")
st.title("GClick Responsáveis Dashboard")

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

def circular_image(img_path, size=(90,90)):
    img = Image.open(img_path).convert("RGBA").resize(size)
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    img.putalpha(mask)
    return img

# Coleta os dados ao abrir a página
with st.spinner("Coletando dados, aguarde..."):
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
            st.success(f"Dados coletados com sucesso! Total de registros: {len(df)}")

            responsaveis = df['Responsável'].unique()
            fotos_dir = os.path.join(os.path.dirname(__file__), 'fotos')

            cols = st.columns(3)
            for idx, responsavel in enumerate(responsaveis):
                sub = df[df['Responsável'] == responsavel]
                counts = sub['Categoria'].value_counts().reindex(['A vencer', 'Concluído', 'Vencida'], fill_value=0)
                values = counts.values
                labels = counts.index.tolist()
                colors = ['#FFD700', '#4CAF50', '#F44336']

                # Gráfico donut
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
                    width=220, height=220
                )

                # Foto circular
                foto_path = os.path.join(fotos_dir, f"{responsavel}.jpg")
                if not os.path.exists(foto_path):
                    foto_path = os.path.join(fotos_dir, f"{responsavel}.png")
                st_img = None
                if os.path.exists(foto_path):
                    st_img = circular_image(foto_path)

                with cols[idx % 3]:
                    st.markdown(f"### {responsavel}")
                    st.plotly_chart(fig)
                    if st_img:
                        st.image(st_img, use_container_width=True)
                    st.markdown(
                        f"""
                        <div style='text-align:center'>
                            <b>A vencer:</b> {counts['A vencer']}<br>
                            <b>Concluído:</b> {counts['Concluído']}<br>
                            <b>Vencida:</b> {counts['Vencida']}
                        </div>
                        """, unsafe_allow_html=True
                    )
        else:
            st.warning("Nenhum dado foi coletado.")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
    finally:
        driver.quit()