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
    pdf_path = "src/11th OCT.pdf"
    
    # Open the PDF file
    open_pdf(pdf_path)

    # Fixed coordinates and increment
    start_x = 1006
    start_y = 645
    increment = 16.636

    # Texts to be typed at each coordinate
    texts_to_type = ["RIG OUT OF CYCLE FOR RIG INTER ASSET MOVEMENT FROM JODHPUR ASSET", "TO ANK ASSET, FURTHER RIG BUILDING IS IN PROGRESS. DRILLING", "FITTED LADDER FROM RIG FLOOR TO MUD TANKS. PLACED BOP CART ON", "IT'S RAILS. PLACED MUD CLEANER CUTTING TRAY. FITTED RETURN FLOW", "LINE. PLACED DGB. CONNECTED 500 TON LINKS TO TDS. HANGED FALSE", "CONDUCTOR ON TDS. M/A & GROUTED THE SAME. M/W M/UP 21¼ X 2M", "ANNULAR BOP WITH 21 1/4 X 2M DOUBLE RAM BOP. MECHANICAL SERVICING", "OF TDS COMPLETE.GEAR OIL AND LUBE OIL CHANGED . MP2 FLUSHING", "MOTOR JAMMED. RECTIFIED.CATWALK VALVE LEAKAGE FOUND. HEX NIPPLE", "RING REPLACED AND FITTED BACK."]
    
    # texts_to_type = [
    # "ONE", "TWO", "THREE", "FOUR", "FIVE", 
    # "SIX", "SEVEN", "EIGHT", "NINE", "TEN", 
    # "ELEVEN", "TWELVE"
    # ]   

    # Type the specified texts at the predefined coordinates
    type_text_at_coordinates(start_x, start_y, increment, texts_to_type)

    print("Text entry completed.")
