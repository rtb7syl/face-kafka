from flask import Flask, Response
from kafka import KafkaConsumer

import numpy as np
import cv2

import recognize_faces
import utils


#Continuously listen to the connection and print messages as recieved
app = Flask(__name__)




def kafkastream(consumer,pkl_file,model,tolerance):

    # takes in serialized raw frames from consumer ,deserializes it, 
    # and pushes it into the face detection and recognition subroutine

    # pkl_file is the pickled file of known embeddings
    # model is the face detection model which is either 'hog' or 'cnn'
    # tolerance is the minimum thershold distance for recognising faces

    # it then serializes the output frame into a bytestring and yields them on the fly



    for msg in consumer:

        #print(msg.value)

        # deserializing bytestring to a numpy array
        img = utils.deserialize(msg.value)

        #output frame from face-recognition subroutine
        img = recognize_faces.who_are_these(img,pkl_file,model=model,tolerance=tolerance)

        #serializing frame to bytestring 
        frame_bytes = utils.serialize_frame(img)







        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + frame_bytes + b'\r\n\r\n')




if __name__ == '__main__':

    #connect to Kafka server and pass the topic we want to consume
    
    topic_name = "raw_frames"
    consumer = KafkaConsumer(topic_name, auto_offset_reset='earliest',bootstrap_servers=['localhost:9092'], api_version=(0, 10), consumer_timeout_ms=1000)
    
    
    pkl_file = 'embeddings.pickle'

    model = 'hog'

    tolerance = 0.6
    


    @app.route('/')

    def index():
        # return a multipart response
        return Response(kafkastream(consumer,pkl_file,model,tolerance),
                        mimetype='multipart/x-mixed-replace; boundary=frame')


    app.run(host='127.0.0.1', debug=True)
