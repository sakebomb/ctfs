#!/bin/bash

# Wait for GitLab to be ready
until curl -s http://localhost:80 > /dev/null; do
  echo "Waiting for GitLab to be ready..."
  sleep 5
done

# Create a new project
curl --request POST --header "PRIVATE-TOKEN: glpat-XXXXXXXXXXXXXXXXXXXX" \
     --header "Content-Type: application/json" \
     --data '{"name": "nutty-calculator", "visibility": "public"}' \
     http://localhost:80/api/v4/projects

# Clone the repository
git clone http://localhost:80/nutty/nutty-calculator.git
cd nutty-calculator

# Copy the vulnerable calculator code
cp /app/main.py .

# Commit and push
git add .
git config --global user.email "nutty@example.com"
git config --global user.name "Nutty"
git commit -m "Initial commit"
git push -u origin master 