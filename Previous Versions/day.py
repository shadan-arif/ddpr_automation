import pyautogui
import subprocess
import time

def open_pdf(pdf_path):
    # Open the PDF file with Adobe Acrobat Reader
    subprocess.Popen(["open", "-a", "Adobe Acrobat Reader", pdf_path])  # Change to the appropriate application if needed
    time.sleep(5)  # Wait for the PDF to open

def type_text_at_coordinates(coordinates, texts):
    # Move to the coordinates and click to focus the field
    for (x, y), text in zip(coordinates, texts):
        pyautogui.click(x, y)  # Click on the field
        time.sleep(0.5)  # Wait for half a second
        pyautogui.typewrite(text)  # Type the text
        time.sleep(0.5)  # Wait for half a second before moving to the next field

if __name__ == "__main__":
    # Path to your PDF file
    pdf_path = "src/19.pdf"

    
    # Open the PDF file
    open_pdf(pdf_path)

    # Predefined coordinates where text should be entered
    coordinates = [
        (1006, 645),
        (1005, 663),
        (1005, 678),
        (1005, 695)
    ]

    # Corresponding texts to be typed at each coordinate
    # texts_to_type = ["ONE", "TWO", "THREE", "FOUR"]
    # texts_to_type = [
    # "FITTED 21 1/4” X 2M BOP STACK ON BOP CART. TIGHTE",
    # "NED CLAMP OF BOP CART. TESTED BOP CART. FOUND OK.",
    # "FITTED INCLINED WALK. CONNECTED MCP-01 AND UTILIT",
    # "Y HOUSE TALKBACK CABLE. CHECKED RACKING BOARD \nLAT"
    # ] This one has 50 characters each

    texts_to_type =[
    "FITTED 21 1/4” X 2M BOP STACK ON BOP CART. TIGHTENED CLAMP OF BOP",
    "CART. TESTED BOP CART. FOUND OK. FITTED INCLINED WALK. CONNECTED",
    "MCP-01 AND UTILITY HOUSE TALKBACK CABLE. CHECKED RACKING BOARD",
    "LATCHES. FOUND ISSUES WITH BIN-1 2,5,11,12 AND BIN-2 10,12"]

    # Type the specified texts at the predefined coordinates
    type_text_at_coordinates(coordinates, texts_to_type)

    print("Text entry completed.")
