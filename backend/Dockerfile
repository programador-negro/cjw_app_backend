FROM python:3.11

WORKDIR /usr/src/app/

COPY requirements.txt /usr/src/app/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY . /usr/src/app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]