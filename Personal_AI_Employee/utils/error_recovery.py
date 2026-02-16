"""
Error Recovery and Graceful Degradation for Personal AI Employee

Implements comprehensive error handling and recovery mechanisms
"""

import os
import json
import time
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Callable, Optional, List
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecoveryStrategy(Enum):
    RETRY = "retry"
    FALLBACK = "fallback"
    DEGRADE = "degrade"
    ALERT = "alert"
    SKIP = "skip"

class ErrorRecoveryManager:
    def __init__(self, vault_path: str = "../AI_Employee_Vault"):
        self.vault_path = Path(vault_path)
        self.recovery_dir = self.vault_path / "Recovery"
        self.errors_dir = self.vault_path / "Errors"
        self.backup_dir = self.vault_path / "Backups"

        # Create necessary directories
        self.recovery_dir.mkdir(parents=True, exist_ok=True)
        self.errors_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        # Track retry attempts
        self.retry_counts: Dict[str, int] = {}

    def execute_with_recovery(self,
                           operation: Callable,
                           context: str = "",
                           max_retries: int = 3,
                           backoff_factor: float = 1.0,
                           recovery_strategy: RecoveryStrategy = RecoveryStrategy.RETRY,
                           fallback_operation: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Execute an operation with comprehensive error recovery
        """
        operation_id = f"{context}_{datetime.now().isoformat()}"

        for attempt in range(max_retries + 1):
            try:
                # Execute the operation
                result = operation()

                # Log successful execution
                self.log_recovery_event("operation_success", {
                    "operation_id": operation_id,
                    "attempt": attempt + 1,
                    "context": context
                })

                return {
                    "status": "success",
                    "result": result,
                    "attempts": attempt + 1,
                    "recovered": attempt > 0
                }

            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed for {context}: {e}")

                # Log error
                self.log_error(e, context, attempt + 1)

                if attempt == max_retries:
                    # Final attempt failed, try recovery strategy
                    return self.apply_recovery_strategy(
                        e, context, recovery_strategy, fallback_operation
                    )

                # Apply backoff if not the last attempt
                if attempt < max_retries:
                    sleep_time = backoff_factor * (2 ** attempt)
                    logger.info(f"Waiting {sleep_time}s before retry {attempt + 2}")
                    time.sleep(sleep_time)

        # This should never be reached, but included for completeness
        return {
            "status": "failed",
            "error": "Max retries exceeded",
            "attempts": max_retries + 1
        }

    def apply_recovery_strategy(self,
                              error: Exception,
                              context: str,
                              strategy: RecoveryStrategy,
                              fallback_operation: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Apply the specified recovery strategy
        """
        if strategy == RecoveryStrategy.RETRY:
            return {
                "status": "failed",
                "error": str(error),
                "message": "Retry strategy exhausted"
            }

        elif strategy == RecoveryStrategy.FALLBACK and fallback_operation:
            try:
                result = fallback_operation()
                self.log_recovery_event("fallback_success", {
                    "context": context,
                    "error": str(error)
                })
                return {
                    "status": "success",
                    "result": result,
                    "recovered": True,
                    "fallback_used": True
                }
            except Exception as fallback_error:
                logger.error(f"Fallback operation failed: {fallback_error}")
                return {
                    "status": "failed",
                    "error": str(error),
                    "fallback_error": str(fallback_error),
                    "message": "Both primary and fallback operations failed"
                }

        elif strategy == RecoveryStrategy.DEGRADE:
            # Return a degraded but functional result
            self.log_recovery_event("graceful_degradation", {
                "context": context,
                "error": str(error),
                "strategy": "degraded_mode"
            })
            return {
                "status": "degraded",
                "result": None,
                "recovered": True,
                "degraded": True,
                "message": "Operation degraded to minimal functionality"
            }

        elif strategy == RecoveryStrategy.ALERT:
            # Log the error and alert but continue
            self.log_recovery_event("error_alerted", {
                "context": context,
                "error": str(error),
                "strategy": "alert_only"
            })
            return {
                "status": "alerted",
                "error": str(error),
                "recovered": False,
                "message": "Error detected and logged"
            }

        elif strategy == RecoveryStrategy.SKIP:
            # Skip the operation but continue processing
            self.log_recovery_event("operation_skipped", {
                "context": context,
                "error": str(error),
                "strategy": "skip"
            })
            return {
                "status": "skipped",
                "error": str(error),
                "recovered": True,
                "skipped": True,
                "message": "Operation skipped due to error"
            }

        else:
            return {
                "status": "failed",
                "error": str(error),
                "message": "No suitable recovery strategy applied"
            }

    def log_error(self, error: Exception, context: str, attempt: int):
        """Log error details to the vault"""
        error_data = {
            "timestamp": datetime.now().isoformat(),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context,
            "attempt": attempt,
            "session_id": os.environ.get("SESSION_ID", "unknown")
        }

        # Write to error log
        error_file = self.errors_dir / f"errors_{datetime.now().strftime('%Y-%m-%d')}.log"
        with open(error_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(error_data) + "\n")

        logger.error(f"Error logged: {error_data['error_type']} in {context}")

    def log_recovery_event(self, event_type: str, details: Dict[str, Any]):
        """Log a recovery event to the vault"""
        event_data = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "details": details,
            "session_id": os.environ.get("SESSION_ID", "unknown")
        }

        # Write to recovery log
        recovery_file = self.recovery_dir / f"recovery_events_{datetime.now().strftime('%Y-%m-%d')}.log"
        with open(recovery_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(event_data) + "\n")

        logger.info(f"Recovery event logged: {event_type}")

    def backup_state(self, state: Dict[str, Any], label: str = ""):
        """Backup current state to vault"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_id = f"backup_{timestamp}_{label}" if label else f"backup_{timestamp}"

        backup_data = {
            "timestamp": datetime.now().isoformat(),
            "backup_id": backup_id,
            "state": state,
            "session_id": os.environ.get("SESSION_ID", "unknown")
        }

        backup_file = self.backup_dir / f"{backup_id}.json"
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2)

        logger.info(f"State backed up: {backup_id}")

    def restore_state(self, backup_id: str) -> Optional[Dict[str, Any]]:
        """Restore state from a backup"""
        backup_file = self.backup_dir / f"{backup_id}.json"

        if not backup_file.exists():
            logger.error(f"Backup file not found: {backup_file}")
            return None

        try:
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)

            logger.info(f"State restored from: {backup_id}")
            return backup_data.get("state", {})
        except Exception as e:
            logger.error(f"Error restoring backup {backup_id}: {e}")
            return None

    def quarantine_failed_operation(self, operation_data: Dict[str, Any], error: Exception):
        """Quarantine a failed operation for manual review"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        quarantine_id = f"quarantine_{timestamp}"

        quarantine_data = {
            "quarantine_id": quarantine_id,
            "timestamp": datetime.now().isoformat(),
            "operation": operation_data,
            "error": str(error),
            "error_type": type(error).__name__,
            "session_id": os.environ.get("SESSION_ID", "unknown")
        }

        quarantine_dir = self.vault_path / "Quarantine"
        quarantine_dir.mkdir(exist_ok=True)

        quarantine_file = quarantine_dir / f"{quarantine_id}.json"
        with open(quarantine_file, 'w', encoding='utf-8') as f:
            json.dump(quarantine_data, f, indent=2)

        logger.info(f"Operation quarantined: {quarantine_id}")

    def cleanup_old_logs(self, days_to_keep: int = 30):
        """Clean up old logs to prevent disk space issues"""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)

        for log_dir in [self.errors_dir, self.recovery_dir]:
            for log_file in log_dir.glob("*.log"):
                try:
                    file_date_str = log_file.name.split('_')[-1].replace('.log', '')
                    if file_date_str:
                        file_date = datetime.strptime(file_date_str, '%Y-%m-%d')
                        if file_date < cutoff_date:
                            log_file.unlink()
                            logger.info(f"Cleaned up old log: {log_file}")
                except ValueError:
                    # If date parsing fails, skip the file
                    continue

    def get_system_resilience_metrics(self) -> Dict[str, Any]:
        """Get metrics about system resilience"""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "total_errors": 0,
            "recovery_attempts": 0,
            "successful_recoveries": 0,
            "degraded_operations": 0,
            "quarantined_operations": 0
        }

        # Count error logs
        for error_file in self.errors_dir.glob("errors_*.log"):
            try:
                with open(error_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    metrics["total_errors"] += len(lines)
            except:
                continue

        # Count recovery logs
        for recovery_file in self.recovery_dir.glob("recovery_events_*.log"):
            try:
                with open(recovery_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    metrics["recovery_attempts"] += len(lines)
                    # Count successful recoveries
                    for line in lines:
                        if '"event_type": "operation_success"' in line:
                            metrics["successful_recoveries"] += 1
                        elif '"event_type": "graceful_degradation"' in line:
                            metrics["degraded_operations"] += 1
            except:
                continue

        # Count quarantined operations
        quarantine_dir = self.vault_path / "Quarantine"
        if quarantine_dir.exists():
            metrics["quarantined_operations"] = len(list(quarantine_dir.glob("quarantine_*.json")))

        return metrics

# Global error recovery manager instance
error_recovery_manager = ErrorRecoveryManager()

def get_error_recovery_manager() -> ErrorRecoveryManager:
    """Get the global error recovery manager instance"""
    return error_recovery_manager

def execute_with_recovery(operation: Callable,
                        context: str = "",
                        max_retries: int = 3,
                        backoff_factor: float = 1.0,
                        recovery_strategy: RecoveryStrategy = RecoveryStrategy.RETRY,
                        fallback_operation: Optional[Callable] = None) -> Dict[str, Any]:
    """Convenience function to execute with recovery"""
    return error_recovery_manager.execute_with_recovery(
        operation, context, max_retries, backoff_factor,
        recovery_strategy, fallback_operation
    )

def backup_state(state: Dict[str, Any], label: str = ""):
    """Convenience function to backup state"""
    return error_recovery_manager.backup_state(state, label)

def quarantine_failed_operation(operation_data: Dict[str, Any], error: Exception):
    """Convenience function to quarantine failed operations"""
    return error_recovery_manager.quarantine_failed_operation(operation_data, error)

def get_system_resilience_metrics() -> Dict[str, Any]:
    """Convenience function to get resilience metrics"""
    return error_recovery_manager.get_system_resilience_metrics()

if __name__ == "__main__":
    # Example usage
    print("Error Recovery Manager initialized")

    # Test recovery execution
    def test_operation():
        # Simulate an operation that might fail
        import random
        if random.random() < 0.7:  # 70% chance of failure
            raise Exception("Simulated operation failure")
        return "Success!"

    def fallback_operation():
        return "Fallback success!"

    result = execute_with_recovery(
        test_operation,
        context="test_operation",
        max_retries=2,
        fallback_operation=fallback_operation
    )

    print(f"Execution result: {result}")

    # Test metrics
    metrics = get_system_resilience_metrics()
    print(f"System resilience metrics: {metrics}")