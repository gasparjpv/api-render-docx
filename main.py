from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from docxtpl import DocxTemplate
import os, uuid
import asyncio

app = FastAPI()

OUTPUT_DIR = "generated"
os.makedirs(OUTPUT_DIR, exist_ok=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "template.docx")

@app.post("/gerar-documento")
async def gerar_documento(payload: dict, request: Request):
    await asyncio.sleep(5)  # Simula um delay
    try:
        doc = DocxTemplate(TEMPLATE_PATH)
        doc.render(payload)

        filename = f"{uuid.uuid4().hex}.docx"
        filepath = os.path.join(OUTPUT_DIR, filename)
        doc.save(filepath)

        # monta a URL pública se existir, senão usa a base do request
        PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "").rstrip("/")
        if PUBLIC_BASE_URL:
            download_url = f"{PUBLIC_BASE_URL}/download/{filename}"
        else:
            download_url = f"{request.base_url}download/{filename}"

        return {
            "message": "Documento gerado com sucesso.",
            "download_url": download_url
        }
    except Exception as e:
        return {"error": str(e)}


    except Exception as e:
        print("❌ Erro ao gerar documento:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/download/{filename}")
async def download(filename: str):
    path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(path):
        print("⚠️ Arquivo não encontrado:", path)
        return JSONResponse(status_code=404, content={"error": "Arquivo não encontrado."})

    return FileResponse(
        path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename="documento_gerado.docx"
    )
