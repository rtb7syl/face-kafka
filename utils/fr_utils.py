# import the necessary packages
import face_recognition

import pickle

import numpy as np
import cv2
import os





def images_paths(path_to_dir):

    #returns list of path to the images in a dir

    impaths = []

    for path in os.listdir(path_to_dir):

        path_to_subdir = os.path.join(path_to_dir,path)

        for fname in os.listdir(path_to_subdir):

            path_to_img = os.path.join(path_to_subdir,fname)

            print(path_to_img)

            impaths.append(path_to_img)



    return impaths





def extract_name(impath):

    # extracts the class label and img fname from the path to the img

    fname = impath.split('/')[-1]

    class_label = fname.split('_')[0]

    return (class_label,fname)





def load_image(img_path):

    # opens an image in RGB format

    image = cv2.imread(img_path)

    

    #image = np.array(image, dtype=np.uint8)
    

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return rgb



def embed(img,upsample=1,model='hog'):
    
    # returns 128 dims encodings list of all faces found in a RGB image




    # return list of tuples of bboxes in a (top,right,bottom,left) format

    boxes = face_recognition.face_locations(img, 
                                            
                            number_of_times_to_upsample=upsample,
                                            
                            model=model
                            
                            )




    # returns a list of 128-dimensional face embeddings,
    # (one for each face in the image)

    embeddings = face_recognition.face_encodings(img, boxes)[0]

    print(embeddings)

    return embeddings


def serialize_embeddings(data,pkl_file_path):

    # serializes a data dict consisting of face embeddings and names

    f = open(pkl_file_path, "wb+")
    f.write(pickle.dumps(data))
    f.close()


def draw_bbox(bgr,class_label,top,bottom,left,right):

    # draw the predicted face name on the image
    cv2.rectangle(bgr, (left, top), (right, bottom),(0, 255, 0), 2)

    y = top - 15 if top - 15 > 15 else top + 15
    
    cv2.putText(bgr, class_label, (left, y), cv2.FONT_HERSHEY_SIMPLEX,0.75, (0, 255, 0), 2)

    return bgr
    