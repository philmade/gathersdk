#!/usr/bin/env python3
"""
Check current PyPI version and suggest next version
"""

import subprocess
import json
import re

def get_pypi_versions(package_name):
    """Get all versions from PyPI"""
    try:
        result = subprocess.run(
            ["pip", "index", "versions", package_name],
            capture_output=True,
            text=True
        )
        
        # Parse the output
        output = result.stdout
        if "Available versions:" in output:
            versions_line = output.split("Available versions:")[1].split("\n")[0]
            versions = [v.strip() for v in versions_line.split(",")]
            return versions
        return []
    except Exception as e:
        print(f"Error checking PyPI: {e}")
        return []

def get_setup_version():
    """Get current version from setup.py"""
    with open("setup.py", "r") as f:
        content = f.read()
        match = re.search(r'version="([^"]+)"', content)
        if match:
            return match.group(1)
    return None

def suggest_next_version(current_version):
    """Suggest next patch version"""
    parts = current_version.split(".")
    if len(parts) == 3:
        major, minor, patch = parts
        return f"{major}.{minor}.{patch}.1"
    elif len(parts) == 4:
        major, minor, patch, micro = parts
        return f"{major}.{minor}.{patch}.{int(micro) + 1}"
    return None

if __name__ == "__main__":
    package = "gathersdk"
    
    print(f"Checking {package} versions...")
    
    # Get PyPI versions
    pypi_versions = get_pypi_versions(package)
    if pypi_versions:
        print(f"Latest PyPI version: {pypi_versions[0]}")
        print(f"All PyPI versions: {', '.join(pypi_versions)}")
    
    # Get local version
    local_version = get_setup_version()
    if local_version:
        print(f"Current setup.py version: {local_version}")
    
    # Suggest next version
    if pypi_versions:
        next_version = suggest_next_version(pypi_versions[0])
        if next_version:
            print(f"\nSuggested next version: {next_version}")
            print(f"\nTo update, run:")
            print(f"  sed -i 's/version=\"{local_version}\"/version=\"{next_version}\"/' setup.py")