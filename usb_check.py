import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import time
import platform

class USBMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("USB Geräte Monitor")

        self.label = ttk.Label(root, text="Angeschlossene USB-Geräte:", font=("Arial", 14))
        self.label.pack(pady=10)

        self.device_listbox = tk.Listbox(root, width=50, height=15)
        self.device_listbox.pack(pady=10)

        self.existing_devices = self.get_connected_devices()
        self.update_device_listbox(self.existing_devices)

        self.thread = threading.Thread(target=self.monitor_devices)
        self.thread.daemon = True
        self.thread.start()

    def get_connected_devices(self):
        if platform.system() == 'Linux':
            try:
                result = subprocess.run(['lsusb'], stdout=subprocess.PIPE)
                devices = result.stdout.decode('utf-8', errors='ignore').strip().split('\n')
                return devices
            except Exception as e:
                print(f"Error getting USB devices: {e}")
                return []
        elif platform.system() == 'Windows':
            try:
                result = subprocess.run(['wmic', 'path', 'Win32_USBHub', 'get', 'DeviceID,Description'], stdout=subprocess.PIPE)
                devices = result.stdout.decode('utf-8', errors='ignore').strip().split('\n')[1:]
                devices = [device.strip() for device in devices if device.strip()]
                return devices
            except Exception as e:
                print(f"Error getting USB devices: {e}")
                return []

    def update_device_listbox(self, devices):
        self.device_listbox.delete(0, tk.END)
        for device in devices:
            self.device_listbox.insert(tk.END, device)

    def monitor_devices(self):
        while True:
            time.sleep(1)
            current_devices = self.get_connected_devices()
            if set(current_devices) != set(self.existing_devices):
                self.existing_devices = current_devices
                self.update_device_listbox(current_devices)

if __name__ == "__main__":
    root = tk.Tk()
    usb_monitor = USBMonitor(root)
    root.mainloop()
