FROM python:3.11-slim
COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt
COPY ./src/ /meme_server/
WORKDIR /meme_server/

EXPOSE 8000
ENTRYPOINT ["python3", "./main.py"]