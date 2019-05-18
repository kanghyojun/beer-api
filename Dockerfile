FROM python:3.7.3
COPY setup.cfg /app/setup.cfg
COPY setup.py /app/setup.py
RUN mkdir -p /app/beer && echo '__version__ = "0.1"' >> /app/beer/__init__.py && pip install /app --no-cache-dir

COPY . /app
WORKDIR /app
EXPOSE 8000
CMD ["./run.py", "-e", "prod", "-p", "8000"]
