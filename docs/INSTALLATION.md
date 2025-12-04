# Installation Guide

Complete step-by-step installation instructions for Moode Audio Touchscreen Display.

## Prerequisites

Before starting, ensure you have:
- Raspberry Pi 4B (2GB+ RAM recommended)
- 5" DSI touchscreen (800×480)
- MicroSD card (16GB+)
- Power supply (5V 3A recommended)
- Keyboard for initial setup (optional, can use SSH)

## Step 1: Install Moode Audio

### 1.1 Download Moode Audio

Visit [moodeaudio.org](https://moodeaudio.org/) and download the latest image.

### 1.2 Flash to SD Card

**Using Raspberry Pi Imager (recommended):**
1. Download [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
2. Select "Use custom" and choose Moode Audio image
3. Select your SD card
4. Click "Write"

**Using Balena Etcher:**
1. Download [Balena Etcher](https://www.balena.io/etcher/)
2. Select Moode Audio image
3. Select SD card
4. Click "Flash"

### 1.3 Initial Moode Setup

1. Insert SD card and boot Raspberry Pi
2. Connect to network (Ethernet or WiFi)
3. Open browser and go to `http://moode.local`
4. Complete initial setup wizard
5. Configure audio output (I2S, USB, HDMI, etc.)

## Step 2: Configure Touchscreen

### 2.1 DSI Touchscreen Setup

If using DSI touchscreen (Waveshare 5", etc.):

```bash
# SSH into your Pi
ssh moodepi@moode.local
# Password: moodeaudio (default)

# Edit config.txt
sudo nano /boot/firmware/config.txt

# Add these lines if not present:
dtoverlay=vc4-kms-v3d
dtparam=spi=on
dtparam=i2c_arm=on

# For Waveshare 5" DSI LCD specifically:
dtoverlay=vc4-kms-dsi-7inch

# Save and exit (Ctrl+X, Y, Enter)
```

### 2.2 Reboot

```bash
sudo reboot
```

### 2.3 Test Touch

After reboot, touch should work. Test by:
```bash
# Install evtest
sudo apt-get install evtest

# Test touch input
sudo evtest
# Select your touch device and tap screen
```

## Step 3: Install Dependencies

### 3.1 Update System

```bash
ssh moodepi@moode.local

# Update package lists
sudo apt-get update

# Upgrade installed packages
sudo apt-get upgrade -y
```

### 3.2 Install Required Packages

```bash
# Install X11 and GUI components
sudo apt-get install -y xinit openbox

# Install Python imaging library
sudo apt-get install -y python3-pil python3-pil.imagetk

# Install fonts for better text rendering
sudo apt-get install -y fonts-dejavu fonts-liberation

# Install Git (if not present)
sudo apt-get install -y git
```

### 3.3 Verify Python

```bash
# Check Python version (should be 3.7+)
python3 --version

# Check tkinter is available
python3 -c "import tkinter; print('tkinter OK')"

# Check PIL is available
python3 -c "from PIL import Image; print('PIL OK')"
```

## Step 4: Install Display Script

### 4.1 Download Repository

**Option A: Using Git (recommended)**

```bash
# Clone repository
cd /home/moodepi
git clone https://github.com/YOUR_USERNAME/moode-display.git moode-display
cd moode-display
```

**Option B: Manual Download**

```bash
# Create directory
mkdir -p /home/moodepi/moode-display
cd /home/moodepi/moode-display

# Download main script
wget https://raw.githubusercontent.com/YOUR_USERNAME/moode-display/main/moode_display.py

# Make executable
chmod +x moode_display.py
```

### 4.2 Test Installation

```bash
# Run display manually
python3 moode_display.py

# You should see the display interface
# Press Escape key to exit
```

**If you see errors:**
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Verify all dependencies installed
- Check logs: `tail -f /home/moodepi/display_debug.log`

## Step 5: Configure Auto-Start

### 5.1 Edit .bashrc

```bash
# Edit bashrc
nano ~/.bashrc

# Scroll to the end and add:
# Auto-start X server on console login
if [ -z "$DISPLAY" ] && [ -z "$SSH_CLIENT" ] && [ -z "$SSH_TTY" ]; then
    if [ "$(tty)" = "/dev/tty1" ]; then
        cd /home/moodepi/moode-display
        startx
    fi
fi

# Save and exit (Ctrl+X, Y, Enter)
```

This starts the display when you log in to the console (not SSH).

### 5.2 Create .xinitrc

```bash
# Create .xinitrc file
cat > ~/.xinitrc << 'EOF'
#!/bin/bash

# Disable screen blanking and power management
xset -dpms
xset s off
xset s noblank

# Start window manager in background
openbox &

# Wait for window manager to start
sleep 2

# Run the display script
cd /home/moodepi/moode-display
python3 moode_display.py
EOF

# Make executable
chmod +x ~/.xinitrc
```

### 5.3 Configure Openbox (Optional)

For cleaner appearance without window decorations:

```bash
# Create openbox config directory
mkdir -p ~/.config/openbox

# Create config
cat > ~/.config/openbox/rc.xml << 'EOF'
<?xml version="1.0"?>
<openbox_config>
  <applications>
    <application class="*">
      <decor>no</decor>
      <maximized>yes</maximized>
    </application>
  </applications>
</openbox_config>
EOF
```

## Step 6: Final Configuration

### 6.1 Set Auto-Login (Optional but Recommended)

```bash
# Edit systemd config
sudo systemctl edit getty@tty1

# Add these lines:
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin moodepi --noclear %I $TERM

# Save and exit
```

### 6.2 Disable Cursor (Optional)

To hide mouse cursor:

```bash
# Install unclutter
sudo apt-get install -y unclutter

# Edit .xinitrc
nano ~/.xinitrc

# Add before the display script line:
unclutter -idle 0 &

# Save and exit
```

### 6.3 Test Auto-Start

```bash
# Reboot to test everything
sudo reboot
```

The display should start automatically after boot!

## Step 7: Verify Installation

After reboot, verify:

- [ ] Display shows automatically
- [ ] Touch works on all buttons
- [ ] 📻 Radio button opens browser
- [ ] Stations can be selected and play
- [ ] Spotify shows when playing from app
- [ ] Volume controls work
- [ ] Display updates when changing sources

## Post-Installation

### Customize Display

Edit `moode_display.py` to customize:
- Screen resolution
- Colors
- Stations per page
- Update interval

See [CONFIGURATION.md](CONFIGURATION.md) for details.

### Add Your Own Stations

Add stations through Moode web UI:
1. Go to Library → Radio
2. Click "Create station"
3. Fill in details
4. Station appears in display browser

### Update Display

```bash
cd /home/moodepi/moode-display
git pull origin main
sudo reboot
```

## Uninstall

To remove the display:

```bash
# Remove auto-start from .bashrc
nano ~/.bashrc
# Delete the auto-start section

# Remove files
rm -rf /home/moodepi/moode-display

# Reboot
sudo reboot
```

## Next Steps

- [Configuration Guide](CONFIGURATION.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [Hardware Build Guide](../hardware/HARDWARE_GUIDE.md)

---

**Need help?** Open an issue on GitHub or ask in the Moode forum!
