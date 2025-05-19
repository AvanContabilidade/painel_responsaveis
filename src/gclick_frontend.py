import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from gclick_scraper import scrape_responsibles

st.set_page_config(page_title="GClick Responsáveis Scraper", layout="wide")

st.title("GClick Responsáveis Scraper")
st.write("Clique no botão abaixo para coletar os dados dos responsáveis do GClick.")

if st.button("Coletar Dados"):
    with st.spinner("Coletando dados, aguarde..."):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options=chrome_options)
        try:
            dados = scrape_responsibles(driver)
            if dados:
                df = pd.DataFrame(dados, columns=["Meta", "Responsável"])
                st.success(f"Dados coletados com sucesso! Total de registros: {len(df)}")
                st.dataframe(df, use_container_width=True)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Baixar CSV",
                    data=csv,
                    file_name="responsaveis_gclick.csv",
                    mime="text/csv"
                )
            else:
                st.warning("Nenhum dado foi coletado.")
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")
        finally:
            driver.quit()
else:
    st.info("Aguardando ação do usuário.")