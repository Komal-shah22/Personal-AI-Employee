"""
Comprehensive Audit Logging for Personal AI Employee

Implements detailed audit logging for compliance and security
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from enum import Enum
import hashlib
import threading
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuditEventType(Enum):
    TASK_CREATED = "task_created"
    TASK_COMPLETED = "task_completed"
    EMAIL_PROCESSED = "email_processed"
    FILE_ACCESSED = "file_accessed"
    SKILL_EXECUTED = "skill_executed"
    MCP_CALLED = "mcp_called"
    APPROVAL_REQUESTED = "approval_requested"
    APPROVAL_GRANTED = "approval_granted"
    APPROVAL_DENIED = "approval_denied"
    SECURITY_EVENT = "security_event"
    SYSTEM_STARTED = "system_started"
    SYSTEM_STOPPED = "system_stopped"
    CONFIG_CHANGED = "config_changed"
    DATA_EXPORTED = "data_exported"

class AuditLogger:
    def __init__(self, vault_path: str = "../AI_Employee_Vault"):
        self.vault_path = Path(vault_path)
        self.audit_dir = self.vault_path / "Audit"

        # Create necessary directories
        self.audit_dir.mkdir(parents=True, exist_ok=True)

        # Thread lock for concurrent access
        self.lock = threading.Lock()

    def log_event(self,
                  event_type: AuditEventType,
                  actor: str,
                  target: str,
                  details: Dict[str, Any] = None,
                  severity: str = "info") -> str:
        """
        Log an audit event with comprehensive details
        """
        with self.lock:
            # Create audit entry
            audit_entry = {
                "timestamp": datetime.now().isoformat(),
                "event_type": event_type.value,
                "actor": actor,
                "target": target,
                "severity": severity,
                "details": details or {},
                "session_id": os.environ.get("SESSION_ID", ""),
                "thread_id": threading.current_thread().ident,
                "process_id": os.getpid()
            }

            # Add hash for integrity verification
            audit_entry["hash"] = self._calculate_hash(audit_entry)

            # Write to daily audit log
            audit_file = self.audit_dir / f"audit_{datetime.now().strftime('%Y-%m-%d')}.log"
            with open(audit_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(audit_entry) + "\n")

            logger.info(f"Audit event logged: {event_type.value} by {actor}")

            # Return the audit entry ID
            return audit_entry["hash"]

    def _calculate_hash(self, audit_entry: Dict[str, Any]) -> str:
        """Calculate hash for audit entry integrity"""
        # Remove hash field if present before calculating
        entry_copy = {k: v for k, v in audit_entry.items() if k != "hash"}
        entry_json = json.dumps(entry_copy, sort_keys=True, default=str)
        return hashlib.sha256(entry_json.encode()).hexdigest()

    def search_events(self,
                     event_types: List[AuditEventType] = None,
                     start_date: datetime = None,
                     end_date: datetime = None,
                     actor: str = None,
                     target: str = None,
                     severity: str = None,
                     limit: int = 100) -> List[Dict[str, Any]]:
        """
        Search audit events with various filters
        """
        results = []

        # Determine date range
        if not start_date:
            start_date = datetime.now() - timedelta(days=7)  # Last 7 days
        if not end_date:
            end_date = datetime.now()

        # Search through audit files in date range
        for i in range((end_date - start_date).days + 1):
            date = start_date + timedelta(days=i)
            audit_file = self.audit_dir / f"audit_{date.strftime('%Y-%m-%d')}.log"

            if not audit_file.exists():
                continue

            try:
                with open(audit_file, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        try:
                            audit_entry = json.loads(line.strip())

                            # Apply filters
                            if event_types and audit_entry["event_type"] not in [et.value for et in event_types]:
                                continue
                            if actor and audit_entry["actor"] != actor:
                                continue
                            if target and audit_entry["target"] != target:
                                continue
                            if severity and audit_entry["severity"] != severity:
                                continue

                            # Check timestamp is within range
                            entry_time = datetime.fromisoformat(audit_entry["timestamp"])
                            if not (start_date <= entry_time <= end_date):
                                continue

                            results.append(audit_entry)

                            # Limit results
                            if len(results) >= limit:
                                return results

                        except json.JSONDecodeError:
                            logger.warning(f"Invalid JSON in audit log {audit_file}:{line_num}")
                            continue
                        except Exception as e:
                            logger.error(f"Error processing audit log {audit_file}:{line_num}: {e}")
                            continue

            except Exception as e:
                logger.error(f"Error reading audit file {audit_file}: {e}")
                continue

        return results

    def get_event_statistics(self,
                           start_date: datetime = None,
                           end_date: datetime = None) -> Dict[str, Any]:
        """
        Get statistics about audit events
        """
        stats = {
            "total_events": 0,
            "events_by_type": {},
            "events_by_severity": {},
            "actors": {},
            "date_range": {
                "start": start_date.isoformat() if start_date else None,
                "end": end_date.isoformat() if end_date else None
            }
        }

        # Determine date range
        if not start_date:
            start_date = datetime.now() - timedelta(days=7)  # Last 7 days
        if not end_date:
            end_date = datetime.now()

        # Collect statistics
        for i in range((end_date - start_date).days + 1):
            date = start_date + timedelta(days=i)
            audit_file = self.audit_dir / f"audit_{date.strftime('%Y-%m-%d')}.log"

            if not audit_file.exists():
                continue

            try:
                with open(audit_file, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        try:
                            audit_entry = json.loads(line.strip())

                            # Check timestamp is within range
                            entry_time = datetime.fromisoformat(audit_entry["timestamp"])
                            if not (start_date <= entry_time <= end_date):
                                continue

                            # Update statistics
                            stats["total_events"] += 1

                            # Count by type
                            event_type = audit_entry["event_type"]
                            stats["events_by_type"][event_type] = stats["events_by_type"].get(event_type, 0) + 1

                            # Count by severity
                            severity = audit_entry["severity"]
                            stats["events_by_severity"][severity] = stats["events_by_severity"].get(severity, 0) + 1

                            # Count actors
                            actor = audit_entry["actor"]
                            stats["actors"][actor] = stats["actors"].get(actor, 0) + 1

                        except json.JSONDecodeError:
                            continue
                        except Exception:
                            continue

            except Exception:
                continue

        return stats

    def verify_integrity(self, start_date: datetime = None, end_date: datetime = None) -> Dict[str, Any]:
        """
        Verify the integrity of audit logs
        """
        if not start_date:
            start_date = datetime.now() - timedelta(days=7)  # Last 7 days
        if not end_date:
            end_date = datetime.now()

        verification_results = {
            "verified": True,
            "issues": [],
            "total_entries": 0,
            "valid_entries": 0,
            "invalid_entries": 0
        }

        for i in range((end_date - start_date).days + 1):
            date = start_date + timedelta(days=i)
            audit_file = self.audit_dir / f"audit_{date.strftime('%Y-%m-%d')}.log"

            if not audit_file.exists():
                continue

            try:
                with open(audit_file, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        try:
                            audit_entry = json.loads(line.strip())
                            expected_hash = audit_entry.get("hash")

                            # Verify hash
                            calculated_hash = self._calculate_hash(audit_entry)

                            if expected_hash != calculated_hash:
                                verification_results["verified"] = False
                                verification_results["issues"].append({
                                    "file": str(audit_file),
                                    "line": line_num,
                                    "issue": "Hash mismatch",
                                    "expected": expected_hash,
                                    "calculated": calculated_hash
                                })
                                verification_results["invalid_entries"] += 1
                            else:
                                verification_results["valid_entries"] += 1

                        except json.JSONDecodeError:
                            verification_results["verified"] = False
                            verification_results["issues"].append({
                                "file": str(audit_file),
                                "line": line_num,
                                "issue": "Invalid JSON"
                            })
                            verification_results["invalid_entries"] += 1
                        except Exception as e:
                            verification_results["verified"] = False
                            verification_results["issues"].append({
                                "file": str(audit_file),
                                "line": line_num,
                                "issue": f"Verification error: {str(e)}"
                            })
                            verification_results["invalid_entries"] += 1

                        verification_results["total_entries"] += 1

            except Exception as e:
                verification_results["verified"] = False
                verification_results["issues"].append({
                    "file": str(audit_file),
                    "issue": f"File read error: {str(e)}"
                })

        return verification_results

    def export_audit_data(self,
                         output_path: str,
                         start_date: datetime = None,
                         end_date: datetime = None,
                         event_types: List[AuditEventType] = None) -> bool:
        """
        Export audit data to a file
        """
        try:
            events = self.search_events(
                event_types=event_types,
                start_date=start_date,
                end_date=end_date
            )

            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "exporter": "audit_logger",
                "total_events": len(events),
                "date_range": {
                    "start": start_date.isoformat() if start_date else None,
                    "end": end_date.isoformat() if end_date else None
                },
                "events": events
            }

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, default=str)

            logger.info(f"Audit data exported to {output_path}")
            return True

        except Exception as e:
            logger.error(f"Error exporting audit data: {e}")
            return False

    def get_compliance_report(self, start_date: datetime = None, end_date: datetime = None) -> Dict[str, Any]:
        """
        Generate a compliance report
        """
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)  # Last 30 days
        if not end_date:
            end_date = datetime.now()

        stats = self.get_event_statistics(start_date, end_date)
        integrity = self.verify_integrity(start_date, end_date)

        report = {
            "report_timestamp": datetime.now().isoformat(),
            "date_range": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            },
            "summary": {
                "total_events": stats["total_events"],
                "unique_actors": len(stats["actors"]),
                "integrity_verified": integrity["verified"]
            },
            "statistics": stats,
            "integrity": integrity,
            "recommendations": []
        }

        # Add recommendations based on findings
        if not integrity["verified"]:
            report["recommendations"].append("Audit log integrity compromised - investigate immediately")

        if stats["total_events"] == 0:
            report["recommendations"].append("No audit events recorded - verify audit logging is enabled")

        if "security_event" in stats["events_by_type"]:
            report["recommendations"].append("Security events detected - review security logs")

        return report

# Global audit logger instance
audit_logger = AuditLogger()

def get_audit_logger() -> AuditLogger:
    """Get the global audit logger instance"""
    return audit_logger

def log_audit_event(event_type: AuditEventType,
                   actor: str,
                   target: str,
                   details: Dict[str, Any] = None,
                   severity: str = "info") -> str:
    """Convenience function to log audit events"""
    return audit_logger.log_event(event_type, actor, target, details, severity)

def search_audit_events(event_types: List[AuditEventType] = None,
                       start_date: datetime = None,
                       end_date: datetime = None,
                       actor: str = None,
                       target: str = None,
                       severity: str = None,
                       limit: int = 100) -> List[Dict[str, Any]]:
    """Convenience function to search audit events"""
    return audit_logger.search_events(event_types, start_date, end_date, actor, target, severity, limit)

def get_audit_statistics(start_date: datetime = None, end_date: datetime = None) -> Dict[str, Any]:
    """Convenience function to get audit statistics"""
    return audit_logger.get_event_statistics(start_date, end_date)

def verify_audit_integrity(start_date: datetime = None, end_date: datetime = None) -> Dict[str, Any]:
    """Convenience function to verify audit integrity"""
    return audit_logger.verify_integrity(start_date, end_date)

def generate_compliance_report(start_date: datetime = None, end_date: datetime = None) -> Dict[str, Any]:
    """Convenience function to generate compliance report"""
    return audit_logger.get_compliance_report(start_date, end_date)

@contextmanager
def audit_context(event_type: AuditEventType, actor: str, target: str, details: Dict[str, Any] = None):
    """Context manager for audit logging"""
    start_time = datetime.now()
    try:
        yield
        # Log successful completion
        log_audit_event(
            event_type,
            actor,
            target,
            {**(details or {}), "duration": (datetime.now() - start_time).total_seconds()},
            "info"
        )
    except Exception as e:
        # Log failure
        log_audit_event(
            event_type,
            actor,
            target,
            {**(details or {}), "error": str(e), "duration": (datetime.now() - start_time).total_seconds()},
            "error"
        )
        raise

if __name__ == "__main__":
    # Example usage
    print("Audit Logger initialized")

    # Test logging
    event_id = log_audit_event(
        AuditEventType.TASK_CREATED,
        "test_user",
        "test_task",
        {"task_name": "Test Task", "priority": "high"},
        "info"
    )
    print(f"Logged event with ID: {event_id}")

    # Test search
    events = search_audit_events(
        event_types=[AuditEventType.TASK_CREATED],
        start_date=datetime.now() - timedelta(hours=1)
    )
    print(f"Found {len(events)} events")

    # Test statistics
    stats = get_audit_statistics()
    print(f"Audit stats: {stats}")

    # Test compliance report
    report = generate_compliance_report()
    print(f"Compliance report generated with {report['summary']['total_events']} events")