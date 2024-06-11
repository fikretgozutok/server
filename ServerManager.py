import socket
from typing import Callable

class ServerManager:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.serverSocket = None
        self.clientSocket = None
        self.clientAddress = None
        self.isRunning = False


    def startServer(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.host, self.port))
        self.serverSocket.listen(1)
        self.isRunning = True
        
        print(f"Listening on {self.host}:{self.port}")

    def acceptClient(self) -> bool:
        connectionStatus = False
        try:
            self.clientSocket, self.clientAddress = self.serverSocket.accept()

            print(f"Client connected: {self.clientAddress}")
            
            connectionStatus = True

        except Exception as e:
            raise e
        finally:
            return connectionStatus

    def handleClient(self, func: Callable[[socket.socket, tuple, dict], None], kwargs):
        if self.isRunning:
            try:
                func(self.clientSocket, self.clientAddress, kwargs)
            except ConnectionResetError as e:
                raise e
            finally:
                self.disconnectClient()



    def disconnectClient(self):
        if(self.clientSocket and self.clientAddress):
            self.clientSocket.close()

            self.clientSocket = None
            self.clientAddress = None

            print("Disconnected")
        else:
            raise Exception("There is no connected client!")


    def stopServer(self):
        try:
            if(self.isRunning and self.serverSocket != None):
            
                if(self.clientSocket):
                    self.clientSocket.close()
                
                self.serverSocket.close()
                self.isRunning = False

                print("Server stopped!")

        except Exception as e:
            raise e
        
