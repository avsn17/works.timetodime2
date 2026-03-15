#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════╗
║   ✦ STELLAR FOCUS TIMER ✦                        ║
║     Navigator: avsn17  |  timetodime2            ║
╚══════════════════════════════════════════════════╝
"""

import time, sys, os, threading, random, json, select
import termios, tty
from datetime import datetime
from pathlib import Path

# ─── CONFIG ───────────────────────────────────────────────────────────────────
DATA_FILE         = Path.home() / '.pomodoro_stats.json'
SIGNAL_FILE       = Path('music_signal.txt')
METERS_PER_MINUTE = 10
USER_ID           = "avsn17"

# ─── COLORS ───────────────────────────────────────────────────────────────────
C = {
    'gold':    '\033[38;5;220m',   # bright gold
    'amber':   '\033[38;5;214m',   # amber
    'silver':  '\033[38;5;252m',   # silver white
    'dim':     '\033[38;5;240m',   # dim gray
    'cyan':    '\033[38;5;87m',    # ice cyan
    'violet':  '\033[38;5;135m',   # deep violet
    'rose':    '\033[38;5;211m',   # rose
    'green':   '\033[38;5;120m',   # mint green
    'red':     '\033[38;5;196m',   # red
    'bg':      '\033[48;5;232m',   # near-black bg
    'bold':    '\033[1m',
    'dim_txt': '\033[2m',
    'reset':   '\033[0m',
}

# ─── STAR ANIMATIONS ──────────────────────────────────────────────────────────
STAR_FRAMES = [
    "    ✦    ",
    "   ✦✦✦   ",
    "  ✦ ★ ✦  ",
    "   ✦✦✦   ",
    "    ✦    ",
]

SHOOTING_STAR = ['·', '–', '—', '✦', '★', '✦', '—', '–', '·']

CONSTELLATIONS = [
    # Orion belt (3 stars in a row)
    ["      ✦           ",
     "  ✦       ✦      ",
     "      ✦   ✦  ✦   ",
     "    ✦ ★ ✦ ★ ✦ ★  ",
     "      ✦       ✦  ",
     "  ✦       ✦      "],
    # Big dipper
    ["  ✦ ✦             ",
     "      ✦ ✦         ",
     "          ★       ",
     "        ★   ★     ",
     "      ★       ★   ",
     "                  "],
    # Cross
    ["      ★           ",
     "    ✦ ★ ✦         ",
     "  ✦   ★   ✦       ",
     "    ✦ ★ ✦         ",
     "      ✦           ",
     "                  "],
]

# ─── STAR RANK SYSTEM ─────────────────────────────────────────────────────────
RANK_TIERS = [
    (0,     "⚫ Brown Dwarf"),
    (100,   "🟡 Yellow Dwarf"),
    (500,   "🔵 Blue Giant"),
    (1000,  "🔴 Red Supergiant"),
    (2500,  "💥 Supernova"),
    (5000,  "⚡ Neutron Star"),
    (10000, "🌌 Singularity"),
]

MILESTONE_MSGS = {
    25:  "✦ First light detected",
    50:  "★ Halfway to the stars",
    75:  "✦✦ Approaching nova",
    100: "★ STELLAR COMPLETE ★",
}

# ─── QUOTES ───────────────────────────────────────────────────────────────────
QUOTES = {
    'wisdom': [
        'The cosmos is within us. We are made of star-stuff. — Sagan',
        'For small creatures such as we, the vastness is bearable only through love. — Sagan',
        'Look up at the stars and not down at your feet. — Hawking',
        'The universe is under no obligation to make sense to you. — deGrasse Tyson',
        'Silence is a source of great strength.',
    ],
    'heroic': [
        'Success is not final, failure is not fatal.',
        'Fortune favors the brave.',
        'Per aspera ad astra — through hardship to the stars.',
        'Ad astra et ultra — to the stars and beyond.',
        'The impediment to action advances action. — Aurelius',
    ],
    'iro': [
        'While it is always best to believe in oneself, a little help can be a blessing.',
        'Hope is something you give yourself. That is the meaning of inner strength.',
        'Sharing tea with a fascinating stranger is one of lifes true delights.',
    ],
    'bronte': [
        'I am no bird; and no net ensnares me.',
        'I would always rather be happy than dignified.',
        'The soul that sees beauty may sometimes walk alone.',
    ],
    'kant': [
        'Two things fill me with wonder: the starry heavens above, the moral law within.',
        'Seek not the favor of the multitude; it is seldom got by honest means.',
        'Act only according to that maxim whereby you can will it to be universal.',
    ],
    'lyrics': [
        'Bowie: Ground Control to Major Tom, commencing countdown.',
        'Bowie: We can be heroes, just for one day.',
        'Lana: Heaven is a place on earth with you.',
        'MJ: If you want to make the world a better place, take a look at yourself.',
        'Billie: You should see me in a crown.',
        'CAS: I am a dreamer, and you are the dream.',
    ],
    'star': [
        '✦ You are made of the same atoms as the stars.',
        '★ Every photon of focus brings you closer to the constellation.',
        '✦ The universe spent 13 billion years making you — make it count.',
        '★ You are not a drop in the ocean. You are the entire ocean in a drop.',
        '✦ Even black holes radiate. So do you.',
    ],
    'vibe': [
        'Main Character Energy: STELLAR 📈',
        'Vibe check: ABSOLUTE SUPERNOVA.',
        'Big brain moves only.',
        'No cap, your focus is at light speed.',
    ],
}

BREAK_ADVICES = [
    "Stretch — your spine is not a black hole.",
    "Drink water. Stars are mostly hydrogen too. 💧",
    "Look at something 20 feet away for 20 seconds.",
    "Take 5 deep breaths. Reset the orbit.",
    "Step outside. Touch grass. Then return to the cosmos.",
    "Do 10 jumping jacks. Get the blood moving.",
    "Message someone you like.",
    "Enjoy a snack. Fuel the star.",
]

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def get_rank(total_m: float) -> str:
    rank = RANK_TIERS[0][1]
    for threshold, label in RANK_TIERS:
        if total_m >= threshold:
            rank = label
    return rank

def clear():
    sys.stdout.write("\033[H\033[2J")
    sys.stdout.flush()

def signal_music(state: str = "PLAY_NEXT"):
    try:
        SIGNAL_FILE.write_text(state)
    except Exception:
        pass

def _try_notify(fn_name: str, *args):
    try:
        import kirby_notify
        getattr(kirby_notify, fn_name)(*args)
    except Exception:
        pass

# ─── MAIN CLASS ───────────────────────────────────────────────────────────────
class StellarTimer:
    def __init__(self):
        self.user_name       = USER_ID
        self.distance_goal   = 0
        self.time_goal       = 0.0
        self.elapsed         = 0.0
        self.running         = False
        self.paused          = False
        self.in_subscreen    = False
        self.chat_messages   = []
        self.stats           = self._load_stats()
        self.star_offset     = 0
        self.frame_idx       = 0
        self.constellation   = random.choice(CONSTELLATIONS)
        self.bg_color        = 'gold'
        self.timer_thread    = None
        self.mood            = "Stellar"
        self.remind_interval = "10"
        self.session_count   = 0
        self.music_enabled   = True
        self._status_banner  = ("", 0.0)
        self._old_termios    = None
        self._last_percent   = -1

    # ── Stats ─────────────────────────────────────────────────────────────────
    def _load_stats(self) -> dict:
        if DATA_FILE.exists():
            try:
                return json.loads(DATA_FILE.read_text())
            except Exception:
                pass
        return {}

    def _save_stats(self):
        DATA_FILE.write_text(json.dumps(self.stats, indent=2))

    def _add_session(self, distance: float, duration: float, completed: bool = True):
        u = self.user_name
        if u not in self.stats:
            self.stats[u] = {'sessions': [], 'total_distance': 0.0,
                              'total_time': 0.0, 'completed_sessions': 0}
        self.stats[u]['sessions'].append({
            'date': datetime.now().isoformat(),
            'distance': round(distance, 2),
            'duration': round(duration, 1),
            'completed': completed,
        })
        self.stats[u]['total_distance'] += distance
        self.stats[u]['total_time']     += duration
        if completed:
            self.stats[u]['completed_sessions'] += 1
            self.session_count += 1
        self._save_stats()

    def _total_distance(self) -> float:
        return self.stats.get(self.user_name, {}).get('total_distance', 0.0)

    # ── Banner ────────────────────────────────────────────────────────────────
    def _set_banner(self, text: str, duration: float = 2.5):
        self._status_banner = (text, time.time() + duration)

    def _get_banner(self) -> str:
        text, expiry = self._status_banner
        return text if time.time() < expiry else ""

    # ── Timer thread ──────────────────────────────────────────────────────────
    def _timer_loop(self):
        while self.running:
            if not self.paused and not self.in_subscreen:
                time.sleep(0.1)
                self.elapsed     += 0.1
                self.star_offset  = (self.star_offset + 1) % 300
                self.frame_idx    = (self.frame_idx + 1) % len(STAR_FRAMES)
                if self.elapsed >= self.time_goal:
                    self._complete()
                    break
            else:
                time.sleep(0.05)

    def _start_timer(self):
        self.running      = True
        self.timer_thread = threading.Thread(target=self._timer_loop, daemon=True)
        self.timer_thread.start()

    def _complete(self):
        self.running = False
        dist = (self.elapsed / 60) * METERS_PER_MINUTE
        self._add_session(dist, self.elapsed, completed=True)
        _try_notify('notify_session_end', dist, get_rank(self._total_distance()))
        if self.music_enabled:
            signal_music("PLAY_NEXT")

    # ── UI ────────────────────────────────────────────────────────────────────
    def _draw_starfield(self, cols, rows):
        chars = ['·', '∙', '•', '✦', '✧', '★', '*', '⋆']
        grid  = [[' '] * cols for _ in range(rows)]
        n     = (cols * rows) // 25
        for _ in range(n):
            x  = random.randint(0, cols - 1)
            y  = random.randint(0, rows - 1)
            nx = (x + self.star_offset) % cols
            # Gold/silver mix
            grid[y][nx] = random.choice(chars)
        # Shooting star across row 2
        ss_x = (self.star_offset * 2) % max(cols - 10, 1)
        for i, ch in enumerate(SHOOTING_STAR):
            px = ss_x + i
            if 0 <= px < cols:
                grid[2][px] = ch
        return grid

    def _draw_ui(self):
        clear()
        try:
            cols, rows = os.get_terminal_size()
        except Exception:
            cols, rows = 80, 24

        col   = C[self.bg_color]
        print(col, end='')

        grid      = self._draw_starfield(cols, rows - 1)
        progress  = min(self.elapsed / self.time_goal, 1.0) if self.time_goal > 0 else 0.0
        bar_w     = max(cols - 32, 20)
        dist_done = (self.elapsed / 60) * METERS_PER_MINUTE
        mins, sec = divmod(int(self.elapsed), 60)
        total_d   = self._total_distance()
        percent   = int(progress * 100)

        # Shooting star progress bar
        filled    = int(bar_w * progress)
        bar_str   = "❮" + "─" * max(filled - 1, 0) + ("★" if filled > 0 else "") + "·" * (bar_w - filled) + "❯" + f" {dist_done:.0f}/{self.distance_goal}m"

        header    = (f"✦ Navigator: {self.user_name}  |  Sessions: {self.session_count}"
                     f"  |  Rank: {get_rank(total_d)}")
        timer_d   = f"◈  {mins:02d}:{sec:02d}"
        music_ind = '♪ ON' if self.music_enabled else '♪ OFF'

        if self.running and not self.paused: status_str = f"▶ IN ORBIT    {music_ind}"
        elif self.paused:                    status_str = f"⏸ DRIFTING    {music_ind}"
        else:                                status_str = f"⏹ GROUNDED    {music_ind}"

        # Star animation (right side)
        star_anim  = STAR_FRAMES[self.frame_idx % len(STAR_FRAMES)]
        # Constellation (right column)
        const_col  = cols - 22
        banner     = self._get_banner()

        def _wr(r, text, start=0):
            plain = text
            for i, ch in enumerate(plain):
                p = start + i
                if 0 <= r < len(grid) and 0 <= p < len(grid[r]):
                    grid[r][p] = ch

        for r in range(rows - 1):
            if r == 1:   _wr(r, header[:cols - 25])
            elif r == 4: _wr(r, timer_d, 2)
            elif r == 6: _wr(r, bar_str[:cols - 2], 2)
            elif r == 8: _wr(r, status_str, 2)
            elif r == 10:
                if banner:
                    _wr(r, banner, max(0, (cols - len(banner)) // 2))
                else:
                    _wr(r, star_anim, max(0, (cols // 2) - 5))

            # Constellation right panel
            if const_col > 40:
                ci = r - 3
                if 0 <= ci < len(self.constellation):
                    _wr(r, self.constellation[ci], const_col)

            # Wisdom sidebar
            chat_col = cols - 50
            if chat_col > 40:
                if r == 14:
                    _wr(r, "✦ STELLAR TRANSMISSIONS", chat_col)
                elif 15 <= r <= rows - 3:
                    idx     = r - 15
                    visible = self.chat_messages[-(rows - 18):]
                    if idx < len(visible):
                        _wr(r, visible[idx][:47], chat_col)

            print(''.join(grid[r]))

        controls = ("[Space] Pause  [N] New  [S] Stars  [A] Config  "
                    "[C] Chat  [M] Music  [O] Color  [Q] Quit")
        print(controls[:cols] + C['reset'])
        sys.stdout.flush()

    # ── Subscreen helpers ─────────────────────────────────────────────────────
    def _enter_sub(self):
        self.in_subscreen = True
        if self._old_termios:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._old_termios)

    def _exit_sub(self):
        self.in_subscreen = False
        tty.setcbreak(sys.stdin.fileno())

    # ── Chat ──────────────────────────────────────────────────────────────────
    def _chat(self):
        self._enter_sub()
        clear()
        print(f"{C['gold']}{C['bold']}✦ STELLAR TRANSMISSIONS ✦{C['reset']}")
        print(f"{C['dim']}Categories: wisdom · star · heroic · iro · bronte · kant · lyrics · vibe{C['reset']}")
        print(f"{C['dim']}Type 'back' to return to orbit.\n{C['reset']}")
        while True:
            try:
                raw = input(f"{C['green']}You: {C['reset']}").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if raw.lower() == 'back':
                break
            if raw:
                resp = self._bot_reply(raw)
                self.chat_messages.append(f"✦ {raw[:43]}")
                self.chat_messages.append(f"★ {resp[:43]}")
                print(f"\n{C['gold']}★ {resp}{C['reset']}\n")
        self._exit_sub()

    def _bot_reply(self, msg: str) -> str:
        ml = msg.lower()
        if any(w in ml for w in ['star', 'cosmos', 'space', 'universe']): cat = 'star'
        elif any(w in ml for w in ['iro', 'tea', 'uncle']):               cat = 'iro'
        elif any(w in ml for w in ['bronte', 'emily', 'love', 'soul']):   cat = 'bronte'
        elif any(w in ml for w in ['kant', 'moral', 'reason']):           cat = 'kant'
        elif any(w in ml for w in ['song', 'music', 'lyric']):            cat = 'lyrics'
        elif any(w in ml for w in ['hero', 'brave', 'courage']):          cat = 'heroic'
        elif any(w in ml for w in ['vibe', 'cap', 'legend']):             cat = 'vibe'
        else:                                                               cat = random.choice(list(QUOTES))
        return random.choice(QUOTES[cat])

    # ── Stats ─────────────────────────────────────────────────────────────────
    def _show_stats(self):
        self._enter_sub()
        clear()
        print(f"{C['gold']}{C['bold']}★ STELLAR LEADERBOARD ★{C['reset']}\n")
        print("═" * 82)
        if not self.stats:
            print("No data yet. Complete a session to chart your stars!")
        else:
            print(f"{'#':<5} {'Navigator':<22} {'Distance':<12} {'Time':<12} {'Sessions':<10} {'Rank'}")
            print("─" * 82)
            for i, (name, d) in enumerate(sorted(
                    self.stats.items(), key=lambda x: x[1].get('total_distance', 0), reverse=True), 1):
                total_d   = d.get('total_distance', 0)
                total_t   = d.get('total_time', 0)
                sessions  = len(d.get('sessions', []))
                completed = d.get('completed_sessions', 0)
                h, m      = divmod(int(total_t) // 60, 60)
                t_str     = f"{h}h {m:02d}m" if h else f"{m}m"
                col       = C['gold'] if i == 1 else C['amber'] if i <= 3 else ''
                print(f"{col}{i:<5} {name:<22} {total_d:.0f}m{'':<6} {t_str:<12} {sessions}/{completed}{'':<4} {get_rank(total_d)}{C['reset']}")
        print("\nPress ENTER to return to orbit...")
        input()
        self._exit_sub()

    # ── Settings ──────────────────────────────────────────────────────────────
    def _open_settings(self):
        self._enter_sub()
        clear()
        print(f"\n{C['gold']}{C['bold']}✦ ─── STELLAR CONFIG ─── ✦{C['reset']}\n")
        print(f"  [1] Hydration Reminder  (Every: {self.remind_interval}m)")
        print(f"  [2] Navigator Mood      ({self.mood})")
        print(f"  [3] Reset Session Count ({self.session_count})")
        print(f"  [4] Toggle Music        ({'ON ♪' if self.music_enabled else 'OFF ♪'})")
        print(f"  [5] Change Star Color")
        print(f"  [6] Back\n")
        try:
            ch = input(f"{C['cyan']}Select: {C['reset']}").strip()
            if ch == '1':
                v = input("  Interval (minutes): ").strip()
                if v.isdigit():
                    self.remind_interval = v
                    print(f"  ✦ Updated to {v}m!")
            elif ch == '2':
                self.mood = 'Calm' if self.mood == 'Stellar' else 'Stellar'
                print(f"  ★ Mood: {self.mood}!")
            elif ch == '3':
                self.session_count = 0
                print("  ✦ Session count reset.")
            elif ch == '4':
                self.music_enabled = not self.music_enabled
                if self.music_enabled:
                    signal_music("PLAY_NEXT")
                print(f"  Music: {'ON ♪' if self.music_enabled else 'OFF'}")
            elif ch == '5':
                self._choose_color()
        except (EOFError, KeyboardInterrupt):
            pass
        time.sleep(0.6)
        self._exit_sub()

    def _choose_color(self):
        opts   = {'1':'gold','2':'amber','3':'silver','4':'cyan','5':'violet','6':'rose'}
        labels = {'gold':'Gold ✦','amber':'Amber ★','silver':'Silver ✧',
                  'cyan':'Ice Cyan ◈','violet':'Deep Violet ✦','rose':'Rose ★'}
        print()
        for k, v in opts.items():
            print(f"  [{k}] {labels[v]}")
        ch = input("  Pick (1-6): ").strip()
        if ch in opts:
            self.bg_color = opts[ch]
            print(f"  ✦ Color set to {labels[opts[ch]]}!")

    # ── Splash ────────────────────────────────────────────────────────────────
    def _splash(self):
        clear()
        for line in [
            "",
            f"{C['gold']}{C['bold']}  ╔══════════════════════════════════════════╗{C['reset']}",
            f"{C['gold']}{C['bold']}  ║   ✦ ✦ ✦  STELLAR FOCUS TIMER  ✦ ✦ ✦   ║{C['reset']}",
            f"{C['gold']}{C['bold']}  ║       Navigator: {self.user_name:<22}║{C['reset']}",
            f"{C['gold']}{C['bold']}  ╚══════════════════════════════════════════╝{C['reset']}",
            "",
            f"  {C['amber']}Rank: {get_rank(self._total_distance())}{C['reset']}",
            f"  {C['silver']}Sessions: {self.session_count}{C['reset']}",
            "",
            f"  {C['dim']}{random.choice(QUOTES['star'])}{C['reset']}",
            "",
        ]:
            print(line)

    # ── Finish ────────────────────────────────────────────────────────────────
    def _finish_screen(self):
        clear()
        dist = (self.elapsed / 60) * METERS_PER_MINUTE
        rank = get_rank(self._total_distance())
        print(f"\n{C['gold']}{C['bold']}  ★ ─── STELLAR MISSION COMPLETE ─── ★{C['reset']}")
        print(f"  {C['green']}Distance: {dist:.0f} m{C['reset']}")
        print(f"  {C['amber']}Rank: {rank}{C['reset']}")
        print(f"\n  ✦ Break: {random.choice(BREAK_ADVICES)}")
        print(f"\n  ★ {random.choice(QUOTES['star'])}")
        _try_notify('notify_session_end', dist, rank)
        if self.music_enabled:
            signal_music("PLAY_NEXT")
            print(f"\n  ♪ Music signal sent.")
        self._ask_restart()

    def _ask_restart(self):
        try:
            ch = input(f"\n  {C['green']}Launch new mission? (y/n): {C['reset']}").strip().lower()
        except (EOFError, KeyboardInterrupt):
            ch = 'n'
        if ch == 'y':
            self.elapsed        = 0.0
            self.running        = False
            self.paused         = False
            self.chat_messages  = []
            self._last_percent  = -1
            self.constellation  = random.choice(CONSTELLATIONS)
            self.run()
        else:
            print(f"\n  {C['gold']}✦ Safe travels, {self.user_name}. Ad astra. 🌌{C['reset']}\n")

    # ── Main loop ─────────────────────────────────────────────────────────────
    def run(self):
        self._splash()

        while True:
            try:
                raw  = input(f"\n  {C['green']}Enter distance goal in meters (10 m = 1 min): {C['reset']}").strip()
                dist = int(raw)
                if dist <= 0:
                    raise ValueError
                self.distance_goal = dist
                self.time_goal     = (dist / METERS_PER_MINUTE) * 60
                self.elapsed       = 0.0
                break
            except ValueError:
                print(f"  {C['red']}Please enter a positive integer.{C['reset']}")

        self._start_timer()
        _try_notify('notify_session_start', self.distance_goal)
        self._old_termios = termios.tcgetattr(sys.stdin)

        try:
            tty.setcbreak(sys.stdin.fileno())

            while self.running or self.paused:
                if not self.in_subscreen:
                    percent = int((self.elapsed / self.time_goal) * 100) if self.time_goal > 0 else 0
                    if percent != self._last_percent and percent in MILESTONE_MSGS:
                        self._set_banner(MILESTONE_MSGS[percent], 3.0)
                        _try_notify('notify_milestone', percent)
                    self._last_percent = percent
                    self._draw_ui()

                if select.select([sys.stdin], [], [], 0.08)[0]:
                    key = sys.stdin.read(1).lower()

                    if key == ' ':
                        self.paused = not self.paused

                    elif key == 'q':
                        dist = (self.elapsed / 60) * METERS_PER_MINUTE
                        self._add_session(dist, self.elapsed, completed=False)
                        self.running = False
                        break

                    elif key == 'n':
                        dist = (self.elapsed / 60) * METERS_PER_MINUTE
                        self._add_session(dist, self.elapsed, completed=False)
                        self.running = False
                        break

                    elif key == 'c':
                        self._chat()

                    elif key == 's':
                        self._show_stats()

                    elif key == 'a':
                        self._open_settings()

                    elif key == 'm':
                        self.music_enabled = not self.music_enabled
                        if self.music_enabled:
                            signal_music("PLAY_NEXT")
                            banner = "♪ MUSIC ON  — signal sent!"
                        else:
                            signal_music("STOP")
                            banner = "♪ MUSIC OFF — signal sent."
                        self._set_banner(banner, 2.5)
                        self.chat_messages.append(banner)

                    elif key == 'o':
                        self._enter_sub()
                        clear()
                        self._choose_color()
                        time.sleep(0.4)
                        self._exit_sub()

                time.sleep(0.05)

        finally:
            try:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._old_termios)
            except Exception:
                pass
            print(C['reset'])

        if self.elapsed >= self.time_goal > 0:
            self._finish_screen()
        else:
            self._ask_restart()


# ─── ENTRY POINT ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        StellarTimer().run()
    except KeyboardInterrupt:
        print(f"\n\n{C['gold']}✦ Mission aborted. Ad astra, {USER_ID}. 🌌{C['reset']}\n")