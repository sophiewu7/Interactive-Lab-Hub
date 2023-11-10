import cv2

# Initialize the camera
cap = cv2.VideoCapture(0)  # 0 is the index of the camera, change if you have multiple cameras

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
else:
    try:
        # Capture frames continuously
        while True:
            ret, frame = cap.read()
            
            if ret:
                # Display the captured image
                cv2.imshow('Tarot Reader Camera', frame)
                
                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                print("Error: Could not read frame.")
                
    finally:
        # Release the camera and close all OpenCV windows
        cap.release()
        cv2.destroyAllWindows()