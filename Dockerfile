ARG DEBIAN_NAME=stretch
FROM python:3.6.10-slim-${DEBIAN_NAME}


RUN \
    apt-get update \
    && apt-get install -y \
        make \
        build-essential \
        libssl1.0-dev \
        zlib1g-dev \
        libbz2-dev \
        libreadline-dev \
        libsqlite3-dev \
        llvm \
        libncurses5-dev \
        libncursesw5-dev \
        xz-utils \
        tk-dev \
        libffi-dev \
        liblzma-dev \
        python3-openssl \
        curl \
        git \
    && apt-get autoclean

RUN echo "Installing pyenv" \
    && curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

ENV PATH="/root/.pyenv/bin:$PATH"
RUN touch /root/.bashrc \
    && echo 'eval "$(pyenv init -)"' >> /root/.bashrc \
    && echo 'eval "$(pyenv virtualenv-init -)"' >> /root/.bashrc

RUN bash -c "pyenv install 2.7.16 && pyenv install 3.5.0 && pyenv install 3.7.6 && pyenv install 3.8.1"

ARG DEBIAN_NAME=stretch
ENV ARC="$(dpkg --print-architecture)"
ENV WKHL="wkhtmltox_0.12.5-1.${DEBIAN_NAME}_${ARC}.deb"
RUN bash -c "curl -o ${WKHL} -SL https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/${WKHL}" \
    && bash -c "apt install -y ./${WKHL}" \
    bash -c "rm ./${WKHL}"
RUN pip install tox tox-pyenv django==3.0
