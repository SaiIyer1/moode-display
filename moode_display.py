#!/usr/bin/env python3
"""
Moode Audio Display UI - Version 3.0
New Features:
- Integrated Radio Station Browser
- Grid view with 6 stations per page
- Touch to play any station
- Previous/Next pagination
- Access via Radio button

Previous improvements (V2.6.1):
- Proper source detection (MPD vs Spotify)
- MPD priority when both sources active
- Volume controls (hide during Spotify)
- Accurate volume control with mute
- Stable Spotify playback (no file age checking)
"""

import tkinter as tk
from tkinter import Canvas
import subprocess
import time
import os
import re
import sqlite3
from PIL import Image, ImageTk, ImageFilter, ImageDraw, ImageFont, ImageEnhance
from io import BytesIO
from urllib import request
import threading

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
BG_COLOR = "#000000"
TEXT_COLOR = "#FFFFFF"
ACCENT_COLOR = "#00FF00"
UPDATE_INTERVAL = 500  # milliseconds

# Moode metadata file
SPOTMETA_FILE = "/var/local/www/spotmeta.txt"
LOG_FILE = "/home/moodepi/display_debug.log"

# Radio browser constants
DB_PATH = "/var/local/www/db/moode-sqlite3.db"
STATIONS_PER_PAGE = 6  # 3x2 grid
BUTTON_BG = "#222222"
BUTTON_ACTIVE = "#444444"

def log_debug(message):
    """Write debug messages to log file"""
    try:
        timestamp = time.strftime("%H:%M:%S")
        with open(LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
    except:
        pass

class RadioBrowser:
    """Radio station browser with grid view and pagination"""
    
    def __init__(self, parent, main_display, width=800, height=480):
        self.parent = parent
        self.main_display = main_display  # Reference to main display
        self.width = width
        self.height = height
        
        # State
        self.stations = []
        self.current_page = 0
        self.total_pages = 0
        
        # UI elements
        self.frame = None
        self.station_buttons = []
        
        # Load stations
        self.load_stations()
    
    def load_stations(self):
        """Load radio stations from Moode database"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Get all radio stations, ordered by name
            cursor.execute("""
                SELECT id, name, station, genre, country
                FROM cfg_radio
                WHERE type = 'r'
                ORDER BY name
            """)
            
            rows = cursor.fetchall()
            conn.close()
            
            # Store stations as tuples (id, name, url, genre, country)
            self.stations = []
            for row in rows:
                station_id = row[0]
                station_name = row[1]
                stream_url = row[2]  # This is the actual stream URL!
                genre = row[3]
                country = row[4]
                
                # Remove .pls from display name if present
                display_name = station_name.replace('.pls', '')
                
                # Store with actual stream URL from database
                self.stations.append((station_id, display_name, stream_url, genre, country))
            
            self.total_pages = (len(self.stations) + STATIONS_PER_PAGE - 1) // STATIONS_PER_PAGE
            log_debug(f"Loaded {len(self.stations)} stations, {self.total_pages} pages")
            
        except Exception as e:
            log_debug(f"Error loading stations: {e}")
            self.stations = []
            self.total_pages = 0
    
    def show(self):
        """Show the radio browser"""
        if self.frame:
            self.frame.destroy()
        
        # Create main frame (covers entire screen)
        self.frame = tk.Frame(self.parent, bg=BG_COLOR)
        self.frame.place(x=0, y=0, width=self.width, height=self.height)
        
        # Title
        title = tk.Label(self.frame, text="📻 Radio Stations",
                        font=("Arial", 24, "bold"),
                        fg=TEXT_COLOR, bg=BG_COLOR)
        title.pack(pady=15)
        
        # Grid frame for station buttons
        grid_frame = tk.Frame(self.frame, bg=BG_COLOR)
        grid_frame.pack(expand=True, fill=tk.BOTH, padx=30, pady=10)
        
        # Create station buttons (3 columns x 2 rows)
        self.station_buttons = []
        start_idx = self.current_page * STATIONS_PER_PAGE
        end_idx = min(start_idx + STATIONS_PER_PAGE, len(self.stations))
        
        for i in range(STATIONS_PER_PAGE):
            row = i // 3
            col = i % 3
            
            if start_idx + i < end_idx:
                station = self.stations[start_idx + i]
                station_id, station_name, url, genre, country = station
                
                # Format station name for display
                display_name = self.format_station_name(station_name)
                
                # Create button for station
                btn = tk.Button(grid_frame, 
                               text=display_name,
                               font=("Arial", 14, "bold"),
                               bg=BUTTON_BG, fg=TEXT_COLOR,
                               activebackground=BUTTON_ACTIVE,
                               relief=tk.RAISED, bd=3,
                               wraplength=200,
                               command=lambda s=station: self.play_station(s))
                btn.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
                self.station_buttons.append(btn)
        
        # Configure grid weights for equal sizing
        for i in range(3):
            grid_frame.columnconfigure(i, weight=1, minsize=200)
        for i in range(2):
            grid_frame.rowconfigure(i, weight=1, minsize=140)
        
        # Bottom control panel
        control_frame = tk.Frame(self.frame, bg=BG_COLOR)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=15)
        
        # Previous button
        btn_prev = tk.Button(control_frame, text="◀ Previous",
                            font=("Arial", 18, "bold"),
                            bg=BUTTON_BG, fg=TEXT_COLOR,
                            activebackground=BUTTON_ACTIVE,
                            relief=tk.FLAT, bd=0,
                            width=11, height=2,
                            command=self.previous_page)
        btn_prev.pack(side=tk.LEFT, padx=10)
        
        if self.current_page == 0:
            btn_prev.config(state=tk.DISABLED, fg="#555555")
        
        # Page indicator
        page_text = f"Page {self.current_page + 1} of {self.total_pages}"
        tk.Label(control_frame, text=page_text,
                font=("Arial", 18, "bold"),
                fg=TEXT_COLOR, bg=BG_COLOR).pack(side=tk.LEFT, expand=True)
        
        # Next button
        btn_next = tk.Button(control_frame, text="Next ▶",
                            font=("Arial", 18, "bold"),
                            bg=BUTTON_BG, fg=TEXT_COLOR,
                            activebackground=BUTTON_ACTIVE,
                            relief=tk.FLAT, bd=0,
                            width=11, height=2,
                            command=self.next_page)
        btn_next.pack(side=tk.LEFT, padx=10)
        
        if self.current_page >= self.total_pages - 1:
            btn_next.config(state=tk.DISABLED, fg="#555555")
        
        # Close button
        btn_close = tk.Button(control_frame, text="✕ Close",
                             font=("Arial", 18, "bold"),
                             bg="#CC0000", fg=TEXT_COLOR,
                             activebackground="#990000",
                             relief=tk.FLAT, bd=0,
                             width=10, height=2,
                             command=self.hide)
        btn_close.pack(side=tk.RIGHT, padx=10)
    
    def format_station_name(self, name):
        """Format station name for display"""
        # Remove .pls extension if present
        if name.endswith('.pls'):
            name = name[:-4]
        
        # Shorten very long names
        if len(name) > 28:
            return name[:25] + "..."
        return name
    
    def play_station(self, station):
        """Play selected radio station"""
        station_id, station_name, url, genre, country = station
        log_debug(f"User selected station: {station_name}")
        log_debug(f"Station URL: {url}")
        
        try:
            # Check current playback state first
            status_result = subprocess.run(['mpc', 'status'], 
                                         capture_output=True, text=True, check=False)
            was_playing = '[playing]' in status_result.stdout
            
            # Clear queue and add station
            clear_result = subprocess.run(['mpc', 'clear'], 
                                        capture_output=True, text=True, check=False)
            log_debug(f"mpc clear result: {clear_result.returncode}")
            
            # Add the station - try with RADIO/ prefix
            add_result = subprocess.run(['mpc', 'add', url], 
                                      capture_output=True, text=True, check=False)
            log_debug(f"mpc add result: {add_result.returncode}, stderr: {add_result.stderr}")
            
            # If add failed, try without RADIO/ prefix
            if add_result.returncode != 0 or add_result.stderr:
                log_debug(f"Trying without RADIO/ prefix")
                # Remove RADIO/ prefix
                url_without_prefix = url.replace('RADIO/', '')
                add_result = subprocess.run(['mpc', 'add', url_without_prefix], 
                                          capture_output=True, text=True, check=False)
                log_debug(f"mpc add (no prefix) result: {add_result.returncode}, stderr: {add_result.stderr}")
            
            # Start playback
            play_result = subprocess.run(['mpc', 'play'], 
                                       capture_output=True, text=True, check=False)
            log_debug(f"mpc play result: {play_result.returncode}, stderr: {play_result.stderr}")
            
            # Verify what's playing
            current_result = subprocess.run(['mpc', 'current'], 
                                          capture_output=True, text=True, check=False)
            log_debug(f"Now playing: {current_result.stdout.strip()}")
            
            # Close browser after selection
            self.hide()
            
        except Exception as e:
            log_debug(f"Error playing station: {e}")
            import traceback
            log_debug(f"Traceback: {traceback.format_exc()}")
    
    def next_page(self):
        """Go to next page"""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.show()
    
    def previous_page(self):
        """Go to previous page"""
        if self.current_page > 0:
            self.current_page -= 1
            self.show()
    
    def hide(self):
        """Hide the radio browser"""
        if self.frame:
            self.frame.destroy()
            self.frame = None
            log_debug("Radio browser closed")

class MoodeDisplay:
    def __init__(self, root):
        self.root = root
        self.root.title("Moode Audio")
        self.root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.root.configure(bg=BG_COLOR, cursor="none")
        
        # Fullscreen
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        
        # State variables
        self.current_track = ""
        self.current_artist = ""
        self.current_album = ""
        self.current_duration = 0
        self.elapsed_time = 0
        self.is_playing = False
        self.current_volume = 0
        self.is_muted = False
        self.album_art_url = None
        self.album_art_image = None
        self.current_source = "unknown"  # "mpd" or "spotify"
        
        # Create UI
        self.create_widgets()
        
        # Initialize radio browser (after UI created)
        self.radio_browser = RadioBrowser(self.root, self, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Start update thread
        self.running = True
        self.update_thread = threading.Thread(target=self.update_loop, daemon=True)
        self.update_thread.start()
        
        log_debug("Display initialized")
    
    def create_widgets(self):
        """Create all UI elements"""
        
        # Album art background canvas
        self.canvas = Canvas(self.root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT,
                            bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Track info labels (no frame - place directly on canvas)
        # Title label
        self.title_label = tk.Label(self.root, text="No Track Playing",
                                    font=("Arial", 22, "bold"),
                                    fg=TEXT_COLOR, bg=BG_COLOR)
        self.title_label.place(x=SCREEN_WIDTH//2, y=60, anchor="center")
        
        # Artist label
        self.artist_label = tk.Label(self.root, text="",
                                     font=("Arial", 16),
                                     fg=TEXT_COLOR, bg=BG_COLOR)
        self.artist_label.place(x=SCREEN_WIDTH//2, y=95, anchor="center")
        
        # Album label
        self.album_label = tk.Label(self.root, text="",
                                   font=("Arial", 14),
                                   fg="#CCCCCC", bg=BG_COLOR)
        self.album_label.place(x=SCREEN_WIDTH//2, y=125, anchor="center")
        
        # Status indicator (playing/paused)
        self.status_canvas = Canvas(self.root, width=20, height=20,
                                   bg=BG_COLOR, highlightthickness=0)
        self.status_canvas.place(x=20, y=20)
        self.status_dot = self.status_canvas.create_oval(5, 5, 15, 15, fill="#666666")
        
        # Progress bar frame (bottom third)
        progress_y = SCREEN_HEIGHT - 150
        
        # Time labels
        self.elapsed_label = tk.Label(self.root, text="0:00",
                                     font=("Arial", 12),
                                     fg=TEXT_COLOR, bg=BG_COLOR)
        self.elapsed_label.place(x=50, y=progress_y - 5)
        
        self.duration_label = tk.Label(self.root, text="0:00",
                                      font=("Arial", 12),
                                      fg=TEXT_COLOR, bg=BG_COLOR)
        self.duration_label.place(x=SCREEN_WIDTH - 90, y=progress_y - 5)
        
        # Progress bar
        self.progress_canvas = Canvas(self.root, width=SCREEN_WIDTH - 160,
                                     height=8, bg="#333333", highlightthickness=0)
        self.progress_canvas.place(x=80, y=progress_y + 10)
        self.progress_bar = self.progress_canvas.create_rectangle(
            0, 0, 0, 8, fill=ACCENT_COLOR, outline="")
        
        # Control buttons (center bottom)
        button_y = SCREEN_HEIGHT - 100
        button_size = 50
        button_spacing = 80
        center_x = SCREEN_WIDTH // 2
        
        # Previous button
        self.btn_prev = tk.Button(self.root, text="⏮", font=("Arial", 28),
                                 bg="#222222", fg=TEXT_COLOR,
                                 activebackground="#444444",
                                 relief=tk.FLAT, bd=0,
                                 width=2, height=1,
                                 command=self.prev_track)
        self.btn_prev.place(x=center_x - button_spacing - button_size//2,
                          y=button_y, anchor="center")
        
        # Play/Pause button
        self.btn_play = tk.Button(self.root, text="▶", font=("Arial", 28),
                                 bg="#222222", fg=TEXT_COLOR,
                                 activebackground="#444444",
                                 relief=tk.FLAT, bd=0,
                                 width=2, height=1,
                                 command=self.toggle_play)
        self.btn_play.place(x=center_x, y=button_y, anchor="center")
        
        # Next button
        self.btn_next = tk.Button(self.root, text="⏭", font=("Arial", 28),
                                 bg="#222222", fg=TEXT_COLOR,
                                 activebackground="#444444",
                                 relief=tk.FLAT, bd=0,
                                 width=2, height=1,
                                 command=self.next_track)
        self.btn_next.place(x=center_x + button_spacing + button_size//2,
                          y=button_y, anchor="center")
        
        # Radio button (bottom left) - Opens radio station browser
        self.btn_radio = tk.Button(self.root, text="📻",
                                   font=("Arial", 28),
                                   bg="#222222", fg=TEXT_COLOR,
                                   activebackground="#444444",
                                   relief=tk.FLAT, bd=0,
                                   width=3, height=2,
                                   command=self.show_radio_browser)
        self.btn_radio.place(x=60, y=SCREEN_HEIGHT - 60, anchor="center")
        
        # Volume controls (bottom right) - Better spacing
        vol_x = SCREEN_WIDTH - 180
        vol_y = SCREEN_HEIGHT - 50
        
        # Volume down button
        self.btn_vol_down = tk.Button(self.root, text="−", font=("Arial", 24, "bold"),
                                      bg="#222222", fg=TEXT_COLOR,
                                      activebackground="#444444",
                                      relief=tk.FLAT, bd=0,
                                      width=2, height=1,
                                      command=self.volume_down)
        self.btn_vol_down.place(x=vol_x - 60, y=vol_y, anchor="center")
        
        # Volume label (larger, more readable)
        self.volume_label = tk.Label(self.root, text="Vol: 0",
                                    font=("Arial", 16, "bold"),
                                    fg=TEXT_COLOR, bg=BG_COLOR,
                                    width=8)  # Fixed width for stability
        self.volume_label.place(x=vol_x + 10, y=vol_y, anchor="center")
        
        # Volume up button
        self.btn_vol_up = tk.Button(self.root, text="+", font=("Arial", 24, "bold"),
                                    bg="#222222", fg=TEXT_COLOR,
                                    activebackground="#444444",
                                    relief=tk.FLAT, bd=0,
                                    width=2, height=1,
                                    command=self.volume_up)
        self.btn_vol_up.place(x=vol_x + 80, y=vol_y, anchor="center")
        
        # Mute button (further right)
        self.btn_mute = tk.Button(self.root, text="🔊", font=("Arial", 20),
                                 bg="#222222", fg=TEXT_COLOR,
                                 activebackground="#444444",
                                 relief=tk.FLAT, bd=0,
                                 width=2, height=1,
                                 command=self.toggle_mute)
        self.btn_mute.place(x=vol_x + 140, y=vol_y, anchor="center")
    
    def get_mpd_status(self):
        """Get current MPD status and track info"""
        try:
            # Get playback state
            result = subprocess.run(['mpc', 'status'], capture_output=True, text=True)
            status_output = result.stdout
            
            # Check if anything is playing
            if '[playing]' in status_output:
                self.is_playing = True
                self.current_source = "mpd"
            elif '[paused]' in status_output:
                self.is_playing = False
                self.current_source = "mpd"
            else:
                # Nothing playing in MPD
                log_debug("MPD not playing or paused")
                return False
            
            # Get track info - first try formatted, then fall back to plain
            result = subprocess.run(['mpc', 'current', '-f', '%artist%|||%title%|||%album%|||%time%'],
                                  capture_output=True, text=True)
            
            track_data_found = False
            
            if result.stdout.strip():
                parts = result.stdout.strip().split('|||')
                log_debug(f"MPD formatted output: {len(parts)} parts")
                
                # Try to parse formatted output (local files)
                if len(parts) >= 2:  # At least artist and title
                    self.current_artist = parts[0] if parts[0] else ""
                    self.current_track = parts[1] if parts[1] else ""
                    self.current_album = parts[2] if len(parts) > 2 and parts[2] else ""
                    
                    # Parse duration if available
                    if len(parts) > 3 and parts[3] and ':' in parts[3]:
                        time_str = parts[3]
                        try:
                            m, s = time_str.split(':', 1)
                            self.current_duration = int(m) * 60 + int(s)
                        except:
                            self.current_duration = 0
                    else:
                        self.current_duration = 0
                    
                    track_data_found = True
            
            # If formatted output failed or returned nothing useful, try plain current
            if not track_data_found or (not self.current_artist and not self.current_track):
                log_debug("Trying plain mpc current for radio stream")
                result = subprocess.run(['mpc', 'current'], capture_output=True, text=True)
                
                if result.stdout.strip():
                    # For radio: entire line is usually the station name or current song
                    stream_info = result.stdout.strip()
                    log_debug(f"MPD plain output: {stream_info}")
                    
                    # Check if it looks like "Artist - Title" format
                    if ' - ' in stream_info:
                        parts = stream_info.split(' - ', 1)
                        self.current_artist = parts[0].strip()
                        self.current_track = parts[1].strip()
                    else:
                        # Just use the whole thing as the title (station name)
                        self.current_artist = ""
                        self.current_track = stream_info
                    
                    self.current_album = ""
                    self.current_duration = 0
                    track_data_found = True
                    log_debug(f"Radio: artist='{self.current_artist}', track='{self.current_track}'")
            
            if not track_data_found:
                log_debug("MPD: No track data found")
                return False
            
            # Get elapsed time from status (if available - won't be for streams)
            time_match = re.search(r'(\d+):(\d+)/(\d+):(\d+)', status_output)
            if time_match:
                elapsed_min = int(time_match.group(1))
                elapsed_sec = int(time_match.group(2))
                self.elapsed_time = elapsed_min * 60 + elapsed_sec
                log_debug(f"MPD: elapsed {elapsed_min}:{elapsed_sec}")
            else:
                self.elapsed_time = 0
            
            log_debug(f"MPD active: {self.current_track}")
            return True
            
        except Exception as e:
            log_debug(f"MPD status error: {e}")
            return False
    
    def get_spotify_status(self):
        """Get current Spotify Connect status from spotmeta.txt"""
        try:
            if not os.path.exists(SPOTMETA_FILE):
                return False
            
            with open(SPOTMETA_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            # Check if content is empty, null, or whitespace
            if not content or content == "null" or content == "" or len(content) < 10:
                log_debug("Spotify metadata empty or null")
                return False
            
            # Parse Spotify metadata
            # Format: Title~~~Artist~~~Album~~~Duration(ms)~~~ImageURLs~~~Format
            parts = content.split('~~~')
            
            if len(parts) < 4:
                log_debug(f"Spotify metadata incomplete ({len(parts)} parts)")
                return False
            
            # Verify we have actual data (not empty fields)
            if not parts[0] or not parts[1]:  # No title or artist
                log_debug("Spotify metadata missing title or artist")
                return False
            
            # NOTE: We do NOT check file age anymore!
            # Moode only updates spotmeta.txt when track changes, not continuously.
            # As long as the file has valid Spotify data, we assume Spotify is active.
            # When Spotify disconnects, Moode will write "null" to the file.
            
            self.current_track = parts[0] if parts[0] else "Unknown Track"
            
            # Artists (may be newline-separated)
            artists = parts[1].split('\n') if parts[1] else []
            self.current_artist = artists[0] if artists else "Unknown Artist"
            
            self.current_album = parts[2] if parts[2] else ""
            
            # Duration (in milliseconds)
            try:
                self.current_duration = int(parts[3]) // 1000 if parts[3] else 0
            except:
                self.current_duration = 0
            
            # Image URLs (newline-separated, first is largest)
            if len(parts) > 4 and parts[4]:
                image_urls = parts[4].split('\n')
                self.album_art_url = image_urls[0] if image_urls else None
            else:
                self.album_art_url = None
            
            # Spotify is playing if we have valid metadata
            self.is_playing = True
            self.current_source = "spotify"
            
            log_debug(f"Spotify active: {self.current_track}")
            
            # Note: Spotify doesn't provide elapsed time in spotmeta.txt
            # Progress bar won't move for Spotify tracks
            
            return True
            
        except Exception as e:
            log_debug(f"Spotify status error: {e}")
            return False
    
    def get_volume(self):
        """Get current volume from mpc"""
        try:
            result = subprocess.run(['mpc', 'volume'], capture_output=True, text=True)
            # Output format: "volume: 75%"
            match = re.search(r'volume:\s*(\d+)%', result.stdout)
            if match:
                volume = int(match.group(1))
                
                # Check if muted (volume = 0 but was previously > 0)
                if volume == 0 and self.current_volume > 0:
                    self.is_muted = True
                elif volume > 0:
                    self.is_muted = False
                    self.current_volume = volume
                
                return volume
            return self.current_volume
        except Exception as e:
            log_debug(f"Volume get error: {e}")
            return self.current_volume
    
    def set_volume(self, volume):
        """Set volume via mpc"""
        try:
            volume = max(0, min(100, volume))  # Clamp to 0-100
            subprocess.run(['mpc', 'volume', str(volume)], capture_output=True)
            self.current_volume = volume
            if volume > 0:
                self.is_muted = False
        except Exception as e:
            log_debug(f"Volume set error: {e}")
    
    def volume_up(self):
        """Increase volume by 5%"""
        if self.is_muted:
            self.toggle_mute()  # Unmute first
        else:
            new_vol = min(100, self.current_volume + 5)
            self.set_volume(new_vol)
    
    def volume_down(self):
        """Decrease volume by 5%"""
        if self.is_muted:
            self.toggle_mute()  # Unmute first
        else:
            new_vol = max(0, self.current_volume - 5)
            self.set_volume(new_vol)
    
    def toggle_mute(self):
        """Toggle mute/unmute"""
        try:
            if self.is_muted:
                # Unmute - restore previous volume
                subprocess.run(['mpc', 'volume', str(self.current_volume)],
                             capture_output=True)
                self.is_muted = False
                log_debug(f"Unmuted to {self.current_volume}%")
            else:
                # Mute - set to 0
                subprocess.run(['mpc', 'volume', '0'], capture_output=True)
                self.is_muted = True
                log_debug("Muted")
        except Exception as e:
            log_debug(f"Mute toggle error: {e}")
    
    def toggle_play(self):
        """Toggle play/pause"""
        try:
            subprocess.run(['mpc', 'toggle'], capture_output=True)
            log_debug("Toggled play/pause")
        except Exception as e:
            log_debug(f"Play toggle error: {e}")
    
    def next_track(self):
        """Skip to next track"""
        try:
            subprocess.run(['mpc', 'next'], capture_output=True)
            log_debug("Next track")
        except Exception as e:
            log_debug(f"Next track error: {e}")
    
    def prev_track(self):
        """Go to previous track"""
        try:
            subprocess.run(['mpc', 'prev'], capture_output=True)
            log_debug("Previous track")
        except Exception as e:
            log_debug(f"Previous track error: {e}")
    
    def show_radio_browser(self):
        """Show the radio station browser"""
        log_debug("Opening radio browser")
        self.radio_browser.show()
    
    def load_album_art(self):
        """Load and process album art"""
        try:
            if not self.album_art_url:
                # No URL, clear album art
                self.album_art_image = None
                return
            
            log_debug(f"Loading album art: {self.album_art_url}")
            
            # Download image
            with request.urlopen(self.album_art_url, timeout=5) as response:
                image_data = response.read()
            
            # Open image
            img = Image.open(BytesIO(image_data))
            log_debug(f"Image loaded: {img.size} - {img.mode}")
            
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize to fill screen (maintain aspect ratio)
            img_ratio = img.width / img.height
            screen_ratio = SCREEN_WIDTH / SCREEN_HEIGHT
            
            if img_ratio > screen_ratio:
                # Image is wider than screen
                new_height = SCREEN_HEIGHT
                new_width = int(new_height * img_ratio)
            else:
                # Image is taller than screen
                new_width = SCREEN_WIDTH
                new_height = int(new_width / img_ratio)
            
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            log_debug(f"Resized to: {img.size}")
            
            # Crop to screen size (center)
            left = (new_width - SCREEN_WIDTH) // 2
            top = (new_height - SCREEN_HEIGHT) // 2
            img = img.crop((left, top, left + SCREEN_WIDTH, top + SCREEN_HEIGHT))
            log_debug(f"Cropped to: {img.size}")
            
            # Apply blur (subtle background effect)
            img = img.filter(ImageFilter.GaussianBlur(radius=10))
            log_debug("Blur applied")
            
            # Darken (create overlay effect)
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(0.4)  # 40% brightness
            log_debug("Darkened")
            
            # Convert to PhotoImage
            self.album_art_image = ImageTk.PhotoImage(img)
            log_debug("Album art ready")
            
        except Exception as e:
            log_debug(f"Album art load error: {e}")
            self.album_art_image = None
    
    def update_display(self):
        """Update UI elements"""
        try:
            # Update album art background
            if self.album_art_image:
                self.canvas.delete("all")
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.album_art_image)
            else:
                self.canvas.delete("all")
                self.canvas.create_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT,
                                            fill=BG_COLOR, outline="")
            
            # Update track info
            if self.current_track:
                self.title_label.config(text=self.current_track)
                self.artist_label.config(text=self.current_artist)
                self.album_label.config(text=self.current_album)
            else:
                self.title_label.config(text="No Track Playing")
                self.artist_label.config(text="")
                self.album_label.config(text="")
            
            # Update status indicator
            if self.is_playing:
                self.status_canvas.itemconfig(self.status_dot, fill=ACCENT_COLOR)
            else:
                self.status_canvas.itemconfig(self.status_dot, fill="#666666")
            
            # Update play button
            if self.is_playing:
                self.btn_play.config(text="⏸")
            else:
                self.btn_play.config(text="▶")
            
            # Update progress bar
            if self.current_duration > 0:
                progress = self.elapsed_time / self.current_duration
                bar_width = (SCREEN_WIDTH - 160) * progress
                self.progress_canvas.coords(self.progress_bar, 0, 0, bar_width, 8)
                
                # Update time labels
                elapsed_str = f"{self.elapsed_time // 60}:{self.elapsed_time % 60:02d}"
                duration_str = f"{self.current_duration // 60}:{self.current_duration % 60:02d}"
                self.elapsed_label.config(text=elapsed_str)
                self.duration_label.config(text=duration_str)
            else:
                self.progress_canvas.coords(self.progress_bar, 0, 0, 0, 8)
                self.elapsed_label.config(text="0:00")
                self.duration_label.config(text="0:00")
            
            # Update volume display
            if self.current_source == "spotify":
                # Hide volume controls during Spotify (Spotify has its own volume)
                self.volume_label.place_forget()
                self.btn_vol_down.place_forget()
                self.btn_vol_up.place_forget()
                self.btn_mute.place_forget()
            else:
                # Show volume controls for MPD/radio
                vol_x = SCREEN_WIDTH - 180
                vol_y = SCREEN_HEIGHT - 50
                
                self.btn_vol_down.place(x=vol_x - 60, y=vol_y, anchor="center")
                self.volume_label.place(x=vol_x + 10, y=vol_y, anchor="center")
                self.btn_vol_up.place(x=vol_x + 80, y=vol_y, anchor="center")
                self.btn_mute.place(x=vol_x + 140, y=vol_y, anchor="center")
                
                # Update volume text
                if self.is_muted:
                    self.volume_label.config(text="Vol: 🔇")
                    self.btn_mute.config(text="🔇")
                else:
                    self.volume_label.config(text=f"Vol: {self.current_volume}")
                    self.btn_mute.config(text="🔊")
            
        except Exception as e:
            log_debug(f"Display update error: {e}")
    
    def update_loop(self):
        """Background thread to update status"""
        last_track = ""
        
        while self.running:
            try:
                # Check Spotify first, then fall back to MPD
                # BUT: If MPD is actively playing, prefer MPD over stale Spotify data
                spotify_active = self.get_spotify_status()
                mpd_active = False
                
                if spotify_active:
                    # Spotify metadata exists, but check if MPD is ALSO playing
                    # If MPD is playing, it means user switched away from Spotify
                    # and Moode hasn't cleared the old Spotify metadata yet
                    mpd_check = subprocess.run(['mpc', 'status'], capture_output=True, text=True)
                    if '[playing]' in mpd_check.stdout:
                        # MPD is playing - prefer MPD over stale Spotify data
                        log_debug("Both Spotify metadata and MPD active - preferring MPD")
                        spotify_active = False
                        mpd_active = True
                
                if not spotify_active:
                    # No Spotify (or MPD took priority), try MPD
                    if not mpd_active:  # Only check if we didn't already check above
                        mpd_active = self.get_mpd_status()
                    else:
                        # We already know MPD is playing, just get the details
                        mpd_active = self.get_mpd_status()
                    
                    if not mpd_active:
                        # Nothing playing
                        self.is_playing = False
                        self.current_track = ""
                        self.current_artist = ""
                        self.current_album = ""
                        self.current_duration = 0
                        self.elapsed_time = 0
                        self.album_art_url = None
                        self.current_source = "unknown"
                
                # Get volume
                self.get_volume()
                
                # Load album art if track changed
                current_track_id = f"{self.current_artist}-{self.current_track}"
                if current_track_id != last_track:
                    if self.current_source == "spotify" and self.album_art_url:
                        self.load_album_art()
                    else:
                        self.album_art_image = None
                    last_track = current_track_id
                
                # Schedule UI update on main thread
                self.root.after(0, self.update_display)
                
                # Wait before next update
                time.sleep(UPDATE_INTERVAL / 1000.0)
                
            except Exception as e:
                log_debug(f"Update loop error: {e}")
                time.sleep(1)
    
    def cleanup(self):
        """Cleanup before exit"""
        self.running = False
        log_debug("Display shutting down")

def main():
    log_debug("="*50)
    log_debug("Moode Display starting...")
    
    root = tk.Tk()
    app = MoodeDisplay(root)
    
    # Handle window close
    root.protocol("WM_DELETE_WINDOW", lambda: [app.cleanup(), root.destroy()])
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        app.cleanup()
        log_debug("Display stopped by user")

if __name__ == "__main__":
    main()
