# cli/commands.py
import argparse
import asyncio
from cli.devices import list_devices


def parse_args():
    parser = argparse.ArgumentParser(description="Tailscale CLI Tool")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # 'devices' command
    subparsers.add_parser('devices', help='List all devices')

    # Placeholder for future commands
    subparsers.add_parser('ssh', help='SSH into a device (coming soon)')

    return parser.parse_args()


def run():
    args = parse_args()
    if args.command == 'devices':
        asyncio.run(list_devices())
    elif args.command == 'ssh':
        print("SSH functionality is under development.")
    else:
        print("Please provide a valid command. Use -h for help.")

