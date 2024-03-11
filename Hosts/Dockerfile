FROM python:3.10-alpine

WORKDIR /host

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["flask", "run"]