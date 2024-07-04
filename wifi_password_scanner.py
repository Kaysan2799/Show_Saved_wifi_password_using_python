import subprocess
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import threading

def get_active_wifi_ssid():
    try:
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces'], stderr=subprocess.STDOUT).decode('utf-8').split('\n')
        ssid_line = [line.split(':')[1].strip() for line in results if "SSID" in line and "BSSID" not in line]
        return ssid_line[0] if ssid_line else None
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode('utf-8')}"

def get_wifi_password(ssid):
    try:
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', f'name={ssid}', 'key=clear'], stderr=subprocess.STDOUT).decode('utf-8').split('\n')
        password_line = [line.split(':')[1].strip() for line in results if "Key Content" in line]
        return password_line[0] if password_line else "Cannot retrieve password."
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode('utf-8')}"

def get_saved_wifi_profiles():
    try:
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'], stderr=subprocess.STDOUT).decode('utf-8').split('\n')
        profiles = [line.split(':')[1].strip() for line in results if "All User Profile" in line]
        return profiles
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode('utf-8')}"

def save_password_to_file():
    with open('passwords.txt', 'a') as file:
        file.write(result_text.get('1.0', tk.END))

def show_active_wifi_password():
    progress_bar.start()
    result_text.delete('1.0', tk.END)  # Clear previous text

    def fetch_active_wifi():
        active_ssid = get_active_wifi_ssid()
        if active_ssid and not active_ssid.startswith("Error"):
            password = get_wifi_password(active_ssid)
            result_text.insert(tk.END, f"Active WiFi Network: {active_ssid}\nPassword: {password}\n")
            save_button.config(state=tk.NORMAL)
            clear_button.config(state=tk.NORMAL)
        elif active_ssid:
            result_text.insert(tk.END, active_ssid)  # Display error message
        else:
            result_text.insert(tk.END, "No active WiFi network found.")

        progress_bar.stop()

    threading.Thread(target=fetch_active_wifi).start()

def show_saved_wifi_passwords():
    progress_bar.start()
    result_text.delete('1.0', tk.END)  # Clear previous text

    def fetch_saved_wifi():
        saved_profiles = get_saved_wifi_profiles()
        if isinstance(saved_profiles, list) and saved_profiles:
            for profile in saved_profiles:
                password = get_wifi_password(profile)
                result_text.insert(tk.END, f"Saved WiFi Network: {profile}\nPassword: {password}\n\n")
            save_button.config(state=tk.NORMAL)
            clear_button.config(state=tk.NORMAL)
        elif isinstance(saved_profiles, str):
            result_text.insert(tk.END, saved_profiles)  # Display error message
        else:
            result_text.insert(tk.END, "No saved WiFi networks found.")

        progress_bar.stop()

    threading.Thread(target=fetch_saved_wifi).start()

def clear_passwords():
    result_text.delete('1.0', tk.END)
    save_button.config(state=tk.DISABLED)
    clear_button.config(state=tk.DISABLED)

# Create the main window
root = tk.Tk()
root.title("WiFi Password Retrieval")
root.geometry("1200x810")

# Apply a style to the widgets
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 14), padding=10)
style.configure('Small.TButton', font=('Helvetica', 12), padding=5)
style.configure('TLabel', font=('Helvetica', 20), padding=10)
style.configure('TFrame', padding=10)
style.configure('TScrolledText', font=('Helvetica', 14))

# Create and pack widgets
frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

title_label = ttk.Label(frame, text="WiFi Password Retrieval", font=('Helvetica', 20))
title_label.grid(row=0, column=0, columnspan=2, pady=20)

active_wifi_button = ttk.Button(frame, text="Scan Active WiFi", command=show_active_wifi_password, style='TButton')
active_wifi_button.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

saved_wifi_button = ttk.Button(frame, text="Scan Saved WiFi", command=show_saved_wifi_passwords, style='TButton')
saved_wifi_button.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

save_button = ttk.Button(frame, text="Save Passwords", command=save_password_to_file, state=tk.DISABLED, style='Small.TButton')
save_button.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

clear_button = ttk.Button(frame, text="Clear Passwords", command=clear_passwords, state=tk.DISABLED, style='Small.TButton')
clear_button.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

progress_bar = ttk.Progressbar(frame, orient='horizontal', mode='indeterminate', length=400)
progress_bar.grid(row=3, column=0, columnspan=2, pady=10)

result_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=100, height=20, font=('Helvetica', 14))
result_text.grid(row=4, column=0, columnspan=2, padx=20, pady=20)

# Start the application
root.mainloop()
