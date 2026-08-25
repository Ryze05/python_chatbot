# Ollama Project

## Descripción

**Ollama Project** es un asistente interactivo de matemáticas que se conecta a un servidor Ollama local para proporcionar respuestas educativas estructuradas. La aplicación está construida con Python y utiliza la librería `rich` para una interfaz de terminal atractiva.

## Características

- ✅ Interfaz de terminal bonita con `rich`
- ✅ Asistente de matemáticas con system prompt dedicado
- ✅ Commands interactivos: `/help`, `/clear`, `/history`, `/save`
- ✅ Respuestas en tiempo real con streaming
- ✅ Guardado de historial de conversaciones a archivos Markdown
- ✅ Contexto configurable (últimos N mensajes)

## Comandos disponibles

| Comando | Descripción |
|---------|-------------|
| `/help` | Muestra este menú de ayuda |
| `/clear` | Limpia la memoria y reinicia la conversación |
| `/history` | Muestra el historial completo de la sesión |
| `/save` | Exporta la conversación actual a un archivo `.md` |
| `exit` | Cierra el asistente y sale del programa |

## Requisitos previos

- Python >= 3.14
- Ollama corriendo localmente en `http://localhost:11434`
- Modelo `llama3.2` disponible (o cambiar en `main.py`)

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/ollama-practice.git
   cd ollama-practice
   ```

2. Instala las dependencias:
   ```bash
   uv pip install -e .
   # o manualmente:
   pip install -r requirements.txt
   ```

3. Asegúrate de que Ollama esté corriendo:
   ```bash
   ollama serve
   ```

4. Ejecuta la aplicación:
   ```bash
   ollama-practice
   ```

## Estructura del proyecto

```
ollama-practice/
├── .venv/                # Entorno virtual
├── pyproject.toml        # Configuración del proyecto
├── uv.lock               # Lock file de dependencias
├── src/
│   └── ollama_practice/
│       ├── __init__.py   # Package init
│       ├── main.py       # Interfaz CLI principal
│       └── ollama_client.py  # Cliente de IA
└── README.md             # Este archivo
```

## Personalización

- Cambia el modelo editando `src/ollama_practice/main.py:130`
- Ajusta el contexto máximo en `src/ollama_practice/ollama_client.py:17`
- Modifica el system prompt en `main.py:102-128` para cambiar el comportamiento del asistente
