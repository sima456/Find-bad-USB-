import os
import subprocess
import smtplib

# Configuration file containing allowed USB devices
ALLOWED_USB_FILE = "allowed_usb.txt"

# Email settings
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "your-email@gmail.com"
SMTP_PASSWORD = "your-email-password"
ALERT_EMAIL = "recipient-email@example.com"


def get_allowed_usb():
    # Read configuration file and return list of allowed USB IDs
    allowed_usb = []
    with open(ALLOWED_USB_FILE, "r") as f:
        for line in f:
            vid, pid = line.strip().split(":")
            allowed_usb.append((vid, pid))
    return allowed_usb


def send_alert_email():
    # Send alert email to recipient
    subject = "Unauthorized USB detected"
    body = "An unknown USB device was detected and disabled."
    message = f"Subject: {subject}\n\n{body}"
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, ALERT_EMAIL, message)


def disable_usb_device(bus, device):
    # Disable USB device by unbinding it from kernel driver
    device_path = f"/sys/bus/usb/devices/{bus}/{device}/"
    driver_path = os.path.realpath(f"{device_path}/driver")
    driver_name = os.path.basename(driver_path)
    subprocess.run(["sudo", "sh", "-c", f"echo {bus}-{device} > {driver_path}/unbind"])
    print(f"Disabled USB device {bus}-{device} using driver {driver_name}")
    send_alert_email()


def main():
    # Get list of allowed USB IDs from configuration file
    allowed_usb = get_allowed_usb()

    # Monitor USB devices
    while True:
        # Get list of connected USB devices
        lsusb_output = subprocess.check_output(["lsusb", "-v"]).decode()
        devices = lsusb_output.split("\n\n")
        for device in devices:
            if not device:
                continue
            lines = device.split("\n")
            vid = lines[2].split()[-1]
            pid = lines[3].split()[-1]
            bus, device_id = lines[0].split()[-3:-1]
            if (vid, pid) not in allowed_usb:
                # Disable unauthorized USB device
                disable_usb_device(bus, device_id)


if __name__ == "__main__":
    main()
