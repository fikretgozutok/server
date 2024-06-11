import socket
import time


class ControlServerManager:
    def __init__(self, host: str, port: int, bufferSize: int = 1024):
        self.host = host
        self.port = port
        self.bufferSize = bufferSize

        self.isConnected = False

        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __enter__(self) -> 'ControlServerManager':
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        pass


    def connect(self) -> bool:
        try:
            self.serverSocket.connect((self.host, self.port))
            self.isConnected = True
        except:
            pass
        finally:
            return self.isConnected
        
    def write(self, data: str):
        self.serverSocket.sendall(data.encode(encoding="utf-8"))

    def disconnect(self):
        try:
            self.serverSocket.close()
            self.isConnected = False
        except:
            raise Exception("Not connected!")
        
      
    def stopServer(self):
        try:
            self.serverSocket.connect((self.host, self.port))
            time.sleep(0.5)
            self.write("SDOWN")
            time.sleep(0.5)
            self.disconnect()
        except Exception as e:
            raise e
        
        
    def testConnection(self) -> bool:
        testResult = False
        try:
            self.serverSocket.connect((self.host, self.port))
            time.sleep(0.5)
            self.write("TEST")
            time.sleep(0.5)
            if self.serverSocket.recv(self.bufferSize) == b"OK":
                testResult = True
            time.sleep(0.5)
            self.disconnect()
        except Exception as e:
            raise e
        finally:
            return testResult
        
        
    