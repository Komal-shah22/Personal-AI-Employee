"""
Security and Error Monitoring for Personal AI Employee

Implements advanced security features and error recovery
"""

import os
import json
from pathlib import Path
from datetime import datetime
import logging
import traceback
from typing import Dict, Any, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityMonitor:
    def __init__(self, vault_path: str = "../AI_Employee_Vault"):
        self.vault_path = Path(vault_path)
        self.logs_dir = self.vault_path / "Logs"
        self.security_dir = self.vault_path / "Security"
        self.audit_dir = self.vault_path / "Audit"

        # Create necessary directories
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.security_dir.mkdir(parents=True, exist_ok=True)
        self.audit_dir.mkdir(parents=True, exist_ok=True)

    def log_security_event(self, event_type: str, details: Dict[str, Any], severity: str = "info"):
        """Log a security event to the vault"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = {
            "timestamp": timestamp,
            "event_type": event_type,
            "severity": severity,
            "details": details,
            "source": "SecurityMonitor"
        }

        # Write to security log
        security_log_file = self.security_dir / f"security_events_{datetime.now().strftime('%Y-%m-%d')}.log"
        with open(security_log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + "\n")

        logger.info(f"Security event logged: {event_type} - {severity}")

    def log_audit_trail(self, action: str, actor: str, target: str, result: str, metadata: Dict[str, Any] = None):
        """Log an audit trail entry"""
        timestamp = datetime.now().isoformat()
        audit_entry = {
            "timestamp": timestamp,
            "action": action,
            "actor": actor,
            "target": target,
            "result": result,
            "metadata": metadata or {},
            "session_id": os.environ.get("SESSION_ID", "unknown")
        }

        # Write to audit log
        audit_log_file = self.audit_dir / f"audit_trail_{datetime.now().strftime('%Y-%m-%d')}.log"
        with open(audit_log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(audit_entry) + "\n")

        logger.info(f"Audit trail logged: {action} by {actor} on {target}")

    def check_permissions(self, actor: str, action: str, resource: str) -> bool:
        """Check if an actor has permissions to perform an action on a resource"""
        # In a real implementation, this would check against a permissions matrix
        # For now, we'll implement basic rules

        # Define basic permissions
        permissions = {
            "claude_code": ["read", "write", "process"],
            "orchestrator": ["read", "move", "update"],
            "watcher": ["read", "create"],
            "skill": ["read", "write", "update"],
            "mcp_server": ["execute", "update"]
        }

        actor_type = actor.split(":")[0] if ":" in actor else actor
        allowed_actions = permissions.get(actor_type, [])

        return action in allowed_actions

    def validate_input(self, data: Any, schema: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate input data against a schema"""
        errors = []

        # Basic validation against schema
        if "type" in schema:
            expected_type = schema["type"]
            if expected_type == "string" and not isinstance(data, str):
                errors.append(f"Expected string, got {type(data).__name__}")
            elif expected_type == "number" and not isinstance(data, (int, float)):
                errors.append(f"Expected number, got {type(data).__name__}")
            elif expected_type == "boolean" and not isinstance(data, bool):
                errors.append(f"Expected boolean, got {type(data).__name__}")
            elif expected_type == "array" and not isinstance(data, list):
                errors.append(f"Expected array, got {type(data).__name__}")
            elif expected_type == "object" and not isinstance(data, dict):
                errors.append(f"Expected object, got {type(data).__name__}")

        if "required" in schema and isinstance(data, dict):
            required_fields = schema["required"]
            for field in required_fields:
                if field not in data:
                    errors.append(f"Missing required field: {field}")

        if "maxLength" in schema and isinstance(data, str):
            max_length = schema["maxLength"]
            if len(data) > max_length:
                errors.append(f"String exceeds maximum length of {max_length}")

        return len(errors) == 0, errors

    def sanitize_input(self, data: str) -> str:
        """Sanitize input to prevent injection attacks"""
        # Remove dangerous characters/patterns
        sanitized = data.replace("<script", "&lt;script").replace("javascript:", "javascript_")
        sanitized = sanitized.replace("eval(", "eval_").replace("__import__", "_import_")
        return sanitized

    def detect_anomaly(self, action: str, actor: str, context: Dict[str, Any]) -> bool:
        """Detect anomalous behavior"""
        # Simple anomaly detection based on patterns
        anomalies = []

        # Check for unusual timing (non-business hours)
        current_hour = datetime.now().hour
        if current_hour < 6 or current_hour > 22:
            anomalies.append("Off-hours activity")

        # Check for unusual frequency
        if context.get("frequency", 0) > 10:  # More than 10 actions in short time
            anomalies.append("High frequency activity")

        # Check for unusual targets
        target = context.get("target", "")
        if "admin" in target.lower() or "system" in target.lower():
            anomalies.append("System resource access")

        if anomalies:
            self.log_security_event("anomaly_detected", {
                "action": action,
                "actor": actor,
                "anomalies": anomalies,
                "context": context
            }, "warning")
            return True

        return False

    def handle_error(self, error: Exception, context: str = "", recoverable: bool = True) -> Dict[str, Any]:
        """Handle an error with appropriate logging and recovery"""
        error_details = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
            "context": context,
            "timestamp": datetime.now().isoformat(),
            "recoverable": recoverable
        }

        # Log the error
        error_file = self.security_dir / f"errors_{datetime.now().strftime('%Y-%m-%d')}.log"
        with open(error_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(error_details) + "\n")

        logger.error(f"Error handled: {error_details['error_type']} - {error_details['error_message']}")

        # Attempt recovery if possible
        if recoverable:
            return self.attempt_recovery(error_details)
        else:
            return {
                "status": "error_handled",
                "recovered": False,
                "message": f"Non-recoverable error: {error_details['error_message']}"
            }

    def attempt_recovery(self, error_details: Dict[str, Any]) -> Dict[str, Any]:
        """Attempt to recover from an error"""
        try:
            # Based on error type, attempt different recovery strategies
            error_type = error_details["error_type"]

            if error_type in ["FileNotFoundError", "PermissionError"]:
                # Try to recreate missing directories
                self.logs_dir.mkdir(parents=True, exist_ok=True)
                self.security_dir.mkdir(parents=True, exist_ok=True)
                self.audit_dir.mkdir(parents=True, exist_ok=True)

                return {
                    "status": "recovered",
                    "strategy": "directory_recreation",
                    "message": "Recovered by recreating directories"
                }

            elif error_type in ["ConnectionError", "TimeoutError"]:
                # Connection-related error, suggest retry
                return {
                    "status": "retry_advised",
                    "strategy": "connection_retry",
                    "message": "Connection error, retry advised"
                }

            elif error_type in ["ValueError", "TypeError"]:
                # Data validation error, suggest correction
                return {
                    "status": "data_correction_needed",
                    "strategy": "input_validation",
                    "message": "Data validation error, input correction needed"
                }

            else:
                # Unknown error type, log and continue
                return {
                    "status": "logged_only",
                    "strategy": "logging",
                    "message": "Error logged, no specific recovery strategy"
                }

        except Exception as recovery_error:
            logger.error(f"Recovery attempt failed: {recovery_error}")
            return {
                "status": "recovery_failed",
                "strategy": "none",
                "message": f"Recovery failed: {recovery_error}"
            }

    def monitor_system_health(self) -> Dict[str, Any]:
        """Monitor overall system health"""
        health_status = {
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "overall_status": "healthy"
        }

        # Check vault directory health
        vault_health = self.check_vault_health()
        health_status["checks"]["vault"] = vault_health

        # Check log directory health
        logs_health = self.check_logs_health()
        health_status["checks"]["logs"] = logs_health

        # Check security directory health
        security_health = self.check_security_health()
        health_status["checks"]["security"] = security_health

        # Determine overall status
        if any(check["status"] == "unhealthy" for check in health_status["checks"].values()):
            health_status["overall_status"] = "unhealthy"
        elif any(check["status"] == "warning" for check in health_status["checks"].values()):
            health_status["overall_status"] = "warning"

        return health_status

    def check_vault_health(self) -> Dict[str, Any]:
        """Check vault directory health"""
        try:
            vault_path = Path(self.vault_path)
            if not vault_path.exists():
                return {"status": "unhealthy", "message": "Vault directory missing"}

            # Check if we can write to vault
            test_file = vault_path / ".health_check"
            test_file.touch()
            test_file.unlink()

            return {"status": "healthy", "message": "Vault accessible and writable"}
        except Exception as e:
            return {"status": "unhealthy", "message": f"Vault access error: {str(e)}"}

    def check_logs_health(self) -> Dict[str, Any]:
        """Check logs directory health"""
        try:
            logs_path = Path(self.logs_dir)
            if not logs_path.exists():
                logs_path.mkdir(parents=True)
                return {"status": "warning", "message": "Logs directory recreated"}

            # Check if we can write to logs
            test_file = logs_path / ".health_check"
            test_file.touch()
            test_file.unlink()

            return {"status": "healthy", "message": "Logs directory accessible"}
        except Exception as e:
            return {"status": "unhealthy", "message": f"Logs access error: {str(e)}"}

    def check_security_health(self) -> Dict[str, Any]:
        """Check security directory health"""
        try:
            security_path = Path(self.security_dir)
            if not security_path.exists():
                security_path.mkdir(parents=True)
                return {"status": "warning", "message": "Security directory recreated"}

            # Check if we can write to security
            test_file = security_path / ".health_check"
            test_file.touch()
            test_file.unlink()

            return {"status": "healthy", "message": "Security directory accessible"}
        except Exception as e:
            return {"status": "unhealthy", "message": f"Security access error: {str(e)}"}

# Global security monitor instance
security_monitor = SecurityMonitor()

def get_security_monitor() -> SecurityMonitor:
    """Get the global security monitor instance"""
    return security_monitor

# Example usage functions
def log_security_event(event_type: str, details: Dict[str, Any], severity: str = "info"):
    """Convenience function to log security events"""
    return security_monitor.log_security_event(event_type, details, severity)

def log_audit_trail(action: str, actor: str, target: str, result: str, metadata: Dict[str, Any] = None):
    """Convenience function to log audit trails"""
    return security_monitor.log_audit_trail(action, actor, target, result, metadata)

def check_permissions(actor: str, action: str, resource: str) -> bool:
    """Convenience function to check permissions"""
    return security_monitor.check_permissions(actor, action, resource)

def handle_error(error: Exception, context: str = "", recoverable: bool = True) -> Dict[str, Any]:
    """Convenience function to handle errors"""
    return security_monitor.handle_error(error, context, recoverable)

def monitor_system_health() -> Dict[str, Any]:
    """Convenience function to monitor system health"""
    return security_monitor.monitor_system_health()

if __name__ == "__main__":
    # Example usage
    print("Security Monitor initialized")

    # Test logging
    log_security_event("test_event", {"test": "data"}, "info")
    log_audit_trail("test_action", "test_actor", "test_target", "success")

    # Test permissions
    print(f"Permission check: {check_permissions('claude_code', 'read', 'test')}")

    # Test system health
    health = monitor_system_health()
    print(f"System health: {health['overall_status']}")