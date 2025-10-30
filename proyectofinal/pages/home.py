import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="🐄 Calculadora Ganadera", layout="centered")

st.title("🐄 Calculadora Ganadera")
st.markdown(
    "Completa los parámetros y obtén la **ganancia estimada de tu inversión ganadera**. "
    "También podrás compararla con un CDT mensual usando la misma inversión inicial."
)

# --- Parámetros productivos ---
st.header("Parámetros productivos")
dict_topografia = {"Plana": 4, "Ondulada": 3, "Montañoso": 2}
dict_clima = {"Frío (>18°C)": 2, "Templado (18-24°C)": 3, "Calor (<24°C)": 4}
dict_pasturas = {"Braquiaria": 4, "Strella africana": 5, "Sabana": 3}
dict_calidad = {"Cebú puro": 5, "Cebú cruzado": 3, "Criollos fríos": 4, "Cárnicas": 2, "Otros": 2}
dict_suplementacion = {"Sí": 2, "No": 0}

col1, col2 = st.columns(2)
with col1:
    topografia = st.selectbox("Topografía", options=list(dict_topografia.keys()))
    clima = st.selectbox("Clima", options=list(dict_clima.keys()))
    pasturas = st.selectbox("Tipo de pasturas", options=list(dict_pasturas.keys()))
with col2:
    calidad_animal = st.selectbox("Calidad del animal", options=list(dict_calidad.keys()))
    suplementacion = st.radio("¿Hay suplementación?", options=list(dict_suplementacion.keys()))

# --- Parámetros económicos ---
st.header("Datos económicos y de producción")
col1, col2 = st.columns(2)
with col1:
    precio_kg_inicial = st.number_input(
        "Precio por kg de animal ($)", min_value=0.0, value=9000.0, step=500.0
    )
    peso_animal = st.number_input("Peso del animal (kg)", min_value=0.0, value=200.0, step=10.0)
with col2:
    meses = st.number_input("Cantidad de meses", min_value=1, value=8, step=1)
    cantidad_animales = st.number_input("Cantidad de animales", min_value=1, value=20, step=1)

# --- Tabla de precios automáticos ---
tabla_precios = {
    "Cebú puro":      {"bajo": 11500, "medio": 12000, "alto": 14000},
    "Cebú cruzado":   {"bajo": 10500, "medio": 10000, "alto": 12000},
    "Criollos fríos": {"bajo": 8000,  "medio": 7500,  "alto": 8000},
    "Cárnicas":       {"bajo": 11300, "medio": 11000, "alto": 13000},
    "Otros":          {"bajo": 10000, "medio": 9000,  "alto": 9500},
}

# --- Tasa de mortalidad ---
tasa_mortalidad = 0.05

# --- Comparación con CDT ---
st.header("Comparación con CDT")
cdt_mensual_pct = st.slider(
    "Tasa mensual de tu CDT (%)", min_value=0.0, max_value=10.0, value=0.75, step=0.05
)

# --- Cálculo ---
if st.button("Calcular valor total"):

    # --- Puntaje y peso final ---
    puntaje_total = (
        dict_topografia[topografia]
        + dict_clima[clima]
        + dict_pasturas[pasturas]
        + dict_calidad[calidad_animal]
        + dict_suplementacion[suplementacion]
    )
    kg_total = (puntaje_total * meses) + peso_animal

    # --- Precio final según peso ---
    if kg_total > 350:
        precio_kg_final = tabla_precios[calidad_animal]["alto"]
    elif kg_total > 180:
        precio_kg_final = tabla_precios[calidad_animal]["medio"]
    else:
        precio_kg_final = tabla_precios[calidad_animal]["bajo"]

    # --- Valores iniciales y finales ---
    valor_animal_inicial = peso_animal * precio_kg_inicial
    valor_animal_final = kg_total * precio_kg_final
    animales_vivos = cantidad_animales * (1 - tasa_mortalidad)
    valor_total = valor_animal_final * animales_vivos
    valor_inicial_lote = valor_animal_inicial * cantidad_animales
    ganancia_total_lote = valor_total - valor_inicial_lote
    ganancia_mensual = ganancia_total_lote / meses
    ganancia_mensual_pct = (ganancia_mensual / valor_inicial_lote) * 100

    # --- Ganancia CDT ---
    ganancia_cdt_mensual = valor_inicial_lote * (cdt_mensual_pct / 100)
    ganancia_cdt_total = ganancia_cdt_mensual * meses

    # --- Mostrar datos ganaderos originales ---
    st.subheader("🐄 Datos Ganaderos")
    st.write(f"- Peso inicial por animal: {peso_animal:,.2f} kg")
    st.write(f"- Precio inicial por animal: ${valor_animal_inicial:,.2f}")
    st.write(f"- Cantidad de animales: {cantidad_animales}")
    st.write(f"- Puntaje de condiciones productivas: {puntaje_total}")
    st.write(f"- Peso final por animal: {kg_total:,.2f} kg")
    st.write(f"- Precio final por animal según calidad y peso: ${precio_kg_final:,.2f}")
    st.write(f"- Animales vivos tras mortalidad (5%): {animales_vivos:,.2f}")
    st.write(f"- Valor total del lote ajustado por mortalidad: ${valor_total:,.2f}")
    st.write(f"- Ganancia total del lote: ${ganancia_total_lote:,.2f}")
    st.write(f"- Ganancia mensual promedio: ${ganancia_mensual:,.2f} ({ganancia_mensual_pct:.2f}%)")

    # --- Tabla comparativa ---
    data = {
        "Concepto": [
            "Ganancia mensual ($)",
            "Ganancia total ($)",
            "Ganancia mensual (%)"
        ],
        "Inversión Ganadera": [
            ganancia_mensual,
            ganancia_total_lote,
            ganancia_mensual_pct
        ],
        f"CDT ({cdt_mensual_pct:.2f}% mensual)": [
            ganancia_cdt_mensual,
            ganancia_cdt_total,
            cdt_mensual_pct
        ]
    }
    df_comparacion = pd.DataFrame(data)
    st.subheader("📊 Comparación Ganancia Ganadera vs CDT")
    st.dataframe(df_comparacion.style.format({
        "Inversión Ganadera": "${:,.2f}", 
        f"CDT ({cdt_mensual_pct:.2f}% mensual)": "${:,.2f}"
    }))

    # --- Gráfica ---
    labels = ["Ganancia Ganadera", "Ganancia CDT"]
    values = [ganancia_mensual, ganancia_cdt_mensual]

    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(7,4))
    bars = ax.bar(labels, values, color=sns.color_palette("Set2", 2))
    ax.set_ylabel("Ganancia mensual ($)")
    ax.set_title("Comparación Ganancia Mensual: Ganadera vs CDT", fontsize=14)

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 0.01*max(values), f"${yval:,.2f}", ha='center', fontsize=11)

    st.pyplot(fig)

    # --- Mensaje de rentabilidad ---
    if ganancia_mensual > ganancia_cdt_mensual:
        st.success(f"✅ La inversión ganadera genera más dinero que un CDT con {cdt_mensual_pct:.2f}% mensual.")
    else:
        st.warning(f"⚠️ La inversión ganadera genera igual o menos dinero que un CDT con {cdt_mensual_pct:.2f}% mensual.")

    st.info(
        "El precio inicial por kg fue ingresado manualmente, "
        "y el precio final se determinó automáticamente según el peso final y la calidad del animal."
    )



