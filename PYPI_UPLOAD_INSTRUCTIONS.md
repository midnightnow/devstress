# 📦 PyPI Upload Instructions

## Prerequisites
1. Create accounts at:
   - https://pypi.org/account/register/ (Production)
   - https://test.pypi.org/account/register/ (Testing)

2. Generate API tokens:
   - Go to Account Settings → API tokens
   - Create a token for "Entire account" (first upload) or "Project: devstress" (updates)
   - Save the token securely (starts with `pypi-`)

## Upload to Test PyPI (Recommended First)
```bash
# Using token (recommended)
python3 -m twine upload --repository testpypi dist/* \
  --username __token__ \
  --password YOUR_TEST_PYPI_TOKEN

# Test installation
pip install -i https://test.pypi.org/simple/ devstress
```

## Upload to Production PyPI
```bash
# Using token
python3 -m twine upload dist/* \
  --username __token__ \
  --password YOUR_PYPI_TOKEN

# Verify installation
pip install devstress
devstress --version
```

## Alternative: Using .pypirc File
Create `~/.pypirc`:
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR-TOKEN-HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR-TEST-TOKEN-HERE
```

Then upload with:
```bash
# Test PyPI
python3 -m twine upload --repository testpypi dist/*

# Production PyPI
python3 -m twine upload dist/*
```

## Post-Upload Verification
1. Check package page: https://pypi.org/project/devstress/
2. Test installation in a fresh environment:
   ```bash
   python3 -m venv test_env
   source test_env/bin/activate
   pip install devstress
   devstress --version
   ```

## Updating the Package
For future updates:
1. Update version in `setup.py`
2. Rebuild: `python3 -m build`
3. Upload: `python3 -m twine upload dist/* --skip-existing`

## GitHub Release
After PyPI upload:
```bash
git tag v1.0.0
git push origin v1.0.0
gh release create v1.0.0 dist/* \
  --title "DevStress v1.0.0 - Zero-Config Load Testing" \
  --notes "First public release of DevStress"
```