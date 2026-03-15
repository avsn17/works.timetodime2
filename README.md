# ✦ timetodime2

> Terminal Pomodoro suite by **avsn17**. Focus timer with Y2K mode, Kirby widget, music autoplay, galactic ranks, and cosmic boot system.

---

## 🚀 Quick Start

```bash
git clone https://github.com/avsn17/timetodime2
cd timetodime2
chmod +x install.sh && ./install.sh

# Main timer
python3 pomodoro_timer.py

# Quick launcher alias
echo "alias poyo='cd $(pwd) && python3 pomodoro_timer.py'" >> ~/.zshrc
source ~/.zshrc
poyo

# Mission launcher
chmod +x launch_mission.sh && ./launch_mission.sh

# Auto boot (git sync + patch + launch)
python3 cosmic_boot.py
```

---

## 📁 Files

| File | Description |
|------|-------------|
| `pomodoro_timer.py` | ✦ Main stellar focus timer |
| `poyo.py` | Compact cosmic timer with progress bar + chat |
| `pomodoro_y2k.py` | Y2K glitch aesthetic standalone timer |
| `pomodoro_web.html` | Browser-based timer UI |
| `kirby_widget.py` | Terminal status monitor widget |
| `kirby_dance.html` | Kirby dance animation page |
| `cosmic_boot.py` | Auto git sync + feature repair + launcher |
| `music_watcher.py` | Signal file watcher for music autoplay |
| `launch_mission.sh` | Shell launcher |
| `install.sh` | Setup script |
| `session_history.json` | Session data log |
| `music_signal.txt` | Music control signal file |
| `history.log` | Raw session history |

---

## ⌨️ Controls

| Key | Action |
|-----|--------|
| `Space` | Pause / Resume |
| `C` | Wisdom Chat |
| `S` | Stats Leaderboard |
| `A` | Config / Settings |
| `M` | Toggle Music Signal |
| `O` | Change Color Theme |
| `N` | Save & New Session |
| `Q` | Save & Quit |

---

## 📊 Stellar Rank System

| Distance | Rank |
|----------|------|
| 0 m | ⚫ Brown Dwarf |
| 100 m | 🟡 Yellow Dwarf |
| 500 m | 🔵 Blue Giant |
| 1,000 m | 🔴 Red Supergiant |
| 2,500 m | 💥 Supernova |
| 5,000 m | ⚡ Neutron Star |
| 10,000 m+ | 🌌 Singularity |

> 10 meters = 1 minute of focus time

---

## 💬 Wisdom Chat Categories

`wisdom` · `star` · `heroic` · `iro` · `bronte` · `kant` · `lyrics` · `vibe` · `mj` · `lana`

---

## 🎵 Music Autoplay

```bash
# Start watcher in background
python3 music_watcher.py &

# Drop your music
mkdir -p data && cp ~/music.mp3 data/focus_music.mp3
```

Signal protocol written to `music_signal.txt`:

| Signal | Action |
|--------|--------|
| `PLAY_NEXT` | Start playback |
| `STOP` | Stop playback |
| `PAUSE` | Freeze playback |
| `RESUME` | Resume playback |
| `IDLE` | No action |

---

## 🖥️ Variants

**Y2K Glitch Mode:**
```bash
python3 pomodoro_y2k.py
```

**Compact Timer (poyo):**
```bash
python3 poyo.py
```

**Web UI:**
```bash
python3 -m http.server && open http://localhost:8000/pomodoro_web.html
```

**Terminal Widget** (run in a separate terminal):
```bash
python3 kirby_widget.py
```

**Auto Boot System:**
```bash
python3 cosmic_boot.py   # git pull + repair + launch
```

---

## 🛠️ Requirements

- Python 3.10+
- `mpv` — local music: `sudo apt install mpv` / `brew install mpv`
- `libnotify-bin` — Linux notifications: `sudo apt install libnotify-bin`
- `tkinter` — bundled with most Python installs

---

## 🔗 Related

- **[kirbs.pomodoro](https://github.com/avsn17/kirbs.pomodoro)** — full upgrade: notifications, local music control, Base44 web dashboard

---

**avsn17** — *Ad astra. ✦*
