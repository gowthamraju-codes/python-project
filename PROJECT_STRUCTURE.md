# Python Project - Organized Structure

## Directory Layout

```
python-project/
├── src/                          # Python source files
│   ├── monaco-editor.py          # Main editor application
│   ├── handler.py                # Original MediaConvert handler
│   ├── alright-handler.py        # Custom variant
│   ├── alright-jackman-handler.py
│   ├── custom-handler.py
│   ├── custom-handler1.py
│   ├── handler-tryout.py
│   └── test_history.py           # Testing utilities
│
├── docs/                         # Documentation files
│   ├── README.md                 # Project overview
│   ├── CURSOR_FIX_FINAL.md      # Cursor reset fix documentation
│   ├── CURSOR_RESET_FIX.md      # Cursor reset issue details
│   ├── FILE_BROWSER_FEATURE.md  # File browser documentation
│   ├── HISTORY_FEATURE.md       # History tracking feature
│   ├── HISTORY_QUICK_REFERENCE.md
│   ├── SAVE_NEW_FILE_FEATURE.md
│   └── QUICK_FIX_SUMMARY.txt
│
├── scripts/                      # Shell scripts and launchers
│   └── launch_editor.sh         # Editor launcher script
│
├── config/                       # Configuration files
│   ├── requirements.txt         # Python dependencies
│   └── mediaconvert_job.json   # MediaConvert job configuration
│
├── .venv/                       # Python virtual environment (not in git)
├── .script_history.json         # Editor history (not in git)
├── .gitignore                   # Git ignore rules
└── python-project.iml           # IntelliJ project file
```

## Quick Start

### Launch the Editor
```bash
./scripts/launch_editor.sh
```
Or from the root directory:
```bash
source .venv/bin/activate
streamlit run src/monaco-editor.py
```

### Install Dependencies
```bash
pip install -r config/requirements.txt
```

## Folder Purposes

### `src/` - Source Code
Contains all Python source files:
- **monaco-editor.py** - The main web-based Python editor application
- **handler*.py** - Various MediaConvert handler implementations
- **test_history.py** - Testing utilities for history tracking

The editor automatically lists and allows editing of all `.py` files in this directory.

### `docs/` - Documentation
All markdown documentation and reference files:
- Feature documentation
- Fix notes and technical details
- Quick reference guides
- Original README

### `scripts/` - Executable Scripts
Shell scripts and launchers:
- **launch_editor.sh** - Convenient launcher for the editor application

### `config/` - Configuration Files
Configuration and dependency files:
- **requirements.txt** - Python package dependencies
- **mediaconvert_job.json** - Sample MediaConvert job configuration

## Features

### Monaco Editor
A web-based Python editor with:
- ✅ Multi-file editing (all files in src/)
- ✅ File browser dropdown
- ✅ Create new files
- ✅ Save with history tracking
- ✅ Run scripts and view output
- ✅ Theme customization
- ✅ No cursor reset issues
- ✅ VSCode keybindings

### History Tracking
Every save operation records:
- Filename
- Timestamp
- User
- Update message
- File size

View complete history via "Show History" button in the editor.

## Working with Files

### Editing Files
1. Launch editor: `./scripts/launch_editor.sh`
2. Select file from dropdown in sidebar
3. Edit in the Ace editor
4. Save with optional update message
5. View history of all changes

### Creating New Files
Two methods:
1. **Via sidebar:** Click "Create New File" section
2. **Via save:** Type new filename in save field, click save

New files are automatically:
- Created in `src/` directory
- Added to file browser dropdown
- Loaded in editor
- Ready to edit

### Running Scripts
1. Select/edit any Python file
2. Click "Run Script" button
3. View output below editor
4. Scripts execute with proper Python environment

## Git Ignored Files

The following are not tracked in git:
- `.venv/` - Virtual environment
- `__pycache__/` - Python cache
- `.script_history.json` - Editor history
- `*.pyc` - Compiled Python files
- `.idea/` - IDE settings (except .iml)

## Dependencies

Main packages (see `config/requirements.txt`):
- **streamlit** - Web application framework
- **streamlit-ace** - Ace code editor component
- **boto3** - AWS SDK for MediaConvert operations

## Development

### Adding New Python Files
Simply save with a new filename in the editor, or create a `.py` file in `src/` directory.

### Modifying Configuration
Edit `config/requirements.txt` for dependencies or `config/mediaconvert_job.json` for job templates.

### Updating Documentation
Add or edit markdown files in `docs/` directory.

## Troubleshooting

### Editor won't start
```bash
# Ensure dependencies are installed
source .venv/bin/activate
pip install -r config/requirements.txt

# Launch from project root
cd /path/to/python-project
./scripts/launch_editor.sh
```

### Files not appearing in dropdown
- Ensure files have `.py` extension
- Files must be in `src/` directory
- Refresh browser if needed

### Cannot run scripts
- Ensure virtual environment is activated
- Check that Python is in PATH
- Verify script has valid Python syntax

## Project Status

✅ Organized structure implemented  
✅ All files categorized and moved  
✅ Paths updated in launch script  
✅ Editor works with new structure  
✅ Documentation up to date  

Last updated: January 12, 2026

