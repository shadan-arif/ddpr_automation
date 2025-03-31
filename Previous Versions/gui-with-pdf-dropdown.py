import customtkinter as ctk
import threading
import time
import pyautogui
import shutil
import subprocess
from pathlib import Path
import re

# Initialize the app with a dark theme and modern styling
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# PDF Options
pdf_options = ["SAMPLE1.pdf", "SAMPLE2.pdf", "SAMPLE3.pdf", "SAMPLE4.pdf"]

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
def copy_pdf(selected_pdf):
    src_path = Path(f"src/{selected_pdf}")
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
    
    upt_message = extract_data(message4)
    pdf_path = copy_pdf(selected_pdf)
    open_pdf(pdf_path)
    time.sleep(4)  # Simulate processing time
    type_hsd_stock(upt_message['HSD Stock'])
    type_date(upt_message['Date'])

    status_label.configure(text="Execution Completed!", text_color="green")

# Create the main app window
app = ctk.CTk()
app.title("Automated DDPR Application")
app.geometry("600x450")

# Title Label
title_label = ctk.CTkLabel(app, text="Please Enter DDPR to Convert to IADC Format", font=("Arial", 20, "bold"))
title_label.pack(pady=10)

# Dropdown for PDF Selection
pdf_dropdown = ctk.CTkComboBox(app, values=pdf_options, font=("Arial", 14))
pdf_dropdown.pack(pady=10)
pdf_dropdown.set("SAMPLE1.pdf")  # Default selection

# Input Text Box
input_text = ctk.CTkTextbox(app, height=150, width=500, font=("Arial", 14))
input_text.pack(pady=10)

# Start Button
start_button = ctk.CTkButton(app, text="Start Execution", font=("Arial", 16), command=lambda: threading.Thread(target=start_execution).start())
start_button.pack(pady=10)

# Status Label
status_label = ctk.CTkLabel(app, text="", font=("Arial", 14))
status_label.pack(pady=10)

# Run the App
app.mainloop()



#sample
sample = ''' *MDPR*
*NG-1500-4*
*GNDHT*
*03.03.2025*
*0600 HRS*
*TARGET DEPTH: 3412 M*
*PRESENT DEPTH: 3415 M*
*OPERATIONS*

*0600-1300*:-CONTD PIPE BREAKING. B/OFF AND L/DN 18 STDS(TOTAL 30) OF 5" D/P INTO 54 SGLS.
*1300-1530*:- CONNECTED HYD LINES TO PROD BOP. C/O FUNCTION TEST. FOUND OK. R/I TEST PLUG WITH 01 SGL OF TBG. C/O PRESSURE TEST OF P-BOP AS PER NORMS. FOUND OK. P/O AND L/DN TEST PLUG WITH 01 SGL OF 2 7/8” TBG.
*1530-0300*:- RESUMED PIPE BREAKING. B/OFF AND L/DN 47 STDS ( TOTAL 77 STDS) OF 5” D/P INTO 141 SGLS + 04 STDS OF 5” HWDP INTO 12 SGLS.
SOME JOINTS FOUND TIGHT. OPENED USING BOTH P/TONGS.
*0300-0600*:- M/A FOR R/I OF 7" SCRAPPER WITH 2⅞" TBG. M/UP SCRAPPER WITH X/O & WELDED STRIPS ON JOINT. R/I SCRAPPER + X-O + 8 SGLS OF 2⅞" TBG. FRIIP.

M/WHILE STACKED 2⅞" TUBINGS AND MEASURED THE SAME
GO-GAUGED TUBING PRIOR TO R/I.

 *# D/WORKS LUBE OIL HEAT EXCHANGER FAN MOTOR OUT OF ORDER.*
 *#S/SHAKER#01 MOTOR NOT WORKING EFFICIENTLY*

*MUD PARAMETERS*
MW-1.38
Viscosity-56
PH-8.5
PV/YP-26/35
Gel 0/Gel 10 - 8/17
Water loss-5.5
Solid-15%
Sand<1%
KCl-6%
PHPA-0.4%

*NPT HRS*
DRILLING: NIL
MECHANICAL: NIL.
INSTRUMENTATION: NIL
ELECTRICAL: NIL

*NOTE*
FIRE FIGHTING SYSTEM- OK
ACC/FIRE/NM: NIL

*HSD STOCK:- 59666 L*
*GAS CONSUMPTION: 1485.3 m³*

*Note*:-
1)VEHICLE FOR GENERAL SHIFT DUTY: GJ23AW 2765
2) VEHICLE FOR EMERGENCY DUTY: GJ16AV 5156

*REQUIREMENTS*
1.AMBULANCE FOR DRILL SITE
2) TECHNICAL WATER-
3) DRINKING WATER -  *05 Tankers*.

*REMARKS*
# AVPH IS OUT OF ORDER.
# OBSD MUD LEAKAGE FROM I-BOP IN CLOSED  CONDITION.
# OBSD 1ST TDS GUIDE RAIL (NEAR RIG FLOOR) OFFSET WITH REFERENCE TO REMAINING TDS GUIDE RAILING.'''