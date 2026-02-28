#!/usr/bin/env python3
"""
Send WhatsApp message to Karen on +923170027046
"""
import os
import json
import sys
from datetime import datetime
from pathlib import Path

def send_whatsapp_to_karen():
    """Create a WhatsApp message file for Karen with the specific number"""

    # Use the specific number provided
    karen_number = "+923170027046"

    # Create a WhatsApp message file in Needs_Action folder
    vault_path = os.environ.get('VAULT_PATH', 'AI_Employee_Vault')
    needs_action_path = Path(vault_path) / 'Needs_Action'
    needs_action_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'WHATSAPP_KAREN_{timestamp}.md'
    filepath = needs_action_path / filename

    content = f"""---
type: whatsapp
from: dashboard_test
to: {karen_number}
priority: high
status: pending
created: {datetime.now().isoformat()}
source: karen_whatsapp_test
---

# WhatsApp Message to Karen - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This is a WhatsApp message to Karen on {karen_number}.

## Message Details
- **To**: {karen_number}
- **Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Test Type**: Direct communication to Karen

## Message Content
Hello Karen,

This is a test message sent directly to your number +923170027046 to verify WhatsApp communication functionality.

The AI Employee Dashboard can send direct messages to your WhatsApp number via the orchestrator system.

Best regards,
AI Employee Dashboard System

---
*Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Created WhatsApp message for Karen: {filepath}")
    print(f"📞 Number: {karen_number}")
    print(f"🔄 The orchestrator will process this file and send the message")

    return filepath

def main():
    print("="*60)
    print("SEND WHATSAPP TO KAREN")
    print("="*60)

    print("📱 Attempting to send WhatsApp message to Karen...")
    print("📞 Number: +923170027046")

    whatsapp_file = send_whatsapp_to_karen()

    print("\n" + "="*60)
    print("SUCCESS! 🎉")
    print("="*60)
    print(f"📁 WhatsApp message file created: {whatsapp_file}")
    print("🔄 The orchestrator will process this and send the message to Karen")
    print("\n📋 To send the message immediately, run:")
    print("   python orchestrator.py")

if __name__ == "__main__":
    main()