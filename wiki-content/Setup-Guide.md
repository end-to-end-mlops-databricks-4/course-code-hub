# Setup Guide

## Environment Setup

### Prerequisites
- Python 3.11
- UV package manager
- Databricks account
- GitHub account

### Step 1: Install UV
```bash
# macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Step 2: Clone Repository
```bash
git clone https://github.com/end-to-end-mlops-databricks-3/course-code-hub3.git
cd course-code-hub3
```

### Step 3: Create Environment
```bash
uv venv -p 3.11 .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv sync --extra dev
```

### Step 4: Databricks CLI Setup
```bash
# Install Databricks CLI
brew install databricks  # macOS
# For Windows: download from GitHub releases

# Authenticate
databricks auth login --configure-cluster --host <workspace-url>
```