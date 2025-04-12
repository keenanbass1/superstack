platform:
  os: Windows 11
  shell: WSL 2 (Ubuntu 22.04)
  location: Australia (timezone: AEST)
  arch: x86_64
  resources:
    cpu: Intel i9
    ram: 32GB
    gpu: RTX 4080 (CUDA support: true)
    storage: 1TB NVMe

dev_environment:
  editor: Cursor + Remote WSL
  terminal: Zsh with Oh-My-Zsh
  container: Docker Desktop (WSL backend)
  version_managers: nvm, bun
  ai_tools: Cursor, Cursor AI paid plan, Claude Desktop paid plan, ChatGPT Plus, Ollama (local models), Vercel v0 paid plan
