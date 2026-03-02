import time  # ✅ time module (for time.sleep)
from datetime import time as dt_time  # if you need datetime's time class elsewhere

from pomodoro_timer import COLORS


def run(self):
    """Main application loop with Y2K Start - Licensed to Cosmic Kirbs"""
    # 1. Hardcoded identity (The New Era)
    self.user_name = "Cosmic Kirbs"

    # 2. Start the Glitch Aesthetic Welcome
    self.show_y2k_splash()

    # 3. Stats & History Check (Locked in)
    print(f"{COLORS['cosmic']}>> PILOT IDENTIFIED: {self.user_name} <<{COLORS['reset']}")
    print(f"{COLORS['nebula']}Current Rank: {self.get_rank()} | Let's get it. ✨{COLORS['reset']}\n")

    # 4. Mission Setup — loop until valid input instead of recursing
    while True:
        try:
            goal_input = input(f"{COLORS['solar']}Set orbit distance (e.g. 250m): {COLORS['reset']}")
            self.target_distance = float(goal_input)
            break  # ✅ valid input, exit loop
        except ValueError:
            print(f"{COLORS['red']}Error: Enter a number, bestie. 🛑{COLORS['reset']}")
            time.sleep(1)  # ✅ now correctly calls time.sleep

    # Ignition
    self.start_timer()