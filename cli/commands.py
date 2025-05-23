# cli/commands.py
import argparse
import asyncio
from cli.devices import list_devices
from cli.connect import connect_to_device


def parse_args():
    parser = argparse.ArgumentParser(description="Tailscale CLI Tool")
    subparsers = parser.add_subparsers(dest='command', required=True,
                                       help='Available commands')

    # 'devices' command
    subparsers.add_parser('devices', help='List all devices')

    # Placeholder for future commands
    connect_parser = subparsers.add_parser('connect', help='ssh into a device')
    connect_parser.add_argument('device_name',
                                help='Name of the device to connect to')

    return parser.parse_args()


def run():
    args = parse_args()
    if args.command == 'devices':
        asyncio.run(list_devices())
    elif args.command == 'connect':
        asyncio.run(connect_to_device(args.device_name))
    else:
        print("Please provide a valid command. Use -h for help.")
