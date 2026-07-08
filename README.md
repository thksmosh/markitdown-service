# 🔄 MarkItDown Service

Microservicio FastAPI que convierte documentos (PDF, Word, Excel, PowerPoint, CSV) a Markdown optimizado para consumo de agentes de IA. Diseñado para integrarse con flujos de n8n y reducir el consumo de tokens al preprocesar archivos antes de enviarlos a Claude o GPT.

---

## 📐 Arquitectura

```
WhatsApp
    ↓
   n8n
    ↓
┌─────────────────┐        ┌─────────────────────┐
│  Imagen / Audio │───────▶│   Agente IA          │
│  (directo)      │        │   (Claude / GPT)     │
└─────────────────┘        └─────────────────────┘
                                    ▲
┌─────────────────┐        ┌────────┴────────────┐
│  PDF / Word     │───────▶│  MarkItDown Service  │
│  Excel / CSV    │        │  (este microservicio)│
└─────────────────┘        └─────────────────────┘
```

> Las imágenes y audios se envían **directamente** al agente de IA aprovechando su capacidad de visión y transcripción nativa. Los documentos pasan primero por este servicio para ser convertidos a Markdown eficiente en tokens.

---

## 🚀 Endpoints

### `POST /convert`
Convierte un archivo a Markdown.

**Request:** `multipart/form-data`

| Campo | Tipo   | Requerido | Descripción          |
|-------|--------|-----------|----------------------|
| file  | File   | ✅        | Archivo a convertir  |

**Formatos soportados:**

| Extensión | Formato          |
|-----------|------------------|
| `.pdf`    | PDF              |
| `.docx`   | Word             |
| `.xlsx`   | Excel (nuevo)    |
| `.xls`    | Excel (antiguo)  |
| `.pptx`   | PowerPoint       |
| `.csv`    | CSV              |

**Response `200`:**
```json
{
  "filename": "documento.pdf",
  "markdown": "# Título\n\nContenido extraído en Markdown..."
}
```

**Response `415`:**
```json
{
  "detail": "Tipo de archivo no soportado: .mp4"
}
```

---

### `GET /health`
Verifica que el servicio está activo.

**Response `200`:**
```json
{
  "status": "ok"
}
```

---

### `GET /docs`
Interfaz Swagger UI interactiva para probar los endpoints manualmente.

---

## 🛠️ Stack

| Componente    | Tecnología                        |
|---------------|-----------------------------------|
| Framework     | FastAPI                           |
| Servidor      | Uvicorn                           |
| Conversión    | MarkItDown (Microsoft)            |
| Lenguaje      | Python 3.13                       |
| Deploy        | Railway (sin Docker)              |
| CI/CD         | GitHub → Railway (auto-deploy)    |

---

## 📦 Instalación local

### Prerrequisitos
- Python 3.10+
- pip

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/thksmosh/markitdown-service.git
cd markitdown-service

# 2. Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Correr el servidor
uvicorn main:app --reload
```

El servicio estará disponible en `http://localhost:8000`

---

## 🌐 Producción

| Detalle     | Valor                                          |
|-------------|------------------------------------------------|
| URL base    | `https://web-production-65dc2.up.railway.app`  |
| Health      | `/health`                                      |
| Docs        | `/docs`                                        |
| Deploy      | Automático al hacer push a `main`              |
| Plataforma  | Railway — Hobby Plan ($5/mes)                  |

---

## 🔌 Integración con n8n

### Nodo HTTP Request — Configuración

| Campo           | Valor                                                        |
|-----------------|--------------------------------------------------------------|
| Method          | `POST`                                                       |
| URL             | `https://web-production-65dc2.up.railway.app/convert`        |
| Body Type       | `Form Data (Multipart)`                                      |
| Campo `file`    | Binary data del archivo recibido por WhatsApp                |

### Flujo recomendado en n8n

```
[Webhook WhatsApp]
        ↓
[Switch por MIME type]
        ├── image/* / audio/*  ──────────────▶ [Agente IA directamente]
        │
        └── application/pdf
            application/vnd.openxmlformats*
            text/csv             ────────────▶ [POST /convert]
                                                      ↓
                                              [Set: prompt con markdown]
                                                      ↓
                                              [Agente IA]
```

### Ejemplo de expresión n8n para el prompt

```
Contexto del documento enviado por el cliente:

{{ $json.markdown }}

Pregunta del cliente: {{ $('Webhook').item.json.body.text }}
```

---

## 🔒 Seguridad

- Solo acepta extensiones explícitamente permitidas (whitelist)
- Usa `convert_local()` en lugar de `convert()` para evitar acceso a URIs remotas
- Los archivos temporales se eliminan inmediatamente después de la conversión
- No almacena ningún archivo ni dato del usuario

---

## 📁 Estructura del proyecto

```
markitdown-service/
├── main.py              # FastAPI app — lógica principal
├── requirements.txt     # Dependencias Python
├── Procfile             # Comando de inicio para Railway
├── .gitignore           # Exclusiones de Git
└── README.md            # Este archivo
```

---

## 🧩 Contexto del proyecto

Este microservicio forma parte del ecosistema **StarkComApi**, una plataforma SaaS de facturación electrónica (DTE) para micro y pequeñas empresas en El Salvador. El flujo completo permite a los clientes enviar documentos por WhatsApp, los cuales son procesados y analizados por agentes de IA para asistir en la generación de facturas electrónicas cumpliendo con los requisitos del Ministerio de Hacienda.

**Repositorios relacionados:**
- `StarkComApi` — Backend principal (.NET Core 10, Clean Architecture)
- `markitdown-service` — Este microservicio (Python, FastAPI)

---

## 📄 Licencia

Uso privado — StarkCom © 2026
