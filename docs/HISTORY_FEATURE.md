# Script History Tracking Feature

## Overview
The Monaco Editor now includes a comprehensive history tracking system that records all script updates with detailed metadata.

## Features

### 1. **Update Message Input**
- When saving a script, users can now provide an update message describing their changes
- Message is displayed in a text area below the filename input
- Examples: "Fixed bug in function X", "Added new feature Y", "Refactored code"
- If no message is provided, it defaults to "No message provided"

### 2. **Automatic History Recording**
Every time a script is saved, the system automatically records:
- **Filename**: The name of the file that was saved
- **Timestamp**: Date and time of the update (format: YYYY-MM-DD HH:MM:SS)
- **User**: System username of the person who made the update
- **Update Message**: The description provided by the user
- **File Size**: Number of characters in the saved script

### 3. **Show History Button**
- Located in the action buttons row alongside "Save to File" and "Run Script"
- Click to toggle the history display on/off
- Shows a comprehensive view of all updates

### 4. **History Display**
When history is shown, you'll see:
- **Expandable Cards**: Each update is shown in an expandable card
- **Newest First**: Updates are displayed in reverse chronological order
- **Detailed Information**: Each entry shows all recorded metadata
- **First Entry Expanded**: The most recent update is automatically expanded

### 5. **Sidebar Statistics**
The sidebar now includes a "History Stats" section showing:
- **Total Updates Count**: Number of saves recorded
- **Last Update Info**: Timestamp and user of the most recent save
- Quick at-a-glance visibility of activity

### 6. **Clear History**
- Option to clear all history records
- Removes the `.script_history.json` file
- Confirmation message displayed after clearing

## Technical Details

### Storage
- History is stored in `.script_history.json` file in the project root
- JSON format for easy parsing and portability
- Persists across application restarts

### Data Structure
```json
{
  "filename": "handler.py",
  "timestamp": "2026-01-12 12:30:07",
  "user": "username",
  "update_message": "Fixed bug in function",
  "file_size": 1234
}
```

### Files Modified
- `monaco-editor.py`: Main application file with history tracking logic
- `.script_history.json`: Auto-generated history storage (gitignored)
- `.gitignore`: Added to exclude history file from version control

## Usage Example

1. Edit your code in the Monaco editor
2. Enter a filename (e.g., `my_script.py`)
3. Add an update message (e.g., "Added error handling")
4. Click "💾 Save to File"
5. Click "📜 Show History" to view all updates
6. See your update with timestamp, username, and message

## Benefits

- **Accountability**: Know who made changes and when
- **Documentation**: Update messages provide context for changes
- **Audit Trail**: Complete history of all modifications
- **Collaboration**: Better understanding of code evolution
- **Recovery**: Can reference when specific changes were made

