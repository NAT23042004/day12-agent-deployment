# Production-Ready AI Agent (Day 12 Lab)

This repository contains a production-ready AI agent built for the Day 12 Lab of the AICB-P1 course.

## Features

- **FastAPI** backend with **Pydantic** validation.
- **Dockerized** using Multi-stage builds for a lightweight image.
- **Stateless Design** using **Redis** for conversation history.
- **API Security:** API Key authentication, Rate Limiting (10 req/min), and Cost Guard.
- **Reliability:** Health check and Readiness probe endpoints.
- **DevOps:** Pre-configured for **Railway** and **Docker Compose**.

## Project Structure

- `app/`: Main application logic.
- `utils/`: Common utilities (Mock LLM).
- `Dockerfile`: Multi-stage Docker build file.
- `docker-compose.yml`: Local orchestration for Agent + Redis + Nginx Load Balancer.
- `railway.toml`: Cloud deployment configuration.

## Quick Start (Local)

1. Clone the repository.
2. Ensure Docker and Docker Compose are installed.
3. Run the following command:
   ```bash
   docker compose up --build --scale agent=3
   ```
4. Access the agent at `http://localhost:8000`.
## Deployment

The service is deployed on Railway at:
[https://day12-production-f11f.up.railway.app](https://day12-production-f11f.up.railway.app)

Check `MISSION_ANSWERS.md` and `DEPLOYMENT.md` for detailed answers and test commands.
