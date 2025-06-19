#!/bin/bash
# Simple publish script for GatherChat Agent SDK

set -e

echo "Publishing GatherChat Agent SDK..."

# Clean old builds
echo "Cleaning old builds..."
rm -rf dist/ build/ *.egg-info/

# Build the package
echo "Building package..."
python -m build

# Upload to PyPI
echo "Uploading to PyPI..."
echo "Run: python -m twine upload dist/*"
echo ""
echo "For test PyPI first:"
echo "python -m twine upload --repository testpypi dist/*"
echo ""
echo "Make sure you have ~/.pypirc configured with your API tokens"