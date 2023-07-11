import face_recognition
import matplotlib.pyplot as plt
import glob
import cv2

def face_check(YOUR_PICS_DIR, DEBUGGING):

    camera_image = "image.jpg"
    # Open Camera
    cap = cv2.VideoCapture(0)
    # Capture Pic
    ret, frame = cap.read()
    # Save Pic
    cv2.imwrite(camera_image, frame)
    # Close Camera
    cap.release()


    path_list = glob.glob(YOUR_PICS_DIR + '\*')

    # Load Known Faces
    known_face_imgs = []
    for path in path_list:
        img = face_recognition.load_image_file(path)
        known_face_imgs.append(img)
    if(DEBUGGING): print("Loaded Known Images:", path_list)

    # Load Captured Checking Face
    face_img_to_check = face_recognition.load_image_file(camera_image)

    # face detection
    known_face_locs = []
    for img in known_face_imgs:
        loc = face_recognition.face_locations(img, model="hog")
        if len(loc) != 1:
            if(DEBUGGING): print("Known Face Analyzation Error")
            return -1
        known_face_locs.append(loc)

    face_loc_to_check = face_recognition.face_locations(face_img_to_check, model="hog")
    if len(face_loc_to_check) != 1:
        if(DEBUGGING): print("Checking Face Analyzation Error")
        return -1



    # face recognition
    known_face_encodings = []
    for img, loc in zip(known_face_imgs, known_face_locs):
        (encoding,) = face_recognition.face_encodings(img, loc)
        known_face_encodings.append(encoding)

    (face_encoding_to_check,) = face_recognition.face_encodings(
        face_img_to_check, face_loc_to_check
    )


    matches = face_recognition.compare_faces(known_face_encodings, face_encoding_to_check) # check whether matching
    print(matches)  # [True, False, False]?

    for x in matches:
        if(x == True) : return 0
    return 1