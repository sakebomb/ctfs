#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check for -y flag
if [ "$1" != "-y" ]; then
    echo -e "${YELLOW}🚨 WARNING: This will destroy ALL containers and volumes!${NC}"
    read -p "Are you sure you want to continue? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]
    then
        echo -e "${RED}Aborted.${NC}"
        exit 1
    fi
fi

echo -e "${YELLOW}Stopping and removing all containers...${NC}"
docker compose down -v

echo -e "${YELLOW}Removing any remaining volumes...${NC}"
docker volume rm $(docker volume ls -q) 2>/dev/null || true

echo -e "${YELLOW}Removing any remaining containers...${NC}"
docker rm -f $(docker ps -aq) 2>/dev/null || true

echo -e "${YELLOW}Removing any remaining networks...${NC}"
docker network rm $(docker network ls -q) 2>/dev/null || true

echo -e "${GREEN}✅ All Docker resources have been destroyed!${NC}"
echo -e "${GREEN}To start fresh, run: docker compose up -d${NC}" 