#!/bin/bash

# Default passwords - change these if needed
GITLAB_ROOT_PASSWORD="omgwtfbbq"
NUTTY_PASSWORD="N3wP@ssw0rd2024"

# Function to generate a random password
generate_password() {
    # Generate a 16 character password with letters, numbers, and symbols
    tr -dc 'A-Za-z0-9!@#$%^&*' < /dev/urandom | head -c 16
}

# Allow overriding passwords from command line
while getopts "r:n:" opt; do
    case $opt in
        r) GITLAB_ROOT_PASSWORD="$OPTARG" ;;
        n) NUTTY_PASSWORD="$OPTARG" ;;
        \?) echo "Invalid option: -$OPTARG" >&2; exit 1 ;;
    esac
done

echo "[CTF Recovery] Detected unintended system compromise..."
echo "[CTF Recovery] Initiating environment reset..."

echo "[CTF Recovery] Stopping and removing all containers and volumes..."
docker compose down -v

echo "[CTF Recovery] Cleaning up any stray volumes..."
docker volume rm $(docker volume ls -q) 2>/dev/null || true

echo "[CTF Recovery] Cleaning up any stray containers..."
docker rm -f $(docker ps -aq) 2>/dev/null || true

# Update GitLab root password in docker-compose.yml
echo "[CTF Recovery] Updating GitLab root password..."
sed -i "s/gitlab_rails\['initial_root_password'\] = .*/gitlab_rails['initial_root_password'] = '$GITLAB_ROOT_PASSWORD'/" docker-compose.yml

# Update setup.sh with new passwords
echo "[CTF Recovery] Updating user passwords in setup script..."
sed -i "s/ROOT_PASSWORD=.*/ROOT_PASSWORD=\"$GITLAB_ROOT_PASSWORD\"/" setup.sh
sed -i "s/\"password\": \"[^\"]*\"/\"password\": \"$NUTTY_PASSWORD\"/" setup.sh

echo "[CTF Recovery] Environment reset complete. Ready for next player."
echo "[CTF Recovery] New passwords:"
echo "  GitLab Root: $GITLAB_ROOT_PASSWORD"
echo "  Nutty User: $NUTTY_PASSWORD"
echo "[CTF Recovery] Run 'docker compose up -d && ./setup.sh' to reinitialize the challenge."

# Usage instructions
echo ""
echo "Usage:"
echo "  ./gothacked.sh                     # Reset with default passwords"
echo "  ./gothacked.sh -r <root_pass>      # Specify GitLab root password"
echo "  ./gothacked.sh -n <nutty_pass>     # Specify nutty user password"
echo "  ./gothacked.sh -r <root> -n <nutty> # Specify both passwords" 