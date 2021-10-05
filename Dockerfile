FROM ubuntu
RUN apt update
RUN apt install -y git python3 python3-pip
RUN cd ~ && git clone https://github.com/paulbricman/conceptarium
RUN apt install -y libsasl2-dev python-dev libldap2-dev libssl-dev
RUN python3 -m pip install pyOpenSSL uvicorn[standard]
RUN cd ~/conceptarium && python3 -m pip install -r requirements.txt
CMD cd ~/conceptarium; python3 -m uvicorn --host 0.0.0.0 main:app
EXPOSE 8000