import customtkinter as ctk
import threading
import time
import pyautogui
import shutil
import subprocess
from pathlib import Path
import re
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

# Function to show the toast notification (popup)
def show_popup(message, duration=3000):
    popup = tk.Toplevel(app)
    popup.overrideredirect(True)  # Remove window decorations
    popup.geometry(f"250x50+{app.winfo_screenwidth() - 270}+50")  # Position top-right
    
    label = tk.Label(popup, text=message, font=("Arial", 12), bg="black", fg="white", padx=10, pady=5)
    label.pack(fill="both", expand=True)

    # Auto-close after duration
    popup.after(duration, popup.destroy)

# Initialize the app with a dark theme and modern styling
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# PDF Options
pdf_options = ["SHIFT-A.pdf", "SHIFT-B.pdf", "SHIFT-C.pdf", "SHIFT-D.pdf"]

# Colors for different sections (avoiding red, green, orange)
COLOR_DATE = "#8A2BE2"  # Purple
COLOR_DEPTH = "#1E90FF"  # Dodger Blue
COLOR_HSD = "#FF1493"  # Deep Pink
COLOR_OPERATIONS = "#00CED1"  # Dark Turquoise
COLOR_REMARKS = "#FFD700"  # Gold

# Selection tracking variables
selections = {
    'Date': {'start': '0.0', 'end': '0.0', 'color': COLOR_DATE},
    'Present Depth': {'start': '0.0', 'end': '0.0', 'color': COLOR_DEPTH},
    'HSD Stock': {'start': '0.0', 'end': '0.0', 'color': COLOR_HSD},
    'Operations': {'start': '0.0', 'end': '0.0', 'color': COLOR_OPERATIONS},
    'Remarks': {'start': '0.0', 'end': '0.0', 'color': COLOR_REMARKS}
}

# Global variable to store extracted data
upt_message = {}

def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
        return date_obj.strftime("%d %B %Y.pdf")  # Example: 03 March 2025.pdf
    except ValueError:
        return "SAMPLE_copy.pdf"  # Default name if date parsing fails

# Function to extract data from the input message and highlight in the text box
def extract_and_highlight_data():
    global upt_message
    message = input_text.get("1.0", "end-1c")
    
    # Clear previous tags
    for tag in selections.keys():
        input_text.tag_remove(tag, "1.0", "end")
    
    # Reset the data dictionary
    data = {}

    # Extract Date in DD/MM/YYYY format
    date_match = re.search(r'\b(\d{2})\.(\d{2})\.(\d{4})\b', message)
    if date_match:
        data['Date'] = f"{date_match.group(1)}/{date_match.group(2)}/{date_match.group(3)}"
        start_idx = f"1.0 + {date_match.start()} chars"
        end_idx = f"1.0 + {date_match.end()} chars"
        selections['Date']['start'] = input_text.index(start_idx)
        selections['Date']['end'] = input_text.index(end_idx)
        input_text.tag_add('Date', start_idx, end_idx)
        input_text.tag_config('Date', background=COLOR_DATE, foreground='black')
    else:
        data['Date'] = None

    # Extract Present Depth
    present_depth_match = re.search(r'(?i)present depth[:\-]?\s*(\d+\.?\d*)', message)
    if present_depth_match:
        data['Present Depth'] = present_depth_match.group(1)
        start_idx = f"1.0 + {present_depth_match.start()} chars"
        end_idx = f"1.0 + {present_depth_match.end()} chars"
        selections['Present Depth']['start'] = input_text.index(start_idx)
        selections['Present Depth']['end'] = input_text.index(end_idx)
        input_text.tag_add('Present Depth', start_idx, end_idx)
        input_text.tag_config('Present Depth', background=COLOR_DEPTH, foreground='black')
    else:
        data['Present Depth'] = None

    # Extract HSD Stock
    hsd_stock_match = re.search(r'(?i)\*HSD STOCK:\-\s*(\d+)\s*L', message)
    if hsd_stock_match:
        data['HSD Stock'] = hsd_stock_match.group(1)
        start_idx = f"1.0 + {hsd_stock_match.start()} chars"
        end_idx = f"1.0 + {hsd_stock_match.end()} chars"
        selections['HSD Stock']['start'] = input_text.index(start_idx)
        selections['HSD Stock']['end'] = input_text.index(end_idx)
        input_text.tag_add('HSD Stock', start_idx, end_idx)
        input_text.tag_config('HSD Stock', background=COLOR_HSD, foreground='black')
    else:
        data['HSD Stock'] = None

    # Extract Operations
    operations_section = re.search(r'(?i)\*OPERATIONS\*\s*(.*?)(?=\n\*[A-Z ]+\*)', message, re.DOTALL)
    if operations_section:
        start_idx = f"1.0 + {operations_section.start()} chars"
        end_idx = f"1.0 + {operations_section.end()} chars"
        selections['Operations']['start'] = input_text.index(start_idx)
        selections['Operations']['end'] = input_text.index(end_idx)
        input_text.tag_add('Operations', start_idx, end_idx)
        input_text.tag_config('Operations', background=COLOR_OPERATIONS, foreground='black')
        
        operations_text = operations_section.group(1).strip()
        day_operations = []
        night_operations = []

        for line in operations_text.split("\n"):
            time_match = re.match(r'\*(\d{4})-(\d{4})\*[:-]?\s*(.*)', line)
            if time_match:
                start_hour = int(time_match.group(1)[:2])
                start_time = f"{time_match.group(1)[:2]}:{time_match.group(1)[2:]}"
                end_time = f"{time_match.group(2)[:2]}:{time_match.group(2)[2:]}"
                start_minutes = int(time_match.group(1)[:2]) * 60 + int(time_match.group(1)[2:])
                end_minutes = int(time_match.group(2)[:2]) * 60 + int(time_match.group(2)[2:])

                if end_minutes > start_minutes:
                    duration = (end_minutes - start_minutes) / 60
                else:
                    duration = ((1440 - start_minutes) + end_minutes) / 60

                duration_hours = str(duration) if "." in str(duration) else str(int(duration))
                description = time_match.group(3).strip()
                split_desc = [description[i:i+65] for i in range(0, len(description), 65)]

                operation_entry = [start_time, end_time, duration_hours] + split_desc
                
                if start_hour >= 20 or start_hour < 6:  
                    night_operations.append(operation_entry)
                else:
                    day_operations.append(operation_entry)

        data['Day Operations'] = day_operations
        data['Night Operations'] = night_operations
    else:
        data['Day Operations'] = []
        data['Night Operations'] = []

    # Extract Remarks
    remarks_matches = re.finditer(r'(?i)#\s*(.*?)(?=\n|$)', message)
    remarks_text = ""
    for match in remarks_matches:
        start_idx = f"1.0 + {match.start()} chars"
        end_idx = f"1.0 + {match.end()} chars"
        input_text.tag_add('Remarks', start_idx, end_idx)
        input_text.tag_config('Remarks', background=COLOR_REMARKS, foreground='black')
        remarks_text += match.group(1) + " "
    
    if remarks_text:
        def split_remarks(text, limit=100):
            words = text.split()
            result = []
            line = ""

            for word in words:
                if len(line) + len(word) + 1 <= limit:
                    line += " " + word if line else word
                else:
                    result.append(line)
                    line = word  

            if line:
                result.append(line)

            return result

        data['Remarks'] = split_remarks(remarks_text)
    else:
        data['Remarks'] = None
    
    # Update the global variable
    upt_message = data
    
    # Show notification
    show_popup("Text analysis complete. Adjust selections if needed.", duration=3000)
    
    # Return the extracted data
    return data

# Enable selection dragging
# Replace the entire setup_drag_handlers function with this updated version
def setup_drag_handlers():
    # These handlers allow users to drag the end of a selection
    
    def is_near_selection_edge(event_x, event_y):
        """Check if cursor is near any selection edge and return the tag if true"""
        for tag, sel in selections.items():
            try:
                # Check for end position of the selection
                end_pos = input_text.index(sel['end'])
                end_rect = input_text.bbox(end_pos)
                
                if end_rect:  # Make sure we got valid coordinates
                    x, y, width, height = end_rect
                    # If cursor is within 10 pixels of the end of selection
                    if abs(event_x - (x + width)) < 10 and abs(event_y - (y + height/2)) < 10:
                        return tag
            except Exception:
                pass  # Skip if any error occurs during coordinate retrieval
        return None
    
    def check_cursor_position(event):
        """Check cursor position and update cursor style if over a selection edge"""
        tag = is_near_selection_edge(event.x, event.y)
        if tag:
            input_text.configure(cursor="right_side")  # Use right_side cursor (arrow pointing right)
        else:
            input_text.configure(cursor="")  # Reset to default cursor
    
    def start_drag(event):
        """Start dragging a selection edge"""
        tag = is_near_selection_edge(event.x, event.y)
        if tag:
            input_text.dragging_tag = tag
            input_text.configure(cursor="right_side")  # Use right_side cursor while dragging
            # Mark this as an active drag operation
            input_text.is_dragging = True
            return "break"  # Prevent default handling of the click
    
    def drag(event):
        """Update selection while dragging"""
        if hasattr(input_text, 'is_dragging') and input_text.is_dragging and hasattr(input_text, 'dragging_tag'):
            tag = input_text.dragging_tag
            
            # Get the text position at the current mouse coordinates
            current_pos = input_text.index(f"@{event.x},{event.y}")
            
            # Make sure we don't drag before the start position
            start_pos = selections[tag]['start']
            if input_text.compare(current_pos, "<", start_pos):
                current_pos = start_pos
                
            # Update the selection
            selections[tag]['end'] = current_pos
            
            # Remove and re-add the tag to update the visual highlight
            input_text.tag_remove(tag, "1.0", "end")
            input_text.tag_add(tag, selections[tag]['start'], current_pos)
            
            return "break"  # Prevent default handling of the motion
    
    def end_drag(event):
        """End the dragging operation and update the selection"""
        if hasattr(input_text, 'is_dragging') and input_text.is_dragging:
            if hasattr(input_text, 'dragging_tag'):
                tag = input_text.dragging_tag
                
                # Update extracted data based on new selection
                update_selection(tag)
                
                # Show confirmation popup
                show_popup(f"{tag} selection updated", duration=2000)
                
                # Clean up
                delattr(input_text, 'dragging_tag')
            
            # End the drag operation
            input_text.is_dragging = False
            
            # Reset cursor
            input_text.configure(cursor="")
    
    # Bind the event handlers
    input_text.bind("<Motion>", check_cursor_position)
    input_text.bind("<ButtonPress-1>", start_drag)
    input_text.bind("<B1-Motion>", drag) 
    input_text.bind("<ButtonRelease-1>", end_drag)
    
    # Initialize tracking attributes
    input_text.is_dragging = False
    
# Update extracted data based on new selection
def update_selection(tag):
    global upt_message
    start = selections[tag]['start']
    end = selections[tag]['end']
    
    # Get the new selected text
    selected_text = input_text.get(start, end)
    
    # Update the appropriate field in upt_message
    if tag == 'Date':
        date_match = re.search(r'\b(\d{2})\.(\d{2})\.(\d{4})\b', selected_text)
        if date_match:
            upt_message['Date'] = f"{date_match.group(1)}/{date_match.group(2)}/{date_match.group(3)}"
    elif tag == 'Present Depth':
        depth_match = re.search(r'(?i)present depth[:\-]?\s*(\d+\.?\d*)', selected_text)
        if depth_match:
            upt_message['Present Depth'] = depth_match.group(1)
    elif tag == 'HSD Stock':
        hsd_match = re.search(r'(?i)\*HSD STOCK:\-\s*(\d+)\s*L', selected_text)
        if hsd_match:
            upt_message['HSD Stock'] = hsd_match.group(1)
    elif tag == 'Remarks':
        # Just use the raw text for remarks
        if selected_text:
            def split_remarks(text, limit=100):
                words = text.split()
                result = []
                line = ""
                for word in words:
                    if len(line) + len(word) + 1 <= limit:
                        line += " " + word if line else word
                    else:
                        result.append(line)
                        line = word  
                if line:
                    result.append(line)
                return result
            upt_message['Remarks'] = split_remarks(selected_text)

# PDF Automation Functions
def copy_pdf(selected_pdf, formatted_date):
    src_path = Path(f"src/{selected_pdf}")
    dest_path = Path(f"{formatted_date}")  # Save in an 'output' folder
    shutil.copy(src_path, dest_path)
    return dest_path

def open_pdf(pdf_path):
    subprocess.Popen(["open", "-a", "Adobe Acrobat Reader", str(pdf_path)])

def type_operations(operations, start_y):
    start_x = 657  
    x_increment = 23  
    y_increment = 8.27  
    jump_x = 818  

    current_y = start_y  
    first_row = True  # Flag to check if it's the first row

    for operation in operations:
        x, y = start_x, current_y  
        for i, element in enumerate(operation):
            pyautogui.click(x, y)  # Always click first

            if i == 0:
                if first_row:
                    pyautogui.typewrite(str(element))  # Type only for the first row
                    time.sleep(0.02)
                    first_row = False  # Turn off the flag after first row
                x += x_increment  # Move to next column
            elif i==2:
                x = jump_x       
            else:
                pyautogui.typewrite(str(element))  # Type normally for other elements
                time.sleep(0.02)

                if i == 1:
                    x += x_increment   
                else:
                    y += y_increment  

        current_y = y  
        time.sleep(0.01)  

def type_hsd_stock(hsd_stock):
    x, y = 803, 772  
    pyautogui.click(x, y)
    pyautogui.typewrite(str(hsd_stock))
    time.sleep(0.2)

def type_present_depth(present_depth):
    x, y = 510, 210  
    pyautogui.click(x, y)
    pyautogui.typewrite(str(present_depth))
    time.sleep(0.01)

def type_remarks(remarks):
    x, y = 371, 437  
    for remark in remarks:
        pyautogui.click(x, y)
        pyautogui.typewrite(remark)
        y += 7  
        time.sleep(0.01)

    x, y = 371, 670  
    for remark in remarks:
        pyautogui.click(x, y)
        pyautogui.typewrite(remark)
        y += 7.6  
        time.sleep(0.01)

def type_date(date):
    start_x, start_y = 612, 223
    end_x = 642
    pyautogui.click(start_x, start_y)  # Click to focus the date field
    time.sleep(0.3)
    pyautogui.mouseDown(start_x, start_y)  # Click and hold
    time.sleep(0.3)
    pyautogui.moveTo(end_x, start_y, duration=0.2)  # Drag to select
    pyautogui.mouseUp()
    time.sleep(0.3)
    pyautogui.typewrite(date)
    time.sleep(0.5)

# Function to show status message
def show_status_message(message):
    status_popup = ctk.CTkToplevel(app)
    status_popup.title("Status")
    status_popup.geometry("300x100")
    label = ctk.CTkLabel(status_popup, text=message, font=("Arial", 14))
    label.pack(pady=20)
    status_popup.after(2000, status_popup.destroy)

# Function to handle the settings popup
def open_settings_popup():
    settings_popup = ctk.CTkToplevel(app)
    settings_popup.title("PDF Settings")
    settings_popup.geometry("400x300")
    
    for pdf in pdf_options:
        frame = ctk.CTkFrame(settings_popup)
        frame.pack(pady=5, padx=10, fill='x')
        
        label = ctk.CTkLabel(frame, text=pdf, font=("Arial", 14))
        label.pack(side='left', padx=5)
        
        edit_button = ctk.CTkButton(frame, text="Edit", width=50, command=lambda p=pdf: open_pdf(f"src/{p}"))
        edit_button.pack(side='left', padx=5)
        
        download_button = ctk.CTkButton(frame, text="Download", width=80, command=lambda p=pdf: download_pdf(p))
        download_button.pack(side='left', padx=5)
        
        change_button = ctk.CTkButton(frame, text="Change PDF", width=100, command=lambda p=pdf: change_pdf(p))
        change_button.pack(side='left', padx=5)

# Function to allow user to download the PDF
def download_pdf(pdf_name):
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile=pdf_name)
    if file_path:
        shutil.copy(f"src/{pdf_name}", file_path)
        show_status_message(f"{pdf_name} downloaded successfully.")

# Function to allow user to replace an existing PDF
def change_pdf(pdf_name):
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        shutil.copy(file_path, f"src/{pdf_name}")
        show_status_message(f"{pdf_name} has been replaced.")

# Function to show and allow modification of extracted data
def show_and_modify():
    if not input_text.get("1.0", "end-1c").strip():
        status_label.configure(text="Error: Please enter valid input", text_color="red")
        return
    
    status_label.configure(text="Analyzing text...", text_color="yellow")
    extract_and_highlight_data()
    status_label.configure(text="Text analyzed. You can now adjust selections by dragging the edges.", text_color="#00CED1")  # Dark Turquoise
    
    # Enable the execution button after analysis
    start_button.configure(state="normal")

# Function to automate the PDF filling process
def start_execution():
    global upt_message
    selected_pdf = pdf_dropdown.get()
    
    if not upt_message:
        status_label.configure(text="Error: Please analyze the input first", text_color="red")
        return
    
    status_label.configure(text="Processing...", text_color="yellow")
    
    formatted_date = format_date(upt_message.get('Date', ''))
    
    # Copy the selected PDF with the extracted date as filename
    pdf_path = copy_pdf(selected_pdf, formatted_date)
    open_pdf(pdf_path)
    time.sleep(4)  # Simulate processing time

    # Type data into PDF based on selected checkboxes
    type_date(upt_message['Date'])

    if remarks_var.get():
        type_remarks(upt_message['Remarks'])
    if hsd_stock_var.get():
        type_hsd_stock(upt_message['HSD Stock'])
    if present_depth_var.get():
        type_present_depth(upt_message['Present Depth'])
    if day_operations_var.get():
        type_operations(upt_message.get('Day Operations', []), start_y=413)
    if night_operations_var.get():
        type_operations(upt_message.get('Night Operations', []), start_y=641)

    status_label.configure(text="Execution Completed!", text_color="#00FF7F")  # Spring Green

    # Show pop-up notification
    show_popup("Execution Completed!", duration=3000)

# Create the main app window
app = ctk.CTk()
app.title("Automated DDPR Application")
app.geometry("800x800")

# Title Label
title_label = ctk.CTkLabel(app, text="Please Enter DDPR to Convert to IADC Format", font=("Arial", 20, "bold"))
title_label.pack(pady=10)

# Dropdown for PDF Selection
pdf_dropdown = ctk.CTkComboBox(app, values=pdf_options, font=("Arial", 14))
pdf_dropdown.pack(pady=10)
pdf_dropdown.set("SHIFT-A.pdf")  # Default selection

# Input Text Box
input_text = ctk.CTkTextbox(app, height=400, width=700, font=("Arial", 14))
input_text.pack(pady=10)

# Setup handlers for dragging selections
setup_drag_handlers()

# Button to show and modify extracted data
show_modify_button = ctk.CTkButton(
    app, 
    text="Show & Modify", 
    font=("Arial", 16), 
    fg_color="#9370DB",  # Medium Purple
    hover_color="#8A2BE2",  # Blue Violet
    command=show_and_modify
)
show_modify_button.pack(pady=5)

# Frame to hold checkboxes aligned vertically
checkbox_frame = ctk.CTkFrame(app)
checkbox_frame.pack(pady=5, anchor="w")

# Variables for checkboxes
remarks_var = ctk.IntVar(value=1)
hsd_stock_var = ctk.IntVar(value=1)
present_depth_var = ctk.IntVar(value=1)
day_operations_var = ctk.IntVar(value=1)
night_operations_var = ctk.IntVar(value=1)

# Define a fixed width for alignment
fixed_width = 200  

# Checkboxes for each function with corresponding colors
remarks_checkbox = ctk.CTkCheckBox(
    checkbox_frame, 
    text="Type Remarks", 
    variable=remarks_var, 
    font=("Arial", 14), 
    width=fixed_width,
    fg_color=COLOR_REMARKS,
    hover_color="#B8860B"  # Dark Golden Rod (darker version of gold)
)
remarks_checkbox.pack(anchor="w", pady=2)

hsd_stock_checkbox = ctk.CTkCheckBox(
    checkbox_frame, 
    text="Type HSD Stock", 
    variable=hsd_stock_var, 
    font=("Arial", 14), 
    width=fixed_width,
    fg_color=COLOR_HSD,
    hover_color="#C71585"  # Medium Violet Red (darker version of deep pink)
)
hsd_stock_checkbox.pack(anchor="w", pady=2)

present_depth_checkbox = ctk.CTkCheckBox(
    checkbox_frame, 
    text="Type Present Depth", 
    variable=present_depth_var, 
    font=("Arial", 14), 
    width=fixed_width,
    fg_color=COLOR_DEPTH,
    hover_color="#0000CD"  # Medium Blue (darker version of dodger blue)
)
present_depth_checkbox.pack(anchor="w", pady=2)

day_operations_checkbox = ctk.CTkCheckBox(
    checkbox_frame, 
    text="Type Day Operations", 
    variable=day_operations_var, 
    font=("Arial", 14), 
    width=fixed_width,
    fg_color=COLOR_OPERATIONS,
    hover_color="#008B8B"  # Dark Cyan (darker version of dark turquoise)
)
day_operations_checkbox.pack(anchor="w", pady=2)

night_operations_checkbox = ctk.CTkCheckBox(
    checkbox_frame, 
    text="Type Night Operations", 
    variable=night_operations_var, 
    font=("Arial", 14), 
    width=fixed_width,
    fg_color=COLOR_OPERATIONS,
    hover_color="#008B8B"  # Dark Cyan (darker version of dark turquoise)
)
night_operations_checkbox.pack(anchor="w", pady=2)

# Start Button (initially disabled)
start_button = ctk.CTkButton(
    app, 
    text="Start Execution", 
    font=("Arial", 16), 
    command=lambda: threading.Thread(target=start_execution).start(),
    state="disabled",
    fg_color="#2E8B57",  # Sea Green
    hover_color="#006400"  # Dark Green
)
start_button.pack(pady=10)

# Status Label
status_label = ctk.CTkLabel(app, text="", font=("Arial", 14))
status_label.pack(pady=10)

# Legend for colors
legend_frame = ctk.CTkFrame(app)
legend_frame.pack(pady=5)

legend_title = ctk.CTkLabel(legend_frame, text="Color Legend:", font=("Arial", 14, "bold"))
legend_title.grid(row=0, column=0, columnspan=2, padx=5, pady=2, sticky="w")

# Add color legends
legend_items = [
    ("Date", COLOR_DATE),
    ("Present Depth", COLOR_DEPTH),
    ("HSD Stock", COLOR_HSD),
    ("Operations", COLOR_OPERATIONS),
    ("Remarks", COLOR_REMARKS)
]

for i, (name, color) in enumerate(legend_items):
    color_box = ctk.CTkFrame(legend_frame, width=20, height=20, fg_color=color)
    color_box.grid(row=i+1, column=0, padx=5, pady=2)
    color_label = ctk.CTkLabel(legend_frame, text=name, font=("Arial", 12))
    color_label.grid(row=i+1, column=1, padx=5, pady=2, sticky="w")

# Settings Button (Top Right)
settings_button = ctk.CTkButton(app, text="⚙", width=30, command=open_settings_popup)
settings_button.place(x=750, y=10)

# Run the App
app.mainloop()