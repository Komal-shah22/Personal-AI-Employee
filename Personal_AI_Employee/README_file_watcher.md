# File Watcher Setup Guide

The File Watcher automatically monitors a desktop drop folder and processes any files you add to it.

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the watcher**:
   ```bash
   python watchers/file_watcher.py
   ```

3. **Drop files**: The watcher creates `~/Desktop/AI_Drop_Folder/` automatically. Just drag and drop files there.

## How It Works

### Monitored Folder
- **Location**: `~/Desktop/AI_Drop_Folder/`
- Created automatically on first run
- Monitors for any new files added

### File Processing

When you drop a file:
1. **Waits for file to be ready** (handles locked files, retries after 2 seconds)
2. **Copies to action folder**: `AI_Employee_Vault/Needs_Action/`
3. **Creates metadata file**: Companion `.md` file with file details
4. **Sends desktop notification**: "New File Detected" with file type
5. **Logs activity**: All actions logged to `AI_Employee_Vault/Logs/file_watcher.log`

### File Type Detection

The watcher automatically detects file types:

| Extension | Detected Type | Suggested Actions |
|-----------|---------------|-------------------|
| `.pdf` | invoice | Review invoice, verify amount, process payment |
| `.csv`, `.xlsx`, `.xls` | data | Review data, validate format, import to system |
| `.jpg`, `.jpeg`, `.png` | image | Review content, determine purpose, process |
| `.docx`, `.doc`, `.txt` | document | Read document, determine action, respond |
| Other | unknown | Identify type and purpose |

### Duplicate Handling

If a file with the same name already exists:
- Adds timestamp suffix: `filename_20260216_143022.ext`
- Logs the duplicate and new name
- Processes normally

### Error Handling

**Permission Denied**:
- Logs error and skips file
- Continues monitoring

**File Locked**:
- Retries up to 5 times with 2-second delays
- Skips if still locked after retries

**Temporary Files**:
- Ignores files starting with `.` or `~`
- Ignores `.md` files (metadata)

## Metadata File Format

Each processed file gets a companion markdown file:

```markdown
---
type: file_drop
original_name: invoice.pdf
size: 245.67 KB
size_bytes: 251584
date_added: 2026-02-16T14:30:22
detected_type: invoice
file_location: invoice.pdf
status: pending
---

# File Drop: invoice.pdf

## File Information
- **Original Name**: invoice.pdf
- **Size**: 245.67 KB
- **Detected Type**: INVOICE
- **Date Added**: 2026-02-16T14:30:22
- **Location**: `AI_Employee_Vault/Needs_Action/invoice.pdf`

## Suggested Actions
- [ ] Review invoice details
- [ ] Verify amount and vendor
- [ ] Process payment if approved
- [ ] File in accounting system

## Notes
Add any additional notes or context about this file here.
```

## Desktop Notifications

The watcher sends native desktop notifications:
- **Title**: "New File Detected"
- **Message**: Filename and detected type
- **Duration**: 5 seconds
- **App Name**: "AI Employee"

### Platform Support
- **Windows**: Uses Windows Toast notifications
- **macOS**: Uses native notification center
- **Linux**: Uses notify-send or similar

## Logs

View logs in real-time:
```bash
tail -f AI_Employee_Vault/Logs/file_watcher.log
```

Log entries include:
- Timestamp of each file detection
- File processing steps
- Copy operations
- Metadata creation
- Errors and warnings

## Usage Examples

### Example 1: Invoice Processing
1. Save invoice PDF to `~/Desktop/AI_Drop_Folder/`
2. Watcher detects it as "invoice" type
3. Creates action item with invoice-specific checklist
4. You receive notification
5. Process via dashboard or orchestrator

### Example 2: Data Import
1. Export CSV from external system
2. Drop into AI_Drop_Folder
3. Watcher detects as "data" type
4. Creates action item with data validation checklist
5. Import script can pick it up from Needs_Action folder

### Example 3: Receipt Scanning
1. Scan receipt to JPG
2. Drop into AI_Drop_Folder
3. Watcher detects as "image" type
4. Creates action item for review
5. Can be processed by OCR or manual review

## Integration with AI Employee

The File Watcher integrates seamlessly:

1. **Orchestrator**: Can pick up file_drop tasks from Needs_Action
2. **Dashboard**: Shows file drops in activity feed
3. **Skills**: Custom skills can process specific file types
4. **Approval Flow**: High-value files can trigger approval requests

## Running as a Service

### Windows (Task Scheduler)
1. Open Task Scheduler
2. Create Basic Task: "AI File Watcher"
3. Trigger: At startup
4. Action: Start a program
   - Program: `python`
   - Arguments: `E:\hackathon-0\Personal_AI_Employee\watchers\file_watcher.py`
   - Start in: `E:\hackathon-0\Personal_AI_Employee`

### Linux/Mac (systemd)
Create `/etc/systemd/system/ai-file-watcher.service`:
```ini
[Unit]
Description=AI Employee File Watcher
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/Personal_AI_Employee
ExecStart=/usr/bin/python3 watchers/file_watcher.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable ai-file-watcher
sudo systemctl start ai-file-watcher
```

### Mac (launchd)
Create `~/Library/LaunchAgents/com.ai-employee.file-watcher.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ai-employee.file-watcher</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/Personal_AI_Employee/watchers/file_watcher.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

Load:
```bash
launchctl load ~/Library/LaunchAgents/com.ai-employee.file-watcher.plist
```

## Customization

### Change Drop Folder Location
Edit `watchers/file_watcher.py`:
```python
DROP_FOLDER = Path.home() / "Desktop" / "AI_Drop_Folder"
# Change to:
DROP_FOLDER = Path("C:/MyCustomFolder")
```

### Add Custom File Types
Edit the `FILE_TYPE_MAP` dictionary:
```python
FILE_TYPE_MAP = {
    '.pdf': 'invoice',
    '.py': 'code',  # Add custom type
    '.sql': 'database_script',  # Add custom type
    # ... more types
}
```

Then add corresponding actions in `SUGGESTED_ACTIONS`:
```python
SUGGESTED_ACTIONS = {
    'code': [
        '- [ ] Review code for security issues',
        '- [ ] Run tests',
        '- [ ] Deploy if approved'
    ],
    # ... more actions
}
```

### Adjust Retry Settings
Edit the `wait_for_file_ready` method:
```python
def wait_for_file_ready(self, file_path: Path, max_attempts: int = 5):
    # Change max_attempts or sleep duration
```

## Troubleshooting

### No notifications appearing
- **Windows**: Check notification settings in Windows Settings
- **macOS**: Check System Preferences > Notifications
- **Linux**: Ensure `notify-send` is installed

### Files not being detected
- Check the watcher is running: `ps aux | grep file_watcher`
- Verify drop folder path: `~/Desktop/AI_Drop_Folder/`
- Check logs: `tail -f AI_Employee_Vault/Logs/file_watcher.log`

### Permission errors
- Ensure write permissions on `AI_Employee_Vault/Needs_Action/`
- Run with appropriate user permissions
- Check file ownership

### File locked errors
- Close the file in other applications
- Wait a few seconds after saving before dropping
- Watcher will retry automatically

## Security Notes

- Files are copied, not moved (originals remain in drop folder)
- No automatic execution of code files
- All file operations are logged
- Metadata files are plain text markdown

## Performance

- Minimal CPU usage when idle
- Processes files immediately upon detection
- Handles multiple files dropped simultaneously
- No file size limits (but large files take longer to copy)

---

**Need Help?**
- Check logs: `AI_Employee_Vault/Logs/file_watcher.log`
- Verify drop folder exists: `~/Desktop/AI_Drop_Folder/`
- Ensure dependencies installed: `pip install -r requirements.txt`
