FROM registry.access.redhat.com/ubi9/python-312:1-25.1726696862

WORKDIR /opt/app-root/src

USER root

ENV TZ=America/Campo_Grande
ENV LOCAL_CERTIFICADO="/etc/pki/ca-trust/source/anchors/FAC.crt"
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=0

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm requirements.txt

USER 1001

COPY --chown=1001 . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]