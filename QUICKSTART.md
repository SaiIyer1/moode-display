# Quick Start Guide

Get your Moode Audio Touchscreen Display running in 15 minutes!

## Prerequisites Check

Before starting, verify you have:
- ✅ Raspberry Pi 4B running Moode Audio
- ✅ 5" DSI touchscreen connected and working
- ✅ SSH or direct console access
- ✅ Internet connection

## 5-Minute Install

### 1. SSH into your Pi

```bash
ssh moodepi@moode.local
# Default password: moodeaudio
```

### 2. Install Dependencies

```bash
sudo apt-get update
sudo apt-get install -y xinit openbox python3-pil python3-pil.imagetk git
```

### 3. Download Display

```bash
cd /home/moodepi
git clone https://github.com/YOUR_USERNAME/moode-display.git moode-display
cd moode-display
chmod +x moode_display.py
```

### 4. Test Run

```bash
# If you have physical access, test from console
python3 moode_display.py
# Press Escape to exit

# If via SSH:
export DISPLAY=:0
python3 moode_display.py
```

### 5. Configure Auto-Start

```bash
# Add to .bashrc
echo '
# Auto-start display on console
if [ -z "$DISPLAY" ] && [ -z "$SSH_CLIENT" ] && [ -z "$SSH_TTY" ]; then
    if [ "$(tty)" = "/dev/tty1" ]; then
        cd /home/moodepi/moode-display
        startx
    fi
fi' >> ~/.bashrc

# Create .xinitrc
cat > ~/.xinitrc << 'EOF'
#!/bin/bash
xset -dpms
xset s off
xset s noblank
openbox &
sleep 2
python3 /home/moodepi/moode-display/moode_display.py
EOF

chmod +x ~/.xinitrc
```

### 6. Reboot

```bash
sudo reboot
```

**Done!** Display should start automatically after reboot.

## Quick Test

After reboot:

1. ✅ Display shows on screen
2. ✅ Touch "📻" button → Browser opens
3. ✅ Tap a station → Plays
4. ✅ Play Spotify from app → Shows on display
5. ✅ Volume +/− buttons work (for MPD/Radio)

## Troubleshooting

### Display doesn't start

```bash
# Check logs
tail -20 /home/moodepi/display_debug.log

# Try manual start
startx
```

### Touch doesn't work

```bash
# Test touch device
sudo apt-get install evtest
sudo evtest
# Select touch device, tap screen
```

### Stations don't play

```bash
# Test MPD
mpc status
mpc ls RADIO

# Check database
ls -l /var/local/www/db/moode-sqlite3.db
```

## Next Steps

- 📖 Read [INSTALLATION.md](docs/INSTALLATION.md) for detailed setup
- ⚙️ See [CONFIGURATION.md](docs/CONFIGURATION.md) for customization
- 🐛 Check [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) if issues
- 🏗️ Build hardware case: [HARDWARE_GUIDE.md](hardware/HARDWARE_GUIDE.md)

## Getting Help

- **Issues:** [GitHub Issues](https://github.com/YOUR_USERNAME/moode-display/issues)
- **Forum:** [Moode Audio Forum](https://moodeaudio.org/forum/)

## Customize

Quick customizations to try:

### Change Colors

Edit `moode_display.py`:
```python
BG_COLOR = "#000000"  # Background
TEXT_COLOR = "#FFFFFF"  # Text
```

### Stations Per Page

```python
STATIONS_PER_PAGE = 6  # Try 4, 9, or 12
```

### Update Speed

```python
UPDATE_INTERVAL = 500  # Milliseconds (500-1000 recommended)
```

## Common Commands

```bash
# Restart display
sudo reboot

# Stop display
sudo pkill python3

# View logs
tail -f /home/moodepi/display_debug.log

# Test station
mpc clear && mpc add "http://stream-url" && mpc play

# Update display
cd /home/moodepi/moode-display
git pull origin main
sudo reboot
```

---

**Enjoy your new display!** 🎵📻

For complete documentation, see [README.md](README.md)
