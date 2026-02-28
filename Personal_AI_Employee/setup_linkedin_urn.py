#!/usr/bin/env python3
"""
LinkedIn Configuration Manager - Store LinkedIn Person URN
"""

import os
import json
from pathlib import Path

# Configuration file path
CONFIG_FILE = Path('linkedin_config.json')

def save_linkedin_urn(person_urn):
    """Save the LinkedIn Person URN to config file"""
    config = {
        'linkedin_person_urn': person_urn,
        'config_version': '1.0'
    }

    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"LinkedIn Person URN saved to {CONFIG_FILE}")
    print(f"URN: {person_urn}")

def load_linkedin_urn():
    """Load the LinkedIn Person URN from config file"""
    if not CONFIG_FILE.exists():
        return None

    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            return config.get('linkedin_person_urn')
    except Exception as e:
        print(f"Error loading LinkedIn config: {e}")
        return None

def main():
    print("LinkedIn Person URN Configuration")
    print("=" * 35)
    print()
    print("To use direct posting without r_liteprofile scope:")
    print("1. Find your LinkedIn Person ID from your profile URL")
    print("   Example: https://www.linkedin.com/in/JOHNCID")
    print("   Your ID would be: JOHNCID")
    print("2. The URN format will be: urn:li:person:JOHNCID")
    print()

    current_urn = load_linkedin_urn()
    if current_urn:
        print(f"Current URN: {current_urn}")
        response = input("Do you want to update it? (y/N): ")
        if response.lower() != 'y':
            print(f"Using existing URN: {current_urn}")
            return
        print()

    print("Enter your LinkedIn Person ID:")
    print("From URL like: https://www.linkedin.com/in/YOUR_ID_HERE")
    person_id = input("Your Person ID: ").strip()

    if not person_id:
        print("No Person ID provided. Exiting.")
        return

    person_urn = f"urn:li:person:{person_id}"
    print(f"Generated URN: {person_urn}")

    save_linkedin_urn(person_urn)
    print()
    print("Configuration complete! You can now use direct posting.")

if __name__ == '__main__':
    main()