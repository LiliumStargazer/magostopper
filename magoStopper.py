import base64

code = base64.b64encode(b"""
import sys
import ctypes
import psutil
import pygetwindow as gw
from pynput import mouse, keyboard
import time

# Function to check if the program is running as an administrator
def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin() != 0

# Function to restart the script as an administrator if it is not already
def run_as_admin():
    if not is_admin():
        # Use ShellExecute to run the script as an administrator
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, sys.argv[0], None, 1)
        sys.exit()

# Run this function at the start of the program
run_as_admin()

# Target window title
target_window_title = "Mago4"

# Name of the process to terminate
target_process_name = "TbAppManager.exe"

# Timeout in seconds (5 minutes)
timeout = 5 * 60

# Variable to record the last interaction
last_interaction = time.time()

# Function to find the specific process by name
def find_process_by_name(name):
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if name.lower() in proc.info['name'].lower():
                return proc
        except psutil.NoSuchProcess:
            continue
    return None

# Function to get the details of the target window
def get_target_window():
    for window in gw.getWindowsWithTitle(target_window_title):
        if target_window_title.lower() in window.title.lower():
            return window
    return None

# Function to check if the mouse is inside the target window
def is_mouse_in_target_window(x, y):
    window = get_target_window()
    if window:
        left, top, right, bottom = window.left, window.top, window.right, window.bottom
        return left <= x <= right and top <= y <= bottom
    return False

# Mouse callback (updates the last interaction if the window is active and the click is inside the target window)
def on_click(x, y, _button, _pressed):
    global last_interaction
    active_window = gw.getActiveWindow()
    if active_window and target_window_title.lower() in active_window.title.lower() and is_mouse_in_target_window(x, y):
        last_interaction = time.time()

# Keyboard callback (updates the last interaction if the window is active)
def on_key_press(_key):
    global last_interaction
    active_window = gw.getActiveWindow()
    if active_window and target_window_title.lower() in active_window.title.lower():
        last_interaction = time.time()

# Main function
def main():
    # Mouse and keyboard listeners
    global last_interaction
    mouse_listener = mouse.Listener(on_click=on_click)
    keyboard_listener = keyboard.Listener(on_press=on_key_press)

    mouse_listener.start()
    keyboard_listener.start()

    try:
        while True:
            # Check if the target window is open
            if get_target_window():
                # Check if the timeout is exceeded
                if time.time() - last_interaction > timeout:
                    print("No interaction for 5 minutes. Terminating the process...")
                    target_process = find_process_by_name(target_process_name)
                    if target_process:
                        target_process.terminate()
                        print(f"Process {target_process.info['name']} terminated.")
                    else:
                        print(f"Process {target_process_name} not found.")
                    # After terminating the process, reset the interaction
                    last_interaction = time.time()
            else:
                print("Target window not found. Continuing to check...")

            # Wait a second before repeating the check
            time.sleep(1)

    except KeyboardInterrupt:
        print("Monitoring manually interrupted.")
    finally:
        mouse_listener.stop()
        keyboard_listener.stop()

# Run the main function
if __name__ == "__main__":
    main()
""")

exec(base64.b64decode(code))