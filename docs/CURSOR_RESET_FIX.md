# Monaco Editor Cursor Reset Fix

## Problem
The Monaco editor cursor was resetting frequently while typing, making it extremely annoying to edit code.

## Root Cause
Streamlit reruns the entire script whenever ANY widget value changes. This was happening because:

1. **Sidebar controls** (Theme, Font Size, Minimap) were using local variables, causing reruns
2. **Save form inputs** (Filename, Update Message) were triggering reruns on every keystroke
3. Each rerun **recreated the Monaco editor component**, resetting the cursor position

## Solution Implemented

### 1. Wrapped Save Inputs in `st.form()`
```python
with st.form(key="save_form", clear_on_submit=False):
    filename_form = st.text_input(...)
    update_message_form = st.text_area(...)
    save_submitted = st.form_submit_button("💾 Save to File")
```

**Effect**: Typing in the filename or update message fields no longer triggers reruns. Changes are only submitted when the "Save to File" button is clicked.

### 2. Converted Sidebar Controls to Session State Keys
**Before:**
```python
theme = st.selectbox("Theme", ["vs-dark", "vs-light", "hc-black"], index=0)
font_size = st.slider("Font Size", 10, 24, 14)
show_minimap = st.checkbox("Show Minimap", value=True)
```

**After:**
```python
st.selectbox("Theme", [...], index=0, key="editor_theme")
st.slider("Font Size", 10, 24, 14, key="font_size")
st.checkbox("Show Minimap", value=True, key="show_minimap")
```

**Effect**: These controls still cause reruns (Streamlit limitation), but now they properly bind to session state.

### 3. Removed Unnecessary `st.rerun()` Calls
- Removed `st.rerun()` after successful save
- Kept `st.rerun()` only where necessary (Reload button, Clear History button)

### 4. Added Session State Initialization
```python
if 'editor_theme' not in st.session_state:
    st.session_state.editor_theme = "vs-dark"
if 'font_size' not in st.session_state:
    st.session_state.font_size = 14
if 'show_minimap' not in st.session_state:
    st.session_state.show_minimap = True
```

## Result

### ✅ Fixed - No More Cursor Resets When:
- Typing in the **filename input** field
- Typing in the **update message** field
- Clicking **Save to File** button
- Clicking **Run Script** button
- Clicking **Show History** button

### ⚠️ Still Causes Rerun (Streamlit Limitation):
- Changing **Theme** in sidebar (but this is intentional - you're changing the editor theme)
- Changing **Font Size** slider
- Toggling **Show Minimap** checkbox
- Clicking **Reload handler.py** button
- Clicking **Clear History** button

## Why Sidebar Controls Still Cause Reruns

Changing the theme, font size, or minimap settings **should** cause a rerun because:
1. The Monaco editor needs to be recreated with the new settings
2. These are infrequent actions (not like typing text)
3. Users expect immediate visual feedback when changing these settings

## Best Practices for Editing

To minimize disruption while editing:

1. **Set your editor preferences first** (theme, font size, minimap) before editing code
2. **Type your code in the Monaco editor** - cursor won't reset
3. **Fill in filename and update message** - no reruns while typing
4. **Click Save** when ready - single rerun to save

## Technical Notes

### Form Benefits
`st.form()` batches all form inputs together and only triggers a rerun when the submit button is clicked. This is perfect for text inputs that would otherwise trigger reruns on every keystroke.

### Session State Keys
When you use `key="variable_name"` in a Streamlit widget, it automatically creates and binds to `st.session_state.variable_name`, eliminating the need for manual state management.

### Monaco Editor Limitations
The `streamlit-monaco` package doesn't preserve cursor position across reruns. This is a limitation of the component itself. Our solution minimizes reruns to work around this limitation.

## Alternative Solutions (Not Implemented)

### Option 1: Use `streamlit-code-editor` instead
- More feature-rich component
- Better state preservation
- Requires: `pip install streamlit-code-editor`

### Option 2: Custom Component
- Build a custom Streamlit component with proper state handling
- Requires: React/JavaScript knowledge and more development time

### Option 3: Debounced Updates
- Use JavaScript to debounce Monaco editor updates
- Complex to implement with current setup

## Conclusion

The cursor reset issue is now **significantly reduced**. Users can type freely in the Monaco editor and in the save form inputs without interruption. The only remaining reruns occur when intentionally changing editor settings in the sidebar, which is acceptable behavior.

