"""
ERP MCP Server for Personal AI Employee

Integrates with Odoo ERP Community for business management
"""
import asyncio
import json
import logging
from typing import Dict, Any, List
from pathlib import Path
import xmlrpc.client
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ERPMCPServer:
    def __init__(self):
        self.capabilities = {
            "name": "erp-mcp",
            "version": "1.0.0",
            "description": "Odoo ERP Community integration for business management, accounting, and operations",
            "resources": [
                {
                    "type": "erp_action",
                    "name": "create_customer",
                    "description": "Create a new customer in Odoo"
                },
                {
                    "type": "erp_action",
                    "name": "create_invoice",
                    "description": "Create an invoice in Odoo"
                },
                {
                    "type": "erp_action",
                    "name": "create_product",
                    "description": "Create a product in Odoo"
                },
                {
                    "type": "erp_action",
                    "name": "create_purchase_order",
                    "description": "Create a purchase order in Odoo"
                },
                {
                    "type": "erp_action",
                    "name": "create_sales_order",
                    "description": "Create a sales order in Odoo"
                },
                {
                    "type": "erp_action",
                    "name": "get_customers",
                    "description": "Retrieve customer list from Odoo"
                },
                {
                    "type": "erp_action",
                    "name": "get_products",
                    "description": "Retrieve product list from Odoo"
                },
                {
                    "type": "erp_action",
                    "name": "get_invoices",
                    "description": "Retrieve invoice list from Odoo"
                },
                {
                    "type": "erp_action",
                    "name": "get_orders",
                    "description": "Retrieve order list from Odoo"
                },
                {
                    "type": "erp_action",
                    "name": "update_record",
                    "description": "Update an existing record in Odoo"
                }
            ]
        }

        # Odoo connection parameters (these would be configured in production)
        self.odoo_url = "http://localhost:8069"  # Default local Odoo instance
        self.db_name = "odoo_db"  # Default database name
        self.username = "admin"  # Default username
        self.password = "admin"  # Default password (would be secured in env vars)

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

            elif method == "create_customer":
                return await self.create_customer(request)
            elif method == "create_invoice":
                return await self.create_invoice(request)
            elif method == "create_product":
                return await self.create_product(request)
            elif method == "create_purchase_order":
                return await self.create_purchase_order(request)
            elif method == "create_sales_order":
                return await self.create_sales_order(request)
            elif method == "get_customers":
                return await self.get_customers(request)
            elif method == "get_products":
                return await self.get_products(request)
            elif method == "get_invoices":
                return await self.get_invoices(request)
            elif method == "get_orders":
                return await self.get_orders(request)
            elif method == "update_record":
                return await self.update_record(request)
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

    async def connect_to_odoo(self):
        """Connect to Odoo instance and return common objects"""
        try:
            # In a real implementation, this would connect to the actual Odoo instance
            # For simulation, we'll return mock connection objects
            common_proxy = None  # Would be xmlrpc.client.ServerProxy(f'{self.odoo_url}/xmlrpc/2/common')
            models_proxy = None  # Would be xmlrpc.client.ServerProxy(f'{self.odoo_url}/xmlrpc/2/object')

            # Authenticate and get user ID
            uid = 1  # Mock user ID

            return common_proxy, models_proxy, uid
        except Exception as e:
            logger.error(f"Error connecting to Odoo: {e}")
            raise

    async def create_customer(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new customer in Odoo"""
        params = request.get("params", {})
        name = params.get("name", "")
        email = params.get("email", "")
        phone = params.get("phone", "")
        address = params.get("address", "")
        vat = params.get("vat", "")
        approval_required = params.get("approval_required", True)

        # Simulate customer creation (in real implementation, would connect to Odoo)
        logger.info(f"Creating customer: {name}")

        customer_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "address": address,
            "vat": vat,
            "status": "pending_approval" if approval_required else "created",
            "timestamp": datetime.now().isoformat(),
            "message": f"Customer {name} creation initiated"
        }

        # Log the customer creation to the vault for audit trail
        self.log_erp_activity("customer_creation", customer_data)

        # If approval required, create approval request
        if approval_required:
            self.create_approval_request(customer_data, action_type="customer_creation")

        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": customer_data
        }

    async def create_invoice(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Create an invoice in Odoo"""
        params = request.get("params", {})
        customer_id = params.get("customer_id", "")
        amount = params.get("amount", 0)
        currency = params.get("currency", "USD")
        description = params.get("description", "")
        due_date = params.get("due_date", "")
        lines = params.get("lines", [])
        approval_required = params.get("approval_required", True)

        # Simulate invoice creation (in real implementation, would connect to Odoo)
        logger.info(f"Creating invoice for customer {customer_id}")

        invoice_data = {
            "customer_id": customer_id,
            "amount": amount,
            "currency": currency,
            "description": description,
            "due_date": due_date,
            "lines": lines,
            "status": "pending_approval" if approval_required else "created",
            "timestamp": datetime.now().isoformat(),
            "message": f"Invoice of ${amount} created for customer {customer_id}"
        }

        # Log the invoice creation to the vault for audit trail
        self.log_erp_activity("invoice_creation", invoice_data)

        # If approval required, create approval request
        if approval_required:
            self.create_approval_request(invoice_data, action_type="invoice_creation")

        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": invoice_data
        }

    async def create_product(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Create a product in Odoo"""
        params = request.get("params", {})
        name = params.get("name", "")
        code = params.get("code", "")
        price = params.get("price", 0)
        category = params.get("category", "")
        description = params.get("description", "")
        quantity = params.get("quantity", 0)
        approval_required = params.get("approval_required", True)

        # Simulate product creation (in real implementation, would connect to Odoo)
        logger.info(f"Creating product: {name}")

        product_data = {
            "name": name,
            "code": code,
            "price": price,
            "category": category,
            "description": description,
            "quantity": quantity,
            "status": "pending_approval" if approval_required else "created",
            "timestamp": datetime.now().isoformat(),
            "message": f"Product {name} created with code {code}"
        }

        # Log the product creation to the vault for audit trail
        self.log_erp_activity("product_creation", product_data)

        # If approval required, create approval request
        if approval_required:
            self.create_approval_request(product_data, action_type="product_creation")

        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": product_data
        }

    async def create_purchase_order(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Create a purchase order in Odoo"""
        params = request.get("params", {})
        supplier_id = params.get("supplier_id", "")
        products = params.get("products", [])
        total_amount = params.get("total_amount", 0)
        expected_date = params.get("expected_date", "")
        approval_required = params.get("approval_required", True)

        # Simulate purchase order creation (in real implementation, would connect to Odoo)
        logger.info(f"Creating purchase order for supplier {supplier_id}")

        po_data = {
            "supplier_id": supplier_id,
            "products": products,
            "total_amount": total_amount,
            "expected_date": expected_date,
            "status": "pending_approval" if approval_required else "created",
            "timestamp": datetime.now().isoformat(),
            "message": f"Purchase order created for supplier {supplier_id}"
        }

        # Log the purchase order creation to the vault for audit trail
        self.log_erp_activity("purchase_order_creation", po_data)

        # If approval required, create approval request
        if approval_required:
            self.create_approval_request(po_data, action_type="purchase_order")

        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": po_data
        }

    async def create_sales_order(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Create a sales order in Odoo"""
        params = request.get("params", {})
        customer_id = params.get("customer_id", "")
        products = params.get("products", [])
        total_amount = params.get("total_amount", 0)
        delivery_date = params.get("delivery_date", "")
        approval_required = params.get("approval_required", True)

        # Simulate sales order creation (in real implementation, would connect to Odoo)
        logger.info(f"Creating sales order for customer {customer_id}")

        so_data = {
            "customer_id": customer_id,
            "products": products,
            "total_amount": total_amount,
            "delivery_date": delivery_date,
            "status": "pending_approval" if approval_required else "created",
            "timestamp": datetime.now().isoformat(),
            "message": f"Sales order created for customer {customer_id}"
        }

        # Log the sales order creation to the vault for audit trail
        self.log_erp_activity("sales_order_creation", so_data)

        # If approval required, create approval request
        if approval_required:
            self.create_approval_request(so_data, action_type="sales_order")

        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": so_data
        }

    async def get_customers(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve customer list from Odoo"""
        params = request.get("params", {})
        domain = params.get("domain", [])
        limit = params.get("limit", 20)

        # Simulate retrieving customers (in real implementation, would connect to Odoo)
        logger.info(f"Retrieving customers with domain: {domain}")

        customers = [
            {"id": 1, "name": "John Doe", "email": "john@example.com", "status": "active"},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "status": "active"},
            {"id": 3, "name": "Acme Corp", "email": "contact@acme.com", "status": "active"}
        ]

        result_data = {
            "customers": customers[:limit],
            "total_count": len(customers),
            "retrieved_at": datetime.now().isoformat(),
            "message": f"Retrieved {min(len(customers), limit)} customers"
        }

        # Log the retrieval to the vault for audit trail
        self.log_erp_activity("customers_retrieval", result_data)

        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": result_data
        }

    async def get_products(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve product list from Odoo"""
        params = request.get("params", {})
        domain = params.get("domain", [])
        limit = params.get("limit", 20)

        # Simulate retrieving products (in real implementation, would connect to Odoo)
        logger.info(f"Retrieving products with domain: {domain}")

        products = [
            {"id": 1, "name": "Basic Service", "code": "BS001", "price": 100.0, "qty": 100},
            {"id": 2, "name": "Premium Service", "code": "PS001", "price": 500.0, "qty": 50},
            {"id": 3, "name": "Consulting Hour", "code": "CH001", "price": 200.0, "qty": 200}
        ]

        result_data = {
            "products": products[:limit],
            "total_count": len(products),
            "retrieved_at": datetime.now().isoformat(),
            "message": f"Retrieved {min(len(products), limit)} products"
        }

        # Log the retrieval to the vault for audit trail
        self.log_erp_activity("products_retrieval", result_data)

        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": result_data
        }

    async def get_invoices(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve invoice list from Odoo"""
        params = request.get("params", {})
        domain = params.get("domain", [])
        limit = params.get("limit", 20)

        # Simulate retrieving invoices (in real implementation, would connect to Odoo)
        logger.info(f"Retrieving invoices with domain: {domain}")

        invoices = [
            {"id": 1, "number": "INV001", "customer": "John Doe", "amount": 1000.0, "status": "paid"},
            {"id": 2, "number": "INV002", "customer": "Jane Smith", "amount": 500.0, "status": "sent"},
            {"id": 3, "number": "INV003", "customer": "Acme Corp", "amount": 2500.0, "status": "overdue"}
        ]

        result_data = {
            "invoices": invoices[:limit],
            "total_count": len(invoices),
            "retrieved_at": datetime.now().isoformat(),
            "message": f"Retrieved {min(len(invoices), limit)} invoices"
        }

        # Log the retrieval to the vault for audit trail
        self.log_erp_activity("invoices_retrieval", result_data)

        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": result_data
        }

    async def get_orders(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve order list from Odoo"""
        params = request.get("params", {})
        order_type = params.get("type", "both")  # 'sales', 'purchase', 'both'
        limit = params.get("limit", 20)

        # Simulate retrieving orders (in real implementation, would connect to Odoo)
        logger.info(f"Retrieving {order_type} orders")

        orders = [
            {"id": 1, "number": "SO001", "type": "sale", "customer": "John Doe", "amount": 1000.0, "status": "confirmed"},
            {"id": 2, "number": "PO001", "type": "purchase", "supplier": "Supplier A", "amount": 500.0, "status": "draft"},
            {"id": 3, "number": "SO002", "type": "sale", "customer": "Jane Smith", "amount": 750.0, "status": "shipped"}
        ]

        if order_type != "both":
            orders = [o for o in orders if o["type"] == order_type]

        result_data = {
            "orders": orders[:limit],
            "total_count": len(orders),
            "retrieved_at": datetime.now().isoformat(),
            "message": f"Retrieved {min(len(orders), limit)} {order_type} orders"
        }

        # Log the retrieval to the vault for audit trail
        self.log_erp_activity("orders_retrieval", result_data)

        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": result_data
        }

    async def update_record(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing record in Odoo"""
        params = request.get("params", {})
        model = params.get("model", "")
        record_id = params.get("id", "")
        values = params.get("values", {})
        approval_required = params.get("approval_required", True)

        # Simulate record update (in real implementation, would connect to Odoo)
        logger.info(f"Updating {model} record {record_id}")

        update_data = {
            "model": model,
            "record_id": record_id,
            "values": values,
            "status": "pending_approval" if approval_required else "updated",
            "timestamp": datetime.now().isoformat(),
            "message": f"Update initiated for {model} record {record_id}"
        }

        # Log the update to the vault for audit trail
        self.log_erp_activity("record_update", update_data)

        # If approval required, create approval request
        if approval_required:
            self.create_approval_request(update_data, action_type="record_update")

        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": update_data
        }

    def log_erp_activity(self, action: str, data: Dict[str, Any]):
        """Log ERP activity to the vault"""
        import os
        from datetime import datetime

        # Get vault path from environment or default
        vault_path = os.environ.get('VAULT_PATH', '../AI_Employee_Vault')
        logs_dir = Path(vault_path) / 'Logs'
        logs_dir.mkdir(parents=True, exist_ok=True)

        # Create log entry
        log_entry = f"[{datetime.now().strftime('%H:%M:%S')}] ERP_MCP: {action.upper()} - {json.dumps(data, default=str)[:100]}...\n"

        # Write to today's log file
        log_file = logs_dir / f"{datetime.now().strftime('%Y-%m-%d')}.txt"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

    def create_approval_request(self, transaction_data: Dict[str, Any], action_type: str = "erp_action"):
        """Create an approval request for sensitive ERP actions"""
        import os
        from datetime import datetime, timedelta

        # Get vault path from environment or default
        vault_path = os.environ.get('VAULT_PATH', '../AI_Employee_Vault')
        pending_approval_dir = Path(vault_path) / 'Pending_Approval'
        pending_approval_dir.mkdir(parents=True, exist_ok=True)

        # Create approval file name
        safe_desc = "".join(c for c in str(transaction_data.get('name', transaction_data.get('description', action_type))) if c.isalnum() or c in (' ', '-', '_')).rstrip()
        if not safe_desc:
            safe_desc = action_type

        filename = f"APPROVAL_{action_type}_{safe_desc}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = pending_approval_dir / filename

        # Create approval request content
        approval_content = f"""---
type: approval_request
action: {action_type}
entity: {transaction_data.get('name', transaction_data.get('customer_id', transaction_data.get('supplier_id', 'unknown')))}
amount: {transaction_data.get('amount', transaction_data.get('total_amount', 0))}
created: {datetime.now().isoformat()}
expires: {(datetime.now() + timedelta(days=1)).isoformat()}
status: pending
---

# ERP Action Approval Required

## Transaction Details
- **Action**: {action_type.replace('_', ' ').title()}
- **Entity**: {transaction_data.get('name', transaction_data.get('customer_id', transaction_data.get('supplier_id', 'unknown')))}
- **Amount**: ${transaction_data.get('amount', transaction_data.get('total_amount', 0))}
- **Details**: {transaction_data.get('description', transaction_data.get('email', ''))}
- **Timestamp**: {transaction_data.get('timestamp', datetime.now().isoformat())}

## Action Required
Please review this ERP transaction and move this file to either:
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

        logger.info(f"Created ERP approval request: {filepath}")

async def main():
    """Main server loop"""
    server = ERPMCPServer()
    logger.info("ERP MCP Server starting...")

    # In a real implementation, this would connect to MCP protocol
    # For now, we'll just run a simple test
    print("ERP MCP Server ready for requests")

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