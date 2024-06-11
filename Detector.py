import cv2
import numpy as np
from Helper import Helper

class Detector():
    def __init__(self, cfgFile: str, weightsFile: str):

        self.labels: list[str] = Helper.readLabelsFromFile('labels.txt')
        self.boxColor = (0, 0, 255)
        self.cfgFile: str = cfgFile
        self.weightsFile: str = weightsFile

        self.setModel()

    def readFrame(self, frame: np.ndarray):
        self.frame = frame
        
        self.frameWidth = self.frame.shape[1]
        self.frameHeight = self.frame.shape[0]

        self.frameBlob = cv2.dnn.blobFromImage(self.frame, 1/255, (416,416), swapRB=True, crop=False)

    def setModel(self):
        self.model = cv2.dnn.readNetFromDarknet(self.cfgFile, self.weightsFile)

        self.layers = self.model.getLayerNames()

        self.outputLayer = [self.layers[layer-1] for layer in self.model.getUnconnectedOutLayers()]

    def predict(self):
        self.model.setInput(self.frameBlob)

        detectionLayers = self.model.forward(self.outputLayer)

        idList = []
        boxList = []
        confidenceList = []

        for detectionLayer in detectionLayers:

            for objectDetection in detectionLayer:

                scores = objectDetection[5:]
                predictedId = np.argmax(scores)
                confidence = scores[predictedId]

                if confidence > 0.60:

                    label = self.labels[predictedId]
                    boundingBox = objectDetection[0:4] * np.array([self.frameWidth, self.frameHeight, self.frameWidth, self.frameHeight])

                    (boxCenter_X, boxCenter_Y, boxWidth, boxHeight) = boundingBox.astype('int')

                    startX = int(boxCenter_X - (boxWidth/2))
                    startY = int(boxCenter_Y - (boxHeight/2))

                    idList.append(predictedId)
                    confidenceList.append(float(confidence))
                    boxList.append([startX, startY, int(boxWidth), int(boxHeight)])

        maxIdList = cv2.dnn.NMSBoxes(boxList, confidenceList, 0.5, 0.4)

        for maxId in maxIdList:
            maxClassId = maxId
            box = boxList[maxClassId]

            startX = box[0]
            startY = box[1]
            boxWidth = box[2]
            boxHeight = box[3]

            predictedId = idList[maxClassId]
            label = self.labels[predictedId]
            confidence = confidenceList[maxClassId]

            endX = startX + boxWidth
            endY = startY + boxHeight


            return (
                label,
                confidence,
                self.boxColor,
                startX,
                startY,
                endX,
                endY
            )