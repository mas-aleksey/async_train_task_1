FROM codercom/code-server:3.12.0

USER root
RUN code-server --install-extension ms-python.python
RUN apt update && apt install -y python3-pip apache2-utils
WORKDIR /mercury
ADD requirements.txt .
RUN pip install -r requirements.txt

USER 1000
ENV USER=coder
ADD . /mercury
