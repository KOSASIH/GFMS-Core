# Deployment Guide

## Overview

This guide provides instructions for deploying the Global Financial Management System (GFMS) to a production environment.

## Prerequisites

- A cloud server or on-premises server with Python 3.8 or higher.
- Docker installed on the server (optional but recommended).

## Deployment Steps

1. **Clone the Repository**:
   ```bash
   1 git clone https://github.com/KOSASIH/gfms.git
   2 cd gfms
   ```
2. **Set Up Environment Variables**: Create a .env file in the root directory and configure the necessary environment variables.

3. **Install Dependencies**:

   ```bash
   1 pip install -r requirements.txt
   ```

4. **Run Database Migrations**: If using Alembic for migrations, run:

   ```bash
   1 alembic upgrade head
   ```

5. **Start the Application**: You can run the application using Uvicorn:

   ```bash
   1 uvicorn src.main:app --host 0.0.0.0 --port 8000
   ```

6. **Using Docker (optional)**:

- Build the Docker image:
   ```bash
   1 docker build -t gfms .
   ```
- Run the Docker container:
   ```bash
   1 docker run -d -p 8000:8000 --env-file .env gfms
   ```

## Monitoring and Maintenance
- Monitor application logs for errors and performance issues.
- Regularly update dependencies and apply security patches.
- Backup the database regularly to prevent data loss.
