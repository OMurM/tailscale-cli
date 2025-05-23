# cli/devices.py

import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('TAILSCALE_API_KEY')
TAILNET = os.getenv('TAILNET_NAME')

if not TAILNET:
    raise ValueError("TAILNET_NAME environment variable not set. Please set it in your .env file.")

API_BASE_URL = "https://api.tailscale.com/api/v2"


async def fetch_devices():
    url = f'{API_BASE_URL}/tailnet/{TAILNET}/devices'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Accept': 'application/json'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('devices', [])
            else:
                print(f"Failed to fetch devices. Status code: {response.status}")
                error_message = await response.text()
                print(f"Error message: {error_message}")
                return []


async def list_devices():
    devices = await fetch_devices()
    if not devices:
        print("No devices found.")
        return
    for device in devices:
        name = device.get('name', 'N/A')
        addresses = device.get('addresses', [])
        last_seen = device.get('lastSeen', 'N/A')
        device_os = device.get('os', 'N/A')
        device_id = device.get('id', 'N/A')
        print(f"Name: {name}")
        print(f"Device id: {device_id}")
        print(f"Addresses: {', '.join(addresses)}")
        print(f"Last Seen: {last_seen}")
        print(f"Device OS: {device_os}")
        print("-" * 40)


async def get_device_details(device_id):
    url = f"{API_BASE_URL}/device/{device_id}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Failed to fetch device details. Status code: {response.status}")
                error_message = await response.text()
                print(f"Error message: {error_message}")
                return None
