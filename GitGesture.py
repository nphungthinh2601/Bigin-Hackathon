import cv2
import mediapipe as mp
import pyautogui
import time
from tkinter import *
from PIL import Image, ImageTk

# Set up the pop-up screen
root = Tk()
root.title("Hand Gesture Detection")
root.geometry("500x500")

# Set up the video window
label = Label(root)
label.pack(padx=10, pady=10)

# Initialize the detection module
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Define a function to detect the thumb up gesture
def detect_thumb_up(image):
    isThumb = False
    with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        
        # Convert the image to RGB format
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process the image to detect hands
        results = hands.process(image)
        
        # Draw hand landmarks and gesture on the image
        annotated_image = image.copy()
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    annotated_image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    
                # Create a list of the finger landmark IDs
                finger_ids = [
                    mp_hands.HandLandmark.INDEX_FINGER_TIP,
                    mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                    mp_hands.HandLandmark.RING_FINGER_TIP,
                    mp_hands.HandLandmark.PINKY_TIP
                ]
                
                # Check if all the fingers in the list are extended
                all_fingers_extended = all(
                    [hand_landmarks.landmark[finger_id].y < hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y
                     for finger_id in finger_ids])
                
                # Check if the thumb is up
                thumb_landmark = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                wrist_landmark = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                thumb_up = (thumb_landmark.y < wrist_landmark.y)
                
                # Draw the gesture text on the image
                if all_fingers_extended and thumb_up:
                    gesture_text = "Thumb up"
                    isThumb = True
                else:
                    gesture_text = ""
                cv2.putText(
                    annotated_image, gesture_text, (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
                
        # Return the annotated image
        return isThumb, annotated_image

# Set up the timeout variable
timeout = 0

# Capture video from the default webcam
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video stream
    ret, frame = cap.read()
    
    # Flip the frame horizontally for a mirrored view
    frame = cv2.flip(frame, 1)

    # Check if the timeout has expired
    if (time.time() > timeout):
        # Detect the hand gesture and draw on the image
        annotated_frame = detect_thumb_up(frame)

        # Check if a thumb up gesture is detected
        if annotated_frame[0]:
            # Set the timeout to 1 second into the future
            timeout = time.time() + 1.0
            
            # Perform a left click
            pyautogui.click()
            
            print("Left click performed!")
        
        # Convert the image to PIL format and display it in the pop-up screen
        image = Image.fromarray(cv2.cvtColor(annotated_frame[1], cv2.COLOR_BGR2RGB))
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
