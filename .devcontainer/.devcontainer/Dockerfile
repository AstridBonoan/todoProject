# Use the official Ubuntu image
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install basic tools and Python
RUN apt-get update && apt-get install -y \
    curl \
    git \
    sudo \
    python3 \
    python3-pip \
    # Install Node.js (adjust version if needed)
    ca-certificates \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    # Clean up
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m vscode && echo "vscode ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Set default user
USER vscode

# (Optional) Verify installations during build for debug
RUN node -v && npm -v && python3 --version && pip3 --version