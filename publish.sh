#!/bin/bash
# Comprehensive publish script for GatherChat Agent SDK
# Handles: version increment, git push, PyPI build & publish

set -e

echo "🚀 Publishing GatherChat Agent SDK..."

# Function to increment version
increment_version() {
    local version=$1
    local part=${2:-patch}  # default to patch
    
    IFS='.' read -ra PARTS <<< "$version"
    major=${PARTS[0]}
    minor=${PARTS[1]}
    patch=${PARTS[2]}
    
    case $part in
        major)
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        minor)
            minor=$((minor + 1))
            patch=0
            ;;
        patch)
            patch=$((patch + 1))
            ;;
    esac
    
    echo "${major}.${minor}.${patch}"
}

# Get current version from setup.py
CURRENT_VERSION=$(python3 -c "import re; content = open('setup.py').read(); print(re.search(r'version=\"([^\"]+)\"', content).group(1))")
echo "Current version: $CURRENT_VERSION"

# Increment version (default to patch)
VERSION_PART=${1:-patch}
NEW_VERSION=$(increment_version $CURRENT_VERSION $VERSION_PART)
echo "New version: $NEW_VERSION"

# Update version in setup.py
sed -i "s/version=\"$CURRENT_VERSION\"/version=\"$NEW_VERSION\"/" setup.py

# Update version in __init__.py
sed -i "s/__version__ = \"$CURRENT_VERSION\"/__version__ = \"$NEW_VERSION\"/" gathersdk/__init__.py

# Update version in pyproject.toml if it exists
if [ -f "pyproject.toml" ]; then
    sed -i "s/version = \"$CURRENT_VERSION\"/version = \"$NEW_VERSION\"/" pyproject.toml
fi

echo "✅ Version updated to $NEW_VERSION"

# Git operations
echo "📝 Committing changes..."
git add -A
git commit -m "Release v$NEW_VERSION - SDK improvements and fixes" || true

echo "📤 Pushing to GitHub..."
git push origin main || git push origin master || git push origin HEAD

echo "🏷️  Creating git tag..."
git tag -a "v$NEW_VERSION" -m "Release v$NEW_VERSION"
git push --tags

# Clean old builds
echo "🧹 Cleaning old builds..."
rm -rf dist/ build/ *.egg-info/

# Build the package
echo "📦 Building package..."
python3 -m build

# Upload to PyPI
echo "📤 Uploading to PyPI..."
python3 -m twine upload dist/* --skip-existing

echo "✅ Successfully published gathersdk v$NEW_VERSION to PyPI!"
echo ""
echo "Install with: pip install gathersdk==$NEW_VERSION"