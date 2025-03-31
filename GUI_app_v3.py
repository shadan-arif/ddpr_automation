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

def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
        return date_obj.strftime("%d %B %Y.pdf")  # Example: 03 March 2025.pdf
    except ValueError:
        return "SAMPLE_copy.pdf"  # Default name if date parsing fails

# Function to extract data from the input message
def extract_data(message):
    data = {}

    # Extract Date in DD/MM/YYYY format
    date_match = re.search(r'\b(\d{2})\.(\d{2})\.(\d{4})\b', message)
    data['Date'] = f"{date_match.group(1)}/{date_match.group(2)}/{date_match.group(3)}" if date_match else None
    
    # Extract Present Depth
    present_depth_match = re.search(r'(?i)present depth[:\-]?\s*(\d+\.?\d*)', message)
    data['Present Depth'] = present_depth_match.group(1) if present_depth_match else None

    # Extract HSD Stock
    hsd_stock_match = re.search(r'(?i)\*HSD STOCK:\-\s*(\d+)\s*L', message)
    data['HSD Stock'] = hsd_stock_match.group(1) if hsd_stock_match else None

    # Extract Operations
    operations_section = re.search(r'(?i)\*OPERATIONS\*\s*(.*?)(?=\n\*[A-Z ]+\*)', message, re.DOTALL)
    if operations_section:
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
    remarks_text = " ".join(re.findall(r'(?i)#\s*(.*?)(?=\n|$)', message))

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

    data['Remarks'] = split_remarks(remarks_text) if remarks_text else None

    return data

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

# --------- NEW FUNCTIONS FOR SELECTION PREVIEW AND MODIFICATION ---------

# Global variable to store extracted data
extracted_data = {}

# Function to show extracted data and allow modifications
def show_and_modify_selection():
    message = input_text.get("1.0", "end-1c")
    
    if not message.strip():
        status_label.configure(text="Error: Please enter valid input", text_color="red")
        return
    
    # Extract data first without executing the rest of the code
    global extracted_data
    extracted_data = extract_data(message)
    
    # Create selection preview window
    preview_window = ctk.CTkToplevel(app)
    preview_window.title("Preview Extracted Data")
    preview_window.geometry("800x600")
    
    # Create a scrollable frame for content
    scroll_frame = ctk.CTkScrollableFrame(preview_window, width=750, height=500)
    scroll_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    # Title
    title_label = ctk.CTkLabel(scroll_frame, text="Review and Modify Extracted Data", 
                              font=("Arial", 18, "bold"))
    title_label.pack(pady=10)
    
    # Add fields for each type of extracted data
    add_editable_field(scroll_frame, "Date", extracted_data.get('Date', ''), 'purple')
    add_editable_field(scroll_frame, "Present Depth", extracted_data.get('Present Depth', ''), 'blue')
    add_editable_field(scroll_frame, "HSD Stock", extracted_data.get('HSD Stock', ''), 'teal')
    
    # Display remarks
    if extracted_data.get('Remarks'):
        remarks_frame = create_section_frame(scroll_frame, "Remarks", 'indigo')
        remarks_text = ctk.CTkTextbox(remarks_frame, height=100, width=700)
        remarks_text.pack(pady=5, fill="both", expand=True)
        remarks_text.insert("1.0", "\n".join(extracted_data.get('Remarks', [])))
        
        def save_remarks():
            new_remarks = remarks_text.get("1.0", "end-1c")
            extracted_data['Remarks'] = new_remarks.split('\n')
            show_popup("Remarks updated!", 1500)
        
        save_btn = ctk.CTkButton(remarks_frame, text="Save Changes", 
                               command=save_remarks, fg_color="indigo")
        save_btn.pack(pady=5)
    
    # Display Day Operations
    if extracted_data.get('Day Operations'):
        operations_frame = create_section_frame(scroll_frame, "Day Operations", 'navy')
        display_operations(operations_frame, extracted_data.get('Day Operations', []), 'Day Operations')
    
    # Display Night Operations
    if extracted_data.get('Night Operations'):
        operations_frame = create_section_frame(scroll_frame, "Night Operations", 'purple4')
        display_operations(operations_frame, extracted_data.get('Night Operations', []), 'Night Operations')
    
    # Buttons for actions
    button_frame = ctk.CTkFrame(preview_window)
    button_frame.pack(pady=10, fill="x")
    
    save_btn = ctk.CTkButton(button_frame, text="Save All Changes", 
                          command=lambda: save_all_changes(preview_window),
                          fg_color="forest green", hover_color="green4")
    save_btn.pack(side="left", padx=20, pady=10)
    
    cancel_btn = ctk.CTkButton(button_frame, text="Cancel", 
                             command=preview_window.destroy,
                             fg_color="firebrick", hover_color="dark red")
    cancel_btn.pack(side="right", padx=20, pady=10)

# Helper function to create a section frame
def create_section_frame(parent, title, color):
    section_frame = ctk.CTkFrame(parent)
    section_frame.pack(pady=10, fill="both", expand=True)
    
    label = ctk.CTkLabel(section_frame, text=title, 
                       font=("Arial", 16, "bold"), 
                       fg_color=color, 
                       corner_radius=8,
                       text_color="white")
    label.pack(pady=5, fill="x")
    
    return section_frame

# Helper function to add editable field
def add_editable_field(parent, field_name, value, color):
    field_frame = ctk.CTkFrame(parent)
    field_frame.pack(pady=5, fill="x")
    
    label = ctk.CTkLabel(field_frame, text=field_name, width=150, 
                       font=("Arial", 14), fg_color=color, 
                       corner_radius=5, text_color="white")
    label.pack(side="left", padx=10, pady=5)
    
    entry = ctk.CTkEntry(field_frame, width=300, font=("Arial", 14))
    entry.pack(side="left", padx=10, pady=5)
    entry.insert(0, value if value else "")
    
    # Store reference to this entry widget and its field name for later retrieval
    entry.field_name = field_name
    
    # Add extendable arrow functionality
    extend_btn = ctk.CTkButton(field_frame, text="↔", width=30, 
                             command=lambda: toggle_extension(entry, extend_btn),
                             fg_color=color, hover_color="gray30")
    extend_btn.pack(side="left", padx=5)
    extend_btn.is_extended = False
    
    return entry

# Helper function to toggle extension of an entry field
def toggle_extension(entry_widget, button):
    if button.is_extended:
        entry_widget.configure(width=300)
        button.is_extended = False
    else:
        entry_widget.configure(width=500)
        button.is_extended = True

# Helper function to display operations
def display_operations(parent, operations, operations_key):
    if not operations:
        empty_label = ctk.CTkLabel(parent, text="No operations found")
        empty_label.pack(pady=5)
        return
    
    table_frame = ctk.CTkFrame(parent)
    table_frame.pack(pady=5, fill="both", expand=True)
    
    # Headers
    headers = ["Start Time", "End Time", "Duration", "Description"]
    for i, header in enumerate(headers):
        header_label = ctk.CTkLabel(table_frame, text=header, font=("Arial", 12, "bold"),
                                  fg_color="gray30", corner_radius=2, text_color="white")
        header_label.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
    
    # Operations
    for i, operation in enumerate(operations):
        row_entries = []
        for j, value in enumerate(operation[:3]):  # First three columns (start, end, duration)
            entry = ctk.CTkEntry(table_frame, width=80 if j < 2 else 60)
            entry.grid(row=i+1, column=j, padx=2, pady=2, sticky="ew")
            entry.insert(0, value)
            row_entries.append(entry)
        
        # Description field can be longer and might need extension
        desc_entry = ctk.CTkEntry(table_frame, width=300)
        desc_entry.grid(row=i+1, column=3, padx=2, pady=2, sticky="ew")
        desc_entry.insert(0, operation[3] if len(operation) > 3 else "")
        row_entries.append(desc_entry)
        
        # Extension button for description
        extend_btn = ctk.CTkButton(table_frame, text="↔", width=20, 
                                 command=lambda e=desc_entry, b=None: toggle_extension(e, extend_btn))
        extend_btn.grid(row=i+1, column=4, padx=2, pady=2)
        extend_btn.is_extended = False
        
        # Save the reference to these entries for the current operation row
        for entry in row_entries:
            entry.operation_index = i
            entry.operations_key = operations_key
    
    # Save changes button for this operation set
    save_ops_btn = ctk.CTkButton(parent, text=f"Save {operations_key}", 
                              command=lambda: save_operations(table_frame, operations_key))
    save_ops_btn.pack(pady=5)

# Function to save changes to operations
def save_operations(table_frame, operations_key):
    new_operations = []
    
    # Find all entry widgets in the table
    entries = [widget for widget in table_frame.winfo_children() if isinstance(widget, ctk.CTkEntry)]
    
    # Group entries by operation (every 4 entries form one operation)
    for i in range(0, len(entries), 4):
        if i+3 < len(entries):  # Ensure we have all fields
            start_time = entries[i].get()
            end_time = entries[i+1].get()
            duration = entries[i+2].get()
            description = entries[i+3].get()
            
            # Split description if needed
            split_desc = [description[j:j+65] for j in range(0, len(description), 65)]
            
            operation_entry = [start_time, end_time, duration] + split_desc
            new_operations.append(operation_entry)
    
    # Update extracted data
    global extracted_data
    extracted_data[operations_key] = new_operations
    
    show_popup(f"{operations_key} updated!", 1500)

# Function to save all changes from the preview window
def save_all_changes(preview_window):
    # Collect all single-field entries
    entries = [widget for widget in preview_window.winfo_children()[0].winfo_children() 
               if isinstance(widget, ctk.CTkFrame)]
    
    # Update basic fields (Date, Present Depth, HSD Stock)
    for frame in entries:
        for widget in frame.winfo_children():
            if isinstance(widget, ctk.CTkEntry) and hasattr(widget, 'field_name'):
                field_name = widget.field_name
                new_value = widget.get()
                global extracted_data
                extracted_data[field_name] = new_value
    
    show_popup("All changes saved!", 2000)
    preview_window.destroy()
    
    # Update the status label
    status_label.configure(text="Data extraction and modification complete", text_color="cyan")

# Function to automate the PDF filling process
def start_execution():
    message = input_text.get("1.0", "end-1c")
    selected_pdf = pdf_dropdown.get()
    
    # Check if we already have extracted data
    global extracted_data
    if not extracted_data:
        if not message.strip():
            status_label.configure(text="Error: Please enter valid input", text_color="red")
            return
        
        status_label.configure(text="Processing...", text_color="yellow")
        
        # Extract data first
        extracted_data = extract_data(message)
    
    print(extracted_data)

    formatted_date = format_date(extracted_data.get('Date', ''))
    
    # Copy the selected PDF with the extracted date as filename
    pdf_path = copy_pdf(selected_pdf, formatted_date)
    open_pdf(pdf_path)
    time.sleep(4)  # Simulate processing time

    # Type data into PDF based on selected checkboxes
    # Execute functions based on checkbox selections
    type_date(extracted_data['Date'])

    if remarks_var.get() and extracted_data.get('Remarks'):
        type_remarks(extracted_data['Remarks'])
    if hsd_stock_var.get() and extracted_data.get('HSD Stock'):
        type_hsd_stock(extracted_data['HSD Stock'])
    if present_depth_var.get() and extracted_data.get('Present Depth'):
        type_present_depth(extracted_data['Present Depth'])
    if day_operations_var.get() and extracted_data.get('Day Operations'):
        type_operations(extracted_data.get('Day Operations', []), start_y=413)
    if night_operations_var.get() and extracted_data.get('Night Operations'):
        type_operations(extracted_data.get('Night Operations', []), start_y=641)

    status_label.configure(text="Execution Completed!", text_color="green")

    # Show pop-up notification
    show_popup("Execution Completed!", duration=3000)
    
    # Reset the extracted data for the next run
    extracted_data = {}

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

# Checkboxes for each function
remarks_checkbox = ctk.CTkCheckBox(checkbox_frame, text="Type Remarks", variable=remarks_var, font=("Arial", 14), width=fixed_width)
remarks_checkbox.pack(anchor="w", pady=2)

hsd_stock_checkbox = ctk.CTkCheckBox(checkbox_frame, text="Type HSD Stock", variable=hsd_stock_var, font=("Arial", 14), width=fixed_width)
hsd_stock_checkbox.pack(anchor="w", pady=2)

present_depth_checkbox = ctk.CTkCheckBox(checkbox_frame, text="Type Present Depth", variable=present_depth_var, font=("Arial", 14), width=fixed_width)
present_depth_checkbox.pack(anchor="w", pady=2)

day_operations_checkbox = ctk.CTkCheckBox(checkbox_frame, text="Type Day Operations", variable=day_operations_var, font=("Arial", 14), width=fixed_width)
day_operations_checkbox.pack(anchor="w", pady=2)

night_operations_checkbox = ctk.CTkCheckBox(checkbox_frame, text="Type Night Operations", variable=night_operations_var, font=("Arial", 14), width=fixed_width)
night_operations_checkbox.pack(anchor="w", pady=2)

# Button Frame (to hold both buttons)
button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=10)

# Show & Modify Selection Button
show_modify_button = ctk.CTkButton(
    button_frame, 
    text="Show & Modify Selection", 
    font=("Arial", 16), 
    command=show_and_modify_selection,
    fg_color="purple",
    hover_color="dark violet"
)
show_modify_button.pack(side="left", padx=10)

# Start Button
start_button = ctk.CTkButton(
    button_frame, 
    text="Start Execution", 
    font=("Arial", 16), 
    command=lambda: threading.Thread(target=start_execution).start()
)
start_button.pack(side="left", padx=10)

# Status Label
status_label = ctk.CTkLabel(app, text="", font=("Arial", 14))
status_label.pack(pady=10)

# Settings Button (Top Right)
settings_button = ctk.CTkButton(app, text="⚙", width=30, command=open_settings_popup)
settings_button.place(x=750, y=10)

# Run the App
app.mainloop()