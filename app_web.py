import streamlit as st
import os
from datetime import datetime, timedelta
from main_waf import main_waf
from main_bot import main_bot

# --- Page Configuration ---
st.set_page_config(
    page_title="Radware Autoreport", 
    page_icon="🌐", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS ---
st.markdown("""
    <style>
    /* Background and Font */
    .main { background-color: #f8f9fa; }
    
    /* Image Quality Enhancement */
    img {
        image-rendering: -webkit-optimize-contrast;
        image-rendering: crisp-edges;
    }

    /* Configuration Card Style */
    div.stBlock {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }

    /* MAIN BUTTON (GENERATE JSON) - ULTRA FORCE WHITE TEXT */
    .stButton>button {
        background: linear-gradient(90deg, #1c5573 0%, #2a7da9 100%) !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 2rem !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
    }

    /* Selector específico para el texto dentro del botón */
    .stButton>button, .stButton>button p, .stButton>button div, .stButton>button span {
        color: white !important;
        font-weight: normal !important;
        text-decoration: none !important;
    }
    
    /* Hover state */
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(28, 85, 115, 0.3) !important;
    }

    .stButton>button:hover p, .stButton>button:hover div {
        color: white !important;
    }

    /* Power BI Download Buttons Style (Secondary) */
    div[data-testid="stVerticalBlock"] > div:has(button[kind="secondary"]) button {
        border: 1px solid #f2c811 !important;
        color: #333 !important;
        background-color: #fff !important;
    }
    div[data-testid="stVerticalBlock"] > div:has(button[kind="secondary"]) button:hover {
        background-color: #f2c811 !important;
        color: #000 !important;
    }

    /* Titles and Header text */
    h1 { color: #1c5573; font-weight: 800 !important; margin-bottom: 0px !important; }
    h3 { color: #1c5573; font-size: 1.4rem !important; margin-top: 5px !important; margin-bottom: 0px !important; }
    
    /* Ajuste para pegar los selectores y la fecha al título h3 */
    h3 + div[data-testid="stHorizontalBlock"] {
        margin-top: -25px !important;
    }
    
    /* Eliminar cualquier padding superior interno de las columnas de entrada */
    h3 + div[data-testid="stHorizontalBlock"] div[data-testid="column"] {
        padding-top: 0px !important;
    }

    .stTextInput>div>div>input {
        border-radius: 8px;
    }

    .header-text-container {
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header Section ---
col_logo, col_title = st.columns([1, 4])

with col_logo:
    st.image("logo_radware.png", width=200)

with col_title:
    st.markdown("""
        <div style='padding-top: 28px; margin-left: 80px;' class='header-text-container'>
            <h1>AUTOREPORT</h1>
            <p style='margin-top:-15px; color:gray; font-size:1.1rem;'>Cloud Security Reporting Tool</p>
        </div>
        """, unsafe_allow_html=True)

# --- Configuration Form ---
with st.container():
    st.markdown("### 🛠️ Configuration")
    
    col1, col2 = st.columns(2)
    with col1:
        domain = st.text_input("Application (Domain)", placeholder="example.com")
        account_id = st.text_input("Account ID", placeholder="Enter Account ID")
    
    with col2:
        x_api_key = st.text_input("X-API-KEY", type="password", placeholder="Secret key")
        service = st.selectbox("Security Service", ["WAF", "BOT"])

    st.markdown("---")
    st.markdown("### 📅 Time Range & Filters")
    
    # Configuración de límites de fecha
    dias_max = 30 if service == "WAF" else 7
    fecha_minima = datetime.now() - timedelta(days=dias_max)
    
    # Generar listas de opciones para los selectbox
    lista_horas = [f"{i:02d}" for i in range(24)]
    lista_minutos = [f"{i:02d}" for i in range(60)]
    
    # --- RANGO DE INICIO ---
    st.markdown("### 🛫 Start")
    col_s_date, col_s_hour, col_s_min = st.columns([2, 1, 1])
    with col_s_date:
        # Se activa la visibilidad del label y se cambia el texto a "Date"
        start_date = st.date_input("Date", value=datetime.now() - timedelta(days=1), min_value=fecha_minima, label_visibility="visible")
    with col_s_hour:
        start_hour = st.selectbox("Hour", options=lista_horas, index=0, key="start_hour")
    with col_s_min:
        start_min = st.selectbox("Minute", options=lista_minutos, index=0, key="start_min")
        
    # Salto de línea controlado para separar Start de End
    st.markdown("<br>", unsafe_allow_html=True)
        
    # --- RANGO DE FIN ---
    st.markdown("### 🛬 End")
    col_e_date, col_e_hour, col_e_min = st.columns([2, 1, 1])
    with col_e_date:
        # Se activa la visibilidad del label y se cambia el texto a "Date"
        end_date = st.date_input("Date", value=datetime.now(), label_visibility="visible")
    with col_e_hour:
        end_hour = st.selectbox("Hour", options=lista_horas, index=23, key="end_hour")
    with col_e_min:
        end_min = st.selectbox("Minute", options=lista_minutos, index=59, key="end_min")

    st.markdown("<br>", unsafe_allow_html=True)
    only_blocked = st.toggle("Only Blocked Events", value=True)


# --- Execution Logic ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button("GENERATE JSON", use_container_width=True):
    if not domain or not x_api_key or not account_id:
        st.warning("⚠️ Please fill in all the required fields before proceeding.")
    else:
        # Construimos el formato string uniendo la fecha, hora y minutos seleccionados
        start_timestamp = f"{start_date} {start_hour}:{start_min}:00"
        end_timestamp = f"{end_date} {end_hour}:{end_min}:59"

        config = {
            "domain": domain,
            "x_api_key": x_api_key,
            "account_id": account_id,
            "start": start_timestamp,
            "end": end_timestamp,
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
                st.error("❌ File was not created. Please check API logs and connectivity.")
                
        except Exception as e:
            st.error(f"❌ Critical Error: {str(e)}")


# --- Power BI Download Section ---
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("📊 Download Power BI Dashboards", expanded=False):
    st.info("Download these templates to visualize the JSON data generated by this tool.")
    
    # --- Fila 1: Dashboards Generales ---
    st.markdown("#### 📈 Executive & General Dashboards")
    pbi_col1, pbi_col2 = st.columns(2)
    
    pbi_waf_file = "CWAAP_AutoReport.pbit"
    pbi_bot_file = "BOTM_AutoReport.pbit"

    with pbi_col1:
        if os.path.exists(pbi_waf_file):
            with open(pbi_waf_file, "rb") as f:
                st.download_button(
                    label="📊 Download Report WAF",
                    data=f,
                    file_name="Radware_WAF_Dashboard.pbit",
                    mime="application/octet-stream",
                    use_container_width=True
                )
        else:
            st.caption("⚠️ WAF Executive template file not found")

    with pbi_col2:
        if os.path.exists(pbi_bot_file):
            with open(pbi_bot_file, "rb") as f:
                st.download_button(
                    label="🤖 Download Report BOT",
                    data=f,
                    file_name="Radware_BOT_Dashboard.pbit",
                    mime="application/octet-stream",
                    use_container_width=True
                )
        else:
            st.caption("⚠️ BOT Executive template file not found")
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- Fila 2: Dashboards de Análisis de Eventos ---
    st.markdown("#### 🔍 Deep-Dive Event Analysis")
    pbi_col3, pbi_col4 = st.columns(2)
    
    pbi_waf_analysis_file = "CWAAP_Event_Analysis.pbit"
    pbi_bot_analysis_file = "BOTM_Event_Analysis.pbit"
    
    with pbi_col3:
        if os.path.exists(pbi_waf_analysis_file):
            with open(pbi_waf_analysis_file, "rb") as f:
                st.download_button(
                    label="🔬 Download WAF Event Analysis",
                    data=f,
                    file_name="Radware_WAF_Event_Analysis.pbit",
                    mime="application/octet-stream",
                    use_container_width=True
                )
        else:
            st.caption("⚠️ WAF Event Analysis template file not found")

    with pbi_col4:
        if os.path.exists(pbi_bot_analysis_file):
            with open(pbi_bot_analysis_file, "rb") as f:
                st.download_button(
                    label="🧠 Download BOT Event Analysis",
                    data=f,
                    file_name="Radware_BOT_Event_Analysis.pbit",
                    mime="application/octet-stream",
                    use_container_width=True
                )
        else:
            st.caption("⚠️ BOT Event Analysis template file not found")

# --- Footer ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
footer_col1, footer_col2 = st.columns([3,1])
with footer_col1:
    st.caption("© 2026 Radware CALA TAM - Technical Internal Tool")
with footer_col2:
    st.caption(f"Author | **Nicolas Pedraza**")
