import json
import cv2
import datetime
import os
import numpy as np
from PyQt5.QtGui import QImage, QPixmap

class Helper:

    @staticmethod
    def getServerIPandPortFromConfig(cfg: str):
        with open(cfg, "r") as f:
            data = json.load(f)
            return data['server']['ipAddress'], int(data['server']['port'])
        

    @staticmethod
    def getContorlServerIPandPortFromConfig(cfg: str):
        with open(cfg, "r") as f:
            data = json.load(f)
            return data['controlServer']['ipAddress'], int(data['controlServer']['port'])
        
    @staticmethod
    def readLabelsFromFile(filePath: str) -> list[str]:
        with open(filePath, 'r') as file:
            content = file.readlines()
            content = [line.strip() for line in content]
            return content
        
    @staticmethod
    def drawBoundingBox(
        frame,
        label: str,
        confidence,
        color,
        startX,
        startY,
        endX,
        endY
    ) -> np.ndarray:
        
        label = "{}: {:.2f}%".format(label, confidence*100)
        
        cv2.rectangle(frame, (startX, startY), (endX, endY), color, 1)
        cv2.putText(frame, label, (startX, startY-10), cv2.FONT_HERSHEY_COMPLEX, 0.5, color, 2)

        return frame
    
    @staticmethod
    def pixmapFromNDArray(img: np.ndarray) -> QPixmap:
        h, w, ch = img.shape

        bytesPerLine = w * ch

        qImage = QImage(img, w, h, bytesPerLine, QImage.Format.Format_RGB888)

        return QPixmap.fromImage(qImage)
    
    @staticmethod
    def BGR2RGB(img: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    @staticmethod
    def getImageFileName():
        date: str = datetime.datetime.now().strftime("%Y-%m-%d__%H_%M_%S")
        
        return os.path.join("images", f"{date}.jpg")

