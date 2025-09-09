from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from docxtpl import DocxTemplate
import os, uuid

app = FastAPI()
OUTPUT_DIR = "generated"
os.makedirs(OUTPUT_DIR, exist_ok=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "template.docx")

@app.post("/gerar-documento-arquivo")
async def gerar_documento_arquivo(payload: dict, request: Request):
    try:
        doc = DocxTemplate(TEMPLATE_PATH)  # template precisa estar no mesmo diretório do main.py
        doc.render(payload)

        filename = f"{uuid.uuid4().hex}.docx"
        path = os.path.join(OUTPUT_DIR, filename)
        doc.save(path)

        # monta a URL de download (baseada no host da requisição)
        base_url = str(request.base_url).rstrip("/")
        download_url = f"{base_url}/download/{filename}"

        return JSONResponse(content={
            "message": "Documento gerado com sucesso.",
            "download_url": download_url
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/download/{filename}")
async def download(filename: str):
    path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(path):
        return JSONResponse(status_code=404, content={"error": "Arquivo não encontrado."})

    return FileResponse(
        path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename="documento_gerado.docx"
    )
