# Moode Audio Touchscreen Display

A beautiful, touch-friendly display interface for [Moode Audio](https://moodeaudio.org/) on Raspberry Pi with integrated radio station browser.

![Version](https://img.shields.io/badge/version-3.3-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.7+-blue)

## ✨ Features

### 📻 Radio Station Browser
- Browse 200+ internet radio stations in a touch-friendly grid
- 3×2 grid layout (6 stations per page)
- Previous/Next pagination
- Touch any station to play instantly
- Stations automatically loaded from Moode's database

### 🎵 Music Playback Display
- **Spotify Integration** - Beautiful album art display with blurred backgrounds
- **MPD/Radio Support** - Display local music and internet radio streams
- **Smart Source Detection** - Automatically switches between Spotify, MPD, and radio
- **Real-time Updates** - Track info updates automatically

### 🎛️ Touch Controls
- **Playback Controls** - Previous, Play/Pause, Next buttons
- **Volume Control** - Volume up/down and mute (auto-hides during Spotify)
- **Radio Browser** - Dedicated button to access station library
- **Responsive UI** - Optimized for 5" touchscreen

### 🎨 Visual Design
- Album art with Gaussian blur background (Spotify)
- Progress bars with elapsed/total time
- Clean, modern dark theme
- Large touch-friendly buttons
- Professional layout optimized for 800×480 displays

## 📸 Screenshots

### Main Display
*[Add screenshot of main display with Spotify playing]*

### Radio Browser
*[Add screenshot of radio browser showing station grid]*

### Radio Playing
*[Add screenshot showing internet radio station playing]*

## 🔧 Hardware Requirements

### Required
- **Raspberry Pi 4B** (2GB+ RAM recommended)
- **5" DSI Touchscreen** - 800×480 resolution (e.g., Waveshare 5" DSI LCD)
- **Moode Audio** installed and configured
- **MicroSD Card** - 16GB+ for Moode Audio

### Optional
- **DAC/Amplifier** - IQaudio DigiAMP+, HiFiBerry, or similar
- **Speakers** - Powered speakers or passive speakers if using amp HAT
- **Case** - 3D printable case files included in `hardware/` folder

### Tested Configuration
- Raspberry Pi 4B (4GB)
- Waveshare 5" DSI LCD (800×480)
- IQaudio DigiAMP+
- Moode Audio 9.x

## 💾 Software Requirements

- **Moode Audio** 9.x or later
- **Python** 3.7+
- **Python Libraries:**
  - tkinter (usually pre-installed)
  - Pillow (PIL Fork)
  - sqlite3 (usually pre-installed)
- **System:**
  - X11 (for GUI)
  - MPD (included with Moode)

## 🚀 Quick Start

### 1. Install Moode Audio

Follow the [official Moode installation guide](https://moodeaudio.org/):
1. Download Moode Audio image
2. Flash to microSD card
3. Boot Raspberry Pi
4. Complete web-based setup

### 2. Install Dependencies

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install required packages
sudo apt-get install -y python3-pil python3-pil.imagetk xinit openbox

# Install fonts (optional, for better text rendering)
sudo apt-get install -y fonts-dejavu fonts-liberation
```

### 3. Install Display Script

```bash
# Create directory
mkdir -p /home/moodepi/moode-display
cd /home/moodepi/moode-display

# Download the script
# (Replace with your actual download method)
wget https://raw.githubusercontent.com/YOUR_USERNAME/moode-display/main/moode_display.py

# Make executable
chmod +x moode_display.py

# Test run (optional)
python3 moode_display.py
# Press Escape to exit
```

### 4. Configure Auto-Start

Add to `.bashrc` for automatic startup:

```bash
# Edit .bashrc
nano ~/.bashrc

# Add at the end:
if [ -z "$DISPLAY" ] && [ -z "$SSH_CLIENT" ] && [ -z "$SSH_TTY" ]; then
    if [ "$(tty)" = "/dev/tty1" ]; then
        cd /home/moodepi/moode-display
        startx
    fi
fi
```

Create `.xinitrc`:

```bash
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

### 5. Reboot and Enjoy!

```bash
sudo reboot
```

The display should start automatically and show your Moode Audio interface!

## 📖 Usage Guide

### Main Display
- Shows currently playing track/station
- Album art background for Spotify tracks
- Progress bar with elapsed/total time
- Playback controls (Previous/Play/Pause/Next)
- Volume controls (only for MPD/Radio, hidden during Spotify)

### Radio Browser
1. **Tap 📻 button** (bottom left) to open radio browser
2. **Browse stations** - 6 stations per page
3. **Navigate pages** - Use Previous/Next buttons
4. **Play station** - Tap any station button
5. **Close** - Tap ✕ Close button (or browser auto-closes after selection)

### Controls
- **⏮ Previous** - Previous track (MPD only)
- **▶/⏸ Play/Pause** - Toggle playback (MPD only)
- **⏭ Next** - Next track (MPD only)
- **📻 Radio** - Open radio station browser
- **− Volume Down** - Decrease volume by 5%
- **+ Volume Up** - Increase volume by 5%
- **🔊 Mute** - Toggle mute

**Note:** Playback controls don't work for Spotify (use Spotify app). Volume controls auto-hide during Spotify playback.

## ⚙️ Configuration

### Screen Resolution

Default: 800×480. To change, edit constants in `moode_display.py`:

```python
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
```

### Stations Per Page

Default: 6 (3×2 grid). To change:

```python
STATIONS_PER_PAGE = 6  # Options: 4, 6, 9, 12
```

### Colors

Customize the color scheme:

```python
BG_COLOR = "#000000"        # Background
TEXT_COLOR = "#FFFFFF"      # Text
ACCENT_COLOR = "#00FF00"    # Playing indicator
BUTTON_BG = "#222222"       # Buttons
BUTTON_ACTIVE = "#444444"   # Button pressed
```

### Update Interval

Change how often the display updates (milliseconds):

```python
UPDATE_INTERVAL = 500  # 500ms = 2 updates per second
```

## 🐛 Troubleshooting

See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for detailed solutions.

### Common Issues

**Display doesn't start on boot:**
- Check `.bashrc` and `.xinitrc` configuration
- Verify X11 is installed: `dpkg -l | grep xinit`
- Check logs: `tail -f /home/moodepi/display_debug.log`

**Stations don't play:**
- Verify Moode is working: test playback in web UI
- Check database: `ls /var/local/www/db/moode-sqlite3.db`
- Test MPD: `mpc ls RADIO`

**Display shows but controls don't work:**
- Check MPD is running: `systemctl status mpd`
- Test commands: `mpc status`
- Check permissions

**Touch not working:**
- Calibrate touchscreen in Moode web UI
- Test touch: `evtest` (install with `apt-get install evtest`)

## 🏗️ Hardware Build

See [hardware/HARDWARE_GUIDE.md](hardware/HARDWARE_GUIDE.md) for:
- Complete parts list with links
- Wiring diagrams
- 3D printable case files
- Assembly instructions
- Speaker selection guide

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/moode-display.git
cd moode-display

# Make changes
nano moode_display.py

# Test
python3 moode_display.py

# Check syntax
python3 -m py_compile moode_display.py
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[Moode Audio](https://moodeaudio.org/)** - Excellent audiophile music player for Raspberry Pi
- **Moode Community** - Inspiration and support
- **Radio Station Providers** - Thanks to all internet radio stations included in Moode's database
- UI development assisted by Claude (Anthropic)

## ⚠️ Disclaimer

This software is provided "as is" without warranty of any kind. Use at your own risk.

This project interfaces with Moode Audio but is not affiliated with or endorsed by the Moode Audio project. Moode Audio is a trademark of Moode Audio.

## 📧 Support

- **Issues:** [GitHub Issues](https://github.com/YOUR_USERNAME/moode-display/issues)
- **Discussions:** [GitHub Discussions](https://github.com/YOUR_USERNAME/moode-display/discussions)
- **Moode Forum:** [Moode Audio Forum](https://moodeaudio.org/forum/)

## 🗺️ Roadmap

Planned features:
- [ ] Favorites system (star favorite stations)
- [ ] Search bar for station filtering
- [ ] Genre/country filters
- [ ] Now playing indicator in browser
- [ ] Screensaver mode
- [ ] Multiple language support
- [ ] Customizable themes

## 📊 Stats

- **Lines of Code:** ~950
- **Stations Supported:** 200+
- **Python Version:** 3.7+
- **Display Resolution:** 800×480 (configurable)

---

**Made with ❤️ for the Moode Audio community**
