import cv2
import mediapipe as mp
import pyautogui
from tkinter import *
from PIL import Image, ImageTk
import time

# Set up the pop-up screen
root = Tk()
root.title("Hand Gesture Detection")
root.geometry("1280x720")

# Set up the video window
label = Label(root)
label.pack(padx=10, pady=10)
thresold_y = 0.2
thresold_x = 0.2
scroll_up_amount = 600
# Initialize the detection module
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
timeout = 0
timeout_amount = 0.5
# Define a function to detect the thumb up gesture
def detect_abc(image):
    with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        
        # Convert the image to RGB format
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process the image to detect hands
        results = hands.process(image)
        
        # Draw hand landmarks on the image
        annotated_image = image.copy()
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    annotated_image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Check if the thumb is up
                thumb_landmark = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                wrist_landmark = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                if (thumb_landmark.y - wrist_landmark.y > thresold_y):
                    return 0
                if (wrist_landmark.y - thumb_landmark.y > thresold_y):
                    return 1
                if (thumb_landmark.x - wrist_landmark.x > thresold_x):
                    return 2
                if (wrist_landmark.x - thumb_landmark.x > thresold_x):
                    return 3
                
        # Return False if no thumb up gesture is detected
        return -1

# Capture video from the default webcam
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video stream
    ret, frame = cap.read()
    
    # Flip the frame horizontally for a mirrored view
    frame = cv2.flip(frame, 1)
    hehe = detect_abc(frame)
    print(hehe)

    # Detect the thumb up gesture
    if(time.time() > timeout):
        if hehe == 0:
            # Perform a left click
            pyautogui.scroll(scroll_up_amount)
            print("scroll down performed!")
            timeout = time.time() + timeout_amount
        elif hehe == 1:
            # Perform a left click
            pyautogui.scroll(-scroll_up_amount)

            print("scroll up performed!")

            timeout = time.time() + timeout_amount
        elif hehe == 2:
            # Perform a left click
            pyautogui.click()
            timeout = time.time() + timeout_amount
            print("Left click performed!")
        elif hehe == 3:
            # Perform a left click
            # pyautogui.click(button=2)
            timeout = time.time() + timeout_amount
            print("right click performed!")
            
    
    # Convert the image to PIL format and display it in the pop-up screen
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    photo = ImageTk.PhotoImage(image=image)
    label.config(image=photo)
    label.image = photo
    # cv2.imshow('Hand Gesture Detection', frame)
    # Update the GUI
    root.update()
    
    # If the user presses "q", break out of the loop and exit
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break

# Release the video stream and close all windows
cap.release()
cv2.destroyAllWindows()
root.destroy()