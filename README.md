# Predicción de retrasos en entregas

Aplicación web académica para el proyecto de clasificación binaria de `Late_delivery_risk`.

## Arquitectura
Formulario HTML → FastAPI → preprocesador guardado → `model.predict()` → resultado.

## Ejecutar localmente
Requiere Python 3.11.11.

```bash
python -m venv .venv
```

Windows:
```powershell
.venv\\Scripts\\Activate.ps1
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Instalar e iniciar:
```bash
pip install -r requirements.txt
uvicorn app:app --host 127.0.0.1 --port 8000
```

Abrir `http://127.0.0.1:8000`. Estado del servidor: `/health`.

## Despliegue en Render
1. En Render, crea un **New Web Service** y conecta este repositorio.
2. Render puede usar `render.yaml`; si configuras manualmente, usa:
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
3. Espera el despliegue y prueba la URL HTTPS asignada, tanto `/` como `/health` y el formulario.

## Nota metodológica
El modelo de referencia incluye `Days for shipping (real)`, una variable conocida después de la entrega. La aplicación demuestra la integración web del modelo académico, pero no debe interpretarse como predictor anticipatorio real de producción.
