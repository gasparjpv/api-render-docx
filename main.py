from fastapi import FastAPI, Response
from pydantic import BaseModel
from docxtpl import DocxTemplate
import io

app = FastAPI()

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

@app.post("/gerar-documento")
def gerar_documento(dados: DadosDocx):
    doc = DocxTemplate("template.docx")
    doc.render(dados.dict())

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    return Response(
        content=buffer.read(),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=documento.docx"}
    )
