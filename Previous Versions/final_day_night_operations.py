import time
import pyautogui
import shutil
import subprocess
from pathlib import Path

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

message = {
    'Present Depth': '3032',
    'HSD Stock': '83756',
    'Day Operations': [
        ['06:00', '15:30', '9.5', '- First',
     'Second','- 3',
     '4','- Fifth',
     '6','- 7',
     '8','- Nine',
     '10','11','12'],
    ],
    'Night Operations': [
        ['06:00', '15:30', '9.5', '- First',
     'Second','- 3',
     '4','- Fifth',
     '6','- 7',
     '8','- Nine',
     '10','11','12'],
    ],
    'Remarks': [
        '01 MOTOR NOT WORKING EFFICIENTLY*',
        'OBSD LEAKAGE FROM LIFTING ARM OF METALIC PRESSURE LINE OF HYD CATWALK.',
        'AVPH IS OUT OF ORDER.',
        'OBSD MUD LEAKAGE FROM I-BOP IN CLOSED CONDITION.',
        'OBSD 1ST TDS GUIDE RAIL (NEAR RIG FLOOR) OFFSET WITH REFERENCE TO REMAINING TDS GUIDE RAILING.'
    ]
}

sample_remarks = {'Present Depth': '3415', 'HSD Stock': 59666, 
 'Day Operations': [['06:00', '13:00', '7.0', '-CONTD PIPE BREAKING. B/OFF AND L/DN 18 STDS(TOTAL 30) OF 5" D/P ', 'INTO 54 SGLS.'], ['13:00', '15:30', '2.5', '- CONNECTED HYD LINES TO PROD BOP. C/O FUNCTION TEST. FOUND OK. R', '/I TEST PLUG WITH 01 SGL OF TBG. C/O PRESSURE TEST OF P-BOP AS PE', 'R NORMS. FOUND OK. P/O AND L/DN TEST PLUG WITH 01 SGL OF 2 7/8” T', 'BG.'], ['15:30', '03:00', '11.5', '- RESUMED PIPE BREAKING. B/OFF AND L/DN 47 STDS ( TOTAL 77 STDS) ', 'OF 5” D/P INTO 141 SGLS + 04 STDS OF 5” HWDP INTO 12 SGLS.', 'SOME JOINTS FOUND TIGHT. OPENED USING BOTH P/TONGS.', 'M/WHILE STACKED 2⅞" TUBINGS AND MEASURED THE SAME', 'GO-GAUGED TUBING PRIOR TO R/I.', '*# D/WORKS LUBE OIL HEAT EXCHANGER FAN MOTOR OUT OF ORDER.*', '*#S/SHAKER#01 MOTOR NOT WORKING EFFICIENTLY*']], 'Night Operations': [['03:00', '06:00', '3.0', '- M/A FOR R/I OF 7" SCRAPPER WITH 2⅞" TBG. M/UP SCRAPPER WITH X/O', ' & WELDED STRIPS ON JOINT. R/I SCRAPPER + X-O + 8 SGLS OF 2⅞" TBG', '. FRIIP.']], 
 'Remarks': ['Testing Typing Speed Testing Typing Speed Testing Typing Speed', 'Second Testing Typing SpeedTesting Typing Speed', 'Third Testing Typing Speed Testing Typing Speed']}


upt_message = {'Present Depth': '3415', 'HSD Stock': 59666, 
 'Day Operations': [['06:00', '13:00', '7.0', '-CONTD PIPE BREAKING. B/OFF AND L/DN 18 STDS(TOTAL 30) OF 5" D/P ', 'INTO 54 SGLS.'], ['13:00', '15:30', '2.5', '- CONNECTED HYD LINES TO PROD BOP. C/O FUNCTION TEST. FOUND OK. R', '/I TEST PLUG WITH 01 SGL OF TBG. C/O PRESSURE TEST OF P-BOP AS PE', 'R NORMS. FOUND OK. P/O AND L/DN TEST PLUG WITH 01 SGL OF 2 7/8” T', 'BG.'], ['15:30', '03:00', '11.5', '- RESUMED PIPE BREAKING. B/OFF AND L/DN 47 STDS ( TOTAL 77 STDS) ', 'OF 5” D/P INTO 141 SGLS + 04 STDS OF 5” HWDP INTO 12 SGLS.', 'SOME JOINTS FOUND TIGHT. OPENED USING BOTH P/TONGS.', 'M/WHILE STACKED 2⅞" TUBINGS AND MEASURED THE SAME', 'GO-GAUGED TUBING PRIOR TO R/I.', '*# D/WORKS LUBE OIL HEAT EXCHANGER FAN MOTOR OUT OF ORDER.*', '*#S/SHAKER#01 MOTOR NOT WORKING EFFICIENTLY*']], 'Night Operations': [['03:00', '06:00', '3.0', '- M/A FOR R/I OF 7" SCRAPPER WITH 2⅞" TBG. M/UP SCRAPPER WITH X/O', ' & WELDED STRIPS ON JOINT. R/I SCRAPPER + X-O + 8 SGLS OF 2⅞" TBG', '. FRIIP.']], 
 'Remarks': ['D/WORKS LUBE OIL HEAT EXCHANGER FAN MOTOR OUT OF ORDER.* S/SHAKER#01 MOTOR NOT WORKING EFFICIENTLY*', 'AVPH IS OUT OF ORDER. OBSD MUD LEAKAGE FROM I-BOP IN CLOSED CONDITION. OBSD 1ST TDS GUIDE RAIL (NEAR', 'RIG FLOOR) OFFSET WITH REFERENCE TO REMAINING TDS GUIDE RAILING.']}




pdf_path = copy_pdf()  # Copy the PDF file
open_pdf(pdf_path)  # Open the copied PDF

time.sleep(6)  # Give time to switch to the PDF

# # Start typing Remarks
# type_remarks(upt_message['Remarks'])

# Start typing HSD Stock
type_hsd_stock(upt_message['HSD Stock'])

# # Start typing HSD Stock
# type_present_depth(upt_message['Present Depth'])

# # Start typing operations for Day Operations
# type_operations(upt_message.get('Day Operations', []), start_y=413)

# # Start typing operations for Night Operations
# type_operations(upt_message.get('Night Operations', []), start_y=641)
