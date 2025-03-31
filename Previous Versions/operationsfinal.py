import time
import pyautogui
import keyboard  # For detecting key press
import sys

def type_operations(operations):
    start_x, start_y = 657, 413  # Starting position
    x_increment = 23  # Change in x for first two elements
    y_increment = 8.27  # Change in y for rest of the elements after third
    jump_x = 818  # x position jump for third element
    
    current_y = start_y  # Track last y position
    
    for operation in operations:
        x, y = start_x, current_y  # Use last y position for next sublist
        for i, element in enumerate(operation):
            if keyboard.is_pressed('esc'):
                print("Script terminated by user.")
                sys.exit(0)
            
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

# message = {
#     'Present Depth': '3415',
#     'HSD Stock': 43174,
#     'Operations': [
#         ['06:00', '15:30', '9.5', '- RIG UP WIRELINE UNIT AND INSTALLATED STANDING VALVE.',
#          'CEMENTING UNIT REPORTED AT D/SITE AT 1000 HRS. M/A AND *SET HYDRA',
#          'ULIC PACKER* AT 2800 PSI. CHECKED RETURN AT 500 PSI, OBSD NO RETU',
#          'RN. P/O STANDING VALVE AND R/DN WIRELINE UNIT.',
#          'KNOCKOUT 1500 M WATER COLUMN BY GAS INJECTION.'],
#         ['15:30', '21:00', '5.5', '- C/O JSA AND *PERFORATED  OBJECT-1 IN THE INTERVAL 3214 M-3216M*',
#          ' M BY UB-TCP(S&D). OBSD SURFACE INDICATION OF PERFORATION. KNOCKO',
#          'UT WELL VOLUME  BY GAS INJECTION.',
#          'WELL IS DIVERTED TO GGS-3 AFTER KNOCKOUT OF  *31.8 M3* WELL VOLUM',
#          'E INTO OIL TANK.',
#          'WELL UNDER OBSERVATION, *WELL BECAME ACTIVE  WITH OIL &  WATER*'],
#         ['21:00', '06:00', '9.0', '- STOPPED GAS INJECTION. WELL IS FLOWING TO GGS-3',
#          'VIA 6MM BEAN.',
#          'TOTAL FIVE SAMPLE COLLECTED. SAMPLE AVERAGE DENSITY: 0.81 SG',
#          'TOTAL WATER PERCENTAGE BY VOLUME: SAMPLE 1- 1.8 & SAMPLE 2- 27.']
#     ],
#     'Remarks': [
#         'D/WORKS LUBE OIL HEAT EXCHANGER FAN MOTOR OUT OF ORDER.* ',
#         'S/SHAKER#01 MOTOR NOT WORKING EFFICIENTLY* ',
#         '*CHEMISTRY MUD CONTINGENTS ARE NOT REPORTED FROM 01.03.2025* ',
#         'AVPH IS OUT OF ORDER.',
#         'OBSD MUD LEAKAGE FROM I-BOP IN CLOSED  CONDITION.',
#         'OBSD 1ST TDS GUIDE RAIL (NEAR RIG FLOOR) OFFSET WITH REFERENCE TO REMAINING TDS GUIDE RAILING.'
#     ]
# }

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

time.sleep(5)  # Give time to switch to the PDF

# Start typing operations
type_operations(message['Operations'])
