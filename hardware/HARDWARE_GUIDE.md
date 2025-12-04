# Hardware Build Guide

Complete guide for building your Moode Audio touchscreen display.

## Parts List

### Required Components

| Component | Specification | Approx. Cost | Notes |
|-----------|--------------|--------------|-------|
| Raspberry Pi 4B | 2GB or 4GB RAM | $45-55 | 4GB recommended |
| 5" DSI Touchscreen | 800×480 resolution | $30-50 | Waveshare or similar |
| MicroSD Card | 16GB+ Class 10 | $8-15 | For Moode Audio |
| Power Supply | 5V 3A USB-C | $8-12 | Official recommended |
| **Total** | | **~$100** | |

### Optional Components (for Standalone Unit)

| Component | Specification | Approx. Cost | Notes |
|-----------|--------------|--------------|-------|
| DAC/Amp HAT | IQaudio DigiAMP+ | $40-50 | Or similar |
| Speakers | 3" full range | $15-25 pair | Dayton CE81PF-8 or similar |
| Case | 3D printed | $5-10 | Filament cost, STL provided |
| DC Jack | Panel mount | $3-6 | For power input |
| Speaker Wire | 18-20 AWG | $5-8 | Short lengths needed |
| Screws/Hardware | M2.5, M3 | $8-12 | Assorted kit |
| **Total** | | **~$180** | Complete unit |

## Recommended Products

### Raspberry Pi 4B
- **Official Raspberry Pi 4B 4GB** - Best compatibility
- Source: Official retailers, Amazon, Newark

### Touchscreen
- **Waveshare 5" DSI LCD** (800×480) - Tested, works great
  - DSI connection (better than HDMI)
  - Capacitive touch
  - Good viewing angles
  
- **Alternative:** Official Raspberry Pi 7" Touch Display
  - Larger but still works
  - Adjust screen resolution in config

### DAC/Amplifier HAT
- **IQaudio DigiAMP+** (Tested) - 2×35W, excellent sound
- **HiFiBerry Amp2** - Similar performance
- **Justboom Amp HAT** - Budget option

### Speakers
- **Dayton Audio CE81PF-8** - 3" full range, 8Ω, great for desk
- **Tang Band W3-2141** - Higher end option
- **Peerless Tymphany** - Various models

## Wiring Diagrams

### Basic Setup (Display Only)

```
Raspberry Pi 4B
├── DSI Port → 5" DSI Touchscreen
├── USB-C → Power Supply (5V 3A)
└── Ethernet/WiFi → Network
```

### Complete Setup (With Audio)

```
Raspberry Pi 4B
├── DSI Port → 5" DSI Touchscreen
├── GPIO Header → DAC/Amp HAT
│   └── Speaker Terminals → Speakers (Left + Right)
├── USB-C → Power Supply (5V 3A)
└── Ethernet/WiFi → Network
```

*Detailed wiring diagram: Coming soon*

## Assembly Instructions

### Step 1: Prepare Raspberry Pi

1. Flash Moode Audio to microSD card
2. Insert card into Pi
3. Attach DSI touchscreen ribbon cable
4. Mount touchscreen to Pi (if using standoffs)

### Step 2: Install DAC/Amp HAT (Optional)

1. Carefully align HAT with GPIO pins
2. Press firmly to seat all pins
3. Secure with screws if provided
4. Do NOT force - pins should slide in easily

### Step 3: Connect Speakers (Optional)

1. Strip speaker wire ends (~5mm)
2. Connect to amp terminals:
   - Red → + (positive)
   - Black → − (negative)
3. Left speaker → Left channel
4. Right speaker → Right channel
5. Tighten terminal screws firmly

### Step 4: Power Up

1. Connect power supply to Pi USB-C
2. Pi boots, display should light up
3. Complete Moode setup via web UI
4. Install display software (see INSTALLATION.md)

## Case Options

### Option 1: 3D Printed Case

STL files provided in this repository:
- `hardware/case-stl/case-main.stl` - Main case body
- `hardware/case-stl/case-back.stl` - Back panel
- Coming soon!

**Print Settings:**
- Material: PETG or ABS (heat resistant)
- Layer Height: 0.2mm
- Infill: 20%
- Supports: Yes (for overhangs)
- Print Time: ~30-40 hours total

### Option 2: Commercial Case

- SmartiPi Touch 2 - Fits Pi + 7" display
- Modify for 5" display
- Various on Amazon/eBay

### Option 3: DIY Wood Case

- Plans coming soon
- Great for custom designs
- Can match room decor

## Cable Management

Tips for clean installation:
- Use ribbon cables where possible
- Route cables behind display
- Use zip ties or velcro straps
- Keep power and audio cables separated

## Cooling

Raspberry Pi 4B can run warm:
- Passive: Heatsinks on CPU/RAM (included with many kits)
- Active: Small 30mm fan (recommended for enclosed cases)
- Keep ventilation holes clear

## Power Considerations

**Minimum:** 5V 2.5A (Pi only)
**Recommended:** 5V 3A (Pi + display)
**With Amp:** 5V 3A + separate amp power OR powered speakers

**Using IQaudio DigiAMP+:**
- Requires 12-24V separate power for speakers
- Pi still powered via USB-C
- DC jack panel mount for clean look

## Testing

Before final assembly:

1. **Test display** - Verify touch works
2. **Test audio** - Play music, check both channels
3. **Test all features** - Run through full feature set
4. **Check temperatures** - Ensure adequate cooling

## Troubleshooting Hardware

### Display Issues
- Check DSI cable seated properly
- Try different HDMI cable (if using HDMI display)
- Verify display power

### Audio Issues
- Check speaker polarity (+ to +, − to −)
- Verify amp HAT seated correctly
- Test with headphones first
- Check Moode audio output settings

### Touch Not Working
- Check touch controller detected: `ls /dev/input/`
- Calibrate via Moode settings
- Try different USB port (if USB touch)

## Resources

- [Raspberry Pi GPIO Pinout](https://pinout.xyz/)
- [Moode Audio Hardware List](https://moodeaudio.org/)
- [Waveshare Wiki](https://www.waveshare.com/wiki/)

## Contributing

Have a different hardware setup that works well? Share it!
- Take photos
- Document your build
- Submit PR with your configuration

---

**Coming Soon:**
- Detailed wiring diagrams
- 3D printable case STL files
- Build video/photos
- Custom speaker enclosure designs
