#!/bin/bash

while true; do
    # Get number of monitors connected
    monitor_count=$(xrandr -q | grep ' connected' | wc -l)
    
    # Get info about connected USB devices
    lsusb_output=$(lsusb -v)
    
    # Check for Rubber Ducky device by VID and PID
    if echo "$lsusb_output" | grep -q "idVendor.*0x1b4f" && echo "$lsusb_output" | grep -q "idProduct.*0x9205"; then
        # Deactivate USB ports
        echo "Disabling USB ports"
        echo '<bus>-1' | sudo tee /sys/bus/usb/drivers/usb/unbind
        echo '<bus>-1' | sudo tee /sys/bus/usb/drivers/usb/unbind
        echo '<bus>-1' | sudo tee /sys/bus/usb/drivers/usb/unbind
        echo '<bus>-1' | sudo tee /sys/bus/usb/drivers/usb/unbind
    fi
    
    # Check for HID device by class and subclass
    if echo "$lsusb_output" | grep -q "bInterfaceClass.*03" && echo "$lsusb_output" | grep -q "bInterfaceSubClass.*01"; then
        # Deactivate USB ports
        echo "Disabling USB ports"
        echo '<bus>-1' | sudo tee /sys/bus/usb/drivers/usb/unbind
        echo '<bus>-1' | sudo tee /sys/bus/usb/drivers/usb/unbind
        echo '<bus>-1' | sudo tee /sys/bus/usb/drivers/usb/unbind
        echo '<bus>-1' | sudo tee /sys/bus/usb/drivers/usb/unbind
    fi
    
    # Check for change in number of monitors connected
    new_monitor_count=$(xrandr -q | grep ' connected' | wc -l)
    if [[ "$new_monitor_count" != "$monitor_count" ]]; then
        # Activate USB ports
        echo "Enabling USB ports"
        echo '<bus>-1' | sudo tee /sys/bus/usb/drivers/usb/bind
        echo '<bus>-1' | sudo tee /sys/bus/usb/drivers/usb/bind
        echo '<bus>-1' | sudo tee /sys/bus/usb/drivers/usb/bind
        echo '<bus>-1' | sudo tee /sys/bus/usb/drivers/usb/bind
    fi
done
