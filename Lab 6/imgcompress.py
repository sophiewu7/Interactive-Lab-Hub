import cv2

# Initialize the camera
cap = cv2.VideoCapture(0)  # 0 is the index of the camera, change if you have multiple cameras

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
else:
    # Capture frames continuously
    while True:
        ret, frame = cap.read()
        
        if ret:
            # Display the captured image
            quality = 50
            cv2.imshow('Tarot Reader Camera', frame)
                
        cv2.imwrite('tarotimg/compressresult.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
                