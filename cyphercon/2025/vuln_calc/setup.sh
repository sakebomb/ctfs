#!/bin/bash

# Wait for GitLab to be ready
echo "Waiting for GitLab to be ready..."
while true; do
    if curl -s http://localhost:50002 | grep -q "sign_in"; then
        echo "GitLab is ready!"
        break
    fi
    echo "Waiting for GitLab to be ready..."
    sleep 10
done

# Get root token
echo "Getting root token..."
ROOT_PASSWORD="omgwtfbbq"
ROOT_TOKEN=$(curl -X POST -H "Content-Type: application/json" \
    -d "{\"grant_type\":\"password\",\"username\":\"root\",\"password\":\"$ROOT_PASSWORD\"}" \
    http://localhost:50002/oauth/token | jq -r '.access_token')

if [ -z "$ROOT_TOKEN" ] || [ "$ROOT_TOKEN" = "null" ]; then
    echo "Failed to get root token"
    exit 1
fi

# Create personal access token for root user
echo "Creating personal access token for root user..."
PAT_TOKEN=$(curl -X POST -H "Authorization: Bearer $ROOT_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"name":"setup-token","scopes":["api"]}' \
    http://localhost:50002/api/v4/users/1/personal_access_tokens | jq -r '.token')

if [ -z "$PAT_TOKEN" ] || [ "$PAT_TOKEN" = "null" ]; then
    echo "Failed to create personal access token"
    exit 1
fi

# Save the token for later use
echo "$PAT_TOKEN" > .gitlab_token

# Create user 'nutty'
echo "Creating user 'nutty'..."
curl -X POST -H "PRIVATE-TOKEN: $PAT_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"username": "nutty", "name": "Nutty User", "email": "nutty@example.com", "password": "N3wP@ssw0rd!2024"}' \
    http://localhost:50002/api/v4/users

# Create projects
echo "Creating projects..."
curl -X POST -H "PRIVATE-TOKEN: $PAT_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"name": "project1", "visibility": "private"}' \
    http://localhost:50002/api/v4/projects

curl -X POST -H "PRIVATE-TOKEN: $PAT_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"name": "project2", "visibility": "private"}' \
    http://localhost:50002/api/v4/projects

# Create the Domino's coupon cracker project
echo "Creating Domino's coupon cracker project..."
curl -X POST -H "PRIVATE-TOKEN: $PAT_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"name": "dominos-coupon-cracker", "visibility": "private", "description": "A tool to generate and validate Domino'\''s Pizza coupon codes"}' \
    http://localhost:50002/api/v4/projects

# Initialize the repository and push the code
echo "Setting up the Domino's coupon cracker repository..."
cd dominos-coupon-cracker
git init
git add .
git config user.email "nutty@example.com"
git config user.name "Nutty User"
git commit -m "Initial commit"
git remote add origin http://root:$PAT_TOKEN@localhost:50002/root/dominos-coupon-cracker.git
git push -u origin master
cd ..

# Set up the fakegit directory
echo "Setting up fakegit directory..."
cd flask_app
./setup_fakegit.sh
cd ..

echo "Setup complete!" 