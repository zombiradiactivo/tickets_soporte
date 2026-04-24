# Guía de Instalación y Configuración

## Requisitos Previos

- Python 3.10 o superior
- 8GB RAM (para modelos de 7B) o 4GB RAM (para modelos de 3B)
- Ollama instalado

## Instalación Paso a Paso

### 1. Instalar Ollama

**Windows/Mac:**
Descarga desde https://ollama.ai

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Descargar Modelo

```bash
# Recomendado para español
ollama pull qwen2.5:7b

# Alternativas (menos RAM requerida)
ollama pull llama3.2:3b   # 4GB RAM
ollama pull phi3:mini       # 4GB RAM
```

### 3. Iniciar Servidor Ollama

```bash
ollama serve
```

Deja esta terminal abierta y usa otra para los siguientes pasos.

### 4. Clonar el Repositorio

```bash
git clone https://github.com/zombiradiactivo/tickets_soporte.git
cd tickets_soporte
```

### 5. Instalar Dependencias Python

```bash
pip install -r requirements.txt
```

### 6. Configurar Variables de Entorno (Opcional)

Crea un archivo `.env` (opcional):
```bash
# .env
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b
```

## Verificación

### Verificar Ollama
```bash
curl http://localhost:11434
# Debería responder con "Ollama is running"
```

### Verificar Modelo
```bash
ollama list
# Debería mostrar qwen2.5:7b en la lista
```

### Ejecutar Tests
```bash
python -m pytest tests/ -v
```

## Ejecución

### Aplicación de Consola
```bash
python app.py
```

### Interfaz Gráfica
```bash
python gui.py
```

## Modelos Disponibles

| Modelo | Tamaño | RAM | Velocidad | Calidad Español |
|--------|--------|-----|-----------|------------------|
| qwen2.5:7b | 7B | 8GB | Media | Excelente ⭐⭐⭐⭐⭐ |
| llama3.1:8b | 8B | 8GB | Media | Buena ⭐⭐⭐⭐ |
| mistral:7b | 7B | 8GB | Media | Buena ⭐⭐⭐⭐ |
| llama3.2:3b | 3B | 4GB | Rápida | Regular ⭐⭐⭐ |
| phi3:mini | 3.8B | 4GB | Muy Rápida | Regular ⭐⭐⭐ |

## Solución de Problemas

### Error: "No se pudo conectar a Ollama"
- Verifica que `ollama serve` esté ejecutándose
- Verifica que el puerto 11434 esté disponible

### Error: "model not found"
```bash
ollama pull qwen2.5:7b
```

### La interfaz gráfica no abre
```bash
pip install customtkinter
```
