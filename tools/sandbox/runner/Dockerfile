FROM python:3.12-slim
# The image for the code. Add packages the course code needs here, for example:
# RUN pip install --no-cache-dir pandas==2.2.3
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY bootstrap.py /sandbox/bootstrap.py
USER 65534:65534
WORKDIR /work
ENTRYPOINT ["python", "/sandbox/bootstrap.py"]
