import pyautogui
import time

print("Hover over the field you want to get the coordinates of, and wait for 5 seconds...")
time.sleep(4)  # Wait for 5 seconds before capturing the position

x, y = pyautogui.position()  # Get the current mouse position
print(f"Coordinates: x={x}, y={y}")
