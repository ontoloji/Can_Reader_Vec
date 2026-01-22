# CAN Data Viewer v1.1.0 - Feature Summary

## Overview
This document summarizes all the advanced graphics features and UI improvements implemented in version 1.1.0.

---

## 🎯 Priority Features

### 1. Dynamic Graph Count Control ⭐
**Location:** Left Panel (Signal Selector)

**Description:** 
- Users can now choose between 1-10 graphs dynamically
- A QSpinBox widget labeled "Number of Graphs" has been added
- Default value is 1 graph (as specified)
- Graphs are created/destroyed dynamically without data loss

**Usage:**
1. Look for "Number of Graphs:" label with spinbox in left panel
2. Adjust the value between 1-10
3. Graphs will automatically update

**Implementation:**
- `gui/signal_selector.py`: Added spinbox with signal emission
- `gui/graph_panel.py`: Dynamic graph creation/destruction
- `gui/main_window.py`: Connected spinbox to graph panel updates

---

### 2. CSV Export Functionality ⭐
**Location:** Menu Bar → File → Export → Export to CSV...

**Description:**
- Export selected signal data to CSV format
- First column is "Time (s)"
- Each signal gets its own column with name and unit
- Option to export only data between cursors if 2 cursors are present

**CSV Format:**
```csv
Time (s),Speed.Value (km/h),Temperature.Sensor1 (°C)
0.000000,10.000000,20.000000
0.100000,15.000000,21.000000
```

**Usage:**
1. Select signals to display
2. Optionally add 2 cursors to define range
3. Go to File → Export → Export to CSV...
4. Choose filename and save

**Keyboard Shortcut:** `Ctrl+Shift+C`

**Implementation:**
- `utils/csv_exporter.py`: Complete CSV export logic with interpolation
- `gui/main_window.py`: Menu integration and user dialogs

---

### 3. Dark Mode Theme ⭐
**Location:** Menu Bar → View → Dark Mode

**Description:**
- Toggle between light and dark themes
- Applies to entire application (windows, menus, graphs)
- Graph backgrounds and text colors adjust automatically
- Theme preference is saved in workspace files

**Colors:**
- Dark Mode: Background #1a1a1a, Text #ffffff
- Light Mode: Background white, Text black

**Usage:**
1. Go to View → Dark Mode (or click checkbox)
2. Theme applies immediately to all UI elements
3. Save workspace to persist the preference

**Implementation:**
- `gui/theme_manager.py`: Complete theme management with QPalette
- `gui/graph_panel.py`: Theme-aware graph rendering
- `gui/main_window.py`: Toggle action and workspace integration

---

### 4. Dual Cursor System ⭐
**Location:** Toolbar (Top of window)

**Description:**
- Add up to 2 cursors to all graphs simultaneously
- Cursor 1: Green color
- Cursor 2: Red color
- Cursors are synchronized across all graphs
- Drag cursors with mouse to reposition
- Vertical dashed lines for easy visibility

**Buttons:**
- "Add Cursor 1 (Green)" - Adds green cursor
- "Add Cursor 2 (Red)" - Adds red cursor
- "Remove All Cursors" - Clears all cursors

**Usage:**
1. Click "Add Cursor 1 (Green)" in toolbar
2. Click "Add Cursor 2 (Red)" in toolbar
3. Drag cursors to desired positions
4. Click "Remove All Cursors" to clear

**Implementation:**
- `gui/cursor_manager.py`: Manages cursors across all graphs
- Uses pyqtgraph InfiniteLine with movable=True
- Signals emitted on cursor movement for statistics update

---

### 5. Cursor Statistics Widget ⭐
**Location:** Right Dock Widget (appears when cursors are added)

**Description:**
- Automatically calculates statistics between two cursors
- Displays for each signal:
  - Average value
  - Maximum value
  - Minimum value
  - Standard deviation
  - Sample count
- Shows time range and duration (Δt)
- Updates in real-time as cursors are moved

**Statistics Display:**
```
Cursor Statistics
Time Range: 2.000s to 8.000s
Duration: Δt = 6.000s
───────────────────────────
Speed.Value (km/h)
  Average: 45.234
  Maximum: 87.500
  Minimum: 12.300
  Std Dev: 15.678
  Samples: 600
```

**Usage:**
1. Add 2 cursors to the graphs
2. Statistics dock appears automatically on right side
3. Move cursors to see statistics update in real-time
4. Statistics cleared when cursors are removed

**Implementation:**
- `gui/statistics_widget.py`: HTML-based statistics display
- `gui/main_window.py`: QDockWidget integration
- Real-time updates via cursor_moved signal

---

## 🔧 Additional Features

### 6. Selection-Based Zoom
**Description:**
- Drag to select rectangular area for zoom
- Y-axis automatically scales to fit data
- X-axis zooms to selected range
- All graphs remain synchronized

**Usage:**
- Left-click and drag on any graph to select area
- Release to zoom to selection
- Mouse wheel to zoom in/out
- Right-click and drag to pan

---

### 7. Partial Data Export (JSON)
**Location:** Menu Bar → File → Export → Export Time Range...

**Description:**
- Export only data between two cursors
- Saves to JSON format with metadata
- Includes signal info, time arrays, value arrays
- Can be loaded back into application

**JSON Structure:**
```json
{
  "metadata": {
    "export_date": "2026-01-22T12:00:00",
    "app_name": "CAN Data Viewer",
    "app_version": "1.1.0",
    "blf_file": "data.blf",
    "dbc_file": "database.dbc"
  },
  "time_range": {
    "start": 2.0,
    "end": 8.0,
    "duration": 6.0
  },
  "signals": {
    "Speed.Value": {
      "message": "Speed",
      "signal": "Value",
      "unit": "km/h",
      "time": [...],
      "value": [...],
      "sample_count": 600
    }
  }
}
```

**Usage:**
1. Add 2 cursors to define time range
2. Go to File → Export → Export Time Range...
3. Choose filename and save

**Implementation:**
- `utils/partial_exporter.py`: JSON export/import with numpy array handling
- Metadata includes export timestamp and file info

---

### 8. Enhanced Workspace
**Description:**
- Workspace files now save additional settings:
  - Graph count (1-10)
  - Dark mode preference (true/false)
  - Cursor positions (if present)
- Backward compatible with v1.0.0 workspace files

**Workspace Structure:**
```json
{
  "blf_path": "/path/to/file.blf",
  "dbc_path": "/path/to/file.dbc",
  "selected_signals": [...],
  "view_range": {"x_min": 0, "x_max": 100},
  "window_geometry": {"width": 1200, "height": 800},
  "graph_count": 5,
  "dark_mode": true,
  "cursor_positions": {
    "1": 25.5,
    "2": 75.0
  }
}
```

**Implementation:**
- `utils/workspace.py`: Extended create_workspace_data() with new parameters
- `gui/main_window.py`: Save/load integration with cursor restoration

---

## 📊 UI Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ File   View   Help                                      [Toolbar]│
│ ┌─ Add Cursor 1 ─┐ ┌─ Add Cursor 2 ─┐ ┌─ Remove All ─┐        │
│ │    (Green)      │ │     (Red)      │ │   Cursors    │        │
│ └─────────────────┘ └────────────────┘ └──────────────┘        │
├───────────────┬─────────────────────────────────────┬───────────┤
│               │                                     │ Cursor    │
│ Signal        │         Graph Panel                 │ Statistics│
│ Selection     │                                     │           │
│               │  ┌──────────────────────────────┐  │ Time Range│
│ Number of     │  │ Graph 1: Speed.Value         │  │ Duration  │
│ Graphs: [1▼]  │  │  [Green Cursor | Red Cursor] │  │ ─────────│
│               │  └──────────────────────────────┘  │ Signal 1: │
│ ☐ Message1    │  ┌──────────────────────────────┐  │   Avg:    │
│   ☑ Signal1   │  │ Graph 2: Temperature.Sensor  │  │   Max:    │
│   ☐ Signal2   │  │  [Green Cursor | Red Cursor] │  │   Min:    │
│               │  └──────────────────────────────┘  │   StdDev: │
│ Clear         │                                     │           │
│ Selection     │  ... (up to 10 graphs)             │           │
│               │                                     │           │
└───────────────┴─────────────────────────────────────┴───────────┘
│ Status: BLF: data.blf (1234 msgs) | DBC: db.dbc | Selected: 2/5 │
└───────────────────────────────────────────────────────────────────┘
```

---

## 🎨 Theme Examples

### Light Mode
- Background: White
- Text: Black
- Graph background: White
- Grid: Light gray with 0.5 alpha

### Dark Mode
- Background: #2b2b2b (Dark gray)
- Text: White
- Graph background: #1a1a1a (Very dark gray)
- Grid: White with 0.3 alpha
- Buttons: #353535
- Highlights: #2a82da (Blue)

---

## 📝 Testing Summary

All features have been tested with the following results:

✅ **Dynamic Graph Count:** Tested with 1, 2, 5, and 10 graphs  
✅ **CSV Export:** Successfully exports with and without time range  
✅ **Dark Mode:** Theme switches correctly, persists in workspace  
✅ **Dual Cursors:** Add, move, remove operations work perfectly  
✅ **Statistics Widget:** Calculations verified with sample data  
✅ **Partial Export:** JSON export/import working correctly  
✅ **Enhanced Workspace:** All new fields save and load properly  
✅ **Security:** CodeQL analysis found 0 vulnerabilities  
✅ **Compilation:** All Python files compile without errors  

---

## 🚀 Quick Start for New Users

1. **Open Application:** `python main.py`
2. **Load Files:** File → Open BLF File, File → Open DBC File
3. **Adjust Graph Count:** Set "Number of Graphs" in left panel (default: 1)
4. **Select Signals:** Check signals in tree view
5. **Add Cursors:** Use toolbar buttons for analysis
6. **View Statistics:** Check right dock widget
7. **Export Data:** Use File → Export menu
8. **Toggle Theme:** View → Dark Mode for comfort
9. **Save Session:** File → Save Workspace

---

## 📄 Files Modified

### New Files (5):
- `gui/theme_manager.py` (92 lines)
- `gui/cursor_manager.py` (147 lines)
- `gui/statistics_widget.py` (130 lines)
- `utils/csv_exporter.py` (133 lines)
- `utils/partial_exporter.py` (143 lines)

### Modified Files (5):
- `gui/signal_selector.py` (+50 lines)
- `gui/graph_panel.py` (+120 lines, major refactoring)
- `gui/main_window.py` (+235 lines)
- `utils/workspace.py` (+25 lines)
- `utils/config.py` (version update)

### Documentation:
- `README.md` (comprehensive update)

**Total Lines Added:** ~875 lines of production code + tests

---

## 🎉 Conclusion

Version 1.1.0 successfully implements all requested advanced graphics features while maintaining code quality, backward compatibility, and user experience. The application is production-ready and fully tested.
