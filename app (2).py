import streamlit as st

# ============================================================
# CONFIGURACIÓN DE PÁGINA
# ============================================================
st.set_page_config(
    page_title="CopilotoIA · Tu Guía de IA",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# ESTILOS
# ============================================================
st.markdown("""
    <style>
    /* Ocultar elementos por defecto de Streamlit para look más limpio */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #FF5A00;
        text-align: center;
        margin-bottom: 0px;
        letter-spacing: -1px;
    }
    .tagline {
        font-size: 17px;
        text-align: center;
        color: #6B6B6B;
        margin-bottom: 25px;
        font-style: italic;
    }
    .section-title {
        font-size: 26px;
        font-weight: 700;
        color: #262730;
        margin-bottom: 4px;
    }
    .section-sub {
        color: #7A7A7A;
        margin-bottom: 20px;
    }
    .card {
        background-color: #FDFDFD;
        padding: 22px;
        border-radius: 14px;
        border: 1px solid #EDEDED;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
        margin-bottom: 18px;
    }
    .model-box {
        padding: 18px 20px;
        border-radius: 10px;
        margin-bottom: 16px;
    }
    .claude-box   { background-color: #FBF6F0; border-left: 6px solid #D97706; }
    .chatgpt-box  { background-color: #EDF7ED; border-left: 6px solid #2E7D32; }
    .perplexity-box{ background-color: #F0F7FF; border-left: 6px solid #0056B3; }
    .gemini-box   { background-color: #F5F0FF; border-left: 6px solid #7C3AED; }

    .pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        background-color: #FFEDE0;
        color: #FF5A00;
        font-size: 13px;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    .welcome-box {
        background: linear-gradient(135deg, #FFF3EC 0%, #FFFFFF 100%);
        padding: 30px;
        border-radius: 16px;
        border: 1px solid #FFE0CC;
        text-align: center;
        margin-bottom: 20px;
    }
    .coder-card {
        background-color: #FDFDFD;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #EAEAEA;
        border-left: 6px solid #FF5A00;
        margin-bottom: 20px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.02);
    }
    .coder-card.success { border-left-color: #2E7D32; }
    .kpi-box {
        background-color: #F7FBF7;
        padding: 16px 18px;
        border-radius: 10px;
        border: 1px solid #DCEEDC;
        text-align: center;
    }
    .kpi-number {
        font-size: 26px;
        font-weight: 800;
        color: #2E7D32;
    }
    .kpi-label {
        font-size: 13px;
        color: #6B6B6B;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# ESTADO DE SESIÓN (para recordar el onboarding del usuario)
# ============================================================
if "onboarding_done" not in st.session_state:
    st.session_state.onboarding_done = False
if "nombre" not in st.session_state:
    st.session_state.nombre = ""
if "rol" not in st.session_state:
    st.session_state.rol = "Otro / Emprendedor"
if "nivel" not in st.session_state:
    st.session_state.nivel = "Recién empiezo"
if "objetivo_ia" not in st.session_state:
    st.session_state.objetivo_ia = "Ahorrar tiempo en tareas repetitivas"

ROLES = [
    "Growth Hacker / Marketer",
    "Product Manager",
    "Copywriter / Creador de Contenido",
    "Diseñador/a Gráfico/a",
    "Programador / Perfil Técnico",
    "Project Manager / Operaciones",
    "Educación / Salud / ONG",
    "Otro / Emprendedor",
]

NIVELES = ["Recién empiezo", "Uso IA de vez en cuando", "La uso todos los días"]

OBJETIVOS = [
    "Ahorrar tiempo en tareas repetitivas",
    "Mejorar la calidad de lo que produzco",
    "Aprender a delegar tareas complejas",
    "Automatizar procesos de mi equipo",
]

# ============================================================
# ENCABEZADO
# ============================================================
st.markdown("<div class='main-title'>🚀 CopilotoIA</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='tagline'>Tu guía para pasar de chatear con una IA a delegarle trabajo de verdad</div>",
    unsafe_allow_html=True
)

# ============================================================
# BARRA LATERAL — NAVEGACIÓN + MINI PERFIL
# ============================================================
with st.sidebar:
    st.markdown("### 🧭 Navegación")
    seccion = st.radio(
        "Elegí una sección",
        [
            "👋 Onboarding",
            "🤖 Recomendador de IAs",
            "📖 Glosario Sin Humo",
            "✍️ Constructor de Prompts",
            "🏆 Caso de Éxito",
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    if st.session_state.onboarding_done:
        st.markdown("#### 🙋 Tu perfil")
        st.success(f"**{st.session_state.nombre or 'Sin nombre'}**\n\n{st.session_state.rol}")
        if st.button("✏️ Editar perfil"):
            st.session_state.onboarding_done = False
    else:
        st.info("Todavía no completaste tu onboarding. ¡Empezá por ahí! 👋")

    st.markdown("---")
    st.markdown("#### 💡 Reglas de oro")
    st.caption(
        "1. **Verificá** datos, cifras y aspectos legales.\n\n"
        "2. **Buen input, buen output**: cuanto más contexto le des, mejor responde.\n\n"
        "3. La IA es tu **copiloto**, no un oráculo. La decisión final es tuya."
    )

# ============================================================
# SECCIÓN 1: ONBOARDING
# ============================================================
if seccion == "👋 Onboarding":
    st.markdown("<div class='section-title'>👋 Contanos quién sos</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-sub'>Con esto vamos a poder mostrarte recomendaciones más relevantes en toda la app.</div>",
        unsafe_allow_html=True
    )

    with st.form("onboarding_form"):
        col1, col2 = st.columns(2)

        with col1:
            nombre = st.text_input("¿Cómo te llamás?", value=st.session_state.nombre, placeholder="Ej: Ana")
            rol = st.selectbox("¿Cuál es tu rol principal?", ROLES, index=ROLES.index(st.session_state.rol))

        with col2:
            nivel = st.select_slider(
                "¿Qué tan familiarizado/a estás con IA?",
                options=NIVELES,
                value=st.session_state.nivel
            )
            objetivo = st.selectbox(
                "¿Qué buscás lograr principalmente con IA?",
                OBJETIVOS,
                index=OBJETIVOS.index(st.session_state.objetivo_ia)
            )

        enviado = st.form_submit_button("✅ Guardar y continuar", type="primary")

        if enviado:
            st.session_state.nombre = nombre
            st.session_state.rol = rol
            st.session_state.nivel = nivel
            st.session_state.objetivo_ia = objetivo
            st.session_state.onboarding_done = True
            st.rerun()

    if st.session_state.onboarding_done:
        st.markdown(f"""
        <div class='welcome-box'>
            <h3>🎉 ¡Listo, {st.session_state.nombre or 'copiloto'}!</h3>
            <p>Ya configuramos tu perfil como <b>{st.session_state.rol}</b>, con nivel
            <b>{st.session_state.nivel}</b>. Tu objetivo principal es
            <b>{st.session_state.objetivo_ia.lower()}</b>.</p>
            <p>👉 Ahora te recomendamos pasar a <b>"🤖 Recomendador de IAs"</b> en el menú de la izquierda.</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# SECCIÓN 2: RECOMENDADOR DE IAS
# ============================================================
elif seccion == "🤖 Recomendador de IAs":
    st.markdown("<div class='section-title'>🤖 ¿Qué IA se adapta mejor a tu necesidad?</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-sub'>Elegí por caso de uso real y rendimiento técnico, no por moda.</div>",
        unsafe_allow_html=True
    )

    if st.session_state.onboarding_done:
        st.caption(f"Mostrando recomendaciones pensadas para: **{st.session_state.rol}**")

    tarea = st.selectbox(
        "¿Qué tarea específica necesitás delegar hoy?",
        [
            "Análisis profundo de documentos largos (PDFs, reportes)",
            "Refactorización de código y lógica técnica avanzada",
            "Brainstorming creativo, copys de redes sociales e ideas de campañas",
            "Generar imágenes artísticas o piezas visuales",
            "Investigación de mercado actualizada con datos y fuentes en internet",
            "Crear automatizaciones integradas sin código (workflows)",
        ]
    )

    st.markdown("#### 🎯 Nuestra recomendación")

    RECOMENDACIONES = {
        "Análisis profundo de documentos largos (PDFs, reportes)": {
            "clase": "claude-box",
            "titulo": "Claude (Anthropic)",
            "por_que": "Razonamiento lógico sólido, tono natural y una ventana de contexto muy amplia para asimilar múltiples archivos técnicos sin perder el hilo.",
            "uso": "Pegar varios PDFs o documentos y pedirle que encuentre inconsistencias o arme un resumen estructurado.",
            "limite": "No genera imágenes de forma nativa.",
        },
        "Refactorización de código y lógica técnica avanzada": {
            "clase": "claude-box",
            "titulo": "Claude (Anthropic)",
            "por_que": "Muy fuerte en razonamiento paso a paso y en mantener consistencia en bases de código grandes.",
            "uso": "Pegar varios archivos de código y pedirle que detecte bugs o proponga una refactorización.",
            "limite": "No genera imágenes de forma nativa.",
        },
        "Brainstorming creativo, copys de redes sociales e ideas de campañas": {
            "clase": "chatgpt-box",
            "titulo": "ChatGPT (OpenAI)",
            "por_que": "Su lienzo interactivo (Canvas) es muy cómodo para iterar textos creativos en tiempo real.",
            "uso": "Lluvia de ideas, variantes de copys, guiones cortos para redes.",
            "limite": "En análisis técnico muy profundo puede alucinar más que otras opciones en hilos largos.",
        },
        "Generar imágenes artísticas o piezas visuales": {
            "clase": "chatgpt-box",
            "titulo": "ChatGPT (OpenAI) con DALL-E",
            "por_que": "Generación de imágenes integrada de forma nativa en la misma conversación.",
            "uso": "Conceptos visuales rápidos, moodboards de referencia, piezas ilustrativas.",
            "limite": "Para piezas finales de diseño profesional, seguí ajustando en tu software de diseño habitual.",
        },
        "Investigación de mercado actualizada con datos y fuentes en internet": {
            "clase": "perplexity-box",
            "titulo": "Perplexity AI (o modo Research)",
            "por_que": "Está optimizado para rastrear internet en tiempo real y citar cada fuente que usa.",
            "uso": "Buscar estadísticas actualizadas, comparar competidores, sintetizar reviews.",
            "limite": "Menos potente que otras IAs para tareas creativas largas.",
        },
        "Crear automatizaciones integradas sin código (workflows)": {
            "clase": "gemini-box",
            "titulo": "Orquestadores de Workflows (n8n, Make, Zapier)",
            "por_que": "El salto real de productividad está en conectar la API de un modelo de IA a tus herramientas (CRM, planillas, WhatsApp) para disparar flujos automáticos.",
            "uso": "Ej: nuevo lead → la IA redacta un mensaje personalizado → se envía automáticamente.",
            "limite": "Requiere una configuración inicial más técnica que usar un chat.",
        },
    }

    r = RECOMENDACIONES[tarea]
    st.markdown(f"""
    <div class='model-box {r["clase"]}'>
        <h3>🏆 {r["titulo"]}</h3>
        <p><b>Por qué:</b> {r["por_que"]}</p>
        <p><b>Uso óptimo:</b> {r["uso"]}</p>
        <p><b>Límite a tener en cuenta:</b> {r["limite"]}</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# SECCIÓN 3: GLOSARIO SIN HUMO
# ============================================================
elif seccion == "📖 Glosario Sin Humo":
    st.markdown("<div class='section-title'>📖 Glosario de Bolsillo</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-sub'>La IA explicada de forma clara, sin términos pretenciosos.</div>",
        unsafe_allow_html=True
    )

    GLOSARIO = {
        "💬 Entender la conversación": {
            "Prompt": "La instrucción o pedido específico que le das a la IA. Tu forma de pedir las cosas.",
            "Contexto": "Toda la información de soporte (reglas, restricciones, datos) que le das a la IA para que su respuesta sea más precisa y personalizada.",
            "Modelo": "El 'cerebro' entrenado detrás del asistente conversacional (ej. Claude, GPT, Gemini).",
            "Alucinación": "Cuando la IA inventa información con tono de total seguridad porque no tiene suficiente contexto o datos confiables.",
        },
        "⚡ Pasar a la acción": {
            "Agente": "Una IA configurada con un rol, contexto y objetivos persistentes que puede ejecutar tareas de forma más autónoma.",
            "Workflow (flujo de trabajo)": "Pasos encadenados y automatizados (Paso A → Paso B → Paso C) para resolver un proceso completo.",
            "Deploy (puesta en producción)": "Hacer que una herramienta o agente esté disponible para muchas personas, no solo para vos en tu compu.",
            "Few-shot": "Técnica de prompting: darle a la IA uno o varios ejemplos resueltos para guiar el estilo y formato de su respuesta.",
        },
    }

    busqueda = st.text_input("🔎 Buscar un término", placeholder="Ej: prompt, agente, contexto...")

    col_g1, col_g2 = st.columns(2)
    columnas = [col_g1, col_g2]

    for i, (grupo, terminos) in enumerate(GLOSARIO.items()):
        with columnas[i % 2]:
            st.markdown(f"#### {grupo}")
            for termino, definicion in terminos.items():
                if busqueda.lower() in termino.lower() or busqueda.lower() in definicion.lower():
                    with st.expander(termino):
                        st.write(definicion)

# ============================================================
# SECCIÓN 4: CONSTRUCTOR DE PROMPTS (MÉTODO O.C.F.E.)
# ============================================================
elif seccion == "✍️ Constructor de Prompts":
    st.markdown("<div class='section-title'>✍️ Diseñá tu prompt perfecto (Método O.C.F.E.)</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-sub'>El 80% de un mal resultado es culpa de un input flojo. Completá los campos para armar un prompt robusto.</div>",
        unsafe_allow_html=True
    )

    col_prompt1, col_prompt2 = st.columns([1, 1])

    with col_prompt1:
        st.markdown("**1. Ingredientes clave**")

        objetivo_input = st.text_area(
            "🎯 Objetivo (¿qué querés lograr y para quién?)",
            placeholder="Ej: Escribir un posteo de Instagram para difundir una charla sobre estimulación temprana para familias con bebés de 0 a 2 años."
        )

        contexto_input = st.text_area(
            "🌐 Contexto (audiencia, marca, restricciones o dolores)",
            placeholder="Ej: Familias con niños pequeños, muchas primerizas. El tono debe ser cálido, cercano y nada técnico."
        )

        formato_input = st.text_input(
            "📋 Formato (largo, estructura, tono, canal)",
            placeholder="Ej: Posteo corto para Instagram, máximo 80 palabras, con 3 hashtags y una pregunta final para generar comentarios."
        )

        ejemplos_input = st.text_area(
            "📝 Ejemplos (opcional — referencias de lo que considerás bueno)",
            placeholder="Ej: Pegá acá algún posteo o texto que ya haya funcionado bien antes."
        )

    with col_prompt2:
        st.markdown("**2. Potenciadores avanzados**")

        usar_roleplay = st.checkbox("🎭 Activar Roleplay (asignar un rol de sistema)", value=True)
        default_role_text = f"Sos un/a experto/a en {st.session_state.rol} con amplia trayectoria y obsesión por los resultados."
        system_role = st.text_input("Definir rol de sistema:", value=default_role_text, disabled=not usar_roleplay)

        usar_cot = st.checkbox("🧠 Activar Cadena de Pensamiento (Chain of Thought)", value=False)

        st.markdown("---")

        if st.button("✨ ¡Generar mi prompt optimizado!", type="primary"):
            if not objetivo_input or not contexto_input:
                st.warning("⚠️ Completá al menos el **Objetivo** y el **Contexto** para generar un prompt de calidad.")
            else:
                prompt_final = ""

                if usar_roleplay:
                    prompt_final += f"**[ROL DE SISTEMA]**\n{system_role}\n\n"

                prompt_final += f"**[OBJETIVO]**\n{objetivo_input}\n\n"
                prompt_final += f"**[CONTEXTO]**\n{contexto_input}\n\n"

                if formato_input:
                    prompt_final += f"**[FORMATO Y ESTRUCTURA]**\n{formato_input}\n\n"
                else:
                    prompt_final += "**[FORMATO]**\nAdaptá el formato de salida de forma profesional e intuitiva para el objetivo planteado.\n\n"

                if ejemplos_input:
                    prompt_final += f"**[EJEMPLOS DE REFERENCIA]**\n{ejemplos_input}\n\n"

                if usar_cot:
                    prompt_final += (
                        "**[REGLA DE RAZONAMIENTO]**\n"
                        "Antes de dar la respuesta final, pensá paso a paso (Chain of Thought) "
                        "analizando riesgos, el tono adecuado y las mejores alternativas para cumplir el objetivo."
                    )

                st.success("🎉 ¡Tu prompt está listo! Copialo y pegalo en tu IA preferida:")
                st.text_area("📋 Prompt para copiar:", prompt_final, height=280)
                st.caption(
                    "💡 Truco: la primera respuesta es solo un borrador (80%). "
                    "Hacé 2 o 3 vueltas de iteración criticando el output para pulir el 20% final."
                )

# ============================================================
# SECCIÓN 5: CASO DE ÉXITO
# ============================================================
elif seccion == "🏆 Caso de Éxito":
    st.markdown("<div class='section-title'>🏆 Caso de Éxito: Rappi Turbo × Panini</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-sub'>Un ejemplo real de cómo la IA aplicada con criterio estratégico genera retornos concretos.</div>",
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class='coder-card'>
        <h4>🚨 El desafío operativo</h4>
        <p>Durante el furor del álbum Panini en Argentina, miles de usuarios nuevos compraban el álbum y las figuritas
        en <b>Rappi Turbo</b> por la velocidad de entrega (10 minutos), pero luego desaparecían sin consumir otras
        categorías de supermercado. No había equipo de datos disponible para armar una campaña manual a tiempo.</p>
    </div>
    <div class='coder-card'>
        <h4>⛓️ El workflow implementado</h4>
        <ol>
            <li><b>Adquisición:</b> los usuarios nuevos entran por la compra del álbum Panini.</li>
            <li><b>Segmentación automática:</b> se clasifica a los usuarios en tiers según su historial previo en Rappi.</li>
            <li><b>Trigger semanal:</b> si el usuario no vuelve a comprar en un período establecido, un trigger automático
            consulta la plataforma de incentivos.</li>
            <li><b>Acción personalizada:</b> un agente genera y envía un incentivo calibrado al tier del usuario para
            motivarlo a comprar en la sección de supermercado.</li>
        </ol>
    </div>
    <div class='coder-card success'>
        <h4>📈 El impacto en los números</h4>
        <ul>
            <li><b>+7 puntos porcentuales</b> de retención en estos cohortes, comparado con países que no aplicaron la automatización.</li>
            <li><b>Aumento sostenido</b> del piso de usuarios activos mensuales (MAU).</li>
            <li><b>Mayor rentabilidad</b> al diluir costos fijos sobre un volumen de órdenes mucho más alto.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.markdown("<div class='kpi-box'><div class='kpi-number'>+7pp</div><div class='kpi-label'>Retención</div></div>", unsafe_allow_html=True)
    with kpi2:
        st.markdown("<div class='kpi-box'><div class='kpi-number'>3.7x</div><div class='kpi-label'>ROI promedio</div></div>", unsafe_allow_html=True)
    with kpi3:
        st.markdown("<div class='kpi-box'><div class='kpi-number'>Días</div><div class='kpi-label'>Tiempo de desarrollo</div></div>", unsafe_allow_html=True)

    st.info(
        "💡 **Conclusión:** el futuro no es que la IA reemplace a los profesionales; el futuro pertenece a "
        "quienes tienen criterio estratégico y usan la IA como copiloto ejecutor de workflows."
    )
