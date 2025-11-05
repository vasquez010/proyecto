import streamlit as st

# Configuración general
st.set_page_config(
    page_title="🐄 Calculadora Ganadera",
    page_icon="🐄",
    layout="centered"
)

# --- Fondo con imagen y estilo global ---
st.markdown("""
    <style>
    body {
        background: url('https://images.unsplash.com/photo-1500937386664-56c0baf9582b?auto=format&fit=crop&w=1500&q=80') no-repeat center center fixed;
        background-size: cover;
    }
    .main {
        background-color: rgba(255, 255, 255, 0.92);
        padding: 2.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 30px rgba(0,0,0,0.1);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
    }
    .title {
        text-align: center;
        font-size: 2.8em;
        font-weight: bold;
        color: #2E7D32;
        margin-bottom: 0.4em;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2em;
        color: #444;
        margin-bottom: 1.5em;
    }
    .emoji {
        font-size: 3em;
        text-align: center;
        margin-bottom: 10px;
    }
    .card {
        background-color: #ffffffcc;
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .feature {
        font-size: 1.05em;
        color: #333;
    }
    .footer {
        text-align: center;
        font-size: 0.9em;
        color: #777;
        margin-top: 1.5em;
    }
    </style>
""", unsafe_allow_html=True)

# --- Contenedor principal ---
st.markdown("<div class='emoji'>🐄</div>", unsafe_allow_html=True)
st.markdown("<div class='title'>Calculadora Ganadera</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Evalúa tu inversión en ganado y compárala con un CDT</div>", unsafe_allow_html=True)

# --- Sección de descripción ---
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("""
    ### 🌱 ¿Qué puedes hacer aquí?
    - Calcular **ganancias totales y mensuales** de tu inversión ganadera.  
    - Considerar factores como **clima, pastura, topografía y calidad del animal**.  
    - Comparar tus resultados con la rentabilidad de un **CDT bancario tradicional**.  
    - Tomar decisiones **más informadas** sobre tus inversiones agropecuarias.
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Botón principal ---
st.markdown("<br>", unsafe_allow_html=True)
st.success("¡Listo para comenzar tu simulación ganadera! 🚜")

if st.button("👉 Ir a la Calculadora"):
    st.switch_page("pages/home.py")

# --- Pie de página ---
st.markdown(
    "<div class='footer'>"
    "Desarrollado por <b>Osman Vásquez</b> · Proyecto académico 2025 🧠<br>"
    "<span style='font-size:0.85em;'>Universidad / Curso de Programación Aplicada</span>"
    "</div>",
    unsafe_allow_html=True
)