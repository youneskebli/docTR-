FROM python:3.8

RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libgdk-pixbuf2.0-0 \
    libpango1.0-0 \
    libcairo2 \
    libpangocairo-1.0-0 \
    libglib2.0-0 \
    shared-mime-info \
    libgl1-mesa-dev

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 5000

ENV NAME World

CMD ["python", "./app.py"]
