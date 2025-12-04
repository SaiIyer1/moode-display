# Troubleshooting Guide

Common issues and solutions for Moode Audio Touchscreen Display.

## Table of Contents

- [Display Issues](#display-issues)
- [Radio Browser Issues](#radio-browser-issues)
- [Touch Issues](#touch-issues)
- [Audio Issues](#audio-issues)
- [Performance Issues](#performance-issues)
- [Debugging Tools](#debugging-tools)

---

## Display Issues

### Display Doesn't Start on Boot

**Symptoms:** Black screen or console after boot, no GUI appears.

**Solutions:**

1. **Check auto-start configuration:**
```bash
# Verify .bashrc has auto-start code
cat ~/.bashrc | grep startx
```

Should show the auto-start section. If missing, re-add it.

2. **Check .xinitrc exists:**
```bash
ls -la ~/.xinitrc
```

If missing, recreate it (see Installation Guide).

3. **Test manual start:**
```bash
# From console (not SSH)
startx
```

If this works, auto-start is misconfigured.

4. **Check X11 installed:**
```bash
dpkg -l | grep xinit
dpkg -l | grep openbox
```

If missing, install: `sudo apt-get install xinit openbox`

5. **Check logs:**
```bash
cat ~/.xsession-errors
tail -f /home/moodepi/display_debug.log
```

### Display Shows But Is Blank/Black

**Symptoms:** GUI window appears but is completely black.

**Solutions:**

1. **Check Python script is running:**
```bash
ps aux | grep moode_display
```

Should show python3 process. If not, script crashed.

2. **Run manually to see errors:**
```bash
cd /home/moodepi/moode-display
python3 moode_display.py
```

Look for error messages.

3. **Check dependencies:**
```bash
python3 -c "import tkinter; from PIL import Image, ImageTk; import sqlite3; print('All OK')"
```

### Display Shows "No Track Playing"

**Symptoms:** Display works but always shows "No Track Playing" even when music is playing.

**Solutions:**

1. **Check MPD is running:**
```bash
systemctl status mpd
mpc status
```

2. **Test Spotify metadata:**
```bash
cat /var/local/www/spotmeta.txt
```

Should show track info if Spotify playing.

3. **Check database access:**
```bash
ls -l /var/local/www/db/moode-sqlite3.db
```

Should be readable by moodepi user.

4. **Check logs for errors:**
```bash
tail -50 /home/moodepi/display_debug.log | grep error
```

### IndentationError on Startup

**Symptoms:** Script fails with "IndentationError" or "SyntaxError".

**Solutions:**

1. **Redownload script:**
```bash
cd /home/moodepi/moode-display
mv moode_display.py moode_display.py.backup
wget https://raw.githubusercontent.com/YOUR_USERNAME/moode-display/main/moode_display.py
```

2. **Check Python version:**
```bash
python3 --version
```

Must be 3.7 or higher.

---

## Radio Browser Issues

### Radio Browser Doesn't Open

**Symptoms:** Tapping 📻 button does nothing.

**Solutions:**

1. **Check logs when tapping:**
```bash
tail -f /home/moodepi/display_debug.log
```

Should show "Opening radio browser". If not, touch not working.

2. **Check database:**
```bash
ls -l /var/local/www/db/moode-sqlite3.db
sqlite3 /var/local/www/db/moode-sqlite3.db "SELECT COUNT(*) FROM cfg_radio WHERE type='r';"
```

Should return number of stations (200+).

3. **Test browser standalone:**
```bash
cd /home/moodepi/moode-display
python3 -c "from moode_display import RadioBrowser; print('OK')"
```

### Stations Don't Play When Selected

**Symptoms:** Tapping station in browser doesn't play, or plays briefly then stops.

**Solutions:**

1. **Check logs:**
```bash
tail -20 /home/moodepi/display_debug.log
```

Look for:
```
mpc add result: 0  ← Should be 0
mpc play result: 0 ← Should be 0
```

If return code is 1, there's an error.

2. **Test station manually:**
```bash
# Get station URL from database
sqlite3 /var/local/www/db/moode-sqlite3.db \
  "SELECT station FROM cfg_radio WHERE name LIKE 'BBC Radio 1%' LIMIT 1;"

# Test with mpc
mpc clear
mpc add "URL_FROM_ABOVE"
mpc play
```

3. **Check MPD logs:**
```bash
tail -50 /var/log/mpd/mpd.log
```

Look for connection or streaming errors.

4. **Verify internet connection:**
```bash
ping -c 4 8.8.8.8
```

### Station List Is Empty

**Symptoms:** Radio browser shows "Page 0 of 0" or no stations.

**Solutions:**

1. **Verify stations in database:**
```bash
sqlite3 /var/local/www/db/moode-sqlite3.db \
  "SELECT COUNT(*) FROM cfg_radio WHERE type='r';"
```

Should be 200+. If 0, reimport radio stations in Moode web UI.

2. **Check database path:**
```bash
ls -l /var/local/www/db/moode-sqlite3.db
```

Should exist and be readable.

---

## Touch Issues

### Touch Not Responding

**Symptoms:** Can't interact with display, buttons don't respond to touch.

**Solutions:**

1. **Check touchscreen detected:**
```bash
ls /dev/input/event*
```

Should show event devices.

2. **Test touch events:**
```bash
sudo apt-get install evtest
sudo evtest
```

Select touch device and tap screen. Should show events.

3. **Calibrate touchscreen:**
```bash
sudo apt-get install xinput-calibrator
DISPLAY=:0 xinput_calibrator
```

Follow on-screen instructions.

4. **Check touch permissions:**
```bash
groups moodepi
```

Should include "input" group. If not:
```bash
sudo usermod -a -G input moodepi
```

### Touch Is Inverted or Offset

**Symptoms:** Touch works but in wrong location.

**Solutions:**

1. **Calibrate via Moode web UI:**
   - Go to System → Display
   - Find touch calibration options

2. **Manual calibration:**
```bash
# Create calibration file
sudo nano /etc/X11/xorg.conf.d/99-calibration.conf

# Add transformation matrix
# (Values depend on your screen)
```

---

## Audio Issues

### No Sound

**Symptoms:** Stations play (display updates) but no audio output.

**Solutions:**

1. **Check Moode audio output:**
   - Go to Moode web UI
   - Audio → Configure
   - Verify correct output selected

2. **Check volume:**
```bash
mpc volume
# Set to higher if low
mpc volume 75
```

3. **Test audio outside display:**
   - Play music from Moode web UI
   - If that works, issue is display-related

### Volume Controls Don't Work

**Symptoms:** Volume +/− buttons don't change volume.

**Solutions:**

1. **Check MPD volume:**
```bash
mpc volume 50
# Wait a moment
mpc volume
```

Should show new volume.

2. **During Spotify:**
   - Volume buttons are hidden during Spotify (expected)
   - Use Spotify app volume control

3. **Check logs:**
```bash
tail -f /home/moodepi/display_debug.log | grep volume
```

---

## Performance Issues

### Display Is Laggy/Slow

**Symptoms:** UI updates slowly, touch response delayed.

**Solutions:**

1. **Check CPU usage:**
```bash
top
```

Press 'P' to sort by CPU. Display script should use <10%.

2. **Reduce update interval:**
Edit `moode_display.py`:
```python
UPDATE_INTERVAL = 1000  # Change from 500 to 1000ms
```

3. **Reduce stations per page:**
```python
STATIONS_PER_PAGE = 4  # Change from 6 to 4
```

4. **Check memory:**
```bash
free -h
```

Should have >500MB free.

### Album Art Loads Slowly

**Symptoms:** Spotify album art takes long to appear or appears blurry initially.

**Solutions:**

1. **Check internet speed:**
```bash
ping -c 10 i.scdn.co
```

Spotify's image servers.

2. **Reduce image processing:**
Edit image processing settings in script (advanced).

---

## Debugging Tools

### Check What's Playing

```bash
# MPD status
mpc status
mpc current

# Current file/URL
mpc current --format "%file%"

# Spotify metadata
cat /var/local/www/spotmeta.txt
```

### Monitor Debug Log

```bash
# Follow log in real-time
tail -f /home/moodepi/display_debug.log

# Search for errors
grep -i error /home/moodepi/display_debug.log

# Last 50 entries
tail -50 /home/moodepi/display_debug.log
```

### Check Process Status

```bash
# Check display running
ps aux | grep moode_display

# Check X server running
ps aux | grep Xorg

# Check MPD running
systemctl status mpd
```

### Test Components Individually

```bash
# Test database query
sqlite3 /var/local/www/db/moode-sqlite3.db \
  "SELECT name FROM cfg_radio WHERE type='r' LIMIT 5;"

# Test MPD command
mpc clear && mpc add "RADIO/BBC Radio 1.pls" && mpc play

# Test Python imports
python3 -c "import tkinter; from PIL import Image; import sqlite3"
```

### Network Diagnostics

```bash
# Check internet
ping -c 4 google.com

# Check DNS
nslookup moode.local

# Check Moode web server
curl -I http://localhost
```

---

## Getting Help

If none of these solutions work:

1. **Collect diagnostic info:**
```bash
# Create diagnostic report
cat > ~/diagnostic.txt << EOF
Python Version: $(python3 --version)
System: $(uname -a)
MPD Status: $(mpc status)
Display Log:
$(tail -50 /home/moodepi/display_debug.log)
EOF

cat ~/diagnostic.txt
```

2. **Open GitHub Issue:**
   - Go to Issues tab
   - Click "New Issue"
   - Include diagnostic info
   - Describe your problem

3. **Ask in Moode Forum:**
   - Visit [moodeaudio.org/forum](https://moodeaudio.org/forum/)
   - Search for similar issues
   - Post in appropriate section

---

## Advanced Debugging

### Enable Verbose Logging

Edit `moode_display.py` and add more debug statements:

```python
# Find the log_debug function and use liberally
log_debug(f"Variable name: {variable_value}")
```

### Run in Debug Mode

```bash
# Run with full error output
python3 -u moode_display.py 2>&1 | tee debug_output.txt
```

### Check System Resources

```bash
# Disk space
df -h

# Memory
free -h

# CPU temp
vcgencmd measure_temp

# Throttling status
vcgencmd get_throttled
```

---

**Still stuck?** Don't hesitate to ask for help on GitHub or the Moode forum!
