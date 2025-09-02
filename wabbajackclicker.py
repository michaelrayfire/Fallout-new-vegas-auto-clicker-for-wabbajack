import pyautogui
import time
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

# Global variables
running = False
button_image_path = ""
deadzone_image_path = ""
confidence = 0.7

# Function to run the auto-clicker
def auto_clicker():
    global running
    while running:
        try:
            button_location = pyautogui.locateCenterOnScreen(button_image_path, confidence=confidence)
            if button_location:
                log(f"Found button at {button_location}, clicking...")
                pyautogui.click(button_location)

                # Move to dead zone
                deadzone_location = pyautogui.locateCenterOnScreen(deadzone_image_path, confidence=0.9)
                if deadzone_location:
                    pyautogui.moveTo(deadzone_location[0], deadzone_location[1], duration=0.3)
                else:
                    pyautogui.moveRel(0, -50, duration=0.3)

                time.sleep(1)  # avoid double-clicking
            else:
                time.sleep(0.5)
        except pyautogui.ImageNotFoundException:
            time.sleep(0.5)

# Helper function to log messages to the GUI
def log(message):
    log_text.configure(state='normal')
    log_text.insert(tk.END, message + "\n")
    log_text.see(tk.END)
    log_text.configure(state='disabled')

# GUI button callbacks
def browse_button_image():
    global button_image_path
    path = filedialog.askopenfilename(title="Select Slow Download Button Image", filetypes=[("PNG Files", "*.png")])
    if path:
        button_image_path = path
        button_label.config(text=os.path.basename(path))

def browse_deadzone_image():
    global deadzone_image_path
    path = filedialog.askopenfilename(title="Select Dead Zone Image", filetypes=[("PNG Files", "*.png")])
    if path:
        deadzone_image_path = path
        deadzone_label.config(text=os.path.basename(path))

def start_clicker():
    global running
    if not button_image_path or not deadzone_image_path:
        messagebox.showerror("Error", "Please select both images first!")
        return
    running = True
    threading.Thread(target=auto_clicker, daemon=True).start()
    log("Auto-clicker started.")

def stop_clicker():
    global running
    running = False
    log("Auto-clicker stopped.")

# Tkinter GUI
root = tk.Tk()
root.title("Wabbajack Auto-Clicker")
root.geometry("500x400")

# Browse buttons
tk.Button(root, text="Select Slow Download Button", command=browse_button_image).pack(pady=5)
button_label = tk.Label(root, text="No file selected")
button_label.pack()

tk.Button(root, text="Select Dead Zone Image", command=browse_deadzone_image).pack(pady=5)
deadzone_label = tk.Label(root, text="No file selected")
deadzone_label.pack()

# Start/Stop buttons
tk.Button(root, text="Start Auto-Clicker", command=start_clicker, bg="green", fg="white").pack(pady=10)
tk.Button(root, text="Stop Auto-Clicker", command=stop_clicker, bg="red", fg="white").pack(pady=5)

# Log box
log_text = tk.Text(root, height=10, state='disabled')
log_text.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)

root.mainloop()
