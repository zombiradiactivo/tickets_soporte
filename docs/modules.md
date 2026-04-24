# Documentación de Módulos

## src/models.py

### Enums

#### `CategoriaTicket`
```python
class CategoriaTicket(Enum):
    CUENTA = "cuenta"
    TECNICO = "tecnico"
    FACTURACION = "facturacion"
    PRODUCTO = "producto"
    OTRO = "otro"
```

#### `UrgenciaTicket`
```python
class UrgenciaTicket(Enum):
    ALTA = "alta"
    MEDIA = "media"
    BAJA = "baja"
```

### Clase TicketAnalizado

Representa un ticket después del análisis.

```python
@dataclass
class TicketAnalizado:
    texto_original: str
    categoria: CategoriaTicket
    urgencia: UrgenciaTicket
    intencion: str
    accion_sugerida: str
    entidades: Dict
    fecha_analisis: datetime
```

#### Métodos

**`to_dict() -> Dict`**
Convierte el ticket a diccionario para serialización JSON.

---

## src/preprocess.py

### Clase Preprocessor

```python
class Preprocessor:
    def __init__(self, max_caracteres: int = 10000)
    def preprocesar(self, texto: str) -> str
```

#### `preprocesar(texto: str) -> str`
Limpia el texto eliminando HTML, normalizando espacios y truncando si es necesario.

**Ejemplo:**
```python
preprocessor = Preprocessor()
texto_limpio = preprocessor.preprocesar("<p>Hola   mundo</p>")
# Resultado: "Hola mundo"
```

---

## src/nlp_analyzer.py

### Clase NLPAnalyzer

```python
class NLPAnalyzer:
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "qwen2.5:7b")
    def analizar(self, texto: str) -> Dict
```

#### `analizar(texto: str) -> Dict`
Envía el texto a Ollama y devuelve el análisis.

**Respuesta exitosa:**
```python
{
    "exito": True,
    "analisis": {
        "categoria": "cuenta",
        "urgencia": "alta",
        "intencion": "recuperar acceso",
        "accion_sugerida": "resetear contraseña",
        "entidades": {"email": "user@test.com"}
    }
}
```

**Respuesta con error:**
```python
{
    "exito": False,
    "error": "No se pudo conectar a Ollama..."
}
```

---

## src/actions.py

### Clase ActionExecutor

```python
class ActionExecutor:
    def ejecutar(self, ticket: TicketAnalizado) -> None
```

Imprime en consola las acciones sugeridas según la categoría y urgencia del ticket.

---

## src/pipeline.py

### Clase Pipeline

```python
class Pipeline:
    def __init__(
        self,
        analyzer: NLPAnalyzer,
        preprocessor: Optional[Preprocessor] = None,
        action_executor: Optional[ActionExecutor] = None
    )
    
    def procesar(self, texto_usuario: str) -> Optional[TicketAnalizado]
    def procesar_lote(self, tickets: List[str]) -> List[TicketAnalizado]
```

#### `procesar(texto_usuario: str) -> Optional[TicketAnalizado]`
Ejecuta el pipeline completo para un ticket individual.

#### `procesar_lote(tickets: List[str]) -> List[TicketAnalizado]`
Procesa múltiples tickets en lote.

**Ejemplo:**
```python
pipeline = Pipeline(analyzer=NLPAnalyzer())
ticket = pipeline.procesar("No puedo acceder a mi cuenta")
if ticket:
    print(f"Categoría: {ticket.categoria.value}")
```
