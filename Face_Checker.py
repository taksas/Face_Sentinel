import asyncio
import io
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, QualityForRecognition
import cv2
from azure.storage.blob import BlobClient

def face_check(VISION_KEY, VISION_ENDPOINT, COMPARE_ID):

    
    # Open Camera
    cap = cv2.VideoCapture(0)
    # Capture Pic
    ret, frame = cap.read()
    # Save Pic
    cv2.imwrite("image.jpg", frame)
    # Close Camera
    cap.release()

    

    target_dir = null

    # This key will serve all examples in this document.
    KEY = VISION_KEY

    # This endpoint will be used in all examples in this quickstart.
    ENDPOINT = VISION_ENDPOINT


    # Used in the Person Group Operations and Delete Person Group examples.
    # You can call list_person_groups to print a list of preexisting PersonGroups.
    # SOURCE_PERSON_GROUP_ID should be all lowercase and alphanumeric. For example, 'mygroupname' (dashes are OK).
    PERSON_GROUP_ID = str(uuid.uuid4()) # assign a random ID (or name it anything)

    # Create an authenticated FaceClient.
    face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))


    '''
    Identify a face against a defined PersonGroup
    '''
    # Group image for testing against
    test_image = target_dir

    print('Pausing for 10 seconds to avoid triggering rate limit on free account...')
    time.sleep (10)

    # Detect faces
    face_ids = []
    # We use detection model 3 to get better performance, recognition model 4 to support quality for recognition attribute.
    faces = face_client.face.detect_with_url(test_image, detection_model='detection_03', recognition_model='recognition_04', return_face_attributes=['qualityForRecognition'])
    for face in faces:
        # Only take the face if it is of sufficient quality.
        if face.face_attributes.quality_for_recognition == QualityForRecognition.high or face.face_attributes.quality_for_recognition == QualityForRecognition.medium:
            face_ids.append(face.face_id)

    # Identify faces
    results = face_client.face.identify(face_ids, PERSON_GROUP_ID)
    print('Identifying faces in image')
    if not results:
        print('No person identified in the person group')
    for identifiedFace in results:
        if len(identifiedFace.candidates) > 0:
            print('Person is identified for face ID {} in image, with a confidence of {}.'.format(identifiedFace.face_id, identifiedFace.candidates[0].confidence)) # Get topmost confidence score

            # Verify faces
            verify_result = face_client.face.verify_face_to_person(identifiedFace.face_id, identifiedFace.candidates[0].person_id, PERSON_GROUP_ID)
            print('verification result: {}. confidence: {}'.format(verify_result.is_identical, verify_result.confidence))
            if(verify_result.is_identical == COMPARE_ID) : return 0
        else:
            print('No person identified for face ID {} in image.'.format(identifiedFace.face_id))
    return 1
