import time
import pyautogui
import shutil
import subprocess
from pathlib import Path
import re

message4 = '''*MDPR*
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

    # Extract Operations (Splitting into Day and Night Operations)
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
                
                if start_hour >= 20 or start_hour < 6:  # Night shift (8 PM - 6 AM)
                    night_operations.append(operation_entry)
                else:
                    day_operations.append(operation_entry)
                    
            elif (day_operations or night_operations) and line.strip():
                split_desc = [line.strip()[i:i+65] for i in range(0, len(line.strip()), 65)]
                
                # Append additional details to the last operation in the correct category
                if night_operations and start_hour >= 20:
                    night_operations[-1].extend(split_desc)
                elif day_operations:
                    day_operations[-1].extend(split_desc)

        data['Day Operations'] = day_operations
        data['Night Operations'] = night_operations
    else:
        data['Day Operations'] = []
        data['Night Operations'] = []

    # Extract Remarks and break into 100-character segments without breaking words
    remarks_text = " ".join(re.findall(r'(?i)#\s*(.*?)(?=\n|$)', message))

    def split_remarks(text, limit=100):
        words = text.split()
        result = []
        line = ""

        for word in words:
            if len(line) + len(word) + 1 <= limit:  # +1 for space
                line += " " + word if line else word
            else:
                result.append(line)
                line = word  # Start new line with the word

        if line:
            result.append(line)  # Add last line

        return result

    data['Remarks'] = split_remarks(remarks_text) if remarks_text else None

    return data


# Extracting data
upt_message = extract_data(message4)
# print(upt_message)




# Code For Entering Content in PDF 
def copy_pdf():
    src_path = Path("src/SAMPLE.pdf")  # Source file path
    dest_path = Path("SAMPLE_copy.pdf")  # Destination file path in root folder
    shutil.copy(src_path, dest_path)  # Copy the file
    return dest_path

def open_pdf(pdf_path):
    subprocess.Popen(["open", "-a", "Adobe Acrobat Reader", str(pdf_path)])  # Open PDF

def type_operations(operations, start_y):
    start_x = 657  # Starting x position
    x_increment = 23  # Change in x for first two elements
    y_increment = 8.27 # Change in y for rest of the elements after third
    jump_x = 818  # x position jump for third element
    
    current_y = start_y  # Track last y position
    
    for operation in operations:
        x, y = start_x, current_y  # Use last y position for next sublist
        for i, element in enumerate(operation):
            pyautogui.click(x, y)  # Click to focus (optional, depends on PDF editor)
            pyautogui.typewrite(str(element))
            time.sleep(0.02)  # Short delay to simulate typing
            
            if i == 0:
                x += x_increment  # Move x for second element
            elif i == 1:
                x += x_increment  # Move x for third element
            elif i == 2:
                x = jump_x  # Jump to new x for rest of the elements
            else:
                y += y_increment  # Modify y for the remaining elements
        
        current_y = y  # Update y to avoid overwriting next sublist
        time.sleep(0.01)  # Delay between typing actions

def type_hsd_stock(hsd_stock):
    x, y = 803, 772  # Coordinates for HSD Stock
    pyautogui.click(x, y)
    pyautogui.typewrite(str(hsd_stock))
    time.sleep(0.01)

def type_present_depth(present_depth):
    x, y = 510, 210  # Coordinates for HSD Stock
    pyautogui.click(x, y)
    pyautogui.typewrite(str(present_depth))
    time.sleep(0.01)

def type_remarks(remarks):
    x, y = 371, 437  # First set of remarks
    for remark in remarks:
        pyautogui.click(x, y)
        pyautogui.typewrite(remark)
        y += 7  # Increment y for next line
        time.sleep(0.01)
    
    x, y = 371, 670  # Repeat remarks at new position
    for remark in remarks:
        pyautogui.click(x, y)
        pyautogui.typewrite(remark)
        y += 7.6  # Increment y for next line
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


# pdf_path = copy_pdf()  # Copy the PDF file
# open_pdf(pdf_path)  # Open the copied PDF

time.sleep(3)  # Give time to switch to the PDF

type_date(upt_message['Date'])

# # Start typing Remarks
# type_remarks(upt_message['Remarks'])

# # Start typing HSD Stock
# type_hsd_stock(upt_message['HSD Stock'])

# # Start typing HSD Stock
# type_present_depth(upt_message['Present Depth'])

# # Start typing operations for Day Operations
# type_operations(upt_message.get('Day Operations', []), start_y=413)

# # Start typing operations for Night Operations
# type_operations(upt_message.get('Night Operations', []), start_y=641)
