import os
import cv2
import numpy as np
from time import time

import grpc
from src.gRPCs import detection_pb2
from src.gRPCs import detection_pb2_grpc

def run():
    channelDetection = grpc.insecure_channel('192.168.49.2:30005')
    stubDetection = detection_pb2_grpc.DetectionServiceStub(channelDetection)
    
    path = "InputImages"
    dirs = os.listdir(path)
    
    for imageName in dirs:

        inputImage = cv2.imread(os.path.join(path, imageName)).astype(np.uint8)
        
        # Encode image
        byteImage = inputImage.tobytes()
        
        # Request detection
        s = time()
        detectionsResponse = stubDetection.detectFace(detection_pb2.InputImage(
            byteImage=byteImage,
            width=inputImage.shape[0],
            height=inputImage.shape[1]
        ))
        print("[Client] Detect face time: ", round(time()- s, 4))

        arrayBoxes = np.frombuffer(detectionsResponse.boundingBoxes, dtype=np.int64).reshape(detectionsResponse.numFaces, 4)
        arrayLandmarks = np.frombuffer(detectionsResponse.landmarks, dtype=np.int64).reshape(detectionsResponse.numFaces, 5, 2)

run()