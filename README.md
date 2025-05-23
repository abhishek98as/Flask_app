# Flask Todo App

A complete Flask Todo application with MongoDB integration, featuring a beautiful frontend and full CRUD functionality.

## Deployment with GitHub Actions + Docker + EC2

This application is set up for CI/CD deployment using GitHub Actions, Docker, and Amazon EC2.

### Prerequisites

1. GitHub repository with this code
2. DockerHub account
3. Amazon EC2 instance
4. MongoDB Atlas account and database (already configured)

### Setup Instructions

#### 1. GitHub Repository Setup

1. Push your code to a GitHub repository
2. Add the following secrets to your GitHub repository:
   - `DOCKER_USERNAME`: Your DockerHub username
   - `DOCKER_PASSWORD`: Your DockerHub password
   - `EC2_HOST`: Your EC2 instance public IP address
   - `EC2_USERNAME`: EC2 login username (usually `ec2-user` or `ubuntu`)
   - `EC2_SSH_KEY`: Your EC2 private SSH key
   - `MONGO_URI`: Your MongoDB Atlas connection string with URL-encoded credentials
   - `SECRET_KEY`: Secret key for Flask app

#### 2. EC2 Instance Setup

1. Launch an EC2 instance with Ubuntu or Amazon Linux
2. Configure security group to allow inbound traffic on port 80
3. Install Docker:
   ```bash
   sudo apt update
   sudo apt install -y docker.io
   sudo systemctl start docker
   sudo systemctl enable docker
   sudo usermod -aG docker $USER
   ```

#### 3. Deployment Process

When you push to the main branch, GitHub Actions will:

1. Build the Docker image
2. Push it to DockerHub
3. Connect to your EC2 instance
4. Pull the latest image
5. Run the container with the required environment variables

## Local Development

### Using Docker Compose

```bash
docker-compose up
```

### Manual Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `flask run`

## Monitoring and Logs

To view logs on EC2:

```bash
docker logs flask-todo-app
```
#   F l a s k _ a p p  
 