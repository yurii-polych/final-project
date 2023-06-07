FROM python:3.11

WORKDIR /data

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 4242

CMD python run.py
