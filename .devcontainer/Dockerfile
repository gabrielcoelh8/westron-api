FROM registry.access.redhat.com/ubi9/python-312:9.5-1736338296
# acompanhar atualizações da versão em:
# https://catalog.redhat.com/software/containers/ubi9/python-312/657b08d023df896ebfacf402

# 0 para escrever arquivos .pyc no disco. 1 caso contrário
ENV PYTHONDONTWRITEBYTECODE 1

# Mostra a saída sem armazenar em buffer
ENV PYTHONUNBUFFERED 1

USER root

WORKDIR /opt/app-root/src

ENV TZ=America/Campo_Grande

COPY .devcontainer/requirements.txt /tmp/pip-tmp/

RUN pip install --upgrade pip && \ 
    pip install -r /tmp/pip-tmp/requirements.txt && \
    rm -rf /tmp/pip-tmp

USER default