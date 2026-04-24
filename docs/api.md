# Referencia de API

## Respuesta del Modelo (JSON)

El modelo Ollama devuelve un JSON con la siguiente estructura:

```json
{
  "categoria": "cuenta",
  "urgencia": "alta",
  "intencion": "El usuario no puede acceder a su cuenta",
  "accion_sugerida": "resetear contraseña",
  "entidades": {
    "email": "usuario@ejemplo.com",
    "nombre": "Juan Pérez"
  }
}
```

### Campos

| Campo | Tipo | Valores Posibles | Descripción |
|-------|------|------------------|-------------|
| categoria | string | cuenta, tecnico, facturacion, producto, otro | Categoría del ticket |
| urgencia | string | alta, media, baja | Nivel de urgencia |
| intencion | string | - | Descripción de qué quiere el usuario |
| accion_sugerida | string | - | Qué acción debe tomarse |
| entidades | object | - | Datos extraídos del texto |

## Ollama API

### Endpoint: POST /api/chat

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "qwen2.5:7b",
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."}
  ],
  "stream": false,
  "options": {
    "temperature": 0.0,
    "num_predict": 300
  }
}'
```

### Respuesta

```json
{
  "model": "qwen2.5:7b",
  "created_at": "2024-...",
  "message": {
    "role": "assistant",
    "content": "{\"categoria\": \"...\", ...}"
  },
  "done": true,
  "total_duration": 1234567890,
  "load_duration": 1234567890,
  "prompt_eval_count": 50,
  "eval_count": 100
}
```

## TicketAnalizado (Dict)

Método `to_dict()` serializa el ticket:

```python
ticket_dict = {
    "texto_original": "No puedo entrar...",
    "categoria": "cuenta",
    "urgencia": "alta",
    "intencion": "recuperar acceso",
    "accion_sugerida": "resetear contraseña",
    "entidades": {"email": "..."},
    "fecha_analisis": "2024-01-01T12:00:00"
}
```

## Prompt del Sistema

```
Eres un sistema de clasificación de tickets de soporte técnico.

Analiza el texto del usuario y devuelve ÚNICAMENTE un JSON con estos campos:
- categoria: una de ["cuenta", "tecnico", "facturacion", "producto", "otro"]
- urgencia: una de ["alta", "media", "baja"]
- intencion: descripción breve de qué quiere hacer el usuario
- accion_sugerida: qué debería hacer la aplicación
- entidades: objeto con información extraída

Reglas:
- Si el usuario menciona problemas de acceso/login → categoria: "cuenta"
- Si menciona errores técnicos → categoria: "tecnico"
- Si menciona pagos/facturas → categoria: "facturacion"
- Urgencia alta si hay palabras como "urgente", "ya", "inmediatamente"
- No añadas texto fuera del JSON.
```
