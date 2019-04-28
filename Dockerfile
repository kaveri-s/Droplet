FROM python:3.6

RUN \
    git clone https://github.com/kaveri-s/Droplet.git && \
    cd Droplet && \
    pip install -r requirements.txt
    
WORKDIR /Droplet/src

CMD [ "python3", "server.py" ]
