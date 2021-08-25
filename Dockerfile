FROM python:3.9.5-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD requirements.txt ./requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

ADD st_app.py ./st_app.py
COPY .streamlit /root/.streamlit

EXPOSE 80

CMD [ "streamlit", "run", "st_app.py" ]