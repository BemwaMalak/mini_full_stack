
# Pharmacy App

A basic full-stack application with a Django backend, React frontend, and a PostgreSQL database. The application allows users to register, log in, view a list of medications, and request a refill. Additionally, it has a basic dashboard that displays refill request statistics using a simple chart.

## Table of Contents

- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
  - [Server `.env` File](#server-env-file)
  - [Client `.env` File](#client-env-file)
- [Setting Up the Media Folder](#setting-up-the-media-folder)
- [Running the Containers](#running-the-containers)
- [Post-Setup Commands](#post-setup-commands)
- [Deploying to AWS EC2](#deploying-to-aws-ec2)
- [Accessing the Application](#accessing-the-application)
- [Troubleshooting](#troubleshooting)
- [Additional Information](#additional-information)
- [License](#license)

## Project Structure

```
.
├── apps
│   ├── client
│   │   ├── Dockerfile           # Docker configuration for the client application
│   │   ├── .env.example         # Example environment variables for the client
│   │   ├── public               # Public assets for the client (e.g., index.html)
│   │   ├── src                  # Source code for the client application
│   │   │   ├── components       # Reusable React components
│   │   │   ├── pages            # Page components for routing
│   │   └── package.json         # Client-side dependencies and scripts
│   └── server
│       ├── app
│       │   ├── __init__.py       # Initializes the Django app
│       │   ├── wsgi.py           # WSGI configuration for Django
│       │   ├── settings.py       # Django settings module
│       │   ├── urls.py           # URL configurations for the Django app
│       │   └── ...                # Additional Django app modules
│       ├── Dockerfile            # Docker configuration for the server application
│       ├── entrypoint.sh         # Entrypoint script for Docker container initialization
│       ├── wait-for-it.sh        # Script to wait for dependent services (e.g., database) to be ready
│       ├── requirements.txt      # Python dependencies for the server
│       ├── .env.example          # Example environment variables for the server
│       ├── manage.py             # Django management script
├── docker-compose.yml            # Docker Compose configuration to orchestrate containers
├── README.md                     # Project documentation
└── .gitignore                     # Specifies intentionally untracked files to ignore
```

## Prerequisites

Ensure you have Docker, Docker Compose, and Git installed on your machine. For installation, visit [Docker](https://www.docker.com/get-started) and [Git](https://git-scm.com/downloads).

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/BemwaMalak/mini_full_stack.git
   cd mini_full_stack
   ```

2. **Navigate to the Project Directory**

   Ensure you're in the project's root directory where the `docker-compose.yml` file is located.

   ```bash
   cd mini_full_stack
   ```

## Environment Variables

The application requires certain environment variables for both the server and the client.

### Server `.env` File

1. **Create the `.env` File**

   ```bash
   cd apps/server
   cp .env.example .env
   ```

2. **Configure the `.env` File**

   ```env
   # Database Configuration
    DATABASE_NAME=app
    DATABASE_USERNAME=postgres
    DATABASE_PASSWORD=12345
    DATABASE_HOST=db
    DATABASE_PORT_NUMBER=5432
    
    # Database Docker Configuration
    POSTGRES_DB=app
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=12345
    
    # Django Application Settings
    SECRET_KEY=nvj!-^i%19em0$qcb_8ibnfz6ujp5bh=6k&r0s--i3b_acm6x8
    DEBUG=True
    ALLOWED_HOSTS=localhost
    RATE_LIMIT_ENABLED=True
    
    # CORS and CSRF Settings
    CORS_ALLOWED_ORIGINS=http://localhost:3000
    CSRF_TRUSTED_ORIGINS=http://localhost:3000
    
    # Test Database Configuration
    TEST_DATABASE_NAME=app_test
    TEST_DATABASE_USERNAME=postgres
    TEST_DATABASE_PASSWORD=12345
    TEST_DATABASE_HOST=db
    TEST_DATABASE_PORT_NUMBER=5432
   ```

3. **Server `.env` Example**

   Use `apps/server/.env.example` as a reference.

### Client `.env` File

1. **Create the `.env` File**

   ```bash
   cd ../../apps/client
   cp .env.example .env
   ```

2. **Configure the `.env` File**

   ```env
   VITE_API_URL=http://localhost:8000/api
   ```

## Setting Up the Media Folder

Create a `media` folder in `apps/server`:

```bash
mkdir apps/server/media
```

## Running the Containers

To build and start:

```bash
docker-compose up --build
```

To run in detached mode:

```bash
docker-compose up --build -d
```

To stop:

```bash
docker-compose down
```
## Post-Setup Commands

After the containers are running, additional commands need to be executed inside the server container to set up the database:

1. **Enter the Server Container**

   ```bash
   docker exec -it <container_id> /bin/bash
   ```

   Replace `<container_id>` with the actual container ID of the server.

2. **Run Migrations**

   ```bash
   python3 manage.py migrate
   ```

3. **Seed Groups**

   ```bash
   python3 manage.py seed_groups
   ```

4. **Optional Data Seeding**

   You can also seed random data for users or medications:

   ```bash
   python3 manage.py seed_users        # Seed random user accounts (password for all accounts is password123)
   python3 manage.py seed_medications  # Seed random medication data
   ```

These commands set up the initial database structure and seed sample data, making the application ready for use.

## Deploying to AWS EC2

To deploy this application to an AWS EC2 instance, follow these steps:

1. **Launch an EC2 Instance**
   - Sign in to your AWS account and navigate to the EC2 dashboard.
   - Launch a new EC2 instance using an Ubuntu Server AMI (e.g., Ubuntu 22.04 LTS).
   - Configure security groups to allow HTTP (port 80), HTTPS (port 443), and custom ports if necessary (e.g., 3000 and 8000).
   - Generate and download a key pair (.pem file) to connect to the instance.

2. **Connect to the EC2 Instance**
   - Open a terminal on your local machine and connect to the instance:

     ```bash
     ssh -i /path/to/your-key.pem ubuntu@your-ec2-public-ip
     ```

3. **Install Docker and Docker Compose**
   - Update the package index:

     ```bash
     sudo apt update
     ```

   - Install Docker:

     ```bash
     sudo apt install -y docker.io
     ```

   - Enable and start Docker:

     ```bash
     sudo systemctl enable docker
     sudo systemctl start docker
     ```

   - Install Docker Compose:

     ```bash
     sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
     sudo chmod +x /usr/local/bin/docker-compose
     ```

4. **Transfer Project Files to EC2**
   - From your local machine or Github repo, transfer your project files to the EC2 instance using `scp`:

     ```bash
     scp -i /path/to/your-key.pem -r /path/to/your-project ubuntu@your-ec2-public-ip:/home/ubuntu/
     ```

5. **Configure Environment Variables**
   - SSH into your instance and navigate to the project directory:

     ```bash
     cd /home/ubuntu/your-project
     ```

   - Set up the necessary `.env` files as described in the [Environment Variables](#environment-variables) section.

6. **Run Docker Compose**
   - Run the following command to build and start the Docker containers on the EC2 instance:

     ```bash
     sudo docker-compose up --build -d
     ```

7. **Execute Post-Setup Commands**
   - Follow the [Post-Setup Commands](#post-setup-commands) to initialize the database and seed any necessary data.

8. **Access the Application**
   - Visit `http://your-ec2-public-ip:3000` for the client application and `http://your-ec2-public-ip:8000/admin` for the Django admin.

**Note:** For a production deployment, consider using a reverse proxy (e.g., Nginx) and securing the connection with SSL certificates.

## Accessing the Application

- Client: [http://localhost:3000](http://localhost:3000)

## Troubleshooting

Common issues like `ModuleNotFoundError` can be resolved by checking Docker volumes.

## Additional Information

- [Django Documentation](https://docs.djangoproject.com/)
- [React Documentation](https://reactjs.org/docs/getting-started.html)

## License

MIT License
