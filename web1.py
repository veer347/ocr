import streamlit as st
import cv2
import numpy as np
import utlis

st.title('OMG Grading')

cam = st.text_input("Do you want to use camera? (y/n): ") # if y, then True else False
if cam.lower() == "y":
    cam=True
    path=None
else:
    cam=False
    path = st.text_input("Enter the path of video file: ")  # If cam is false, enter the image path here

NO_q = st.number_input("Enter number of Questions to be graded. ", min_value=0, max_value=10, step=1)
NO_c = st.number_input("Enter number of Choices each question has? ", min_value=0, max_value=10, step=1)
ans_key = []
for i in range(1, NO_q+1):
    ans = st.number_input("Enter answer key for Q"+str(i)+": ", min_value=0, max_value=10, step=1)  # Example: For Q5 answer key will be 5
    ans_key.append(ans-1)

########################################################################
webCamFeed = cam
pathImage = path
heightImg = 700
widthImg = 700
questions = NO_q
choices = NO_c
ans = ans_key
########################################################################

count = 0
frame_placeholder = st.empty()
stop_button_pressed = st.button("Stop")
for i in range(10):  # Try indices from 0 to 9
    cap = cv2.VideoCapture(i)
    if not cap.isOpened():
        break
    cap.release()
    print(f"Camera index {i} is available.")

if st.button('Start Grading'):
    if cam:
        cap = cv2.VideoCapture(0)
        cap.set(10, 160)

    while (webCamFeed or path) and not stop_button_pressed:

        if webCamFeed:
            success, img = cap.read()
            if not success:
                st.error("Failed to capture frame from the camera.")
                break
        else:
            img = cv2.imread(pathImage)
            if img is None:
                st.error(f"Failed to load image from path: {pathImage}")
                break

        try:
            img = cv2.resize(img, (widthImg, heightImg))  # RESIZE IMAGE
            st.image(img, channels='BGR', caption="Resized Image")  # Display the resized image

            # ... (remaining code)
        except cv2.error as e:
            st.error(f"OpenCV Resize Error: {e}")
            break

        if stop_button_pressed:
            cv2.destroyAllWindows()
            break

# RELEASE RESOURCES IF STOP BUTTON PRESSED
if stop_button_pressed and cam:
    try:
        cap.release()
    except Exception as e:
        st.error(f"Error releasing camera: {e}")
