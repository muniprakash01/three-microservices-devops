# Three Microservices DevOps Project

## Project Overview

This project demonstrates the DevOps implementation of a
three-microservice application using Docker, Docker Compose,
Jenkins and Trivy.

## Microservices

1. User Service
2. Product Service
3. Order Service

## Technologies Used

- Git and GitHub
- Python and Flask
- Docker
- Docker Compose
- Jenkins
- Trivy
- Ubuntu EC2

## Application Ports

| Service | Host Port |
|---------|-----------|
| User Service | 5001 |
| Product Service | 5002 |
| Order Service | 5003 |

## Run the Application

Build and start all services:

    docker compose up -d --build

Check running containers:

    docker compose ps

View logs:

    docker compose logs

Stop the application:

    docker compose down

## Health Checks

- http://localhost:5001/health
- http://localhost:5002/health
- http://localhost:5003/health

## Persistent Storage

Docker named volumes store application data:

- user-data
- product-data
- order-data

## CI/CD Workflow

1. Git checkout
2. Docker Compose validation
3. Application testing
4. Docker image building
5. Trivy security scanning
6. Application deployment
7. Health checks
