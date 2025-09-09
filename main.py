from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from docxtpl import DocxTemplate
import os

app = FastAPI()

# Configuração de CORS (se for necessário para testes locais ou GPT Actions)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, use domínio restrito
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/gerar-documento")
async def gerar_documento(payload: dict):
    try:
        # Carrega o template (certifique-se de que template.docx está na raiz do projeto)
        doc = DocxTemplate("template.docx")

        # Renderiza o template com os dados recebidos
        doc.render(payload)

        # Caminho de saída do documento gerado
        output_path = "ultimo.docx"
        doc.save(output_path)

        # Retorna link de download
        return {
            "message": "Documento gerado com sucesso.",
            "download_url": "/download/ultimo"
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/download/ultimo")
async def download_documento():
    file_path = "ultimo.docx"
    if not os.path.exists(file_path):
        return JSONResponse(status_code=404, content={"detail": "Not Found"})

    return FileResponse(
        file_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename="proposta_tecnica.docx"
    )

@app.post("/gerar-documento")
async def gerar_documento(payload: dict):
    doc = DocxTemplate("template.docx")
    doc.render(payload)
    doc.save("ultimo.docx")
    return {"message": "Documento gerado com sucesso.", "download_url": "/download/ultimo"}
