#!/bin/bash

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
BOLD='\033[1m'
RESET='\033[0m'

echo -e "${BOLD}${BLUE}Superstack Developer CLI Installer${RESET}\n"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
  echo -e "${RED}Error: npm is not installed. Please install Node.js and npm first.${RESET}"
  exit 1
fi

# Install dependencies
echo -e "${BLUE}Installing dependencies...${RESET}"
npm install

# Build the CLI
echo -e "${BLUE}Building the CLI...${RESET}"
npm run build

# Create environment file if it doesn't exist
ENV_FILE="$HOME/.env"
if [[ ! -f "$ENV_FILE" ]]; then
  echo -e "${BLUE}Creating environment file at $ENV_FILE...${RESET}"
  
  # Get user's home directory
  USER_HOME="$HOME"
  
  # Create .env file
  cat > "$ENV_FILE" << EOF
# Superstack Developer CLI Environment Variables
DEV_ROOT=$USER_HOME/dev
PROJECTS_DIR=$USER_HOME/dev/projects
EOF
  
  echo -e "${GREEN}Created environment file: $ENV_FILE${RESET}"
  
  # Create directories
  mkdir -p "$USER_HOME/dev/projects"
  mkdir -p "$USER_HOME/dev/superstack/templates/project-types"
  
  echo -e "${GREEN}Created required directories${RESET}"
else
  echo -e "${GREEN}Environment file already exists: $ENV_FILE${RESET}"
fi

# Install globally
echo -e "${BLUE}Installing CLI globally...${RESET}"
npm link

echo -e "\n${GREEN}${BOLD}Installation complete!${RESET}"
echo -e "You can now use the ${BOLD}dev${RESET} command from anywhere."
echo -e "Try ${BOLD}dev --help${RESET} to get started."
