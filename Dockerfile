FROM python:3.9.6

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./main.py ./main.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]