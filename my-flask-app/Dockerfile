# Stage 1: Build stage (install dependencies)
FROM python:3.11-alpine AS flask-build

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev

RUN chown -R appuser:appgroup /app

# Copy requirements separately for caching
COPY backend/requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY backend/ .

# Stage 2: Production stage (minimal runtime)
FROM python:3.11-alpine

WORKDIR /app

# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy installed packages + app from build stage
COPY --from=flask-build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=flask-build /app /app

# Set file ownership and permissions
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 5000

CMD ["python3", "app.py"]
