import streamlit as st

st.set_page_config(page_title="Cálculo Ganadero", layout="centered")

st.title("🐄 Calculadora Ganadera")
st.markdown("Completa los siguientes parámetros para calcular el valor total de tu producción.")

# --- Parámetros productivos ---
st.header("Parámetros productivos")

dict_topografia = {"Plana": 4, "Ondulada": 3, "Montañoso": 2}
dict_clima = {"Frío (>18°C)": 2, "Templado (18-24°C)": 3, "Calor (<24°C)": 4}
dict_pasturas = {"Braquiaria": 4, "Strella africana": 5, "Sabana": 3}
dict_calidad = {"Cebú puro": 5, "Cebú cruzado": 3, "Criollos fríos": 4, "Cárnicas": 2, "Otros": 2}
dict_suplementacion = {"Sí": 2, "No": 0}

topografia = st.selectbox("Topografía", options=list(dict_topografia.keys()))
clima = st.selectbox("Clima", options=list(dict_clima.keys()))
pasturas = st.selectbox("Tipo de pasturas", options=list(dict_pasturas.keys()))
calidad_animal = st.selectbox("Calidad del animal", options=list(dict_calidad.keys()))
suplementacion = st.radio("¿Hay suplementación?", options=list(dict_suplementacion.keys()))

# --- Parámetros numéricos ---
st.header("Datos económicos y de producción")

precio_kg_inicial = st.number_input(
    "Precio por kg de animal (valor inicial $)", min_value=0.0, value=9000.0, step=500.0
)
peso_animal = st.number_input("Peso del animal (kg)", min_value=0.0, value=200.0, step=10.0)
meses = st.number_input("Cantidad de meses", min_value=1, value=8, step=1)
cantidad_animales = st.number_input("Cantidad de animales", min_value=1, value=20, step=1)

# --- Tabla de precios automáticos (para el valor final) ---
tabla_precios = {
    "Cebú puro":      {"bajo": 11500, "medio": 12000, "alto": 14000},
    "Cebú cruzado":   {"bajo": 10500, "medio": 10000, "alto": 12000},
    "Criollos fríos": {"bajo": 8000,  "medio": 7500,  "alto": 8000},
    "Cárnicas":       {"bajo": 11300, "medio": 11000, "alto": 13000},
    "Otros":          {"bajo": 10000, "medio": 9000,  "alto": 9500},
}

# --- Tasa de mortalidad ---
tasa_mortalidad = 0.05  # 5%

# --- Cálculo ---
if st.button("Calcular valor total"):
    # Puntaje de condiciones productivas
    puntaje_total = (
        dict_topografia[topografia]
        + dict_clima[clima]
        + dict_pasturas[pasturas]
        + dict_calidad[calidad_animal]
        + dict_suplementacion[suplementacion]
    )

    # Peso total final
    kg_total = (puntaje_total * meses) + peso_animal

    # Determinar precio final según peso total
    if kg_total > 350:
        precio_kg_final = tabla_precios[calidad_animal]["alto"]
    elif kg_total > 180:
        precio_kg_final = tabla_precios[calidad_animal]["medio"]
    else:
        precio_kg_final = tabla_precios[calidad_animal]["bajo"]

    # Cálculos
    valor_animal_inicial = peso_animal * precio_kg_inicial
    valor_animal_final = kg_total * precio_kg_final

    # Aplicar mortalidad
    animales_vivos = cantidad_animales * (1 - tasa_mortalidad)
    valor_total = valor_animal_final * animales_vivos
    valor_inicial_lote = valor_animal_inicial * cantidad_animales
    ganancia_total_lote = valor_total - valor_inicial_lote
    ganancia_mensual = ganancia_total_lote / meses

    # Ganancia mensual en %
    ganancia_mensual_pct = (ganancia_mensual / valor_inicial_lote) * 100

    # --- Resultados ---
    st.success("✅ Resultados del cálculo:")
    st.write(f"**Peso total final (kg):** {kg_total:,.2f} kg")
    st.write(f"**Valor inicial por animal:** ${valor_animal_inicial:,.2f}")
    st.write(f"**Valor final por animal:** ${valor_animal_final:,.2f}")
    st.write(f"**Cantidad de animales con tasa de mortalidad del 5%:** {animales_vivos:,.2f}")
    st.write(f"**Valor total del lote (ajustado por mortalidad):** ${valor_total:,.2f}")
    st.write(f"**Ganancia total del lote:** ${ganancia_total_lote:,.2f}")
    st.write(f"**Ganancia mensual promedio:** ${ganancia_mensual:,.2f} por mes")
    st.write(f"**Ganancia mensual promedio (% sobre inversión inicial):** {ganancia_mensual_pct:,.2f}%")

        # --- Comparación con CDT personalizado ---
    st.header("Comparación con CDT")

    cdt_mensual_pct = st.number_input(
        "Ingresa la tasa mensual de tu CDT (%)", min_value=0.0, max_value=10.0, value=0.75, step=0.05
    )

    # Comparación
    if ganancia_mensual_pct > cdt_mensual_pct:
        st.info(f"✅ Esta inversión ganadera es más rentable que un CDT con {cdt_mensual_pct:.2f}% mensual.")
    else:
        st.info(f"⚠️ La inversión ganadera tiene un rendimiento similar o inferior a un CDT con {cdt_mensual_pct:.2f}% mensual.")





