import cv2
import time

# Define the duration of the video
capture_duration = 10

# Set up the capture with the default camera
cap = cv2.VideoCapture(1)

# Define the codec and create VideoWriter object to write the video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 10.0, (640, 480))

start_time = time.time()
while(int(time.time() - start_time) < capture_duration):
    ret, frame = cap.read()
    if ret:
        # Write the frame into the file 'output.avi'
        out.write(frame)

        # You can also display the recording frame

        cv2.imshow('frame', frame)

        # Press 'q' to quit early
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything when the job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
