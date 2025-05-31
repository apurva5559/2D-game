import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Key, Controller
import pyautogui
import speech_recognition as sr

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Function to recognize speech
def recognize_speech():
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)  # Convert speech to text
        print("Command:", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return None
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return None

# Function to click the start button
def click_start_button():
    x, y = 1466, 900  # Coordinates for the start button
    pyautogui.click(x, y)

# Initialize video capture
cap = cv2.VideoCapture(0)
cap.set(3, 720)  # Set width
cap.set(4, 420)  # Set height

# Initialize hand detector
detector = HandDetector(detectionCon=0.7, maxHands=1)

# Initialize keyboard controller
keyboard = Controller()

# Main loop
while True:
    _, img = cap.read()
    hands, img = detector.findHands(img)

    # Gesture handling
    if hands:
        fingers = detector.fingersUp(hands[0])
        if fingers == [0, 0, 0, 0, 0]:  # Gesture for applying brake
            keyboard.press(Key.left)
            keyboard.release(Key.right)
        elif fingers == [1, 1, 1, 1, 1]:  # Gesture for applying gas
            keyboard.press(Key.right)
            keyboard.release(Key.left)
        elif fingers == [1, 1, 0, 0, 1]:  # Gesture for clicking the pause symbol
            pyautogui.click(1835, 361)  # Coordinates for pause symbol
        elif fingers == [0, 1, 0, 0, 0]:  # Gesture for restart
            pyautogui.click(1466, 773)  # Coordinates for restart button
        elif fingers == [0, 1, 1, 0, 0]:  # Gesture for resuming
            pyautogui.click(1466, 810)  # Coordinates for resume button
        elif fingers == [1, 0, 0, 0, 0]:  # Gesture for exit
            pyautogui.click(1466, 850)  # Coordinates for exit button
    else:
        keyboard.release(Key.left)
        keyboard.release(Key.right)

    # Voice command handling
    command = recognize_speech()
    if command == "gas":
        keyboard.press(Key.right)
        keyboard.release(Key.left)
    elif command == "brake":
        keyboard.press(Key.left)
        keyboard.release(Key.right)
    elif command == "pause":
        pyautogui.click(1835, 361)  # Coordinates for pause symbol
    elif command == "restart":
        pyautogui.click(1466, 773)  # Coordinates for restart button
    elif command == "resume":
        pyautogui.click(1466, 810)  # Coordinates for resume button
    elif command == "exit":
        pyautogui.click(1466, 850)  # Coordinates for exit button

    cv2.imshow("problem solving", img)
    if cv2.waitKey(1) == ord("q"):  # Press 'q' to quit
        break

cv2.destroyAllWindows()
