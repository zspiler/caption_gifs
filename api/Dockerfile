FROM python:3.9-slim 
WORKDIR /usr/local
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY src /app
WORKDIR /app
CMD ["python", "app.py"]
EXPOSE 5000