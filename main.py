from fastapi import FastAPI, Response
from pydantic import BaseModel
from docxtpl import DocxTemplate
import io
import os

app = FastAPI()

# MODELOS DE DADOS
class Etapa(BaseModel):
    numero: str
    titulo: str
    itens: list[str]

class Topico(BaseModel):
    titulo: str
    descricao: str

class DadosDocx(BaseModel):
    cenarioAtual: str
    objetivoDosServicos: str
    solucaoProposta: list[Etapa]
    escopoDeAtividades: str
    premissasExecucao: str
    cronogramaMacro: list[Topico]
    suposicoes: str
    foraDoEscopo: str

# ENDPOINT
@app.post("/gerar-documento")
def gerar_documento(dados: DadosDocx):
    # Caminho para o template (deve estar na raiz do projeto)
    template_path = "template.docx"

    # Gera o documento preenchido
    doc = DocxTemplate(template_path)
    doc.render(dados.dict())

    # Salva em memória (em vez de arquivo)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    return Response(
        content=buffer.read(),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=documento-preenchido.docx"}
    )
