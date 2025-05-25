import cv2

def take_photo(filename='photo.png', camera_index=0):
    camera = cv2.VideoCapture(camera_index)

    if not camera.isOpened():
        print("Error: Could not open camera")
        return False
    ret, frame = camera.read()

    if ret:
        cv2.imshow('Captured Photo', frame)
        print("Image preview - Press any key to save and close the window")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite(filename, frame)
        print(f"Photo saved as {filename}")
    else:
        print("Error: Failed to capture image")
    camera.release()
    return ret
