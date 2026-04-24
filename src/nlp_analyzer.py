import json
import logging
from typing import Dict, Optional

import requests

from config.config import MODEL_NAME, OLLAMA_HOST
from src.models import CategoriaTicket, UrgenciaTicket

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
Eres un sistema de clasificación de tickets de soporte técnico.

Analiza el texto del usuario y devuelve ÚNICAMENTE un JSON con estos campos:
- categoria: una de ["cuenta", "tecnico", "facturacion", "producto", "otro"]
- urgencia: una de ["alta", "media", "baja"]
- intencion: descripción breve de qué quiere hacer el usuario
- accion_sugerida: qué debería hacer la aplicación (ej: "resetear contraseña", "escalar a tecnico", "reembolsar")
- entidades: objeto con información extraída como { "email": "...", "pedido_id": "...", "producto": "..." }

Reglas:
- Si el usuario menciona problemas de acceso/login/contraseña → categoria: "cuenta"
- Si menciona errores técnicos, bugs, la app no funciona → categoria: "tecnico"
- Si menciona pagos, facturas, reembolsos → categoria: "facturacion"
- Si menciona productos específicos, características → categoria: "producto"
- Urgencia alta si hay palabras como "urgente", "ya", "inmediatamente", "no funciona"
- No añadas texto fuera del JSON.
"""


class NLPAnalyzer:
    def __init__(self, base_url: str = OLLAMA_HOST, model: str = MODEL_NAME):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.api_url = f"{self.base_url}/api/chat"

    def analizar(self, texto: str) -> Dict:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": texto}
            ],
            "stream": False,
            "think":False,
            "options": {"temperature": 0.0, "num_predict": 300}
        }

        try:
            logger.info(f"Enviando solicitud a Ollama ({self.model})...")
            response = requests.post(self.api_url, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            respuesta_texto = data.get("message", {}).get("content", "")

            try:
                resultado = json.loads(respuesta_texto)
            except json.JSONDecodeError:
                import re
                match = re.search(r'\{.*\}', respuesta_texto, re.DOTALL)
                if match:
                    resultado = json.loads(match.group())
                else:
                    return {"exito": False, "error": "La API no devolvió JSON válido", "respuesta_raw": respuesta_texto}

            for campo in ["categoria", "urgencia", "intencion", "accion_sugerida"]:
                if campo not in resultado:
                    resultado[campo] = "desconocido"

            if resultado["categoria"] not in [c.value for c in CategoriaTicket]:
                resultado["categoria"] = "otro"
            if resultado["urgencia"] not in [u.value for u in UrgenciaTicket]:
                resultado["urgencia"] = "media"

            return {"exito": True, "analisis": resultado}

        except requests.exceptions.ConnectionError:
            return {"exito": False, "error": "No se pudo conectar a Ollama. ¿Ejecutaste 'ollama serve'?"}
        except requests.exceptions.Timeout:
            return {"exito": False, "error": "Timeout: El modelo tardó demasiado en responder."}
        except Exception as e:
            logger.error(f"Error en análisis NLP: {e}")
            return {"exito": False, "error": str(e)}
