FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["hypercorn", "--bind", "0.0.0.0:5000", "app:app"]
