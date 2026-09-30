FROM debian:trixie


# https://stackoverflow.com/a/71071332/7363348 
RUN apt-get update \
	&& apt-get upgrade -y && \
	apt-get install -y --no-install-recommends make build-essential libssl-dev zlib1g-dev \
	libbz2-dev libreadline-dev libsqlite3-dev wget ca-certificates curl llvm libncurses5-dev \
	xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev mecab-ipadic-utf8 git \
	&& apt-get autoclean \
	&& apt-get autoremove -y

ENV PYTHON_VERSION="3.10"
ENV PYENV_ROOT="/root/.pyenv"
ENV PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"

RUN set -ex \
	&& curl -fsSL https://pyenv.run | bash \
    && pyenv update \
    && pyenv install $PYTHON_VERSION \
    && pyenv global $PYTHON_VERSION \
    && pyenv rehash


WORKDIR /app
RUN git clone https://github.com/alexmolas/microsearch --depth=1
WORKDIR /app/microsearch

RUN pip install .


ENTRYPOINT ["python", "-m", "app.app", "--data-path","data.json"]
