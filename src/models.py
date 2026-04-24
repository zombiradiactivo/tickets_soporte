from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Optional


class CategoriaTicket(Enum):
    CUENTA = "cuenta"
    TECNICO = "tecnico"
    FACTURACION = "facturacion"
    PRODUCTO = "producto"
    OTRO = "otro"


class UrgenciaTicket(Enum):
    ALTA = "alta"
    MEDIA = "media"
    BAJA = "baja"


@dataclass
class TicketAnalizado:
    texto_original: str
    categoria: CategoriaTicket
    urgencia: UrgenciaTicket
    intencion: str
    accion_sugerida: str
    entidades: Dict = field(default_factory=dict)
    fecha_analisis: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        return {
            "texto_original": self.texto_original[:100] + "..." if len(self.texto_original) > 100 else self.texto_original,
            "categoria": self.categoria.value,
            "urgencia": self.urgencia.value,
            "intencion": self.intencion,
            "accion_sugerida": self.accion_sugerida,
            "entidades": self.entidades,
            "fecha_analisis": self.fecha_analisis.isoformat()
        }
