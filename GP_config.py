import tkinter as tk
from tkinter import ttk
import xml.etree.ElementTree as ET
import os
import sys

exe_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
print(exe_dir)

# Function to save the selection and update XML
def save_selection():
    selected_item = dropdown.get()
    active_control_point.set(selected_item)
    active_control_point_label.config(text=f"Active Control Point: {selected_item}")
    update_xml(selected_item)

# Function to update XML file with new control point value
def update_xml(new_value):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        
        # Update the value of the active control point in XML
        for item in root.findall('.//active_control_point'):
            item.text = new_value
        
        # Write updated XML back to file
        tree.write(xml_file)
        print(f"XML updated successfully with new value: {new_value}")
        
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
    except IOError as e:
        print(f"Error reading/writing XML file: {e}")

# Function to load active control point from XML
def load_active_control_point(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        active_control_point_value = root.find('.//active_control_point').text
        return active_control_point_value
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
    except IOError as e:
        print(f"Error reading XML file: {e}")
    return None

# Parse XML to extract control points for dropdown menu
def parse_xml(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        control_points = [cp.text for cp in root.findall('.//control_point_selection/item')]
        return control_points
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
    except IOError as e:
        print(f"Error reading XML file: {e}")
    return []

# Load XML file
xml_file = exe_dir + '/__config__.xml'
print(xml_file)

# Load active control point from XML
initial_active_control_point = load_active_control_point(xml_file)

# Parse XML to get control points for dropdown
control_points = parse_xml(xml_file)

# Create main application window
root = tk.Tk()
root.title("Control Point Selection")
root.geometry("200x200")

# Create a label for active control point
active_control_point_label = ttk.Label(root, text="Active Control Point: ")
active_control_point_label.pack(pady=10)

# Variable to store selected control point
active_control_point = tk.StringVar()
active_control_point.set(initial_active_control_point)  # Initialize with value from XML

# Create label to display active control point
active_control_point_display = ttk.Label(root, textvariable=active_control_point, font=('Arial', 14, 'bold'))
active_control_point_display.pack(pady=5)

# Create a label for dropdown
label = ttk.Label(root, text="Select Control Point:")
label.pack(pady=10)

# Create dropdown menu
dropdown = ttk.Combobox(root, values=control_points, state="readonly")
dropdown.pack(pady=10)
dropdown.current(control_points.index(initial_active_control_point))  # Set default selection

# Button to save selection
save_button = ttk.Button(root, text="Save Selection", command=save_selection)
save_button.pack(pady=10)

# Run the main loop
root.mainloop()
