# cli/devices.py
import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('TAILSCALE_API_KEY')
TAILNET = os.getenv('TAILNET_NAME')


async def list_devices():
    url = f'https://api.tailscale.com/api/v2/tailnet/{TAILNET}/devices'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Accept': 'application/json'
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                devices = data.get('devices', [])
                if not devices:
                    print("No devices found.")
                    return
                for device in devices:
                    name = device.get('name', 'N/A')
                    addresses = device.get('addresses', [])
                    last_seen = device.get('lastSeen', 'N/A')
                    print(f"Name: {name}")
                    print(f"Addresses: {', '.join(addresses)}")
                    print(f"Last Seen: {last_seen}")
                    print("-" * 40)
            else:
                print(f"Failed to fetch devices. Status code: {response.status}")
                error_message = await response.text()
                print(f"Error message: {error_message}")
