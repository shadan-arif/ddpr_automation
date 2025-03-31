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

def type_operations(operations, operation_type):
    start_x, start_y = 657, 413 if operation_type == 'Day Operations' else 642  # Starting y position based on type
    x_increment = 23  # Change in x for first two elements
    y_increment = 9  # Change in y for rest of the elements after third
    jump_x = 818  # x position jump for third element
    
    current_y = start_y  # Track last y position
    
    for operation in operations:
        x, y = start_x, current_y  # Use last y position for next sublist
        for i, element in enumerate(operation):
            pyautogui.click(x, y)  # Click to focus (optional, depends on PDF editor)
            pyautogui.typewrite(str(element))
            time.sleep(0.2)  # Short delay to simulate typing
            
            if i == 0:
                x += x_increment  # Move x for second element
            elif i == 1:
                x += x_increment  # Move x for third element
            elif i == 2:
                x = jump_x  # Jump to new x for rest of the elements
            else:
                y += y_increment  # Modify y for the remaining elements
        
        current_y = y  # Update y to avoid overwriting next sublist
        time.sleep(0.1)  # Delay between typing actions

def type_hsd_stock(stock_value):
    x, y = 803, 772
    pyautogui.click(x, y)
    pyautogui.typewrite(str(stock_value) if stock_value else "N/A")
    time.sleep(0.2)

def type_remarks(remarks):
    x, y = 371, 437
    for remark in remarks:
        pyautogui.click(x, y)
        pyautogui.typewrite(str(remark))
        y += 7  # Increment y position
    
    x, y = 371, 670  # Repeat at new position
    for remark in remarks:
        pyautogui.click(x, y)
        pyautogui.typewrite(str(remark))
        y += 7

message = {
    'Present Depth': '3032',
    'HSD Stock': '349534',
    'Day Operations': [['06:00', '16:00', '10.0', '- CONT\'D P/O, FURTHER P/O 32 STANDS OF 5" D/P + 13 SINGLES OF 5" ',
        'HWDP + D/JAR+ 1 SINGLE OF 5" HWPD + 2 STANDS OF 6 1/2" D/C+ 2 SIN',
        'GLES OF NMDC. FURTHER L/DN UBHO+ F/SUB + SDMM + 8 ½" PDC BIT.',
        '*TESTED MWD TOOL AT SURFACE AFTER P/OUT @ 30,40 & 70 SPM. FOUND O',
        'K. OBSERVED NO SURVEY AT 90 SPM BUT OBSERVED PULSE*'],
        ['16:00', '20:00', '4.0', '- M/A FOR R/I. M/UP 8 ½" PDC BIT + SDMM + S/STAB+ FLOAT SUB+ UBHO',
        ' + TWO NMDC.',
        '*SURFACE TESTED MWD TOOL AND SDMM. OBSERVED SURVEY WITH SEPERATE ',
        'PUMPS, AND ALSO RECEIVED SURVEY DATA WITH BOTH MUD PUMPS @ TOTAL ',
        '70 SPM. BUT NO SURVEY DATA ABOVE\xa0\xa090 SPM WITH BOTH MUD PUMPS, DEC',
        'IDED TO RI AS PER INSTRUCTION FROM I/C DD ONGC ANK*',
        'R/I 02 STDS OF 6 ½" D/C.']],
    'Night Operations': [['20:00', '06:00', '10.0', '- R/I 05 STDS OF HWDP WITH D/JAR + 80 STDS OF 5" D/P UPTO C/SHOE.',
        ' *TESTED MWD TOOL AT 70 SPM, FOUND OK* RESUMED R/I. *OBSD SEVERE ',
        'H/UP AT 2800 M*, UNABLE TO CLEAR BY RECIPROCATION. CONNECTED TDS ',
        'AND CLEARED UPTO 2834 M. RESUMED R/I. OBSD *SEVERE H/UP AT 2975 M',
        '*. CLEARING BY REAMING IIP.',
        '*S/SHAKER #01 MOTOR NOT WORKING EFFICIENTLY*',
        '*RECTIFIED THE PROBLEM OF DGB BY MECH & INSTRUMENTATION (RIG) TEA',
        'M, DGB IS WORKING*',
        '*CHECKED 7" C/S, OBSERVED SURFACE CRACK AND LEAKAGE FROM SIDE*']],
    'Remarks': [
        '01 MOTOR NOT WORKING EFFICIENTLY*',
        'OBSD LEAKAGE FROM LIFTING ARM OF METALIC PRESSURE LINE OF HYD CATWALK.',
        'AVPH IS OUT OF ORDER.',
        'OBSD MUD LEAKAGE FROM I-BOP IN CLOSED CONDITION.',
        'OBSD 1ST TDS GUIDE RAIL (NEAR RIG FLOOR) OFFSET WITH REFERENCE TO REMAINING TDS GUIDE RAILING.'
    ]
}

pdf_path = copy_pdf()  # Copy the PDF file
open_pdf(pdf_path)  # Open the copied PDF

time.sleep(10)  # Give time to switch to the PDF

# type_operations(message['Day Operations'], 'Day Operations')
# type_operations(message['Night Operations'], 'Night Operations')
type_hsd_stock(message['HSD Stock'])
# type_remarks(message['Remarks'])
