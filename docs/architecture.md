# Arquitectura del Sistema

## Visión General

El Sistema de Análisis de Tickets de Soporte es una aplicación modular que utiliza NLP local (Ollama) para clasificar y procesar tickets de soporte automáticamente.

## Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                     INTERFAZ DE USUARIO                      │
│  ┌──────────────┐              ┌──────────────┐            │
│  │   app.py     │              │   gui.py     │            │
│  │ (Consola)    │              │  (CustomTk)  │            │
│  └──────┬───────┘              └──────┬───────┘            │
└─────────┼─────────────────────────────┼────────────────────┘
          │                             │
          └─────────────┬───────────────┘
                        │
          ┌─────────────▼────────────────┐
          │      src/pipeline.py          │
          │      (Orquestador)           │
          └──────┬──────────┬───────────┘
                 │          │
      ┌──────────▼──┐  ┌───▼──────────┐
      │ Preprocess  │  │ NLPAnalyzer  │
      │ (Limpieza) │  │  (Ollama)    │
      └─────────────┘  └──────┬───────┘
                               │
                    ┌──────────▼───────┐
                    │  models.py       │
                    │ (TicketAnalizado)│
                    └──────────┬───────┘
                               │
                    ┌──────────▼───────┐
                    │ ActionExecutor   │
                    │ (Acciones)       │
                    └──────────────────┘
```

## Componentes Principales

### 1. Pipeline (`src/pipeline.py`)
Orquesta el flujo completo de procesamiento:
1. Preprocesamiento del texto
2. Análisis con NLP (Ollama)
3. Transformación a objeto TicketAnalizado
4. Ejecución de acciones

### 2. Preprocessor (`src/preprocess.py`)
Limpia y normaliza el texto:
- Elimina HTML
- Normaliza espacios
- Elimina caracteres de control
- Trunca textos largos

### 3. NLPAnalyzer (`src/nlp_analyzer.py`)
Comunicación con Ollama API:
- Envía prompts al modelo local
- Parsea respuestas JSON
- Maneja errores de conexión

### 4. Models (`src/models.py`)
Clases de datos:
- `TicketAnalizado`: Resultado del análisis
- `CategoriaTicket`: Enum (cuenta, tecnico, facturacion, producto, otro)
- `UrgenciaTicket`: Enum (alta, media, baja)

### 5. ActionExecutor (`src/actions.py`)
Ejecuta acciones según categoría y urgencia del ticket.

## Flujo de Datos

```
Texto del ticket
       │
       ▼
[Preprocessor] → Texto limpio
       │
       ▼
[NLPAnalyzer] → JSON con categoría, urgencia, intención, acción
       │
       ▼
[Pipeline.transformar] → Objeto TicketAnalizado
       │
       ▼
[ActionExecutor] → Acciones en consola/UI
```

## Inyección de Dependencias

El `Pipeline` recibe sus dependencias por constructor:

```python
pipeline = Pipeline(
    analyzer=NLPAnalyzer(),
    preprocessor=Preprocessor(),
    action_executor=ActionExecutor()
)
```

Esto permite:
- Fácil testing con mocks
- Cambiar implementaciones sin modificar el pipeline
- Mayor modularidad
