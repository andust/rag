FROM python:3.12.6-bookworm

WORKDIR /code/rag_chat

COPY ./requirements.txt /code/rag_chat/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/rag_chat/requirements.txt

COPY ./app /code/rag_chat/app

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload" ]
