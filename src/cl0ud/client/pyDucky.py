import os
import subprocess
import webbrowser
import time
import pyautogui

def execute_command(command):
    try:
        if command.startswith("DELAY"):
            delay_time = int(command.split()[1]) / 1000.0
            time.sleep(delay_time)
        elif command.startswith("STRING"):
            string_to_type = command.split("STRING ")[1].strip()
            pyautogui.typewrite(string_to_type)
        elif command.startswith("ENTER"):
            pyautogui.press('enter')
        elif command.startswith("GUI"):
            gui_key = command.split()[1].lower()
            if gui_key == "r":
                pyautogui.hotkey('win', 'r')
            elif gui_key == "l":
                pyautogui.hotkey('win', 'l')
            else:
                print("Unsupported GUI key:", gui_key)
        elif command.startswith("MENU"):
            pyautogui.press('menu')
        elif command.startswith("CTRL"):
            ctrl_key = command.split()[1].lower()
            pyautogui.hotkey('ctrl', ctrl_key)
        elif command.startswith("ALT"):
            alt_key = command.split()[1].lower()
            pyautogui.hotkey('alt', alt_key)
        elif command.startswith("SHIFT"):
            shift_key = command.split()[1].lower()
            pyautogui.hotkey('shift', shift_key)
        elif command.startswith("REM") or command.startswith("//"):
            # Ignore comments
            pass
        elif command.startswith("EXECUTE:"):
            file_path = command.split(":")[1].strip()
            subprocess.Popen(file_path, shell=True)
        elif command.startswith("BROWSE:"):
            url = command.split(":")[1].strip()
            webbrowser.open(url)
        elif command.startswith("CUSTOM:"):
            custom_command = command.split(":")[1].strip()
            # Add more custom command handling here as needed
        else:
            # Invalid command
            print("Invalid command:", command)
    except Exception as e:
        print("Error executing command:", e)

# def execute_payload():
#     current_directory = os.path.dirname(os.path.realpath(__file__))
#     file_path = os.path.join(current_directory, 'payload.txt')
#     with open(file_path, 'r') as file:
#         for line in file:
#             execute_command(line.strip())

def execute_payload():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_directory, 'payload.txt')
    if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r') as file:
            for line in file:
                execute_command(line.strip())
    else:
        print("Payload file is empty or does not exist.")

if __name__ == "__main__":
    execute_payload()

