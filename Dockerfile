# Multi-stage build để tối ưu image size
FROM python:3.11-slim as builder

# Metadata
LABEL maintainer="your-email@example.com"
LABEL description="Vehicle Rental System - Containerized Python Application"

WORKDIR /app

# Copy only requirements first (leverage Docker cache)
COPY requirements-minimal.txt .

# Install dependencies
RUN pip install --no-cache-dir --user -r requirements-minimal.txt

# Final stage
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/root/.local/bin:$PATH

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/data && \
    chown -R appuser:appuser /app

WORKDIR /app

# Copy Python dependencies from builder stage
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser data/ ./data/

# Switch to non-root user
USER appuser

# Health check (optional for console app)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Run the application
CMD ["python", "src/main.py"]