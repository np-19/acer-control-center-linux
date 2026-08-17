#!/bin/bash

set -e

APP_NAME="acer-control-center"
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
INSTALL_DIR="/opt/$APP_NAME"
BIN="/usr/local/bin/$APP_NAME"
DESKTOP="/usr/share/applications/$APP_NAME.desktop"
ICON_DIR="/usr/share/icons/hicolor/scalable/apps"
ICON="$ICON_DIR/$APP_NAME.svg"

echo "======================================"
echo " Acer Control Center for Linux"
echo " Installation"
echo "======================================"
echo ""

# Check for sudo
if ! command -v sudo >/dev/null 2>&1; then
    echo "Error: sudo is required."
    exit 1
fi

# Check for Python
if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: python3 is required."
    echo "Please install Python 3 first."
    exit 1
fi
echo ""
echo "Checking required dependencies..."

sudo apt-get update

sudo apt-get install -y \
    python3 \
    python3-gi \
    python3-psutil \
    gir1.2-gtk-4.0
echo "[1/5] Creating installation directories..."

sudo mkdir -p "$INSTALL_DIR"
sudo mkdir -p "$ICON_DIR"

echo "[2/5] Installing application files..."

sudo cp -r "$PROJECT_DIR/app" "$INSTALL_DIR/"
sudo cp -r "$PROJECT_DIR/assets" "$INSTALL_DIR/"
sudo cp -r "$PROJECT_DIR/backend" "$INSTALL_DIR/"
sudo cp -r "$PROJECT_DIR/gpu" "$INSTALL_DIR/"
sudo cp -r "$PROJECT_DIR/monitor" "$INSTALL_DIR/"
sudo cp -r "$PROJECT_DIR/power" "$INSTALL_DIR/"
sudo cp -r "$PROJECT_DIR/rgb" "$INSTALL_DIR/"

echo "[3/5] Creating application launcher..."

sudo tee "$BIN" > /dev/null <<EOF
#!/bin/bash
cd "$INSTALL_DIR"
exec python3 app/main.py "\$@"
EOF

sudo chmod +x "$BIN"

echo "[4/5] Installing application icon..."

sudo tee "$ICON" > /dev/null <<'EOF'
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <rect width="256" height="256" rx="48" fill="#171923"/>
  <rect x="36" y="52" width="184" height="120" rx="14"
        fill="none" stroke="#b026ff" stroke-width="12"/>
  <path d="M70 204h116"
        stroke="#b026ff" stroke-width="12" stroke-linecap="round"/>
  <path d="M92 92h72M92 124h48"
        stroke="#ffffff" stroke-width="10" stroke-linecap="round"/>
  <circle cx="174" cy="124" r="7" fill="#b026ff"/>
</svg>
EOF

echo "[5/5] Creating desktop entry..."

sudo tee "$DESKTOP" > /dev/null <<EOF
[Desktop Entry]
Name=Acer Control Center
Comment=Control and monitor Acer laptop hardware
Exec=$BIN
Icon=$APP_NAME
Terminal=false
Type=Application
Categories=Settings;System;HardwareSettings;
StartupNotify=true
EOF

# Refresh desktop/icon databases
sudo update-desktop-database /usr/share/applications 2>/dev/null || true
sudo gtk-update-icon-cache /usr/share/icons/hicolor 2>/dev/null || true

echo ""
echo "======================================"
echo " Installation completed successfully!"
echo "======================================"
echo ""
echo "Launch from the Applications menu:"
echo "  Acer Control Center"
echo ""
echo "Or run:"
echo "  acer-control-center"
echo ""
