# Pharmacy App

a basic full-stack application with a Django backend, React frontend, and a PostgreSQL database.
The application allow users to register, log in, view a list of medications, and request a refill.
Additionally, it has a dashboard that displays refill request statistics using a simple chart.

## Table of Contents

- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
  - [Server `.env` File](#server-env-file)
  - [Client `.env` File](#client-env-file)
- [Setting Up the Media Folder](#setting-up-the-media-folder)
- [Running the Containers](#running-the-containers)
- [Accessing the Application](#accessing-the-application)
- [Troubleshooting](#troubleshooting)
- [Additional Information](#additional-information)
- [License](#license)

## Project Structure

- **`apps/`**
  - **`client/`**: Contains the frontend application built with React.
    - **`Dockerfile`**: Defines the Docker image for the client.
    - **`.env.example`**: Example environment variables for the client. Users should create a `.env` file based on this template.
    - **`public/`**: Static files like `index.html` and favicon.
    - **`src/`**: Source code for the React application.
    - **`package.json`**: Lists dependencies and scripts for the client application.

  - **`server/`**: Contains the backend application built with Django.
    - **`app/`**: Django project directory.
      - **`__init__.py`**: Makes the directory a Python package.
      - **`wsgi.py`**: WSGI configuration for deploying the Django app.
      - **`settings.py`**: Configuration settings for Django.
      - **`urls.py`**: URL routing configurations.
    - **`Dockerfile`**: Defines the Docker image for the server.
    - **`entrypoint.sh`**: Script executed when the Docker container starts. Typically handles tasks like applying migrations and starting the server.
    - **`wait-for-it.sh`**: Utility script to wait for dependent services (e.g., the database) to become available before starting the server.
    - **`requirements.txt`**: Lists Python dependencies for the server application.
    - **`.env.example`**: Example environment variables for the server. Users should create a `.env` file based on this template.
    - **`manage.py`**: Django's command-line utility for administrative tasks.
    - **`media/`**: Directory to store user-uploaded media files.
    - **`staticfiles/`**: Directory where Django collects static files for production.

- **`docker-compose.yml`**: Orchestrates the multi-container Docker application, defining services for the client, server, and database, along with their configurations, environment variables, and dependencies.

- **`README.md`**: Documentation for setting up, running, and understanding the project.

- **`.gitignore`**: Specifies files and directories that should be ignored by Git, such as environment files and compiled code.


## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Docker**: Make sure Docker is installed on your machine. You can download it from [Docker Official Website](https://www.docker.com/get-started).
- **Docker Compose**: Ensure Docker Compose is installed. It typically comes bundled with Docker Desktop.
- **Git**: To clone the repository. Download from [Git Official Website](https://git-scm.com/downloads).

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/BemwaMalak/mini_full_stack.git
   cd your-repo
   ```

