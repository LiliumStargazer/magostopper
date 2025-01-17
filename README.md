# Process Monitor and Terminator

This project is a Python script that monitors user interactions with a specific window and terminates a target process if there is no interaction for a specified timeout period. The script ensures it runs with administrator privileges and uses various libraries to achieve its functionality.

## Features

- Monitors mouse and keyboard interactions within a specified window.
- Terminates a target process if there is no interaction for a specified timeout period.
- Ensures the script runs with administrator privileges.

## Requirements

- Python 3.6+
- Poetry (for dependency management)

## Dependencies

- `psutil`: For process management.
- `pygetwindow`: For window management.
- `pynput`: For mouse and keyboard event handling.

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```

2. **Install Poetry:**

    Follow the instructions on the [Poetry website](https://python-poetry.org/docs/#installation) to install Poetry.

3. **Install dependencies:**

    ```sh
    poetry install
    ```

## Usage

1. **Activate the virtual environment:**

    ```sh
    poetry shell
    ```

2. **Run the script:**

    ```sh
    python script_name.py
    ```

    Replace `script_name.py` with the actual name of your script file.

## Configuration

- **Target Window Title:** Modify the `target_window_title` variable in the script to match the title of the window you want to monitor.
- **Target Process Name:** Modify the `target_process_name` variable in the script to match the name of the process you want to terminate.
- **Timeout:** Modify the `timeout` variable in the script to set the desired timeout period (in seconds).

## How It Works

1. **Administrator Privileges:**
    - The script checks if it is running with administrator privileges. If not, it restarts itself with elevated privileges.

2. **Monitoring:**
    - The script uses `pynput` to listen for mouse and keyboard events.
    - It checks if the mouse clicks or key presses occur within the target window.
    - If there is no interaction within the specified timeout period, it terminates the target process.

3. **Process Termination:**
    - The script uses `psutil` to find and terminate the target process.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Acknowledgements

- [psutil](https://github.com/giampaolo/psutil)
- [pygetwindow](https://github.com/asweigart/PyGetWindow)
- [pynput](https://github.com/moses-palmer/pynput)
