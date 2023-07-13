import face_recognition
import matplotlib.pyplot as plt
import glob
import cv2
import datetime



def camera_capture(capture_pics_dir):
    camera_image = capture_pics_dir + "\\" + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ".jpg"
    # Open Camera
    cap = cv2.VideoCapture(0)
    # Capture Pic
    ret, frame = cap.read()
    # Save Pic
    cv2.imwrite(camera_image, frame)
    # Close Camera
    cap.release()
    return camera_image



def authorization(your_pics_dir, capture_pics_dir, rigidity, threshold, debugging):

    

    # Load Known Faces
    path_list = glob.glob(your_pics_dir + '\*')
    known_face_imgs = []
    for path in path_list:
        img = face_recognition.load_image_file(path)
        known_face_imgs.append(img)
    if(debugging): print("Loaded Known Images:", path_list)

    # Load Captured Target Face
    target_image = camera_capture(capture_pics_dir)
    face_img_to_check = face_recognition.load_image_file(target_image)

    # face detection
    known_face_locs = []
    for img in known_face_imgs:
        loc = face_recognition.face_locations(img, model="hog")
        if len(loc) != 1:
            if(debugging): print("Known Face Analyzation Error")
            return -1, -1, -1, -1, -1
        known_face_locs.append(loc)

    face_loc_to_check = face_recognition.face_locations(face_img_to_check, model="hog")
    if len(face_loc_to_check) != 1:
        if(debugging): print("Target Face Analyzation Error")
        return -2, -1, -1, -1, -1


    # face recognition
    known_face_encodings = []
    for img, loc in zip(known_face_imgs, known_face_locs):
        (encoding,) = face_recognition.face_encodings(img, loc)
        known_face_encodings.append(encoding)

    (face_encoding_to_check,) = face_recognition.face_encodings(
        face_img_to_check, face_loc_to_check
    )

    dists = face_recognition.face_distance(known_face_encodings, face_encoding_to_check)  # check similarity level
    if(debugging): print(len(dists), "\n", dists)  # 3 [True, False, False]?


    true_count = 0
    ave_threshold = 0
    min_threshold = 1
    max_threshold = 0
    
    for x in dists:
        if(x < threshold) : true_count += 1
        ave_threshold += x
        if(x < min_threshold): min_threshold = x
        if(x > max_threshold): max_threshold = x

    if(debugging): print("rigidity:",rigidity,"%\n", "threshold:", threshold)
    last_rigidity = true_count / len(dists)
    if( last_rigidity >= rigidity*0.01 ): return 0, last_rigidity*100, ave_threshold/len(dists), min_threshold, max_threshold
    else: return 1, last_rigidity*100, ave_threshold/len(dists), min_threshold, max_threshold