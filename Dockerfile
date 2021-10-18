FROM ubuntu
EXPOSE 8000
WORKDIR /app
RUN apt update
RUN apt install -y git python3 python3-pip
RUN apt install -y libsasl2-dev python-dev libldap2-dev libssl-dev
COPY requirements.txt ./requirements.txt
RUN pip3 install pyOpenSSL uvicorn[standard]
RUN pip3 install -r requirements.txt
COPY . .
CMD python3 -m uvicorn --host 0.0.0.0 main:app