# CrehanaAPI Project

## Running the Project with Docker

This guide will help you set up and run the CrehanaAPI project using Docker.

### Prerequisites
Ensure you have the following installed on your system:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Poetry](https://python-poetry.org/)

### Steps to Run the Project

1. **Clone the Repository**
    ```bash
    git clone https://github.com/your-username/CrehanaAPI.git
    cd CrehanaAPI
    ```

2. **Install Pre-Commit Hooks**
    Install pre-commit hooks to ensure code quality:
    ```bash
    pre-commit install
    ```

3. **Install Dependencies with Poetry**
    Use Poetry to install project dependencies:
    ```bash
    poetry install
    ```

4. **Add New Packages with Poetry**
    To add new packages to the project, use:
    ```bash
    poetry add <package-name>
    ```

5. **Ensure `.env` Variables**
    Create a `.env` file in the root of the project and ensure all required environment variables are properly set. Refer to the `.env.example` file for the expected variables.

    Generate a secret key for the `.env` file using the following command:
    ```bash
    openssl rand -hex 32
    ```


6. **Build and Start the Docker Image**
    Run the following command to build the Docker image:
    ```bash
    docker compose -f docker-compose.yml up --build --remove-orphans
    ```
    or in detached mode:
    ```bash
    docker compose -f docker-compose.yml up -d --build --remove-orphans
    ````

7. **Access the Application**
    Once the containers are up and running, the application will be accessible at:
    ```
    http://localhost:8000
    ```

### Stopping the Containers
To stop the running containers, use:
```bash
docker compose -f docker-compose.yml down
```

### Additional Notes
- Ensure that the `docker-compose.yml` file is properly configured for your project.
- If you encounter any issues, check the logs using:
  ```bash
  docker-compose logs
  ```

### License
This project is licensed under the MIT License.
