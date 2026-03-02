import time, os, sys, threading, json, termios, tty, subprocess, random

COLORS = {
    "cosmic": "\033[38;5;141m", "solar": "\033[38;5;220m",
    "pink": "\033[38;5;213m", "reset": "\033[0m", "cyan": "\033[36m"
}

QUOTES = {
    "iro": ["Tea is just hot leaf juice!", "Sharing tea with a fascinating stranger is one of life’s true delights."],
    "mj": ["Heal the world, make it a better place.", "Just beat it, beat it!"],
    "lana": ["Live fast, die young, be wild and have fun.", "Blue jeans, white shirt..."],
    "heroic": ["Hard times create strong men.", "With great power comes great responsibility."]
}

class PomodoroTimer:
    def __init__(self):
        self.user_name = 'Cosmic Kirbs'
        self.history_file = 'session_history.json'
        self.time_goal = 25 * 60
        self.distance_goal = 100
        self.elapsed = 0
        self.paused = True
        self.mood = 'Hype'
        self.remind_interval = 10
        self.sessions = 0
        self.star_offset = 0

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def update_widget(self):
        try:
            progress = min(1.0, self.elapsed / self.time_goal) if self.time_goal > 0 else 0
            pos = int(15 * progress)
            kirby = '<( ^.^ )>✨' if progress >= 1.0 else ('<( -.- )>' if self.paused else '<( o.o )>')
            path = '·' * pos + kirby + '·' * (15 - pos) + '🌟'
            mood_icon = '💖' if self.mood == 'Hype' else '🍵'
            mins, secs = divmod(int(self.elapsed), 60)
            data = f' {mood_icon} {mins:02d}:{secs:02d} | {path} | {int(self.distance_goal)}m '
            with open('/tmp/pomodoro_widget.txt', 'w') as f: f.write(data)
        except: pass

    def chat(self):
        self.clear_screen()
        print(f"{COLORS['pink']}💬 WISDOM BOT ONLINE. Type 'iro', 'mj', 'lana', or 'back'.{COLORS['reset']}")
        while True:
            cmd = input("You: ").lower()
            if cmd == 'back': break
            category = QUOTES.get(cmd, ["Poyo! (I don't know that one yet)"])
            print(f"Bot: {random.choice(category)}")

    def open_settings(self):
        self.clear_screen()
        print("🛠️ KIRBY CONFIG\n[1] Interval [2] Mood [3] Back")
        choice = input("Select: ")
        if choice == '1': self.remind_interval = int(input("Minutes: "))
        elif choice == '2': self.mood = 'Calm' if self.mood == 'Hype' else 'Hype'

    def run(self):
        self.clear_screen()
        print(f"🌟 MISSION START: {self.user_name} 🌟")
        self.paused = False
        
        # Start Key Listener Thread
        def listen():
            while True:
                fd = sys.stdin.fileno()
                old = termios.tcgetattr(fd)
                try:
                    tty.setcbreak(fd)
                    key = sys.stdin.read(1)
                    if key == ' ': self.paused = not self.paused
                    elif key.lower() == 'c': self.chat()
                    elif key.lower() == 'a': self.open_settings()
                    elif key.lower() == 'q': os._exit(0)
                finally: termios.tcsetattr(fd, termios.TCSADRAIN, old)

        threading.Thread(target=listen, daemon=True).start()

        while True:
            if not self.paused:
                self.elapsed += 1
                if self.elapsed % (self.remind_interval * 60) == 0:
                    subprocess.run(['notify-send', 'KIRBY', '💧 Hydrate & Stretch!'])
            self.update_widget()
            self.draw_ui()
            time.sleep(1)

    def draw_ui(self):
        self.clear_screen()
        mins, secs = divmod(int(self.elapsed), 60)
        print(f"{COLORS['cosmic']}🚀 COSMIC POMODORO | Pilot: {self.user_name}{COLORS['reset']}")
        print(f"{COLORS['solar']}Time: {mins:02d}:{secs:02d} | Goal: {self.distance_goal}m{COLORS['reset']}")
        print(f"\nMood: {self.mood} {'💖' if self.mood == 'Hype' else '🍵'}")
        print("\n" + " " * (self.elapsed % 15) + "<( \" )> *poyo*")
        print("-" * 45)
        print("[Space] Pause | [A] Config | [C] Chat | [Q] Quit")

if __name__ == "__main__":
    app = PomodoroTimer()
    app.run()
