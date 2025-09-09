from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from docxtpl import DocxTemplate
import os
import uuid

app = FastAPI()

# Cria a pasta para os documentos gerados (se não existir)
OUTPUT_DIR = "generated"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/gerar-documento")
async def gerar_documento(payload: dict):
    try:
        # Carrega o template
        template_path = "template.docx"
        if not os.path.exists(template_path):
            return JSONResponse(status_code=500, content={"error": "Arquivo template.docx não encontrado."})

        # Preenche o documento com os dados recebidos
        doc = DocxTemplate(template_path)
        doc.render(payload)

        # Gera nome único e salva o documento
        filename = f"{uuid.uuid4().hex}.docx"
        output_path = os.path.join(OUTPUT_DIR, filename)
        doc.save(output_path)

        # URL pública para download
        url_publica = f"https://api-render-docx.onrender.com/download/{filename}"

        return {
            "message": "Documento gerado com sucesso.",
            "download_url": url_publica
        }

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
