# import the necessary packages
import face_recognition

import pickle

import numpy
import cv2
import os
import time

import fr_utils as utils




def predict_name_from_embedding(embedding,data,tolerance=0.6):

    # given the face image embedding and the data of all the embeddings,
    # predicts the name of the person (class label)


    matches = face_recognition.compare_faces(data["known_embeddings"],embedding,
                                    
                                        tolerance)

    print(matches)
    name = "unknown"


    # check to see if we have found a match
    if True in matches:

        # find the indexes of all matched faces then initialize a
        # dictionary to count the total number of times each face
        # was matched

        matchedIdxs = [i for (i, b) in enumerate(matches) if b]
        counts = {}


        # loop over the matched indexes and maintain a count for
        # each recognized face face
        for i in matchedIdxs:

            name = data["known_names"][i]
            counts[name] = counts.get(name, 0) + 1


        # determine the recognized face with the largest number of
        # votes (note: in the event of an unlikely tie Python will
        # select first entry in the dictionary)

        name = max(counts, key=counts.get)

        



    return name



def who_are_these_util(rgb,data,model='hog',tolerance=0.6):



    

    
    # detect the (x, y)-coordinates of the bounding boxes corresponding
    # to each face in the input image, then compute the facial embeddings
    # for each face

    print("[INFO] recognizing faces...")
    boxes = face_recognition.face_locations(rgb,model=model)

    embeddings = face_recognition.face_encodings(rgb, boxes)

    print(len(embeddings))
    
    # initialize the list of names for each face detected
    names = []


    for embedding in embeddings:

        name = predict_name_from_embedding(embedding,data,tolerance=0.6)

        names.append(name)

    print(names)

    return zip(names,boxes)
    #return (boxes,names)


def draw_bboxes_around_faces(img,name_to_bboxes_mapping):

    # draws bboxes around faces on img which is in bgr format

	
    # loop over the recognized faces
    for (name,(top, right, bottom, left)) in name_to_bboxes_mapping:

        img = utils.draw_bbox(img,name,top,bottom,left,right)

    
    return img




def who_are_these(img,pkl_file_path,model='hog',tolerance=0.6):


    # load the known faces and embeddings
    print("[INFO] loading encodings...")
    data = pickle.loads(open(pkl_file_path, "rb").read())
    
    # loading the image as rgb

    #img = cv2.imread(impath)

    

    #image = np.array(image, dtype=np.uint8)
    

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    names_to_bboxes_mapping = who_are_these_util(rgb,data,model=model,
                                                
                                            tolerance=0.6)

    


    img = draw_bboxes_around_faces(img,names_to_bboxes_mapping)

    return img


def recognise_faces_from_video(vid_in,vid_out,pkl_file_path,model='hog'):

    # processes a video frame by frame,predicts faces for each frame
    # and writes the entire processed video to an output video file



    # Create a VideoCapture object
    cap = cv2.VideoCapture(vid_in)

    time.sleep(2.0)
    
    # Check if camera opened successfully
    if (cap.isOpened() == False): 
        print("Error opening video stream or file")
    
    # Default resolutions of the frame are obtained.The default resolutions are system dependent.
    # We convert the resolutions from float to integer.
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    
    # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
    out = cv2.VideoWriter(vid_out,cv2.VideoWriter_fourcc('X','V','I','D'), 10, (frame_width,frame_height))
    
    # frame_id gives us the num of frames processed uptill now
    frame_id = 0

    start = time.time()

    while(True):

        ret, frame = cap.read()


        frame_id = frame_id + 1 
        print(frame_id)


        if ret == True: 
            

            
            frame = who_are_these(frame,pkl_file_path,model=model,tolerance=0.6)
            
            end = time.time()

            secs = end - start

            # calculating fps as num of frames processed / seconds passed
            fps = frame_id / secs

            fps_text = 'FPS = ' + str(fps)

            print(fps_text)
            
            # put fps at the bottom of image 
            cv2.putText(frame, fps_text, (frame_width-450, frame_height-10), cv2.FONT_HERSHEY_SIMPLEX,0.75, (0, 255, 0), 2)
            
            
            # Write the frame into the file 'output.avi'
            out.write(frame)
        

            
            target_path = '../imgs/frames1/'
            cv2.imwrite(os.path.join(target_path , 'frame-'+str(frame_id)+'.jpg'), frame)

        
            # Press Q on keyboard to stop recording
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break
        
        # Break the loop
        else:
            break 
    
    # When everything done, release the video capture and video write objects
    cap.release()
    out.release()
    




if __name__ == "__main__":

    #impath = '../imgs/predict/friends'
    vid_in = '../imgs/predict/friends.mp4'
    vid_out = '../imgs/predict/friends_output0.avi'

    pkl_file_path = 'embeddings.pickle'

    '''
    img = who_are_these(impath,pkl_file_path,model='hog',tolerance=0.6)

    # show the output image
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    '''

    recognise_faces_from_video(vid_in,vid_out,pkl_file_path)
