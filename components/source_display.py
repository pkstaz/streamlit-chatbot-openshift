# Display de sources 

import streamlit as st

def render_sources(sources, response_metadata=None):
    """Renderiza las fuentes del RAG API de forma elegante."""
    
    if not sources:
        return
    
    st.markdown("---")
    st.markdown("### 📚 Fuentes consultadas")
    
    # Mostrar metadata de la respuesta si está disponible
    if response_metadata:
        with st.expander("📊 Información de la consulta", expanded=False):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Modelo", response_metadata.get("model", "N/A"))
            with col2:
                st.metric("Latencia", f"{response_metadata.get('latency_ms', 0)}ms")
            with col3:
                st.metric("Fuentes", len(sources))
    
    # Mostrar cada fuente
    for i, source in enumerate(sources):
        with st.expander(f"📄 Fuente {i+1} - Score: {source.get('score', 0):.2f}", expanded=False):
            st.markdown(f"**ID:** {source.get('id', 'N/A')}")
            st.markdown(f"**Texto:** {source.get('text', 'N/A')}")
            
            # Mostrar metadata si está disponible
            metadata = source.get('metadata', {})
            if metadata:
                st.markdown("**Metadata:**")
                for key, value in metadata.items():
                    st.markdown(f"- **{key}:** {value}")

def render_simple_sources(sources):
    """Renderiza las fuentes de forma simple para respuestas rápidas."""
    
    if not sources:
        return
    
    st.markdown("---")
    st.markdown("**📚 Fuentes:**")
    for i, source in enumerate(sources[:3]):  # Solo mostrar las primeras 3
        st.markdown(f"{i+1}. {source.get('text', 'N/A')[:100]}...") 