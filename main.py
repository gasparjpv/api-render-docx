from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from docxtpl import DocxTemplate
import os, uuid
# import asyncio  # pode manter se quiser, mas recomendo tirar o sleep

app = FastAPI()
OUTPUT_DIR = "generated"
os.makedirs(OUTPUT_DIR, exist_ok=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "template.docx")

@app.post("/gerar-documento-arquivo")
async def gerar_documento_arquivo(payload: dict, request: Request):
    try:
        doc = DocxTemplate("template.docx")  # precisa estar junto do main.py :contentReference[oaicite:2]{index=2}
        doc.render(payload)
        filename = f"{uuid.uuid4().hex}.docx"
        path = os.path.join(OUTPUT_DIR, filename)
        doc.save(path)
        # devolve o binário direto
        return FileResponse(
            path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename="documento_gerado.docx"
        )
    except Exception as e:
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
