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

# Instala o certifi
RUN pip install certifi

# Esta configuração é necessária apenas usando DevContainer e não deve ser utilizada em produção
RUN curl -k -SL https://satellite.mpms.mp.br/pub/FAC.crt -o /etc/pki/ca-trust/source/anchors/FAC.crt && \
    chmod -R 755 /etc/pki/ca-trust/source/anchors/ && \
    chmod -R 755 /etc/pki/ca-trust/extracted/openssl/ && \
    update-ca-trust

# Anexa o certificado ao certifi para que o Python o reconheça
RUN CERTIFI_CA=$(python -m certifi) && \
    cat /etc/pki/ca-trust/source/anchors/FAC.crt >> $CERTIFI_CA

# Configurações do Oracle
RUN yum update -y && \
    yum install -y libaio unzip && \
    mkdir -p /opt/oracle && \
    wget https://download.oracle.com/otn_software/linux/instantclient/2113000/instantclient-basic-linux.x64-21.13.0.0.0dbru.zip && \
    unzip -q instantclient-basic-linux.x64-21.13.0.0.0dbru.zip -d /opt/oracle && \
    rm instantclient-basic-linux.x64-21.13.0.0.0dbru.zip

COPY .devcontainer/requirements.txt /tmp/pip-tmp/

RUN pip install --upgrade pip && \ 
    pip install -r /tmp/pip-tmp/requirements.txt && \
    rm -rf /tmp/pip-tmp

USER default