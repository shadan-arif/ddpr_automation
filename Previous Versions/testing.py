import time
import pyautogui


def type_operations(operations):
    start_x, start_y = 657, 413  # Starting position
    x_increment = 23  # Change in x for first two elements
    y_increment = 8.27  # Change in y for rest of the elements after third
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

message = {
    'Present Depth': '3415',
    'HSD Stock': 43174,
    'Operations': [
    ['06:00', '15:30', '9.5', '- First',
     'Second'],
    ['15:30', '21:00', '5.5', '- First',
     'Second'],
    ['21:00', '06:00', '9.0', '- First',
     'Second']
    ],
    'Remarks': [
        'D/WORKS LUBE OIL HEAT EXCHANGER FAN MOTOR OUT OF ORDER.* ',
        'S/SHAKER#01 MOTOR NOT WORKING EFFICIENTLY* ',
        '*CHEMISTRY MUD CONTINGENTS ARE NOT REPORTED FROM 01.03.2025* ',
        'AVPH IS OUT OF ORDER.',
        'OBSD MUD LEAKAGE FROM I-BOP IN CLOSED  CONDITION.',
        'OBSD 1ST TDS GUIDE RAIL (NEAR RIG FLOOR) OFFSET WITH REFERENCE TO REMAINING TDS GUIDE RAILING.'
    ]
}

message1 = {'Present Depth': '3032', 
            'HSD Stock': None, 
            'Day Operations': [['06:00', '16:00', '10.0', '- CONT\'D P/O, FURTHER P/O 32 STANDS OF 5" D/P + 13 SINGLES OF 5" ', 'HWDP + D/JAR+ 1 SINGLE OF 5" HWPD + 2 STANDS OF 6 1/2" D/C+ 2 SIN', 'GLES OF NMDC. FURTHER L/DN UBHO+ F/SUB + SDMM + 8 ½" PDC BIT.', '*TESTED MWD TOOL AT SURFACE AFTER P/OUT @ 30,40 & 70 SPM. FOUND O', 'K. OBSERVED NO SURVEY AT 90 SPM BUT OBSERVED PULSE*'], ['16:00', '20:00', '4.0', '- M/A FOR R/I. M/UP 8 ½" PDC BIT + SDMM + S/STAB+ FLOAT SUB+ UBHO', ' + TWO NMDC.', '*SURFACE TESTED MWD TOOL AND SDMM. OBSERVED SURVEY WITH SEPERATE ', 'PUMPS, AND ALSO RECEIVED SURVEY DATA WITH BOTH MUD PUMPS @ TOTAL ', '70 SPM. BUT NO SURVEY DATA ABOVE\xa0\xa090 SPM WITH BOTH MUD PUMPS, DEC', 'IDED TO RI AS PER INSTRUCTION FROM I/C DD ONGC ANK*', 'R/I 02 STDS OF 6 ½" D/C.']], 
            'Night Operations': [['20:00', '06:00', '10.0', '- R/I 05 STDS OF HWDP WITH D/JAR + 80 STDS OF 5" D/P UPTO C/SHOE.', ' *TESTED MWD TOOL AT 70 SPM, FOUND OK* RESUMED R/I. *OBSD SEVERE ', 'H/UP AT 2800 M*, UNABLE TO CLEAR BY RECIPROCATION. CONNECTED TDS ', 'AND CLEARED UPTO 2834 M. RESUMED R/I. OBSD *SEVERE H/UP AT 2975 M', '*. CLEARING BY REAMING IIP.', '*S/SHAKER #01 MOTOR NOT WORKING EFFICIENTLY*', '*RECTIFIED THE PROBLEM OF DGB BY MECH & INSTRUMENTATION (RIG) TEA', 'M, DGB IS WORKING*', '*CHECKED 7" C/S, OBSERVED SURFACE CRACK AND LEAKAGE FROM SIDE*']], 
            'Remarks': ['01 MOTOR NOT WORKING EFFICIENTLY*', 'OBSD LEAKAGE FROM LIFTING ARM OF METALIC PRESSURE LINE OF HYD CATWALK.', 'AVPH IS OUT OF ORDER.', 'OBSD MUD LEAKAGE FROM I-BOP IN CLOSED CONDITION.', 'OBSD 1ST TDS GUIDE RAIL (NEAR RIG FLOOR) OFFSET WITH REFERENCE TO REMAINING TDS GUIDE RAILING.']}




time.sleep(5)  # Give time to switch to the PDF

# Start typing operations
type_operations(message1['Day Operations'])
