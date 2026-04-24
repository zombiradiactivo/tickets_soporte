# Guía de Testing

## Estructura de Tests

```
tests/
├── __init__.py
├── test_preprocess.py    # Tests de preprocesamiento
├── test_nlp_analyzer.py  # Tests de análisis NLP
├── test_actions.py       # Tests de acciones
└── test_pipeline.py      # Tests de integración del pipeline
```

## Ejecutar Tests

### Todos los tests
```bash
python -m pytest tests/ -v
```

### Con cobertura
```bash
python -m pytest tests/ --cov=src --cov-report=term-missing --cov-report=html
```

### Tests específicos
```bash
# Solo tests de preprocess
python -m pytest tests/test_preprocess.py -v

# Un test específico
python -m pytest tests/test_pipeline.py::test_pipeline_procesar -v
```

## Cobertura Actual

| Módulo | Statements | Miss | Coverage |
|--------|------------|------|----------|
| src/__init__.py | 0 | 0 | 100% |
| src/models.py | 20 | 1 | 95% |
| src/preprocess.py | 12 | 0 | 100% |
| src/nlp_analyzer.py | 43 | 8 | 81% |
| src/pipeline.py | 48 | 0 | 100% |
| src/actions.py | 36 | 10 | 72% |
| **TOTAL** | **159** | **19** | **88%** |

## Escribir Nuevos Tests

### Ejemplo: Test de Preprocess

```python
import pytest
from src.preprocess import Preprocessor

def test_preprocesar_elimina_html():
    p = Preprocessor()
    resultado = p.preprocesar("<b>hola</b>")
    assert "<b>" not in resultado
    assert "hola" in resultado
```

### Ejemplo: Test de NLPAnalyzer con Mock

```python
import json
import pytest
import requests_mock
from src.nlp_analyzer import NLPAnalyzer

def test_analizar_exito():
    analyzer = NLPAnalyzer()
    respuesta = {
        "message": {
            "content": json.dumps({
                "categoria": "cuenta",
                "urgencia": "alta",
                "intencion": "test",
                "accion_sugerida": "test"
            })
        }
    }
    with requests_mock.Mocker() as m:
        m.post(f"{analyzer.api_url}", json=respuesta)
        resultado = analyzer.analizar("test")
    assert resultado["exito"] is True
```

## Mocks Disponibles

Para tests que no requieren Ollama ejecutándose:

```python
class MockAnalyzer:
    def analizar(self, texto):
        return {"exito": True, "analisis": {
            "categoria": "cuenta",
            "urgencia": "alta",
            "intencion": "test",
            "accion_sugerida": "test"
        }}
```

## CI/CD

Los tests se ejecutan automáticamente en GitHub Actions para:
- Python 3.10, 3.11, 3.12
- Linting con pylint
- Type checking con mypy
- Reporte de cobertura a Codecov
