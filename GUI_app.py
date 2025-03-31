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

    for operation in operations:
        x, y = start_x, current_y  
        for i, element in enumerate(operation):
            pyautogui.click(x, y)  
            pyautogui.typewrite(str(element))
            time.sleep(0.02)  

            if i == 0:
                x += x_increment  
            elif i == 1:
                x += x_increment  
            elif i == 2:
                x = jump_x  
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

# Function to automate the PDF filling process
def start_execution():
    message4 = input_text.get("1.0", "end-1c")
    selected_pdf = pdf_dropdown.get()
    
    if not message4.strip():
        status_label.configure(text="Error: Please enter valid input", text_color="red")
        return
    
    status_label.configure(text="Processing...", text_color="yellow")
    
    # Extract data first
    upt_message = extract_data(message4)
    print(upt_message)

    formatted_date = format_date(upt_message.get('Date', ''))
    
    # Copy the selected PDF with the extracted date as filename
    pdf_path = copy_pdf(selected_pdf, formatted_date)
    open_pdf(pdf_path)
    time.sleep(4)  # Simulate processing time


    # type_hsd_stock(upt_message['HSD Stock'])
    # type_date(upt_message['Date'])


    # Type data into PDF based on selected checkboxes
    # Execute functions based on checkbox selections
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

        

    status_label.configure(text="Execution Completed!", text_color="green")

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

# Start Button
start_button = ctk.CTkButton(app, text="Start Execution", font=("Arial", 16), command=lambda: threading.Thread(target=start_execution).start())
start_button.pack(pady=10)

# Status Label
status_label = ctk.CTkLabel(app, text="", font=("Arial", 14))
status_label.pack(pady=10)

# Run the App
app.mainloop()

