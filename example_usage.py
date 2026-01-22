#!/usr/bin/env python3
"""
Example script demonstrating the CAN Data Viewer usage.

This script shows how to use the data layer components independently
without the GUI, which can be useful for testing or automation.

NOTE: This requires actual BLF and DBC files to run.
"""

def example_usage():
    """Example of using the data layer components."""
    
    print("=" * 60)
    print("CAN Data Viewer - Example Usage")
    print("=" * 60)
    print()
    
    # Import data layer components
    from data import BLFReader, DBCParser, SignalProcessor
    
    print("Step 1: Load BLF file")
    print("-" * 60)
    blf_reader = BLFReader()
    # blf_success = blf_reader.load_file('path/to/your/file.blf')
    print("Example: blf_reader.load_file('data.blf')")
    print()
    
    print("Step 2: Load DBC file")
    print("-" * 60)
    dbc_parser = DBCParser()
    # dbc_success = dbc_parser.load_file('path/to/your/file.dbc')
    print("Example: dbc_parser.load_file('database.dbc')")
    print()
    
    print("Step 3: Get available messages")
    print("-" * 60)
    # messages = dbc_parser.get_messages()
    # unique_ids = blf_reader.get_unique_message_ids()
    print("Example: dbc_parser.get_messages()")
    print("Returns: List of message dictionaries with signals")
    print()
    
    print("Step 4: Process signals")
    print("-" * 60)
    # signal_processor = SignalProcessor(blf_reader, dbc_parser)
    # time_data, value_data = signal_processor.process_signal('MessageName', 'SignalName')
    print("Example: signal_processor.process_signal('EngineStatus', 'RPM')")
    print("Returns: (time_array, value_array) as numpy arrays")
    print()
    
    print("Step 5: Visualize with GUI")
    print("-" * 60)
    print("Run the full application:")
    print("  python main.py")
    print()
    
    print("Or use in your own code:")
    print("""
    from PyQt5.QtWidgets import QApplication
    from gui import MainWindow
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
    """)
    print()
    
    print("=" * 60)
    print("Workspace Example")
    print("=" * 60)
    print()
    
    from utils import Workspace
    
    print("Save workspace:")
    print("-" * 60)
    workspace_data = {
        'blf_path': '/path/to/data.blf',
        'dbc_path': '/path/to/database.dbc',
        'selected_signals': [
            {'message': 'EngineStatus', 'signal': 'RPM', 'unit': 'rpm'},
            {'message': 'VehicleSpeed', 'signal': 'Speed', 'unit': 'km/h'}
        ],
        'view_range': {'x_min': 0, 'x_max': 100},
        'window_geometry': {'width': 1200, 'height': 800}
    }
    # Workspace.save('my_workspace.workspace', workspace_data)
    print("Example: Workspace.save('session.workspace', workspace_data)")
    print()
    
    print("Load workspace:")
    print("-" * 60)
    # loaded_data = Workspace.load('my_workspace.workspace')
    print("Example: Workspace.load('session.workspace')")
    print("Returns: Dictionary with saved configuration")
    print()
    
    print("=" * 60)
    print("Export Example")
    print("=" * 60)
    print()
    
    print("Export graphs:")
    print("-" * 60)
    print("From GUI: File → Export Graphs...")
    print("Or programmatically:")
    print("  GraphExporter.export_graph(plot_widget, 'graph.png')")
    print("  GraphExporter.export_all_graphs(plot_widgets, 'graphs.png')")
    print()


def main():
    """Main function."""
    try:
        example_usage()
        
        print("=" * 60)
        print("Ready to use CAN Data Viewer!")
        print()
        print("To start the GUI application:")
        print("  python main.py")
        print()
        print("For more information, see README.md")
        print("=" * 60)
        
    except ImportError as e:
        print(f"Error: {e}")
        print()
        print("Please install dependencies first:")
        print("  pip install -r requirements.txt")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
