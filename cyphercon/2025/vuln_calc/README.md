# Vulnerable Calculator CTF Challenge

A deliberately vulnerable calculator service running in Docker, with an accompanying GitLab instance and web application. This is a CTF (Capture The Flag) challenge environment.

## ⚠️ WARNING

This system contains intentional vulnerabilities for educational purposes. DO NOT deploy this in a production environment or expose it to the public internet.

## Quick Start

To set up the challenge environment:

```bash
# Start all services
docker compose up -d

# Run initial setup (creates users, projects, etc.)
./setup.sh
```

## Services

The environment consists of three services:

1. **Nutty Calculator** (Port 31337)
   - A vulnerable calculator service
   - Accepts arithmetic expressions via TCP

2. **GitLab Instance** (Port 50002)
   - Self-hosted GitLab CE
   - Contains repositories with potential secrets
   - Default credentials:
     - Root user: root / omgwtfbbq
     - Regular user: nutty / N3wP@ssw0rd2024

3. **Flask Web App** (Port 50001)
   - Python Flask application
   - Interacts with other services

## For CTF Operators

### Recovery Scripts

If the system is compromised in an unintended way, use the recovery scripts to reset the environment:

```bash
# Quick reset with default passwords
./gothacked.sh

# Reset with custom root password
./gothacked.sh -r <new_root_password>

# Reset with custom nutty user password
./gothacked.sh -n <new_nutty_password>

# Reset with both custom passwords
./gothacked.sh -r <root_pass> -n <nutty_pass>
```

For complete cleanup and reset:

```bash
# Interactive cleanup (requires confirmation)
./developer/destroy_all.sh

# Non-interactive cleanup (skips confirmation)
./developer/destroy_all.sh -y
```

The recovery scripts will:
1. Stop and remove all containers and volumes
2. Clean up any stray Docker resources
3. Update passwords in configuration files
4. Preserve intended flags and vulnerabilities

### Default Ports

- Nutty Calculator: 31337
- GitLab: 50002
- Flask App: 50001

### Directory Structure

```
.
├── docker-compose.yml      # Service definitions and configuration
├── setup.sh               # Initial environment setup
├── gothacked.sh           # Recovery script for operators
├── developer/             # Developer tools and scripts
│   └── destroy_all.sh     # Complete cleanup script
├── nutty_calculator/      # Vulnerable calculator service
│   ├── main.py           # Calculator service code
│   └── Dockerfile        # Calculator service container definition
├── flask_app/            # Web application files
└── gitlab/               # GitLab configuration files
```

## Features

- Configurable service ports
- Automatic Docker environment setup
- Multiple interconnected services
- Built-in recovery mechanism
- Preserved flags across resets
- Developer tools for environment management

## Testing the Challenges

The environment includes a test script (`test_challenges.sh`) that verifies all challenges are working correctly:

```bash
# Run the test script
./test_challenges.sh
```

The script tests the following challenges:

1. **Nutty Calculator**
   - Type: RedTeam
   - Difficulty: 3/5
   - Tests arbitrary file read vulnerability
   - Verifies flag: `flag{AcidSmellsLikeCheese}`
   - Description: "This new Nutty intern can't even get a freaking calculator right. Thing doesn't seem to exit. I know there is a flag on his machine. Good luck."

2. **Nutty's Pipeline Paradise**
   - Type: RedTeam
   - Difficulty: 4/5
   - Tests GitLab CI/CD configuration exposure
   - Verifies flag: `flag{AllWorkAndNoPlayMakesNuttyAdullboi-uwu}`
   - Description: "Nutty's been promoted to DevOps (heaven help us). He's been raving about how 'automation is the future' and something about his 'super secure' CI/CD setup. At least he's using GitLab's built-in security features this time..."

3. **Nutty's Web Adventure (Git)**
   - Type: RedTeam
   - Difficulty: 4/5
   - Tests exposed Git repository
   - Verifies flag: `flag{GitIsWeirdAintIt}`
   - Description: "After the calculator incident, we let Nutty build a simple web server. He says it's totally secure because 'nobody can see how it works'. I don't have a good feeling about this..."

4. **Nutty's Web Adventure (Env)**
   - Type: RedTeam
   - Difficulty: 3/5
   - Tests exposed environment file
   - Verifies flag: `flag{Dominos20percentOffCoupon1126}`
   - Description: "Nutty's back! He's now claiming to be a 'web security expert'. He keeps muttering about environmental variables and how they're 'like ninjas - invisible but deadly'. I think he might have left his lunch order somewhere he shouldn't have... You know there is a domino's just down the road."

The test script verifies that:
- All services are running and accessible
- Each vulnerability can be successfully exploited
- All flags are present and correct
- The environment is properly configured

If any test fails, the script will provide detailed error output to help diagnose the issue. 