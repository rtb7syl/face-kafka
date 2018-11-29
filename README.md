# face-kafka

## Project Title
This project is about detection and recognition of faces in real time with Apache Kafka message passing architecture.
Ideally,there can be multiple remote video streams captured from multiple IP cams ,but since this is a prototype version, we're using a single video source (local or remote), a single Kafka broker , producer and consumer.
But, this prototype application can be scaled up for multiple video sources with some changes.

Therefore a producer captures the data frame by frame from the video source, serializes it to a bytestring, and publishes it to a topic in the Kafka broker. 
The consumer then subscribes to the topic , gets the data (the bytestring of each frame) , deserializes it into a numpy array,and pushes it into the face recognition pipeline.
The frame that gets out of the face recognition pipeline, is basically the original frame with bboxes around the faces detected, with their corresponding names if the algorithm could reognize the face , else it's labelled as "Unknown".

A Flask Webserver,then renders these "transformed" frames on localhost:5000.

