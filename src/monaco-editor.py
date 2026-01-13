import streamlit as st
from streamlit_ace import st_ace
import os
import sys
import subprocess
import tempfile
from io import StringIO
from datetime import datetime
import getpass
import json

st.set_page_config(layout="wide", page_title="Python Script Editor")

st.title("🐍 Python Script Editor with Monaco")

# Initialize session state
if 'script_content' not in st.session_state:
    # Load handler.py content on first run
    handler_path = os.path.join(os.path.dirname(__file__), 'handler.py')
    if os.path.exists(handler_path):
        with open(handler_path, 'r') as f:
            st.session_state.script_content = f.read()
    else:
        st.session_state.script_content = "# Write your Python script here\n\ndef main():\n    print('Hello, World!')\n\nif __name__ == '__main__':\n    main()"

if 'execution_output' not in st.session_state:
    st.session_state.execution_output = ""

if 'save_filename' not in st.session_state:
    st.session_state.save_filename = "handler.py"

if 'update_history' not in st.session_state:
    # Load history from project root (one level up from src/)
    project_root = os.path.dirname(os.path.dirname(__file__))
    history_file = os.path.join(project_root, ".script_history.json")
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r') as f:
                st.session_state.update_history = json.load(f)
        except:
            st.session_state.update_history = []
    else:
        st.session_state.update_history = []

if 'update_message' not in st.session_state:
    st.session_state.update_message = ""

if 'editor_theme' not in st.session_state:
    st.session_state.editor_theme = "monokai"

if 'font_size' not in st.session_state:
    st.session_state.font_size = 14

if 'show_minimap' not in st.session_state:
    st.session_state.show_minimap = True

if 'selected_file' not in st.session_state:
    st.session_state.selected_file = "handler.py"


def get_python_files():
    """Get all Python files in the current directory."""
    try:
        current_dir = os.path.dirname(__file__) if os.path.dirname(__file__) else "."
        files = [f for f in os.listdir(current_dir) if f.endswith('.py') and os.path.isfile(os.path.join(current_dir, f))]
        return sorted(files)
    except Exception as e:
        st.error(f"Error listing files: {str(e)}")
        return []


def load_file_content(filename):
    """Load content from a Python file."""
    try:
        filepath = os.path.join(os.path.dirname(__file__) if os.path.dirname(__file__) else ".", filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return f.read()
        else:
            return f"# File not found: {filename}"
    except Exception as e:
        return f"# Error loading file: {str(e)}"


def execute_python_script(script_code):
    """
    Execute Python script locally and capture output.

    Args:
        script_code (str): The Python script code to execute

    Returns:
        tuple: (success: bool, output: str)
    """
    try:
        if script_code is None:
            return False, "Error: No script content to execute"

        # Create a temporary file to store the script
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp_file:
            tmp_file.write(script_code)
            tmp_file_path = tmp_file.name

        # Execute the script and capture output
        result = subprocess.run(
            [sys.executable, tmp_file_path],
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout
        )

        # Clean up temporary file
        os.unlink(tmp_file_path)

        # Combine stdout and stderr
        output = ""
        if result.stdout:
            output += "STDOUT:\n" + result.stdout
        if result.stderr:
            if output:
                output += "\n\n"
            output += "STDERR:\n" + result.stderr

        if result.returncode != 0:
            return False, f"Execution failed with return code {result.returncode}\n\n{output}"

        return True, output if output else "Script executed successfully (no output)"

    except subprocess.TimeoutExpired:
        return False, "Error: Script execution timed out (30 seconds)"
    except Exception as e:
        return False, f"Error executing script: {str(e)}"


def save_script_to_file(script_code, filename="handler.py", update_message=""):
    """Save the script to a file and record update history."""
    try:
        if script_code is None:
            return False, "Error: No script content to save"

        # Ensure filename is just the basename (no path)
        filename = os.path.basename(filename)

        # Construct filepath in src/ directory
        src_dir = os.path.dirname(__file__)  # Gets the src/ directory
        filepath = os.path.join(src_dir, filename)

        # Save the script to src/ directory
        with open(filepath, 'w') as f:
            f.write(script_code)

        # Record history entry
        history_entry = {
            "filename": filename,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": getpass.getuser(),
            "update_message": update_message if update_message else "No message provided",
            "file_size": len(script_code)
        }

        # Add to history
        st.session_state.update_history.append(history_entry)

        # Save history to project root (one level up from src/)
        project_root = os.path.dirname(src_dir)
        history_file = os.path.join(project_root, ".script_history.json")
        with open(history_file, 'w') as f:
            json.dump(st.session_state.update_history, f, indent=2)

        return True, f"Script saved to src/{filename}"
    except Exception as e:
        return False, f"Error saving script: {str(e)}"


# Sidebar controls
with st.sidebar:
    st.header("📂 File Browser")

    # Get all Python files
    python_files = get_python_files()

    if python_files:
        # Find the index of the currently selected file
        try:
            current_index = python_files.index(st.session_state.selected_file)
        except ValueError:
            current_index = 0
            st.session_state.selected_file = python_files[0]

        # File selector
        selected = st.selectbox(
            "Select a Python file to edit:",
            python_files,
            index=current_index,
            key="file_selector"
        )

        # Load file content when selection changes
        if selected != st.session_state.selected_file:
            st.session_state.selected_file = selected
            st.session_state.script_content = load_file_content(selected)
            st.session_state.save_filename = selected
            st.rerun()

        # Show file info
        st.caption(f"📄 Editing: **{st.session_state.selected_file}**")
        try:
            filepath = os.path.join(os.path.dirname(__file__) if os.path.dirname(__file__) else ".", st.session_state.selected_file)
            file_size = os.path.getsize(filepath)
            st.caption(f"📏 Size: {file_size} bytes")
        except:
            pass
    else:
        st.warning("No Python files found in directory")

    # Create new file option
    with st.expander("➕ Create New File"):
        new_filename = st.text_input("New file name:", placeholder="my_script.py")
        if st.button("Create File", use_container_width=True):
            if new_filename:
                if new_filename.endswith('.py'):
                    try:
                        filepath = os.path.join(os.path.dirname(__file__) if os.path.dirname(__file__) else ".", new_filename)
                        if not os.path.exists(filepath):
                            with open(filepath, 'w') as f:
                                f.write("# New Python script\n\ndef main():\n    print('Hello, World!')\n\nif __name__ == '__main__':\n    main()\n")
                            st.session_state.selected_file = new_filename
                            st.session_state.script_content = load_file_content(new_filename)
                            st.session_state.save_filename = new_filename
                            st.success(f"Created {new_filename}")
                            st.rerun()
                        else:
                            st.error("File already exists!")
                    except Exception as e:
                        st.error(f"Error creating file: {str(e)}")
                else:
                    st.error("Filename must end with .py")
            else:
                st.error("Please enter a filename")

    st.markdown("---")
    st.header("⚙️ Editor Settings")

    st.selectbox(
        "Theme",
        ["monokai", "github", "tomorrow", "twilight", "solarized_dark", "solarized_light"],
        index=0,
        key="editor_theme"  # Binds directly to session state
    )

    st.slider("Font Size", 10, 24, 14, key="font_size")  # Binds directly to session state

    st.checkbox("Show Minimap", value=True, key="show_minimap")  # Binds directly to session state

    st.markdown("---")
    st.header("📁 File Operations")

    if st.button("🔄 Reload Current File", use_container_width=True):
        filepath = os.path.join(os.path.dirname(__file__) if os.path.dirname(__file__) else ".", st.session_state.selected_file)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                st.session_state.script_content = f.read()
            st.success(f"Reloaded {st.session_state.selected_file}!")
            st.rerun()
        else:
            st.error(f"{st.session_state.selected_file} not found!")

    st.markdown("---")
    st.header("📊 History Stats")
    history_count = len(st.session_state.update_history)
    st.metric("Total Updates", history_count)
    if history_count > 0:
        last_update = st.session_state.update_history[-1]
        st.caption(f"Last update: {last_update['timestamp']}")
        st.caption(f"By: {last_update['user']}")

    st.markdown("---")
    st.info("💡 **Tip:** Select a file from the sidebar, edit it, then save or run.")

# Main editor area
st.subheader(f"📝 Code Editor - {st.session_state.selected_file}")

code = st_ace(
    value=st.session_state.script_content,
    height=500,
    language="python",
    theme=st.session_state.editor_theme if st.session_state.editor_theme != "vs-light" else "github",
    keybinding="vscode",
    font_size=st.session_state.font_size,
    tab_size=4,
    show_gutter=True,
    show_print_margin=False,
    wrap=False,
    auto_update=False,  # Critical: prevents automatic updates that cause cursor reset
    readonly=False,
    key=f"code_editor_{st.session_state.selected_file}"  # Dynamic key per file for proper reloading
)

# Don't update session state here - it causes reruns and cursor resets!
# The code variable now contains the current editor content
# We'll use it directly for save/run operations

# If code is None (shouldn't happen, but just in case), use session state
if code is None:
    code = st.session_state.script_content

# File save form - prevents reruns while typing
st.markdown("---")
st.subheader("💾 Save Settings")

with st.form(key="save_form", clear_on_submit=False):
    filename_form = st.text_input(
        "File name to save:",
        value=st.session_state.save_filename,
        placeholder="Enter filename (e.g., my_script.py)",
        help="Specify the filename where the code will be saved"
    )

    update_message_form = st.text_area(
        "Update message:",
        value=st.session_state.update_message,
        placeholder="Describe what changes you made (e.g., 'Fixed bug in function X', 'Added new feature Y')",
        help="Add a message describing the changes made in this update",
        height=80
    )

    save_submitted = st.form_submit_button("💾 Save to File", use_container_width=True)

    if save_submitted:
        # Update session state with current editor content before saving
        st.session_state.script_content = code

        # Check if this is a new file (different from currently selected)
        is_new_file = filename_form != st.session_state.selected_file

        success, message = save_script_to_file(code, filename_form, update_message_form)
        if success:
            st.success(message)
            st.session_state.save_filename = filename_form
            st.session_state.update_message = ""  # Clear for next save

            # If it's a new file or different file, switch context to it
            if is_new_file:
                st.session_state.selected_file = filename_form
                # Load the content we just saved to ensure consistency
                st.session_state.script_content = code
                st.info(f"✨ Switched to editing: {filename_form}")
                st.rerun()  # Rerun to refresh file list and editor
        else:
            st.error(message)

# Note: We don't update session state here to avoid triggering reruns while typing
# The values will be used directly from the input variables when saving

# Action buttons (Run Script and Show History)
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("▶️ Run Script", use_container_width=True, type="primary"):
        # Update session state with current editor content before running
        st.session_state.script_content = code

        with st.spinner("Executing script..."):
            success, output = execute_python_script(code)
            st.session_state.execution_output = output
            if success:
                st.success("✅ Execution completed!")
            else:
                st.error("❌ Execution failed!")

with col2:
    if st.button("📜 Show History", use_container_width=True):
        st.session_state.show_history = not st.session_state.get('show_history', False)

# History display section
if st.session_state.get('show_history', False):
    st.markdown("---")
    st.subheader("📜 Update History")

    if st.session_state.update_history:
        # Display history in reverse chronological order (newest first)
        for idx, entry in enumerate(reversed(st.session_state.update_history)):
            with st.expander(f"🕒 {entry['timestamp']} - {entry['filename']} by {entry['user']}", expanded=(idx == 0)):
                st.markdown(f"**File:** `{entry['filename']}`")
                st.markdown(f"**User:** {entry['user']}")
                st.markdown(f"**Timestamp:** {entry['timestamp']}")
                st.markdown(f"**File Size:** {entry['file_size']} characters")
                st.markdown(f"**Update Message:**")
                st.info(entry['update_message'])

        # Add clear history button
        if st.button("🗑️ Clear History"):
            st.session_state.update_history = []
            history_file = ".script_history.json"
            if os.path.exists(history_file):
                os.remove(history_file)
            st.success("History cleared!")
            st.rerun()
    else:
        st.info("No update history available yet. Save a file to start tracking updates.")

# Output area
if st.session_state.execution_output:
    st.markdown("---")
    st.subheader("📤 Execution Output")
    st.code(st.session_state.execution_output, language="text")
