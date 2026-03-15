import os
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Escala de Confort",
    page_icon="🐶",
    layout="wide",
    initial_sidebar_state="collapsed",
)

EVALUADORES = ["Ana Galdino", "Andrea Allende", "Ignacio Segura", "Miguel Cabezas"]
CSV_FILE = "evaluaciones_caninas.csv"

SECTIONS = [
    {
        "id": "paso_1",
        "title": "Paso 1. Observación a distancia, sin intervenir",
        "description": "Instrucción para el evaluador: observar al perro durante 2 minutos, sin hablarle, sin tocarlo y sin hacer contacto directo innecesario. Registrar respiración, postura, movilidad espontánea, conductas repetitivas, atención al entorno y señales emocionales visibles.",
        "groups": [
            {
                "id": "grupo_1",
                "title": "1) Respiración en reposo",
                "questions": [
                    {
                        "key": "resp_1_1",
                        "label": "1.1 ¿Durante ≥80% del tiempo observado respira de forma regular, sin jadeo y sin respiración abdominal marcada?",
                    },
                    {
                        "key": "resp_1_2",
                        "label": "1.2 ¿Jadea en reposo (sin calor ni ejercicio) durante ≥10 s seguidos o presenta ≥3 episodios en 2 min, sin respiración abdominal marcada?",
                    },
                    {
                        "key": "resp_1_3",
                        "label": "1.3 ¿Presenta respiración abdominal marcada y/o aumento evidente del trabajo respiratorio en reposo durante ≥10 s, con o sin jadeo?",
                    },
                ],
            },
            {
                "id": "grupo_2",
                "title": "2) Reposo y cambios de postura",
                "questions": [
                    {
                        "key": "reposo_2_1",
                        "label": "2.1 ¿Puede sentarse o tumbarse y mantenerse en la misma postura durante ≥30 s sin recolocarse?",
                    },
                    {
                        "key": "reposo_2_2",
                        "label": "2.2 ¿Se recoloca o cambia de postura ≥3 veces en 2 min y no logra mantenerse en la misma postura durante ≥30 s?",
                    },
                    {
                        "key": "reposo_2_3",
                        "label": "2.3 ¿Permanece de pie durante ≥60% del tiempo observado sin sentarse ni tumbarse?",
                    },
                ],
            },
            {
                "id": "grupo_3",
                "title": "3) Postura predominante y rigidez",
                "questions": [
                    {
                        "key": "postura_3_1",
                        "label": "3.1 ¿Durante ≥80% del tiempo el tronco y las extremidades se observan relajados, sin rigidez visible, y se mueve sin dureza?",
                    },
                    {
                        "key": "postura_3_2",
                        "label": "3.2 ¿Se observa rigidez visible en reposo durante ≥30 s y/o camina con rigidez o con pasos cortos o duros al menos una vez?",
                    },
                    {
                        "key": "postura_3_3",
                        "label": "3.3 ¿Mantiene una postura de protección durante ≥30 s, como espalda arqueada, cabeza baja persistente y/o negativa a apoyar una extremidad?",
                    },
                ],
            },
            {
                "id": "grupo_4",
                "title": "4) Conductas dirigidas a una zona corporal",
                "questions": [
                    {
                        "key": "conducta_4_1",
                        "label": "4.1 ¿No lame, muerde, rasca ni fija la mirada en la misma zona ≥3 veces en 2 min?",
                    },
                    {
                        "key": "conducta_4_2",
                        "label": "4.2 ¿Lame, muerde, rasca o mira fijamente la misma zona ≥3 veces en 2 min?",
                    },
                    {
                        "key": "conducta_4_3",
                        "label": "4.3 ¿Impide el acceso a una zona corporal cuando la mano se aproxima, girando o encogiendo el cuerpo, al menos una vez?",
                    },
                ],
            },
        ],
    },
    {
        "id": "paso_2",
        "title": "Paso 2. Observación emocional a distancia",
        "description": "Instrucción para el evaluador: continuar observando sin contacto físico. Registrar señales corporales emocionales, orientación al entorno, sobresaltos y conductas repetitivas.",
        "groups": [
            {
                "id": "grupo_5",
                "title": "5) Cola",
                "questions": [
                    {
                        "key": "cola_5_1",
                        "label": "5.1 ¿Mantiene la cola en posición neutra o relajada durante ≥80% del tiempo, sin llevarla entre las piernas?",
                    },
                    {
                        "key": "cola_5_2",
                        "label": "5.2 ¿Mantiene la cola baja o entre las piernas durante ≥80% del tiempo?",
                    },
                    {
                        "key": "cola_5_3",
                        "label": "5.3 ¿Mueve la cola rápidamente mientras el tronco permanece rígido durante ≥5 s al menos una vez?",
                    },
                ],
            },
            {
                "id": "grupo_6",
                "title": "6) Orejas",
                "questions": [
                    {
                        "key": "orejas_6_1",
                        "label": "6.1 ¿Mantiene las orejas en posición neutra o móvil durante ≥80% del tiempo, sin llevarlas pegadas hacia atrás?",
                    },
                    {
                        "key": "orejas_6_2",
                        "label": "6.2 ¿Mantiene las orejas pegadas hacia atrás durante ≥80% del tiempo?",
                    },
                    {
                        "key": "orejas_6_3",
                        "label": "6.3 ¿Mantiene las orejas orientadas hacia delante de forma sostenida durante ≥30 s ante un estímulo, al menos una vez?",
                    },
                ],
            },
            {
                "id": "grupo_7",
                "title": "7) Respuesta a estímulos ambientales",
                "questions": [
                    {
                        "key": "estimulos_7_1",
                        "label": "7.1 ¿Mira o gira la cabeza hacia un estímulo ambiental visible o audible al menos una vez durante la observación?",
                    },
                    {
                        "key": "estimulos_7_2",
                        "label": "7.2 ¿Permanece hipervigilante, mirando o girando la cabeza repetidamente hacia estímulos visibles o audibles durante gran parte de la observación, pese a estar despierto?",
                    },
                    {
                        "key": "estimulos_7_3",
                        "label": "7.3 ¿Se sobresalta ante un ruido al menos una vez?",
                    },
                ],
            },
            {
                "id": "grupo_8",
                "title": "8) Conductas repetitivas o estereotipadas",
                "questions": [
                    {
                        "key": "estereo_8_1",
                        "label": "8.1 ¿No repite trayectos ni realiza acciones repetidas sobre reja, puerta o suelo durante la observación?",
                    },
                    {
                        "key": "estereo_8_2",
                        "label": "8.2 ¿Repite el mismo trayecto ≥3 ciclos completos de ida y vuelta en 2 min?",
                    },
                    {
                        "key": "estereo_8_3",
                        "label": "8.3 ¿Rasca, cava o muerde reja, puerta o suelo ≥3 veces en 30 s?",
                    },
                    {
                        "key": "estereo_8_4",
                        "label": "8.4 ¿Gira sobre sí mismo, se balancea o salta en el sitio ≥3 veces en 30 s?",
                    },
                ],
            },
        ],
    },
    {
        "id": "paso_3",
        "title": "Paso 3. Interacción social suave, sin contacto físico inicial",
        "description": "Instrucción para el evaluador: acercarse de forma calmada, hablar en tono suave y valorar respuesta social antes de tocar al perro. Se pueden realizar hasta 3 intentos de llamado.",
        "groups": [
            {
                "id": "grupo_9",
                "title": "9) Vocalización",
                "questions": [
                    {
                        "key": "vocal_9_1",
                        "label": "9.1 ¿Durante ≥80% del tiempo observado no vocaliza, sin gemidos, quejidos, chillidos ni ladridos?",
                    },
                    {
                        "key": "vocal_9_2",
                        "label": "9.2 ¿Vocaliza repetidamente, con ≥3 episodios en 30 s o ≥10 s de forma sostenida, sin un estímulo inmediato visible?",
                    },
                    {
                        "key": "vocal_9_3",
                        "label": "9.3 ¿Vocaliza orientado a una persona y la vocalización disminuye dentro de 10 s tras recibir atención o contacto?",
                    },
                ],
            },
            {
                "id": "grupo_10",
                "title": "10) Respuesta a interacción humana",
                "questions": [
                    {
                        "key": "humana_10_1",
                        "label": "10.1 ¿Se acerca voluntariamente a una persona y reduce la distancia por iniciativa propia al menos una vez?",
                    },
                    {
                        "key": "humana_10_2",
                        "label": "10.2 ¿Se acerca solo para oler y se retira dentro de 2 s, al menos una vez?",
                    },
                    {
                        "key": "humana_10_3",
                        "label": "10.3 ¿No reduce la distancia por iniciativa propia durante toda la observación?",
                    },
                ],
            },
            {
                "id": "grupo_11",
                "title": "11) Respuesta al llamado (3 intentos)",
                "questions": [
                    {
                        "key": "llamado_11_1",
                        "label": "11.1 ¿Responde al llamado dentro de 3 intentos, orientando ojos o cabeza hacia el evaluador o acercándose?",
                    },
                    {
                        "key": "llamado_11_2",
                        "label": "11.2 ¿No responde tras 3 intentos y mantiene los ojos abiertos durante los intentos?",
                    },
                    {
                        "key": "llamado_11_3",
                        "label": "11.3 ¿No responde tras 3 intentos y mantiene los ojos cerrados durante los intentos?",
                    },
                ],
            },
            {
                "id": "grupo_12",
                "title": "12) Inmovilidad o “bloqueo” ante estímulo social suave",
                "questions": [
                    {
                        "key": "bloqueo_12_1",
                        "label": "12.1 ¿No permanece inmóvil más de 30 s con los ojos abiertos ante un estímulo social suave?",
                    },
                    {
                        "key": "bloqueo_12_2",
                        "label": "12.2 ¿Permanece inmóvil más de 30 s con los ojos abiertos ante un estímulo social suave?",
                    },
                    {
                        "key": "bloqueo_12_3",
                        "label": "12.3 ¿Permanece inmóvil más de 30 s con los ojos abiertos y con tensión o rigidez visible durante la inmovilidad?",
                    },
                ],
            },
        ],
    },
    {
        "id": "paso_4",
        "title": "Paso 4. Interacción directa con contacto",
        "description": "Instrucción para el evaluador: si el perro lo permite, realizar contacto físico suave en cuello y hombros. Después, si es seguro, hacer palpación suave de la zona de interés o una manipulación mínima.",
        "groups": [
            {
                "id": "grupo_13",
                "title": "13) Contacto físico en cuello/hombros",
                "questions": [
                    {
                        "key": "contacto_13_1",
                        "label": "13.1 ¿Durante el contacto no se aparta ni muestra rigidez visible durante ≥2 s?",
                    },
                    {
                        "key": "contacto_13_2",
                        "label": "13.2 ¿Durante el contacto retira la cabeza o el cuerpo, intenta apartarse o evita la mano al menos una vez?",
                    },
                    {
                        "key": "contacto_13_3",
                        "label": "13.3 ¿Durante el contacto permanece inmóvil >2 s y presenta rigidez visible, aunque no se aparte?",
                    },
                ],
            },
            {
                "id": "grupo_14",
                "title": "14) Conducta defensiva dirigida al humano",
                "questions": [
                    {
                        "key": "defensa_14_1",
                        "label": "14.1 ¿Durante la interacción o aproximación no gruñe, no lanza mordidas al aire ni intenta morder a la persona?",
                    },
                    {
                        "key": "defensa_14_2",
                        "label": "14.2 ¿Gruñe ante la aproximación o el contacto al menos una vez?",
                    },
                    {
                        "key": "defensa_14_3",
                        "label": "14.3 ¿Lanza mordidas al aire o intenta morder a la persona al menos una vez?",
                    },
                ],
            },
            {
                "id": "grupo_15",
                "title": "15) Reacción a la palpación o manipulación",
                "questions": [
                    {
                        "key": "palpacion_15_1",
                        "label": "15.1 ¿No hay reacción visible ante la palpación suave, sin sobresalto, retirada ni vocalización?",
                    },
                    {
                        "key": "palpacion_15_2",
                        "label": "15.2 ¿Se sobresalta, gira rápidamente hacia la mano o vocaliza ante la palpación suave al menos una vez?",
                    },
                    {
                        "key": "palpacion_15_3",
                        "label": "15.3 ¿Retira con fuerza, llora, chilla o protege claramente la zona, evitando que la mano la toque, al menos una vez?",
                    },
                ],
            },
        ],
    },
]

ALL_QUESTIONS = [
    question
    for section in SECTIONS
    for group in section["groups"]
    for question in group["questions"]
]

CSS = """
<style>
    .stApp {
        background: linear-gradient(180deg, #f5f7fb 0%, #eef2ff 100%);
    }
    .block-container {
        max-width: 1120px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    .hero-card {
        background: linear-gradient(135deg, #1f2937 0%, #312e81 100%);
        color: white;
        border-radius: 24px;
        padding: 1.45rem 1.6rem;
        box-shadow: 0 18px 50px rgba(30, 41, 59, 0.18);
        margin-bottom: 1rem;
    }
    .hero-card h1 {
        color: #ffffff !important;
    }
    .meta-card {
        background: rgba(255,255,255,0.96);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(226,232,240,0.98);
        border-radius: 20px;
        padding: 1rem 1.1rem;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05);
        margin-bottom: 1rem;
        color: #0f172a;
    }
    .instruction-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-left: 6px solid #6366f1;
        border-radius: 20px;
        padding: 1rem 1.1rem;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.05);
        margin-bottom: 1rem;
        color: #0f172a;
    }
    .instruction-card h2, .instruction-card h3, .instruction-card p, .instruction-card div, .instruction-card span {
        color: #0f172a !important;
    }
    .group-card {
        background: rgba(255,255,255,0.96);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(226,232,240,0.98);
        border-radius: 18px;
        padding: 0.8rem 0.95rem 0.2rem 0.95rem;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
        margin-bottom: 0.7rem;
        color: #0f172a;
    }
    .group-card h2, .group-card h3, .group-card p, .group-card div, .group-card span {
        color: #0f172a !important;
    }
    .question-card {
        background: #ffffff;
        border: 1px solid #eceff5;
        border-radius: 16px;
        padding: 0.85rem 0.95rem 0.35rem 0.95rem;
        margin-bottom: 0.45rem;
        color: #0f172a;
        box-shadow: 0 6px 16px rgba(15, 23, 42, 0.03);
    }
    .question-card h2, .question-card h3, .question-card p, .question-card div, .question-card span {
        color: #0f172a !important;
    }
    .tiny-muted {
        color: #64748b;
        font-size: 0.95rem;
    }
    .pill {
        display: inline-block;
        padding: 0.3rem 0.7rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.18);
        border: 1px solid rgba(255,255,255,0.16);
        font-size: 0.88rem;
        margin-right: 0.45rem;
    }
    div[data-testid="stRadio"] > label {
        display: none;
    }
    div[role="radiogroup"] {
        gap: 0.55rem;
        display: flex;
        flex-wrap: wrap;
        padding-bottom: 0.4rem;
    }
    div[role="radiogroup"] label {
        background: #f8fafc;
        border: 1px solid #dbe4f0;
        border-radius: 999px;
        padding: 0.15rem 0.9rem 0.15rem 0.75rem;
        min-height: 40px;
        display: inline-flex !important;
        align-items: center;
        transition: all 0.18s ease;
        box-shadow: 0 2px 6px rgba(15, 23, 42, 0.03);
    }
    div[role="radiogroup"] label:hover {
        border-color: #6366f1;
        background: #eef2ff;
        transform: translateY(-1px);
    }
    div[role="radiogroup"] label p {
        font-weight: 600;
        color: #0f172a !important;
        font-size: 0.98rem;
    }
    .summary-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 20px;
        padding: 1rem 1.1rem;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.05);
        margin-bottom: 1rem;
        color: #0f172a;
    }
    .summary-card h2, .summary-card h3, .summary-card p, .summary-card div, .summary-card span {
        color: #0f172a !important;
    }
    .stTextInput label, .stSelectbox label, .stMarkdown, .stSubheader {
        color: #0f172a !important;
    }
    .stTextInput input {
        color: #0f172a !important;
        background: #ffffff !important;
    }
    .stTextInput input::placeholder {
        color: #0f172a !important;
        opacity: 0.75 !important;
    }
    [data-testid="stTextInputRootElement"] input::placeholder {
        color: #0f172a !important;
        opacity: 0.75 !important;
    }
    [data-testid="stTextInputRootElement"] input {
        color: #0f172a !important;
    }
    h2, h3, .screen-title {
        color: #0f172a !important;
    }
    .stSelectbox div[data-baseweb="select"] > div {
        color: #0f172a !important;
        background: #ffffff !important;
    }
    [data-testid="stAlertContainer"] {
        color: #0f172a !important;
    }
    [data-testid="stAlertContainer"] p,
    [data-testid="stAlertContainer"] div,
    [data-testid="stAlertContainer"] span {
        color: #0f172a !important;
    }
</style>
"""


def init_state() -> None:
    defaults = {
        "screen": "inicio",
        "section_index": 0,
        "codigo_animal": "",
        "codigo_registro": "",
        "evaluador": EVALUADORES[0],
        "last_saved_file": CSV_FILE,
    }
    for q in ALL_QUESTIONS:
        defaults[q["key"]] = None

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_form() -> None:
    st.session_state.screen = "inicio"
    st.session_state.section_index = 0
    st.session_state.codigo_animal = ""
    st.session_state.codigo_registro = ""
    st.session_state.evaluador = EVALUADORES[0]
    for q in ALL_QUESTIONS:
        st.session_state[q["key"]] = None


def section_complete(section: dict) -> bool:
    keys = [q["key"] for g in section["groups"] for q in g["questions"]]
    return all(st.session_state[k] in (True, False) for k in keys)


def total_answered() -> int:
    return sum(1 for q in ALL_QUESTIONS if st.session_state[q["key"]] in (True, False))


def save_to_csv() -> str:
    row = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "codigo_animal": st.session_state.codigo_animal.strip(),
        "codigo_registro": st.session_state.codigo_registro.strip(),
        "evaluador": st.session_state.evaluador,
    }

    for q in ALL_QUESTIONS:
        value = st.session_state[q["key"]]
        row[q["key"]] = "Sí" if value is True else "No" if value is False else ""

    df_new = pd.DataFrame([row])

    if os.path.exists(CSV_FILE):
        df_old = pd.read_csv(CSV_FILE)
        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df = df_new

    df.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")
    return CSV_FILE


def response_switch(label: str, key: str) -> None:
    st.markdown(
        f'<div class="question-card"><div style="font-size:1rem; font-weight:600; line-height:1.5; color:#0f172a;">{label}</div></div>',
        unsafe_allow_html=True,
    )
    current = st.session_state[key]
    default_index = 0 if current is None else 1 if current is True else 2
    selected = st.radio(
        f"radio_{key}",
        ["Sin responder", "Sí", "No"],
        index=default_index,
        horizontal=True,
        key=f"widget_{key}",
        label_visibility="collapsed",
    )
    if selected == "Sí":
        st.session_state[key] = True
    elif selected == "No":
        st.session_state[key] = False
    else:
        st.session_state[key] = None


def go_to_section(index: int) -> None:
    st.session_state.section_index = index
    st.session_state.screen = "seccion"


def render_top_bar() -> None:
    answered = total_answered()
    total = len(ALL_QUESTIONS)
    progress = answered / total if total else 0
    st.markdown(
        f'''
        <div class="hero-card">
            <div style="display:flex; flex-wrap:wrap; justify-content:space-between; gap:1rem; align-items:flex-start;">
                <div>
                    <div class="pill">🐶 Evaluación canina</div>
                    <div class="pill">{answered}/{total} respuestas</div>
                    <h1 style="margin:0.8rem 0 0.35rem 0; font-size:2rem;">Escala de Confort</h1>
                    <div style="opacity:0.96; line-height:1.55; max-width:760px; color:#eef2ff;">
                        Herramienta en desarrollo para evaluar el confort del perro de forma estructurada.
                    </div>
                </div>
            </div>
        </div>
        ''',
        unsafe_allow_html=True,
    )
    st.progress(progress)


def render_section_navigation() -> None:
    cols = st.columns(len(SECTIONS))
    for i, section in enumerate(SECTIONS):
        completed = "✅" if section_complete(section) else "•"
        label = f"{completed} Paso {i+1}"
        if cols[i].button(label, key=f"nav_{section['id']}", use_container_width=True):
            go_to_section(i)
            st.rerun()


init_state()
st.markdown(CSS, unsafe_allow_html=True)
render_top_bar()

if st.session_state.screen == "inicio":
    st.markdown('<div class="meta-card">', unsafe_allow_html=True)
    st.subheader("Datos iniciales")
    left, right = st.columns([1, 1])
    with left:
        codigo_animal = st.text_input(
            "Código del animal",
            value=st.session_state.codigo_animal,
            placeholder="EJEMPLO: Q00000"
        )
        codigo_registro = st.text_input(
            "Código de registro",
            value=st.session_state.codigo_registro,
            placeholder="EJEMPLO: 0001, 0002"
        )
        st.session_state.codigo_animal = codigo_animal
        st.session_state.codigo_registro = codigo_registro
    with right:
        evaluador = st.selectbox("Evaluador", EVALUADORES, index=EVALUADORES.index(st.session_state.evaluador))
        st.session_state.evaluador = evaluador
        st.markdown('<p class="tiny-muted">Completa estos datos antes de comenzar la evaluación.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Comenzar evaluación", use_container_width=True, type="primary"):
            if not st.session_state.codigo_animal.strip() or not st.session_state.codigo_registro.strip():
                st.error("Completa el código del animal y el código de registro.")
            else:
                st.session_state.section_index = 0
                st.session_state.screen = "instrucciones"
                st.rerun()
    with col2:
        st.button("Limpiar formulario", on_click=reset_form, use_container_width=True)

elif st.session_state.screen == "instrucciones":
    render_section_navigation()
    section = SECTIONS[st.session_state.section_index]
    st.markdown(
        f'''
        <div class="instruction-card">
            <div class="tiny-muted" style="color:#475569;">Antes de empezar</div>
            <h2 style="margin:0.35rem 0 0.5rem 0; color:#0f172a;">{section['title']}</h2>
            <div style="line-height:1.6; color:#1f2937;">{section['description']}</div>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("Volver a datos iniciales", use_container_width=True):
            st.session_state.screen = "inicio"
            st.rerun()
    with c2:
        if st.button("Empezar este bloque", use_container_width=True, type="primary"):
            st.session_state.screen = "seccion"
            st.rerun()

elif st.session_state.screen == "seccion":
    render_section_navigation()
    section = SECTIONS[st.session_state.section_index]
    st.markdown(
        f'''
        <div class="instruction-card">
            <div class="tiny-muted" style="color:#475569;">Bloque activo</div>
            <h2 style="margin:0.35rem 0 0.5rem 0; color:#0f172a;">{section['title']}</h2>
            <div style="line-height:1.6; color:#1f2937;">{section['description']}</div>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    for group in section["groups"]:
        st.markdown(
            f'''
            <div class="group-card">
                <h3 style="margin:0.1rem 0 0.9rem 0; color:#0f172a;">{group['title']}</h3>
            </div>
            ''',
            unsafe_allow_html=True,
        )
        for q in group["questions"]:
            response_switch(q["label"], q["key"])

    if not section_complete(section):
        st.info("Este bloque todavía tiene preguntas sin responder.")

    prev_disabled = st.session_state.section_index == 0
    next_disabled = st.session_state.section_index == len(SECTIONS) - 1

    a, b, c = st.columns([1, 1, 1])
    with a:
        if st.button("Instrucciones del bloque", use_container_width=True):
            st.session_state.screen = "instrucciones"
            st.rerun()
    with b:
        if st.button("Bloque anterior", use_container_width=True, disabled=prev_disabled):
            st.session_state.section_index -= 1
            st.session_state.screen = "instrucciones"
            st.rerun()
    with c:
        if st.button("Siguiente bloque", use_container_width=True, disabled=next_disabled):
            st.session_state.section_index += 1
            st.session_state.screen = "instrucciones"
            st.rerun()

    st.divider()
    x, y = st.columns([1, 1])
    with x:
        if st.button("Revisar resumen", use_container_width=True):
            st.session_state.screen = "resumen"
            st.rerun()
    with y:
        if st.button("Guardar evaluación", use_container_width=True, type="primary"):
            if all(section_complete(sec) for sec in SECTIONS):
                file_path = save_to_csv()
                st.session_state.last_saved_file = file_path
                st.session_state.screen = "guardado"
                st.rerun()
            else:
                st.warning("Aún hay bloques con preguntas sin responder.")

elif st.session_state.screen == "resumen":
    render_section_navigation()
    st.markdown('<div class="summary-card">', unsafe_allow_html=True)
    st.subheader("Resumen de la evaluación")
    m1, m2, m3 = st.columns(3)
    m1.metric("Código del animal", st.session_state.codigo_animal)
    m2.metric("Código de registro", st.session_state.codigo_registro)
    m3.metric("Evaluador", st.session_state.evaluador)
    st.markdown('</div>', unsafe_allow_html=True)

    for section in SECTIONS:
        st.markdown(f"### {section['title']}")
        for group in section["groups"]:
            st.markdown(f"**{group['title']}**")
            for q in group["questions"]:
                value = st.session_state[q["key"]]
                shown = "Sí" if value is True else "No" if value is False else "Sin responder"
                st.write(f"- {q['label']}")
                st.write(f"  **Respuesta:** {shown}")

    r1, r2 = st.columns([1, 1])
    with r1:
        if st.button("Volver al bloque actual", use_container_width=True):
            st.session_state.screen = "seccion"
            st.rerun()
    with r2:
        if st.button("Guardar definitivamente", use_container_width=True, type="primary"):
            if all(section_complete(sec) for sec in SECTIONS):
                file_path = save_to_csv()
                st.session_state.last_saved_file = file_path
                st.session_state.screen = "guardado"
                st.rerun()
            else:
                st.warning("No puedes guardar todavía. Hay preguntas sin responder.")

elif st.session_state.screen == "guardado":
    st.success("La evaluación se guardó correctamente.")
    st.write(f"**Archivo generado:** `{st.session_state.get('last_saved_file', CSV_FILE)}`")

    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "rb") as f:
            st.download_button(
                "Descargar CSV",
                data=f,
                file_name=CSV_FILE,
                mime="text/csv",
                use_container_width=True,
            )

    st.markdown('<div class="summary-card">', unsafe_allow_html=True)
    st.subheader("Vista previa del archivo")
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    z1, z2 = st.columns([1, 1])
    with z1:
        if st.button("Nueva evaluación", use_container_width=True):
            reset_form()
            st.rerun()
    with z2:
        if st.button("Ir al resumen", use_container_width=True):
            st.session_state.screen = "resumen"
            st.rerun()
