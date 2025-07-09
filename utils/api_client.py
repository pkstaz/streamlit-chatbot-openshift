# Cliente para RAG API 
import requests
import logging
import time
from config import RAG_API_URL, API_TIMEOUT

# Configuración básica de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)

# Icon-based log helpers
def log_success(msg):
    logger.info(f"✅ {msg}")

def log_warning(msg):
    logger.warning(f"⚠️ {msg}")

def log_error(msg):
    logger.error(f"❌ {msg}")

def log_info(msg):
    logger.info(f"ℹ️ {msg}")


def health_check():
    url = f"{RAG_API_URL}/health"
    try:
        log_info(f"Checking health at {url}")
        resp = requests.get(url, timeout=API_TIMEOUT)
        if resp.status_code == 200:
            log_success("API is healthy!")
            return True
        else:
            log_warning(f"Health check failed: {resp.status_code}")
            return False
    except Exception as e:
        log_error(f"Health check error: {e}")
        return False

def ready_check():
    url = f"{RAG_API_URL}/ready"
    try:
        log_info(f"Checking readiness at {url}")
        resp = requests.get(url, timeout=API_TIMEOUT)
        if resp.status_code == 200:
            log_success("API is ready!")
            return True
        else:
            log_warning(f"Ready check failed: {resp.status_code}")
            return False
    except Exception as e:
        log_error(f"Ready check error: {e}")
        return False

def query_rag_api(query, top_k=3, max_retries=3):
    url = f"{RAG_API_URL}/api/v1/query"
    payload = {"question": query, "top_k": top_k}
    
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                log_info(f"🔄 Reintento {attempt + 1}/{max_retries}")
                time.sleep(2)  # Esperar 2 segundos entre reintentos
            
            log_info(f"Sending query to RAG API: {payload}")
            resp = requests.post(url, json=payload, timeout=API_TIMEOUT)
            
            if resp.status_code == 200:
                log_success("Query successful!")
                return resp.json()
            elif resp.status_code == 504:  # Gateway Timeout
                log_warning(f"Query timeout (attempt {attempt + 1}/{max_retries}): {resp.status_code}")
                if attempt == max_retries - 1:
                    log_error("All retry attempts failed due to timeout")
                    return None
                continue
            else:
                log_warning(f"Query failed: {resp.status_code} - {resp.text}")
                return None
                
        except requests.exceptions.Timeout:
            log_warning(f"Request timeout (attempt {attempt + 1}/{max_retries})")
            if attempt == max_retries - 1:
                log_error("All retry attempts failed due to timeout")
                return None
            continue
        except Exception as e:
            log_error(f"Query error: {e}")
            return None
    
    return None 