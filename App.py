import sys
import os
import time
import Helper
from threading import Thread
from ServerManager import ServerManager
from ControlServerManager import ControlServerManager
from Handler import Handler
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QDesktopWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QMessageBox
)

from PyQt5.QtCore import QEvent

class Main(QWidget):
    def __init__(self):
        super().__init__()

        config = "config.json"

        self.serverIPAddress, self.serverPort = Helper.Helper.getServerIPandPortFromConfig(config)
        self.controlServerIPAddress, self.controlServerPort = Helper.Helper.getContorlServerIPandPortFromConfig(config)

        self.serverManager = ServerManager(self.serverIPAddress, self.serverPort)
        self.controlServerManager = ControlServerManager(self.controlServerIPAddress, self.controlServerPort)
        self.clientHandler = Handler(self.serverManager)


        self.createImageFolder()

        self.initWidgets()
        self.initLayouts()
        self.setActions()
        self.initUI()

        self.testControlServerConnection()

    def initWidgets(self):
        #ImageView Widget
        self.imageView = QLabel()

        #Server Control Widgets
        self.btnStartServer = QPushButton('Start Server')
        self.btnStopServer = QPushButton('Stop Server')
        self.btnStartServer.setDisabled(True)
        self.btnStopServer.setDisabled(True)

    def initLayouts(self):
        #Layouts Definition
        self.lytMain = QHBoxLayout()
        self.lytControl = QVBoxLayout()
        self.lytServerControl = QHBoxLayout()

        #Connect Layouts

        self.lytServerControl.addWidget(self.btnStartServer)
        self.lytServerControl.addWidget(self.btnStopServer)

        self.lytControl.addLayout(self.lytServerControl)

        self.lytMain.addWidget(self.imageView, stretch= 70)
        self.lytMain.addLayout(self.lytControl)

        self.lytControl.setAlignment(Qt.AlignmentFlag.AlignTop)

    def setActions(self):
        self.btnStartServer.clicked.connect(self.startServer)
        self.btnStopServer.clicked.connect(self.stopServer)

    def initUI(self):
        self.setWindowTitle("Application")
        self.resize(500,300)

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.setLayout(self.lytMain)


    def closeEvent(self, event: QEvent):
        self.stopServer()
        event.accept()


    #Action Methods

    def startServer(self):  
        self.serverManager.startServer()
        time.sleep(0.5)
        Thread(target = self.clientHandler.handleServer, kwargs={"imageView": self.imageView}).start()
        self.btnStartServer.setDisabled(True)
        self.btnStopServer.setEnabled(True)
        
        

    def stopServer(self):
        Thread(target = self.serverManager.stopServer).start()
        time.sleep(0.5)
        self.btnStartServer.setEnabled(True)
        self.btnStopServer.setDisabled(True)

    #Methods

    def createImageFolder(self):
        if not os.path.exists("images"):
            os.mkdir("images")

    def testControlServerConnection(self):
            
        if self.controlServerManager.testConnection():
            self.btnStartServer.setEnabled(True)
        else:
            errorMessage = QMessageBox(self)
            errorMessage.setWindowTitle("Control Server Connection Error")
            errorMessage.setText("Control server connection is not established. Please check your IP Address and Port number in config file and try again.")
            errorMessage.setIcon(QMessageBox.Icon.Critical)
        
            btnQuit = errorMessage.addButton("Quit", QMessageBox.ButtonRole.AcceptRole)

            btnQuit.clicked.connect(lambda: QApplication.quit())

            errorMessage.show()
                

def run():
    app = QApplication(sys.argv)
    mainApp = Main()
    mainApp.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    run()

