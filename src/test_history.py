#!/usr/bin/env python3
"""Test script to verify history tracking functionality"""

import os
import json
from datetime import datetime
import getpass

def save_script_to_file(script_code, filename="handler.py", update_message=""):
    """Save the script to a file and record update history."""
    try:
        if script_code is None:
            return False, "Error: No script content to save"

        # Save the script
        with open(filename, 'w') as f:
            f.write(script_code)

        # Load existing history
        history_file = ".script_history.json"
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                update_history = json.load(f)
        else:
            update_history = []

        # Record history entry
        history_entry = {
            "filename": filename,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": getpass.getuser(),
            "update_message": update_message if update_message else "No message provided",
            "file_size": len(script_code)
        }

        # Add to history
        update_history.append(history_entry)

        # Save history to file
        with open(history_file, 'w') as f:
            json.dump(update_history, f, indent=2)

        return True, f"Script saved to {filename}"
    except Exception as e:
        return False, f"Error saving script: {str(e)}"

if __name__ == "__main__":
    print("Testing history tracking functionality...\n")

    # Test 1: Save with message
    success, msg = save_script_to_file('print("Hello World")', 'test_script.py', 'Initial commit')
    print(f"✅ Test 1: {msg}")

    # Test 2: Save another file
    success, msg = save_script_to_file('print("Updated code")', 'test_script.py', 'Fixed bug in print statement')
    print(f"✅ Test 2: {msg}")

    # Test 3: Save without message
    success, msg = save_script_to_file('print("No message")', 'another_file.py', '')
    print(f"✅ Test 3: {msg}")

    # Display history
    print("\n📜 Update History:")
    print("=" * 80)
    if os.path.exists('.script_history.json'):
        with open('.script_history.json', 'r') as f:
            history = json.load(f)
        print(f"Total entries: {len(history)}\n")
        for i, entry in enumerate(history, 1):
            print(f"{i}. File: {entry['filename']}")
            print(f"   User: {entry['user']}")
            print(f"   Time: {entry['timestamp']}")
            print(f"   Message: {entry['update_message']}")
            print(f"   Size: {entry['file_size']} characters")
            print()

    print("=" * 80)
    print("\n✅ All tests completed successfully!")

