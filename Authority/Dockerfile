ARG PYTHON_VERSION=3.10

FROM python:${PYTHON_VERSION}-alpine

WORKDIR /auth

COPY ./requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "auth.py"]