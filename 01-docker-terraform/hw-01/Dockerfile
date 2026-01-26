FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /hw

ENV PATH="/hw/.venv/bin/:$PATH"

COPY ".python-version" "pyproject.toml" "uv.lock" ./

RUN uv sync --locked

COPY ingest_hw_data.py ./ingest_data.py

ENTRYPOINT ["python", "-u", "ingest_data.py"]