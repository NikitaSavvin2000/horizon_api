FROM python:3.9.16-slim-buster
#
#WORKDIR app
#COPY ./ ./

COPY . /app
WORKDIR /app

ENV PYTHONPATH=/app

COPY pyproject.toml .

RUN pip install -U pip setuptools wheel
RUN pip install zstandard
RUN pip install pdm
RUN pdm install --prod --frozen-lockfile --no-editable

EXPOSE 7079

ENTRYPOINT ["pdm", "run", "src/server.py"]

