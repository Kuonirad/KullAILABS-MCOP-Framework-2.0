#!/bin/bash
set -e

VERSION=${1:-"2.0.0"}

# Ensure git is available
if ! command -v git &> /dev/null; then
    echo "Error: git is not installed"
    exit 1
fi

# Check for clean working directory
if [ -n "$(git status --porcelain)" ]; then
  echo "Error: Working directory not clean. Commit or stash changes first."
  exit 1
fi

# Fetch tags to ensure we don't conflict
git fetch --tags

# Check if tag exists
if git rev-parse "v$VERSION" >/dev/null 2>&1; then
    echo "Error: Tag v$VERSION already exists"
    exit 1
fi

echo "Tagging v$VERSION on current commit $(git rev-parse --short HEAD)"
git tag -a "v$VERSION" -m "Release v$VERSION – Production-ready with hardened CI/CD and observability"
git push origin "v$VERSION"

echo "Tag v$VERSION pushed successfully."
echo "This will trigger the publish.yml workflow to build and push versioned Docker images to GHCR."
echo "Note: Ensure you have approved the deployment in GitHub Settings > Environments > production."
