import cv2
import os
import numpy as np
from socket import socket
from ServerManager import ServerManager
from ControlServerManager import ControlServerManager
from Detector import Detector
from datetime import datetime
from Helper import Helper     
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

class Handler:
    def __init__(self, manager: ServerManager):
        self.serverManager = manager
        self.detector = Detector(
            "model/yolov3.cfg",
            "model/yolov3.weights"
        )
        self.controlServerIPAddress, self.controlServerPort = Helper.getContorlServerIPandPortFromConfig("config.json")
        
    def handleServer(self, **kwargs):
        while self.serverManager.isRunning:
            if self.serverManager.acceptClient():
                self.serverManager.handleClient(self.handleClient, kwargs)


    def handleClient(self, socket: socket, address: tuple, kwargs: dict = {}):
        
            imageView: QLabel = kwargs['imageView']
            image: np.ndarray = None
            bufferSize = (1024*1024)
            imageDataByteArray = bytearray()
            
            if socket.recv(bufferSize) == b"START":
                print("Package receive process start...")
                package = socket.recv(1024)
                dataSize = int(package.decode(encoding="ascii").split()[0])
                remainingDataSize = dataSize

                print(f"Package size: {dataSize}Byte")

                while remainingDataSize > 0:

                    imageBufferSize = min(bufferSize, remainingDataSize)
                    imgData = socket.recv(imageBufferSize)
                    if not imgData:
                        break
                    imageDataByteArray.extend(imgData)
                    remainingDataSize -= len(imgData)
                    print(f"Remaining package: {remainingDataSize}")


            if socket.recv(bufferSize) == b"END":

                print("Process finished...")

                imageName = Helper.getImageFileName()

                with open(imageName, "wb") as f:
                    f.write(imageDataByteArray)

                self.detector.readFrame(cv2.imread(imageName))

                (
                label,
                confidence,
                boxColor,
                startX,
                startY,
                endX,
                endY
                ) = self.detector.predict()
                
                image = Helper.BGR2RGB(self.detector.frame)

                if label == "person":
                    with ControlServerManager(self.controlServerIPAddress, self.controlServerPort) as controlServerManager:
                        print("person detected")
                        controlServerManager.connect()
                        controlServerManager.write('DETECTED')
                        controlServerManager.disconnect()

                    image = Helper.drawBoundingBox(
                        image, 
                        label, 
                        confidence, 
                        boxColor,
                        startX,
                        startY,
                        endX,
                        endY)
                    
                pixmap = Helper.pixmapFromNDArray(image).scaled(imageView.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    
                imageView.setPixmap(pixmap)