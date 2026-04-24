import logging
from typing import List, Optional

from src.models import TicketAnalizado, CategoriaTicket, UrgenciaTicket
from src.preprocess import Preprocessor
from src.nlp_analyzer import NLPAnalyzer
from src.actions import ActionExecutor

logger = logging.getLogger(__name__)


class Pipeline:
    def __init__(self, analyzer: NLPAnalyzer, preprocessor: Optional[Preprocessor] = None, action_executor: Optional[ActionExecutor] = None):
        self.preprocessor = preprocessor or Preprocessor()
        self.analyzer = analyzer
        self.action_executor = action_executor or ActionExecutor()

    def procesar(self, texto_usuario: str) -> Optional[TicketAnalizado]:
        print("\n" + "=" * 70)
        print("🚀 PIPELINE DE PROCESAMIENTO NLP")
        print("=" * 70)

        print("\n📥 PASO 1: PREPROCESAMIENTO")
        texto_limpio = self.preprocessor.preprocesar(texto_usuario)
        print(f"   Texto original: {texto_usuario[:100]}...")
        print(f"   Texto limpio: {texto_limpio[:100]}...")

        print("\n🤖 PASO 2: ANÁLISIS CON IA (Ollama)")
        resultado = self.analyzer.analizar(texto_usuario)

        if not resultado["exito"]:
            print(f"   ❌ Error: {resultado.get('error')}")
            return None

        print(f"   ✅ Análisis completado")

        print("\n🔄 PASO 3: TRANSFORMACIÓN")
        ticket = self._transformar(texto_usuario, resultado)
        print(f"   Categoría: {ticket.categoria.value}")
        print(f"   Urgencia: {ticket.urgencia.value}")

        print("\n⚡ PASO 4: EJECUCIÓN DE ACCIONES")
        self.action_executor.ejecutar(ticket)

        return ticket

    def procesar_lote(self, tickets: List[str]) -> List[TicketAnalizado]:
        resultados = []
        for i, ticket in enumerate(tickets, 1):
            print(f"\n📝 Procesando ticket {i}/{len(tickets)}")
            resultado = self.procesar(ticket)
            if resultado:
                resultados.append(resultado)
        return resultados

    def _transformar(self, texto_usuario: str, resultado_api: dict) -> TicketAnalizado:
        analisis = resultado_api.get("analisis", {})

        categoria_map = {c.value: c for c in CategoriaTicket}
        urgencia_map = {u.value: u for u in UrgenciaTicket}

        categoria = categoria_map.get(analisis.get("categoria", "otro"), CategoriaTicket.OTRO)
        urgencia = urgencia_map.get(analisis.get("urgencia", "media"), UrgenciaTicket.MEDIA)

        return TicketAnalizado(
            texto_original=texto_usuario,
            categoria=categoria,
            urgencia=urgencia,
            intencion=analisis.get("intencion", "No especificada"),
            accion_sugerida=analisis.get("accion_sugerida", "Revisar manualmente"),
            entidades=analisis.get("entidades", {})
        )
