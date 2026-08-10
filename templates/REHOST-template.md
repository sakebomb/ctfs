# Rehosting Instructions

Instructions for running this challenge locally for practice or educational purposes.

## Prerequisites

- Docker and Docker Compose
- [Any other tools: Python 3.x, netcat, etc.]
- [Minimum system requirements if relevant]

## Quick Start

```bash
# Clone/navigate to challenge directory
cd [challenge-name]

# Build and run
docker-compose up -d

# Access the challenge
# Web: http://localhost:8080
# Service: nc localhost 9999
```

## Detailed Setup

### 1. Build the Container

```bash
docker build -t [challenge-name] .
```

### 2. Run the Service

**For web challenges:**
```bash
docker run -d -p 8080:80 [challenge-name]
```

**For pwn/network services:**
```bash
docker run -d -p 9999:9999 [challenge-name]
```

### 3. Verify It's Running

```bash
# Check container status
docker ps

# Test connection
curl http://localhost:8080
# Or
nc localhost 9999
```

## Environment Variables

If the challenge requires specific configuration:

```bash
docker run -d \
  -p 8080:80 \
  -e FLAG="flag{test_flag_for_local}" \
  -e DEBUG=false \
  [challenge-name]
```

## File Structure

```
.
├── Dockerfile          # Container definition
├── docker-compose.yml  # Easy deployment
├── challenge/          # Challenge files
│   ├── app.py
│   └── flag.txt
├── README.md           # Writeup
└── REHOST.md          # This file
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using the port
lsof -i :8080

# Change port in docker-compose.yml
ports:
  - "8081:80"  # Use different local port
```

### Container Won't Start
```bash
# Check logs
docker logs [container-id]

# Rebuild without cache
docker build --no-cache -t [challenge-name] .
```

### Network Issues
```bash
# Verify container network
docker network ls
docker network inspect bridge

# Try host networking (less isolated)
docker run --network host [challenge-name]
```

## Local vs Competition Differences

**Modified for local hosting:**
- Flag changed from competition flag to `flag{local_test_flag}`
- Removed rate limiting (if present)
- Exposed additional debugging endpoints (if applicable)
- [Any other modifications]

**To make it identical to competition:**
- [Steps to restore original configuration]

## Cleanup

```bash
# Stop and remove containers
docker-compose down

# Remove images
docker rmi [challenge-name]

# Remove volumes (if any)
docker volume prune
```

## Notes

- This rehost is for **educational purposes only**
- Original challenge from: [CTF Name Year]
- [Any specific caveats or warnings]

## Alternative Deployment

### Using Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  challenge:
    build: .
    ports:
      - "8080:80"
    environment:
      - FLAG=flag{local_test}
    restart: unless-stopped
```

### Without Docker

If you want to run natively:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment
export FLAG="flag{local_test}"

# Run
python app.py
```

**Note:** Native deployment may have security implications. Docker isolation is recommended.

---

**Questions or issues?** Open an issue in the parent repository.
