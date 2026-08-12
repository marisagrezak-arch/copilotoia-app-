"""
CopilotoIA (Promptify) — Prototipo interactivo en Streamlit
Educá a profesionales para pasar de "chatear" a "delegar" con IA,
siguiendo la metodología de Coderhouse.

Ejecutar con: streamlit run copilotoia_app.py
"""

import streamlit as st

# ─────────────────────────────────────────────────────────────────
# CONFIGURACIÓN GENERAL DE LA PÁGINA
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CopilotoIA · De chatear a delegar",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────
# ESTILOS — Paleta tech: naranjas vibrantes + oscuros
# ─────────────────────────────────────────────────────────────────
CUSTOM_CSS = """
<style>
:root {
    --naranja: #FF6B35;
    --naranja-suave: #FF8C5A;
    --oscuro: #0E1117;
    --oscuro-panel: #1A1D24;
    --texto-claro: #F5F5F5;
}

.stApp {
    background-color: var(--oscuro);
}

h1, h2, h3 {
    color: var(--texto-claro) !important;
}

section[data-testid="stSidebar"] {
    background-color: var(--oscuro-panel);
    border-right: 2px solid var(--naranja);
}

div[data-testid="stExpander"] {
    background-color: var(--oscuro-panel);
    border: 1px solid #2A2E38;
    border-radius: 10px;
}

.hero-box {
    background: linear-gradient(135deg, var(--naranja) 0%, #C1441E 100%);
    padding: 1.6rem 2rem;
    border-radius: 14px;
    color: white;
    margin-bottom: 1.5rem;
}

.golden-rule {
    background-color: var(--oscuro-panel);
    border-left: 4px solid var(--naranja);
    padding: 0.9rem 1.2rem;
    border-radius: 8px;
    margin-bottom: 0.7rem;
}

.model-card {
    background-color: var(--oscuro-panel);
    border: 1px solid #2A2E38;
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 1rem;
}

.badge {
    display: inline-block;
    background-color: var(--naranja);
    color: white;
    padding: 0.15rem 0.6rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    margin-bottom: 0.4rem;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# DATOS BASE
# ─────────────────────────────────────────────────────────────────
ROLES = {
    "Growth Marketer": {
        "emoji": "📈",
        "bienvenida": (
            "Bienvenido/a, crack del Growth. Acá vas a aprender a convertir "
            "a la IA en tu copiloto para hipótesis, funnels y experimentos "
            "que realmente muevan la aguja."
        ),
        "roleplay": (
            "Sos un Growth Marketer experto con años de experiencia en "
            "adquisición, retención y optimización de funnels de conversión..."
        ),
    },
    "Product Manager": {
        "emoji": "🧭",
        "bienvenida": (
            "Bienvenido/a, PM. Vamos a afinar cómo delegás research, specs "
            "y priorización a la IA sin perder el control de la decisión final."
        ),
        "roleplay": (
            "Sos un Product Manager senior con experiencia en discovery, "
            "priorización y definición de producto..."
        ),
    },
    "Copywriter": {
        "emoji": "✍️",
        "bienvenida": (
            "Bienvenido/a, pluma afilada. Acá la IA va a ser tu sparring "
            "para generar copies que conviertan de verdad, sin sonar genéricos."
        ),
        "roleplay": (
            "Sos un Copywriter experto con años de experiencia en conversión..."
        ),
    },
    "Programador": {
        "emoji": "💻",
        "bienvenida": (
            "Bienvenido/a, dev. Vamos a exprimir la IA para refactor, "
            "debugging y documentación, sin delegar el criterio técnico."
        ),
        "roleplay": (
            "Sos un Programador Senior con experiencia en arquitectura de "
            "software, buenas prácticas y code review..."
        ),
    },
}

REGLAS_DE_ORO = [
    (
        "🔍 Verificar",
        "Validá datos y fuentes. La IA suena segura pero puede alucinar: "
        "nunca des por cierto algo sin chequearlo.",
    ),
    (
        "🎯 Buen input",
        "A mejor información, mejor respuesta. Contexto pobre = output pobre.",
    ),
    (
        "🧑‍✈️ Copiloto",
        "No es un oráculo. Te ayuda a decidir mejor, pero la decisión final "
        "siempre es humana.",
    ),
]

TAREAS_MODELOS = {
    "Análisis de código / PDFs largos": {
        "modelo": "Claude",
        "razon": (
            "Ideal para profundidad analítica, refactorización de código y "
            "procesamiento de documentos extensos. Mantiene el hilo en "
            "contextos largos y es muy preciso siguiendo instrucciones."
        ),
        "color": "#FF6B35",
    },
    "Lluvia de ideas creativa": {
        "modelo": "ChatGPT",
        "razon": (
            "Ideal para brainstorming, copywriting rápido, lienzo "
            "interactivo (Canvas) y generación de imágenes integradas."
        ),
        "color": "#10A37F",
    },
    "Copywriting rápido": {
        "modelo": "ChatGPT",
        "razon": (
            "Rapidez y versatilidad para iterar copies, headlines y variantes "
            "en cuestión de segundos, con Canvas para edición colaborativa."
        ),
        "color": "#10A37F",
    },
    "Búsqueda de mercado actualizada": {
        "modelo": "Perplexity",
        "razon": (
            "Ideal para investigación en tiempo real y scraping de mercado, "
            "con fuentes citadas y datos actualizados."
        ),
        "color": "#20808D",
    },
}

GLOSARIO = {
    "Prompt": "La instrucción o pedido que le das a un modelo de IA para "
    "obtener una respuesta. Cuanto más claro y estructurado, mejor el resultado.",
    "Contexto": "Toda la información de fondo (audiencia, restricciones, "
    "marca, objetivo) que le das al modelo para que entienda la situación real.",
    "Modelo": "El sistema de IA entrenado (por ejemplo Claude, ChatGPT o "
    "Perplexity) que procesa tu prompt y genera una respuesta.",
    "Agente": "Un sistema de IA que no solo responde, sino que puede tomar "
    "acciones encadenadas (buscar, ejecutar código, usar herramientas) para "
    "cumplir un objetivo de forma más autónoma.",
    "Workflow": "La secuencia de pasos y herramientas conectadas que "
    "conforman un proceso, muchas veces automatizado con IA en el medio.",
    "Deploy": "El momento en que una solución (app, modelo, workflow) pasa "
    "de estar en desarrollo a estar en producción, disponible para usarse.",
    "Few-shot": "Técnica de prompting en la que le das al modelo unos pocos "
    "ejemplos del resultado esperado para guiar su respuesta.",
    "Alucinación": "Cuando la IA genera información falsa o inventada con "
    "total seguridad, como si fuera un hecho comprobado.",
}

# ─────────────────────────────────────────────────────────────────
# SIDEBAR — NAVEGACIÓN
# ─────────────────────────────────────────────────────────────────
st.sidebar.markdown("## 🚀 CopilotoIA")
st.sidebar.caption("De chatear a delegar, con criterio.")
st.sidebar.markdown("---")

seccion = st.sidebar.radio(
    "Navegación",
    [
        "1️⃣ Onboarding & Perfil",
        "2️⃣ Constructor de Prompts O.C.F.E.",
        "3️⃣ Recomendador de Modelos",
        "4️⃣ Glosario & Caso de Éxito",
    ],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.caption("Metodología basada en la Clase 2 de Coderhouse 🧑‍💻")

# ─────────────────────────────────────────────────────────────────
# SECCIÓN 1 — ONBOARDING & PERFIL DE USUARIO
# ─────────────────────────────────────────────────────────────────
if seccion == "1️⃣ Onboarding & Perfil":
    st.markdown(
        '<div class="hero-box"><h1>👋 ¡Arrancamos!</h1>'
        "<p>Elegí tu rol para personalizar tu experiencia con CopilotoIA.</p></div>",
        unsafe_allow_html=True,
    )

    rol_seleccionado = st.selectbox(
        "¿Cuál es tu rol profesional?",
        list(ROLES.keys()),
        key="rol_perfil",
    )

    # Guardamos el rol en session_state para reutilizarlo en la sección 2
    st.session_state["rol_actual"] = rol_seleccionado

    data_rol = ROLES[rol_seleccionado]

    st.success(f"{data_rol['emoji']} {data_rol['bienvenida']}")

    st.markdown("### 🏆 Las 3 Reglas de Oro de la IA")
    for titulo, descripcion in REGLAS_DE_ORO:
        st.markdown(
            f'<div class="golden-rule"><strong>{titulo}</strong><br>{descripcion}</div>',
            unsafe_allow_html=True,
        )

    st.info(
        "💡 Tip: guardá estas reglas en la nuca. Van a aparecer en cada "
        "sección de la app para que no se te escapen."
    )

# ─────────────────────────────────────────────────────────────────
# SECCIÓN 2 — CONSTRUCTOR DE PROMPTS O.C.F.E.
# ─────────────────────────────────────────────────────────────────
elif seccion == "2️⃣ Constructor de Prompts O.C.F.E.":
    st.markdown(
        '<div class="hero-box"><h1>🧩 Constructor de Prompts O.C.F.E.</h1>'
        "<p>Objetivo · Contexto · Formato · Ejemplos. Los 4 ingredientes "
        "de un prompt que realmente delega.</p></div>",
        unsafe_allow_html=True,
    )

    rol_actual = st.session_state.get("rol_actual", "Programador")
    st.caption(f"Perfil activo: **{rol_actual}** (cambialo en Onboarding si querés otro)")

    col1, col2 = st.columns(2)

    with col1:
        objetivo = st.text_area(
            "🎯 O — Objetivo",
            placeholder="¿Qué querés lograr y para quién? Ej: escribir un mail "
            "de bienvenida para nuevos usuarios de una app fintech.",
            height=110,
        )
        formato = st.text_area(
            "📐 F — Formato",
            placeholder="Largo, tono, formato de salida. Ej: 150 palabras, "
            "tono cercano y directo, en formato de mail con asunto.",
            height=110,
        )

    with col2:
        contexto = st.text_area(
            "🌎 C — Contexto",
            placeholder="Audiencia, restricciones, marca. Ej: usuarios "
            "jóvenes 25-35 años, marca informal pero confiable, evitar "
            "tecnicismos financieros.",
            height=110,
        )
        ejemplos = st.text_area(
            "📎 E — Ejemplos",
            placeholder="Pegá un ejemplo del resultado deseado (opcional "
            "pero recomendado).",
            height=110,
        )

    st.markdown("### ⚙️ Técnicas Avanzadas")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        activar_roleplay = st.toggle(
            "🎭 Activar Roleplay",
            help="Agrega automáticamente un rol de sistema según tu perfil.",
        )
    with col_t2:
        activar_cot = st.toggle(
            "🧠 Activar Chain of Thought",
            help='Agrega al final: "Pensá paso a paso antes de responder '
            'para optimizar el razonamiento lógico."',
        )

    st.markdown("---")

    if st.button("✨ Generar Prompt", type="primary", use_container_width=True):
        if not objetivo.strip():
            st.warning("⚠️ Como mínimo, completá el campo Objetivo para generar el prompt.")
        else:
            partes = []

            if activar_roleplay:
                partes.append(ROLES[rol_actual]["roleplay"])

            partes.append(f"OBJETIVO: {objetivo.strip()}")

            if contexto.strip():
                partes.append(f"CONTEXTO: {contexto.strip()}")

            if formato.strip():
                partes.append(f"FORMATO: {formato.strip()}")

            if ejemplos.strip():
                partes.append(f"EJEMPLOS DE REFERENCIA: {ejemplos.strip()}")

            if activar_cot:
                partes.append(
                    "Pensá paso a paso antes de responder para optimizar "
                    "el razonamiento lógico."
                )

            prompt_final = "\n\n".join(partes)

            st.markdown("### 📋 Tu prompt está listo")
            st.code(prompt_final, language="markdown")
            st.success("¡Copialo con el ícono de arriba y pegalo directo en tu IA favorita! 🚀")

# ─────────────────────────────────────────────────────────────────
# SECCIÓN 3 — RECOMENDADOR DE MODELOS
# ─────────────────────────────────────────────────────────────────
elif seccion == "3️⃣ Recomendador de Modelos":
    st.markdown(
        '<div class="hero-box"><h1>🧭 Recomendador de Modelos</h1>'
        "<p>No todas las IA sirven para todo. Elegí tu tarea y te decimos "
        "cuál conviene usar.</p></div>",
        unsafe_allow_html=True,
    )

    tarea = st.selectbox("¿Qué tarea querés resolver?", list(TAREAS_MODELOS.keys()))

    recomendacion = TAREAS_MODELOS[tarea]

    st.markdown(
        f"""
        <div class="model-card">
            <span class="badge" style="background-color:{recomendacion['color']}">
                RECOMENDADO
            </span>
            <h2>{recomendacion['modelo']}</h2>
            <p>{recomendacion['razon']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 📊 Comparativa rápida")
    for tarea_nombre, info in TAREAS_MODELOS.items():
        marca = "👉 " if tarea_nombre == tarea else "• "
        st.markdown(f"{marca}**{tarea_nombre}** → {info['modelo']}")

    st.info(
        "💡 Regla general: Claude para profundidad y código, ChatGPT para "
        "velocidad y creatividad visual, Perplexity para datos frescos."
    )

# ─────────────────────────────────────────────────────────────────
# SECCIÓN 4 — GLOSARIO DE BOLSILLO Y CASO DE ÉXITO
# ─────────────────────────────────────────────────────────────────
elif seccion == "4️⃣ Glosario & Caso de Éxito":
    st.markdown(
        '<div class="hero-box"><h1>📚 Glosario de Bolsillo</h1>'
        "<p>Los términos que tenés que manejar sí o sí para no perderte "
        "en ninguna reunión de IA.</p></div>",
        unsafe_allow_html=True,
    )

    for termino, definicion in GLOSARIO.items():
        with st.expander(f"🔑 {termino}"):
            st.write(definicion)

    st.markdown("---")
    st.markdown("## 🏆 Caso de Éxito: Rappi Turbo x Panini")

    with st.expander("❌ El Problema", expanded=True):
        st.write(
            "Rappi Turbo detectaba una caída en la retención de usuarios "
            "que compraban productos Panini: pedían una vez y no volvían "
            "a repetir la compra en las semanas siguientes."
        )

    with st.expander("⚙️ El Workflow implementado (Claude Code + Braze)"):
        st.write(
            "El equipo usó Claude Code para analizar patrones de compra "
            "en los datos históricos y detectar el momento exacto en el "
            "que un usuario dejaba de comprar. Con esos insights, armaron "
            "un workflow automatizado en Braze que disparaba campañas de "
            "reactivación personalizadas, con mensajes y ofertas ajustadas "
            "al comportamiento de cada segmento de usuarios."
        )

    with st.expander("📈 El Resultado"):
        st.success("**+7 puntos porcentuales de retención** en el segmento afectado.")
        st.write(
            "La clave no fue solo automatizar, sino delegar bien el análisis "
            "inicial a la IA para tomar mejores decisiones humanas después: "
            "el equipo verificó los patrones, dio buen contexto de negocio "
            "y usó a la IA como copiloto, no como piloto automático."
        )

    st.markdown("---")
    st.caption(
        "🎨 Si querés, también podemos seguir redactando el diseño UX "
        "completo de esta app."
    )
