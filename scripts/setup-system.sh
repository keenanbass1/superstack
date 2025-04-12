#!/bin/bash
# Superstack Development Environment Setup Script
# This script installs and configures all necessary tools for the Superstack development workflow

# Text formatting
BOLD="\e[1m"
RESET="\e[0m"
GREEN="\e[32m"
BLUE="\e[34m"
YELLOW="\e[33m"
RED="\e[31m"

echo -e "${BOLD}${BLUE}🚀 SUPERSTACK DEVELOPMENT ENVIRONMENT SETUP${RESET}"
echo -e "This script will set up your development environment for the Superstack workflow system.\n"

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  OS="Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
  OS="MacOS"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
  OS="Windows"
else
  OS="Unknown"
fi
echo -e "${BOLD}Detected OS:${RESET} $OS"

# Check for WSL on Windows
if [[ "$OS" == "Windows" && -f /proc/version ]] && grep -q Microsoft /proc/version; then
  echo -e "${BOLD}Running in WSL:${RESET} Yes"
  IS_WSL=true
else
  IS_WSL=false
fi

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Function to create backup of config files
backup_config() {
  local config_file="$1"
  if [[ -f "$config_file" ]]; then
    local backup_file="${config_file}.bak-$(date +%Y%m%d%H%M%S)"
    cp "$config_file" "$backup_file"
    echo -e "${GREEN}✓${RESET} Backed up ${config_file} to ${backup_file}"
  fi
}

# Function to install packages based on OS
install_packages() {
  echo -e "\n${BOLD}${BLUE}📦 Checking for required packages...${RESET}"
  
  local packages_to_install=()
  
  # Check for required tools
  for tool in git curl; do
    if ! command_exists "$tool"; then
      packages_to_install+=("$tool")
    else
      echo -e "${GREEN}✓${RESET} $tool is already installed"
    fi
  done
  
  # Check for Node.js and npm
  if command_exists node; then
    NODE_VERSION=$(node -v)
    echo -e "${GREEN}✓${RESET} Node.js ${NODE_VERSION} is already installed"
    NEED_NODE=false
  else
    packages_to_install+=("nodejs")
    NEED_NODE=true
  fi
  
  if command_exists npm; then
    NPM_VERSION=$(npm -v)
    echo -e "${GREEN}✓${RESET} npm ${NPM_VERSION} is already installed"
    NEED_NPM=false
  else
    packages_to_install+=("npm")
    NEED_NPM=true
  fi
  
  # Check for zsh
  if ! command_exists zsh; then
    packages_to_install+=("zsh")
  else
    echo -e "${GREEN}✓${RESET} zsh is already installed"
  fi
  
  # Install missing packages if needed
  if [ ${#packages_to_install[@]} -ne 0 ]; then
    echo -e "Installing packages: ${packages_to_install[*]}"
    
    case $OS in
      Linux)
        sudo apt update
        sudo apt install -y "${packages_to_install[@]}"
        ;;
      MacOS)
        if command_exists brew; then
          brew update
          brew install "${packages_to_install[@]}"
        else
          echo -e "${YELLOW}Homebrew not found. Please install Homebrew first:${RESET}"
          echo "https://brew.sh/"
          exit 1
        fi
        ;;
      Windows)
        if $IS_WSL; then
          sudo apt update
          sudo apt install -y "${packages_to_install[@]}"
        else
          echo -e "${YELLOW}On Windows, please install these tools manually:${RESET}"
          echo "- Git: https://git-scm.com/download/win"
          echo "- Node.js: https://nodejs.org/"
          echo "- WSL: https://docs.microsoft.com/en-us/windows/wsl/install"
          exit 1
        fi
        ;;
      *)
        echo "Unsupported OS. Please install dependencies manually."
        exit 1
        ;;
    esac
    
    echo -e "${GREEN}✓${RESET} Required packages installed"
  else
    echo -e "${GREEN}✓${RESET} All required packages are already installed"
  fi
}

# Set up Node.js environment (only if needed)
setup_node() {
  echo -e "\n${BOLD}${BLUE}🟢 Checking Node.js environment...${RESET}"
  
  # Check if NVM is already installed and working
  if [[ -d "$HOME/.nvm" ]]; then
    echo -e "${GREEN}✓${RESET} NVM directory exists"
    
    # Try to load NVM
    export NVM_DIR="$HOME/.nvm"
    if [[ -s "$NVM_DIR/nvm.sh" ]]; then
      source "$NVM_DIR/nvm.sh"  # This loads nvm
      if command_exists nvm; then
        echo -e "${GREEN}✓${RESET} NVM is working"
        NVM_WORKS=true
      else
        echo -e "${YELLOW}⚠️ NVM directory exists but command not found. Skipping NVM setup.${RESET}"
        NVM_WORKS=false
      fi
    else
      echo -e "${YELLOW}⚠️ NVM installation appears incomplete. Skipping NVM setup.${RESET}"
      NVM_WORKS=false
    fi
  else
    echo -e "NVM not found. Using system Node.js and npm."
    NVM_WORKS=false
  fi
  
  # Check Node.js version
  if command_exists node; then
    NODE_VERSION=$(node -v)
    NODE_MAJOR_VERSION=$(echo $NODE_VERSION | cut -d. -f1 | tr -d 'v')
    
    echo -e "${GREEN}✓${RESET} Using Node.js ${NODE_VERSION}"
    
    # Only attempt to install node with NVM if current version is old and NVM works
    if [[ $NODE_MAJOR_VERSION -lt 16 ]] && [[ "$NVM_WORKS" = true ]]; then
      echo -e "${YELLOW}Current Node.js version is older than recommended. Installing LTS version with NVM...${RESET}"
      nvm install --lts
      nvm use --lts
      echo -e "${GREEN}✓${RESET} Now using Node.js $(node -v)"
    fi
  elif [[ "$NVM_WORKS" = true ]]; then
    # No Node.js found, but NVM works, so install Node.js
    echo -e "Installing Node.js LTS with NVM..."
    nvm install --lts
    nvm use --lts
    echo -e "${GREEN}✓${RESET} Node.js $(node -v) installed and active"
  else
    echo -e "${YELLOW}⚠️ Node.js not found and NVM not working. Please install Node.js manually.${RESET}"
    exit 1
  fi
  
  # Install global npm packages if needed
  echo -e "\nChecking for required global npm packages..."
  
  for package in typescript ts-node nodemon eslint prettier; do
    if npm list -g "$package" > /dev/null 2>&1; then
      echo -e "${GREEN}✓${RESET} $package is already installed globally"
    else
      echo -e "Installing $package globally..."
      npm install -g "$package"
    fi
  done
  
  echo -e "${GREEN}✓${RESET} All required global npm packages are installed"
}

# Set up CLI tool
setup_cli() {
  echo -e "\n${BOLD}${BLUE}🛠️  Setting up the dev CLI...${RESET}"
  
  # Navigate to CLI directory
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  CLI_DIR="${SCRIPT_DIR}/dev"
  
  if [[ ! -d "$CLI_DIR" ]]; then
    echo -e "${RED}❌ CLI directory not found at ${CLI_DIR}${RESET}"
    return 1
  fi
  
  # Save current directory to return to it later
  CURRENT_DIR=$(pwd)
  cd "$CLI_DIR" || return 1
  
  # Install dependencies
  echo "Installing CLI dependencies..."
  npm install
  
  # Build the CLI
  echo "Building the CLI..."
  npm run build
  
  # Link the CLI globally
  echo "Linking the CLI globally..."
  npm link
  
  # Return to the original directory
  cd "$CURRENT_DIR" || return 1
  
  echo -e "${GREEN}✓${RESET} CLI tool installed"
  echo -e "You can now use the ${BOLD}dev${RESET} command globally"
}

# Set up configuration files
setup_config() {
  echo -e "\n${BOLD}${BLUE}⚙️  Setting up configuration files...${RESET}"
  
  # Define project directories
  DEV_ROOT="$HOME/dev"
  SUPERSTACK_DIR="$HOME/dev/superstack"
  PROJECTS_DIR="$HOME/dev/projects"
  
  # Create directories if they don't exist
  for dir in "$DEV_ROOT" "$PROJECTS_DIR"; do
    if [[ ! -d "$dir" ]]; then
      mkdir -p "$dir"
      echo -e "${GREEN}✓${RESET} Created directory: $dir"
    else
      echo -e "${GREEN}✓${RESET} Directory already exists: $dir"
    fi
  done
  
  # Set up environment variables
  ENV_FILE="$HOME/.dev_env"
  if [[ ! -f "$ENV_FILE" ]]; then
    cat > "$ENV_FILE" << EOF
# Superstack Environment Variables
export DEV_ROOT="$DEV_ROOT"
export SUPERSTACK_DIR="$SUPERSTACK_DIR"
export PROJECTS_DIR="$PROJECTS_DIR"
export PATH="\$PATH:\$SUPERSTACK_DIR/scripts/bin"
EOF
    
    echo -e "${GREEN}✓${RESET} Created environment file: $ENV_FILE"
  else
    echo -e "${GREEN}✓${RESET} Environment file already exists: $ENV_FILE"
  fi
  
  # Add sourcing to shell config if not already there
  for shell_rc in "$HOME/.zshrc" "$HOME/.bashrc"; do
    if [[ -f "$shell_rc" ]]; then
      # Backup the shell config file
      backup_config "$shell_rc"
      
      # Check if sourcing already exists
      if ! grep -q "source ~/.dev_env" "$shell_rc"; then
        echo -e "\n# Superstack Environment\n[ -f ~/.dev_env ] && source ~/.dev_env" >> "$shell_rc"
        echo -e "${GREEN}✓${RESET} Added environment sourcing to $shell_rc"
      else
        echo -e "${GREEN}✓${RESET} Environment sourcing already exists in $shell_rc"
      fi
    fi
  done
}

# Main installation flow
main() {
  install_packages
  setup_node
  setup_config
  setup_cli
  
  echo -e "\n${BOLD}${GREEN}✅ Superstack development environment setup complete!${RESET}"
  echo -e "\nTo start using the system:"
  echo -e "1. Close and reopen your terminal (or run 'source ~/.zshrc' or 'source ~/.bashrc')"
  echo -e "2. Run ${BOLD}dev${RESET} to see available commands"
  echo -e "3. Create your first project with ${BOLD}dev new my-project${RESET}"
}

# Ask for confirmation
read -p "This will install various tools and modify your shell configuration. Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Setup canceled."
  exit 0
fi

# Run the main installation
main
