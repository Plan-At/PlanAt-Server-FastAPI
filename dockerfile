FROM python:3.8.10
WORKDIR .
COPY . .
RUN python -m pip install -r requirements.txt
CMD ["python", "server.py"]
EXPOSE 8000