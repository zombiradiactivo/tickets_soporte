import pytest
from src.preprocess import Preprocessor


def test_preprocesar_elimina_html():
    p = Preprocessor()
    assert "<b>" not in p.preprocesar("<b>hola</b>")


def test_preprocesar_elimina_espacios():
    p = Preprocessor()
    assert p.preprocesar("  hola   mundo  ") == "hola mundo"


def test_preprocesar_trunca():
    p = Preprocessor(max_caracteres=10)
    resultado = p.preprocesar("a" * 100)
    assert len(resultado) == 13
    assert resultado.endswith("...")


def test_preprocesar_vacio():
    p = Preprocessor()
    assert p.preprocesar("") == ""


def test_preprocesar_caracteres_control():
    p = Preprocessor()
    assert "\x00" not in p.preprocesar("hola\x00mundo")
