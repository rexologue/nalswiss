#!/usr/bin/env bash
set -euo pipefail

# Build wheel with Poetry, compute SHA256, and print a ready-to-copy pipx line.
# Usage: scripts/release.sh https://your.git.host/you/nalswiss/releases/download v0.1.0

BASE_URL="${1:-}"   # e.g. https://github.com/you/nalswiss/releases/download
VERSION="${2:-}"    # e.g. v0.1.0

if [[ -z "$BASE_URL" || -z "$VERSION" ]]; then
  echo "Usage: $0 <BASE_RELEASE_URL> <TAG_VERSION>" 1>&2
  exit 1
fi

poetry build
WHEEL_PATH=$(ls -1 dist/nalswiss-*-py3-none-any.whl | tail -n1)
WHEEL_FILE=$(basename "$WHEEL_PATH")
HASH=$(sha256sum "$WHEEL_PATH" | awk '{print $1}')

FULL_URL="$BASE_URL/$VERSION/$WHEEL_FILE"

echo "
Wheel: $WHEEL_FILE"
echo "SHA256: $HASH"
echo "
Install via pipx (one line):"
echo "pipx install $FULL_URL"
echo "
With integrity pinning (one line):"
echo "pipx install \"$FULL_URL#sha256=$HASH\""
