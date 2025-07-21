FROM python:3.12-slim
RUN pip install uv
WORKDIR /app
RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock ./
RUN uv pip install --system --no-cache-dir -e .
COPY src/ src/
COPY .env .env
RUN pip freeze
ENV PYTHONPATH=/app \
    PORT=8000
EXPOSE $PORT
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]