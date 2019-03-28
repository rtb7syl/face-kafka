from flask import Flask, Response
from kafka import KafkaConsumer

import numpy as np
import cv2

from face_rec.recognize_faces import who_are_these
from utils.utils import *


#Continuously listen to the connection and print messages as recieved
app = Flask(__name__)




def kafkastream(consumer,pkl_file,imwrite_path,model,tolerance):

    # takes in serialized raw frames from consumer ,deserializes it, 
    # and pushes it into the face detection and recognition subroutine

    # pkl_file is the pickled file of known embeddings
    # model is the face detection model which is either 'hog' or 'cnn'
    # tolerance is the minimum thershold distance for recognising faces

    # it then serializes the output frame into a bytestring and yields them on the fly



    for msg in consumer:

        #print(msg.value)

        # deserializing bytestring to a numpy array
        img = deserialize(msg.value)

        #output frame from face-recognition subroutine
        img = who_are_these(img,pkl_file,imwrite_path,model=model,tolerance=tolerance)
        print('xx')

        '''
        #serializing frame to bytestring 
        frame_bytes = serialize_frame(img)







        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + frame_bytes + b'\r\n\r\n')

        '''


if __name__ == '__main__':

    #connect to Kafka server and pass the topic we want to consume
    
    topic_name = "test"
    consumer = KafkaConsumer(topic_name, auto_offset_reset='earliest',bootstrap_servers=['192.168.1.2:9569'], api_version=(0, 10), consumer_timeout_ms=1000)
    
    
    pkl_file = 'embeddings.pickle'

    model = 'hog'

    tolerance = 0.6

    imwrite_path = 'recognized_faces'

    kafkastream(consumer,pkl_file,imwrite_path,model,tolerance)
    

    '''
    @app.route('/')

    def index():
        # return a multipart response
        return Response(kafkastream(consumer,pkl_file,imwrite_path,model,tolerance),
                        mimetype='multipart/x-mixed-replace; boundary=frame')


    app.run(host='127.0.0.1', debug=True)
    '''