import cv2
import numpy as np

def main():
    cap = cv2.VideoCapture(1)

    # Define the lower and upper bounds for the blue color in HSV
    lower_blue = np.array([100, 150, 50])  # Lower bound of blue color
    upper_blue = np.array([140, 255, 255])  # Upper bound of blue color

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        # Convert the frame to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Create a mask for blue color
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Optional: perform some morphological operations to clean up the mask
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw bounding boxes around the detected blue objects
        for contour in contours:
            if cv2.contourArea(contour) > 500:  # Filter out small contours
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Blue Color Tracking', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
