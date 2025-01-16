# Use the official Python image as a base
FROM python:3.9-slim

# Set environment variables to avoid writing bytecode and to make output unbuffered
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (JupyterLab and common data science libraries)
RUN pip install --no-cache-dir \
    jupyterlab \
    pandas \
    numpy \
    matplotlib \
    seaborn \
    scikit-learn \
    scipy \
    ipykernel \
    jupyterhub \
    notebook

# Expose JupyterLab's port
EXPOSE 8888

# Set the working directory in the container
WORKDIR /app

# Start JupyterLab when the container is run
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser"]


