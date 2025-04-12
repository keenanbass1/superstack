#!/bin/bash
# Superstack Development Environment Setup Script
# This script installs and configures all necessary tools for the Superstack development workflow

# Text formatting
BOLD="\e[1m"
RESET="\e[0m"
GREEN="\e[32m"
BLUE="\e[34m"
YELLOW="\e[33m"

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

# Function to install packages based on OS
install_packages() {
  echo -e "\n${BOLD}${BLUE}📦 Installing required packages...${RESET}"
  
  case $OS in
    Linux)
      sudo apt update
      sudo apt install -y curl git nodejs npm zsh
      ;;
    MacOS)
      if command_exists brew; then
        brew update
        brew install git node zsh
      else
        echo -e "${YELLOW}Homebrew not found. Please install Homebrew first:${RESET}"
        echo "https://brew.sh/"
        exit 1
      fi
      ;;
    Windows)
      if $IS_WSL; then
        sudo apt update
        sudo apt install -y curl git nodejs npm zsh
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
  
  echo -e "${GREEN}✓${RESET} Basic packages installed"
}

# Install Oh My Zsh
install_oh_my_zsh() {
  if [[ ! -d "$HOME/.oh-my-zsh" ]]; then
    echo -e "\n${BOLD}${BLUE}🐚 Installing Oh My Zsh...${RESET}"
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
    echo -e "${GREEN}✓${RESET} Oh My Zsh installed"
  else
    echo -e "\n${GREEN}✓${RESET} Oh My Zsh already installed"
  fi
}

# Install Node.js and npm packages
setup_node() {
  echo -e "\n${BOLD}${BLUE}🟢 Setting up Node.js environment...${RESET}"
  
  # Install NVM
  if [[ ! -d "$HOME/.nvm" ]]; then
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
    
    # Add NVM to path for current session
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    
    echo -e "${GREEN}✓${RESET} NVM installed"
  else
    echo -e "${GREEN}✓${RESET} NVM already installed"
  fi
  
  # Install latest LTS Node.js
  nvm install --lts
  nvm use --lts
  
  echo -e "${GREEN}✓${RESET} Node.js $(node -v) installed and active"
  
  # Install global npm packages
  npm install -g typescript ts-node nodemon eslint prettier
  echo -e "${GREEN}✓${RESET} Global npm packages installed"
}

# Set up CLI tool
setup_cli() {
  echo -e "\n${BOLD}${BLUE}🛠️  Setting up the dev CLI...${RESET}"
  
  # Navigate to CLI directory
  cd "$(dirname "$0")/dev"
  
  # Install dependencies
  npm install
  
  # Build the CLI
  npm run build
  
  # Link the CLI globally
  npm link
  
  echo -e "${GREEN}✓${RESET} CLI tool installed"
  echo -e "You can now use the ${BOLD}dev${RESET} command globally"
}

# Set up configuration files
setup_config() {
  echo -e "\n${BOLD}${BLUE}⚙️  Setting up configuration files...${RESET}"
  
  # Set up environment variables
  ENV_FILE="$HOME/.dev_env"
  if [[ ! -f "$ENV_FILE" ]]; then
    cat > "$ENV_FILE" << EOF
# Superstack Environment Variables
export DEV_ROOT="$HOME/dev"
export SUPERSTACK_DIR="$HOME/dev/superstack"
export PROJECTS_DIR="$HOME/dev/projects"
export PATH="\$PATH:\$SUPERSTACK_DIR/scripts/bin"
EOF
    
    # Add sourcing to shell config
    if [[ -f "$HOME/.zshrc" ]]; then
      echo -e "\n# Superstack Environment\n[ -f ~/.dev_env ] && source ~/.dev_env" >> "$HOME/.zshrc"
    fi
    
    if [[ -f "$HOME/.bashrc" ]]; then
      echo -e "\n# Superstack Environment\n[ -f ~/.dev_env ] && source ~/.dev_env" >> "$HOME/.bashrc"
    fi
    
    echo -e "${GREEN}✓${RESET} Environment variables configured"
  else
    echo -e "${GREEN}✓${RESET} Environment file already exists"
  fi
}

# Main installation flow
main() {
  install_packages
  install_oh_my_zsh
  setup_node
  setup_config
  setup_cli
  
  echo -e "\n${BOLD}${GREEN}✅ Superstack development environment setup complete!${RESET}"
  echo -e "\nTo start using the system:"
  echo -e "1. Close and reopen your terminal (or run 'source ~/.zshrc')"
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
