# Multi-stage Dockerfile for AI Employee System
# Optimized for Oracle Cloud Free Tier (ARM64)

# Stage 1: Base image with system dependencies
FROM python:3.13-slim AS base

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    NODE_VERSION=24

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    gnupg \
    ca-certificates \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: Node.js installation
FROM base AS nodejs

# Install Node.js 24
RUN curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION}.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@latest \
    && npm install -g pm2 \
    && rm -rf /var/lib/apt/lists/*

# Stage 3: Playwright and Chrome installation
FROM nodejs AS playwright

# Install Playwright dependencies
RUN apt-get update && apt-get install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libcairo2 \
    && rm -rf /var/lib/apt/lists/*

# Install Playwright
RUN pip install playwright && \
    playwright install chromium && \
    playwright install-deps chromium

# Stage 4: Final application image
FROM playwright AS final

# Create app directory
WORKDIR /app

# Create non-root user for security
RUN useradd -m -u 1000 aiemployee && \
    chown -R aiemployee:aiemployee /app

# Copy requirements first (for layer caching)
COPY --chown=aiemployee:aiemployee requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY --chown=aiemployee:aiemployee . .

# Create necessary directories
RUN mkdir -p \
    AI_Employee_Vault/Needs_Action \
    AI_Employee_Vault/In_Progress \
    AI_Employee_Vault/Done \
    AI_Employee_Vault/Pending_Approval \
    AI_Employee_Vault/Approved \
    AI_Employee_Vault/Plans \
    AI_Employee_Vault/Logs \
    AI_Employee_Vault/Briefings \
    sessions \
    && chown -R aiemployee:aiemployee AI_Employee_Vault sessions

# Make scripts executable
RUN chmod +x scripts/*.sh scripts/*.py || true

# Switch to non-root user
USER aiemployee

# Expose ports (if needed for dashboard)
EXPOSE 3000

# Health check
HEALTHCHECK --interval=60s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import os; exit(0 if os.path.exists('AI_Employee_Vault/Logs') else 1)"

# Set entrypoint
ENTRYPOINT ["/bin/bash"]
CMD ["scripts/start_employee.sh"]
