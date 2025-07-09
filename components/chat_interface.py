# Componentes de chat 
import streamlit as st
from streamlit_chat import message
from utils.api_client import query_rag_api, log_info, log_success, log_warning
from components.source_display import render_sources

def render_chat_interface():
    """Renderiza la interfaz de chat completa con historial y input."""
    
    # Inicializar historial en session_state
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "sources" not in st.session_state:
        st.session_state["sources"] = []

    # Mostrar historial de chat
    for i, msg in enumerate(st.session_state["messages"]):
        is_user = msg["role"] == "user"
        
        # Renderizar mensaje según preferencias del usuario
        if is_user:
            message(
                msg["content"],
                is_user=True,
                key=f"msg_{i}",
                avatar_style="big-smile"
            )
        else:
            # Verificar si Markdown está habilitado
            enable_markdown = st.session_state.get("enable_markdown", True)
            
            if enable_markdown:
                # Usar st.markdown para respuestas del bot con soporte de Markdown
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(msg["content"])
            else:
                # Usar texto plano
                message(
                    msg["content"],
                    is_user=False,
                    key=f"msg_{i}",
                    avatar_style="bottts"
                )
        
        # Mostrar sources para respuestas del bot
        if not is_user and i < len(st.session_state["sources"]):
            sources = st.session_state["sources"][i]
            if sources:
                render_sources(sources)

    # Input de usuario
    user_input = st.chat_input("Escribe tu pregunta...")

    if user_input:
        # Obtener contexto del prompt si existe
        prompt_context = st.session_state.get("prompt_context", "")
        
        # Construir la consulta final con contexto
        if prompt_context:
            final_query = f"{prompt_context}\n\nPregunta: {user_input}"
            log_info(f"🎯 Aplicando contexto de prompt: '{prompt_context[:50]}{'...' if len(prompt_context) > 50 else ''}'")
        else:
            final_query = user_input
        
        # Log de inicio de consulta
        log_info(f"🔄 Nueva consulta iniciada: '{user_input[:50]}{'...' if len(user_input) > 50 else ''}'")
        
        # Agregar mensaje del usuario al historial (mostrar solo la pregunta original)
        st.session_state["messages"].append({"role": "user", "content": user_input})
        
        # Spinner más informativo para latencia
        with st.spinner("🤔 Procesando consulta... (puede tomar hasta 2 minutos)"):
            log_info("📡 Enviando consulta al RAG API...")
            response = query_rag_api(final_query)
            
        if response and response.get("answer"):
            log_success("✅ Respuesta recibida exitosamente")
            bot_msg = response["answer"]
            # Guardar sources si están disponibles
            sources = response.get("sources", [])
            if sources:
                log_info(f"📚 Fuentes encontradas: {len(sources)} documentos")
            st.session_state["sources"].append(sources)
        else:
            log_warning("⏰ Timeout después de múltiples intentos")
            bot_msg = """⏰ **La consulta tardó demasiado tiempo**

**Posibles causas:**
- Consulta muy amplia o compleja
- Servidor bajo alta carga
- Problemas de conectividad

**Sugerencias:**
- Reformula la pregunta de forma más específica
- Divide consultas complejas en partes más pequeñas
- Intenta nuevamente en unos minutos

*El sistema intentó 3 veces automáticamente.*"""
            st.session_state["sources"].append([])
            
        # Agregar respuesta del bot al historial
        st.session_state["messages"].append({"role": "bot", "content": bot_msg})
        log_info("💬 Mensaje agregado al historial")
        st.rerun()

def clear_chat_history():
    """Limpia el historial de chat."""
    if "messages" in st.session_state:
        st.session_state["messages"] = []
    if "sources" in st.session_state:
        st.session_state["sources"] = []
    log_info("🗑️ Historial de chat limpiado") 