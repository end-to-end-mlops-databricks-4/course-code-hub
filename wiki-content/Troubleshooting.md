# Troubleshooting

## Common Issues and Solutions

### Environment Issues

#### Python Version Mismatch
**Problem**: Wrong Python version
**Solution**: 
```bash
pyenv install 3.11.6
pyenv shell 3.11.6
uv venv -p 3.11 .venv
```

#### Package Installation Fails
**Problem**: UV sync fails
**Solution**:
```bash
# Clear cache and retry
uv cache clean
uv sync --extra dev --no-cache
```

### Databricks Issues

#### Authentication Fails
**Problem**: Cannot connect to Databricks
**Solution**:
1. Check workspace URL format
2. Verify access tokens
3. Use Course cluster policy

#### Private Package Access
**Problem**: Cannot install marvelous package
**Solution**:
1. Update `pyproject.toml` with HTTPS URL
2. Set `GITHUB_TOKEN` environment variable
3. Use Course cluster policy with init script

### GitHub Issues

#### PR Creation Fails
**Problem**: Cannot create pull request
**Solution**:
1. Ensure you're on a feature branch
2. Check repository permissions
3. Verify branch naming conventions

### MLflow Issues

#### Experiment Tracking Not Working
**Problem**: MLflow runs not appearing
**Solution**:
1. Check experiment name
2. Verify MLflow tracking URI
3. Ensure proper authentication

## Getting Help

1. **Check this wiki first** - common issues are documented here
2. **Search course repository issues** - others may have faced similar problems
3. **Ask in course discussions** - instructors and peers can help
4. **Create detailed issue reports** - include error messages and environment info
