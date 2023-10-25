# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 12:12:05 2023

@author: Lepi
"""

import cv2
import numpy as np

# Initialize the camera
cap = cv2.VideoCapture(0)  # Use the default camera (you can change this if needed)

# Create a background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Apply background subtraction to the frame
    fgmask = fgbg.apply(frame)

    # Apply morphological operations to clean up the mask
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    # Find contours in the mask
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > 0.1 * frame.shape[0] * frame.shape[1]:
            # If the contour area is larger than 10% of the screen area, trigger an alert
            cv2.drawContours(frame, [contour], -1, (0, 0, 255), 2)  # Draw a red rectangle around the object

    # Display the result
    cv2.imshow("Large Object Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()
