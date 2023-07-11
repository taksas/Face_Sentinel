import asyncio
import io
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, QualityForRecognition

def train_me(VISION_KEY, VISION_ENDPOINT, WORKING_DIR):
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
    Create the PersonGroup
    '''
    # Create empty Person Group. Person Group ID must be lower case, alphanumeric, and/or with '-', '_'.
    print('Person group:', PERSON_GROUP_ID)
    face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID, recognition_model='recognition_04')

    # Define me friend
    me = face_client.person_group_person.create(PERSON_GROUP_ID, name="Me")


    '''
    Detect faces and register them to each person
    '''
    # Find all jpeg images of friends in working directory (TBD pull from web instead)
    me_images = WORKING_DIR

    print(me_images)



    # Add to me person
    for image in me_images:
        # Check if the image is of sufficent quality for recognition.
        sufficientQuality = True
        detected_faces = face_client.face.detect_with_url(url=image, detection_model='detection_03', recognition_model='recognition_04', return_face_attributes=['qualityForRecognition'])
        for face in detected_faces:
            if face.face_attributes.quality_for_recognition != QualityForRecognition.high:
                sufficientQuality = False
                break
            face_client.person_group_person.add_face_from_url(PERSON_GROUP_ID, me.person_id, image)
            print("face {} added to person {}".format(face.face_id, me.person_id))

        if not sufficientQuality: continue


    '''
    Train PersonGroup
    '''
    # Train the person group
    print("pg resource is {}".format(PERSON_GROUP_ID))
    rawresponse = face_client.person_group.train(PERSON_GROUP_ID, raw= True)
    print(rawresponse)

    while (True):
        training_status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
        print("Training status: {}.".format(training_status.status))
        print()
        if (training_status.status is TrainingStatusType.succeeded):
            break
        elif (training_status.status is TrainingStatusType.failed):
            face_client.person_group.delete(person_group_id=PERSON_GROUP_ID)
            sys.exit('Training the person group has failed.')
        time.sleep(5)



    print("All Training Process was Finished!\n Your Face Group ID is:", PERSON_GROUP_ID, "\nAnd Your ID is:", me.person_id)
    

    if __name__ == '__main__':
        KEY = os.environ["VISION_KEY"]
        ENDPOINT = os.environ["VISION_ENDPOINT"]

        target = ["https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/Family1-Mom1.jpg", "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/Family1-Mom2.jpg"]
        
        train_me(KEY, ENDPOINT, target)