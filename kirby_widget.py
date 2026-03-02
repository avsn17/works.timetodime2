import time
import os

def draw_widget():
    path = '/tmp/pomodoro_widget.txt'
    while True:
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    data = f.read().strip()
                # Clear terminal and print only the widget line
                print("\033[H\033[J" + data, end='', flush=True)
            else:
                print("\033[H\033[J <( ?_? )> Waiting for Kirby...", end='', flush=True)
        except Exception:
            pass
        time.sleep(1)

if __name__ == "__main__":
    try:
        draw_widget()
    except KeyboardInterrupt:
        print("\nWidget Closed.")
