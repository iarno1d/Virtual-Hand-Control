import cv2, pyautogui, mediapipe as mp, numpy as np

# Function to check if thumb is close to specified fingertip
def is_clicking(thumb_tip, finger_tip, threshold = 60):
    distance = np.sqrt((thumb_tip[0] - finger_tip[0]) ** 2 + (thumb_tip[1] - finger_tip[1]) ** 2)
    return distance < threshold
'''
# Function to check if all fingers are closed or open
def is_all_closed(thumb_tip, fingers_tips, threshold=50):
    for finger_tip in fingers_tips:
        distance = np.sqrt((thumb_tip[0] - finger_tip[0]) ** 2 + (thumb_tip[1] - finger_tip[1]) ** 2)
        if distance < threshold:
            return True
    return False
'''
# Initialize MediaPipe Hand module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
# Open the camera
cap = cv2.VideoCapture(0)

# Define screen dimensions
screen_width, screen_height = pyautogui.size()      # try for a change
#screen_width = 3096
#screen_height = 2160

# Adjust PyAutoGUI settings for speed and accuracy
pyautogui.PAUSE = 0  # Adjust this value to control the speed of each PyAutoGUI call
pyautogui.FAILSAFE = False  # Disable failsafe to allow rapid mouse movements

while cap.isOpened():
    # Read a frame from the camera
    ret, frame = cap.read()
    
    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    results = hands.process(rgb_frame)

    # Check if hand landmarks are detected
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]  # Get the landmarks for the first (and only) detected hand

        # Get hand landmark coordinates
        normalized_landmarks = np.array([(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark])

        # Map hand coordinates to screen coordinates
        index_tip = (normalized_landmarks[8][0] * screen_width, normalized_landmarks[8][1] * screen_height)
        thumb_tip = (normalized_landmarks[4][0] * screen_width, normalized_landmarks[4][1] * screen_height)
        middle_tip = (normalized_landmarks[12][0] * screen_width, normalized_landmarks[12][1] * screen_height)
        ring_tip = (normalized_landmarks[16][0] * screen_width, normalized_landmarks[16][1] * screen_height)
        pinky_tip = (normalized_landmarks[20][0] * screen_width, normalized_landmarks[20][1] * screen_height)

        # Map hand coordinates to screen coordinates
        palm_center = (normalized_landmarks[9][0] * screen_width, normalized_landmarks[9][1] * screen_height)

        # Move mouse to palm center position (opposite direction horizontally)
        pyautogui.moveTo(screen_width - palm_center[0], palm_center[1])
        
        # Check for click gestures
        if is_clicking(index_tip, middle_tip):  # Index touches Middle
            pyautogui.doubleClick()  # Double click
            pyautogui.sleep(1)
        elif is_clicking(thumb_tip, middle_tip):    # Thumb touches Middle
            pyautogui.rightClick()  # Right click
            pyautogui.sleep(1)
        elif is_clicking(thumb_tip, index_tip): # Thumb touches Index
            pyautogui.click() # Left click
            pyautogui.sleep(1)
        elif is_clicking(thumb_tip, ring_tip):  # Thumb touches ring
            pyautogui.scroll(-40)  # Scroll up
        elif is_clicking(thumb_tip, pinky_tip):  # Thumb touches pinky
            pyautogui.scroll(40)  # Scroll down
    cv2.imshow('Nose Controlled Mouse with Blink Click', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
'''
        # Check for mouse drag and drop gestures
        if is_all_closed(thumb_tip, [index_tip, middle_tip, ring_tip, pinky_tip]):
            pyautogui.mouseDown()  # Mouse drag
        else:
            pyautogui.mouseUp()    # Mouse drop
'''    
# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()

