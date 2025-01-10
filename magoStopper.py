import sys
import ctypes
import psutil
import pygetwindow as gw
from pynput import mouse, keyboard
import time

# Funzione per verificare se il programma è in esecuzione come amministratore
def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin() != 0

# Funzione per riavviare lo script come amministratore se non lo è già
def run_as_admin():
    if not is_admin():
        # Usa il comando ShellExecute per eseguire lo script come amministratore
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, sys.argv[0], None, 1)
        sys.exit()

# Esegui questa funzione all'inizio del programma
run_as_admin()

# Titolo della finestra target
target_window_title = "Mago4"

# Nome del processo da terminare
target_process_name = "TbAppManager.exe"

# Timeout in secondi (5 minuti)
timeout = 5 * 60

# Variabile per registrare l'ultima interazione
last_interaction = time.time()

# Funzione per trovare il processo specifico
def find_process_by_name(name):
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if name.lower() in proc.info['name'].lower():
                return proc
        except psutil.NoSuchProcess:
            continue
    return None

# Funzione per ottenere i dettagli della finestra target
def get_target_window():
    for window in gw.getWindowsWithTitle(target_window_title):
        if target_window_title.lower() in window.title.lower():
            return window
    return None

# Funzione per verificare se il mouse è dentro la finestra target
def is_mouse_in_target_window(x, y):
    window = get_target_window()
    if window:
        left, top, right, bottom = window.left, window.top, window.right, window.bottom
        return left <= x <= right and top <= y <= bottom
    return False

# Callback per il mouse (aggiorna l'ultima interazione se la finestra è attiva e il clic è dentro la finestra target)
def on_click(x, y, _button, _pressed):
    global last_interaction
    active_window = gw.getActiveWindow()
    if active_window and target_window_title.lower() in active_window.title.lower() and is_mouse_in_target_window(x, y):
        last_interaction = time.time()

# Callback per la tastiera (aggiorna l'ultima interazione se la finestra è attiva)
def on_key_press(_key):
    global last_interaction
    active_window = gw.getActiveWindow()
    if active_window and target_window_title.lower() in active_window.title.lower():
        last_interaction = time.time()

# Funzione principale
def main():
    # Listener per mouse e tastiera
    global last_interaction
    mouse_listener = mouse.Listener(on_click=on_click)
    keyboard_listener = keyboard.Listener(on_press=on_key_press)

    mouse_listener.start()
    keyboard_listener.start()

    try:
        while True:
            # Controlla se la finestra target è aperta
            if get_target_window():
                # Controlla se il timeout è superato
                if time.time() - last_interaction > timeout:
                    print("Nessuna interazione per 5 minuti. Termino il processo...")
                    target_process = find_process_by_name(target_process_name)
                    if target_process:
                        target_process.terminate()
                        print(f"Processo {target_process.info['name']} terminato.")
                    else:
                        print(f"Processo {target_process_name} non trovato.")
                    # Dopo aver terminato il processo, resetta l'interazione
                    last_interaction = time.time()
            else:
                print("Finestra target non trovata. Continuo a controllare...")

            # Aspetta un secondo prima di ripetere il controllo
            time.sleep(1)

    except KeyboardInterrupt:
        print("Monitoraggio interrotto manualmente.")
    finally:
        mouse_listener.stop()
        keyboard_listener.stop()

# Esegui la funzione main
if __name__ == "__main__":
    main()
