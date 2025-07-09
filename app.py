# Main Streamlit application 
import streamlit as st
from components.chat_interface import render_chat_interface, clear_chat_history
from components.source_display import render_sources

st.set_page_config(page_title="RAG Chatbot", page_icon="💬", layout="centered")

st.markdown("""
<style>
/* Fondo y burbujas tipo chat */
.stChatMessage.user {background: #e6f7ff; border-radius: 12px 12px 0 12px; margin-bottom: 8px;}
.stChatMessage.bot {background: #f4f4f8; border-radius: 12px 12px 12px 0; margin-bottom: 8px;}
.stChatInputContainer {margin-top: 2rem;}
</style>
""", unsafe_allow_html=True)

st.title("💬 RAG Chatbot (OpenShift)")

# Sidebar con controles adicionales
with st.sidebar:
    st.markdown("### ⚙️ Controles")
    if st.button("🗑️ Limpiar historial"):
        clear_chat_history()
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 🎯 Ajuste de Prompt")
    prompt_context = st.text_area(
        "Contexto adicional para las consultas:",
        placeholder="Ej: Responde como un experto en finanzas...",
        help="Agrega contexto adicional que se incluirá en todas las consultas",
        height=100
    )
    
    # Guardar el contexto en session_state
    if "prompt_context" not in st.session_state:
        st.session_state["prompt_context"] = ""
    
    if st.button("💾 Guardar contexto"):
        st.session_state["prompt_context"] = prompt_context
        st.success("Contexto guardado!")
    
    st.markdown("---")
    st.markdown("### 📝 Formato de Respuesta")
    enable_markdown = st.toggle(
        "✨ Habilitar Markdown",
        value=True,
        help="Activa el formato Markdown en las respuestas del bot"
    )
    
    # Guardar preferencia en session_state
    st.session_state["enable_markdown"] = enable_markdown
    
    st.markdown("---")
    st.markdown("### 📊 Estado del API")
    from utils.api_client import health_check
    if health_check():
        st.success("✅ API Conectado")
    else:
        st.error("❌ API Desconectado")

# Renderizar la interfaz de chat
render_chat_interface() 