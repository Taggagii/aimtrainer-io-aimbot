import numpy as np
import cv2
from mss import mss
import pyautogui as pp
from pynput import keyboard, mouse
import tkinter.messagebox

running = True

def on_press(key):
    global running
    try: 
        if key.char == 'q':
            running = False
    except:
        pass

top, left, bottom, right = None, None, None, None

def on_click(x, y, button, pressed):
    global top
    global left
    global bottom
    global right
    
    if button == mouse.Button.left and pressed:
        if (top == None and left == None):
            top = y
            left = x
            print(f"TOP: {top} | LEFT: {left}")
        elif (bottom == None and right == None):
            bottom = y
            right = x
            print(f"BOTTOM: {bottom} | RIGHT: {right}")
            return False

tkinter.messagebox.showinfo(title="Instructions", message="Website: https://aimtrainer.io/challenge\n\nREAD BELOW: \n\nClick on the top left and bottom right of the game window (where the targets appear) AFTER closing this popup to select the bounds for the program to run in. You should see an output in the console every time you click\n\nType 'q' at any point after selecting the bounds to close this program")

keyboard_listener = keyboard.Listener(on_press=on_press)
keyboard_listener.start()

with mouse.Listener(on_click=on_click) as listener:
    listener.join()

sct = mss()


monitor = sct.monitors[1]
left_crop = 550
right_crop = 550
bottom_crop = 225
top_crop = 325

boundary = {'top': top, 'left': left, 'width': abs(left - right), 'height': abs(top - bottom)}

def grab_frame():
    frame = sct.grab(boundary)
    frame = np.array(frame)
    return frame


while running:
    const_frame = grab_frame()

    temp_frame = const_frame.copy()

    hsv = cv2.cvtColor(temp_frame, cv2.COLOR_BGR2HSV)
    
    lower_red = np.array([0,100,100])
    upper_red = np.array([255, 255, 255])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    rect_list = []

    for contour in contours: 
        rect = cv2.boundingRect(contour)

        if (cv2.contourArea(contour) < 65):
            continue

        rect_list.append(rect)
        
            

    rects, groupings = cv2.groupRectangles(rect_list, 1)

    for rect, group in zip(rects, groupings):
        (x, y, w, h) = rect

        center_x, center_y = x + w // 2, y + h // 2

        cv2.circle(temp_frame, (center_x, center_y), 5, (0, 255, 0), 2)
        pp.moveTo(boundary['left'] + center_x, boundary['top'] + center_y)
        pp.click()
        

    # cv2.imshow('screen', temp_frame)
    # cv2.waitKey(1)

    prev_frame = const_frame
cv2.destroyAllWindows()