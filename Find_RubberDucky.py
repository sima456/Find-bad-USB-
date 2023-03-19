import subprocess
import platform
import re
import time

def get_usb_info():
    if platform.system() == "Linux":
        # Get info about connected USB devices on Linux using lsusb
        result = subprocess.run(["lsusb", "-v"], stdout=subprocess.PIPE)
        return result.stdout.decode()
    elif platform.system() == "Windows":
        # Get info about connected USB devices on Windows using WMIC
        result = subprocess.run(["WMIC", "path", "Win32_USBControllerDevice", "get", "Dependent"], stdout=subprocess.PIPE)
        return result.stdout.decode()

def disable_usb():
    if platform.system() == "Linux":
        # Deactivate USB ports on Linux by unbinding USB driver
        subprocess.run(["sudo", "sh", "-c", "echo '<bus>-1' > /sys/bus/usb/drivers/usb/unbind"])
    elif platform.system() == "Windows":
        # Deactivate USB ports on Windows by disabling the corresponding device
        result = subprocess.run(["WMIC", "path", "Win32_USBHub", "where", "status='OK'", "call", "disable"], stdout=subprocess.PIPE)
        print(result.stdout.decode())

def enable_usb():
    if platform.system() == "Linux":
        # Activate USB ports on Linux by binding USB driver
        subprocess.run(["sudo", "sh", "-c", "echo '<bus>-1' > /sys/bus/usb/drivers/usb/bind"])
    elif platform.system() == "Windows":
        # Activate USB ports on Windows by enabling the corresponding device
        result = subprocess.run(["WMIC", "path", "Win32_USBHub", "where", "status='Error'", "call", "enable"], stdout=subprocess.PIPE)
        print(result.stdout.decode())

def check_usb():
    usb_info = get_usb_info()

    # Check for Rubber Ducky device by VID and PID
    if re.search(r"idVendor.*0x1b4f.*idProduct.*0x9205", usb_info):
        return True
    
    # Check for HID device by class and subclass
    if re.search(r"bInterfaceClass.*03.*bInterfaceSubClass.*01", usb_info):
        return True

    return False

def main():
    initial_monitor_count = -1
    while True:
        # Get number of monitors connected
        if platform.system() == "Linux":
            result = subprocess.run(["xrandr", "-q"], stdout=subprocess.PIPE)
            monitor_count = len(re.findall(r"\bconnected\b", result.stdout.decode()))
        elif platform.system() == "Windows":
            result = subprocess.run(["powershell", "-command", "(Get-WmiObject -Class Win32_DesktopMonitor).Count"], stdout=subprocess.PIPE)
            monitor_count = int(result.stdout.decode())

        # Check for USB device and deactivate USB ports if found
        if check_usb():
            print("Disabling USB ports")
            disable_usb()
        else:
            # Check for change in number of monitors connected
            if initial_monitor_count == -1:
                initial_monitor_count = monitor_count
            elif monitor_count != initial_monitor_count:
                print("Enabling USB ports")
                enable_usb()
                initial_monitor_count = monitor_count

        time.sleep(1)

if __name__ == "__main__":
    main()
