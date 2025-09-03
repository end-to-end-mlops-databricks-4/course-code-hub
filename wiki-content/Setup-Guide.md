# Setup Guide

## Environment Setup

### Prerequisites
- Python 3.12
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
git clone https://github.com/end-to-end-mlops-databricks-4/course-code-hub.git
cd course-code-hub
```

### Step 3: Create Environment
```bash
uv venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv sync --extra dev
```

### Step 4: Databricks CLI Setup
```bash
# Install Databricks CLI
brew install databricks  # macOS
# For Windows: download from GitHub releases

# Authenticate
databricks auth login --host <workspace-url>
```

---

## Step 5: VS Code Databricks Extension Setup

### 1. Install Visual Studio Code
If you don’t already have VS Code installed, download and install it from the [official website](https://code.visualstudio.com/).

### 2. Install the Databricks VS Code Extension
- Open VS Code.
- Go to the Extensions view by clicking the square icon in the sidebar or pressing `Cmd+Shift+X` (`Ctrl+Shift+X` on Windows).
- Search for `Databricks` and install the official **Databricks** extension by Databricks.

### 3. Configure the Extension
- After installation, open the Command Palette (`Cmd+Shift+P` or `Ctrl+Shift+P`).
- Type `Databricks: Configure Workspace` and select it.
- Enter your Databricks workspace URL (e.g., `https://<your-instance>.cloud.databricks.com`).
- Authenticate using your Databricks personal access token (PAT) or follow the login prompt.

### 4. Connect and Use
- Use the Databricks sidebar in VS Code to browse your workspace, clusters, jobs, and notebooks.
- You can open and edit notebooks directly in VS Code.
- Use the extension to sync local files to your Databricks workspace, run jobs, and more.

**Tip:** For more details, see the [Databricks VS Code Extension documentation](https://marketplace.visualstudio.com/items?itemName=databricks.databricks).

---