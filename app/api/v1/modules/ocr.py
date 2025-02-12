from io import BytesIO
from json import dumps
from os import environ

from PIL import Image
import base64

from app.schemas.requests_ocr import ObjetoOCRRequest
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient


def obter_objeto_de_ocr_request(request: ObjetoOCRRequest) -> dict[str, str]:
    endpoint = environ.get('ENDPOINT')
    key = environ.get('KEY')
    imagem = request.imagem_base64

    imagem_bytes = base64.b64decode(imagem)
    buffer = BytesIO(imagem_bytes)
    imagem = Image.open(buffer)
    imagem.save(buffer, format='PNG')
    documento = buffer.getvalue()

    document_analysis_client = DocumentAnalysisClient(endpoint, AzureKeyCredential(key))
    poller = document_analysis_client.begin_analyze_document('prebuilt-read', documento)
    objeto_de_ocr = poller.result().to_dict()
    return {'objeto_de_ocr': dumps(objeto_de_ocr)}
