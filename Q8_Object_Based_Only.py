import cv2

def main():
    # Start video capture
    cap = cv2.VideoCapture(0)

    # Initialize the tracker
    tracker = cv2.TrackerCSRT_create()

    # Initial frame and ROI selection
    success, frame = cap.read()
    if not success:
        print("Failed to capture video")
        return

    # Use selectROI for the initial bounding box
    bbox = cv2.selectROI("Object Tracking", frame, showCrosshair=True, fromCenter=False)
    cv2.destroyAllWindows()
    ok = tracker.init(frame, bbox)

    # Tracking loop
    while True:
        # Read a new frame
        ok, frame = cap.read()
        if not ok:
            print("Failed to read from camera.")
            break

        # Update tracker and get the updated position
        track_ok, bbox = tracker.update(frame)

        if track_ok:
            # Tracking success: draw a rectangle around the tracked object
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (0, 255, 0), 2, 1)
        else:
            # Tracking failure detected, reinitialize tracker with the same ROI
            tracker = cv2.TrackerCSRT_create()  # Reinitialize the tracker
            ok = tracker.init(frame, bbox)
            cv2.putText(frame, "Reinitializing tracker...", (100, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2)

        # Display result
        cv2.imshow("Object Tracking", frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
