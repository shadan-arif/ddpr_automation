import tkinter as tk
from tkinter import ttk, messagebox
import time
import pyautogui
import shutil
import subprocess
from pathlib import Path
import re

def extract_data(message):
    data = {}

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
def copy_pdf():
    src_path = Path("src/SAMPLE.pdf")
    dest_path = Path("SAMPLE_copy.pdf")
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
    time.sleep(0.01)

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

def start_execution():
    message4 = text_input.get("1.0", tk.END).strip()  

    if not message4:
        messagebox.showwarning("Warning", "Please enter a valid input!")
        return

    upt_message = extract_data(message4)  

    pdf_path = copy_pdf()  
    open_pdf(pdf_path)  

    time.sleep(3)  

    type_remarks(upt_message['Remarks'])
    type_hsd_stock(upt_message['HSD Stock'])
    type_present_depth(upt_message['Present Depth'])
    type_operations(upt_message.get('Day Operations', []), start_y=413)
    type_operations(upt_message.get('Night Operations', []), start_y=641)

    messagebox.showinfo("Success", "Execution completed successfully!")

# GUI Setup
root = tk.Tk()
root.title("PDF Auto-Fill")
root.geometry("500x250")
root.configure(bg="#f5f5f5")

# Label
ttk.Label(root, text="Paste Message Here:", font=("Arial", 12)).pack(pady=5)

# Text Input
text_input = tk.Text(root, height=5, width=50, font=("Arial", 12))
text_input.pack(pady=5, padx=10)

# Execute Button
execute_btn = ttk.Button(root, text="Start Execution", command=start_execution)
execute_btn.pack(pady=10)

# Run GUI
root.mainloop()
