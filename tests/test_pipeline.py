import json
import pytest
import requests_mock
from src.pipeline import Pipeline
from src.models import TicketAnalizado, CategoriaTicket, UrgenciaTicket
from src.preprocess import Preprocessor
from src.nlp_analyzer import NLPAnalyzer
from src.actions import ActionExecutor


class MockAnalyzer:
    def analizar(self, texto):
        return {"exito": True, "analisis": {
            "categoria": "cuenta",
            "urgencia": "alta",
            "intencion": "recuperar acceso",
            "accion_sugerida": "resetear contraseña"
        }}


class MockActionExecutor:
    def ejecutar(self, ticket):
        pass


def test_pipeline_procesar():
    pipeline = Pipeline(analyzer=MockAnalyzer(), action_executor=MockActionExecutor())
    ticket = pipeline.procesar("No puedo entrar a mi cuenta")
    assert ticket is not None
    assert ticket.categoria == CategoriaTicket.CUENTA
    assert ticket.urgencia == UrgenciaTicket.ALTA


def test_pipeline_error():
    class FailingAnalyzer:
        def analizar(self, texto):
            return {"exito": False, "error": "fail"}
    pipeline = Pipeline(analyzer=FailingAnalyzer(), action_executor=MockActionExecutor())
    ticket = pipeline.procesar("test")
    assert ticket is None


def test_pipeline_lote():
    pipeline = Pipeline(analyzer=MockAnalyzer(), action_executor=MockActionExecutor())
    resultados = pipeline.procesar_lote(["ticket 1", "ticket 2"])
    assert len(resultados) == 2
