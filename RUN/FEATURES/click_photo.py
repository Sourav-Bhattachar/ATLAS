import cv2

def take_photo(filename='photo.png', camera_index=0):
    # Initialize the camera
    camera = cv2.VideoCapture(camera_index)
    
    # Check if camera opened successfully
    if not camera.isOpened():
        print("Error: Could not open camera")
        return False
    
    # Capture a single frame
    ret, frame = camera.read()
    
    if ret:
        # Display the captured image
        cv2.imshow('Captured Photo', frame)
        print("Image preview - Press any key to save and close the window")
        
        # Wait for key press and then close window
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        # Save the captured image
        cv2.imwrite(filename, frame)
        print(f"Photo saved as {filename}")
    else:
        print("Error: Failed to capture image")
    
    # Release the camera
    camera.release()
    return ret


