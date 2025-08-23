# Python Environment Setup

## Pyenv + Pipenv Overview
- **Pyenv**: Manages multiple Python versions
- **Pipenv**: Manages project dependencies and virtual environments
- **Pipfile**: Modern replacement for requirements.txt
- **Pipfile.lock**: Locked dependency versions for reproducible builds

## Installation

### Pyenv Setup
```bash
# Ubuntu/Debian
curl https://pyenv.run | bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc

# macOS
brew install pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc
```

### Pipenv Setup
```bash
pip install pipenv
```

## Project Setup

### 1. Set Python Version
```bash
cd /path/to/project
pyenv install 3.11.5
pyenv local 3.11.5
python --version
```

### 2. Initialize Environment
```bash
pipenv install
```

## Dependency Management

### Basic Commands
```bash
pipenv install requests          # Install package
pipenv install pytest --dev      # Install dev dependency
pipenv install --ignore-pipfile  # Install from lock file
pipenv update                    # Update all dependencies
pipenv uninstall requests        # Remove package
pipenv shell                     # Activate environment
exit                            # Deactivate environment
```

### Git Dependencies
```toml
# In Pipfile
[packages]
my-package = {git = "https://github.com/user/package.git", ref = "main"}
```

### Architecture-Specific Dependencies
```bash
pipenv install --platform linux_x86_64 package-name
pipenv install --platform darwin_arm64 package-name
```

## Best Practices

### Project Structure
```
project/
├── Pipfile
├── Pipfile.lock
├── .python-version
├── src/
├── tests/
└── README.md
```

### Version Control
```bash
git add Pipfile Pipfile.lock
pyenv local 3.11.5
echo "3.11.5" > .python-version
```

### Security
```bash
pipenv check                    # Check vulnerabilities
pipenv update --outdated        # Update security patches
```

## Troubleshooting

### Common Issues
```bash
pyenv install --list            # List available Python versions
pipenv --rm                     # Remove virtual environment
pipenv lock --clear             # Regenerate lock file
pipenv install --user           # Install with user flag
```

## CI/CD Integration

### GitHub Actions
```yaml
- name: Install pipenv
  run: pip install pipenv
- name: Install dependencies
  run: pipenv install --dev
- name: Run tests
  run: pipenv run pytest
```

### Docker
```dockerfile
FROM python:3.11-slim
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy
COPY . .
CMD ["python", "app.py"]
```

## Pyenv + Pipenv vs Poetry

| Feature | Pyenv + Pipenv | Poetry |
|---------|----------------|---------|
| **Tools** | Two separate tools | Single unified tool |
| **Config Files** | Pipfile + Pipfile.lock | pyproject.toml + poetry.lock |
| **Python Version Management** | Pyenv handles this | Built-in version management |
| **Dependency Resolution** | Basic resolver | Advanced resolver |
| **Package Building** | Not supported | Built-in build system |
| **Publishing** | Manual process | Built-in publish command |
| **Virtual Environments** | Pipenv creates/manages | Poetry creates/manages |
| **Maturity** | More mature, stable | Newer, actively developed |
| **Learning Curve** | Steeper (two tools) | Gentler (one tool) |
| **Configuration** | Multiple config locations | Single pyproject.toml |
| **Standards Compliance** | Pre-PEP 518 | PEP 518/621 compliant |
| **Community** | Large, established | Growing rapidly |

### When to Choose Each

**Choose Pyenv + Pipenv when:**
- Working with existing projects using Pipfile
- Need fine-grained control over Python versions
- Team is familiar with the workflow
- Working in environments where Poetry isn't available

**Choose Poetry when:**
- Starting new projects
- Need to build/publish packages
- Want modern Python tooling
- Prefer single-tool simplicity

## Useful Commands
```bash
pipenv graph                    # Show dependency graph
pipenv show                     # Show package info
pipenv run python app.py        # Run in environment
pipenv --venv                   # Show venv path
```
