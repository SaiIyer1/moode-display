# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.3] - 2025-12-03

### Added
- Radio station browser with touch interface
- Grid view showing 6 stations per page (3×2 layout)
- Previous/Next pagination for browsing 200+ stations
- Radio button (📻) to access station library
- Direct streaming from database URLs
- Auto-hide volume controls during Spotify playback
- Comprehensive debug logging

### Changed
- Station playback now uses stream URLs from database instead of file paths
- Display names cleaned (removed .pls extension from UI)
- Improved source detection with MPD priority over stale Spotify data
- Enhanced error handling and logging

### Fixed
- Station playback from browser now works correctly
- Spotify to Radio switching with proper staleness detection
- Volume controls properly hide/show based on source
- MPD/Spotify/Radio source switching logic

## [2.6.1] - 2025-12-02

### Fixed
- Indentation error in update_loop function
- Python syntax issues preventing startup

## [2.0] - 2025-12-01

### Added
- Spotify integration with album art display
- Blurred album art backgrounds
- Progress bars with elapsed/total time
- Volume controls (up/down/mute buttons)
- MPD status detection
- Touch-friendly button layout
- Auto-start on boot configuration

### Changed
- Improved UI layout for 800×480 displays
- Better font sizes for readability
- Enhanced button spacing

## [1.0] - 2025-11-30

### Added
- Initial release
- Basic playback display
- Track information display
- Simple controls

---

## Version Numbering

- **Major (X.0.0)** - Breaking changes, major features
- **Minor (0.X.0)** - New features, backward compatible
- **Patch (0.0.X)** - Bug fixes, minor improvements

## Future Plans

See [GitHub Issues](https://github.com/YOUR_USERNAME/moode-display/issues) for planned features.

### Roadmap

**Version 3.4** (Planned)
- Favorites system
- Search functionality
- Genre filters
- Now playing indicator in browser

**Version 4.0** (Future)
- Multi-theme support
- Screensaver mode
- Gesture controls
- Settings menu
