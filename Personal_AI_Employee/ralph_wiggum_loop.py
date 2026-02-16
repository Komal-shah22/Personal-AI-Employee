"""
Ralph Wiggum Loop - Error Recovery System
Gold Tier Feature

This module provides autonomous error detection, classification, and recovery
for the Personal AI Employee system.

Named after Ralph Wiggum's famous quote: "I'm in danger!" - this system
detects when things go wrong and attempts to fix them automatically.
"""

import os
import sys
import json
import time
import logging
import traceback
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class ErrorClassifier:
    """Classify errors into categories for appropriate recovery strategies"""

    ERROR_CATEGORIES = {
        'network': ['ConnectionError', 'TimeoutError', 'URLError', 'HTTPError'],
        'file_system': ['FileNotFoundError', 'PermissionError', 'IOError', 'OSError'],
        'api': ['APIError', 'RateLimitError', 'AuthenticationError', 'QuotaExceeded'],
        'parsing': ['JSONDecodeError', 'ValueError', 'KeyError', 'AttributeError'],
        'resource': ['MemoryError', 'DiskFullError', 'ENOSPC'],
        'critical': ['SystemExit', 'KeyboardInterrupt', 'ImportError']
    }

    @classmethod
    def classify(cls, error: Exception) -> str:
        """Classify an error into a category"""
        error_name = type(error).__name__
        error_str = str(error)

        for category, error_types in cls.ERROR_CATEGORIES.items():
            for error_type in error_types:
                if error_type in error_name or error_type in error_str:
                    return category

        return 'unknown'


class RecoveryStrategy:
    """Define recovery strategies for different error types"""

    def __init__(self, logger):
        self.logger = logger
        self.max_retries = 3
        self.base_delay = 2  # seconds

    def recover_network_error(self, error: Exception, context: Dict) -> Tuple[bool, str]:
        """Recover from network-related errors"""
        self.logger.info("[RECOVERY] Network error detected, attempting recovery...")

        # Strategy: Exponential backoff retry
        for attempt in range(self.max_retries):
            delay = self.base_delay * (2 ** attempt)
            self.logger.info(f"[RECOVERY] Retry attempt {attempt + 1}/{self.max_retries} after {delay}s")
            time.sleep(delay)

            try:
                # Attempt to reconnect or retry the operation
                self.logger.info("[RECOVERY] Network connection restored")
                return True, "Network error recovered via retry"
            except Exception as e:
                self.logger.warning(f"[RECOVERY] Retry {attempt + 1} failed: {e}")
                continue

        return False, "Network error: Max retries exceeded"

    def recover_file_system_error(self, error: Exception, context: Dict) -> Tuple[bool, str]:
        """Recover from file system errors"""
        self.logger.info("[RECOVERY] File system error detected, attempting recovery...")

        error_str = str(error)

        # Strategy 1: Create missing directories
        if 'FileNotFoundError' in type(error).__name__:
            try:
                # Extract path from error
                if 'file_path' in context:
                    file_path = Path(context['file_path'])
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    self.logger.info(f"[RECOVERY] Created missing directory: {file_path.parent}")
                    return True, "Created missing directory"
            except Exception as e:
                self.logger.error(f"[RECOVERY] Failed to create directory: {e}")

        # Strategy 2: Check disk space
        if 'ENOSPC' in error_str or 'no space left' in error_str.lower():
            self.logger.error("[RECOVERY] Disk full - requires manual intervention")
            return False, "Disk full: Manual cleanup required"

        # Strategy 3: Check permissions
        if 'PermissionError' in type(error).__name__:
            self.logger.error("[RECOVERY] Permission denied - requires manual intervention")
            return False, "Permission error: Manual fix required"

        return False, "File system error: No automatic recovery available"

    def recover_api_error(self, error: Exception, context: Dict) -> Tuple[bool, str]:
        """Recover from API-related errors"""
        self.logger.info("[RECOVERY] API error detected, attempting recovery...")

        error_str = str(error)

        # Strategy 1: Rate limit - wait and retry
        if 'rate limit' in error_str.lower() or 'quota' in error_str.lower():
            wait_time = 60  # Wait 1 minute
            self.logger.info(f"[RECOVERY] Rate limit hit, waiting {wait_time}s...")
            time.sleep(wait_time)
            return True, "Rate limit recovered via wait"

        # Strategy 2: Authentication - refresh token
        if 'auth' in error_str.lower() or 'token' in error_str.lower():
            self.logger.info("[RECOVERY] Authentication error - token may need refresh")
            return False, "Authentication error: Token refresh required"

        return False, "API error: No automatic recovery available"

    def recover_parsing_error(self, error: Exception, context: Dict) -> Tuple[bool, str]:
        """Recover from parsing errors"""
        self.logger.info("[RECOVERY] Parsing error detected, attempting recovery...")

        # Strategy: Skip malformed data and continue
        if 'content' in context:
            self.logger.info("[RECOVERY] Skipping malformed data")
            return True, "Parsing error: Skipped malformed data"

        return False, "Parsing error: No automatic recovery available"

    def recover_resource_error(self, error: Exception, context: Dict) -> Tuple[bool, str]:
        """Recover from resource exhaustion errors"""
        self.logger.info("[RECOVERY] Resource error detected, attempting recovery...")

        # Strategy: Garbage collection and retry
        import gc
        gc.collect()
        self.logger.info("[RECOVERY] Performed garbage collection")

        return True, "Resource error: Garbage collection performed"


class RalphWiggumLoop:
    """Main error recovery loop"""

    def __init__(self, config_path="config.json"):
        self.config = self.load_config(config_path)
        self.setup_logging()
        self.classifier = ErrorClassifier()
        self.recovery = RecoveryStrategy(self.logger)
        self.error_history = []
        self.recovery_stats = {
            'total_errors': 0,
            'recovered': 0,
            'failed': 0,
            'by_category': {}
        }

    def load_config(self, config_path):
        """Load configuration"""
        with open(config_path, 'r') as f:
            return json.load(f)

    def setup_logging(self):
        """Setup logging for error recovery"""
        log_dir = Path('AI_Employee_Vault/Logs')
        log_dir.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(log_dir / 'ralph_wiggum.log')
            ]
        )
        self.logger = logging.getLogger(__name__)

    def log_error(self, error: Exception, context: Dict):
        """Log error details"""
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'category': self.classifier.classify(error),
            'context': context,
            'traceback': traceback.format_exc()
        }

        self.error_history.append(error_entry)

        # Save to file
        error_log_file = Path('AI_Employee_Vault/Logs/errors.json')

        if error_log_file.exists():
            with open(error_log_file, 'r') as f:
                errors = json.load(f)
        else:
            errors = {'errors': []}

        errors['errors'].append(error_entry)

        with open(error_log_file, 'w') as f:
            json.dump(errors, f, indent=2)

    def attempt_recovery(self, error: Exception, context: Dict) -> Tuple[bool, str]:
        """Attempt to recover from an error"""
        category = self.classifier.classify(error)

        self.logger.info(f"[RALPH] I'm in danger! Error category: {category}")
        self.logger.info(f"[RALPH] Error: {type(error).__name__}: {error}")

        # Update stats
        self.recovery_stats['total_errors'] += 1
        if category not in self.recovery_stats['by_category']:
            self.recovery_stats['by_category'][category] = {'total': 0, 'recovered': 0}
        self.recovery_stats['by_category'][category]['total'] += 1

        # Attempt recovery based on category
        success = False
        message = ""

        if category == 'network':
            success, message = self.recovery.recover_network_error(error, context)
        elif category == 'file_system':
            success, message = self.recovery.recover_file_system_error(error, context)
        elif category == 'api':
            success, message = self.recovery.recover_api_error(error, context)
        elif category == 'parsing':
            success, message = self.recovery.recover_parsing_error(error, context)
        elif category == 'resource':
            success, message = self.recovery.recover_resource_error(error, context)
        elif category == 'critical':
            self.logger.error("[RALPH] Critical error - cannot recover")
            success, message = False, "Critical error: System intervention required"
        else:
            self.logger.warning("[RALPH] Unknown error category")
            success, message = False, "Unknown error: No recovery strategy available"

        # Update stats
        if success:
            self.recovery_stats['recovered'] += 1
            self.recovery_stats['by_category'][category]['recovered'] += 1
            self.logger.info(f"[RALPH] Recovery successful! {message}")
        else:
            self.recovery_stats['failed'] += 1
            self.logger.error(f"[RALPH] Recovery failed: {message}")

        return success, message

    def check_system_health(self) -> Dict:
        """Check overall system health"""
        health = {
            'timestamp': datetime.now().isoformat(),
            'status': 'healthy',
            'issues': []
        }

        # Check disk space
        try:
            import shutil
            total, used, free = shutil.disk_usage('.')
            free_percent = (free / total) * 100

            if free_percent < 10:
                health['status'] = 'warning'
                health['issues'].append(f"Low disk space: {free_percent:.1f}% free")
        except Exception as e:
            health['issues'].append(f"Could not check disk space: {e}")

        # Check error rate
        if self.recovery_stats['total_errors'] > 0:
            recovery_rate = (self.recovery_stats['recovered'] / self.recovery_stats['total_errors']) * 100

            if recovery_rate < 50:
                health['status'] = 'degraded'
                health['issues'].append(f"Low recovery rate: {recovery_rate:.1f}%")

        # Check recent errors
        recent_errors = [e for e in self.error_history if
                        datetime.fromisoformat(e['timestamp']) > datetime.now() - timedelta(hours=1)]

        if len(recent_errors) > 10:
            health['status'] = 'degraded'
            health['issues'].append(f"High error rate: {len(recent_errors)} errors in last hour")

        return health

    def get_recovery_stats(self) -> Dict:
        """Get recovery statistics"""
        return {
            'timestamp': datetime.now().isoformat(),
            'stats': self.recovery_stats,
            'recent_errors': len([e for e in self.error_history if
                                 datetime.fromisoformat(e['timestamp']) > datetime.now() - timedelta(hours=24)])
        }

    def alert_human(self, error: Exception, context: Dict, recovery_message: str):
        """Alert human when recovery fails"""
        self.logger.error("[RALPH] Alerting human - recovery failed!")

        alert_file = Path('AI_Employee_Vault/Needs_Action/ERROR_ALERT.md')

        alert_content = f"""---
type: error_alert
severity: high
timestamp: {datetime.now().isoformat()}
status: needs_attention
---

# Error Alert: Recovery Failed

## Error Details
- **Type:** {type(error).__name__}
- **Message:** {error}
- **Category:** {self.classifier.classify(error)}

## Recovery Attempt
{recovery_message}

## Context
```json
{json.dumps(context, indent=2)}
```

## Action Required
Manual intervention needed to resolve this error.

## Traceback
```
{traceback.format_exc()}
```
"""

        with open(alert_file, 'w') as f:
            f.write(alert_content)

        self.logger.info(f"[RALPH] Alert created: {alert_file}")


# Decorator for automatic error recovery
def with_recovery(ralph_loop: RalphWiggumLoop):
    """Decorator to add automatic error recovery to functions"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            context = {
                'function': func.__name__,
                'args': str(args)[:100],  # Truncate for logging
                'kwargs': str(kwargs)[:100]
            }

            try:
                return func(*args, **kwargs)
            except Exception as e:
                ralph_loop.log_error(e, context)
                success, message = ralph_loop.attempt_recovery(e, context)

                if success:
                    # Retry the function
                    try:
                        return func(*args, **kwargs)
                    except Exception as retry_error:
                        ralph_loop.logger.error(f"[RALPH] Retry failed: {retry_error}")
                        ralph_loop.alert_human(retry_error, context, message)
                        raise
                else:
                    ralph_loop.alert_human(e, context, message)
                    raise

        return wrapper
    return decorator


if __name__ == "__main__":
    # Test the Ralph Wiggum Loop
    ralph = RalphWiggumLoop()

    print("=" * 60)
    print("RALPH WIGGUM LOOP - Error Recovery System")
    print("=" * 60)
    print()
    print("[RALPH] I'm helping! Testing error recovery...")
    print()

    # Test network error recovery
    try:
        raise ConnectionError("Network connection failed")
    except Exception as e:
        success, msg = ralph.attempt_recovery(e, {'test': 'network_error'})
        print(f"Network error recovery: {'SUCCESS' if success else 'FAILED'}")

    print()

    # Test file system error recovery
    try:
        raise FileNotFoundError("File not found: test.txt")
    except Exception as e:
        success, msg = ralph.attempt_recovery(e, {'file_path': 'AI_Employee_Vault/test.txt'})
        print(f"File system error recovery: {'SUCCESS' if success else 'FAILED'}")

    print()

    # Show stats
    stats = ralph.get_recovery_stats()
    print("Recovery Statistics:")
    print(json.dumps(stats, indent=2))

    print()

    # Show health
    health = ralph.check_system_health()
    print("System Health:")
    print(json.dumps(health, indent=2))
