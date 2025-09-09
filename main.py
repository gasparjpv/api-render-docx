from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from docxtpl import DocxTemplate
import os, uuid

app = FastAPI()

# Diretório onde os arquivos gerados serão salvos
OUTPUT_DIR = "generated"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/gerar-documento")
async def gerar_documento(payload: dict):
    try:
        # Carrega o template (deve estar na raiz do projeto)
        doc = DocxTemplate("template.docx")

        # Preenche o documento com os dados do payload
        doc.render(payload)

        # Gera um nome único com extensão .docx
        filename = f"{uuid.uuid4().hex}.docx"
        output_path = os.path.join(OUTPUT_DIR, filename)
        doc.save(output_path)

        # Logs de debug (opcional)
        print("📁 Documento gerado em:", output_path)
        print("📂 Conteúdo da pasta generated/:", os.listdir(OUTPUT_DIR))

        # Retorna a URL pública para o GPT ou usuário final
        return {
            "message": "Documento gerado com sucesso.",
            "download_url": f"https://api-render-docx.onrender.com/download/{filename}"
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
