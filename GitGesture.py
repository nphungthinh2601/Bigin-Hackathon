import cv2
import mediapipe as mp
import pyautogui
from tkinter import *
from PIL import Image, ImageTk

# Set up the pop-up screen
root = Tk()
root.title("Hand Gesture Detection")
root.geometry("1280x720")

# Set up the video window
label = Label(root)
label.pack(padx=10, pady=10)

# Initialize the detection module
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Define a function to detect the thumb up gesture
def detect_thumb_up(image):
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
                if (thumb_landmark.y < wrist_landmark.y):
                    return True
                
        # Return False if no thumb up gesture is detected
        return False

# Capture video from the default webcam
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video stream
    ret, frame = cap.read()
    
    # Flip the frame horizontally for a mirrored view
    frame = cv2.flip(frame, 1)
    
    # Detect the thumb up gesture
    if detect_thumb_up(frame):
        # Perform a left click
        pyautogui.click()
        
        print("Left click performed!")
    
    # Convert the image to PIL format and display it in the pop-up screen
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    photo = ImageTk.PhotoImage(image=image)
    label.config(image=photo)
    label.image = photo

    # Update the GUI
    root.update()
    
    # If the user presses "q", break out of the loop and exit
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break

# Release the video stream and close all windows
cap.release()
cv2.destroyAllWindows()
root.destroy()
