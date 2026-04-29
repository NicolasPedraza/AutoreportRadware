import streamlit as st
import os
from datetime import datetime, timedelta
from main_waf import main_waf
from main_bot import main_bot

# --- Configuración de Estilo y Página ---
st.set_page_config(
    page_title="Autoreport Radware", 
    page_icon="🌐", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS Personalizado ---
st.markdown("""
    <style>
    /* Fondo y fuente */
    .main { background-color: #f8f9fa; }
    
    /* MEJORA DE CALIDAD DE IMAGEN: Evita el suavizado borroso */
    img {
        image-rendering: -webkit-optimize-contrast;
        image-rendering: crisp-edges;
    }

    /* Estilo para el contenedor de configuración (Cards) */
    div.stBlock {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }

    /* Botón principal */
    .stButton>button {
        background: linear-gradient(90deg, #1c5573 0%, #2a7da9 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(28, 85, 115, 0.3);
        color: white;
    }

    /* Títulos */
    h1 { color: #1c5573; font-weight: 800 !important; margin-bottom: 0px !important; }
    h3 { color: #495057; font-size: 1.2rem !important; margin-top: 0px !important; margin-bottom: 1rem !important; }
    
    /* Inputs */
    .stTextInput>div>div>input {
        border-radius: 8px;
    }

    /* Contenedor del encabezado - Sin márgenes negativos para evitar amontonamiento */
    .header-text-container {
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Encabezado con Logo y Título (Máximo Espaciado) ---
col_logo, col_title = st.columns([1, 4])

with col_logo:
    st.image("logo_radware.png", width=200)

with col_title:
    # 'margin-left: 80px' empuja el título considerablemente a la derecha
    st.markdown("""
        <div style='padding-top: 28px; margin-left: 80px;' class='header-text-container'>
            <h1>AUTOREPORT</h1>
            <p style='margin-top:-15px; color:gray; font-size:1.1rem;'>Cloud Security Reporting Tool</p>
        </div>
        """, unsafe_allow_html=True)

# --- Formulario de Entrada ---
with st.container():
    st.markdown("### 🛠️ Configuration")
    
    col1, col2 = st.columns(2)
    with col1:
        domain = st.text_input("Application (Domain)", placeholder="example.com")
        account_id = st.text_input("Account ID", placeholder="Enter Account ID")
    
    with col2:
        x_api_key = st.text_input("X-API-KEY", type="password", placeholder="Paste secret key")
        service = st.selectbox("Security Service", ["WAF", "BOT"])

    st.markdown("---")
    st.markdown("### 📅 Time Range & Filters")
    
    col3, col4 = st.columns(2)
    dias_max = 30 if service == "WAF" else 7
    fecha_minima = datetime.now() - timedelta(days=dias_max)
    
    with col3:
        start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=1), min_value=fecha_minima)
    with col4:
        end_date = st.date_input("End Date", value=datetime.now())

    only_blocked = st.toggle("Only Blocked Events", value=True)

# --- Lógica de Ejecución ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button("GENERATE JSON"):
    if not domain or not x_api_key or not account_id:
        st.warning("⚠️ Please fill in all the required fields before proceeding.")
    else:
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
            with st.spinner(f"Connecting to Radware Cloud for {domain}..."):
                if service == "WAF":
                    main_waf(config)
                    generated_file = f"{domain}.json"
                else:
                    main_bot(config)
                    generated_file = f"{domain}_bot.json"

            if os.path.exists(generated_file):
                st.balloons()
                st.success(f"✨ Report for {domain} is ready!")
                
                with open(generated_file, "rb") as f:
                    st.download_button(
                        label="⬇️ Download JSON Report",
                        data=f,
                        file_name=generated_file,
                        mime="application/json"
                    )
            else:
                st.error("❌ File was not created. Please check the API logs and connectivity.")
                
        except Exception as e:
            st.error(f"❌ Critical Error: {str(e)}")

# --- Footer ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
footer_col1, footer_col2 = st.columns([3,1])
with footer_col1:
    st.caption("© 2026 Radware CALA TAM - Technical Internal Tool")
with footer_col2:
    st.caption(f"Author | **Nicolas Pedraza**")
