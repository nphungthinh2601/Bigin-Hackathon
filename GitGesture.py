import cv2
import mediapipe as mp
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Define variables for gesture detection
tip_ids = [4, 8, 12, 16, 20] # Fingertip landmarks
min_consecutive_frames = 5 # Minimum number of consecutive frames the gesture must be detected
min_y_dist = 0.06 # Minimum distance (in pixels) moved in the y-direction
min_y_dist = 0.06 # Minimum distance (in pixels) moved in the y-direction
scroll_up_amount = -600
scroll_up_amount = -600
timeout = 0
# Initialize the video feed
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    curr_frames_up = 0 # Current number of consecutive frames the gesture has been detected
    curr_frames_down = 0 # Current number of consecutive frames the gesture has been detected
    starting_y = None # Starting y-coordinate of the gesture
    starting_y_up = None # Starting y-coordinate of the gesture
    
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break
        # Flip the image horizontally for a mirrored view
        image = cv2.flip(image, 1)
        # Convert the BGR image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Process the image and detect hands
        results = hands.process(image_rgb)
        # Draw the hand landmarks on the image
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingertips_y = [hand_landmarks.landmark[i].y for hand_landmarks in results.multi_hand_landmarks for i in tip_ids]
            min_y = min(fingertips_y)
            if starting_y is None:
                    
                starting_y = min_y
            print("min_y      up " +str(min_y))
            print("starting_y up " +str(starting_y))

            y_dist = starting_y - min_y  
            print("y_dist up" +str(y_dist))
            # Check if the y-distance moved is greater than the minimum distance required
            if y_dist > min_y_dist:
                curr_frames_down += 1
                # Check if the gesture has been detected for the minimum number of consecutive frames
                if curr_frames_down >= min_consecutive_frames:
                    print("Swipe up gesture detected!")
                    pyautogui.scroll(scroll_up_amount)
                    curr_frames_down = 0
                    starting_y = None
            # else:
            #     curr_frames_down = 0
            #     starting_y = None  
                 
            max_y = max(fingertips_y)
            if starting_y_up is None:
                starting_y_up = max_y
            y_dist = max_y - starting_y_up
            print("y_dist down" +str(y_dist))

            # Check if the y-distance moved is greater than the minimum distance required
            if y_dist > min_y_dist:
                curr_frames_up += 1
                # Check if the gesture has been detected for the minimum number of consecutive frames
                if curr_frames_up >= min_consecutive_frames:
                    # Perform a scroll down action
                    pyautogui.scroll(-scroll_up_amount)
                    print("Swipe down gesture detected - Performing scroll down!")
                    curr_frames_up = 0
                    starting_y = None
            # else:
            #     curr_frames_up = 0
            #     starting_y_up = None   
        else:
            curr_frames_down = 0
            starting_y = None
            curr_frames_up = 0
            starting_y_up = None
        cv2.imshow('Hand Gesture Detection', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
