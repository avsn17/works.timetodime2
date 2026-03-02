#!/usr/bin/env python3
"""
Pomodoro Timer - Terminal App
A cosmic productivity timer with philosophical wisdom
"""

import time
import sys
import os
import threading
import random
import json
from datetime import datetime
from pathlib import Path

# Configuration
DATA_FILE = Path.home() / '.pomodoro_stats.json'
METERS_PER_MINUTE = 10

# Philosophical Quotes
QUOTES = {
    'wisdom': [
        'The journey is the reward.', 'Be like water, my friend.', 'Focus on the step, not the mountain.',
        'Silence is a source of great strength.', 'He who has a why to live can bear almost any how.'
    ],
    'heroic': [
        'Success is not final, failure is not fatal.', 'Fortune favors the brave.', 'I can do this all day.',
        'With great power comes great responsibility.', 'Hard times create strong men.'
    ],
    'iro': [
        'While it is always best to believe in oneself, a little help can be a blessing.',
        'Sharing tea with a fascinating stranger is one of lifes true delights.',
        'Hope is something you give yourself. That is the meaning of inner strength.'
    ],
    'bronte': [
        'I am no bird; and no net ensnares me.', 'I would always rather be happy than dignified.',
        'The soul that sees beauty may sometimes walk alone.'
    ],
    'kant': [
        'Two things fill the mind with wonder: the starry heavens and the moral law.',
        'Seek not the favor of the multitude; it is seldom got by honest means.',
        'Science is organized knowledge. Wisdom is organized life.'
    ],
    'lyrics': [
        'MJ: If you want to make the world a better place, take a look at yourself and make a change.',
        'MJ: Speed demon, minding my own business. Speedin on the highway of life.',
        'Lana: Will you still love me when I am no longer young and beautiful?',
        'Lana: Heaven is a place on earth with you.',
        'Lana: Summertime sadness, I just wanted you to know that baby you are the best.',
        'Bee Gees: Whether you are a brother or whether you are a mother, you are stayin alive.',
        'Bee Gees: Night fever, night fever! We know how to do it.',
        'CAS: I am a dreamer, and you are the dream.',
        'CAS: K. - I am always thinking of you.',
        'Billie: I am the bad guy, duh.',
        'Billie: Ocean eyes - I have never fallen from quite this high.',
        'Billie: You should see me in a crown.',
        'Bowie: Ground Control to Major Tom, commencing countdown.'
    ],
    'kirby': [
        '<( " )> Poyo! You are doing amazing, Cosmic Kirbs!',
        '<( o_o )> Focus mode: MAXIMUM PINK POWER.',
        '(> ^_^ )> <3 Sending positive vibes to the cockpit!'
    ],
    'vibe': [
        'Main Character Energy detected. 📈', 'No cap, your productivity is skyrocketing.',
        'Vibe check: ABSOLUTE LEGEND.', 'Big brain moves only.'
    ],
    'back': ['Returning to the cockpit...', 'Ready for ignition.', 'Focus mode: Reactivated.']
}

BREAK_ADVICES = [
    "Take a 5-minute walk to refresh your mind.",
    "Stretch your body and relax your shoulders.",
    "Look away from the screen - give your eyes a rest.",
    "Drink some water and stay hydrated.",
    "Take deep breaths and practice mindfulness.",
    "Step outside for fresh air if possible.",
    "Do a quick exercise - jumping jacks or push-ups!",
    "Listen to your favorite song.",
    "Message a friend or loved one.",
    "Enjoy a healthy snack.",
]

COLORS = {
    'stars': '\033[97m',      # Bright white
    'deep_space': '\033[94m', # Blue
    'nebula': '\033[95m',     # Magenta
    'cosmic': '\033[96m',     # Cyan
    'solar': '\033[93m',      # Yellow
    'void': '\033[90m',       # Dark gray
    'reset': '\033[0m',
    'green': '\033[92m',
    'red': '\033[91m',
}

class PomodoroTimer:
    def __init__(self):
        self.distance_goal = 0  
        self.time_goal = 0  
        self.elapsed = 0
        self.running = False
        self.paused = False
        self.chat_messages = []
        self.user_name = "Cosmic Kirbs"
        self.stats = self.load_stats()
        self.star_offset = 0
        self.bg_color = 'deep_space'
        self.timer_thread = None
        self.mood = "Hype"
        self.remind_interval = "10"
        self.session_count = 0
        self.music_playing = False
        
    def load_stats(self):
        if DATA_FILE.exists():
            with open(DATA_FILE, 'r') as f:
                try:
                    return json.load(f)
                except:
                    return {}
        return {}
    
    def save_stats(self):
        with open(DATA_FILE, 'w') as f:
            json.dump(self.stats, f, indent=2)
    
    def add_session(self, username, distance, duration, completed=True):
        if username not in self.stats:
            self.stats[username] = {
                'sessions': [],
                'total_distance': 0,
                'total_time': 0,
                'completed_sessions': 0
            }
        
        session = {
            'date': datetime.now().isoformat(),
            'distance': distance,
            'duration': duration,
            'completed': completed
        }
        
        self.stats[username]['sessions'].append(session)
        self.stats[username]['total_distance'] += distance
        self.stats[username]['total_time'] += duration
        if completed:
            self.stats[username]['completed_sessions'] += 1
            self.session_count += 1
        
        self.save_stats()
    
    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def draw_stars(self, width, height):
        stars = []
        star_chars = ['·', '∙', '•', '*', '✦', '✧']
        num_stars = (width * height) // 40
        for _ in range(num_stars):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            char = random.choice(star_chars)
            stars.append((x, y, char))
        grid = [[' ' for _ in range(width)] for _ in range(height)]
        for x, y, char in stars:
            new_x = (x + self.star_offset) % width
            if 0 <= new_x < width and 0 <= y < height:
                grid[y][new_x] = char
        return grid

    def draw_ui(self):
        self.clear_screen()
        try:
            cols, rows = os.get_terminal_size()
        except:
            cols, rows = 80, 24
        
        print(COLORS[self.bg_color], end='')
        star_grid = self.draw_stars(cols, rows - 1)
        progress = min(self.elapsed / self.time_goal if self.time_goal > 0 else 0, 1.0)
        progress_bar_width = max(cols - 35, 20)
        filled = int(progress_bar_width * progress)
        distance_covered = (self.elapsed / 60) * METERS_PER_MINUTE
        
        header = f" 🎯 Goal: {self.distance_goal}m | User: {self.user_name} | Sessions: {self.session_count} "
        mins, secs = divmod(int(self.elapsed), 60)
        timer_display = f" ⏱️  {mins:02d}:{secs:02d} "
        
        if self.running and not self.paused:
            status = " ▶ RUNNING "
        elif self.paused:
            status = " ⏸ PAUSED "
        else:
            status = " ⏹ STOPPED "
        
        for row_idx in range(rows - 1):
            line = star_grid[row_idx]
            if row_idx == 1:
                for i, char in enumerate(header): 
                    if i < cols: line[i+2] = char
            elif row_idx == 3:
                for i, char in enumerate(timer_display): 
                    if i < cols: line[2 + i] = char
            elif row_idx == 5:
                bar_plain = f" [{'█' * filled}{'░' * (progress_bar_width - filled)}] {distance_covered:.0f}m "
                for i, char in enumerate(bar_plain): 
                    if i < cols: line[2 + i] = char
            elif row_idx == 7:
                for i, char in enumerate(status): 
                    if i < cols: line[2 + i] = char
            
            print(''.join(line))
        
        controls = " [Space] Pause | [N] New | [S] Stats | [A] Settings | [M] Music | [Q] Quit "
        print(COLORS['reset'] + COLORS['solar'] + controls[:cols] + COLORS['reset'])
        sys.stdout.flush()

    def timer_loop(self):
        while self.running:
            if not self.paused:
                time.sleep(0.1)
                self.elapsed += 0.1
                self.star_offset = (self.star_offset + 1) % 100
                if self.elapsed >= self.time_goal:
                    self.timer_complete()
                    break
            else:
                time.sleep(0.1)

    def timer_complete(self):
        self.running = False
        distance_covered = (self.elapsed / 60) * METERS_PER_MINUTE
        self.add_session(self.user_name, distance_covered, int(self.elapsed), completed=True)
        self.clear_screen()
        print(f"\n\n{COLORS['solar']} 🎉 Goal Reached! Session logged. {COLORS['reset']}")
        print(f" ✨ {random.choice(QUOTES['kirby'])}")
        # Signal for music autoplay
        try:
            with open('music_signal.txt', 'w') as f: f.write('toggle')
        except: pass
        time.sleep(3)

    def show_stats(self):
        self.clear_screen()
        print(f"\n {COLORS['solar']}📊 STATISTICS LEADERBOARD{COLORS['reset']}\n")
        if not self.stats:
            print(" No statistics yet.")
        else:
            sorted_stats = sorted(self.stats.items(), key=lambda x: x[1]['total_distance'], reverse=True)
            for rank, (name, data) in enumerate(sorted_stats, 1):
                print(f" {rank}. {name}: {data['total_distance']:.0f}m ({data['completed_sessions']} sessions)")
        input("\n Press ENTER to return to cockpit...")

    def open_settings(self):
        self.clear_screen()
        print(f"\n {COLORS['cosmic']}🛠️ KIRBY CONFIG{COLORS['reset']}")
        print(f" [1] Hydration Interval: {self.remind_interval}m")
        print(f" [2] Kirby Mood: {self.mood}")
        print(f" [3] Reset Session Count")
        print(f" [4] Exit")
        
        choice = input('\n Select: ')
        if choice == '1':
            self.remind_interval = input(' Enter minutes: ')
        elif choice == '2':
            self.mood = 'Calm' if self.mood == 'Hype' else 'Hype'
        elif choice == '3':
            self.session_count = 0

    def run(self):
        while True:
            self.clear_screen()
            print(f"{COLORS['solar']} 🌟 Cosmic Pomodoro Ignition 🌟 {COLORS['reset']}")
            try:
                raw_dist = input(f"\n {COLORS['green']}Enter distance goal (meters) [or Q to quit]: {COLORS['reset']}")
                if raw_dist.lower() == 'q': break
                distance = int(raw_dist)
                self.distance_goal = distance
                self.time_goal = (distance / METERS_PER_MINUTE) * 60
                self.elapsed = 0
            except ValueError:
                continue
            
            self.running = True
            self.paused = False
            self.start_timer_thread()
            
            import select, termios, tty
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setcbreak(fd)
                while self.running:
                    self.draw_ui()
                    if select.select([sys.stdin], [], [], 0.1)[0]:
                        key = sys.stdin.read(1)
                        if key == ' ':
                            self.paused = not self.paused
                        elif key.lower() == 'a':
                            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                            self.open_settings()
                            tty.setcbreak(fd)
                        elif key.lower() == 'm':
                            state = 'toggle'
                            try:
                                with open('music_signal.txt', 'w') as f_sig: f_sig.write(state)
                            except: pass
                        elif key.lower() == 's':
                            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                            self.show_stats()
                            tty.setcbreak(fd)
                        elif key.lower() == 'n':
                            self.running = False
                            break
                        elif key.lower() == 'q':
                            self.running = False
                            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                            sys.exit()
                    time.sleep(0.05)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def start_timer_thread(self):
        self.timer_thread = threading.Thread(target=self.timer_loop, daemon=True)
        self.timer_thread.start()

if __name__ == "__main__":
    try:
        app = PomodoroTimer()
        app.run()
    except KeyboardInterrupt:
        print(f"\n\n 👋 Ground Control to {app.user_name}: Mission Aborted.")