# Cheatsheet

## Docker

### Images

- `docker build -t <name> .` - Build image
- `docker images` - List images
- `docker rmi <id>` - Remove image

### Containers

- `docker run <image>` - Start container
- `docker run -it <image>` - Start in interactive mode
- `docker run -d <image>` - Start in background
- `docker run -p <host>:<container> <image>` - Map ports
- `docker ps` - List running containers
- `docker ps -a` - List all containers
- `docker stop <id>` - Stop container
- `docker rm <id>` - Remove container
- `docker exec -it <id> bash` - Access container

### Cleanup

- `docker system prune` - Remove unused resources
- `docker volume prune` - Remove unused volumes

### Docker Compose

- `docker-compose up` - Start services
- `docker-compose up -d` - Start in background
- `docker-compose down` - Stop and remove
- `docker-compose logs` - View logs
