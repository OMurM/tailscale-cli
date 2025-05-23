# cli/connect.py

import subprocess
from cli.devices import fetch_devices


async def connect_to_device(target):
    devices = await fetch_devices()
    if not devices:
        print("No devices found.")
        return

    # Search for the device by name
    target_device = next(
        (
            device for device in devices
            if device.get('name') == target or target in device.get(
                'addresses', []
            )
        ),
        None
    )

    if not target_device:
        print(f"Device '{target}' not found.")
        return
    # This dosnt work devices are always offline if this is active IDK wtf
    # Check if the device is online
    # if not target_device.get('online', False):
    #    print(f"Device '{target}' is currently offline.")
    #    return

    # Get the device's IP address
    addresses = target_device.get('addresses', [])
    if not addresses:
        print(f"No IP addresses found for device '{target}'.")
        return
    ip_address = addresses[0]  # Use the first IP address

    default_username = "oscar"

    def try_ssh(username):
        try:
            result = subprocess.run(['ssh', f'{username}@{ip_address}'])
            return result.returncode == 0
        except Exception as e:
            print(f"Failed to initiate ssh connection error: {e}")
            return False

    if try_ssh(default_username):
        return
    while True:
        username = input("Ssh connection failed. Please enter username to try: ").strip()
        if not username:
            print("username cannot be empty. Try again")
            continue
        if try_ssh(username):
            break
        else:
            print("Ssh connection failed with username, try again or Ctrl+C to exit")
