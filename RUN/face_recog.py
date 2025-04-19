import cv2


def authenticate_face(root, container, success_callback):
    """Runs face authentication while showing a live camera feed."""
    print('recognising....')
    recognizer = cv2.face.LBPHFaceRecognizer_create()   #pip uninstall opencv-python opencv-contrib-python
                                                        # pip install opencv-contrib-python
                                                            
    # recognizer = cv2.face.LBPHFaceRecognizer_create() if hasattr(cv2, 'face') else cv2.ml.LBPHFaceRecognizer_create()

    recognizer.read(r'ATLAS_UI_VIDEO_AUDIO\auth\trainer\trainer.yml')

    cascadePath = r'ATLAS_UI_VIDEO_AUDIO\auth\haarcascade_frontalface_default.xml'
    faceCascade = cv2.CascadeClassifier(cascadePath)

    font = cv2.FONT_HERSHEY_SIMPLEX
    names = ['', 'Sourav']  

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)
    cam.set(4, 480)

    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    success_flag = False

    while True:
        ret, img = cam.read()
        if not ret:
            continue

        converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            converted_image,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  

            id, accuracy = recognizer.predict(converted_image[y:y + h, x:x + w])

            if accuracy < 100:
                name = names[id]
                confidence = "  {0}%".format(round(100 - accuracy))
                success_flag = True
            else:
                name = "Unknown"
                confidence = "  {0}%".format(round(100 - accuracy))

            cv2.putText(img, str(name), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        cv2.imshow("Face Authentication", img)

        if cv2.waitKey(10) & 0xFF == 27:
            break
        if success_flag:
            break

    cam.release()
    cv2.destroyAllWindows()

    if success_flag:
        print("Face authentication successful!")
        root.after(50, lambda: success_callback(root, container))
