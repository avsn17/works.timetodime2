#!/bin/bash
# name: kirbs
# desc: Cosmic Mission Control for avsn17
# usage: ./kirbs

# --- CONFIGURATION ---
BASE_DIR="/workspaces/timetodime2"
WIDGET_BIN="$BASE_DIR/kirby_widget.py"
TIMER_BIN="$BASE_DIR/pomodoro_timer.py"
WIDGET_LOG="/tmp/pomodoro_widget.txt"

# --- UI STYLING ---
PINK='\033[38;5;218m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' 

# --- SESSION CLEANUP ---
# Standard professional "trap" to ensure background tasks die with the script
cleanup() {
    # Kill all background processes started by this script (the widget)
    kill $(jobs -p) 2>/dev/null
    rm -f "$WIDGET_LOG"
    echo -e "\n${PINK}<( 'o' )> Poyo! Mission complete, avsn17. Closing cockpit...${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM EXIT

# --- PRE-FLIGHT CHECKS ---
clear
echo -e "${CYAN}${BOLD}---------------------------------------------------------------"
echo -e "       ✦  KIRBS MISSION CONTROL | USER: avsn17  ✧       "
echo -e "---------------------------------------------------------------${NC}"

if [[ ! -f "$WIDGET_BIN" || ! -f "$TIMER_BIN" ]]; then
    echo -e "❌ ${BOLD}[ERROR]${NC} Mission files not found. Check your directory."
    exit 1
fi

# Initialize the shared status file
echo "<( \" )> Preparing for ignition..." > "$WIDGET_LOG"

# --- LAUNCH SEQUENCE ---
# 1. Start Widget (Background & Silent)
python3 "$WIDGET_BIN" > /dev/null 2>&1 &
echo -e "🚀 ${BOLD}WIDGET:${NC} Initialized in background."

# 2. Start Main Timer (Foreground & Interactive)
echo -e "🚀 ${BOLD}TIMER:${NC}  Launching cockpit... Good luck, avsn17!"
echo -e "${CYAN}---------------------------------------------------------------${NC}"
python3 "$TIMER_BIN"

# --- POST-MISSION ---
# This part triggers your requested music autoplay behavior
echo -e "\n${PINK}🎶 Session End: Triggering Autoplay...${NC}"
# Terminal bell / Alert
printf '\a'
