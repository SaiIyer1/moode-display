# Configuration Guide

Customize your Moode Audio Touchscreen Display.

## Basic Configuration

All configuration is done by editing `moode_display.py`. The main constants are at the top of the file.

### Screen Resolution

Change display resolution:

```python
# Constants (near top of file)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
```

**Common resolutions:**
- 800×480 (5" displays, default)
- 1024×600 (7" displays)
- 1280×800 (10" displays)

After changing, test before committing:
```bash
python3 moode_display.py
```

### Color Scheme

Customize colors:

```python
BG_COLOR = "#000000"        # Background (black)
TEXT_COLOR = "#FFFFFF"      # Text (white)
ACCENT_COLOR = "#00FF00"    # Playing indicator (green)
BUTTON_BG = "#222222"       # Button background (dark gray)
BUTTON_ACTIVE = "#444444"   # Button when pressed (gray)
```

**Color format:** Hex colors (#RRGGBB)

**Popular themes:**

**Dark Blue:**
```python
BG_COLOR = "#001122"
TEXT_COLOR = "#FFFFFF"
ACCENT_COLOR = "#00AAFF"
BUTTON_BG = "#003366"
BUTTON_ACTIVE = "#004488"
```

**Light Theme:**
```python
BG_COLOR = "#FFFFFF"
TEXT_COLOR = "#000000"
ACCENT_COLOR = "#0066CC"
BUTTON_BG = "#EEEEEE"
BUTTON_ACTIVE = "#CCCCCC"
```

### Update Interval

How often the display refreshes:

```python
UPDATE_INTERVAL = 500  # milliseconds
```

- Lower = more responsive, higher CPU usage
- Higher = less responsive, lower CPU usage
- **Recommended:** 500-1000ms

### Stations Per Page

Number of stations in radio browser:

```python
STATIONS_PER_PAGE = 6  # 3×2 grid
```

**Options:**
- `4` = 2×2 grid (large buttons, easy touch)
- `6` = 3×2 grid (balanced, default)
- `9` = 3×3 grid (more stations, smaller buttons)
- `12` = 4×3 grid (many stations, small buttons)

## Advanced Configuration

### Font Sizes

Adjust text sizes:

```python
# In create_widgets() method:

# Title font
font=("Arial", 22, "bold")  # Change 22 to larger/smaller

# Artist font
font=("Arial", 16)  # Change 16

# Album font
font=("Arial", 14)  # Change 14

# Button fonts
font=("Arial", 28)  # Playback buttons
font=("Arial", 24, "bold")  # Volume buttons
```

### Button Positions

Customize layout by changing coordinates in `create_widgets()`:

```python
# Radio button position
self.btn_radio.place(x=60, y=SCREEN_HEIGHT - 60, anchor="center")

# Adjust x and y values to move button
# x: horizontal position (0 = left, SCREEN_WIDTH = right)
# y: vertical position (0 = top, SCREEN_HEIGHT = bottom)
```

### Album Art Processing

Customize album art blur and darkening:

```python
# In load_album_art() method:

# Blur radius (higher = more blur)
blurred = img.filter(ImageFilter.GaussianBlur(radius=30))

# Darkness (lower = darker, 0.0-1.0)
enhancer = ImageEnhance.Brightness(blurred)
darkened = enhancer.enhance(0.4)  # 40% brightness
```

### Progress Bar Style

Change progress bar appearance:

```python
# In update_display() method:

# Progress bar height
progress_height = 6  # pixels

# Progress bar color (playing)
fill="#00FF00"  # Green

# Progress bar color (elapsed)
fill="#444444"  # Dark gray
```

## Radio Browser Configuration

### Grid Layout

Adjust grid spacing and button sizes:

```python
# In RadioBrowser.show() method:

# Button spacing
padx=8  # Horizontal padding
pady=8  # Vertical padding

# Button size
wraplength=200  # Text wrap width
```

### Station Name Formatting

Adjust station name truncation:

```python
# In format_station_name() method:

# Maximum name length
if len(name) > 28:
    return name[:25] + "..."

# Change 28 and 25 to allow longer/shorter names
```

### Page Navigation Buttons

Customize Previous/Next/Close buttons:

```python
# Button size
width=11  # Characters wide
height=2  # Lines tall

# Button colors
bg=BUTTON_BG  # Background
fg=TEXT_COLOR  # Text color
```

## Volume Control

### Volume Step Size

How much volume changes per button press:

```python
# In volume_up() and volume_down() methods:

def volume_up(self):
    new_vol = min(100, self.current_volume + 5)  # +5%

def volume_down(self):
    new_vol = max(0, self.current_volume - 5)  # -5%
```

Change `5` to increase/decrease step size.

### Hide Volume During Spotify

Already implemented, but you can modify the behavior:

```python
# In update_display() method:

if self.current_source == "spotify":
    # Hide volume controls
    # Modify this section to always show, if desired
```

## Database Configuration

### Custom Station Filtering

Filter which stations appear in browser:

```python
# In RadioBrowser.load_stations() method:

cursor.execute("""
    SELECT id, name, station, genre, country
    FROM cfg_radio
    WHERE type = 'r'
    AND genre LIKE '%Jazz%'  -- Only Jazz stations
    ORDER BY name
""")
```

**Filter examples:**

**By country:**
```sql
AND country = 'United Kingdom'
```

**By genre:**
```sql
AND genre LIKE '%Classical%'
```

**Exclude certain stations:**
```sql
AND name NOT LIKE '%Test%'
```

### Custom Station Ordering

Change sort order:

```python
# By name (default):
ORDER BY name

# By country then name:
ORDER BY country, name

# By genre:
ORDER BY genre, name
```

## Logging Configuration

### Debug Logging

Enable/disable verbose logging:

```python
# Current: Logs to file
LOG_FILE = "/home/moodepi/display_debug.log"

# Disable logging:
def log_debug(message):
    pass  # Do nothing

# Log to console instead:
def log_debug(message):
    print(f"[{time.strftime('%H:%M:%S')}] {message}")
```

### Log File Location

Change where logs are saved:

```python
LOG_FILE = "/home/moodepi/display_debug.log"

# Change to:
LOG_FILE = "/tmp/display.log"  # Temporary, cleared on reboot
# or
LOG_FILE = "/var/log/moode_display.log"  # System logs
```

## Display Behavior

### Screensaver/Blanking

Currently disabled. To enable screen blanking:

```bash
# Edit .xinitrc
nano ~/.xinitrc

# Remove or comment these lines:
# xset -dpms
# xset s off
# xset s noblank

# Or adjust timeout:
xset s 300  # Blank after 5 minutes
```

### Cursor Visibility

Hide/show mouse cursor:

```python
# In __init__ method:
self.root.configure(bg=BG_COLOR, cursor="none")

# Change to:
cursor=""  # Show default cursor
cursor="arrow"  # Show arrow cursor
```

## Performance Tuning

### Reduce CPU Usage

```python
# Increase update interval
UPDATE_INTERVAL = 1000  # 1 second instead of 500ms

# Reduce image quality
# In load_album_art():
img = img.resize((SCREEN_WIDTH, SCREEN_HEIGHT), Image.BILINEAR)
# Change to NEAREST for faster, lower quality
```

### Reduce Memory Usage

```python
# Limit album art size
MAX_ART_SIZE = (400, 400)  # Before: (800, 800)

# Clear old album art
self.album_art_image = None  # Free memory
```

## Startup Options

### Auto-Start Configuration

Modify startup behavior in `.xinitrc`:

```bash
# Wait time before starting display
sleep 2  # Change to more/less

# Run in background (allows other apps)
python3 /home/moodepi/moode-display/moode_display.py &

# Run with error logging
python3 /home/moodepi/moode-display/moode_display.py 2>&1 | tee ~/display_errors.log
```

## Testing Configuration

After making changes:

### Test Syntax

```bash
python3 -m py_compile moode_display.py
```

No output = syntax OK.

### Test Run

```bash
python3 moode_display.py
```

Press Escape to exit.

### Check Logs

```bash
tail -f /home/moodepi/display_debug.log
```

## Configuration Templates

### Minimal (Fast, Low Resource)

```python
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
UPDATE_INTERVAL = 1000  # 1 second
STATIONS_PER_PAGE = 4  # Small grid
# Reduce image processing
```

### Maximum (Full Features, Higher Resource)

```python
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
UPDATE_INTERVAL = 250  # 4 updates/sec
STATIONS_PER_PAGE = 12  # Large grid
# Full image processing
```

### Touch-Optimized (Large Buttons)

```python
STATIONS_PER_PAGE = 4  # 2×2 grid
# Larger fonts:
font=("Arial", 32, "bold")  # Buttons
font=("Arial", 28)  # Text
```

## Backup Configuration

Before making changes:

```bash
# Backup current version
cp moode_display.py moode_display.py.backup

# Test changes
python3 moode_display.py

# If issues, restore:
cp moode_display.py.backup moode_display.py
```

---

**Pro tip:** Make one change at a time and test after each change!
