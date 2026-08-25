# 🤖 Math Assistant CLI (Ollama + Rich)

Asistente interactivo de matemáticas para la terminal que se conecta a un servidor local de **Ollama** a través del SDK compatible de **OpenAI**, ofreciendo explicaciones educativas paso a paso, fórmulas matemáticas formateadas y una interfaz moderna impulsada por **Rich**.

---

## ✨ Características Principales

* ⚡ **Streaming en tiempo real:** Renderizado fluido y progresivo de respuestas con soporte nativo de Markdown y bloques de código (`rich.Live`).
* 🧠 **Gestión eficiente de contexto (*Sliding Window*):** Conserva intacto el rol pedagógico (`system prompt`) mientras recorta el historial para no saturar la ventana de tokens.
* 🛡️ **Resiliencia ante fallos:** Captura explícita de excepciones de red y API (`APIConnectionError`, `APIStatusError`, `OpenAIError`) con mecanismo de *rollback* para no corromper el historial.
* ⚙️ **Configuración robusta y centralizada:** Gestión desacoplada mediante variables de entorno (`.env`) y `@dataclass(frozen=True)` con validación estricta *fail-fast*.
* 💾 **Persistencia de sesiones:** Exportación completa de conversaciones a archivos Markdown limpios (`/save`) con timestamps en formato UTC.
* 🎨 **Experiencia de usuario cuidada:** Paneles visuales, tablas interactivas, banners dinámicos y formateo de sintaxis en consola.

---

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.10+
* **Gestor de paquetes y entorno:** [uv](https://github.com/astral-sh/uv) (o pip)
* **Motor LLM:** [Ollama](https://ollama.com/) (Llama 3.2 por defecto)
* **Librerías principales:** `openai`, `rich`, `python-dotenv`

---

## ⌨️ Comandos Disponibles

| Comando | Descripción |
| :--- | :--- |
| `/help` | Muestra la tabla de ayuda con todos los comandos disponibles. |
| `/history` | Despliega el historial completo de la sesión actual en paneles dedicados. |
| `/save` | Exporta la conversación actual a un archivo `.md` dentro del directorio `history/`. |
| `/clear` | Limpia la memoria del chat y reinicia la conversación manteniendo el rol del sistema. |
| `exit` / `salir` | Cierra la sesión y finaliza la aplicación de forma segura. |

---

## 📋 Requisitos Previos

1. Tener **Python 3.10 o superior** instalado.
2. Tener [Ollama](https://ollama.com/) instalado y en ejecución en tu máquina:
   ```bash
   ollama serve
   ```
3. Descargar el modelo deseado (por ejemplo, `llama3.2`):
   ```bash
   ollama pull llama3.2
   ```

---

## 🚀 Instalación y Puesta en Marcha

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/ollama-practice.git](https://github.com/tu-usuario/ollama-practice.git)
   cd ollama-practice
   ```

2. **Instalar dependencias y preparar el entorno:**
   ```bash
   uv sync
   # O alternativamente con pip:
   # python -m venv .venv && source .venv/bin/activate && pip install -e .
   ```

3. **Configurar las variables de entorno:**
   Copia la plantilla de ejemplo y ajusta tus variables si es necesario:
   ```bash
   cp .env.example .env
   ```

   Valores por defecto en el archivo `.env`:
   ```env
   OLLAMA_BASE_URL="http://localhost:11434/v1"
   OLLAMA_API_KEY="ollama"
   OLLAMA_MODEL="llama3.2"
   OLLAMA_MAX_CONTEXT="8"
   OLLAMA_MAX_TOKENS="600"
   ```

4. **Ejecutar el asistente:**
   ```bash
   uv run ollama-practice
   ```

---

## 📂 Estructura del Proyecto

```text
ollama-practice/
├── src/
│   └── ollama_practice/
│       ├── __init__.py       # Punto de entrada del paquete
│       ├── config.py         # Configuración centralizada vía @dataclass y .env
│       ├── main.py           # CLI interactiva, bucle principal y banners de Rich
│       └── ollama_client.py  # Wrapper del cliente OpenAI, streaming y contexto
├── history/                  # Conversaciones exportadas en formato .md
├── .env.example              # Plantilla pública de variables de entorno
├── .gitignore                # Archivos ignorados por Git (.env, .venv, history/)
├── pyproject.toml            # Metadatos del proyecto y dependencias
└── README.md                 # Documentación técnica del proyecto
```

---

## 🔧 Personalización

* **Cambiar de modelo o parámetros:** Ajusta los valores de `OLLAMA_MODEL`, `OLLAMA_MAX_CONTEXT` o `OLLAMA_MAX_TOKENS` directamente en tu archivo `.env` sin tocar el código fuente.
* **Modificar el comportamiento pedagógico:** Edita la variable `system_prompt` en `src/ollama_practice/main.py` para adaptar el asistente a otros roles (física, programación, idiomas, etc.).
