import os
import cv2
import face_recognition as fr
import numpy as np
from time import sleep
from PIL import Image
import asyncio as asy
import alert_owner as ao


def change_resolution(cap, res):
    print(res)
    if res == 1080:
        cap.set(3,1920)
        cap.set(4, 1080)
    elif res == 720:
        cap.set(3,1280)
        cap.set(4, 720)
    elif res == 480:
        cap.set(3, 640)
        cap.set(4, 480)
    elif res == 140:
        cap.set(3, 350)
        cap.set(4, 140)
    return cap

def rescale_frame( frame, percent ):
    width = int(frame.shape[1] * percent/100)
    height = int(frame.shape[0] * percent/100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

def get_video_feed(res = 1080):
    faces = get_known_faces()
    known_face_encodings = list(faces.values())
    known_face_names = list(faces.keys())
    face_names = []
    face_locations = []
    cap = cv2.VideoCapture('../feed/vid01.mp4')
    
    # cap = cv2.VideoCapture('../feed/02.JPG')
    process_this_frame = True
    #for changing feed to live cam
    # cap = cv2.VideoCapture('0')

    
    if(cap.isOpened() == False):
        print("Error opening")
    # cap = change_resolution(cap, res)
    count = 0
    last_faces = []
    while cap.isOpened():
        #Capturing frame by frame
        # cap.resizeWindow()
        ret, frame = cap.read()
        
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #resize
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        #convert from bgr to rbg
        rgb_small_frame = small_frame[:, :, ::-1]
        #only process every 3 frames
        # while process_this_frame:
        #if last face is same as current, dont run
        if count > 2:
            face_locations = fr.face_locations(rgb_small_frame)
            face_encodings = fr.face_encodings(rgb_small_frame, face_locations)
            
            face_names = []
            #if there are new faces
            # if False in fr.compare_faces(face_encodings, last_faces):
            last_faces = face_encodings[:]
            for face_encoding in face_encodings:
                #check if face matches the last face:

                # See if the face is a match for the known face(s)
                matches = fr.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                
                # # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                # face_distances = fr.face_distance(known_face_encodings, face_encoding)
                # best_match_index = np.argmin(face_distances)
                # if matches[best_match_index]:
                
                #     name = known_face_names[best_match_index]
                face_names.append(name)
            count = 0
        # process_this_frame = not process_this_frame
        count +=1
            # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        # cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        # cap.release()

        #displays the frame
        if ret == True:
            frame = rescale_frame(frame, 50)

            cv2.imshow('Video',frame)
            # frame2 = rescale_frame(frame, 150)


            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else: break
    if "unknown" in face_name:
        ao.sendMail()
    cap.release()
    cv2.destroyAllWindows()

    

def get_known_faces():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(BASE_DIR, "../faces")
    known = {}
    for dirpath, dirname, fileName in os.walk(image_dir):
        for file in fileName:
            if file.endswith("png") or file.endswith("jpg") or file.endswith("JPG"):
                path = os.path.join(dirpath, file)
                label = os.path.basename(dirpath).replace(" ", "-").lower()
                
                face = fr.load_image_file(path)
                encoding = fr.face_encodings(face)[0]
                known[label] = encoding
    return known

# print(get_known_faces())
# get_video_feed(1080)
# cv2.destroyAllWindows()


get_video_feed()
