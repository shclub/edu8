FROM python:3.6

WORKDIR /usr/src/app

EXPOSE 5000

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["ddtrace-run","python3", "app.py"]
