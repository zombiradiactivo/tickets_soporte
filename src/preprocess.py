import re
from typing import Dict, Optional


class Preprocessor:
    def __init__(self, max_caracteres: int = 10000):
        self.max_caracteres = max_caracteres

    def preprocesar(self, texto: str) -> str:
        texto = re.sub(r'<[^>]+>', '', texto)
        texto = re.sub(r'\s+', ' ', texto).strip()
        texto = re.sub(r'[\x00-\x1f\x7f]', '', texto)
        if len(texto) > self.max_caracteres:
            texto = texto[:self.max_caracteres] + "..."
        return texto
