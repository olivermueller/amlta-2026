FROM docker:27.5.1-cli AS cli

FROM python:3.12-slim
# only the docker client: the API starts the sandbox containers through the Docker socket of the host
COPY --from=cli /usr/local/bin/docker /usr/local/bin/docker
RUN pip install --no-cache-dir fastapi==0.115.6 uvicorn==0.34.0
WORKDIR /app
COPY app.py .
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
