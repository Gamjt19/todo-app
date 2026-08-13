# Containerized Full-Stack To-Do Application

## Overview

A containerized To-Do Management Application built using **Python Flask, MySQL, Docker, Docker Compose, and Nginx**.

The project demonstrates application containerization, multi-stage Docker builds, non-root execution, persistent database storage, health checks, reverse proxying, CI/CD automation, Docker Hub integration, and security scanning.

---

## Architecture

```text
                         Client
                           |
                           | HTTP :8080
                           v
                    +--------------+
                    |    Nginx     |
                    | Reverse Proxy|
                    +------+-------+
                           |
                           | app:5000
                           v
                    +--------------+
                    |  Flask App   |
                    |    :5000     |
                    +------+-------+
                           |
                           | db:3306
                           v
                    +--------------+
                    |    MySQL     |
                    |    :3306     |
                    +------+-------+
                           |
                           v
                    +--------------+
                    |   Volume     |
                    | mysql-data   |
                    +--------------+
```

### CI/CD Architecture

```text
Developer
    |
    | git push
    v
 GitHub
    |
    v
GitHub Actions
    |
    +---- pytest
    |
    +---- Flake8
    |
    +---- pip-audit
    |
    +---- Docker Build
    |
    +---- Trivy Scan
    |
    v
Docker Hub
    |
    +---- v1.0
    |
    +---- latest
```

---

## Technologies

* Python 3.12
* Flask
* Flask-SQLAlchemy
* MySQL 8.0
* Nginx
* Docker
* Docker Compose
* Git
* GitHub
* GitHub Actions
* Docker Hub
* pytest
* Flake8
* pip-audit
* Trivy

---

## Project Structure

```text
todo-app/
├── app/
│   ├── __init__.py
│   └── app.py
│
├── tests/
│   └── test_app.py
│
├── nginx/
│   └── nginx.conf
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
├── .gitignore
├── .env
└── README.md
```

> `.env` contains configuration/secrets and must not be committed to Git.

---

## Application Features

* Create Todo
* View all Todos
* Update Todo
* Delete Todo
* Application health check
* MySQL database storage
* Application logging
* Docker health checks

---

## API Endpoints

| Method | Endpoint      | Description              |
| ------ | ------------- | ------------------------ |
| GET    | `/health`     | Application health check |
| GET    | `/todos`      | Get all Todos            |
| POST   | `/todos`      | Create a Todo            |
| PUT    | `/todos/<id>` | Update a Todo            |
| DELETE | `/todos/<id>` | Delete a Todo            |

---

## Environment Configuration

The application uses environment variables instead of hardcoding database configuration.

Example `.env`:

```env
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_DATABASE=todo_db
MYSQL_USER=todo_user
MYSQL_PASSWORD=your_password
MYSQL_HOST=db
```

The `.env` file should be included in `.gitignore`.

---

## Running the Application

Build and start all services:

```bash
docker compose up -d --build
```

Check running services:

```bash
docker compose ps
```

Expected services:

```text
todo-app
todo-db
todo-nginx
```

The application is exposed through Nginx on:

```text
http://localhost:8080
```

---

## Health Check

Test the application:

```bash
curl http://localhost:8080/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

Docker container health can be checked using:

```bash
docker compose ps
```

or:

```bash
docker inspect todo-app
```

---

## Creating a Todo

```bash
curl -X POST http://localhost:8080/todos \
-H "Content-Type: application/json" \
-d '{"title":"Learn Docker"}'
```

Example response:

```json
{
  "id": 1,
  "title": "Learn Docker",
  "completed": false
}
```

---

## Getting Todos

```bash
curl http://localhost:8080/todos
```

---

## Updating a Todo

```bash
curl -X PUT http://localhost:8080/todos/1 \
-H "Content-Type: application/json" \
-d '{"completed":true}'
```

---

## Deleting a Todo

```bash
curl -X DELETE http://localhost:8080/todos/1
```

---

## Dockerfile Features

The application Dockerfile implements:

### Multi-stage Build

The first stage installs Python dependencies and the second stage contains only the required runtime components.

This helps reduce unnecessary files in the final image.

### Non-root User

The application runs using:

```text
appuser
```

instead of the root user.

Verify:

```bash
docker exec todo-app whoami
```

Expected:

```text
appuser
```

### Docker Health Check

The image includes a health check that verifies the Flask `/health` endpoint.

---

## Docker Compose Services

### Application

The Flask application runs on:

```text
5000
```

### MySQL

MySQL runs internally on:

```text
3306
```

### Nginx

Nginx acts as the reverse proxy and exposes:

```text
8080
```

Traffic flow:

```text
Client
  |
  v
Nginx :8080
  |
  v
Flask :5000
  |
  v
MySQL :3306
```

---

## Docker Network

Docker Compose creates a custom bridge network:

```text
todo-network
```

Containers communicate using service names.

For example, the Flask application connects to MySQL using:

```text
db
```

rather than:

```text
localhost
```

Inside the Docker network:

```text
app → db:3306
```

---

## Persistent Storage

MySQL uses a named Docker volume:

```text
mysql-data
```

mounted to:

```text
/var/lib/mysql
```

List volumes:

```bash
docker volume ls
```

This allows database data to survive container recreation.

To stop the application:

```bash
docker compose down
```

The named volume remains unless explicitly removed.

Start again:

```bash
docker compose up -d
```

---

## Useful Docker Commands

View running containers:

```bash
docker ps
```

View all containers:

```bash
docker ps -a
```

View images:

```bash
docker images
```

View application logs:

```bash
docker compose logs app
```

Follow application logs:

```bash
docker compose logs -f app
```

View database logs:

```bash
docker compose logs db
```

Enter the application container:

```bash
docker compose exec app sh
```

Inspect a container:

```bash
docker inspect todo-app
```

Stop the stack:

```bash
docker compose down
```

Start the stack:

```bash
docker compose up -d
```

Rebuild and start:

```bash
docker compose up -d --build
```

---

## Testing

The project uses pytest for unit testing.

Run:

```bash
pytest
```

The health endpoint is tested to verify that the application starts correctly.

Expected:

```text
1 passed
```

---

## Code Quality

Flake8 is used for Python code quality checks.

Run:

```bash
flake8 app tests
```

A successful run produces no output.

---

## Dependency Security

`pip-audit` is used to identify known vulnerabilities in Python dependencies.

Run:

```bash
pip-audit -r requirements.txt
```

---

## Docker Image Security

Trivy is used to scan the Docker image for known vulnerabilities.

The CI/CD pipeline scans for:

```text
HIGH
CRITICAL
```

severity vulnerabilities.

The image is scanned before it is pushed to Docker Hub.

---

## Docker Hub

The application image is published to Docker Hub using two tags:

```text
v1.0
latest
```

Example:

```bash
docker tag todo-app-app:latest username/todo-app:v1.0
docker tag todo-app-app:latest username/todo-app:latest
```

Push:

```bash
docker push username/todo-app:v1.0
docker push username/todo-app:latest
```

Pull:

```bash
docker pull username/todo-app:v1.0
```

---

## CI/CD Pipeline

GitHub Actions automatically runs when code is pushed to the `main` branch.

Pipeline stages:

```text
Checkout
   |
   v
Install Dependencies
   |
   +---- pytest
   |
   +---- Flake8
   |
   +---- pip-audit
   |
   v
Docker Build
   |
   v
Trivy Security Scan
   |
   v
Docker Hub Push
```

The Docker job depends on the successful completion of the test job.

Therefore:

```text
Tests Pass
    |
    v
Docker Build
    |
    v
Security Scan
    |
    v
Docker Push
```

If the test job fails, the Docker image is not pushed.

---

## GitHub Secrets

Docker Hub credentials are stored using GitHub repository secrets.

Required secrets:

```text
DOCKER_USERNAME
DOCKER_PASSWORD
```

The credentials are not hardcoded in the workflow.

---

## Security Measures

The project implements:

* Environment-based configuration
* `.env` excluded from Git
* Non-root Docker user
* Docker health checks
* MySQL persistent storage
* Docker network isolation
* Docker image vulnerability scanning
* Python dependency vulnerability scanning
* GitHub encrypted secrets
* Docker Hub authentication

---

## Logging and Monitoring

Application logs can be viewed with:

```bash
docker compose logs app
```

Follow logs in real time:

```bash
docker compose logs -f app
```

Container status:

```bash
docker compose ps
```

Health status:

```bash
docker inspect todo-app
```

Prometheus and Grafana integration was considered optional and is not required for the core implementation.

---

## Troubleshooting

### Container is not running

Check all containers:

```bash
docker ps -a
```

Check logs:

```bash
docker logs <container-name>
```

### Application cannot connect to MySQL

Check:

```bash
docker compose ps
```

Make sure MySQL is healthy.

Check:

```bash
docker compose logs db
```

Inside Docker Compose, the database hostname should be:

```text
db
```

not:

```text
localhost
```

### Rebuild the application

```bash
docker compose down
docker compose up -d --build
```

### Check Docker networks

```bash
docker network ls
```

### Check Docker volumes

```bash
docker volume ls
```

---

## Conclusion

This project demonstrates a complete containerized application deployment using Docker and Docker Compose with:

* Python Flask application
* MySQL database
* Nginx reverse proxy
* Persistent database storage
* Custom Docker network
* Multi-stage Docker build
* Non-root execution
* Health checks
* Automated testing
* Code quality checks
* Dependency scanning
* Docker image vulnerability scanning
* Docker Hub integration
* GitHub Actions CI/CD

The final deployment provides a reproducible and secure workflow from source code to a container image published on Docker Hub.
