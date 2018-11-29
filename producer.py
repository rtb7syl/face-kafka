
import time
import sys

from kafka import KafkaProducer
import cv2

from utils.utils import *

def publish_message(producer_instance, topic_name, key, value):
    try:
        key_bytes = bytes(key, encoding='utf-8')
        #value_bytes = bytes(value, encoding='utf-8')
        producer_instance.send(topic_name, key=key_bytes, value=value)
        producer_instance.flush()
        print('Message published successfully.')
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))


def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10))
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
    
        return _producer


def video_emitter(source,producer_instance, topic_name, key):
    # Open the video
    video = cv2.VideoCapture(source)

    # Check if camera opened successfully
    if (video.isOpened() == False): 
    
        print("Error opening video stream or file")

    else:
        print(' emitting.....')



    # read the file
    while (video.isOpened):
        # read the image in each frame
        success, frame = video.read()


        
        # check if the file has read to the end
        if not success:
            break


        # Convert the frame to bytes and send to kafka
        
        frame_bytes = serialize_frame(frame)

        publish_message(producer_instance, topic_name, key, frame_bytes)




        # To reduce CPU usage create sleep time of 0.2sec  
        time.sleep(0.2)


    # clear the capture
    video.release()
    print('done emitting')

    if kafka_producer is not None:
        kafka_producer.close()


if __name__ == "__main__":

    #source = 'http://192.168.2.8:8080/video'
    #source = '../imgs/predict/friends.mp4'

    source_arg_param_0 = '--source'
    source_arg_param_1 = '-s'
    
    if (sys.argv[1] == source_arg_param_0) or (sys.argv[1] == source_arg_param_1):

        source = sys.argv[2]

    else:

        raise RuntimeError('Illegal comand line args')

    kafka_producer = connect_kafka_producer()

    topic_name = "raw_frames"

    key = "raw"

    

    video_emitter(source,kafka_producer, topic_name, key)