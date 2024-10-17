import subprocess
import pyautogui
import time

# Path to the PDF file
pdf_path = "src/19.pdf"

# Open the PDF file using Adobe Acrobat Reader
subprocess.Popen(["open", "-a", "Adobe Acrobat Reader", pdf_path])

# Allow some time for the PDF to open
time.sleep(5)  # Wait for 5 seconds to ensure the application has opened

# Now you can add your automation code to interact with the PDF
# Example: Typing in the field with name 'DOPDESC5'
# Replace the coordinates (x, y) with the actual position of the field
pyautogui.click(801, 577)  # Replace x and y with the actual coordinates of the field
pyautogui.typewrite("Hi there")
