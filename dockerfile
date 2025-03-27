FROM python:3.9-slim

WORKDIR /app

COPY . /app

# Set environment variables for IBM MQ client
ENV MQ_VERSION=9.4.0.10
ENV MQ_CLIENT_URL=https://public.dhe.ibm.com/ibmdl/export/pub/software/websphere/messaging/mqdev/redist/
ENV MQ_PACKAGE=9.4.0.10-IBM-MQC-Redist-LinuxX64.tar.gz 
ENV MQ_INSTALL_DIR=/opt/mqm

# Install required dependencies
RUN apt-get update && apt-get install -y \
    wget \
    tar \
    gcc \
#    libssl1.1 \
    && apt-get clean

# Download and install the IBM MQ client
RUN wget ${MQ_CLIENT_URL}/${MQ_PACKAGE} && \
mkdir -p ${MQ_INSTALL_DIR} && \
tar -xvf ${MQ_PACKAGE} -C ${MQ_INSTALL_DIR} && \
rm -rf ${MQ_PACKAGE}

# Set environment variables for MQ runtime
ENV PATH="${MQ_INSTALL_DIR}/bin:${PATH}"
# ENV LD_LIBRARY_PATH="${MQ_INSTALL_DIR}/lib:${LD_LIBRARY_PATH}"
ENV LD_LIBRARY_PATH="${MQ_INSTALL_DIR}/lib"

RUN pip install -r requirements.txt

ENV HOST_NAME="127.0.0.1"
ENV QUEUE_MANAGER_PORT_NUMBER="1415"
ENV QUEUE_MANAGER_NAME="TESTQMGR"  
ENV CHANNEL_NAME="channel" 
ENV QUEUE_NAME="TESTQ"

CMD ["python","mqfeed.py"]