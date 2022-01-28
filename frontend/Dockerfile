FROM python:3.9
COPY requirements.txt app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 8501
ENTRYPOINT ["streamlit","run"]
CMD ["main.py"]