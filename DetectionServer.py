import time
import grpc
import torch
import numpy as np
from time import time
import face_detection
from loguru import logger
from concurrent import futures

from src.gRPCs import detection_pb2
from src.gRPCs import detection_pb2_grpc

class DetectionServer(detection_pb2_grpc.DetectionServiceServicer):
    def __init__(self) -> None:
        super().__init__()
        self.initLogger()
        
        self.initVariables()
        self.initFaceDetector()
        
    def initLogger(self):
        logger.add("logs/file_{time}.log")
        logger.level("INITIALIZE", no=38, color="<blue>")
        logger.level("INFERENCE", no=38, color="<green>")
        
    def initVariables(self):
        self.requestCounter, self.faceCounter = 0, 0
        logger.log("INITIALIZE", "Variables initialized!")
        
    def initFaceDetector(self):
        self.faceDetector = face_detection.build_detector(
            "RetinaNetMobileNetV1",
            max_resolution=720,
            device=torch.device("cpu"),
            confidence_threshold=0.95
            )
        logger.log("INITIALIZE", "Face detector initialized!")
    
    def updateVariables(self, faceNumber):
        self.requestCounter += 1
        self.faceCounter += faceNumber
    
    def detectFace(self, request, context):
        sStart = time()
        arrayImage = np.frombuffer(request.byteImage, dtype=np.uint8).reshape(request.width, request.height, -1)
        logger.log("INFERENCE", "Input image encoded in %s seconds!" % round(time()- sStart, 4))
        
        sDetect = time()
        with torch.no_grad():
            boundingBoxes, landmarks = self.faceDetector.batched_detect_with_landmarks(arrayImage[:, :, ::-1][np.newaxis, ...])
        
        logger.log("INFERENCE", "Input image detected in %s seconds!" % round(time()- sDetect, 4))
        
        
        self.updateVariables(len(boundingBoxes[0]))
        logger.log("INFERENCE", "[Request: %s] - [Detected Faces: %s]" % (self.requestCounter, self.faceCounter))
                
        return detection_pb2.DetectionResults(
            boundingBoxes=np.array(boundingBoxes[0][:, :4], dtype=np.int64).tobytes(),
            landmarks=np.array(landmarks[0], dtype=np.int64).tobytes(),
            numFaces=len(boundingBoxes[0])
        )
      	  
def server():
    options = [
        ('grpc.max_send_message_length', 100 * 1024 * 1024),
        ('grpc.max_receive_message_length', 100 * 1024 * 1024)
    ]
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3), options=options)
    detection_pb2_grpc.add_DetectionServiceServicer_to_server(DetectionServer(), server)
    server.add_insecure_port('[::]:50051')
    logger.log("INITIALIZE", "Detection server started!")
    server.start()
    server.wait_for_termination()
server()