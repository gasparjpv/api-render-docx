from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from docxtpl import DocxTemplate
import os, uuid
import asyncio

app = FastAPI()

OUTPUT_DIR = "generated"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/gerar-documento")
async def gerar_documento(payload: dict, request: Request):
    try:
        # Espera para permitir aprovação no GPT
        await asyncio.sleep(2)

        # Carrega o template e renderiza
        doc = DocxTemplate("template.docx")
        doc.render(payload)

        # Gera nome único e salva
        filename = f"{uuid.uuid4().hex}.docx"
        output_path = os.path.join(OUTPUT_DIR, filename)
        doc.save(output_path)

        # Log para debug (Render mostra isso nos logs)
        print("✅ Documento salvo:", output_path)
        print("📁 Arquivos no diretório 'generated':", os.listdir(OUTPUT_DIR))

        # Monta URL de download com base no host real
        download_url = f"{request.base_url}download/{filename}"

        return {
            "message": "Documento gerado com sucesso.",
            "download_url": download_url
        }

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
