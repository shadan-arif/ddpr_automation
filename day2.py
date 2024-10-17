import pyautogui
import subprocess
import time

def open_pdf(pdf_path):
    # Open the PDF file with Adobe Acrobat Reader
    subprocess.Popen(["open", "-a", "Adobe Acrobat Reader", pdf_path]) # Change to the appropriate application if needed
    time.sleep(2)  # Wait for the PDF to open

def type_text_at_coordinates(start_x, start_y, increment, texts):
    # Move to the coordinates and click to focus the field
    for index, text in enumerate(texts):
        x = start_x
        y = start_y + (index * increment)  # Increment y by 16 for each text
        pyautogui.click(x, y)  # Click on the field
        time.sleep(0.5)  # Wait for half a second
        pyautogui.typewrite(text)  # Type the text
        time.sleep(0.5)  # Wait for half a second before moving to the next field

if __name__ == "__main__":
    # Path to your PDF file
    pdf_path = "src/19.pdf"
    
    # Open the PDF file
    open_pdf(pdf_path)

    # Fixed coordinates and increment
    start_x = 1006
    start_y = 645
    increment = 16.636

    # Texts to be typed at each coordinate
    texts_to_type = [
        "FITTED 21 1/4” X 2M BOP STACK ON BOP CART. TIGHTENED CLAMP OF BOP",
        "CART. TESTED BOP CART. FOUND OK. FITTED INCLINED WALK. CONNECTED",
        "MCP-01 AND UTILITY HOUSE TALKBACK CABLE. CHECKED RACKING BOARD",
        "LATCHES. FOUND ISSUES WITH BIN-1 2,5,11,12 AND BIN-2 10,12",
        "LATCHES. RECTIFICATION OF THE SAME IIP. SCADA CONNECTION DONE.",
        "LAID DAS POWER SUPPLY CABLE FROM PIG HOUSE TO DRILL-PCR.",
        "RECTIFIED POWER SUPPLY ISSUE OF RACKING BOARD JUNCTION BOX.",
        "RECTIFIED POWER SUPPLY ISSUE OF LIGHTING CIRCUIT ON EDG. REPLACED",
        "AND RECTIFIED PUPPET VALVE OF DS AIR WINCH. TESTED AND FOUND OK.",
        "FILLED COOLANT IN POWERPACK-3."
    ]

    # texts_to_type = [
    # "ONE", "TWO", "THREE", "FOUR", "FIVE", 
    # "SIX", "SEVEN", "EIGHT", "NINE", "TEN", 
    # "ELEVEN", "TWELVE"
    # ]   

    # Type the specified texts at the predefined coordinates
    type_text_at_coordinates(start_x, start_y, increment, texts_to_type)

    print("Text entry completed.")
