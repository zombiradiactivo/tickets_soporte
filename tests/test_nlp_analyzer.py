import json
import pytest
import requests
import requests_mock
from config.config import MODEL_NAME
from src.nlp_analyzer import NLPAnalyzer


def test_analizar_exito():
    analyzer = NLPAnalyzer(model=MODEL_NAME)
    respuesta = {
        "message": {
            "content": json.dumps({
                "categoria": "cuenta",
                "urgencia": "alta",
                "intencion": "recuperar acceso",
                "accion_sugerida": "resetear contraseña"
            })
        }
    }
    with requests_mock.Mocker() as m:
        m.post(f"{analyzer.api_url}", json=respuesta)
        resultado = analyzer.analizar("No puedo entrar")
    assert resultado["exito"] is True
    assert resultado["analisis"]["categoria"] == "cuenta"


def test_analizar_conexion_error():
    analyzer = NLPAnalyzer()
    with requests_mock.Mocker() as m:
        m.post(f"{analyzer.api_url}", exc=requests.exceptions.ConnectionError)
        resultado = analyzer.analizar("test")
    assert resultado["exito"] is False
    assert "Ollama" in resultado["error"]


def test_analizar_categoria_invalida():
    analyzer = NLPAnalyzer()
    respuesta = {
        "message": {
            "content": json.dumps({
                "categoria": "invalida",
                "urgencia": "media",
                "intencion": "test",
                "accion_sugerida": "test"
            })
        }
    }
    with requests_mock.Mocker() as m:
        m.post(f"{analyzer.api_url}", json=respuesta)
        resultado = analyzer.analizar("test")
    assert resultado["analisis"]["categoria"] == "otro"


def test_analizar_json_malformado():
    analyzer = NLPAnalyzer()
    respuesta = {"message": {"content": "no es json"}}
    with requests_mock.Mocker() as m:
        m.post(f"{analyzer.api_url}", json=respuesta)
        resultado = analyzer.analizar("test")
    assert resultado["exito"] is False
