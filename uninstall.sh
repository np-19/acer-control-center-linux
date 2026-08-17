#!/bin/bash

set -e

APP_NAME="acer-control-center"
INSTALL_DIR="/opt/$APP_NAME"
BIN="/usr/local/bin/$APP_NAME"
DESKTOP="/usr/share/applications/$APP_NAME.desktop"
ICON="/usr/share/icons/hicolor/scalable/apps/$APP_NAME.svg"

echo "======================================"
echo " Acer Control Center for Linux"
echo " Uninstallation"
echo "======================================"
echo ""

# Check for sudo
if ! command -v sudo >/dev/null 2>&1; then
    echo "Error: sudo is required."
    exit 1
fi

echo "Removing Acer Control Center..."

# Remove application files
if [ -d "$INSTALL_DIR" ]; then
    sudo rm -rf "$INSTALL_DIR"
    echo "✓ Application files removed"
fi

# Remove command launcher
if [ -f "$BIN" ]; then
    sudo rm -f "$BIN"
    echo "✓ Command launcher removed"
fi

# Remove desktop entry
if [ -f "$DESKTOP" ]; then
    sudo rm -f "$DESKTOP"
    echo "✓ Desktop entry removed"
fi

# Remove icon
if [ -f "$ICON" ]; then
    sudo rm -f "$ICON"
    echo "✓ Application icon removed"
fi

# Refresh desktop database
sudo update-desktop-database /usr/share/applications 2>/dev/null || true
sudo gtk-update-icon-cache /usr/share/icons/hicolor 2>/dev/null || true

echo ""
echo "======================================"
echo " Uninstallation completed!"
echo "======================================"
echo ""
echo "Acer Control Center has been removed."
