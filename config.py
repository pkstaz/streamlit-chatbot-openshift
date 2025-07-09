import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env si existe
load_dotenv()

# Configuración principal
RAG_API_URL = os.getenv("RAG_API_URL", "http://localhost:8000")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", 10))

# Puedes agregar más settings aquí si es necesario


def get_settings():
    """Devuelve la configuración global de la app."""
    return {
        "RAG_API_URL": RAG_API_URL,
        "API_TIMEOUT": API_TIMEOUT,
    } 