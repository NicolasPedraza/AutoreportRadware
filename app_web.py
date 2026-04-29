import streamlit as st
import os
import shutil
from datetime import datetime, timedelta
from main_waf import main_waf
from main_bot import main_bot

# --- Configuración de Estilo y Página ---
st.set_page_config(page_title="Autoreport Radware", page_icon="🌐", layout="centered")

# Simulación de la paleta de colores de Radware vía CSS
st.markdown("""
    <style>
    .main { background-color: #f2f2f2; }
    .stButton>button {
        background-color: #1c5573;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
    }
    h1 { color: #1c5573; }
    </style>
    """, unsafe_allow_html=True)

st.title("AUTOREPORT RADWARE")
st.subheader("Cloud Security Reporting Tool")

# --- Formulario de Entrada ---
with st.container():
    st.markdown("### Configuration")
    
    col1, col2 = st.columns(2)
    with col1:
        domain = st.text_input("🌐 Application (Domain)", placeholder="example.com")
        account_id = st.text_input("🏢 Account ID", placeholder="ID")
    
    with col2:
        x_api_key = st.text_input("🔑 X-API-KEY", type="password", placeholder="Insert your key")
        service = st.selectbox("Service", ["WAF", "BOT"])

    # Rango de fechas
    st.markdown("### Time Range")
    col3, col4 = st.columns(2)
    
    # Lógica de restricción que tenías en actualizar_restriccion_fechas
    dias_max = 30 if service == "WAF" else 7
    fecha_minima = datetime.now() - timedelta(days=dias_max)
    
    with col3:
        start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=1), min_value=fecha_minima)
    with col4:
        end_date = st.date_input("End Date", value=datetime.now())

    only_blocked = st.checkbox("Only Blocked Events", value=True)

# --- Lógica de Ejecución ---
if st.button("Generate Report"):
    if not domain or not x_api_key or not account_id:
        st.error("Please fill in all the required fields.")
    else:
        # Preparar el diccionario de configuración compatible con tus funciones existentes
        config = {
            "domain": domain,
            "x_api_key": x_api_key,
            "account_id": account_id,
            "start": f"{start_date} 00:00:00",
            "end": f"{end_date} 23:59:59",
            "service": service,
            "only_blocked": "y" if only_blocked else "n"
        }

        try:
            with st.spinner(f"Requesting data from Radware API for {domain}..."):
                if service == "WAF":
                    main_waf(config)
                    generated_file = f"{domain}.json"
                else:
                    main_bot(config)
                    generated_file = f"{domain}_bot.json"

            if os.path.exists(generated_file):
                st.success(f"✅ Report Generated Successfully")
                
                # Botón de descarga web
                with open(generated_file, "rb") as f:
                    st.download_button(
                        label="📥 Download JSON Report",
                        data=f,
                        file_name=generated_file,
                        mime="application/json"
                    )
            else:
                st.error("File was not created. Check API logs.")
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.markdown("---")
st.caption("Radware CALA TAM - Nicolas Pedraza")