FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    AWS_CLOUDOPS_DEMO=1

COPY pyproject.toml README.md ./
COPY aws_cloudops_mcp ./aws_cloudops_mcp

RUN pip install --no-cache-dir -e ".[web]"

EXPOSE 10000

CMD ["aws-cloudops-ui"]
