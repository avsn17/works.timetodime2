# ⏱️ timetodime2

> Cosmic focus timer by avsn17. Terminal-based Pomodoro with star-themed UI, Kirby widgets, Y2K mode, and galactic ranking.

---

## 🚀 Quick Start

```bash
git clone https://github.com/avsn17/timetodime2
cd timetodime2
chmod +x install.sh && ./install.sh

# Run the main timer
python3 pomodoro_timer.py

# Or use the mission launcher
chmod +x launch_mission.sh && ./launch_mission.sh

# Install alias
echo "alias poyo='cd $(pwd) && python3 pomodoro_timer.py'" >> ~/.zshrc
source ~/.zshrc
poyo
```

---

## 📁 Files

| File | Description |
|------|-------------|
| `pomodoro_timer.py` | ✦ Main stellar focus timer |
| `pomodoro_timer2.py` | Alternative timer variant |
| `pomodoro_y2k.py` | Y2K retro-themed timer |
| `pomodoro_web.html` | Browser-based timer UI |
| `kirby_widget.py` | Floating Kirby desktop widget (tkinter) |
| `kirby_dance.html` | Kirby dance animation page |
| `cosmic_boot.py` | Cosmic boot sequence / splash |
| `poyo.py` | Poyo launcher utility |
| `music_watcher.py` | Watches `music_signal.txt` for autoplay |
| `launch_mission.sh` | Shell launcher for the timer |
| `install.sh` | Setup script |
| `history.log` | Session history log |
| `session_history.json` | JSON session data |
| `music_signal.txt` | Music autoplay signal file |

---

## ⌨️ Controls

| Key | Action |
|-----|--------|
| `Space` | Pause / Resume |
| `C` | Open Wisdom Chat |
| `S` | Show Stats Leaderboard |
| `A` | Config / Settings |
| `M` | Toggle Music Signal |
| `O` | Change Background Color |
| `N` | Save & Start New Session |
| `Q` | Save & Quit |

---

## 📊 Stellar Ranking System

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

`wisdom` · `star` · `heroic` · `iro` · `bronte` · `kant` · `lyrics` · `vibe`

---

## 🎵 Music Autoplay

On session completion, `music_signal.txt` is written with `PLAY_NEXT`.

```bash
# Run the watcher in background
python3 music_watcher.py &
```

| Signal | Action |
|--------|--------|
| `PLAY_NEXT` | Start playing |
| `STOP` | Stop playback |
| `PAUSE` | Pause playback |
| `RESUME` | Resume playback |

---

## 🖥️ Variants

**Y2K Mode:**
```bash
python3 pomodoro_y2k.py
```

**Web UI:**
```bash
open pomodoro_web.html
# or
python3 -m http.server && open http://localhost:8000/pomodoro_web.html
```

**Kirby Widget:**
```bash
python3 kirby_widget.py
```

---

## 🛠️ Requirements

- Python 3.10+
- `tkinter` (for desktop widget — usually bundled)
- `mpv` (optional, for local music): `sudo apt install mpv` / `brew install mpv`

---

## 🔗 Related

- **[kirbs.pomodoro](https://github.com/avsn17/kirbs.pomodoro)** — full upgraded version with notifications, local music control, and Base44 web dashboard

---

## 👾 Navigator

**avsn17** — *Ad astra. ✦*
