import numpy as np 
import cv2

def serialize_frame(img):

    #converts a numpy array to a byte-string


    ret, frame = cv2.imencode('.png', img)
    
    # Convert the frame to bytes 
    frame_bytes = frame.tobytes()

    return frame_bytes


def deserialize(byte_string):

    #convert a byte_string to a numpy array image frame

    nparr = np.fromstring(byte_string,np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    return img





