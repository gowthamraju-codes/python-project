# Quick Reference: History Tracking Feature

## New UI Elements

### Save Settings Section
```
💾 Save Settings
├── File name to save: [text input]
└── Update message: [text area - describes your changes]
```

### Action Buttons
```
┌─────────────────┬─────────────────┬─────────────────┐
│ 💾 Save to File │ ▶️ Run Script   │ 📜 Show History │
└─────────────────┴─────────────────┴─────────────────┘
```

### Sidebar Stats (New)
```
📊 History Stats
├── Total Updates: [count]
├── Last update: [timestamp]
└── By: [username]
```

### History Display (When toggled)
```
📜 Update History
├── 🕒 2026-01-12 12:30:07 - handler.py by user1 [expanded]
│   ├── File: handler.py
│   ├── User: user1
│   ├── Timestamp: 2026-01-12 12:30:07
│   ├── File Size: 1234 characters
│   └── Update Message: "Fixed bug in calculation"
│
├── 🕒 2026-01-12 11:15:32 - test.py by user2
│   └── [collapsed - click to expand]
│
└── [🗑️ Clear History] button
```

## Workflow

1. **Edit Code** → Monaco Editor
2. **Enter Filename** → e.g., "my_script.py"
3. **Add Update Message** → e.g., "Added error handling"
4. **Click Save** → Script saved + history recorded
5. **View History** → Click "Show History" button
6. **Review Updates** → See all past changes with details

## History JSON Structure

Location: `.script_history.json` (auto-created, gitignored)

```json
[
  {
    "filename": "handler.py",
    "timestamp": "2026-01-12 12:30:07",
    "user": "graju318@apac.comcast.com",
    "update_message": "Initial implementation",
    "file_size": 1234
  }
]
```

## Key Functions

### `save_script_to_file(script_code, filename, update_message)`
- Saves script to specified file
- Records history entry with metadata
- Persists history to `.script_history.json`
- Returns: `(success: bool, message: str)`

### History Entry Fields
- `filename`: Name of saved file
- `timestamp`: ISO format datetime
- `user`: System username (from `getpass.getuser()`)
- `update_message`: User-provided description
- `file_size`: Character count of saved script

## Tips

- ✅ Always add descriptive update messages
- ✅ History persists across app restarts
- ✅ Can track multiple files
- ✅ Chronological ordering (newest first)
- ✅ Clear history when needed
- ⚠️  History file is gitignored (not in version control)

