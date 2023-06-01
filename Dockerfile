FROM python:3.11

WORKDIR /data

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 4242

CMD python run.py 0.0.0.0:4242
