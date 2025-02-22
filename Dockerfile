FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y gcc libpq-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./assets /assets

CMD ["uvicorn", "assets.main:app", "--host", "0.0.0.0", "--port", "8000","--timeout-keep-alive", "90", "--reload"]
