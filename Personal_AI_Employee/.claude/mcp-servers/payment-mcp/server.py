"""
Payment MCP Server for Personal AI Employee

Handles payment processing, transaction management, and financial operations
"""
import asyncio
import json
import logging
from typing import Dict, Any, List
from pathlib import Path
import hashlib
import uuid
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PaymentMCPServer:
    def __init__(self):
        self.capabilities = {
            "name": "payment-mcp",
            "version": "1.0.0",
            "description": "Payment processing and financial operations for transactions, invoicing, and accounting",
            "resources": [
                {
                    "type": "payment_action",
                    "name": "process_payment",
                    "description": "Process a payment transaction"
                },
                {
                    "type": "payment_action",
                    "name": "create_invoice",
                    "description": "Create an invoice for a customer"
                },
                {
                    "type": "payment_action",
                    "name": "check_balance",
                    "description": "Check account balance"
                },
                {
                    "type": "payment_action",
                    "name": "generate_receipt",
                    "description": "Generate a payment receipt"
                },
                {
                    "type": "payment_action",
                    "name": "transfer_funds",
                    "description": "Transfer funds between accounts"
                },
                {
                    "type": "payment_action",
                    "name": "schedule_payment",
                    "description": "Schedule a future payment"
                }
            ]
        }

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP requests"""
        try:
            method = request.get("method")

            if method == "mcp/discover":
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {
                        "name": self.capabilities["name"],
                        "version": self.capabilities["version"],
                        "description": self.capabilities["description"],
                        "resources": self.capabilities["resources"]
                    }
                }

            elif method == "process_payment":
                return await self.process_payment(request)
            elif method == "create_invoice":
                return await self.create_invoice(request)
            elif method == "check_balance":
                return await self.check_balance(request)
            elif method == "generate_receipt":
                return await self.generate_receipt(request)
            elif method == "transfer_funds":
                return await self.transfer_funds(request)
            elif method == "schedule_payment":
                return await self.schedule_payment(request)
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {
                        "code": -32601,
                        "message": f"Method {method} not found"
                    }
                }

        except Exception as e:
            logger.error(f"Error handling request: {e}")
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }

    async def process_payment(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process a payment transaction"""
        params = request.get("params", {})
        amount = params.get("amount", 0)
        currency = params.get("currency", "USD")
        recipient = params.get("recipient", "")
        description = params.get("description", "")
        payment_method = params.get("payment_method", "credit_card")
        approval_required = params.get("approval_required", True)

        # Simulate payment processing (in real implementation, would use payment gateway)
        transaction_id = str(uuid.uuid4())

        # Log the transaction attempt
        logger.info(f"Processing payment: ${amount} to {recipient}")

        # In production, this would call a real payment processor
        # For now, simulate the result
        result = {
            "status": "pending_approval" if approval_required else "success",
            "transaction_id": transaction_id,
            "amount": amount,
            "currency": currency,
            "recipient": recipient,
            "description": description,
            "payment_method": payment_method,
            "timestamp": datetime.now().isoformat(),
            "message": f"Payment of ${amount} to {recipient} initiated"
        }

        # Log the payment to the vault for audit trail
        self.log_payment_activity("payment_initiated", result)

        # If approval required, create approval request
        if approval_required:
            self.create_approval_request(result)

        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": result
        }

    async def create_invoice(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Create an invoice for a customer"""
        params = request.get("params", {})
        customer = params.get("customer", "")
        amount = params.get("amount", 0)
        currency = params.get("currency", "USD")
        description = params.get("description", "")
        due_date = params.get("due_date", "")
        items = params.get("items", [])

        # Simulate invoice creation
        invoice_id = f"INV-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"

        logger.info(f"Creating invoice: {invoice_id} for {customer}")

        invoice_data = {
            "invoice_id": invoice_id,
            "customer": customer,
            "amount": amount,
            "currency": currency,
            "description": description,
            "due_date": due_date,
            "items": items,
            "status": "created",
            "created_at": datetime.now().isoformat(),
            "message": f"Invoice {invoice_id} created for {customer}"
        }

        # Log the invoice creation to the vault
        self.log_payment_activity("invoice_created", invoice_data)

        # Save invoice to vault
        self.save_invoice(invoice_data)

        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": invoice_data
        }

    async def check_balance(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Check account balance"""
        params = request.get("params", {})
        account_id = params.get("account_id", "")

        # Simulate balance check (in real implementation, would call banking API)
        balance = {
            "account_id": account_id,
            "balance": 12500.50,  # Simulated balance
            "currency": "USD",
            "available_balance": 12400.00,
            "pending_transactions": 100.50,
            "last_updated": datetime.now().isoformat(),
            "message": f"Balance retrieved for account {account_id}"
        }

        # Log the balance check to the vault
        self.log_payment_activity("balance_check", balance)

        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": balance
        }

    async def generate_receipt(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a payment receipt"""
        params = request.get("params", {})
        transaction_id = params.get("transaction_id", "")
        customer = params.get("customer", "")
        amount = params.get("amount", 0)
        description = params.get("description", "")

        # Simulate receipt generation
        receipt_data = {
            "receipt_id": f"RCT-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}",
            "transaction_id": transaction_id,
            "customer": customer,
            "amount": amount,
            "description": description,
            "issued_at": datetime.now().isoformat(),
            "status": "generated",
            "receipt_url": f"https://receipts.example.com/{transaction_id}",
            "message": f"Receipt generated for transaction {transaction_id}"
        }

        # Log the receipt generation to the vault
        self.log_payment_activity("receipt_generated", receipt_data)

        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": receipt_data
        }

    async def transfer_funds(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Transfer funds between accounts"""
        params = request.get("params", {})
        from_account = params.get("from_account", "")
        to_account = params.get("to_account", "")
        amount = params.get("amount", 0)
        description = params.get("description", "")
        approval_required = params.get("approval_required", True)

        # Simulate fund transfer
        transfer_id = str(uuid.uuid4())

        logger.info(f"Transferring ${amount} from {from_account} to {to_account}")

        transfer_data = {
            "transfer_id": transfer_id,
            "from_account": from_account,
            "to_account": to_account,
            "amount": amount,
            "description": description,
            "status": "pending_approval" if approval_required else "success",
            "timestamp": datetime.now().isoformat(),
            "message": f"Transfer of ${amount} from {from_account} to {to_account} initiated"
        }

        # Log the transfer to the vault
        self.log_payment_activity("transfer_initiated", transfer_data)

        # If approval required, create approval request
        if approval_required:
            self.create_approval_request(transfer_data, action_type="transfer")

        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": transfer_data
        }

    async def schedule_payment(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Schedule a future payment"""
        params = request.get("params", {})
        amount = params.get("amount", 0)
        recipient = params.get("recipient", "")
        scheduled_date = params.get("scheduled_date", "")
        description = params.get("description", "")
        recurrence = params.get("recurrence", "once")  # once, daily, weekly, monthly

        # Simulate payment scheduling
        schedule_id = str(uuid.uuid4())

        logger.info(f"Scheduling payment: ${amount} to {recipient} on {scheduled_date}")

        schedule_data = {
            "schedule_id": schedule_id,
            "amount": amount,
            "recipient": recipient,
            "scheduled_date": scheduled_date,
            "description": description,
            "recurrence": recurrence,
            "status": "scheduled",
            "created_at": datetime.now().isoformat(),
            "message": f"Payment scheduled for {scheduled_date} to {recipient}"
        }

        # Log the scheduled payment to the vault
        self.log_payment_activity("payment_scheduled", schedule_data)

        # Save scheduled payment to vault
        self.save_scheduled_payment(schedule_data)

        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": schedule_data
        }

    def log_payment_activity(self, action: str, data: Dict[str, Any]):
        """Log payment activity to the vault"""
        import os
        from datetime import datetime

        # Get vault path from environment or default
        vault_path = os.environ.get('VAULT_PATH', '../AI_Employee_Vault')
        logs_dir = Path(vault_path) / 'Logs'
        logs_dir.mkdir(parents=True, exist_ok=True)

        # Create log entry
        log_entry = f"[{datetime.now().strftime('%H:%M:%S')}] PAYMENT_MCP: {action.upper()} - {json.dumps(data, default=str)[:100]}...\n"

        # Write to today's log file
        log_file = logs_dir / f"{datetime.now().strftime('%Y-%m-%d')}.txt"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

    def create_approval_request(self, transaction_data: Dict[str, Any], action_type: str = "payment"):
        """Create an approval request for sensitive actions"""
        import os
        from datetime import datetime, timedelta

        # Get vault path from environment or default
        vault_path = os.environ.get('VAULT_PATH', '../AI_Employee_Vault')
        pending_approval_dir = Path(vault_path) / 'Pending_Approval'
        pending_approval_dir.mkdir(parents=True, exist_ok=True)

        # Create approval file name
        safe_desc = "".join(c for c in transaction_data.get('description', 'payment') if c.isalnum() or c in (' ', '-', '_')).rstrip()
        if not safe_desc:
            safe_desc = "payment"

        filename = f"APPROVAL_{action_type}_{safe_desc}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = pending_approval_dir / filename

        # Create approval request content
        approval_content = f"""---
type: approval_request
action: {action_type}
amount: {transaction_data.get('amount', 0)}
recipient: {transaction_data.get('recipient', '')}
transaction_id: {transaction_data.get('transaction_id', '')}
created: {datetime.now().isoformat()}
expires: {(datetime.now() + timedelta(days=1)).isoformat()}
status: pending
---

# Payment Approval Required

## Transaction Details
- **Amount**: ${transaction_data.get('amount', 0)}
- **Recipient**: {transaction_data.get('recipient', '')}
- **Description**: {transaction_data.get('description', '')}
- **Transaction ID**: {transaction_data.get('transaction_id', '')}
- **Timestamp**: {transaction_data.get('timestamp', datetime.now().isoformat())}

## Action Required
Please review this transaction and move this file to either:
- **Approved** folder to approve the transaction
- **Rejected** folder to reject the transaction

## To Approve
Move this file to `/Approved/` folder.

## To Reject
Move this file to `/Rejected/` folder.
"""

        # Write approval request file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(approval_content)

        logger.info(f"Created approval request: {filepath}")

    def save_invoice(self, invoice_data: Dict[str, Any]):
        """Save invoice to vault"""
        import os
        from datetime import datetime

        # Get vault path from environment or default
        vault_path = os.environ.get('VAULT_PATH', '../AI_Employee_Vault')
        invoices_dir = Path(vault_path) / 'Invoices'
        invoices_dir.mkdir(parents=True, exist_ok=True)

        # Create invoice file
        filename = f"{invoice_data['invoice_id']}.md"
        filepath = invoices_dir / filename

        # Create invoice content
        invoice_content = f"""---
invoice_id: {invoice_data['invoice_id']}
customer: {invoice_data['customer']}
amount: {invoice_data['amount']}
currency: {invoice_data['currency']}
due_date: {invoice_data['due_date']}
status: {invoice_data['status']}
created_at: {invoice_data['created_at']}
---

# Invoice {invoice_data['invoice_id']}

**Customer**: {invoice_data['customer']}
**Amount**: {invoice_data['currency']} {invoice_data['amount']}
**Due Date**: {invoice_data['due_date']}

## Items
"""

        for item in invoice_data.get('items', []):
            invoice_content += f"- {item.get('name', '')}: {item.get('price', 0)}\n"

        invoice_content += f"""

## Description
{invoice_data['description']}

## Status
{invoice_data['status']}

Generated by Payment MCP Server
"""

        # Write invoice file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(invoice_content)

    def save_scheduled_payment(self, schedule_data: Dict[str, Any]):
        """Save scheduled payment to vault"""
        import os
        from datetime import datetime

        # Get vault path from environment or default
        vault_path = os.environ.get('VAULT_PATH', '../AI_Employee_Vault')
        scheduled_dir = Path(vault_path) / 'Scheduled'
        scheduled_dir.mkdir(parents=True, exist_ok=True)

        # Create scheduled payment file
        filename = f"SCHEDULED_PAYMENT_{schedule_data['schedule_id']}.md"
        filepath = scheduled_dir / filename

        # Create scheduled payment content
        schedule_content = f"""---
schedule_id: {schedule_data['schedule_id']}
amount: {schedule_data['amount']}
recipient: {schedule_data['recipient']}
scheduled_date: {schedule_data['scheduled_date']}
recurrence: {schedule_data['recurrence']}
status: {schedule_data['status']}
created_at: {schedule_data['created_at']}
---

# Scheduled Payment

**Schedule ID**: {schedule_data['schedule_id']}
**Amount**: ${schedule_data['amount']}
**Recipient**: {schedule_data['recipient']}
**Scheduled Date**: {schedule_data['scheduled_date']}
**Recurrence**: {schedule_data['recurrence']}

## Description
{schedule_data['description']}

## Status
{schedule_data['status']}

Generated by Payment MCP Server
"""

        # Write scheduled payment file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(schedule_content)

async def main():
    """Main server loop"""
    server = PaymentMCPServer()
    logger.info("Payment MCP Server starting...")

    # In a real implementation, this would connect to MCP protocol
    # For now, we'll just run a simple test
    print("Payment MCP Server ready for requests")

    # Example request simulation
    test_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "mcp/discover"
    }

    result = await server.handle_request(test_request)
    print("Server capabilities:", json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(main())