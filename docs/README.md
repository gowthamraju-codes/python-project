# Python Script Editor with Monaco

A web-based Python script editor powered by Monaco Editor (the same editor used in VS Code) and Streamlit.

## Features

✨ **Monaco Editor Integration**
- Full-featured code editor with syntax highlighting
- IntelliSense and auto-completion
- Multiple themes (Dark, Light, High Contrast)
- Customizable font size and minimap

🚀 **Script Execution**
- Load and edit handler.py directly in the browser
- Execute Python scripts locally with live output
- View stdout and stderr separately
- 30-second timeout for safety

💾 **File Operations**
- Save edited scripts back to file
- Reload handler.py from disk
- Persist changes across sessions

## Installation

All required packages are already installed. The dependencies are:
- streamlit
- streamlit-monaco-editor
- boto3 (optional, for AWS features)

## Usage

### Quick Start

Run the launch script:
```bash
./launch_editor.sh
```

Or manually:
```bash
source .venv/bin/activate
streamlit run monaco-editor.py
```

### Opening the Application

Once started, Streamlit will automatically open your default browser to:
- Local URL: http://localhost:8501
- Network URL: http://YOUR_IP:8501

If the browser doesn't open automatically, copy and paste the Local URL into your browser.

## Application Interface

### Main Editor
- The Monaco editor displays the content of `handler.py` on startup
- Edit the code directly in the browser with full syntax highlighting
- Changes are tracked in the session

### Sidebar Controls
- **Theme**: Switch between dark, light, and high-contrast themes
- **Font Size**: Adjust editor font size (10-24px)
- **Show Minimap**: Toggle the code minimap view
- **Reload handler.py**: Reset editor to the current file content

### Action Buttons
- **💾 Save to File**: Save the edited code back to handler.py
- **▶️ Run Script**: Execute the script locally and view output

### Output Display
- Execution output appears below the editor
- Shows both STDOUT and STDERR
- Displays success/failure status
- Includes execution time and error messages

## Current Script

The editor currently loads `handler.py`, which contains:
- A MediaConvert job JSON generator
- Functions to create AWS MediaConvert job configurations
- Example usage with sample inputs

## Tips

1. **Edit Safely**: Use the "Reload" button to reset to the original file
2. **Test Changes**: Run the script before saving to test your changes
3. **View Output**: Check the execution output for any errors or results
4. **Customize**: Adjust theme and font size for your preference

## Troubleshooting

If you encounter issues:

1. **Port already in use**: Stop other Streamlit instances or change the port:
   ```bash
   streamlit run monaco-editor.py --server.port 8502
   ```

2. **Import errors**: Ensure you're using the virtual environment:
   ```bash
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Script execution fails**: Check the error output for Python syntax errors

## Files

- `monaco-editor.py` - Main Streamlit application
- `handler.py` - Python script being edited
- `launch_editor.sh` - Quick launch script
- `requirements.txt` - Python dependencies

## Keyboard Shortcuts (Monaco Editor)

- `Cmd/Ctrl + S` - Save (in editor, triggers browser save)
- `Cmd/Ctrl + F` - Find
- `Cmd/Ctrl + H` - Find and Replace
- `Cmd/Ctrl + /` - Toggle comment
- `Alt + Up/Down` - Move line up/down
- `Shift + Alt + Up/Down` - Copy line up/down

Enjoy coding! 🎉

